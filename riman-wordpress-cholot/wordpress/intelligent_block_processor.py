#!/usr/bin/env python3
"""
Intelligenter Block-Assembly Prozessor
Assembliert dynamisch WordPress-Seiten aus Block-Library basierend auf YAML-Config
"""

import yaml
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re
import copy

class IntelligentBlockProcessor:
    def __init__(self, yaml_config: str, block_library_dir: str = "block_library"):
        self.yaml_file = Path(yaml_config)
        self.block_library_dir = Path(block_library_dir)
        self.config = None
        self.blocks = {}
        self.assembled_pages = []
        self.namespaces = {
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'wfw': 'http://wellformedweb.org/CommentAPI/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'wp': 'http://wordpress.org/export/1.2/'
        }
        
    def load_config(self):
        """Lade die YAML-Konfiguration"""
        with open(self.yaml_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        print(f"✅ Config geladen: {self.yaml_file}")
        
    def load_block_library(self):
        """Lade alle verfügbaren Blocks aus der Library"""
        index_file = self.block_library_dir / "index.json"
        if not index_file.exists():
            print("❌ Block-Library Index nicht gefunden!")
            return False
            
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        print(f"📚 Lade {index['total']} Blocks aus Library...")
        
        for block_info in index['blocks']:
            block_file = self.block_library_dir / f"{block_info['id']}.json"
            if block_file.exists():
                with open(block_file, 'r') as f:
                    self.blocks[block_info['type']] = self.blocks.get(block_info['type'], [])
                    self.blocks[block_info['type']].append(json.load(f))
                    
        print(f"✅ {len(self.blocks)} Block-Typen geladen")
        return True
    
    def assemble_page(self, page_config: Dict) -> Dict:
        """Assembliere eine Seite aus Blocks basierend auf Config"""
        print(f"\n🔨 Assembliere Seite: {page_config['title']}")
        
        assembled_sections = []
        
        # Iteriere über die definierten Blocks
        for block_config in page_config.get('blocks', []):
            block_type = block_config.get('type')
            
            if block_type not in self.blocks:
                print(f"  ⚠️  Block-Typ '{block_type}' nicht in Library")
                continue
                
            # Wähle die passende Block-Variante
            block_template = self._select_block_variant(block_type, block_config)
            
            if not block_template:
                print(f"  ⚠️  Keine passende Variante für '{block_type}'")
                continue
            
            # Fülle Block mit Inhalten aus Config
            filled_block = self._fill_block_template(block_template, block_config)
            
            # Wende Design-Settings an
            if 'design' in self.config:
                filled_block = self._apply_design_settings(filled_block, self.config['design'])
            
            assembled_sections.append(filled_block)
            print(f"  ✅ Block assembliert: {block_type}")
        
        # Erstelle komplette Seiten-Struktur
        page_data = {
            'id': page_config.get('id', self._generate_id()),
            'title': page_config['title'],
            'slug': page_config.get('slug', self._slugify(page_config['title'])),
            'template': page_config.get('template', 'elementor_canvas'),
            'elementor_data': assembled_sections,
            'meta': page_config.get('meta', {})
        }
        
        return page_data
    
    def _select_block_variant(self, block_type: str, config: Dict) -> Dict:
        """Wähle die beste Block-Variante basierend auf Config"""
        available_variants = self.blocks.get(block_type, [])
        
        if not available_variants:
            return None
            
        # Wähle basierend auf Anforderungen
        # Für Demo: Nimm die erste Variante
        # TODO: Intelligente Auswahl basierend auf Config
        selected = available_variants[0]
        
        return copy.deepcopy(selected['structure'])
    
    def _fill_block_template(self, template: Dict, config: Dict) -> Dict:
        """Fülle Block-Template mit Inhalten aus Config"""
        filled = copy.deepcopy(template)
        
        # Erstelle Content-Map aus verschiedenen Config-Feldern
        content_map = {}
        
        # Map für verschiedene Block-Typen
        if config.get('type') == 'hero-slider' and 'slides' in config:
            for i, slide in enumerate(config['slides'][:2]):  # Max 2 slides
                content_map[f'SLIDE_{i}_TITLE'] = slide.get('title', '')
                content_map[f'SLIDE_{i}_SUBTITLE'] = slide.get('subtitle', '')
                content_map[f'SLIDE_{i}_BUTTON'] = slide.get('button_text', 'Learn More')
                
        elif config.get('type') == 'service-cards' and 'services' in config:
            # Generische Service-Platzhalter
            if config['services']:
                content_map['SERVICE_TITLE'] = config['services'][0].get('title', '')
                content_map['SERVICE_TEXT'] = config['services'][0].get('text', '')
                content_map['SERVICE_ICON'] = config['services'][0].get('icon', 'fa fa-check')
                
        elif config.get('type') == 'title-section':
            content_map['TITLE'] = config.get('title', '')
            content_map['SUBTITLE'] = config.get('subtitle', '')
            
        # Allgemeine Inhalte
        if 'title' in config:
            content_map['TITLE'] = config['title']
        if 'subtitle' in config:
            content_map['SUBTITLE'] = config['subtitle']
        if 'content' in config:
            if isinstance(config['content'], dict):
                content_map.update(config['content'])
            else:
                content_map['CONTENT'] = config['content']
        
        # Rekursive Funktion zum Ersetzen von Platzhaltern
        def replace_placeholders(element: Any, content: Dict) -> Any:
            if isinstance(element, str):
                # Ersetze Platzhalter
                for key, value in content.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in element:
                        element = element.replace(placeholder, str(value))
                return element
            elif isinstance(element, dict):
                result = {}
                for k, v in element.items():
                    result[k] = replace_placeholders(v, content)
                
                # Spezielle Behandlung für bestimmte Widget-Typen
                if 'widgetType' in result:
                    result = self._handle_widget_content(result, config)
                    
                return result
            elif isinstance(element, list):
                return [replace_placeholders(item, content) for item in element]
            else:
                return element
        
        # Ersetze Platzhalter mit Inhalten
        filled = replace_placeholders(filled, content_map)
        
        # Handle spezielle Konfigurationen
        if 'settings' in config:
            filled = self._apply_block_settings(filled, config['settings'])
        
        return filled
    
    def _handle_widget_content(self, widget: Dict, config: Dict) -> Dict:
        """Spezielle Behandlung für verschiedene Widget-Typen"""
        widget_type = widget.get('widgetType')
        
        if widget_type == 'cholot-texticon' and 'services' in config:
            # Handle Service-Cards
            if 'settings' in widget:
                service = config['services'][0] if config['services'] else {}
                if 'title' in service:
                    widget['settings']['title'] = service['title']
                if 'text' in service:
                    widget['settings']['text'] = service['text']
                if 'icon' in service:
                    widget['settings']['selected_icon'] = {'value': service['icon']}
                    
        elif widget_type == 'rdn-slider' and 'slides' in config:
            # Handle Slider
            if 'settings' in widget and 'slider_list' in widget['settings']:
                widget['settings']['slider_list'] = []
                for slide in config['slides']:
                    widget['settings']['slider_list'].append({
                        'title': slide.get('title', ''),
                        'subtitle': slide.get('subtitle', ''),
                        'text': slide.get('text', ''),
                        'btn_text': slide.get('button_text', 'Learn More'),
                        'btn_link': {'url': slide.get('button_link', '#')},
                        'image': {'url': slide.get('image', '')}
                    })
        
        elif widget_type == 'cholot-team' and 'team_members' in config:
            # Handle Team Members
            if 'settings' in widget:
                member = config['team_members'][0] if config['team_members'] else {}
                widget['settings']['title'] = member.get('name', '')
                widget['settings']['designation'] = member.get('position', '')
                widget['settings']['text'] = member.get('bio', '')
                
        return widget
    
    def _apply_block_settings(self, block: Dict, settings: Dict) -> Dict:
        """Wende Block-spezifische Settings an"""
        # TODO: Implementiere spezifische Settings-Anwendung
        return block
    
    def _apply_design_settings(self, block: Dict, design: Dict) -> Dict:
        """Wende globale Design-Settings auf Block an"""
        
        def apply_design(element: Any) -> Any:
            if isinstance(element, dict):
                # Wende Design auf Settings an
                if 'settings' in element:
                    settings = element['settings']
                    
                    # Farben
                    if 'primary_color' in design:
                        color_fields = ['color', 'title_color', 'subtitle_color', 
                                      'icon_color', 'iconbg_color', 'btn_border_color']
                        for field in color_fields:
                            if field in settings and '#b68c2f' in str(settings[field]):
                                settings[field] = design['primary_color']
                    
                    # Typography
                    if 'font_family' in design:
                        font_fields = ['title_typo_font_family', 'text_typo_font_family']
                        for field in font_fields:
                            if field in settings:
                                settings[field] = design['font_family']
                    
                    # Spacing
                    if 'spacing' in design:
                        spacing_map = {
                            'small': {'size': 10},
                            'medium': {'size': 20},
                            'large': {'size': 30}
                        }
                        if design['spacing'] in spacing_map:
                            padding_fields = ['padding', 'margin']
                            for field in padding_fields:
                                if field in settings:
                                    settings[field] = {'unit': 'px', **spacing_map[design['spacing']]}
                
                # Rekursiv auf Kinder anwenden
                for key, value in element.items():
                    element[key] = apply_design(value)
                    
            elif isinstance(element, list):
                return [apply_design(item) for item in element]
                
            return element
        
        return apply_design(block)
    
    def generate_wordpress_xml(self, output_file: str):
        """Generiere WordPress XML aus assemblierten Seiten"""
        print(f"\n📝 Generiere WordPress XML...")
        
        # Create root element
        root = ET.Element('rss', version="2.0")
        
        # Add namespaces
        for prefix, uri in self.namespaces.items():
            root.set(f'xmlns:{prefix}', uri)
        
        # Create channel
        channel = ET.SubElement(root, 'channel')
        
        # Site info
        site_config = self.config.get('site', {})
        ET.SubElement(channel, 'title').text = site_config.get('title', 'Generated Site')
        ET.SubElement(channel, 'link').text = site_config.get('url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site_config.get('description', '')
        ET.SubElement(channel, 'language').text = site_config.get('language', 'de-DE')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        
        # Generate pages
        for page_config in self.config.get('pages', []):
            page_data = self.assemble_page(page_config)
            self._add_page_to_xml(channel, page_data)
        
        # Generate navigation
        for menu_config in self.config.get('navigation', []):
            self._add_menu_to_xml(channel, menu_config)
        
        # Pretty print
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        # Clean up
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        final_xml = '\n'.join(lines)
        
        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_xml)
        
        print(f"✅ XML generiert: {output_file} ({len(final_xml)} bytes)")
        print(f"📊 {len(self.config.get('pages', []))} Seiten assembliert")
        
        return output_file
    
    def _add_page_to_xml(self, channel: ET.Element, page_data: Dict):
        """Füge eine assemblierte Seite zur XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        # Basic info
        ET.SubElement(item, 'title').text = page_data['title']
        ET.SubElement(item, 'link').text = f"{self.config['site']['url']}/{page_data['slug']}"
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, 'dc:creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"/?page_id={page_data['id']}"
        
        # WordPress specific
        ET.SubElement(item, 'wp:post_id').text = str(page_data['id'])
        ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:post_name').text = page_data['slug']
        ET.SubElement(item, 'wp:status').text = 'publish'
        ET.SubElement(item, 'wp:post_type').text = 'page'
        
        # Page template
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_wp_page_template'
        ET.SubElement(postmeta, 'wp:meta_value').text = page_data['template']
        
        # Elementor data
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_data'
        ET.SubElement(postmeta, 'wp:meta_value').text = json.dumps(page_data['elementor_data'], ensure_ascii=False)
        
        # Elementor settings
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_edit_mode'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'builder'
        
    def _add_menu_to_xml(self, channel: ET.Element, menu_config: Dict):
        """Füge Navigation zur XML hinzu"""
        # TODO: Implementiere Menu-Generation
        pass
    
    def _generate_id(self) -> int:
        """Generiere eine eindeutige ID"""
        import random
        return random.randint(1000, 9999)
    
    def _slugify(self, text: str) -> str:
        """Erstelle einen URL-Slug aus Text"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9-]', '-', text)
        text = re.sub(r'-+', '-', text)
        return text.strip('-')
    
    def run(self):
        """Hauptausführung"""
        print("\n🚀 Intelligenter Block-Assembly Prozessor")
        print("="*50)
        
        # Lade Config
        self.load_config()
        
        # Lade Block-Library
        if not self.load_block_library():
            return False
        
        # Generiere XML
        output_file = self.config.get('output', 'intelligent-output.xml')
        self.generate_wordpress_xml(output_file)
        
        print("\n✅ Fertig! Seiten wurden aus Block-Library assembliert.")
        print(f"   Output: {output_file}")
        
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intelligent_block_processor.py <yaml_config>")
        print("Example: python intelligent_block_processor.py intelligent-site.yaml")
        sys.exit(1)
    
    processor = IntelligentBlockProcessor(sys.argv[1])
    processor.run()