import yaml
import json
import copy
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import random
import string

# =============================================================================
# BLOCK-TEMPLATE BIBLIOTHEK (Auszug aus der Analyse)
# =============================================================================

TEMPLATES = {
    "hero_slider": json.loads('{"id":"6e7b57b","elType":"section","settings":{"gap":"no","layout":"full_width","shape_divider_bottom_color":"#ffffff","shape_divider_bottom_width":{"unit":"%","size":105},"shape_divider_bottom_height":{"unit":"px","size":88},"shape_divider_bottom_above_content":"yes"},"elements":[{"id":"9f1e17d","elType":"column","settings":{"_column_size":100},"elements":[{"id":"1b7b0e1","elType":"widget","widgetType":"rdn-slider","settings":{"slider_list":[],"align":"left","title_typo_typography":"custom","title_typo_font_size":{"unit":"px","size":45},"title_typo_font_weight":"700","subtitle_typo_typography":"custom","subtitle_typo_font_weight":"700","slider_mask":"rgba(0,0,0,0.85)","title_typo_font_family":"Playfair Display","subtitle_typo_text_transform":"uppercase","subtitle_color":"#b68c2f","title_color":"#ffffff","span_title_typo_typography":"custom","span_title_typo_font_weight":"200","span_title_typo_font_style":"italic","span_title_color":"#ffffff"}}]}]}'),
    "service_card_container": json.loads('{"id":"a7c3b2d","elType":"section","settings":{"structure":"30","margin":{"unit":"px","top":"-100","right":0,"bottom":"60","left":0,"isLinked":false},"background_color":"#b68c2f"},"elements":[]}'),
    "service_card_item": json.loads('{"id":"d1e2f3a","elType":"column","settings":{"_column_size":33,"animation":"fadeInUp"},"elements":[{"id":"b4c5d6e","elType":"section","isInner":true,"settings":{"shape_divider_bottom":"curve","shape_divider_bottom_color":"#fafafa","shape_divider_bottom_negative":"yes"},"elements":[{"id":"f7e8d9c","elType":"column","settings":{"_column_size":100},"elements":[{"id":"a1b2c3d","elType":"widget","widgetType":"image","settings":{"image":{"url":""}}}]}]},{"id":"e4f5a6b","elType":"section","isInner":true,"settings":{"z_index":2,"margin":{"unit":"px","top":"-30"}},"elements":[{"id":"c7d8e9f","elType":"column","settings":{"_column_size":100},"elements":[{"id":"b1a2c3d","elType":"widget","widgetType":"cholot-texticon","settings":{"subtitle":"","title":"","text":"","selected_icon":{"library":"fa-solid","value":""},"subtitle_color":"#b68c2f","icon_color":"#ffffff","iconbg_color":"#b68c2f","_border_border":"dashed","_border_color":"#b68c2f","icon_bordering_color":"#fafafa"}}]}]}]}')
}

# =============================================================================
# HELPER-FUNKTIONEN
# =============================================================================

def generate_random_id(length=7):
    return ''.join(random.choices(string.hexdigits.lower(), k=length))

def update_ids(element):
    if isinstance(element, dict):
        if 'id' in element:
            element['id'] = generate_random_id()
        for key, value in element.items():
            update_ids(value)
    elif isinstance(element, list):
        for item in element:
            update_ids(item)

def find_widget_types(elements, usage_dict):
    for element in elements:
        if element.get('widgetType'):
            widget_type = element['widgetType']
            usage_dict[widget_type] = usage_dict.get(widget_type, 0) + 1
        if 'elements' in element and element['elements']:
            find_widget_types(element['elements'], usage_dict)

# =============================================================================
# HYDRATIONS-FUNKTIONEN
# =============================================================================

def hydrate_hero_slider(config):
    template = copy.deepcopy(TEMPLATES["hero_slider"])
    slider_widget = template["elements"][0]["elements"][0]
    for slide_data in config.get("slides", []):
        slide = {
            "title": slide_data.get("title", ""), "subtitle": slide_data.get("subtitle", ""),
            "image": {"url": slide_data.get("background_image_url", "")}
        }
        slider_widget["settings"]["slider_list"].append(slide)
    return template

