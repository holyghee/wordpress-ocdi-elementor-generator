#!/usr/bin/env python3
"""
Fixed Elementor Block-Assembly Processor
Fixes image URLs and HTML display issues
"""

import json
import yaml
import copy
from pathlib import Path
from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import hashlib

class ElementorFixedProcessor:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = None
        self.blocks = {}
        self.block_library_path = Path("block_library")
        self.generated_pages = []
        self.elementor_version = "3.17.0"
        self.elementor_pro_version = "3.17.0"
        
        # Map external URLs to local uploads
        self.image_url_map = {
            "https://theme.winnertheme.com/cholot/wp-content/uploads/2022/11/slide-1.jpg": 
                "http://localhost:8081/wp-content/uploads/2025/08/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg",
            "https://theme.winnertheme.com/cholot/wp-content/uploads/2022/11/slide-2.jpg": 
                "http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg",
            "https://theme.winnertheme.com/cholot/wp-content/uploads/2022/11/slide-3.jpg": 
                "http://localhost:8081/wp-content/uploads/2025/08/schadstoffsanierung-industrieanlage-riman-gmbh.jpg",
        }
        
    def load_config(self) -> bool:
        """Lade YAML-Konfiguration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            print(f"✅ Config geladen: {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Laden der Config: {e}")
            return False
    
    def load_block_library(self) -> bool:
        """Lade Block-Library"""
        if not self.block_library_path.exists():
            print("❌ Block-Library nicht gefunden")
            return False
            
        # Lade Index
        index_file = self.block_library_path / "index.json"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
                print(f"📚 Lade {index['total']} Blocks aus Library...")
        
        # Lade Blocks
        for block_file in self.block_library_path.glob("*.json"):
            if block_file.name == "index.json":
                continue
                
            with open(block_file, 'r', encoding='utf-8') as f:
                block_data = json.load(f)
                block_type = block_data.get('type', 'unknown')
                
                if block_type not in self.blocks:
                    self.blocks[block_type] = []
                    
                self.blocks[block_type].append(block_data)
        
        print(f"✅ {len(self.blocks)} Block-Typen geladen")
        return True
    
    def fix_image_urls(self, data: Any) -> Any:
        """Fix external image URLs to use local uploads"""
        if isinstance(data, str):
            # Check if it's an external image URL
            for old_url, new_url in self.image_url_map.items():
                if old_url in data:
                    data = data.replace(old_url, new_url)
            # Also fix any remaining external URLs
            if "https://theme.winnertheme.com" in data:
                # Use a default local image
                data = data.replace(
                    "https://theme.winnertheme.com/cholot/wp-content/uploads/",
                    "http://localhost:8081/wp-content/uploads/2025/08/"
                )
            return data
        elif isinstance(data, dict):
            result = {}
            for k, v in data.items():
                result[k] = self.fix_image_urls(v)
            return result
        elif isinstance(data, list):
            return [self.fix_image_urls(item) for item in data]
        else:
            return data
    
    def clean_html_content(self, content: str) -> str:
        """Clean HTML content to avoid display issues"""
        if not isinstance(content, str):
            return content
            
        # Remove style tags that might cause display issues
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        
        # Fix common HTML entities
        content = content.replace('&lt;', '<')
        content = content.replace('&gt;', '>')
        content = content.replace('&amp;', '&')
        
        # Ensure proper escaping for XML
        # But don't double-escape
        if '<p' in content or '<h' in content or '<ul' in content:
            # Already has HTML, leave it
            pass
        else:
            # Plain text, might need wrapping
            if not content.startswith('<'):
                content = f'<p>{content}</p>'
        
        return content
    
    def generate_elementor_kit(self) -> Dict:
        """Generiere Elementor Kit mit globalen Einstellungen"""
        global_settings = self.config.get('global_settings', {})
        
        kit_settings = {
            "system_colors": [
                {
                    "_id": "primary",
                    "title": "Primary",
                    "color": global_settings.get('primary_color', '#333399')
                },
                {
                    "_id": "secondary", 
                    "title": "Secondary",
                    "color": global_settings.get('secondary_color', '#FF0000')
                },
                {
                    "_id": "text",
                    "title": "Text",
                    "color": "#333333"
                },
                {
                    "_id": "accent",
                    "title": "Accent",
                    "color": global_settings.get('accent_color', '#b68c2f')
                }
            ],
            "system_typography": [
                {
                    "_id": "primary",
                    "title": "Primary",
                    "typography_font_family": global_settings.get('font_family', 'Playfair Display'),
                    "typography_font_weight": "700"
                },
                {
                    "_id": "secondary",
                    "title": "Secondary", 
                    "typography_font_family": "Source Sans Pro",
                    "typography_font_weight": "400"
                },
                {
                    "_id": "text",
                    "title": "Text",
                    "typography_font_family": "Source Sans Pro",
                    "typography_font_weight": "400"
                },
                {
                    "_id": "accent",
                    "title": "Accent",
                    "typography_font_family": global_settings.get('font_family', 'Playfair Display'),
                    "typography_font_weight": "700",
                    "typography_font_style": "italic"
                }
            ],
            "custom_colors": [],
            "custom_typography": [],
            "default_generic_fonts": "Sans-serif",
            "site_name": self.config.get('site', {}).get('title', 'RIMAN GmbH'),
            "site_description": self.config.get('site', {}).get('tagline', ''),
            "container_width": {
                "size": 1170,
                "unit": "px"
            },
            "viewport_md": 768,
            "viewport_lg": 1025
        }
        
        return kit_settings
    
    def assemble_page(self, page_config: Dict) -> Dict:
        """Assembliere eine Seite aus Blocks mit vollständigen Elementor-Daten"""
        page_data = {
            'title': page_config.get('title', 'Untitled'),
            'slug': page_config.get('slug', ''),
            'template': page_config.get('template', 'elementor_canvas'),
            'elementor_data': [],
            'elementor_settings': {
                'post_status': 'publish',
                'page_template': 'elementor_canvas',
                'hide_title': 'yes'
            }
        }
        
        # Assembliere Blocks
        for block_config in page_config.get('blocks', []):
            block_type = block_config.get('type')
            
            if block_type not in self.blocks:
                print(f"  ⚠️  Block-Typ nicht gefunden: {block_type}")
                continue
                
            # Wähle Block-Template
            block_template = self.blocks[block_type][0]['structure']
            
            # Fülle Template mit Daten
            filled_block = self._fill_block_template(block_template, block_config)
            
            # Fix image URLs
            filled_block = self.fix_image_urls(filled_block)
            
            # Füge eindeutige IDs hinzu
            filled_block = self._add_unique_ids(filled_block)
            
            # Füge Block zur Seite hinzu
            page_data['elementor_data'].append(filled_block)
            
            print(f"  ✅ Block assembliert: {block_type}")
        
        return page_data
    
    def _fill_block_template(self, template: Dict, config: Dict) -> Dict:
        """Fülle Block-Template mit Inhalten"""
        filled = copy.deepcopy(template)
        
        # Erstelle Content-Map
        content_map = self._create_content_map(config)
        
        # Clean HTML content in content map
        for key, value in content_map.items():
            if isinstance(value, str):
                content_map[key] = self.clean_html_content(value)
        
        # Rekursive Ersetzung
        def replace_content(element: Any, content: Dict) -> Any:
            if isinstance(element, str):
                for key, value in content.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in element:
                        element = element.replace(placeholder, str(value))
                return element
            elif isinstance(element, dict):
                result = {}
                for k, v in element.items():
                    result[k] = replace_content(v, content)
                    
                # Spezielle Widget-Behandlung
                if 'widgetType' in result:
                    result = self._handle_widget_content(result, config)
                    
                return result
            elif isinstance(element, list):
                return [replace_content(item, content) for item in element]
            else:
                return element
        
        return replace_content(filled, content_map)
    
    def _create_content_map(self, config: Dict) -> Dict:
        """Erstelle Content-Map für Block"""
        content_map = {}
        block_type = config.get('type')
        
        # Standard-Mappings
        if 'title' in config:
            content_map['TITLE'] = config['title']
        if 'subtitle' in config:
            content_map['SUBTITLE'] = config['subtitle']
        if 'content' in config:
            if isinstance(config['content'], dict):
                content_map.update(config['content'])
            else:
                content_map['CONTENT'] = self.clean_html_content(config['content'])
        
        # Block-spezifische Mappings
        if block_type == 'hero-slider' and 'slides' in config:
            for i, slide in enumerate(config['slides'][:3]):
                content_map[f'SLIDE_{i}_TITLE'] = slide.get('title', '')
                content_map[f'SLIDE_{i}_SUBTITLE'] = slide.get('subtitle', '')
                content_map[f'SLIDE_{i}_TEXT'] = slide.get('text', '')
                content_map[f'SLIDE_{i}_BUTTON'] = slide.get('button_text', 'Learn More')
                content_map[f'SLIDE_{i}_LINK'] = slide.get('button_link', '#')
                # Fix image URLs directly here
                image_url = slide.get('image', '')
                if image_url:
                    image_url = str(self.fix_image_urls(image_url))
                content_map[f'SLIDE_{i}_IMAGE'] = image_url
        
        elif block_type == 'service-cards' and 'services' in config:
            for i, service in enumerate(config['services'][:6]):
                content_map[f'SERVICE_{i}_TITLE'] = service.get('title', '')
                content_map[f'SERVICE_{i}_TEXT'] = service.get('text', '')
                content_map[f'SERVICE_{i}_ICON'] = service.get('icon', 'fa fa-check')
                content_map[f'SERVICE_{i}_SUBTITLE'] = service.get('subtitle', '')
        
        # Fix placeholder text
        content_map = {k: v.replace('{{', '').replace('}}', '') if isinstance(v, str) else v 
                      for k, v in content_map.items()}
        
        return content_map
    
    def _handle_widget_content(self, widget: Dict, config: Dict) -> Dict:
        """Handle spezielle Widget-Inhalte"""
        widget_type = widget.get('widgetType')
        
        # Hero Slider
        if widget_type == 'rdn-slider' and 'slides' in config:
            if 'settings' in widget and 'slider_list' in widget['settings']:
                widget['settings']['slider_list'] = []
                for slide in config['slides']:
                    image_url = slide.get('image', '')
                    if image_url:
                        image_url = str(self.fix_image_urls(image_url))
                    
                    widget['settings']['slider_list'].append({
                        '_id': self._generate_element_id(),
                        'title': slide.get('title', ''),
                        'subtitle': slide.get('subtitle', ''),
                        'text': self.clean_html_content(slide.get('text', '')),
                        'btn_text': slide.get('button_text', 'Learn More'),
                        'btn_link': {'url': slide.get('button_link', '#')},
                        'image': {'url': image_url, 'id': ''}
                    })
        
        # Service Cards
        elif widget_type == 'cholot-texticon' and 'services' in config:
            if 'settings' in widget and config['services']:
                service = config['services'][0]
                widget['settings']['title'] = service.get('title', '')
                widget['settings']['text'] = self.clean_html_content(service.get('text', ''))
                widget['settings']['subtitle'] = service.get('subtitle', '')
                widget['settings']['selected_icon'] = {'value': service.get('icon', 'fa fa-check')}
        
        # Gallery widget - ensure post_id is set
        elif widget_type == 'gallery':
            if 'settings' not in widget:
                widget['settings'] = {}
            if 'post_id' not in widget['settings']:
                widget['settings']['post_id'] = ''  # Empty string instead of null
        
        return widget
    
    def _add_unique_ids(self, element: Any) -> Any:
        """Füge eindeutige IDs zu Elementor-Elementen hinzu"""
        if isinstance(element, dict):
            if 'elType' in element and 'id' not in element:
                element['id'] = self._generate_element_id()
            
            # Ensure required fields are present
            if 'elType' in element:
                if 'settings' not in element:
                    element['settings'] = {}
                    
            for key, value in element.items():
                element[key] = self._add_unique_ids(value)
                
        elif isinstance(element, list):
            return [self._add_unique_ids(item) for item in element]
            
        return element
    
    def _generate_element_id(self) -> str:
        """Generiere eindeutige Elementor Element-ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    
    def generate_wordpress_xml(self, output_file: str):
        """Generiere vollständige WordPress XML mit Elementor-Daten"""
        # XML-Struktur
        root = ET.Element('rss', {
            'version': '2.0',
            'xmlns:excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:wfw': 'http://wellformedweb.org/CommentAPI/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:wp': 'http://wordpress.org/export/1.2/'
        })
        
        channel = ET.SubElement(root, 'channel')
        
        # Site-Info
        site_config = self.config.get('site', {})
        ET.SubElement(channel, 'title').text = site_config.get('title', 'RIMAN GmbH')
        ET.SubElement(channel, 'link').text = site_config.get('url', 'http://localhost:8081')
        ET.SubElement(channel, 'description').text = site_config.get('description', '')
        ET.SubElement(channel, 'language').text = 'de-DE'
        ET.SubElement(channel, 'wp:wxr_version').text = '1.2'
        
        # Autor
        author = ET.SubElement(channel, 'wp:author')
        ET.SubElement(author, 'wp:author_id').text = '1'
        ET.SubElement(author, 'wp:author_login').text = 'admin'
        ET.SubElement(author, 'wp:author_email').text = 'admin@example.com'
        ET.SubElement(author, 'wp:author_display_name').text = 'Administrator'
        
        # Elementor Kit (Global Settings)
        self._add_elementor_kit_to_xml(channel)
        
        # Generiere Seiten
        page_id = 2000  # Start with new ID range to avoid conflicts
        for page_config in self.config.get('pages', []):
            page_data = self.assemble_page(page_config)
            self._add_page_to_xml(channel, page_data, page_id)
            page_id += 1
            self.generated_pages.append(page_data)
        
        # XML formatieren und speichern
        tree = ET.ElementTree(root)
        ET.indent(tree, '  ')
        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        
        # Dateigröße ausgeben
        file_size = Path(output_file).stat().st_size
        print(f"✅ XML generiert: {output_file} ({file_size} bytes)")
        print(f"📊 {len(self.generated_pages)} Seiten assembliert")
    
    def _add_elementor_kit_to_xml(self, channel):
        """Füge Elementor Kit (Global Settings) zur XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = 'Elementor Kit'
        ET.SubElement(item, 'link').text = ''
        ET.SubElement(item, 'dc:creator').text = 'admin'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = ''
        ET.SubElement(item, 'wp:post_id').text = '1999'
        ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:post_type').text = 'elementor_library'
        ET.SubElement(item, 'wp:status').text = 'publish'
        
        # Kit Meta
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_template_type'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'kit'
        
        # Kit Settings
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_page_settings'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'a:0:{}'
    
    def _add_page_to_xml(self, channel, page_data: Dict, page_id: int):
        """Füge Seite mit vollständigen Elementor-Daten zur XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = page_data['title']
        ET.SubElement(item, 'link').text = f"http://localhost:8081/{page_data['slug']}"
        ET.SubElement(item, 'dc:creator').text = 'admin'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"http://localhost:8081/?page_id={page_id}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, 'content:encoded').text = ''
        ET.SubElement(item, 'wp:post_id').text = str(page_id)
        ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:post_name').text = page_data['slug']
        ET.SubElement(item, 'wp:status').text = 'publish'
        ET.SubElement(item, 'wp:post_type').text = 'page'
        
        # Page Template
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_wp_page_template'
        ET.SubElement(postmeta, 'wp:meta_value').text = page_data['template']
        
        # Elementor Data - ensure it's properly formatted
        elementor_data = page_data['elementor_data']
        # Clean any remaining placeholders
        elementor_data_str = json.dumps(elementor_data, ensure_ascii=False)
        elementor_data_str = elementor_data_str.replace('{{', '').replace('}}', '')
        
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_data'
        ET.SubElement(postmeta, 'wp:meta_value').text = elementor_data_str
        
        # Elementor Edit Mode
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_edit_mode'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'builder'
        
        # Elementor Version
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_version'
        ET.SubElement(postmeta, 'wp:meta_value').text = self.elementor_version
        
        # Elementor Page Settings
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_page_settings'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'a:0:{}'
        
        # Elementor Pro Version
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_pro_version'
        ET.SubElement(postmeta, 'wp:meta_value').text = self.elementor_pro_version
        
        # Elementor CSS
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_css'
        ET.SubElement(postmeta, 'wp:meta_value').text = json.dumps({
            'time': int(datetime.now().timestamp()),
            'fonts': [],
            'icons': ['fa-solid', 'fa-regular'],
            'dynamic_elements_ids': [],
            'status': 'inline',
            'css': ''
        })
    
    def run(self):
        """Hauptausführung"""
        print("\n🚀 Fixed Elementor Block-Assembly Processor")
        print("="*60)
        
        # Lade Config
        if not self.load_config():
            return False
        
        # Lade Block-Library
        if not self.load_block_library():
            return False
        
        # Generiere XML
        print("\n📝 Generiere WordPress XML mit gefixten URLs und HTML...")
        output_file = 'elementor-fixed-output.xml'
        self.generate_wordpress_xml(output_file)
        
        print(f"\n✅ Fertig! Gefixter Output erstellt.")
        print(f"   Output: {output_file}")
        print(f"\n💡 Nächste Schritte:")
        print(f"   1. XML importieren: php test-direct-ocdi.php {output_file}")
        print(f"   2. CSS regenerieren: php regenerate_elementor_css.php")
        
        return True

def main():
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'riman-cholot-intelligent.yaml'
    processor = ElementorFixedProcessor(config_file)
    processor.run()

if __name__ == "__main__":
    main()