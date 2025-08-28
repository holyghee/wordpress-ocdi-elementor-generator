#!/usr/bin/env python3
"""
Editierbarer Content Generator für Cholot WordPress Theme
Ermöglicht das Ändern von Inhalten über YAML-Config
"""

import yaml
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
import re

class EditableContentGenerator:
    def __init__(self, yaml_file, xml_output):
        self.yaml_file = Path(yaml_file)
        self.xml_output = Path(xml_output)
        self.config = None
        self.namespaces = {
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'wfw': 'http://wellformedweb.org/CommentAPI/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'wp': 'http://wordpress.org/export/1.2/'
        }
        
    def load_config(self):
        """Lade YAML-Konfiguration"""
        with open(self.yaml_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        print(f"✅ Config geladen: {self.yaml_file}")
        
    def apply_content_replacements(self, elementor_data, replacements):
        """Wende Content-Ersetzungen auf Elementor-Daten an"""
        if not replacements:
            return elementor_data
            
        # Konvertiere zu String für Ersetzungen
        if isinstance(elementor_data, list):
            data_str = json.dumps(elementor_data, ensure_ascii=False)
        else:
            data_str = elementor_data
            
        # Wende alle Ersetzungen an
        for old_text, new_text in replacements.items():
            # Escape für JSON-Strings
            old_escaped = old_text.replace('"', '\\"')
            new_escaped = new_text.replace('"', '\\"')
            
            # Ersetze in normalen Strings
            data_str = data_str.replace(old_text, new_text)
            # Ersetze in JSON-escaped Strings
            data_str = data_str.replace(old_escaped, new_escaped)
            
        print(f"  📝 {len(replacements)} Ersetzungen angewendet")
        
        # Konvertiere zurück zu Liste wenn nötig
        try:
            return json.loads(data_str)
        except:
            return data_str
    
    def generate_xml(self):
        """Generiere WordPress XML mit editierbaren Inhalten"""
        # Create root element
        root = ET.Element('rss', version="2.0")
        
        # Add namespaces
        for prefix, uri in self.namespaces.items():
            root.set(f'xmlns:{prefix}', uri)
        
        # Create channel
        channel = ET.SubElement(root, 'channel')
        
        # Site info
        ET.SubElement(channel, 'title').text = self.config['site']['title']
        ET.SubElement(channel, 'link').text = self.config['site']['url']
        ET.SubElement(channel, 'description').text = self.config['site'].get('description', '')
        ET.SubElement(channel, 'language').text = 'de-DE'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = self.config['site']['url']
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = self.config['site']['url']
        
        # Generate pages
        for page_config in self.config.get('pages', []):
            self.add_page_item(channel, page_config)
            
        # Generate menus
        for menu_config in self.config.get('menus', []):
            self.add_menu_items(channel, menu_config)
        
        # Pretty print
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        # Clean up empty lines
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        final_xml = '\n'.join(lines)
        
        # Save
        with open(self.xml_output, 'w', encoding='utf-8') as f:
            f.write(final_xml)
            
        print(f"✅ XML generiert: {self.xml_output}")
        print(f"   Größe: {len(final_xml)} bytes")
        
    def add_page_item(self, channel, page_config):
        """Füge eine Seite mit Elementor-Daten hinzu"""
        item = ET.SubElement(channel, 'item')
        
        # Basic page info
        ET.SubElement(item, 'title').text = page_config['title']
        ET.SubElement(item, 'link').text = f"{self.config['site']['url']}/{page_config['slug']}"
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, 'dc:creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"{self.config['site']['url']}/?page_id={page_config['id']}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, 'content:encoded').text = ''
        ET.SubElement(item, 'excerpt:encoded').text = ''
        ET.SubElement(item, 'wp:post_id').text = str(page_config['id'])
        ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:comment_status').text = 'closed'
        ET.SubElement(item, 'wp:ping_status').text = 'closed'
        ET.SubElement(item, 'wp:post_name').text = page_config['slug'] if page_config['slug'] else 'home'
        ET.SubElement(item, 'wp:status').text = 'publish'
        ET.SubElement(item, 'wp:post_parent').text = '0'
        ET.SubElement(item, 'wp:menu_order').text = '0'
        ET.SubElement(item, 'wp:post_type').text = 'page'
        ET.SubElement(item, 'wp:post_password').text = ''
        ET.SubElement(item, 'wp:is_sticky').text = '0'
        
        # Template
        if 'template' in page_config:
            postmeta = ET.SubElement(item, 'wp:postmeta')
            ET.SubElement(postmeta, 'wp:meta_key').text = '_wp_page_template'
            ET.SubElement(postmeta, 'wp:meta_value').text = page_config['template']
        
        # Elementor data
        if 'elementor_file' in page_config:
            elementor_file = Path(page_config['elementor_file'])
            if elementor_file.exists():
                with open(elementor_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                # Extrahiere die eigentlichen Elementor-Daten
                if isinstance(file_data, dict) and '_elementor_data' in file_data:
                    elementor_data = file_data['_elementor_data']
                elif isinstance(file_data, dict) and '_elementor_data_parsed' in file_data:
                    elementor_data = file_data['_elementor_data_parsed']
                else:
                    elementor_data = file_data
                
                # Wende Ersetzungen an
                if 'content_replacements' in page_config:
                    elementor_data = self.apply_content_replacements(
                        elementor_data, 
                        page_config['content_replacements']
                    )
                
                # Füge Elementor-Metadaten hinzu
                # _elementor_data
                postmeta = ET.SubElement(item, 'wp:postmeta')
                ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_data'
                ET.SubElement(postmeta, 'wp:meta_value').text = json.dumps(elementor_data, ensure_ascii=False)
                
                # _elementor_edit_mode
                postmeta = ET.SubElement(item, 'wp:postmeta')
                ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_edit_mode'
                ET.SubElement(postmeta, 'wp:meta_value').text = 'builder'
                
                # _elementor_template_type
                postmeta = ET.SubElement(item, 'wp:postmeta')
                ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_template_type'
                ET.SubElement(postmeta, 'wp:meta_value').text = 'wp-page'
                
                print(f"  ✅ Seite hinzugefügt: {page_config['title']} mit Elementor-Daten")
            else:
                print(f"  ⚠️  Elementor-Datei nicht gefunden: {elementor_file}")
    
    def add_menu_items(self, channel, menu_config):
        """Füge Menü-Items hinzu"""
        # Erstelle das Menü selbst
        menu_item = ET.SubElement(channel, 'item')
        ET.SubElement(menu_item, 'title').text = menu_config['name']
        ET.SubElement(menu_item, 'wp:post_id').text = str(menu_config['id'])
        ET.SubElement(menu_item, 'wp:post_type').text = 'nav_menu'
        ET.SubElement(menu_item, 'wp:term_slug').text = menu_config['slug']
        
        # Füge Menü-Items hinzu
        for item_config in menu_config.get('items', []):
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = item_config['title']
            ET.SubElement(item, 'wp:post_id').text = str(item_config['id'])
            ET.SubElement(item, 'wp:post_type').text = 'nav_menu_item'
            ET.SubElement(item, 'wp:menu_order').text = str(item_config.get('order', 0))
            
            # Link zur Seite
            if 'page_id' in item_config:
                postmeta = ET.SubElement(item, 'wp:postmeta')
                ET.SubElement(postmeta, 'wp:meta_key').text = '_menu_item_object_id'
                ET.SubElement(postmeta, 'wp:meta_value').text = str(item_config['page_id'])
                
                postmeta = ET.SubElement(item, 'wp:postmeta')
                ET.SubElement(postmeta, 'wp:meta_key').text = '_menu_item_object'
                ET.SubElement(postmeta, 'wp:meta_value').text = 'page'
                
                postmeta = ET.SubElement(item, 'wp:postmeta')
                ET.SubElement(postmeta, 'wp:meta_key').text = '_menu_item_type'
                ET.SubElement(postmeta, 'wp:meta_value').text = 'post_type'
        
        print(f"  ✅ Menü hinzugefügt: {menu_config['name']} mit {len(menu_config.get('items', []))} Items")
    
    def run(self):
        """Hauptausführung"""
        print("\n🚀 Editierbarer Content Generator für Cholot")
        print("="*50)
        
        self.load_config()
        self.generate_xml()
        
        print("\n✅ Fertig! Sie können nun:")
        print("   1. Inhalte in der YAML ändern")
        print("   2. Dieses Script erneut ausführen")
        print("   3. Die generierte XML in WordPress importieren")
        print("   4. Ihre Änderungen auf der Website sehen!")
        
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python editable_content_generator.py <yaml_file> <xml_output>")
        print("Example: python editable_content_generator.py cholot-editable-simple.yaml cholot-custom.xml")
        sys.exit(1)
    
    generator = EditableContentGenerator(sys.argv[1], sys.argv[2])
    generator.run()