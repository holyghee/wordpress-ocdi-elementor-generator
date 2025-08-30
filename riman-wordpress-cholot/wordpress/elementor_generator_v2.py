#!/usr/bin/env python3
"""
Elementor Generator V2 - Mit Service Cards Template Support
Nutzt die exportierten Elementor Blocks als Templates
"""

import json
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import copy

class ElementorGeneratorV2:
    """Generator mit Template-Support aus elementor_blocks"""
    
    def __init__(self, blocks_path: str = "elementor_blocks"):
        self.blocks_path = Path(blocks_path)
        self.templates = {}
        self.load_templates()
        
    def load_templates(self):
        """Lädt alle Templates aus dem elementor_blocks Ordner"""
        if not self.blocks_path.exists():
            print(f"⚠️ Blocks Ordner nicht gefunden: {self.blocks_path}")
            return
            
        # Lade alle JSON Templates
        for category_dir in self.blocks_path.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                self.templates[category] = {}
                
                for template_file in category_dir.glob("*.json"):
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        template_name = template_file.stem
                        self.templates[category][template_name] = template_data
                        print(f"✅ Template geladen: {category}/{template_name}")
    
    def generate_unique_id(self) -> str:
        """Generiert eine eindeutige 7-stellige ID für Elementor"""
        timestamp = datetime.now().isoformat()
        random_str = hashlib.md5(timestamp.encode()).hexdigest()
        return random_str[:7]
    
    def process_template(self, template: Dict, replacements: Dict) -> Dict:
        """Verarbeitet ein Template und ersetzt Platzhalter"""
        # Deep copy des Templates
        processed = copy.deepcopy(template)
        
        # Wenn es eine 'content' Struktur gibt (Elementor Export Format)
        if 'content' in processed and isinstance(processed['content'], list):
            processed = processed['content'][0]  # Nimm das erste Element
        
        # Ersetze IDs
        processed = self.replace_ids(processed)
        
        # Ersetze Inhalte
        processed = self.replace_content(processed, replacements)
        
        return processed
    
    def replace_ids(self, element: Any) -> Any:
        """Ersetzt alle IDs mit neuen generierten IDs"""
        if isinstance(element, dict):
            new_element = {}
            for key, value in element.items():
                if key == 'id':
                    new_element[key] = self.generate_unique_id()
                elif isinstance(value, (dict, list)):
                    new_element[key] = self.replace_ids(value)
                else:
                    new_element[key] = value
            return new_element
        elif isinstance(element, list):
            return [self.replace_ids(item) for item in element]
        else:
            return element
    
    def replace_content(self, element: Any, replacements: Dict) -> Any:
        """Ersetzt Inhalte basierend auf Replacements Dictionary"""
        if isinstance(element, dict):
            new_element = {}
            for key, value in element.items():
                # Ersetze Bilder
                if key == 'image' and 'image_url' in replacements:
                    new_element[key] = {
                        "url": replacements['image_url'],
                        "id": ""
                    }
                # Ersetze Titel
                elif key == 'title' and 'title' in replacements:
                    new_element[key] = replacements['title']
                # Ersetze Subtitle
                elif key == 'subtitle' and 'subtitle' in replacements:
                    new_element[key] = replacements['subtitle']
                # Ersetze Text
                elif key in ['text', 'editor'] and 'description' in replacements:
                    new_element[key] = replacements['description']
                # Ersetze Icon
                elif key == 'selected_icon' and 'icon' in replacements:
                    new_element[key] = {
                        "value": replacements['icon'],
                        "library": "fa-solid"
                    }
                # Rekursiv für verschachtelte Strukturen
                elif isinstance(value, (dict, list)):
                    new_element[key] = self.replace_content(value, replacements)
                else:
                    new_element[key] = value
            return new_element
        elif isinstance(element, list):
            return [self.replace_content(item, replacements) for item in element]
        else:
            return element
    
    def generate_service_cards_section(self, cards_config: List[Dict]) -> Dict:
        """Generiert eine komplette Service Cards Section"""
        
        # Basis Section Struktur
        section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "content_width": {"unit": "px", "size": 1140},
                "gap": "extended",
                "padding": {"unit": "px", "top": 80, "bottom": 80}
            },
            "elements": []
        }
        
        # Füge Service Cards hinzu
        for idx, card_config in enumerate(cards_config):
            card = self.generate_service_card(card_config, idx)
            section['elements'].append(card)
        
        return section
    
    def generate_service_card(self, card_config: Dict, index: int) -> Dict:
        """Generiert eine einzelne Service Card mit Cholot Design"""
        
        # Verwende Template wenn vorhanden
        if 'services' in self.templates and 'service_cards_image_1' in self.templates['services']:
            template = self.templates['services']['service_cards_image_1']
            
            # Extrahiere die Struktur
            if 'content' in template:
                card_structure = template['content'][0]
            else:
                card_structure = template
            
            # Prozessiere mit Replacements
            card = self.process_template(card_structure, card_config)
            
            # Wickle in Column wenn es eine Section ist
            if card.get('elType') == 'section':
                column = {
                    "id": self.generate_unique_id(),
                    "elType": "column",
                    "settings": {
                        "_column_size": 33,
                        "animation": "fadeInUp",
                        "animation_delay": index * 200 if index > 0 else 0
                    },
                    "elements": [card]
                }
                return column
            
            return card
        
        # Fallback: Manuelle Struktur
        return self.generate_service_card_manual(card_config, index)
    
    def generate_service_card_manual(self, card_config: Dict, index: int) -> Dict:
        """Manuelle Service Card Generierung (Fallback)"""
        
        card = {
            "id": self.generate_unique_id(),
            "elType": "column",
            "settings": {
                "_column_size": 33,
                "animation": "fadeInUp",
                "animation_delay": index * 200 if index > 0 else 0
            },
            "elements": [
                # Image Section mit Curved Shape
                {
                    "id": self.generate_unique_id(),
                    "elType": "section",
                    "isInner": True,
                    "settings": {
                        "gap": "no",
                        "shape_divider_bottom": "curve",
                        "shape_divider_bottom_color": "#fafafa",
                        "shape_divider_bottom_negative": "yes",
                        "shape_divider_bottom_above_content": "yes",
                        "background_background": "classic",
                        "background_image": {
                            "url": card_config.get('image', ''),
                            "id": ""
                        },
                        "background_position": "center center",
                        "background_size": "cover",
                        "padding": {"unit": "px", "top": 150, "bottom": 50}
                    },
                    "elements": [
                        {
                            "id": self.generate_unique_id(),
                            "elType": "column",
                            "settings": {"_column_size": 100},
                            "elements": []
                        }
                    ]
                },
                # Content Section
                {
                    "id": self.generate_unique_id(),
                    "elType": "section",
                    "isInner": True,
                    "settings": {
                        "gap": "no",
                        "background_background": "classic",
                        "background_color": "#ffffff",
                        "padding": {"unit": "px", "top": 30, "bottom": 40, "left": 30, "right": 30}
                    },
                    "elements": [
                        {
                            "id": self.generate_unique_id(),
                            "elType": "column",
                            "settings": {"_column_size": 100},
                            "elements": [
                                {
                                    "id": self.generate_unique_id(),
                                    "elType": "widget",
                                    "widgetType": "cholot-texticon",
                                    "settings": {
                                        "title": card_config.get('title', ''),
                                        "subtitle": card_config.get('subtitle', ''),
                                        "text": card_config.get('description', ''),
                                        "selected_icon": {
                                            "value": card_config.get('icon', 'fas fa-shield-alt'),
                                            "library": "fa-solid"
                                        },
                                        "icon_color": "#b68c2f",
                                        "subtitle_color": "#b68c2f",
                                        "title_color": "#1f1f1f",
                                        "text_color": "#666666"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        return card
    
    def process_yaml_config(self, yaml_file: str) -> Dict:
        """Verarbeitet YAML Config und generiert Elementor Struktur"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pages = []
        
        for page_config in config.get('pages', []):
            sections = []
            
            for section_config in page_config.get('sections', []):
                if section_config['type'] == 'service_cards':
                    section = self.generate_service_cards_section(section_config.get('cards', []))
                    sections.append(section)
                # Hier können weitere Section-Types hinzugefügt werden
            
            pages.append({
                'title': page_config.get('title', ''),
                'elementor_data': json.dumps(sections),
                'elementor_version': '3.18.3'
            })
        
        return {'pages': pages}
    
    def save_output(self, data: Dict, output_file: str):
        """Speichert generierte Daten als JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Output gespeichert: {output_file}")


def main():
    """Test-Funktion"""
    generator = ElementorGeneratorV2()
    
    # Test YAML Config
    test_config = {
        'pages': [{
            'title': 'RIMAN Startseite',
            'sections': [{
                'type': 'service_cards',
                'cards': [
                    {
                        'title': 'Asbestsanierung',
                        'subtitle': 'ZERTIFIZIERT',
                        'description': 'Professionelle Entfernung von Asbest nach TRGS 519.',
                        'icon': 'fas fa-shield-alt',
                        'image': 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung.jpg'
                    },
                    {
                        'title': 'PCB-Sanierung',
                        'subtitle': 'FACHGERECHT',
                        'description': 'Sichere Beseitigung von PCB-belasteten Materialien.',
                        'icon': 'fas fa-industry',
                        'image': 'http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung.jpg'
                    },
                    {
                        'title': 'Schimmelsanierung',
                        'subtitle': 'NACHHALTIG',
                        'description': 'Nachhaltige Schimmelbeseitigung und Prävention.',
                        'icon': 'fas fa-home',
                        'image': 'http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung.jpg'
                    }
                ]
            }]
        }]
    }
    
    # Speichere Test Config
    with open('test_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(test_config, f, allow_unicode=True)
    
    # Generiere
    result = generator.process_yaml_config('test_config.yaml')
    generator.save_output(result, 'generated_service_cards.json')
    
    print("\n🎉 Service Cards generiert!")
    print("   Nutze generated_service_cards.json für den Import")


if __name__ == "__main__":
    main()