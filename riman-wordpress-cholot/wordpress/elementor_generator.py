#!/usr/bin/env python3
"""
Elementor Generator - YAML to Elementor JSON/XML
Generiert komplette Elementor-Seiten aus einfachen YAML-Konfigurationen
unter Verwendung der Cholot Theme Design-Elemente
"""

import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import re

class ElementorGenerator:
    """Hauptklasse für die Generierung von Elementor-Inhalten"""
    
    def __init__(self, theme_library_path: str = "cholot_theme_library"):
        self.theme_library_path = Path(theme_library_path)
        self.element_library = {}
        self.widget_library = {}
        self.load_theme_library()
        
    def load_theme_library(self):
        """Lädt die Cholot Theme Element-Bibliothek"""
        # Cholot Theme Elemente als wiederverwendbare Komponenten
        self.element_library = {
            # Hero Slider mit Video Background
            "hero_slider": {
                "type": "section",
                "widget": "rdn-slider",
                "base_structure": {
                    "elType": "section",
                    "settings": {
                        "stretch_section": "section-stretched",
                        "layout": "full_width"
                    },
                    "elements": [{
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [{
                            "elType": "widget",
                            "widgetType": "rdn-slider",
                            "settings": {}
                        }]
                    }]
                }
            },
            
            # Service Card mit Bild und Curved Shape
            "service_card": {
                "type": "column",
                "base_structure": {
                    "elType": "column",
                    "settings": {
                        "_column_size": 33,
                        "background_background": "classic",
                        "animation": "fadeInUp"
                    },
                    "elements": [
                        {
                            "elType": "section",
                            "isInner": True,
                            "settings": {
                                "structure": "10",
                                "background_background": "classic",
                                "shape_divider_bottom": "curve",
                                "shape_divider_bottom_negative": "yes",
                                "shape_divider_bottom_color": "#FFFFFF",
                                "gap": "no",
                                "padding": {"unit": "px", "top": 150, "bottom": 50}
                            },
                            "elements": [{
                                "elType": "column",
                                "settings": {"_column_size": 100},
                                "elements": []
                            }]
                        },
                        {
                            "elType": "section",
                            "isInner": True,
                            "settings": {
                                "structure": "10",
                                "background_background": "classic",
                                "background_color": "#FFFFFF",
                                "gap": "no",
                                "padding": {"unit": "px", "top": 30, "bottom": 40, "left": 30, "right": 30}
                            },
                            "elements": [{
                                "elType": "column",
                                "settings": {"_column_size": 100},
                                "elements": [{
                                    "elType": "widget",
                                    "widgetType": "cholot-texticon",
                                    "settings": {}
                                }]
                            }]
                        }
                    ]
                }
            },
            
            # Testimonial Carousel
            "testimonial_carousel": {
                "type": "section",
                "widget": "testimonial-carousel",
                "base_structure": {
                    "elType": "section",
                    "settings": {
                        "background_background": "classic",
                        "background_color": "#f8f8f8"
                    },
                    "elements": [{
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [{
                            "elType": "widget",
                            "widgetType": "testimonial-carousel",
                            "settings": {}
                        }]
                    }]
                }
            },
            
            # Contact Form Section
            "contact_form": {
                "type": "section",
                "base_structure": {
                    "elType": "section",
                    "settings": {
                        "background_background": "classic",
                        "background_color": "#1a1a1a",
                        "padding": {"unit": "px", "top": 80, "bottom": 80}
                    },
                    "elements": [{
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [
                            {
                                "elType": "widget",
                                "widgetType": "heading",
                                "settings": {
                                    "title": "Kontakt",
                                    "align": "center",
                                    "title_color": "#ffffff"
                                }
                            },
                            {
                                "elType": "widget",
                                "widgetType": "shortcode",
                                "settings": {
                                    "shortcode": "[contact-form-7 id=\"FORM_ID\" title=\"Contact form 1\"]"
                                }
                            }
                        ]
                    }]
                }
            },
            
            # Text mit Icon (Cholot Custom Widget)
            "text_icon": {
                "type": "widget",
                "base_structure": {
                    "elType": "widget",
                    "widgetType": "cholot-texticon",
                    "settings": {
                        "selected_icon": {"value": "fas fa-shield-alt", "library": "fa-solid"},
                        "icon_color": "#b68c2f",
                        "subtitle_color": "#b68c2f",
                        "title_color": "#1f1f1f",
                        "text_color": "#666666"
                    }
                }
            }
        }
    
    def generate_unique_id(self, prefix: str = "") -> str:
        """Generiert eine eindeutige ID für Elementor-Elemente"""
        timestamp = datetime.now().isoformat()
        hash_obj = hashlib.md5(f"{prefix}{timestamp}".encode())
        return hash_obj.hexdigest()[:7]
    
    def process_yaml_config(self, yaml_file: str) -> Dict:
        """Verarbeitet YAML-Konfiguration und generiert Elementor-Struktur"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pages = []
        
        for page_config in config.get('pages', []):
            page_data = self.generate_page(page_config)
            pages.append(page_data)
        
        return {
            'site_info': config.get('site_info', {}),
            'pages': pages,
            'menus': config.get('menus', []),
            'settings': config.get('settings', {})
        }
    
    def generate_page(self, page_config: Dict) -> Dict:
        """Generiert eine komplette Seite aus der Konfiguration"""
        sections = []
        
        for section_config in page_config.get('sections', []):
            section = self.generate_section(section_config)
            if section:
                sections.append(section)
        
        elementor_data = json.dumps(sections)
        
        return {
            'title': page_config.get('title', 'Untitled'),
            'slug': page_config.get('slug', ''),
            'template': page_config.get('template', 'elementor_header_footer'),
            'elementor_data': elementor_data,
            'elementor_version': '3.18.3',
            'elementor_edit_mode': 'builder'
        }
    
    def generate_section(self, section_config: Dict) -> Optional[Dict]:
        """Generiert eine Section basierend auf Typ und Konfiguration"""
        section_type = section_config.get('type')
        
        if section_type == 'hero':
            return self.generate_hero_section(section_config)
        elif section_type == 'service_cards':
            return self.generate_service_cards_section(section_config)
        elif section_type == 'testimonials':
            return self.generate_testimonial_section(section_config)
        elif section_type == 'contact':
            return self.generate_contact_section(section_config)
        elif section_type == 'custom':
            return self.generate_custom_section(section_config)
        
        return None
    
    def generate_hero_section(self, config: Dict) -> Dict:
        """Generiert Hero Section mit Slider"""
        base = self.element_library['hero_slider']['base_structure'].copy()
        base['id'] = self.generate_unique_id('hero')
        
        # Slider Settings anpassen
        slider_widget = base['elements'][0]['elements'][0]
        slider_settings = {
            "slider_items": []
        }
        
        for slide in config.get('slides', []):
            slider_settings['slider_items'].append({
                "title": slide.get('title', ''),
                "subtitle": slide.get('subtitle', ''),
                "button_text": slide.get('button_text', ''),
                "button_link": {"url": slide.get('button_link', '#')},
                "background_type": slide.get('background_type', 'image'),
                "background_image": {"url": slide.get('background_image', '')},
                "background_video": slide.get('background_video', '')
            })
        
        slider_widget['settings'] = slider_settings
        return base
    
    def generate_service_cards_section(self, config: Dict) -> Dict:
        """Generiert Service Cards Section"""
        section = {
            "id": self.generate_unique_id('services'),
            "elType": "section",
            "settings": {
                "content_width": {"unit": "px", "size": 1140},
                "gap": "extended",
                "padding": {"unit": "px", "top": 80, "bottom": 80}
            },
            "elements": []
        }
        
        for idx, card_config in enumerate(config.get('cards', [])):
            card = self.element_library['service_card']['base_structure'].copy()
            card['id'] = self.generate_unique_id(f'card_{idx}')
            
            # Animation Delay
            if idx > 0:
                card['settings']['animation_delay'] = idx * 200
            
            # Bild Section
            image_section = card['elements'][0]
            image_section['id'] = self.generate_unique_id(f'img_sec_{idx}')
            image_section['settings']['background_image'] = {
                "url": card_config.get('image', ''),
                "id": "",
                "size": ""
            }
            
            # Text Section
            text_widget = card['elements'][1]['elements'][0]['elements'][0]
            text_widget['id'] = self.generate_unique_id(f'text_{idx}')
            text_widget['settings'].update({
                "title": card_config.get('title', ''),
                "subtitle": card_config.get('subtitle', ''),
                "text": card_config.get('description', ''),
                "selected_icon": {
                    "value": card_config.get('icon', 'fas fa-shield-alt'),
                    "library": "fa-solid"
                }
            })
            
            section['elements'].append(card)
        
        return section
    
    def generate_testimonial_section(self, config: Dict) -> Dict:
        """Generiert Testimonial Carousel Section"""
        base = self.element_library['testimonial_carousel']['base_structure'].copy()
        base['id'] = self.generate_unique_id('testimonials')
        
        carousel_widget = base['elements'][0]['elements'][0]
        carousel_widget['settings'] = {
            "testimonials": [
                {
                    "content": testimonial.get('text', ''),
                    "name": testimonial.get('name', ''),
                    "position": testimonial.get('position', ''),
                    "image": {"url": testimonial.get('image', '')}
                }
                for testimonial in config.get('testimonials', [])
            ]
        }
        
        return base
    
    def generate_contact_section(self, config: Dict) -> Dict:
        """Generiert Contact Form Section"""
        base = self.element_library['contact_form']['base_structure'].copy()
        base['id'] = self.generate_unique_id('contact')
        
        # Heading anpassen
        heading_widget = base['elements'][0]['elements'][0]
        heading_widget['settings']['title'] = config.get('title', 'Kontakt')
        
        # Form ID einsetzen
        form_widget = base['elements'][0]['elements'][1]
        form_id = config.get('form_id', '1')
        form_widget['settings']['shortcode'] = f'[contact-form-7 id="{form_id}" title="Contact form 1"]'
        
        return base
    
    def generate_custom_section(self, config: Dict) -> Dict:
        """Generiert eine Custom Section mit flexiblen Elementen"""
        section = {
            "id": self.generate_unique_id('custom'),
            "elType": "section",
            "settings": config.get('settings', {}),
            "elements": []
        }
        
        for column_config in config.get('columns', []):
            column = {
                "id": self.generate_unique_id('col'),
                "elType": "column",
                "settings": {
                    "_column_size": column_config.get('size', 100)
                },
                "elements": []
            }
            
            for widget_config in column_config.get('widgets', []):
                widget = self.generate_widget(widget_config)
                if widget:
                    column['elements'].append(widget)
            
            section['elements'].append(column)
        
        return section
    
    def generate_widget(self, widget_config: Dict) -> Optional[Dict]:
        """Generiert ein einzelnes Widget"""
        widget_type = widget_config.get('type')
        
        widget = {
            "id": self.generate_unique_id('widget'),
            "elType": "widget",
            "widgetType": widget_type,
            "settings": widget_config.get('settings', {})
        }
        
        return widget
    
    def export_to_xml(self, data: Dict, output_file: str):
        """Exportiert die generierten Daten als WordPress XML"""
        root = ET.Element('wordpress')
        
        # Site Info
        site_info = data.get('site_info', {})
        for key, value in site_info.items():
            elem = ET.SubElement(root, key)
            elem.text = str(value)
        
        # Pages
        for page in data.get('pages', []):
            item = ET.SubElement(root, 'item')
            
            title_elem = ET.SubElement(item, 'title')
            title_elem.text = page['title']
            
            content_elem = ET.SubElement(item, 'content')
            content_elem.text = ''  # Elementor nutzt postmeta
            
            # Postmeta für Elementor
            postmeta = ET.SubElement(item, 'postmeta')
            
            meta_elementor_data = ET.SubElement(postmeta, 'meta')
            key = ET.SubElement(meta_elementor_data, 'meta_key')
            key.text = '_elementor_data'
            value = ET.SubElement(meta_elementor_data, 'meta_value')
            value.text = page['elementor_data']
            
            meta_elementor_version = ET.SubElement(postmeta, 'meta')
            key = ET.SubElement(meta_elementor_version, 'meta_key')
            key.text = '_elementor_version'
            value = ET.SubElement(meta_elementor_version, 'meta_value')
            value.text = page['elementor_version']
            
            meta_template = ET.SubElement(postmeta, 'meta')
            key = ET.SubElement(meta_template, 'meta_key')
            key.text = '_wp_page_template'
            value = ET.SubElement(meta_template, 'meta_value')
            value.text = page['template']
        
        # Pretty print
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        print(f"✅ XML exportiert: {output_file}")
    
    def export_to_json(self, data: Dict, output_file: str):
        """Exportiert die generierten Daten als JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON exportiert: {output_file}")


def main():
    """Hauptfunktion für CLI-Nutzung"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Elementor Generator - YAML zu Elementor JSON/XML')
    parser.add_argument('config', help='YAML Konfigurationsdatei')
    parser.add_argument('--output-json', help='Output JSON Datei', default='output.json')
    parser.add_argument('--output-xml', help='Output XML Datei', default='output.xml')
    
    args = parser.parse_args()
    
    generator = ElementorGenerator()
    
    print(f"📖 Lade Konfiguration: {args.config}")
    data = generator.process_yaml_config(args.config)
    
    generator.export_to_json(data, args.output_json)
    generator.export_to_xml(data, args.output_xml)
    
    print("✅ Generierung abgeschlossen!")


if __name__ == "__main__":
    main()