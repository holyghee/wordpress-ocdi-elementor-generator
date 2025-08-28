#!/usr/bin/env python3
"""
Enhanced WordPress Site Generator with Template and Content Merging
Generates complete WordPress XML with actual content from templates
"""

import xml.etree.ElementTree as ET
import json
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import copy

# Import the section processor for Elementor data
from section_based_processor import SectionBasedProcessor

class EnhancedSiteGenerator:
    def __init__(self, config_file: str):
        """Initialize with configuration file"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.item_counter = 10000  # Start from high ID to avoid conflicts
        self.attachment_ids = {}  # Map URLs to attachment IDs
        self.page_ids = {}  # Map page slugs to IDs
        self.processor = SectionBasedProcessor()
        self.processor.config = self.config  # Share config
    
    def get_next_id(self) -> int:
        """Get next available ID"""
        self.item_counter += 1
        return self.item_counter
    
    def generate(self, output_file: str):
        """Generate complete WordPress site XML"""
        # Create root RSS element
        root = ET.Element('rss', {
            'version': '2.0',
            'xmlns:excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:wfw': 'http://wellformedweb.org/CommentAPI/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:wp': 'http://wordpress.org/export/1.2/'
        })
        
        channel = ET.SubElement(root, 'channel')
        
        # Add site metadata
        self._add_site_metadata(channel)
        
        # Add attachments/media first
        print("📸 Adding media attachments...")
        self._add_media_items(channel)
        
        # Add categories
        print("📁 Adding categories...")
        self._add_category_items(channel)
        
        # Add pages with Elementor data
        print("📄 Adding pages with Elementor content...")
        self._add_page_items(channel)
        
        # Add posts
        print("📝 Adding blog posts...")
        self._add_post_items(channel)
        
        # Add menus
        print("📋 Adding navigation menus...")
        self._add_menu_items(channel)
        
        # Write to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        # Get file size
        size_kb = Path(output_file).stat().st_size / 1024
        
        # Count items
        total_items = len(root.findall('.//item'))
        
        print(f"📄 XML file size: {size_kb:.1f} KB")
        print(f"✅ Complete WordPress site generated: {output_file}")
        print(f"📊 Items: {total_items} total")
    
    def _add_site_metadata(self, channel: ET.Element):
        """Add site metadata to channel"""
        site = self.config.get('site', {})
        
        ET.SubElement(channel, 'title').text = site.get('title', 'WordPress Site')
        ET.SubElement(channel, 'link').text = site.get('url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site.get('description', 'WordPress Site')
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = 'en-US'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = site.get('url', 'http://localhost')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = site.get('url', 'http://localhost')
    
    def _load_template(self, template_path: str) -> List[Dict]:
        """Load Elementor template from JSON file"""
        if not template_path:
            return []
        
        template_file = Path(template_path)
        if not template_file.exists():
            print(f"⚠️ Template not found: {template_path}")
            return []
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _merge_content_with_template(self, template_data: List[Dict], custom_content: List[Dict]) -> List[Dict]:
        """Merge custom content into template structure"""
        if not custom_content:
            return template_data
        
        # Deep copy template to avoid modifying original
        result = copy.deepcopy(template_data)
        
        # Map of widget types to replace
        content_map = {}
        for content_item in custom_content:
            widget_type = content_item.get('widget_type')
            if widget_type:
                if widget_type not in content_map:
                    content_map[widget_type] = []
                content_map[widget_type].append(content_item)
        
        # Recursively update widgets in template
        def update_widgets(elements):
            for element in elements:
                if element.get('elType') == 'widget':
                    widget_type = element.get('widgetType')
                    
                    # Check if we have custom content for this widget type
                    if widget_type in content_map and content_map[widget_type]:
                        custom = content_map[widget_type].pop(0)
                        
                        # Merge settings
                        if 'settings' in custom:
                            element['settings'] = {**element.get('settings', {}), **custom['settings']}
                    
                    # Special handling for specific widget types
                    if widget_type == 'cholot-texticon' and 'settings' in element:
                        settings = element['settings']
                        # Look for matching content by title
                        for content_item in custom_content:
                            if content_item.get('widget_type') == 'cholot-texticon':
                                if content_item.get('title') == settings.get('title'):
                                    # Update with real content
                                    settings.update({
                                        'icon': content_item.get('icon', settings.get('icon', '')),
                                        'text': f"<p>{content_item.get('text', '')}</p>",
                                        'link': {'url': content_item.get('link', '#')}
                                    })
                                    break
                    
                    elif widget_type == 'rdn-slider' and 'settings' in element:
                        # Replace slider content
                        for content_item in custom_content:
                            if content_item.get('widget_type') == 'rdn-slider':
                                element['settings'].update(content_item.get('settings', {}))
                                break
                    
                    elif widget_type == 'cholot-team' and 'settings' in element:
                        # Replace team members
                        for content_item in custom_content:
                            if content_item.get('widget_type') == 'cholot-team':
                                element['settings'].update(content_item.get('settings', {}))
                                break
                    
                    elif widget_type == 'cholot-testimonial-two' and 'settings' in element:
                        # Replace testimonials
                        for content_item in custom_content:
                            if content_item.get('widget_type') == 'cholot-testimonial-two':
                                element['settings'].update(content_item.get('settings', {}))
                                break
                    
                    elif widget_type == 'cholot-contact' and 'settings' in element:
                        # Replace contact info
                        for content_item in custom_content:
                            if content_item.get('widget_type') == 'cholot-contact':
                                element['settings'].update(content_item.get('settings', {}))
                                break
                
                # Recursively process child elements
                if 'elements' in element:
                    update_widgets(element['elements'])
        
        update_widgets(result)
        return result
    
    def _add_page_items(self, channel: ET.Element):
        """Add WordPress pages with Elementor content"""
        pages = self.config.get('pages', [])
        
        for page_config in pages:
            item_id = page_config.get('id', self.get_next_id())
            slug = page_config.get('slug', '')
            
            # Store page ID for menu references
            if slug:
                self.page_ids[slug] = item_id
            
            item = ET.SubElement(channel, 'item')
            
            # Basic page info
            ET.SubElement(item, 'title').text = page_config.get('title', 'Untitled Page')
            ET.SubElement(item, 'link').text = f"{self.config['site']['url']}/{slug}/"
            ET.SubElement(item, 'pubDate').text = 'Wed, 21 Aug 2024 14:29:21 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = '<![CDATA[admin]]>'
            ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"{self.config['site']['url']}/?page_id={item_id}"
            ET.SubElement(item, 'description').text = ''
            
            # Content
            content = page_config.get('content', '')
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = f'<![CDATA[{content}]]>'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = '<![CDATA[]]>'
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            past_date = datetime(2024, 8, 21, 14, 29, 21)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = slug
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Process Elementor data
            elementor_data = []
            
            # Load template if specified
            if page_config.get('elementor_template'):
                elementor_data = self._load_template(page_config['elementor_template'])
            
            # Merge with custom content if provided
            if page_config.get('elementor_content'):
                if elementor_data:
                    elementor_data = self._merge_content_with_template(
                        elementor_data, 
                        page_config['elementor_content']
                    )
                else:
                    # Convert custom content to Elementor format
                    elementor_data = self._convert_content_to_elementor(page_config['elementor_content'])
            
            # Use sections if no template or content
            if not elementor_data and page_config.get('sections'):
                elementor_data = self.processor._create_sections_page({'pages': [page_config]})
            
            # Add Elementor metadata
            if elementor_data:
                clean_json = json.dumps(elementor_data, separators=(',', ':'))
                
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'<![CDATA[{clean_json}]]>'
                
                # Elementor settings
                for key, value in [
                    ('_elementor_edit_mode', 'builder'),
                    ('_elementor_template_type', 'wp-page'),
                    ('_wp_page_template', page_config.get('template', 'elementor_canvas'))
                ]:
                    meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'<![CDATA[{value}]]>'
    
    def _convert_content_to_elementor(self, content_items: List[Dict]) -> List[Dict]:
        """Convert simplified content format to Elementor structure"""
        sections = []
        current_section = None
        
        for item in content_items:
            if item.get('widget_type') == 'section':
                # Create a new section
                current_section = {
                    'id': self._generate_element_id(),
                    'elType': 'section',
                    'settings': item.get('settings', {}),
                    'elements': [{
                        'id': self._generate_element_id(),
                        'elType': 'column',
                        'settings': {'_column_size': 100},
                        'elements': []
                    }]
                }
                sections.append(current_section)
                
                # Process child elements
                if 'elements' in item:
                    for element in item['elements']:
                        widget = self._create_widget(element)
                        if widget:
                            current_section['elements'][0]['elements'].append(widget)
            else:
                # Create widget directly
                if not current_section:
                    # Create default section
                    current_section = {
                        'id': self._generate_element_id(),
                        'elType': 'section',
                        'settings': {},
                        'elements': [{
                            'id': self._generate_element_id(),
                            'elType': 'column',
                            'settings': {'_column_size': 100},
                            'elements': []
                        }]
                    }
                    sections.append(current_section)
                
                widget = self._create_widget(item)
                if widget:
                    current_section['elements'][0]['elements'].append(widget)
        
        return sections
    
    def _create_widget(self, item: Dict) -> Optional[Dict]:
        """Create Elementor widget from content item"""
        widget_type = item.get('widget_type', item.get('type', ''))
        if not widget_type:
            return None
        
        widget = {
            'id': self._generate_element_id(),
            'elType': 'widget',
            'widgetType': widget_type,
            'settings': item.get('settings', {})
        }
        
        # Add specific widget data
        if widget_type == 'cholot-texticon':
            widget['settings'].update({
                'icon': item.get('icon', 'fa fa-child'),
                'title': item.get('title', ''),
                'subtitle': item.get('subtitle', ''),
                'text': f"<p>{item.get('text', '')}</p>",
                'link': {'url': item.get('link', '#')}
            })
        
        return widget
    
    def _generate_element_id(self) -> str:
        """Generate unique Elementor element ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    def _add_media_items(self, channel: ET.Element):
        """Add media attachments"""
        media = self.config.get('media', [])
        
        for media_item in media:
            url = media_item.get('url')
            if url:
                attachment_id = self._add_attachment_item(channel, media_item)
                self.attachment_ids[url] = attachment_id
    
    def _add_attachment_item(self, channel: ET.Element, media_data: Dict) -> int:
        """Add single attachment item"""
        item_id = media_data.get('id', self.get_next_id())
        item = ET.SubElement(channel, 'item')
        
        title = media_data.get('title', 'Image')
        url = media_data.get('url', '')
        filename = media_data.get('filename', 'image.jpg')
        
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = url
        ET.SubElement(item, 'pubDate').text = 'Wed, 21 Aug 2024 14:29:21 +0000'
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = '<![CDATA[admin]]>'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = url
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = '<![CDATA[]]>'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = '<![CDATA[]]>'
        
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
        past_date = datetime(2024, 8, 21, 14, 29, 21)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'inherit'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'attachment'
        
        # Attachment metadata
        meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_attached_file'
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'<![CDATA[2024/08/{filename}]]>'
        
        meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_attachment_metadata'
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'<![CDATA[a:1:{{s:4:"file";s:19:"2024/08/{filename}";}}]]>'
        
        return item_id
    
    def _add_category_items(self, channel: ET.Element):
        """Add category items"""
        categories = self.config.get('categories', [])
        
        for cat in categories:
            cat_id = cat.get('id', self.get_next_id())
            
            wp_cat = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
            ET.SubElement(wp_cat, '{http://wordpress.org/export/1.2/}term_id').text = str(cat_id)
            ET.SubElement(wp_cat, '{http://wordpress.org/export/1.2/}category_nicename').text = cat.get('slug', '')
            ET.SubElement(wp_cat, '{http://wordpress.org/export/1.2/}cat_name').text = f'<![CDATA[{cat.get("name", "")}]]>'
    
    def _add_post_items(self, channel: ET.Element):
        """Add blog post items"""
        posts = self.config.get('posts', [])
        
        for post_config in posts:
            item_id = post_config.get('id', self.get_next_id())
            slug = post_config.get('slug', '')
            
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = post_config.get('title', 'Untitled Post')
            ET.SubElement(item, 'link').text = f"{self.config['site']['url']}/{slug}/"
            ET.SubElement(item, 'pubDate').text = 'Wed, 21 Aug 2024 14:29:21 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = '<![CDATA[admin]]>'
            ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"{self.config['site']['url']}/?p={item_id}"
            ET.SubElement(item, 'description').text = ''
            
            content = post_config.get('content', '')
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = f'<![CDATA[{content}]]>'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = '<![CDATA[]]>'
            
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            past_date = datetime(2024, 8, 21, 14, 29, 21)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = slug
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Categories
            for cat_name in post_config.get('categories', []):
                cat_elem = ET.SubElement(item, 'category', {
                    'domain': 'category',
                    'nicename': cat_name.lower().replace(' ', '-')
                })
                cat_elem.text = f'<![CDATA[{cat_name}]]>'
    
    def _add_menu_items(self, channel: ET.Element):
        """Add navigation menu items"""
        menus = self.config.get('menus', [])
        
        for menu in menus:
            # Add menu term
            menu_id = menu.get('id', self.get_next_id())
            
            wp_term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
            ET.SubElement(wp_term, '{http://wordpress.org/export/1.2/}term_id').text = str(menu_id)
            ET.SubElement(wp_term, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'nav_menu'
            ET.SubElement(wp_term, '{http://wordpress.org/export/1.2/}term_slug').text = menu.get('slug', 'menu')
            ET.SubElement(wp_term, '{http://wordpress.org/export/1.2/}term_name').text = f'<![CDATA[{menu.get("name", "Menu")}]]>'
            
            # Add menu items
            for menu_item in menu.get('items', []):
                self._add_menu_item(channel, menu_item, menu_id)
    
    def _add_menu_item(self, channel: ET.Element, menu_item: Dict, menu_id: int):
        """Add individual menu item"""
        item_id = menu_item.get('id', self.get_next_id())
        
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = menu_item.get('title', '')
        ET.SubElement(item, 'link').text = f"{self.config['site']['url']}/"
        ET.SubElement(item, 'pubDate').text = 'Wed, 21 Aug 2024 14:29:21 +0000'
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = '<![CDATA[admin]]>'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"{self.config['site']['url']}/?p={item_id}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = '<![CDATA[]]>'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = '<![CDATA[]]>'
        
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
        past_date = datetime(2024, 8, 21, 14, 29, 21)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = str(item_id)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(menu_item.get('order', 0))
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'nav_menu_item'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        
        # Menu term relationship
        cat_elem = ET.SubElement(item, 'category', {
            'domain': 'nav_menu',
            'nicename': menu.get('slug', 'menu')
        })
        cat_elem.text = f'<![CDATA[{menu.get("name", "Menu")}]]>'
        
        # Menu item metadata
        object_type = menu_item.get('object_type', 'page')
        object_id = menu_item.get('object_id', 0)
        
        # Map to actual page IDs if referencing pages
        if object_type == 'page':
            for page in self.config.get('pages', []):
                if page.get('id') == object_id:
                    break
        
        meta_fields = [
            ('_menu_item_type', 'post_type'),
            ('_menu_item_menu_item_parent', str(menu_item.get('parent', 0))),
            ('_menu_item_object_id', str(object_id)),
            ('_menu_item_object', object_type),
            ('_menu_item_target', ''),
            ('_menu_item_classes', 'a:1:{i:0;s:0:"";}'),
            ('_menu_item_xfn', ''),
            ('_menu_item_url', '')
        ]
        
        for key, value in meta_fields:
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'<![CDATA[{value}]]>'


def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python enhanced_site_generator.py <config.yaml> <output.xml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(config_file).exists():
        print(f"❌ Configuration file not found: {config_file}")
        sys.exit(1)
    
    print("🚀 Enhanced WordPress Site Generator")
    print("=" * 60)
    print(f"📖 Loading configuration: {config_file}")
    
    generator = EnhancedSiteGenerator(config_file)
    generator.generate(output_file)


if __name__ == "__main__":
    main()