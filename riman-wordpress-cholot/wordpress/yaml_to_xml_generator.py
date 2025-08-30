#!/usr/bin/env python3
"""
YAML zu WordPress XML Generator für Elementor
Basierend auf Geminis Analyse und erweitert für vollständige XML-Generierung
"""

import yaml
import json
import copy
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime
import xml.dom.minidom as minidom

class YamlToWordPressXML:
    def __init__(self):
        self.init_templates()
        self.init_design_tokens()
        
    def init_design_tokens(self):
        """Standard Design-Tokens (können durch YAML überschrieben werden)"""
        self.design_tokens = {
            'colors': {
                'primary': '#b68c2f',
                'text_dark': '#000000',
                'text_light': '#ffffff',
                'background_light': '#fafafa',
                'background_dark': '#1f1f1f'
            },
            'typography': {
                'font_heading': 'Playfair Display',
                'font_body': 'Source Sans Pro'
            }
        }
    
    def init_templates(self):
        """Initialisiert die Block-Templates basierend auf der Cholot-Struktur"""
        self.templates = {
            'service_card_container': {
                "elType": "section",
                "settings": {
                    "gap": "extended",
                    "custom_height": {"unit": "px", "size": 300, "sizes": []},
                    "content_position": "middle",
                    "structure": "30",
                    "background_color": "{{colors.primary}}",
                    "box_shadow_box_shadow": {
                        "horizontal": 10,
                        "vertical": 0,
                        "blur": 0,
                        "spread": 4,
                        "color": "#ededed"
                    },
                    "margin": {"unit": "px", "top": -100, "right": 0, "bottom": 0, "left": 0, "isLinked": False}
                },
                "elements": [],
                "isInner": False
            },
            'service_card_item': {
                "elType": "column",
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None,
                    "background_background": "classic",
                    "background_color": "{{colors.background_light}}",
                    "border_width": {"unit": "px", "top": 10, "right": 0, "bottom": 10, "left": 10, "isLinked": False},
                    "border_color": "#ededed",
                    "animation": "fadeInUp",
                    "animation_duration": "fast"
                },
                "elements": [],
                "isInner": False
            }
        }
    
    def generate_id(self):
        """Generiert eine unique ID für Elementor-Elemente"""
        return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:7]
    
    def apply_design_tokens(self, element, tokens):
        """Ersetzt Platzhalter mit Design-Token-Werten"""
        if isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                    token_path = value.strip(" {}").split('.')
                    resolved_value = tokens
                    for part in token_path:
                        resolved_value = resolved_value.get(part, value)
                    element[key] = resolved_value
                else:
                    self.apply_design_tokens(value, tokens)
        elif isinstance(element, list):
            for item in element:
                self.apply_design_tokens(item, tokens)
        return element
    
    def generate_service_card(self, card_data, index):
        """Generiert eine einzelne Service-Card mit Cholot-Struktur"""
        card = {
            "id": self.generate_id(),
            "elType": "column",
            "settings": {
                "_column_size": 33,
                "background_color": "#fafafa",
                "border_width": {"unit": "px", "top": 10, "right": 0, "bottom": 10, "left": 10, "isLinked": False},
                "border_color": "#ededed",
                "animation": "fadeInUp",
                "animation_delay": index * 200
            },
            "elements": [
                # Inner Section 1: Bild mit Shape Divider
                {
                    "id": self.generate_id(),
                    "elType": "section",
                    "settings": {
                        "gap": "no",
                        "shape_divider_bottom": "curve",
                        "shape_divider_bottom_color": "#fafafa",
                        "shape_divider_bottom_negative": "yes",
                        "shape_divider_bottom_above_content": "yes"
                    },
                    "elements": [{
                        "id": self.generate_id(),
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [{
                            "id": self.generate_id(),
                            "elType": "widget",
                            "settings": {
                                "image": {"url": card_data.get('image', ''), "id": ""},
                                "_border_width": {"unit": "px", "top": 4, "right": 0, "bottom": 0, "left": 0},
                                "_border_color": "{{colors.primary}}"
                            },
                            "elements": [],
                            "widgetType": "image"
                        }],
                        "isInner": True
                    }],
                    "isInner": True
                },
                # Inner Section 2: cholot-texticon
                {
                    "id": self.generate_id(),
                    "elType": "section",
                    "settings": {
                        "gap": "no",
                        "margin": {"unit": "px", "top": -30, "right": 0, "bottom": 0, "left": 0},
                        "z_index": 2
                    },
                    "elements": [{
                        "id": self.generate_id(),
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [{
                            "id": self.generate_id(),
                            "elType": "widget",
                            "settings": {
                                "title": card_data.get('title', ''),
                                "subtitle": card_data.get('subtitle', ''),
                                "text": f"<p>{card_data.get('text', '')}</p>",
                                "selected_icon": {
                                    "value": card_data.get('icon', 'fas fa-star'),
                                    "library": "fa-solid"
                                },
                                "icon_color": "#ffffff",
                                "iconbg_color": "{{colors.primary}}",
                                "subtitle_color": "{{colors.primary}}",
                                "_border_color": "{{colors.primary}}",
                                "_border_border": "dashed",
                                "_padding": {"unit": "px", "top": 30, "right": 30, "bottom": 30, "left": 30}
                            },
                            "elements": [],
                            "widgetType": "cholot-texticon"
                        }],
                        "isInner": True
                    }],
                    "isInner": True
                }
            ],
            "isInner": False
        }
        return card
    
    def generate_service_cards_section(self, config, tokens):
        """Generiert die komplette Service-Cards Section"""
        container = copy.deepcopy(self.templates['service_card_container'])
        container['id'] = self.generate_id()
        
        items = config.get('items', [])
        for i, item in enumerate(items):
            card = self.generate_service_card(item, i)
            card = self.apply_design_tokens(card, tokens)
            container['elements'].append(card)
        
        container = self.apply_design_tokens(container, tokens)
        return container
    
    def generate_hero_slider(self, config, tokens):
        """Generiert Hero Slider Section"""
        slider_section = {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "gap": "no",
                "layout": "full_width",
                "background_color": "rgba(0,0,0,0.6)",
                "shape_divider_bottom": "mountains",
                "shape_divider_bottom_color": "#ffffff",
                "shape_divider_bottom_width": {"unit": "%", "size": 105},
                "shape_divider_bottom_height": {"unit": "px", "size": 88}
            },
            "elements": [{
                "id": self.generate_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_id(),
                    "elType": "widget",
                    "settings": {
                        "slider_list": [
                            {
                                "_id": self.generate_id(),
                                "title": slide.get('title', ''),
                                "subtitle": slide.get('subtitle', ''),
                                "text": slide.get('text', ''),
                                "btn_text": slide.get('button_text', ''),
                                "btn_link": {"url": slide.get('button_link', '#')},
                                "image": {"url": slide.get('background_image', ''), "id": ""}
                            }
                            for slide in config.get('slides', [])
                        ]
                    },
                    "elements": [],
                    "widgetType": "rdn-slider"
                }]
            }],
            "isInner": False
        }
        return self.apply_design_tokens(slider_section, tokens)
    
    def generate_elementor_data(self, yaml_config):
        """Hauptfunktion zur Generierung der Elementor-Daten"""
        page_config = yaml_config.get('page', {})
        design_tokens = yaml_config.get('design_system', self.design_tokens)
        
        elementor_data = []
        
        for section in page_config.get('sections', []):
            section_type = section.get('type')
            section_config = section.get('config', {})
            
            if section_type == 'hero_slider':
                elementor_data.append(self.generate_hero_slider(section_config, design_tokens))
            elif section_type == 'service_cards':
                elementor_data.append(self.generate_service_cards_section(section_config, design_tokens))
            # Weitere Section-Types können hier hinzugefügt werden
        
        return elementor_data
    
    def generate_wordpress_xml(self, yaml_config):
        """Generiert komplettes WordPress XML"""
        # Root Element
        rss = ET.Element('rss', version='2.0')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        channel = ET.SubElement(rss, 'channel')
        
        # Channel Meta
        ET.SubElement(channel, 'title').text = yaml_config.get('company', {}).get('name', 'Website')
        ET.SubElement(channel, 'link').text = 'http://localhost:8081'
        ET.SubElement(channel, 'description').text = yaml_config.get('company', {}).get('tagline', '')
        ET.SubElement(channel, 'language').text = 'de-DE'
        ET.SubElement(channel, 'wp:wxr_version').text = '1.2'
        
        # Page Item
        item = ET.SubElement(channel, 'item')
        page_config = yaml_config.get('page', {})
        
        ET.SubElement(item, 'title').text = page_config.get('name', 'Homepage')
        ET.SubElement(item, 'wp:post_id').text = '3000'
        ET.SubElement(item, 'wp:post_type').text = 'page'
        ET.SubElement(item, 'wp:status').text = 'publish'
        
        # Elementor Data als Postmeta
        elementor_data = self.generate_elementor_data(yaml_config)
        
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_data'
        ET.SubElement(postmeta, 'wp:meta_value').text = json.dumps(elementor_data, ensure_ascii=False)
        
        postmeta2 = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta2, 'wp:meta_key').text = '_elementor_version'
        ET.SubElement(postmeta2, 'wp:meta_value').text = '3.18.3'
        
        postmeta3 = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta3, 'wp:meta_key').text = '_elementor_edit_mode'
        ET.SubElement(postmeta3, 'wp:meta_value').text = 'builder'
        
        # XML String formatieren
        xml_string = ET.tostring(rss, encoding='unicode')
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")

def main():
    # YAML laden
    with open('config_riman.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Generator initialisieren
    generator = YamlToWordPressXML()
    
    # XML generieren
    xml_content = generator.generate_wordpress_xml(config)
    
    # XML speichern
    with open('riman_generated.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ WordPress XML erfolgreich generiert: riman_generated.xml")
    
    # Auch JSON für Debugging speichern
    elementor_data = generator.generate_elementor_data(config)
    with open('riman_elementor_data.json', 'w', encoding='utf-8') as f:
        json.dump(elementor_data, f, indent=2, ensure_ascii=False)
    
    print("💾 Elementor Daten auch als JSON gespeichert: riman_elementor_data.json")

if __name__ == "__main__":
    main()