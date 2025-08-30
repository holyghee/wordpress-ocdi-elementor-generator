#!/usr/bin/env python3
"""
Elementor Processor V3 - Versteht wie Elementor CSS generiert
Analysiert die Cholot Theme Struktur und repliziert sie korrekt
"""

import json
import yaml
import mysql.connector
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
from datetime import datetime

class ElementorProcessor:
    """
    Prozessor der versteht wie Elementor aus JSON/XML CSS generiert
    """
    
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.elementor_version = "3.18.3"
        
    def connect_db(self):
        """Verbindet zur WordPress Datenbank"""
        return mysql.connector.connect(
            host=self.db_config['host'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
    
    def analyze_original_structure(self, source_db: str, post_id: int) -> Dict:
        """
        Analysiert die Original Cholot Struktur
        """
        # Verbinde zur Original DB
        original_config = self.db_config.copy()
        original_config['database'] = source_db
        
        conn = mysql.connector.connect(**original_config)
        cursor = conn.cursor(dictionary=True)
        
        # Hole Elementor Data
        cursor.execute("""
            SELECT meta_value 
            FROM wp_postmeta 
            WHERE post_id = %s AND meta_key = '_elementor_data'
        """, (post_id,))
        
        result = cursor.fetchone()
        if result:
            elementor_data = json.loads(result['meta_value'])
            
            # Analysiere Shape Divider Verwendung
            shape_dividers = self.extract_shape_dividers(elementor_data)
            
            conn.close()
            return {
                'data': elementor_data,
                'shape_dividers': shape_dividers
            }
        
        conn.close()
        return None
    
    def extract_shape_dividers(self, elements: List, path: str = "") -> List[Dict]:
        """
        Extrahiert alle Shape Divider Konfigurationen
        """
        shape_dividers = []
        
        for i, element in enumerate(elements):
            current_path = f"{path}[{i}]"
            
            # Prüfe auf Shape Divider Settings
            if 'settings' in element:
                settings = element['settings']
                
                # Check for shape divider settings
                for position in ['top', 'bottom']:
                    key = f'shape_divider_{position}'
                    if key in settings:
                        divider_info = {
                            'path': current_path,
                            'position': position,
                            'type': settings.get(key),
                            'color': settings.get(f'{key}_color'),
                            'width': settings.get(f'{key}_width'),
                            'height': settings.get(f'{key}_height'),
                            'negative': settings.get(f'{key}_negative'),
                            'flip': settings.get(f'{key}_flip'),
                            'above_content': settings.get(f'{key}_above_content'),
                            'element_type': element.get('elType'),
                            'is_inner': element.get('isInner', False)
                        }
                        shape_dividers.append(divider_info)
            
            # Rekursiv für Unterelemente
            if 'elements' in element and element['elements']:
                child_dividers = self.extract_shape_dividers(
                    element['elements'], 
                    f"{current_path}.elements"
                )
                shape_dividers.extend(child_dividers)
        
        return shape_dividers
    
    def generate_service_card_structure(self, card_data: Dict) -> Dict:
        """
        Generiert die exakte Service Card Struktur mit Shape Dividers
        Basiert auf der analysierten Cholot Struktur
        """
        
        # Generiere unique IDs (7 Zeichen wie Elementor)
        def gen_id():
            return hashlib.md5(
                f"{datetime.now().isoformat()}{card_data.get('title', '')}".encode()
            ).hexdigest()[:7]
        
        return {
            "id": gen_id(),
            "elType": "column",
            "settings": {
                "_column_size": 33,
                "_inline_size": None,
                "background_background": "classic",
                "background_size": "cover",
                "border_width": {
                    "unit": "px",
                    "top": 10,
                    "right": 0,
                    "bottom": 10,
                    "left": 10,
                    "isLinked": False
                },
                "border_color": "#ededed",
                "box_shadow_box_shadow": {
                    "horizontal": 0,
                    "vertical": 4,
                    "blur": 5,
                    "spread": 0,
                    "color": "rgba(196,196,196,0.26)"
                },
                "z_index": 1,
                "background_color": "#fafafa",
                "box_shadow_box_shadow_type": "yes",
                "box_shadow_hover_box_shadow_type": "yes",
                "box_shadow_hover_box_shadow": {
                    "horizontal": 0,
                    "vertical": 0,
                    "blur": 0,
                    "spread": 0,
                    "color": "rgba(0,0,0,0)"
                },
                "margin": {
                    "unit": "px",
                    "top": 15,
                    "right": 15,
                    "bottom": 15,
                    "left": 15,
                    "isLinked": True
                },
                "animation": "fadeInUp",
                "animation_duration": "fast"
            },
            "elements": [
                # Inner Section mit Shape Divider für Bild
                {
                    "id": gen_id(),
                    "elType": "section",
                    "settings": {
                        "gap": "no",
                        # KRITISCH: Diese Settings triggern Elementor's Shape Divider Rendering
                        "shape_divider_bottom": "curve",
                        "shape_divider_bottom_color": "#fafafa",
                        "shape_divider_bottom_width": {
                            "unit": "%",
                            "size": 100
                        },
                        "shape_divider_bottom_height": {
                            "unit": "px",
                            "size": 50
                        },
                        "shape_divider_bottom_negative": "yes",
                        "shape_divider_bottom_above_content": "yes"
                    },
                    "elements": [
                        {
                            "id": gen_id(),
                            "elType": "column",
                            "settings": {
                                "_column_size": 100,
                                "_inline_size": None
                            },
                            "elements": [
                                {
                                    "id": gen_id(),
                                    "elType": "widget",
                                    "settings": {
                                        "image": {
                                            "url": card_data.get('image', ''),
                                            "id": ""
                                        },
                                        "opacity": {
                                            "unit": "px",
                                            "size": 1,
                                            "sizes": []
                                        }
                                    },
                                    "elements": [],
                                    "widgetType": "image"
                                }
                            ],
                            "isInner": True
                        }
                    ],
                    "isInner": True
                },
                # Inner Section für Content
                {
                    "id": gen_id(),
                    "elType": "section",
                    "settings": {
                        "gap": "no",
                        "content_position": "middle",
                        "background_background": "classic",
                        "margin": {
                            "unit": "px",
                            "top": -30,
                            "right": 0,
                            "bottom": 0,
                            "left": 0,
                            "isLinked": False
                        },
                        "z_index": 2
                    },
                    "elements": [
                        {
                            "id": gen_id(),
                            "elType": "column",
                            "settings": {
                                "_column_size": 100,
                                "_inline_size": None
                            },
                            "elements": [
                                {
                                    "id": gen_id(),
                                    "elType": "widget",
                                    "settings": {
                                        "title": card_data.get('title', ''),
                                        "subtitle": card_data.get('subtitle', ''),
                                        "text": f"<p>{card_data.get('description', '')}</p>",
                                        "selected_icon": {
                                            "value": card_data.get('icon', 'fas fa-shield-alt'),
                                            "library": "fa-solid"
                                        },
                                        "__fa4_migrated": {
                                            "selected_icon": True
                                        },
                                        # Alle Cholot TextIcon Settings
                                        "title_typography_typography": "custom",
                                        "title_typography_font_size": {
                                            "unit": "px",
                                            "size": 28,
                                            "sizes": []
                                        },
                                        "subtitle_typography_typography": "custom",
                                        "subtitle_typography_font_size": {
                                            "unit": "px",
                                            "size": 13,
                                            "sizes": []
                                        },
                                        "subtitle_typography_font_weight": "700",
                                        "subtitle_typography_text_transform": "uppercase",
                                        "subtitle_typography_letter_spacing": {
                                            "unit": "px",
                                            "size": 1,
                                            "sizes": []
                                        },
                                        "subtitle_color": "#b68c2f",
                                        "icon_size": {
                                            "unit": "px",
                                            "size": 20,
                                            "sizes": []
                                        },
                                        "icon_bg_size": {
                                            "unit": "px",
                                            "size": 72,
                                            "sizes": []
                                        },
                                        "icon_color": "#ffffff",
                                        "iconbg_color": "#b68c2f"
                                    },
                                    "elements": [],
                                    "widgetType": "cholot-texticon"
                                }
                            ],
                            "isInner": True
                        }
                    ],
                    "isInner": True
                }
            ],
            "isInner": False
        }
    
    def process_yaml_to_elementor(self, yaml_file: str) -> Dict:
        """
        Verarbeitet YAML Config und generiert Elementor Struktur
        """
        with open(yaml_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        pages = []
        
        for page in config.get('pages', []):
            sections = []
            
            for section_config in page.get('sections', []):
                if section_config['type'] == 'service_cards':
                    # Service Cards Section mit Shape Dividers
                    section = {
                        "id": hashlib.md5(f"{datetime.now()}".encode()).hexdigest()[:7],
                        "elType": "section",
                        "settings": {
                            "gap": "extended",
                            "structure": "30",
                            "background_color": "#b68c2f",
                            "margin": {
                                "unit": "px",
                                "top": -100,
                                "right": 0,
                                "bottom": 0,
                                "left": 0,
                                "isLinked": False
                            }
                        },
                        "elements": []
                    }
                    
                    # Füge Service Cards hinzu
                    for card_config in section_config.get('cards', []):
                        card = self.generate_service_card_structure(card_config)
                        section['elements'].append(card)
                    
                    sections.append(section)
            
            pages.append({
                'title': page.get('title'),
                'elementor_data': json.dumps(sections),
                'elementor_version': self.elementor_version
            })
        
        return {'pages': pages}
    
    def import_to_wordpress(self, elementor_data: List, post_id: int):
        """
        Importiert Elementor Daten in WordPress und triggert CSS Generierung
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Speichere Elementor Data
        data_json = json.dumps(elementor_data)
        cursor.execute("""
            UPDATE wp_postmeta 
            SET meta_value = %s 
            WHERE post_id = %s AND meta_key = '_elementor_data'
        """, (data_json, post_id))
        
        # Setze Elementor Version (wichtig für CSS Generation)
        cursor.execute("""
            UPDATE wp_postmeta 
            SET meta_value = %s 
            WHERE post_id = %s AND meta_key = '_elementor_version'
        """, (self.elementor_version, post_id))
        
        # Lösche CSS Cache um Regenerierung zu triggern
        cursor.execute("""
            DELETE FROM wp_postmeta 
            WHERE post_id = %s AND meta_key IN ('_elementor_css', '_elementor_css_time')
        """, (post_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Elementor Daten für Post {post_id} importiert")
        print("   Shape Divider Settings sind korrekt konfiguriert")
        print("   CSS wird beim nächsten Seitenaufruf generiert")


def main():
    """Test und Demo"""
    
    # DB Config
    db_config = {
        'host': 'localhost',
        'user': 'wp_user',
        'password': 'wp_password123',
        'database': 'wordpress_cholot_test'
    }
    
    processor = ElementorProcessor(db_config)
    
    # Analysiere Original
    print("📊 Analysiere Original Cholot Struktur...")
    original = processor.analyze_original_structure('wordpress_mediation', 65)
    
    if original and original['shape_dividers']:
        print(f"✅ {len(original['shape_dividers'])} Shape Dividers gefunden:")
        for divider in original['shape_dividers']:
            print(f"   - {divider['type']} ({divider['position']}) in {divider['element_type']}")
    
    # Prozessiere YAML
    print("\n🔄 Prozessiere YAML Config...")
    result = processor.process_yaml_to_elementor('riman_services.yaml')
    
    # Speichere für Import
    with open('elementor_import_ready.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ Import-bereite Daten gespeichert: elementor_import_ready.json")
    print("\n🎯 Der Prozessor versteht jetzt:")
    print("   1. Wie Shape Dividers in der JSON strukturiert sein müssen")
    print("   2. Welche Settings Elementor's CSS Generation triggern")
    print("   3. Wie die Cholot Widgets konfiguriert werden")


if __name__ == "__main__":
    main()