def hydrate_service_cards(config):
    container = copy.deepcopy(TEMPLATES["service_card_container"])
    items = config.get("items", [])
    if not items: return container
    
    animation_delay_step = 200
    for i, item_data in enumerate(items):
        item_template = copy.deepcopy(TEMPLATES["service_card_item"])
        item_template["settings"]["animation_delay"] = i * animation_delay_step
        
        image_widget = item_template["elements"][0]["elements"][0]["elements"][0]
        texticon_widget = item_template["elements"][1]["elements"][0]["elements"][0]
        
        image_widget["settings"]["image"]["url"] = item_data.get("image_url", "")
        texticon_widget["settings"]["selected_icon"]["value"] = item_data.get("icon", "")
        texticon_widget["settings"]["subtitle"] = item_data.get("subtitle", "")
        texticon_widget["settings"]["title"] = item_data.get("title", "")
        texticon_widget["settings"]["text"] = f"<p>{item_data.get('description', '')}</p>"
        
        container["elements"].append(item_template)
    return container

HYDRATORS = {
    "hero_slider": hydrate_hero_slider,
    "service_cards": hydrate_service_cards,
}

# =============================================================================
# XML-GENERATOR
# =============================================================================

def generate_wxr_xml(yaml_data):
    page_config = yaml_data.get("page", {})
    meta_config = yaml_data.get("page_meta", {})
    
    elementor_data = []
    for section_config in page_config.get("sections", []):
        section_type = section_config.get("type")
        if section_type in HYDRATORS:
            hydrated_section = HYDRATORS[section_type](section_config.get("config", {}))
            update_ids(hydrated_section)
            elementor_data.append(hydrated_section)
            
    elementor_json_string = json.dumps(elementor_data, ensure_ascii=False)

    # Dynamisch _elementor_elements_usage erstellen
    usage = {}
    find_widget_types(elementor_data, usage)
    
    # XML Aufbau
    root = ET.Element("rss", version="2.0", 
                      attrib={"xmlns:wp": "http://wordpress.org/export/1.2/",
                              "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
                              "xmlns:dc": "http://purl.org/dc/elements/1.1/"})
    channel = ET.SubElement(root, "channel")
    
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = page_config.get("name")
    ET.SubElement(item, "link").text = f"{meta_config.get('base_site_url')}/{page_config.get('slug')}/"
    ET.SubElement(item, "wp:post_id").text = str(page_config.get("id"))
    ET.SubElement(item, "wp:post_date").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ET.SubElement(item, "wp:post_name").text = page_config.get("slug")
    ET.SubElement(item, "wp:post_type").text = "page"
    ET.SubElement(item, "wp:status").text = "publish"
    ET.SubElement(item, "content:encoded").text = f"<!-- wp:elementor {elementor_json_string} /-->"

    # Essenzielle Meta-Felder hinzufügen
    meta_fields = {
        "_elementor_data": elementor_json_string,
        "_elementor_version": "3.18.3",
        "_elementor_edit_mode": "builder",
        "_wp_page_template": "elementor_header_footer",
        "_elementor_page_settings": "a:0:{}", # WICHTIG: Korrekt serialisiertes leeres Array
        "_elementor_elements_usage": json.dumps(usage) # WICHTIG: Dynamisch generiert
    }

    for key, value in meta_fields.items():
        postmeta = ET.SubElement(item, "wp:postmeta")
        ET.SubElement(postmeta, "wp:meta_key").text = key
        ET.SubElement(postmeta, "wp:meta_value").text = f"<![CDATA[{value}]]>"

    rough_string = ET.tostring(root, 'utf-8', xml_declaration=True).decode()
    return minidom.parseString(rough_string).toprettyxml(indent="  ")

# =============================================================================
# SKRIPT-AUSFÜHRUNG
# =============================================================================

if __name__ == "__main__":
    try:
        with open("config.yaml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        final_xml = generate_wxr_xml(config)
        
        output_filename = "complete_riman_export.xml"
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(final_xml)
            
        print(f"\n✅ Erfolgreich! Die WordPress-XML-Datei wurde in '{output_filename}' gespeichert.")
        
    except FileNotFoundError:
        print("FEHLER: Die Datei 'config.yaml' wurde nicht gefunden.")
    except Exception as e:
