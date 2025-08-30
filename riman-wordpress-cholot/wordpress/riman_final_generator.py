#!/usr/bin/env python3
"""
RIMAN FINAL GENERATOR - Complete Website with Hero Slider + 8 Service Cards
Bypasses the section_based_processor and directly embeds our custom Elementor data
"""

import json
import yaml
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Any, List
import uuid
from pathlib import Path
from copy import deepcopy

class RimanFinalGenerator:
    """Final RIMAN website generator with direct Elementor embedding"""
    
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
        
        return None
    
    def generate_service_cards_section(self, cards_config: List[Dict]) -> Dict:
        """Generate Service Cards section with 8 cards"""
        
        section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "gap": "extended",
                "content_position": "middle",
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
    
    def generate_wordpress_xml(self, config_path: str, output_path: str) -> str:
        """Generate complete WordPress XML with embedded Elementor data"""
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Generate Elementor sections
        elementor_sections = []
        
        for page_config in config.get('pages', []):
            if page_config.get('sections'):
                for section_config in page_config['sections']:
                    if section_config['type'] == 'hero_slider':
                        section = self.generate_hero_slider_section(section_config.get('slides', []))
                        if section:
                            elementor_sections.append(section)
                    elif section_config['type'] == 'service_cards':
                        section = self.generate_service_cards_section(section_config.get('cards', []))
                        if section:
                            elementor_sections.append(section)
        
        # Generate WordPress XML structure
        rss = self._create_wordpress_structure(config, elementor_sections)
        
        # Save XML file
        return self._save_xml(rss, output_path)
    
    def _create_wordpress_structure(self, config: Dict, elementor_sections: List) -> ET.Element:
        """Create complete WordPress XML structure"""
        
        # Register namespaces
        ET.register_namespace('excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
        ET.register_namespace('wfw', 'http://wellformedweb.org/CommentAPI/')
        ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
        ET.register_namespace('wp', 'http://wordpress.org/export/1.2/')
        
        # Create RSS root
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Add site information
        site = config.get('site', {})
        ET.SubElement(channel, 'title').text = site.get('title', 'Website')
        ET.SubElement(channel, 'link').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site.get('description', '')
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = site.get('language', 'en-US')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'generator').text = 'https://wordpress.org/?v=6.3'
        
        # Add author
        author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = '1'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = 'admin@riman-sanierung.de'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = 'RIMAN Admin'
        
        # Add categories
        for cat_data in config.get('categories', []):
            category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = str(cat_data.get('id'))
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = cat_data.get('slug')
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = cat_data.get('name')
        
        # Add main menu term
        for menu_data in config.get('menus', []):
            term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_id').text = str(menu_data.get('id'))
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'nav_menu'
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_slug').text = menu_data.get('slug')
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_name').text = menu_data.get('name')
        
        # Add media attachments
        self._add_media_attachments(channel, config)
        
        # Add main page with Elementor data
        self._add_main_page(channel, config, elementor_sections)
        
        # Add other pages
        self._add_other_pages(channel, config)
        
        # Add posts
        self._add_posts(channel, config)
        
        # Add menu items
        self._add_menu_items(channel, config)
        
        return rss
    
    def _add_media_attachments(self, channel: ET.Element, config: Dict):
        """Add media attachments"""
        for media_item in config.get('media', []):
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            url = media_item.get('url', '')
            title = media_item.get('title', 'Image')
            filename = url.split('/')[-1] if url else 'image.jpg'
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://localhost/?attachment_id={item_id}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = url
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = filename.split('.')[0]
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'inherit'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'attachment'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Attachment URL
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}attachment_url').text = url
            
            # Meta data
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_attached_file'
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = filename
            
            self.attachment_ids[url] = item_id
    
    def _add_main_page(self, channel: ET.Element, config: Dict, elementor_sections: List):
        """Add main page with Elementor data"""
        item_id = self.get_next_id()
        item = ET.SubElement(channel, 'item')
        
        # Get first page from config
        page = config.get('pages', [{}])[0]
        
        ET.SubElement(item, 'title').text = page.get('title', 'RIMAN Homepage')
        ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url', 'http://localhost')}"
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?page_id={item_id}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = 'startseite'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # Elementor data
        if elementor_sections:
            elementor_json = json.dumps(elementor_sections, separators=(',', ':'))
            
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = elementor_json
            
            # Elementor settings
            for key, value in [
                ('_elementor_edit_mode', 'builder'),
                ('_elementor_template_type', 'wp-page'),
                ('_wp_page_template', 'elementor_canvas')
            ]:
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
    
    def _add_other_pages(self, channel: ET.Element, config: Dict):
        """Add other pages"""
        pages = config.get('pages', [])[1:]  # Skip first page (already added)
        
        for page_config in pages:
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = page_config.get('title', 'Page')
            ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url')}/{page_config.get('slug', 'page')}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?page_id={item_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = page_config.get('content', '')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page_config.get('slug', 'page')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
    
    def _add_posts(self, channel: ET.Element, config: Dict):
        """Add blog posts"""
        for post_config in config.get('posts', []):
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = post_config.get('title', 'Post')
            ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url')}/{post_config.get('slug', 'post')}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = post_config.get('author', 'admin')
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?p={item_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = post_config.get('content', '')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = post_config.get('excerpt', '')
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = post_config.get('slug', 'post')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Categories
            for cat_slug in post_config.get('categories', ['uncategorized']):
                cat = ET.SubElement(item, 'category', domain='category', nicename=cat_slug)
                cat.text = cat_slug.replace('-', ' ').title()
    
    def _add_menu_items(self, channel: ET.Element, config: Dict):
        """Add navigation menu items"""
        menus = config.get('menus', [])
        if not menus:
            return
        
        main_menu = menus[0]
        menu_items = main_menu.get('items', [])
        
        for i, menu_item in enumerate(menu_items):
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = menu_item.get('title', 'Menu Item')
            ET.SubElement(item, 'link').text = menu_item.get('url', '#')
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?p={item_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(i + 1)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'nav_menu_item'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Menu category
            cat = ET.SubElement(item, 'category', domain='nav_menu', nicename=main_menu.get('slug', 'main-menu'))
            cat.text = main_menu.get('name', 'Main Menu')
            
            # Menu item meta
            meta_items = [
                ('_menu_item_type', menu_item.get('type', 'custom')),
                ('_menu_item_menu_item_parent', '0'),
                ('_menu_item_object', menu_item.get('object', 'custom')),
                ('_menu_item_object_id', str(item_id)),
                ('_menu_item_target', ''),
                ('_menu_item_classes', ''),
                ('_menu_item_xfn', ''),
                ('_menu_item_url', menu_item.get('url', '#'))
            ]
            
            for key, value in meta_items:
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
    
    def _save_xml(self, rss: ET.Element, output_path: str) -> str:
        """Save XML file with proper formatting"""
        
        # Convert to string
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Wrap important fields in CDATA
        import re
        
        # Wrap titles, names, etc in CDATA
        for tag in ['title', 'wp:post_name', 'wp:term_name', 'wp:term_slug', 'wp:cat_name']:
            xml_string = re.sub(
                f'<{tag}>([^<]+)</{tag}>',
                lambda m: f'<{tag}><![CDATA[{m.group(1)}]]></{tag}>' if not m.group(1).startswith('<![CDATA[') else m.group(0),
                xml_string
            )
        
        # Pretty format
        try:
            dom = minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
            
            lines = pretty_xml.decode('utf-8').split('\n')
            clean_lines = [line for line in lines if line.strip()]
            clean_xml = '\n'.join(clean_lines)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_xml)
        except Exception as e:
            print(f"Warning: Using fallback XML formatting: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                f.write(xml_string)
        
        return output_path


def main():
    """Generate final RIMAN website with Hero Slider + 8 Service Cards"""
    print("🚀 RIMAN FINAL Generator - Hero Slider + 8 Service Cards")
    print("=" * 70)
    
    generator = RimanFinalGenerator()
    
    config_file = 'riman_complete_config.yaml'
    output_file = 'riman_complete_final.xml'
    
    print(f"📖 Processing: {config_file}")
    
    try:
        # Generate WordPress XML with embedded Elementor data
        xml_output = generator.generate_wordpress_xml(config_file, output_file)
        
        # Get file size
        import os
        file_size = os.path.getsize(output_file) / 1024
        
        print(f"✅ Complete website generated: {xml_output}")
        print(f"📄 File size: {file_size:.1f} KB")
        print(f"📊 Total items: {generator.item_counter - 100}")
        
        print("\n🎯 What's included:")
        print("   • Hero Slider with rdn-slider widget (3 slides)")
        print("   • 8 Service Cards with cholot-texticon widgets")
        print("   • Complete WordPress structure (pages, posts, menus)")
        print("   • Media attachments for all images")
        print("   • Proper Elementor metadata")
        
        print("\n📋 Import Instructions:")
        print("1. Go to WordPress Admin > Tools > Import")
        print("2. Choose 'WordPress' importer")
        print("3. Upload riman_complete_final.xml")
        print("4. Import with 'Download and import file attachments' checked")
        print("5. The Hero Slider and Service Cards will be ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()