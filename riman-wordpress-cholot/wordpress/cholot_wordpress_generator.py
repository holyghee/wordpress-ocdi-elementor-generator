#!/usr/bin/env python3
"""
Cholot WordPress Generator - Uses our fixed YAML processor to generate WordPress XML with Cholot widgets
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List
import uuid

from yaml_to_json_processor import YAMLToJSONProcessor

class CholotWordPressGenerator:
    def __init__(self):
        self.item_counter = 100
        self.attachment_ids = {}
        
    def get_next_id(self) -> int:
        self.item_counter += 1
        return self.item_counter
    
    def generate_wordpress_xml(self, yaml_path: str, output_path: str) -> str:
        """Generate WordPress XML from YAML with Cholot widgets"""
        
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Process with our YAML processor
        processor = YAMLToJSONProcessor(debug=True)
        processed_data = processor.process_yaml_data(config)
        
        # Create WordPress XML structure
        rss = self._create_rss_structure(config, processed_data)
        
        # Save XML file
        self._save_xml(rss, output_path)
        
        return output_path
    
    def _create_rss_structure(self, config: Dict, processed_data: Dict) -> ET.Element:
        """Create WordPress RSS structure"""
        # Register namespaces
        ET.register_namespace('wp', 'http://wordpress.org/export/1.2/')
        ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
        ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
        
        # Create RSS root
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Add site info
        self._add_site_info(channel, config)
        
        # Add authors
        self._add_authors(channel)
        
        # Add pages with Cholot Elementor data
        self._add_pages_with_cholot_data(channel, processed_data)
        
        return rss
    
    def _add_site_info(self, channel: ET.Element, config: Dict):
        """Add site information"""
        site = config.get('site', {})
        ET.SubElement(channel, 'title').text = site.get('name', 'Website')
        ET.SubElement(channel, 'link').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site.get('description', '')
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = site.get('language', 'en-US')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'generator').text = 'https://wordpress.org/?v=6.3'
    
    def _add_authors(self, channel: ET.Element):
        """Add default admin author"""
        author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = '1'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = 'admin@example.com'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = 'Admin'
    
    def _add_pages_with_cholot_data(self, channel: ET.Element, processed_data: Dict):
        """Add pages with processed Cholot Elementor data"""
        pages = processed_data.get('pages', [])
        
        for page_data in pages:
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            # Basic page information
            ET.SubElement(item, 'title').text = page_data.get('title', 'Page')
            ET.SubElement(item, 'link').text = f"http://localhost:8082/{page_data.get('slug', 'page')}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost:8082/?page_id={item_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = '<!-- wp:html --><!-- /wp:html -->'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            past_date = datetime(2024, 8, 28, 14, 29, 21)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page_data.get('slug', 'page')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = page_data.get('status', 'publish')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Add Elementor data with our Cholot widgets
            elementor_data = page_data.get('elementor_data', [])
            if elementor_data:
                clean_json = json.dumps(elementor_data, separators=(',', ':'))
                
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = clean_json
                
                # Elementor settings
                for key, value in [
                    ('_elementor_edit_mode', 'builder'),
                    ('_elementor_template_type', 'wp-page'),
                    ('_wp_page_template', 'elementor_canvas')
                ]:
                    meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
    
    def _save_xml(self, rss: ET.Element, output_path: str):
        """Save XML with proper formatting"""
        try:
            # Convert to string
            xml_string = ET.tostring(rss, encoding='unicode')
            
            # Parse and format
            dom = minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
            
            # Clean up empty lines
            lines = pretty_xml.decode('utf-8').split('\n')
            clean_lines = [line for line in lines if line.strip()]
            clean_xml = '\n'.join(clean_lines)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_xml)
                
        except Exception as e:
            print(f"Warning: Using fallback XML formatting: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                f.write(ET.tostring(rss, encoding='unicode'))


def main():
    """Main function"""
    import sys
    import os
    
    print("🚀 Cholot WordPress Generator")
    print("=" * 60)
    
    generator = CholotWordPressGenerator()
    
    # Get YAML file from command line or use default
    yaml_file = sys.argv[1] if len(sys.argv) > 1 else 'working_riman.yaml'
    output_file = yaml_file.replace('.yaml', '_cholot.xml').replace('.yml', '_cholot.xml')
    
    print(f"📖 Loading configuration: {yaml_file}")
    
    # Generate WordPress XML with Cholot widgets
    result_path = generator.generate_wordpress_xml(yaml_file, output_file)
    
    # Statistics
    file_size = os.path.getsize(result_path)
    print(f"📄 XML file size: {file_size / 1024:.1f} KB")
    print(f"✅ Cholot WordPress site generated: {result_path}")
    
    # Check for Cholot widgets
    with open(result_path, 'r') as f:
        content = f.read()
        cholot_count = content.count('cholot-')
        print(f"🎨 Found {cholot_count} Cholot widgets in XML")


if __name__ == "__main__":
    main()