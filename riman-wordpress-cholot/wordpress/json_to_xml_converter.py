#!/usr/bin/env python3
"""
JSON to WordPress XML Converter
===============================
Converts Elementor JSON (from yaml_to_json_processor.py) to WordPress WXR format 
for importing into WordPress with the Importer plugin.

Features:
- Generates valid WordPress WXR (eXtended RSS) format
- Properly encodes Elementor data as JSON in _elementor_data meta field
- Creates importable pages with correct post structure
- Handles special characters and CDATA sections
- Generates unique post IDs and proper timestamps
- Includes all necessary WordPress fields and meta data
- Supports Elementor version compatibility
"""

import json
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import datetime
import html
import re
import uuid
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class WordPressConfig:
    """Configuration for WordPress XML generation"""
    site_title: str = "Generated Site"
    site_url: str = "http://localhost"
    description: str = "Generated from Elementor JSON"
    language: str = "en-US"
    author_id: int = 1
    author_login: str = "admin"
    author_email: str = "admin@example.com"
    author_display_name: str = "admin"
    elementor_version: str = "3.15.3"
    
    def __post_init__(self):
        """Ensure URL doesn't end with slash"""
        self.site_url = self.site_url.rstrip('/')


class WordPressXMLGenerator:
    """Generates WordPress WXR XML from Elementor JSON data"""
    
    WXR_VERSION = "1.2"
    GENERATOR = "WordPress/6.3"
    
    def __init__(self, config: WordPressConfig = None):
        self.config = config or WordPressConfig()
        self.post_id_counter = 1000
        
    def convert_json_to_xml(self, json_data: Dict[str, Any]) -> str:
        """Convert JSON data to WordPress XML string"""
        try:
            # Extract data
            site_info = json_data.get('site', {})
            pages = json_data.get('pages', [])
            
            # Update config from site info
            self._update_config_from_site_info(site_info)
            
            # Create XML structure
            root = self._create_xml_root()
            channel = self._create_channel(root)
            
            # Add author
            self._add_author(channel)
            
            # Add pages as WordPress posts
            for page_data in pages:
                self._add_page_item(channel, page_data)
            
            # Generate XML string
            xml_string = self._format_xml(root)
            
            logger.info(f"Generated WordPress XML with {len(pages)} pages")
            return xml_string
            
        except Exception as e:
            logger.error(f"Error converting JSON to XML: {str(e)}")
            raise
    
    def _update_config_from_site_info(self, site_info: Dict[str, Any]):
        """Update configuration from site information"""
        if 'title' in site_info:
            self.config.site_title = site_info['title']
        if 'base_url' in site_info:
            self.config.site_url = site_info['base_url'].rstrip('/')
        if 'description' in site_info:
            self.config.description = site_info['description']
        if 'language' in site_info:
            self.config.language = site_info['language']
    
    def _create_xml_root(self) -> ET.Element:
        """Create XML root with proper namespaces"""
        root = ET.Element('rss', {
            'version': '2.0',
            'xmlns:excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:wfw': 'http://wellformedweb.org/CommentAPI/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:wp': 'http://wordpress.org/export/1.2/'
        })
        
        # Add XML comment
        comment_text = """
This is a WordPress eXtended RSS file generated as an export of your site.
It contains information about your site's posts, pages, comments, categories, and other content.
You may use this file to transfer that content from one site to another.
This file is not intended to serve as a complete backup of your site.

To import this information into a WordPress site follow these steps:
1. Log in to that site as an administrator.
2. Go to Tools: Import in the WordPress admin panel.
3. Install the "WordPress" importer from the list.
4. Activate & Run Importer.
5. Upload this file using the form provided on that page.
6. You will first be asked to map the authors in this export file to users
   on the site. For each author, you may choose to map to an
   existing user on the site or to create a new user.
7. WordPress will then import each of the posts, pages, comments, categories, etc.
   contained in this file into your site.
"""
        
        return root
    
    def _create_channel(self, root: ET.Element) -> ET.Element:
        """Create channel element with site information"""
        channel = ET.SubElement(root, 'channel')
        
        # Basic site information
        ET.SubElement(channel, 'title').text = self.config.site_title
        ET.SubElement(channel, 'link').text = self.config.site_url
        ET.SubElement(channel, 'description').text = self.config.description
        ET.SubElement(channel, 'pubDate').text = self._get_current_rfc2822()
        ET.SubElement(channel, 'language').text = self.config.language
        
        # WordPress specific fields
        ET.SubElement(channel, 'wp:wxr_version').text = self.WXR_VERSION
        ET.SubElement(channel, 'wp:base_site_url').text = self.config.site_url
        ET.SubElement(channel, 'wp:base_blog_url').text = self.config.site_url
        
        # Generator comment
        generator = ET.Comment(f' generator="{self.GENERATOR}" created="{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}" ')
        channel.insert(0, generator)
        
        return channel
    
    def _add_author(self, channel: ET.Element):
        """Add author information"""
        author = ET.SubElement(channel, 'wp:author')
        ET.SubElement(author, 'wp:author_id').text = str(self.config.author_id)
        ET.SubElement(author, 'wp:author_login').text = self.config.author_login
        ET.SubElement(author, 'wp:author_email').text = self.config.author_email
        ET.SubElement(author, 'wp:author_display_name').text = self.config.author_display_name
        ET.SubElement(author, 'wp:author_first_name').text = ""
        ET.SubElement(author, 'wp:author_last_name').text = ""
    
    def _add_page_item(self, channel: ET.Element, page_data: Dict[str, Any]):
        """Add page as WordPress item"""
        try:
            # Generate unique post ID
            post_id = self.post_id_counter
            self.post_id_counter += 1
            
            # Extract page information
            title = page_data.get('title', 'Untitled Page')
            slug = page_data.get('slug', f'page-{post_id}')
            status = page_data.get('status', 'publish')
            elementor_data = page_data.get('elementor_data', [])
            
            # Create item
            item = ET.SubElement(channel, 'item')
            
            # Basic post fields
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"{self.config.site_url}/{slug}/"
            ET.SubElement(item, 'pubDate').text = self._get_current_rfc2822()
            ET.SubElement(item, 'dc:creator').text = self.config.author_login
            ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"{self.config.site_url}/?page_id={post_id}"
            ET.SubElement(item, 'description').text = ""
            
            # Content (empty for Elementor pages)
            content_encoded = ET.SubElement(item, 'content:encoded')
            content_encoded.text = ""
            
            # Excerpt
            excerpt_encoded = ET.SubElement(item, 'excerpt:encoded')
            excerpt_encoded.text = ""
            
            # WordPress post fields
            ET.SubElement(item, 'wp:post_id').text = str(post_id)
            ET.SubElement(item, 'wp:post_date').text = self._get_current_mysql_datetime()
            ET.SubElement(item, 'wp:post_date_gmt').text = self._get_current_mysql_datetime()
            ET.SubElement(item, 'wp:comment_status').text = "closed"
            ET.SubElement(item, 'wp:ping_status').text = "closed"
            ET.SubElement(item, 'wp:post_name').text = slug
            ET.SubElement(item, 'wp:status').text = status
            ET.SubElement(item, 'wp:post_parent').text = "0"
            ET.SubElement(item, 'wp:menu_order').text = "0"
            ET.SubElement(item, 'wp:post_type').text = "page"
            ET.SubElement(item, 'wp:post_password').text = ""
            ET.SubElement(item, 'wp:is_sticky').text = "0"
            
            # Add Elementor meta data
            self._add_elementor_meta(item, elementor_data)
            
            logger.debug(f"Added page '{title}' with post ID {post_id}")
            
        except Exception as e:
            logger.error(f"Error adding page item: {str(e)}")
            raise
    
    def _add_elementor_meta(self, item: ET.Element, elementor_data: List[Dict[str, Any]]):
        """Add Elementor-specific meta fields"""
        
        # Add _elementor_edit_mode meta
        edit_mode_meta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(edit_mode_meta, 'wp:meta_key').text = '_elementor_edit_mode'
        ET.SubElement(edit_mode_meta, 'wp:meta_value').text = 'builder'
        
        # Add _elementor_template_type meta
        template_type_meta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(template_type_meta, 'wp:meta_key').text = '_elementor_template_type'
        ET.SubElement(template_type_meta, 'wp:meta_value').text = 'wp-page'
        
        # Add _elementor_version meta
        version_meta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(version_meta, 'wp:meta_key').text = '_elementor_version'
        ET.SubElement(version_meta, 'wp:meta_value').text = self.config.elementor_version
        
        # Add _elementor_data meta (the main Elementor content)
        if elementor_data:
            data_meta = ET.SubElement(item, 'wp:postmeta')
            ET.SubElement(data_meta, 'wp:meta_key').text = '_elementor_data'
            
            # Convert elementor data to JSON string and escape for XML
            json_data = json.dumps(elementor_data, separators=(',', ':'), ensure_ascii=False)
            
            # Escape the JSON for XML CDATA
            escaped_json = self._escape_for_xml(json_data)
            
            meta_value = ET.SubElement(data_meta, 'wp:meta_value')
            meta_value.text = escaped_json
        
        # Add _elementor_page_settings meta (empty but required)
        page_settings_meta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(page_settings_meta, 'wp:meta_key').text = '_elementor_page_settings'
        ET.SubElement(page_settings_meta, 'wp:meta_value').text = '[]'
        
        # Add _elementor_css meta (empty)
        css_meta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(css_meta, 'wp:meta_key').text = '_elementor_css'
        ET.SubElement(css_meta, 'wp:meta_value').text = ''
    
    def _escape_for_xml(self, text: str) -> str:
        """Escape text for XML while preserving JSON structure"""
        # Replace problematic characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        
        # Handle backslashes in URLs and paths
        text = re.sub(r'\\/', '/', text)
        
        return text
    
    def _get_current_rfc2822(self) -> str:
        """Get current time in RFC 2822 format"""
        return datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %z')
    
    def _get_current_mysql_datetime(self) -> str:
        """Get current time in MySQL datetime format"""
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _format_xml(self, root: ET.Element) -> str:
        """Format XML with proper indentation and encoding"""
        # Convert to string with minidom for pretty printing
        rough_string = ET.tostring(root, encoding='unicode')
        
        # Parse with minidom for pretty printing
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Clean up extra blank lines and encoding issues
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        
        # Ensure proper XML declaration
        if not lines[0].startswith('<?xml'):
            lines.insert(0, '<?xml version="1.0" encoding="UTF-8" ?>')
        else:
            lines[0] = '<?xml version="1.0" encoding="UTF-8" ?>'
        
        # Add WordPress XML comments
        xml_comment = [
            '<!-- This is a WordPress eXtended RSS file generated by WordPress as an export of your site. -->',
            '<!-- It contains information about your site\'s posts, pages, comments, categories, and other content. -->',
            '<!-- You may use this file to transfer that content from one site to another. -->',
            '<!-- This file is not intended to serve as a complete backup of your site. -->',
            '',
            '<!-- To import this information into a WordPress site follow these steps: -->',
            '<!-- 1. Log in to that site as an administrator. -->',
            '<!-- 2. Go to Tools: Import in the WordPress admin panel. -->',
            '<!-- 3. Install the "WordPress" importer from the list. -->',
            '<!-- 4. Activate & Run Importer. -->',
            '<!-- 5. Upload this file using the form provided on that page. -->',
            '<!-- 6. You will first be asked to map the authors in this export file to users -->',
            '<!--    on the site. For each author, you may choose to map to an -->',
            '<!--    existing user on the site or to create a new user. -->',
            '<!-- 7. WordPress will then import each of the posts, pages, comments, categories, etc. -->',
            '<!--    contained in this file into your site. -->',
            ''
        ]
        
        # Insert comments after XML declaration
        lines = lines[:1] + xml_comment + lines[1:]
        
        return '\n'.join(lines)


