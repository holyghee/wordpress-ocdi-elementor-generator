import yaml
import json
import copy
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# =============================================================================
# BLOCK-TEMPLATE BIBLIOTHEK
# =============================================================================

TEMPLATES = {
    "hero_slider_mountains_divider": {
        "id": "placeholder_id_section_hero",
        "elType": "section",
        "settings": {
            "gap": "no", "layout": "full_width", "background_color": "rgba(0,0,0,0.6)",
            "shape_divider_bottom": "mountains", "shape_divider_bottom_color": "#ffffff"
        },
        "elements": [{
            "id": "placeholder_id_col_hero", "elType": "column", "settings": {"_column_size": 100},
            "elements": [{
                "id": "placeholder_id_widget_hero", "elType": "widget", "widgetType": "rdn-slider",
                "settings": { "slider_list": [] }
            }]
        }]
    },
    "service_card_container": {
        "id": "placeholder_id_section_cards",
        "elType": "section",
        "settings": {
            "gap": "extended", "structure": "30", "background_color": "#b68c2f",
            "margin": {"unit": "px", "top": "-100", "right": 0, "bottom": 0, "left": 0, "isLinked": False}
        },
        "elements": []
    },
    "service_card_item": {
        "id": "placeholder_id_col_card",
        "elType": "column",
        "settings": { "_column_size": 33, "animation": "fadeInUp", "animation_delay": 0 },
        "elements": [
            {
                "id": "placeholder_id_inner_sec_img", "elType": "section", "isInner": True,
                "settings": {"shape_divider_bottom": "curve", "shape_divider_bottom_negative": "yes"},
                "elements": [{"id": "placeholder_id_inner_col_img", "elType": "column", "settings": {"_column_size": 100},
                    "elements": [{"id": "placeholder_id_widget_img", "elType": "widget", "widgetType": "image", "settings": {"image": {"url": ""}}}]
                }]
            },
            {
                "id": "placeholder_id_inner_sec_text", "elType": "section", "isInner": True,
                "settings": {"z_index": 2, "margin": {"unit": "px", "top": "-30", "right": 0, "bottom": 0, "left": 0, "isLinked": False}},
                "elements": [{"id": "placeholder_id_inner_col_text", "elType": "column", "settings": {"_column_size": 100},
                    "elements": [{"id": "placeholder_id_widget_texticon", "elType": "widget", "widgetType": "cholot-texticon",
                        "settings": {"selected_icon": {"value": "", "library": "fa-solid"}, "subtitle": "", "title": "", "text": ""}
                    }]
                }]
            }
        ]
    }
}

# =============================================================================
# HYDRATIONS-FUNKTIONEN
# =============================================================================

def hydrate_hero_slider(config):
    template = copy.deepcopy(TEMPLATES["hero_slider_mountains_divider"])
    slider_widget = template["elements"][0]["elements"][0]
    for slide_data in config.get("slides", []):
        slide = {
            "title": slide_data.get("title", ""), "subtitle": slide_data.get("subtitle", ""),
            "text": slide_data.get("text", ""), "btn_text": slide_data.get("button_text", ""),
            "btn_link": {"url": slide_data.get("button_link", "#")},
            "image": {"url": slide_data.get("background_image_url", "")}
        }
        slider_widget["settings"]["slider_list"].append(slide)
    return template

def hydrate_service_cards(config):
    container = copy.deepcopy(TEMPLATES["service_card_container"])
    items = config.get("items", [])
    if not items:
        return container
    
    num_items = len(items)
    if num_items == 4:
        container["settings"]["structure"] = "25"
    elif num_items == 2:
        container["settings"]["structure"] = "50"
    else:
        container["settings"]["structure"] = "30"
    
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
    "hero_slider_mountains_divider": hydrate_hero_slider,
    "service_card_curved_image": hydrate_service_cards,
}

def generate_elementor_json(page_config):
    elementor_data = []
    for section_config in page_config.get("sections", []):
        section_type = section_config.get("type")
        if section_type in HYDRATORS:
            hydrated_section = HYDRATORS[section_type](section_config.get("config", {}))
            elementor_data.append(hydrated_section)
    return elementor_data

# =============================================================================
# XML-GENERATOR
# =============================================================================

def generate_wxr_xml(yaml_data):
    page_config = yaml_data.get("page", {})
    meta_config = yaml_data.get("page_meta", {})
    elementor_json_string = json.dumps(generate_elementor_json(page_config), ensure_ascii=False)

    root = ET.Element("rss", version="2.0", 
                      attrib={"xmlns:wp": "http://wordpress.org/export/1.2/",
                              "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
                              "xmlns:dc": "http://purl.org/dc/elements/1.1/"})
    channel = ET.SubElement(root, "channel")
    
    ET.SubElement(channel, "{http://wordpress.org/export/1.2/}wxr_version").text = "1.2"
    
    author = ET.SubElement(channel, "{http://wordpress.org/export/1.2/}author")
    ET.SubElement(author, "{http://wordpress.org/export/1.2/}author_login").text = meta_config.get("author_login", "admin")
    ET.SubElement(author, "{http://wordpress.org/export/1.2/}author_email").text = meta_config.get("author_email", "admin@example.com")
    ET.SubElement(author, "{http://wordpress.org/export/1.2/}author_display_name").text = meta_config.get("author_display_name", "Admin")

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = page_config.get("name", "Generated Page")
    ET.SubElement(item, "{http://purl.org/dc/elements/1.1/}creator").text = meta_config.get("author_login", "admin")
    ET.SubElement(item, "{http://wordpress.org/export/1.2/}post_type").text = "page"
    ET.SubElement(item, "{http://wordpress.org/export/1.2/}status").text = "publish"
    
    postmeta = ET.SubElement(item, "{http://wordpress.org/export/1.2/}postmeta")
    ET.SubElement(postmeta, "{http://wordpress.org/export/1.2/}meta_key").text = "_elementor_data"
    ET.SubElement(postmeta, "{http://wordpress.org/export/1.2/}meta_value").text = elementor_json_string

    postmeta2 = ET.SubElement(item, "{http://wordpress.org/export/1.2/}postmeta")
    ET.SubElement(postmeta2, "{http://wordpress.org/export/1.2/}meta_key").text = "_wp_page_template"
    ET.SubElement(postmeta2, "{http://wordpress.org/export/1.2/}meta_value").text = "elementor_canvas"
    
    postmeta3 = ET.SubElement(item, "{http://wordpress.org/export/1.2/}postmeta")
    ET.SubElement(postmeta3, "{http://wordpress.org/export/1.2/}meta_key").text = "_elementor_edit_mode"
    ET.SubElement(postmeta3, "{http://wordpress.org/export/1.2/}meta_value").text = "builder"

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode()

# =============================================================================
# SKRIPT-AUSFÜHRUNG
# =============================================================================

if __name__ == "__main__":
    try:
        with open("config.yaml", "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
        
        final_xml_structure = generate_wxr_xml(config_data)
        
        output_filename = "elementor_export.xml"
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(final_xml_structure)
            
        print(f"\n✅ Erfolgreich! Die WordPress-XML-Datei wurde in '{output_filename}' gespeichert.")
        
    except FileNotFoundError:
        print("FEHLER: Die Datei 'config.yaml' wurde nicht gefunden. Bitte erstellen Sie sie.")
    except Exception as e:
