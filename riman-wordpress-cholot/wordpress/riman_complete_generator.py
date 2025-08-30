#!/usr/bin/env python3
"""
RIMAN Complete Website Generator
Combines Hero Slider + Service Cards + Full WordPress Site
Enhanced version of ElementorGeneratorV2 with Hero Slider support
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List, Optional
from copy import deepcopy
import uuid
import hashlib
from pathlib import Path

class RimanCompleteGenerator:
    """Complete RIMAN website generator with Hero + Service Cards"""
    
    def __init__(self, blocks_path: str = "elementor_blocks"):
        self.blocks_path = Path(blocks_path)
        self.templates = {}
        self.item_counter = 100
        self.attachment_ids = {}
        self.load_templates()
        
    def load_templates(self):
        """Load all templates from elementor_blocks folder"""
        if not self.blocks_path.exists():
            print(f"⚠️ Blocks folder not found: {self.blocks_path}")
            return
            
        # Load all JSON templates
        for category_dir in self.blocks_path.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                self.templates[category] = {}
                
                for template_file in category_dir.glob("*.json"):
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        template_name = template_file.stem
                        self.templates[category][template_name] = template_data
                        print(f"✅ Template loaded: {category}/{template_name}")
    
    def generate_unique_id(self) -> str:
        """Generate unique Elementor element ID"""
        return uuid.uuid4().hex[:7]
    
    def get_next_id(self) -> int:
        """Get next WordPress item ID"""
        self.item_counter += 1
        return self.item_counter
    
    def generate_hero_slider_section(self, slides_config: List[Dict]) -> Dict:
        """Generate Hero Slider section using rdn-slider template"""
        
        # Use hero template if available
        if 'hero' in self.templates and 'hero_home' in self.templates['hero']:
            template = self.templates['hero']['hero_home']
            
            if 'content' in template and len(template['content']) > 0:
                hero_section = deepcopy(template['content'][0])
                
                # Update section ID
                hero_section['id'] = self.generate_unique_id()
                
                # Find and update slider widget
                if 'elements' in hero_section:
                    for column in hero_section['elements']:
                        if 'elements' in column:
                            for widget in column['elements']:
                                if widget.get('widgetType') == 'rdn-slider':
                                    # Replace slider content with our slides
                                    slider_list = []
                                    for slide in slides_config:
                                        slider_item = {
                                            "title": slide.get('title', ''),
                                            "subtitle": slide.get('subtitle', ''),
                                            "text": slide.get('text', ''),
                                            "_id": self.generate_unique_id()[:7],
                                            "btn_text": slide.get('button_text', ''),
                                            "btn_link": {"url": slide.get('button_link', '#')},
                                            "image": {
                                                "url": slide.get('image', ''),
                                                "id": "",
                                                "alt": "",
                                                "source": "library",
                                                "size": ""
                                            }
                                        }
                                        slider_list.append(slider_item)
                                    
                                    widget['settings']['slider_list'] = slider_list
                                    widget['id'] = self.generate_unique_id()
                
                return hero_section
        
        # Fallback: Generate basic hero section
        return self.generate_hero_fallback(slides_config)
    
    def generate_hero_fallback(self, slides_config: List[Dict]) -> Dict:
        """Fallback hero section generation"""
        return {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "gap": "no",
                "layout": "full_width",
                "background_color": "rgba(0,0,0,0.6)"
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
                            "widgetType": "heading",
                            "settings": {
                                "title": slides_config[0].get('title', 'Hero Title') if slides_config else 'Hero Title',
                                "header_size": "h1"
                            },
                            "elements": []
                        }
                    ]
                }
            ]
        }
    
    def generate_service_cards_section(self, cards_config: List[Dict]) -> Dict:
        """Generate Service Cards section with 8 cards"""
        
        section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "gap": "extended",
                "content_position": "middle",
                "structure": "30",
                "background_color": "#b68c2f",
                "box_shadow_box_shadow": {
                    "horizontal": 10,
                    "vertical": 0,
                    "blur": 0,
                    "spread": 4,
                    "color": "#ededed"
                },
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
        
        # Create cards in rows of 4 (2 rows for 8 cards)
        cards_per_row = 4
        for i in range(0, len(cards_config), cards_per_row):
            row_cards = cards_config[i:i + cards_per_row]
            
            # Create inner section for this row
            row_section = {
                "id": self.generate_unique_id(),
                "elType": "section",
                "settings": {
                    "gap": "extended"
                },
                "elements": [],
                "isInner": True
            }
            
            # Add cards to row
            for j, card_config in enumerate(row_cards):
                card = self.generate_service_card(card_config, i + j)
                row_section['elements'].append(card)
            
            section['elements'].append(row_section)
        
        return section
    
    def generate_service_card(self, card_config: Dict, index: int) -> Dict:
        """Generate a single service card with Cholot design"""
        
        card = {
            "id": self.generate_unique_id(),
            "elType": "column",
            "settings": {
                "_column_size": 25,  # 4 cards per row = 25% each
                "background_background": "classic",
                "background_color": "#fafafa",
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
                "margin": {
                    "unit": "px",
                    "top": 15,
                    "right": 15,
                    "bottom": 15,
                    "left": 15,
                    "isLinked": True
                },
                "animation": "fadeInUp",
                "animation_delay": index * 200
            },
            "elements": [
                # Image section
                {
                    "id": self.generate_unique_id(),
                    "elType": "section",
                    "settings": {
                        "gap": "no",
                        "shape_divider_bottom": "curve",
                        "shape_divider_bottom_color": "#fafafa",
                        "shape_divider_bottom_negative": "yes",
                        "shape_divider_bottom_above_content": "yes"
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
                                    "widgetType": "image",
                                    "settings": {
                                        "image": {
                                            "url": card_config.get('image', ''),
                                            "id": ""
                                        },
                                        "_border_width": {
                                            "unit": "px",
                                            "top": 4,
                                            "right": 0,
                                            "bottom": 0,
                                            "left": 0,
                                            "isLinked": False
                                        },
                                        "_border_color": "#b68c2f"
                                    },
                                    "elements": []
                                }
                            ],
                            "isInner": True
                        }
                    ],
                    "isInner": True
                },
                # Content section
                {
                    "id": self.generate_unique_id(),
                    "elType": "section",
                    "settings": {
                        "gap": "no",
                        "content_position": "middle",
                        "padding": {
                            "unit": "px",
                            "top": 30,
                            "right": 30,
                            "bottom": 30,
                            "left": 30,
                            "isLinked": True
                        },
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
                            "id": self.generate_unique_id(),
                            "elType": "column",
                            "settings": {"_column_size": 100},
                            "elements": [
                                # Text Icon Widget (cholot-texticon)
                                {
                                    "id": self.generate_unique_id(),
                                    "elType": "widget",
                                    "widgetType": "cholot-texticon",
                                    "settings": {
                                        "selected_icon": {
                                            "value": card_config.get('icon', 'fas fa-shield-alt'),
                                            "library": "fa-solid"
                                        },
                                        "title": card_config.get('title', ''),
                                        "subtitle": card_config.get('subtitle', ''),
                                        "text": f"<p>{card_config.get('description', '')}</p>",
                                        "icon_color": "#ffffff",
                                        "iconbg_color": "#b68c2f",
                                        "subtitle_color": "#b68c2f",
                                        "icon_size": {"unit": "px", "size": 20},
                                        "icon_bg_size": {"unit": "px", "size": 72},
                                        "title_typography_typography": "custom",
                                        "title_typography_font_size": {"unit": "px", "size": 28},
                                        "subtitle_typography_typography": "custom",
                                        "subtitle_typography_font_size": {"unit": "px", "size": 13},
                                        "subtitle_typography_font_weight": "700",
                                        "subtitle_typography_text_transform": "uppercase",
                                        "subtitle_typography_letter_spacing": {"unit": "px", "size": 1},
                                        "text_typography_font_size": {"unit": "px", "size": 15},
                                        "text_typography_font_style": "italic",
                                        "icon_bordering_border": "solid",
                                        "icon_bordering_color": "#fafafa",
                                        "icon_bordering_width": {
                                            "unit": "px",
                                            "top": 7,
                                            "right": 7,
                                            "bottom": 7,
                                            "left": 7,
                                            "isLinked": True
                                        },
                                        "_border_border": "dashed",
                                        "_border_color": "#b68c2f",
                                        "_border_width": {
                                            "unit": "px",
                                            "top": 0,
                                            "right": 1,
                                            "bottom": 1,
                                            "left": 1,
                                            "isLinked": False
                                        }
                                    },
                                    "elements": []
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
        
        return card
    
    def process_yaml_to_elementor(self, yaml_path: str) -> List[Dict]:
        """Process YAML config to Elementor sections"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        sections = []
        
        # Process pages
        for page_config in config.get('pages', []):
            if page_config.get('sections'):
                for section_config in page_config['sections']:
                    if section_config['type'] == 'hero_slider':
                        section = self.generate_hero_slider_section(section_config.get('slides', []))
                        sections.append(section)
                    elif section_config['type'] == 'service_cards':
                        section = self.generate_service_cards_section(section_config.get('cards', []))
                        sections.append(section)
        
        return sections
    
    def generate_wordpress_xml(self, yaml_path: str, output_path: str) -> str:
        """Generate complete WordPress XML file"""
        from full_site_generator import FullSiteGenerator
        
        # Use full site generator for complete WordPress structure
        generator = FullSiteGenerator()
        config, rss = generator.process_yaml_to_wordpress(yaml_path)
        
        return generator.generate_wordpress_xml(config, rss, output_path)
    
    def generate_elementor_json(self, yaml_path: str, output_path: str) -> str:
        """Generate Elementor JSON file"""
        sections = self.process_yaml_to_elementor(yaml_path)
        
        # Create Elementor data structure
        elementor_data = json.dumps(sections, separators=(',', ':'))
        
        # Save JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sections, f, indent=2, ensure_ascii=False)
        
        return output_path


def main():
    """Generate complete RIMAN website"""
    print("🚀 RIMAN Complete Website Generator")
    print("=" * 60)
    
    generator = RimanCompleteGenerator()
    
    config_file = 'riman_complete_config.yaml'
    print(f"📖 Loading configuration: {config_file}")
    
    try:
        # Generate Elementor JSON
        elementor_output = generator.generate_elementor_json(
            config_file, 'riman_elementor.json'
        )
        print(f"✅ Elementor JSON generated: {elementor_output}")
        
        # Generate WordPress XML
        xml_output = generator.generate_wordpress_xml(
            config_file, 'riman_complete.xml'
        )
        print(f"✅ WordPress XML generated: {xml_output}")
        
        print("\n🎉 RIMAN complete website generated successfully!")
        print("📁 Files created:")
        print(f"   • Elementor JSON: riman_elementor.json")
        print(f"   • WordPress XML: riman_complete.xml")
        print("\n📋 Import Instructions:")
        print("1. Import riman_complete.xml via WordPress Admin > Tools > Import")
        print("2. The Elementor data is embedded in the XML")
        print("3. Hero Slider uses rdn-slider widget")
        print("4. Service Cards use cholot-texticon widgets")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()