class JSONToXMLConverter:
    """Main converter class"""
    
    def __init__(self, config: WordPressConfig = None):
        self.config = config or WordPressConfig()
        self.generator = WordPressXMLGenerator(config)
        
        logger.info("JSON to XML Converter initialized")
    
    def convert_file(self, input_json_file: str, output_xml_file: str):
        """Convert JSON file to WordPress XML file"""
        try:
            # Read JSON data
            with open(input_json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            logger.info(f"Loaded JSON data from {input_json_file}")
            
            # Convert to XML
            xml_content = self.generator.convert_json_to_xml(json_data)
            
            # Write XML file
            with open(output_xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            logger.info(f"Generated WordPress XML: {output_xml_file}")
            
            # Validate the output
            if self._validate_xml(output_xml_file):
                logger.info("XML validation passed")
            else:
                logger.warning("XML validation failed - check the output file")
            
        except FileNotFoundError:
            logger.error(f"Input file not found: {input_json_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            raise
    
    def convert_data(self, json_data: Dict[str, Any]) -> str:
        """Convert JSON data directly to XML string"""
        try:
            xml_content = self.generator.convert_json_to_xml(json_data)
            logger.info("Direct data conversion completed")
            return xml_content
        except Exception as e:
            logger.error(f"Data conversion error: {str(e)}")
            raise
    
    def _validate_xml(self, xml_file: str) -> bool:
        """Basic XML validation"""
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Check for required WordPress XML elements
            required_elements = [
                'version="2.0"',
                '<channel>',
                '<wp:wxr_version>',
                '<wp:author>',
                '_elementor_data',
                '_elementor_version'
            ]
            
            for element in required_elements:
                if element not in xml_content:
                    logger.error(f"Missing required element: {element}")
                    return False
            
            # Try to parse as XML
            try:
                ET.fromstring(xml_content)
            except ET.ParseError as e:
                logger.error(f"XML parsing error: {str(e)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False


def test_converter_with_sample():
    """Test the converter with sample data"""
    # Sample JSON data structure matching yaml_to_json_processor output
    sample_json = {
        "site": {
            "title": "Test Site",
            "base_url": "http://localhost:8080",
            "description": "Test Elementor site",
            "language": "en-US"
        },
        "pages": [
            {
                "id": 1001,
                "title": "Home Page",
                "slug": "home",
                "status": "publish",
                "elementor_data": [
                    {
                        "id": "abc123",
                        "elType": "section",
                        "settings": {
                            "background_background": "classic",
                            "background_color": "#ffffff"
                        },
                        "elements": [
                            {
                                "id": "def456",
                                "elType": "column",
                                "settings": {
                                    "_column_size": 100
                                },
                                "elements": [
                                    {
                                        "id": "ghi789",
                                        "elType": "widget",
                                        "widgetType": "cholot-title",
                                        "settings": {
                                            "title": "Welcome to Our Site",
                                            "header_size": "h1"
                                        },
                                        "elements": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "metadata": {
            "processor": "Test Processor",
            "total_pages": 1
        }
    }
    
    try:
        converter = JSONToXMLConverter()
        xml_content = converter.convert_data(sample_json)
        
        # Save test output
        with open('test_output.xml', 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        logger.info("Test conversion completed successfully - check test_output.xml")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False


def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='Convert Elementor JSON to WordPress XML')
    parser.add_argument('input_file', nargs='?', help='Input JSON file (from yaml_to_json_processor.py)')
    parser.add_argument('-o', '--output', help='Output XML file', default='wordpress_import.xml')
    parser.add_argument('--site-title', help='WordPress site title', default='Generated Site')
    parser.add_argument('--site-url', help='WordPress site URL', default='http://localhost')
    parser.add_argument('--elementor-version', help='Elementor version', default='3.15.3')
    parser.add_argument('--test', action='store_true', help='Run test conversion with sample data')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    if args.test:
        logger.info("Running test conversion...")
        success = test_converter_with_sample()
        return 0 if success else 1
    
    if not args.input_file:
        parser.error("input_file is required when not using --test mode")
    
    try:
        # Create configuration
        config = WordPressConfig(
            site_title=args.site_title,
            site_url=args.site_url,
            elementor_version=args.elementor_version
        )
        
        # Create converter and process file
        converter = JSONToXMLConverter(config)
        converter.convert_file(args.input_file, args.output)
        
        logger.info("Conversion completed successfully!")
        logger.info(f"Import the generated XML file ({args.output}) using WordPress Tools > Import")
        
        return 0
        
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        return 1


if __name__ == '__main__':
    exit(main())