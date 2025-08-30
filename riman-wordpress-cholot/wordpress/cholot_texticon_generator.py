#!/usr/bin/env python3
"""
Cholot TextIcon Generator - Creates working Elementor JSON with cholot-texticon widgets
Based on the working full_site_generator but with proper cholot-texticon support
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from xml.dom import minidom
from typing import Dict, Any, List, Optional
from copy import deepcopy
import uuid
import random
import re

class CholotTextIconGenerator:
    def __init__(self):
        self.item_counter = 100  # Start IDs from 100
        self.attachment_ids = {}  # Track attachment IDs for reuse
        self.menu_items = []      # Track menu items for ordering
        self.categories = {}      # Track categories
        self.tags = {}           # Track tags
        
    def generate_unique_id(self) -> str:
        """Generate unique Elementor element ID"""
        return uuid.uuid4().hex[:7]
    
    def get_next_id(self) -> int:
        """Get next WordPress item ID"""
        self.item_counter += 1
        return self.item_counter
    
    def create_cholot_texticon_widget(self, service: Dict) -> Dict:
        """Create a proper cholot-texticon widget"""
        return {
            "id": self.generate_unique_id(),
            "elType": "widget",
            "widgetType": "cholot-texticon",
            "settings": {
                "icon": service.get('icon', 'fas fa-cog'),
                "icon_view": "default",
                "icon_shape": "circle",
                "icon_size": "large",
                "icon_primary_color": "#ff6b35",
                "icon_secondary_color": "#ffffff",
                "title": service.get('title', 'Service Title'),
                "title_size": "medium",
                "title_color": "#333333",
                "description": service.get('description', 'Service description goes here.'),
                "description_color": "#666666",
                "button_text": service.get('button_text', 'Learn More'),
                "button_url": {"url": service.get('button_url', '#')},
                "button_style": "default",
                "button_size": "sm",
                "alignment": "center",
                "content_vertical_alignment": "top"
            }
        }
    
    def create_hero_slider_section(self, config: Dict) -> Dict:
        """Create hero slider section"""
        slides = config.get('slides', [])
        if not slides:
            return None
        
        slide = slides[0]
        
        return {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "height": "min-height",
                "custom_height": {"unit": "vh", "size": 100},
                "background_background": "classic",
                "background_image": {"url": slide.get('image', '')},
                "background_position": "center center",
                "background_repeat": "no-repeat",
                "background_size": "cover",
                "background_overlay_background": "classic",
                "background_overlay_color": "rgba(0,0,0,0.4)",
                "content_position": "middle",
                "align": "center"
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": self.generate_unique_id(),
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": slide.get('title', 'Hero Title'),
                            "size": "xxl",
                            "align": "center",
                            "typography_typography": "custom",
                            "typography_font_size": {"unit": "px", "size": 60},
                            "typography_font_weight": "700",
                            "title_color": "#ffffff"
                        }
                    },
                    {
                        "id": self.generate_unique_id(),
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"<p style='text-align: center;'>{slide.get('subtitle', '')}</p>",
                            "text_color": "#ffffff"
                        }
                    },
                    {
                        "id": self.generate_unique_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "settings": {
                            "text": slide.get('button_text', 'Learn More'),
                            "link": {"url": slide.get('button_url', '#')},
                            "align": "center",
                            "size": "lg",
                            "button_background_color": "#ff6b35",
                            "border_radius": {"unit": "px", "size": 5}
                        }
                    }
                ]
            }]
        }
    
    def create_service_cards_section(self, config: Dict) -> List[Dict]:
        """Create service cards with cholot-texticon widgets - returns 2 sections"""
        cards = config.get('cards', [])
        if not cards:
            return []
        
        # Title section
        title_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "content_width": {"unit": "px", "size": 1200},
                "margin": {"unit": "px", "top": 80, "bottom": 40},
                "padding": {"unit": "px", "top": 0, "bottom": 0}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": self.generate_unique_id(),
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": config.get('title', 'Our Services'),
                            "size": "xl",
                            "align": "center",
                            "title_color": "#333333"
                        }
                    },
                    {
                        "id": self.generate_unique_id(),
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"<p style='text-align: center;'>{config.get('subtitle', '')}</p>",
                            "text_color": "#666666"
                        }
                    }
                ]
            }]
        }
        
        # Service cards section - 2 rows of 4 cards each
        service_sections = []
        
        # First row (4 cards)
        if len(cards) > 0:
            first_row_columns = []
            for service in cards[:4]:
                widget = self.create_cholot_texticon_widget(service)
                column = {
                    "id": self.generate_unique_id(),
                    "elType": "column",
                    "settings": {"_column_size": 25},
                    "elements": [widget]
                }
                first_row_columns.append(column)
            
            first_row_section = {
                "id": self.generate_unique_id(),
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "content_width": {"unit": "px", "size": 1200},
                    "margin": {"unit": "px", "top": 0, "bottom": 40},
                    "padding": {"unit": "px", "top": 0, "bottom": 0}
                },
                "elements": first_row_columns
            }
            service_sections.append(first_row_section)
        
        # Second row (4 more cards)
        if len(cards) > 4:
            second_row_columns = []
            for service in cards[4:8]:
                widget = self.create_cholot_texticon_widget(service)
                column = {
                    "id": self.generate_unique_id(),
                    "elType": "column",
                    "settings": {"_column_size": 25},
                    "elements": [widget]
                }
                second_row_columns.append(column)
            
            second_row_section = {
                "id": self.generate_unique_id(),
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "content_width": {"unit": "px", "size": 1200},
                    "margin": {"unit": "px", "top": 0, "bottom": 80},
                    "padding": {"unit": "px", "top": 0, "bottom": 0}
                },
                "elements": second_row_columns
            }
            service_sections.append(second_row_section)
        
        return [title_section] + service_sections
    
    def create_elementor_content(self, page_config: Dict) -> str:
        """Create Elementor JSON content for a page"""
        sections = page_config.get('sections', [])
        elementor_sections = []
        
        for section_config in sections:
            section_type = section_config.get('type')
            
            if section_type == 'hero_slider':
                section = self.create_hero_slider_section(section_config)
                if section:
                    elementor_sections.append(section)
                    
            elif section_type == 'service_cards':
                sections_list = self.create_service_cards_section(section_config)
                if sections_list:
                    elementor_sections.extend(sections_list)
        
        # Convert to JSON string
        return json.dumps(elementor_sections, separators=(',', ':'))
    
    def process_yaml_to_wordpress(self, yaml_path: str) -> tuple:
        """Convert YAML to complete WordPress site structure with cholot-texticon"""
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Create WordPress XML structure using the existing full_site_generator structure
        from full_site_generator import FullSiteGenerator
        base_generator = FullSiteGenerator()
        
        # Override the Elementor data generation
        original_method = base_generator._add_pages
        
        def enhanced_add_pages(channel, config):
            """Enhanced page addition with cholot-texticon support"""
            pages = config.get('pages', [])
            for page_config in pages:
                item_id = base_generator.get_next_id()
                item = ET.SubElement(channel, 'item')
                
                # Basic page information
                ET.SubElement(item, 'title').text = page_config.get('title', 'Page')
                ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url', 'http://localhost')}/{page_config.get('slug', 'page')}"
                ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
                ET.SubElement(item, 'guid', isPermaLink='false').text = f"{config.get('site', {}).get('base_url')}/?page_id={item_id}"
                ET.SubElement(item, 'description').text = ''
                
                # Content
                content = '<!-- wp:html --><!-- /wp:html -->'  # Placeholder for Elementor
                ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = content
                ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = page_config.get('excerpt', '')
                
                # Post details
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
                past_date = datetime(2024, 8, 30, 16, 10, 0)
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page_config.get('slug', 'page')
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = page_config.get('status', 'publish')
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = str(page_config.get('parent', 0))
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(page_config.get('menu_order', 0))
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
                ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
                
                # Add Elementor meta if sections exist
                if page_config.get('sections'):
                    # Create Elementor data with cholot-texticon widgets
                    elementor_json = self.create_elementor_content(page_config)
                        
                    meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = elementor_json
                    
                    # Elementor settings
                    for key, value in [
                        ('_elementor_edit_mode', 'builder'),
                        ('_elementor_template_type', 'wp-page'),
                        ('_wp_page_template', page_config.get('template', 'elementor_canvas'))
                    ]:
                        meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
        
        # Replace the original method
        base_generator._add_pages = enhanced_add_pages
        
        # Process using the enhanced generator
        config_result, rss = base_generator.process_yaml_to_wordpress(yaml_path)
        
        return config_result, rss

def main():
    """Generate cholot XML with working texticon widgets"""
    import sys
    import os
    
    print("🚀 Cholot TextIcon Generator")
    print("=" * 60)
    
    generator = CholotTextIconGenerator()
    
    # Get YAML file from command line or use default
    yaml_file = sys.argv[1] if len(sys.argv) > 1 else 'cholot-working-new.yaml'
    print(f"📖 Loading configuration: {yaml_file}")
    
    # Load configuration
    config, rss = generator.process_yaml_to_wordpress(yaml_file)
    
    # Generate XML using the base generator
    from full_site_generator import FullSiteGenerator
    base_generator = FullSiteGenerator()
    
    output_name = yaml_file.replace('.yaml', '-cholot.xml').replace('.yml', '-cholot.xml')
    output_path = base_generator.generate_wordpress_xml(config, rss, output_name)
    
    # Statistics
    file_size = os.path.getsize(output_path)
    print(f"📄 XML file size: {file_size / 1024:.1f} KB")
    print(f"✅ Cholot XML with texticon widgets generated: {output_path}")

if __name__ == "__main__":
    main()