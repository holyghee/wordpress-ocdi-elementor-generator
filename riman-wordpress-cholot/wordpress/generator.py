import yaml
import json
import copy
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# (Die TEMPLATES und HYDRATORS Sektionen bleiben die gleichen wie zuvor)
# HINWEIS: Fügen Sie hier die vollständigen Templates und Hydrator-Funktionen 
# aus dem vorherigen Skript ein, damit das Skript vollständig ist.
TEMPLATES = {
    "hero_slider_mountains_divider": {
        "id": "placeholder_id", "elType": "section", "settings": {"gap": "no", "layout": "full_width"},
        "elements": [{"id": "placeholder_id", "elType": "column", "elements": [{"id": "placeholder_id", "elType": "widget", "widgetType": "rdn-slider", "settings": {"slider_list": []}}]}]
    },
    "service_card_container": {
        "id": "placeholder_id", "elType": "section", "settings": {"structure": "30", "margin": {"unit": "px", "top": "-100"}},
        "elements": []
    },
    "service_card_item": {
        "id": "placeholder_id", "elType": "column", "settings": {"_column_size": 33, "animation": "fadeInUp"},
        "elements": [
            {"id": "placeholder_id", "elType": "section", "isInner": True, "elements": [{"id": "placeholder_id", "elType": "column", "elements": [{"id": "placeholder_id", "elType": "widget", "widgetType": "image", "settings": {"image": {"url": ""}}}]}]},
            {"id": "placeholder_id", "elType": "section", "isInner": True, "elements": [{"id": "placeholder_id", "elType": "column", "elements": [{"id": "placeholder_id", "elType": "widget", "widgetType": "cholot-texticon", "settings": {"selected_icon": {"value": ""}, "subtitle": "", "title": "", "text": ""}}]}]}
        ]
    }
}

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
    if not items: return container
    column_size = 100 / len(items)
    if len(items) == 3: container["settings"]["structure"] = "30"
    elif len(items) == 4: container["settings"]["structure"] = "25"
    
    for i, item_data in enumerate(items):
        item_template = copy.deepcopy(TEMPLATES["service_card_item"])
        item_template["settings"]["_column_size"] = column_size
        item_template["settings"]["animation_delay"] = i * 200
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

def generate_wxr_xml(yaml_data):
    """
    Erstellt die vollständige WXR-XML-Datei.
    """
    page_config = yaml_data.get("page", {})
    meta_config = yaml_data.get("page_meta", {})
    
    # 1. Generiere die Elementor-JSON-Daten
    elementor_json_data = generate_elementor_json(page_config)
    elementor_json_string = json.dumps(elementor_json_data, ensure_ascii=False)

    # 2. Registriere die XML-Namensräume (KORREKTUR HIER)
    ET.register_namespace('excerpt', "http://wordpress.org/export/1.2/excerpt/")
    ET.register_namespace('content', "http://purl.org/rss/1.0/modules/content/")
    ET.register_namespace('wfw', "http://wellformedweb.org/CommentAPI/")
    ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")
    ET.register_namespace('wp', "http://wordpress.org/export/1.2/")

    # 3. Erstelle die XML-Grundstruktur
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    # ... (Rest der XML-Erstellung bleibt gleich)
    ET.SubElement(channel, "title").text = "Cholot Export"
    author = ET.SubElement(channel, "{http://wordpress.org/export/1.2/}author")
    ET.SubElement(author, "{http://wordpress.org/export/1.2/}author_login").text = meta_config.get("author_login", "admin")
    
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = page_config.get("name", "Unbenannte Seite")
    ET.SubElement(item, "{http://purl.org/dc/elements/1.1/}creator").text = meta_config.get("author_login", "admin")
    ET.SubElement(item, "{http://wordpress.org/export/1.2/}post_type").text = "page"
    ET.SubElement(item, "{http://wordpress.org/export/1.2/}status").text = "publish"

    postmeta_elementor = ET.SubElement(item, "{http://wordpress.org/export/1.2/}postmeta")
    ET.SubElement(postmeta_elementor, "{http://wordpress.org/export/1.2/}meta_key").text = "_elementor_data"
    ET.SubElement(postmeta_elementor, "{http://wordpress.org/export/1.2/}meta_value").text = f"<![CDATA[{elementor_json_string}]]>"
    
    postmeta_template = ET.SubElement(item, "{http://wordpress.org/export/1.2/}postmeta")
    ET.SubElement(postmeta_template, "{http://wordpress.org/export/1.2/}meta_key").text = "_wp_page_template"
    ET.SubElement(postmeta_template, "{http://wordpress.org/export/1.2/}meta_value").text = "elementor_canvas"

    postmeta_edit_mode = ET.SubElement(item, "{http://wordpress.org/export/1.2/}postmeta")
    ET.SubElement(postmeta_edit_mode, "{http://wordpress.org/export/1.2/}meta_key").text = "_elementor_edit_mode"
    ET.SubElement(postmeta_edit_mode, "{http://wordpress.org/export/1.2/}meta_value").text = "builder"

    # 4. XML in einen String konvertieren und formatieren
    rough_string = ET.tostring(rss, 'utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_string)
    
    # Workaround, um CDATA-Escaping durch minidom zu verhindern
    meta_values = reparsed.getElementsByTagName("wp:meta_value")
    for mv in meta_values:
        if "<![CDATA[" in mv.firstChild.nodeValue:
            mv.firstChild.nodeValue = elementor_json_string

    return reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode()

# --- HAUPT-SKRIPT ---
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
