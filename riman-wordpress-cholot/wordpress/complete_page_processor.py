#!/usr/bin/env python3
"""
Complete Page Processor
Generates full Elementor pages with Kit settings like cholot-fixed-urls.xml
"""

import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import html

class CompletePageProcessor:
    def __init__(self):
        # Load original template
        self.load_template()
        
    def load_template(self):
        """Load the original Elementor template"""
        template_path = Path('/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json')
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template = json.load(f)
        else:
            # Try local copy
            local_path = Path('original-template.json')
            if local_path.exists():
                with open(local_path, 'r', encoding='utf-8') as f:
                    self.template = json.load(f)
            else:
                raise FileNotFoundError("Template file not found")
    
    def process_yaml_input(self, yaml_path: str) -> Dict[str, Any]:
        """Process YAML input and generate complete page data"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Import the converter
        from yaml_to_elementor_converter import YamlToElementorConverter
        converter = YamlToElementorConverter()
        
        # Generate Elementor content
        elementor_json = converter.convert_yaml_to_elementor(yaml_path)
        
        return {
            'config': config,
            'elementor_data': elementor_json['content']
        }
    
    def generate_wordpress_xml(self, data: Dict[str, Any], output_path: str):
        """Generate complete WordPress XML with Kit and Page"""
        config = data['config']
        elementor_data = data['elementor_data']
        
        # Create XML structure
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        
        # Add namespaces
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Site info
        site = config.get('site', {})
        ET.SubElement(channel, 'title').text = site.get('title', 'Website')
        ET.SubElement(channel, 'link').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site.get('description', '')
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = site.get('language', 'en-US')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = site.get('base_url', 'http://localhost')
        
        # Add author
        author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = '1'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = 'admin@example.com'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = 'Administrator'
        
        # Add categories and terms
        self.add_categories_and_terms(channel)
        
        # Add Default Kit
        self.add_default_kit(channel, config)
        
        # Add Page with Elementor data
        self.add_page(channel, config, elementor_data)
        
        # Format and save XML
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Pretty print
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
        
        # Remove extra blank lines
        lines = pretty_xml.decode('utf-8').split('\n')
        clean_lines = [line for line in lines if line.strip()]
        clean_xml = '\n'.join(clean_lines)
        
        # Add XML declaration and comment
        final_xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'
        final_xml += '<!-- Generated WordPress XML using Complete Page Processor -->\n'
        final_xml += clean_xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_xml)
        
        print(f"✅ Generated WordPress XML: {output_path}")
        print(f"📄 File size: {len(final_xml):,} characters")
    
    def add_categories_and_terms(self, channel):
        """Add WordPress categories and Elementor terms"""
        # Add category
        category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = '1'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = 'uncategorized'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = 'Uncategorized'
        
        # Add Elementor page term
        term1 = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
        ET.SubElement(term1, '{http://wordpress.org/export/1.2/}term_id').text = '2'
        ET.SubElement(term1, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'elementor_library_type'
        ET.SubElement(term1, '{http://wordpress.org/export/1.2/}term_slug').text = 'page'
        ET.SubElement(term1, '{http://wordpress.org/export/1.2/}term_parent').text = ''
        ET.SubElement(term1, '{http://wordpress.org/export/1.2/}term_name').text = 'page'
        
        # Add Elementor kit term
        term2 = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
        ET.SubElement(term2, '{http://wordpress.org/export/1.2/}term_id').text = '3'
        ET.SubElement(term2, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'elementor_library_type'
        ET.SubElement(term2, '{http://wordpress.org/export/1.2/}term_slug').text = 'kit'
        ET.SubElement(term2, '{http://wordpress.org/export/1.2/}term_parent').text = ''
        ET.SubElement(term2, '{http://wordpress.org/export/1.2/}term_name').text = 'kit'
    
    def add_default_kit(self, channel, config):
        """Add Elementor Default Kit settings"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = 'Default Kit'
        ET.SubElement(item, 'link').text = config['site']['base_url'] + '/?elementor_library=default-kit'
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        
        guid = ET.SubElement(item, 'guid', isPermaLink='false')
        guid.text = config['site']['base_url'] + '/?post_type=elementor_library&p=99'
        
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post metadata
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = '99'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = 'default-kit'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'elementor_library'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # Category
        cat = ET.SubElement(item, 'category', domain='elementor_library_type', nicename='kit')
        cat.text = 'kit'
        
        # Kit settings
        elementor_settings = config.get('pages', [{}])[0].get('elementor_settings', {})
        
        kit_settings = {
            "system_colors": [
                {"_id": "primary", "title": "Primary", "color": elementor_settings.get('primary_color', '#b68c2f')},
                {"_id": "secondary", "title": "Secondary", "color": elementor_settings.get('secondary_color', '#232323')},
                {"_id": "text", "title": "Text", "color": elementor_settings.get('text_color', '#7A7A7A')},
                {"_id": "accent", "title": "Accent", "color": "#61CE70"}
            ],
            "custom_colors": [],
            "system_typography": [
                {"_id": "primary", "title": "Primary", "typography_typography": "custom"},
                {"_id": "secondary", "title": "Secondary", "typography_typography": "custom"},
                {"_id": "text", "title": "Text", "typography_typography": "custom"},
                {"_id": "accent", "title": "Accent", "typography_typography": "custom"}
            ],
            "custom_typography": [],
            "default_generic_fonts": "Sans-serif",
            "site_name": config['site'].get('title', 'Website'),
            "site_description": config['site'].get('description', ''),
            "container_width": {"size": elementor_settings.get('container_width', 1140), "unit": "px"},
            "space_between_widgets": {"size": 20, "unit": "px"}
        }
        
        # Add postmeta
        self.add_postmeta(item, '_elementor_edit_mode', 'builder')
        self.add_postmeta(item, '_elementor_template_type', 'kit')
        self.add_postmeta(item, '_elementor_version', '3.15.0')
        self.add_postmeta(item, '_elementor_page_settings', json.dumps(kit_settings, ensure_ascii=False))
    
    def add_page(self, channel, config, elementor_data):
        """Add the main page with Elementor content"""
        item = ET.SubElement(channel, 'item')
        
        page = config.get('pages', [{}])[0]
        
        ET.SubElement(item, 'title').text = page.get('title', 'Page')
        ET.SubElement(item, 'link').text = config['site']['base_url'] + '/' + page.get('slug', 'page') + '/'
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        
        guid = ET.SubElement(item, 'guid', isPermaLink='false')
        guid.text = config['site']['base_url'] + '/?page_id=1482'
        
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post metadata
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = '1482'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page.get('slug', 'page')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = page.get('status', 'publish')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # Add postmeta
        self.add_postmeta(item, '_elementor_edit_mode', 'builder')
        self.add_postmeta(item, '_elementor_template_type', 'page')
        self.add_postmeta(item, '_elementor_version', '3.15.0')
        self.add_postmeta(item, '_wp_page_template', page.get('template', 'elementor_canvas'))
        
        # Add Elementor data - this is the key!
        elementor_json = json.dumps(elementor_data, ensure_ascii=False, separators=(',', ':'))
        self.add_postmeta(item, '_elementor_data', elementor_json)
        
        # Add page settings if available
        if hasattr(self, 'template') and 'page_settings' in self.template:
            self.add_postmeta(item, '_elementor_page_settings', json.dumps(self.template['page_settings'], ensure_ascii=False))
        
        # SEO metadata if provided
        seo = page.get('seo', {})
        if seo.get('meta_title'):
            self.add_postmeta(item, '_yoast_wpseo_title', seo['meta_title'])
        if seo.get('meta_description'):
            self.add_postmeta(item, '_yoast_wpseo_metadesc', seo['meta_description'])
    
    def add_postmeta(self, item, key, value):
        """Add postmeta to item"""
        postmeta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_key').text = key
        ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_value').text = value

def main():
    """Main execution"""
    print("🚀 Complete Page Processor")
    print("=" * 50)
    
    processor = CompletePageProcessor()
    
    # Process YAML input
    data = processor.process_yaml_input('riman_input.yaml')
    
    # Generate WordPress XML
    processor.generate_wordpress_xml(data, 'riman_complete.xml')
    
    # Check file size
    import os
    file_size = os.path.getsize('riman_complete.xml')
    print(f"📦 XML file size: {file_size / 1024:.1f} KB")
    
    # Count sections and widgets
    elementor_data = data['elementor_data']
    widget_count = 0
    for section in elementor_data:
        for col in section.get('elements', []):
            for elem in col.get('elements', []):
                if elem.get('widgetType'):
                    widget_count += 1
                elif elem.get('elType') == 'section':
                    for subcol in elem.get('elements', []):
                        for widget in subcol.get('elements', []):
                            if widget.get('widgetType'):
                                widget_count += 1
    
    print(f"📊 Sections: {len(elementor_data)}")
    print(f"🎨 Widgets: {widget_count}")
    print(f"✅ Ready for WordPress import!")

if __name__ == '__main__':
    main()