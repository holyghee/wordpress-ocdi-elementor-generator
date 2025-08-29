#!/usr/bin/env python3
"""
Dynamischer Elementor Prozessor
Erstellt Elementor-Seiten komplett dynamisch basierend auf YAML-Config
Keine Template-Befüllung, sondern echter Widget-Assembly
"""

import yaml
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import re
import uuid

class DynamicElementorProcessor:
    def __init__(self, yaml_config: str):
        self.yaml_file = Path(yaml_config)
        self.config = None
        self.elementor_version = "3.18.3"
        self.elementor_pro_version = "3.18.2"
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
    
    def generate_element_id(self) -> str:
        """Generiere eine eindeutige Elementor Element ID"""
        return uuid.uuid4().hex[:7]
    
    def create_widget(self, widget_type: str, settings: Dict) -> Dict:
        """Erstelle ein einzelnes Widget dynamisch"""
        return {
            "id": self.generate_element_id(),
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": widget_type
        }
    
    def create_column(self, widgets: List[Dict], width: int = 100) -> Dict:
        """Erstelle eine Elementor Column"""
        return {
            "id": self.generate_element_id(),
            "elType": "column",
            "settings": {
                "_column_size": width,
                "_inline_size": width
            },
            "elements": widgets
        }
    
    def create_section(self, columns: List[Dict], settings: Dict = None) -> Dict:
        """Erstelle eine Elementor Section"""
        section = {
            "id": self.generate_element_id(),
            "elType": "section",
            "settings": settings or {},
            "elements": columns
        }
        return section
    
    def build_hero_slider(self, config: Dict) -> Dict:
        """Baue einen Hero-Slider dynamisch"""
        slides = []
        for slide in config.get('slides', []):
            slides.append({
                "_id": self.generate_element_id(),
                "title": slide.get('title', ''),
                "subtitle": slide.get('subtitle', ''),
                "text": slide.get('text', ''),
                "btn_text": slide.get('button_text', ''),
                "btn_link": {"url": slide.get('button_link', '#')},
                "image": {
                    "url": slide.get('image', ''),
                    "id": self.get_image_id(slide.get('image', ''))
                }
            })
        
        widget = self.create_widget('rdn-slider', {
            'slider_list': slides,
            'slider_speed': 8000,
            'align': 'left',
            'title_typo_font_family': 'Heebo',
            'title_typo_font_size': {'unit': 'px', 'size': 45},
            'title_typo_font_weight': '700',
            'title_color': '#ffffff',
            'subtitle_color': '#b68c2f',
            'text_color': 'rgba(255,255,255,0.89)',
            'btn_color': '#ffffff',
            'btn_border_color': '#b68c2f',
            'btn_bg_hover': '#b68c2f',
            'show_line': 'show',
            'linecolor': '#b68c2f',
            'slider_mask': 'rgba(0,0,0,0.6)'
        })
        
        column = self.create_column([widget])
        section = self.create_section([column], {
            'layout': 'full_width',
            'gap': 'no',
            'height': 'min-height',
            'custom_height': {'unit': 'vh', 'size': 100}
        })
        
        return section
    
    def build_service_cards(self, config: Dict) -> Dict:
        """Baue Service-Cards Section dynamisch"""
        widgets = []
        columns = []
        
        # Erstelle Title Widget wenn vorhanden
        if config.get('title'):
            title_widget = self.create_widget('cholot-title', {
                'title': config.get('title', ''),
                'subtitle': config.get('subtitle', ''),
                'align': 'center',
                'title_color': '#1f1f1f',
                'subtitle_color': '#b68c2f'
            })
            title_column = self.create_column([title_widget])
            title_section = self.create_section([title_column], {
                'padding': {'unit': 'px', 'top': 50, 'bottom': 30}
            })
            # Gebe Title als separate Section zurück
            
        # Erstelle Service Cards
        for service in config.get('services', []):
            widget = self.create_widget('cholot-texticon', {
                'title': service.get('title', ''),
                'text': service.get('text', ''),
                'subtitle': service.get('subtitle', ''),
                'selected_icon': {'value': service.get('icon', 'fa fa-check')},
                'icon_align': 'center',
                'title_color': '#1f1f1f',
                'text_color': '#666666',
                'icon_color': '#b68c2f',
                'iconbg_color': 'rgba(182, 140, 47, 0.1)'
            })
            
            # Berechne Column-Breite basierend auf Anzahl
            num_services = len(config.get('services', []))
            column_width = 100 // min(num_services, 4)  # Max 4 Spalten
            
            column = self.create_column([widget], column_width)
            columns.append(column)
        
        section = self.create_section(columns, {
            'padding': {'unit': 'px', 'top': 50, 'bottom': 50},
            'background_background': 'classic',
            'background_color': '#f8f8f8'
        })
        
        return section
    
    def build_team_section(self, config: Dict) -> Dict:
        """Baue Team-Section dynamisch"""
        columns = []
        
        for member in config.get('team_members', []):
            widget = self.create_widget('cholot-team', {
                'title': member.get('name', ''),
                'designation': member.get('position', ''),
                'text': member.get('bio', ''),
                'image': {
                    'url': member.get('image', ''),
                    'id': self.get_image_id(member.get('image', ''))
                },
                'social_list': member.get('social', [])
            })
            
            column = self.create_column([widget], 33)  # 3 Spalten
            columns.append(column)
        
        section = self.create_section(columns, {
            'padding': {'unit': 'px', 'top': 70, 'bottom': 70}
        })
        
        return section
    
    def build_text_content(self, config: Dict) -> Dict:
        """Baue Text-Content Section"""
        content_html = config.get('content', '')
        
        # Wenn content ein dict ist, konvertiere zu HTML
        if isinstance(content_html, dict):
            content_html = content_html.get('html', '')
        
        widget = self.create_widget('text-editor', {
            'editor': content_html
        })
        
        column = self.create_column([widget])
        section = self.create_section([column], {
            'padding': {'unit': 'px', 'top': 40, 'bottom': 40},
            'content_width': {'unit': 'px', 'size': 1170}
        })
        
        return section
    
    def build_gallery_section(self, config: Dict) -> Dict:
        """Baue Gallery Section"""
        gallery_items = []
        
        for idx, image_url in enumerate(config.get('images', [])):
            gallery_items.append({
                'id': self.generate_element_id(),
                'url': image_url
            })
        
        widget = self.create_widget('image-gallery', {
            'gallery': gallery_items,
            'gallery_columns': 3,
            'gallery_link': 'file',
            'gallery_display_caption': ''
        })
        
        column = self.create_column([widget])
        section = self.create_section([column], {
            'padding': {'unit': 'px', 'top': 50, 'bottom': 50}
        })
        
        return section
    
    def build_contact_form(self, config: Dict) -> Dict:
        """Baue Contact Form Section"""
        # Erstelle Title wenn vorhanden
        widgets = []
        
        if config.get('title'):
            title_widget = self.create_widget('heading', {
                'title': config.get('title', 'Kontakt'),
                'header_size': 'h2',
                'align': 'center',
                'title_color': '#1f1f1f'
            })
            widgets.append(title_widget)
        
        if config.get('subtitle'):
            subtitle_widget = self.create_widget('heading', {
                'title': config.get('subtitle', ''),
                'header_size': 'h4',
                'align': 'center',
                'title_color': '#666666'
            })
            widgets.append(subtitle_widget)
        
        # Contact Form Widget
        form_widget = self.create_widget('shortcode', {
            'shortcode': '[contact-form-7 title="Kontaktformular"]'
        })
        widgets.append(form_widget)
        
        column = self.create_column(widgets)
        section = self.create_section([column], {
            'padding': {'unit': 'px', 'top': 70, 'bottom': 70},
            'content_width': {'unit': 'px', 'size': 800}
        })
        
        return section
    
    def build_title_section(self, config: Dict) -> Dict:
        """Baue reine Title Section"""
        widget = self.create_widget('heading', {
            'title': config.get('title', ''),
            'header_size': 'h2',
            'align': 'center',
            'title_color': '#1f1f1f'
        })
        
        column = self.create_column([widget])
        section = self.create_section([column], {
            'padding': {'unit': 'px', 'top': 50, 'bottom': 20}
        })
        
        return section
    
    def build_testimonials(self, config: Dict) -> Dict:
        """Baue Testimonials Section"""
        testimonials = []
        
        for testimonial in config.get('testimonials', []):
            testimonials.append({
                '_id': self.generate_element_id(),
                'content': testimonial.get('text', ''),
                'name': testimonial.get('author', ''),
                'title': testimonial.get('position', '')
            })
        
        widget = self.create_widget('testimonial-carousel', {
            'testimonials': testimonials,
            'slides_to_show': 1,
            'autoplay': 'yes',
            'autoplay_speed': 5000,
            'pause_on_hover': 'yes'
        })
        
        column = self.create_column([widget])
        section = self.create_section([column], {
            'padding': {'unit': 'px', 'top': 70, 'bottom': 70},
            'background_background': 'classic',
            'background_color': '#f8f8f8'
        })
        
        return section
    
    def get_image_id(self, image_url: str) -> str:
        """Hole die WordPress Media ID für eine Bild-URL"""
        # Lade Image-Mapping wenn vorhanden
        mapping_file = Path("clean_image_mapping.json")
        if mapping_file.exists():
            with open(mapping_file, 'r') as f:
                mapping = json.load(f)
                # Konvertiere URL von 8082 zu 8081 wenn nötig
                for old_url, data in mapping.items():
                    if data['url'] == image_url:
                        return data['id']
        return ""
    
    def assemble_page(self, page_config: Dict) -> List[Dict]:
        """Assembliere eine komplette Seite aus Blocks"""
        print(f"\n🔨 Assembliere Seite: {page_config['title']}")
        
        sections = []
        
        for block_config in page_config.get('blocks', []):
            block_type = block_config.get('type')
            
            if block_type == 'hero-slider':
                section = self.build_hero_slider(block_config)
            elif block_type == 'service-cards':
                section = self.build_service_cards(block_config)
            elif block_type == 'team-section':
                section = self.build_team_section(block_config)
            elif block_type == 'text-content':
                section = self.build_text_content(block_config)
            elif block_type == 'gallery-section':
                section = self.build_gallery_section(block_config)
            elif block_type == 'contact-form':
                section = self.build_contact_form(block_config)
            elif block_type == 'title-section':
                section = self.build_title_section(block_config)
            elif block_type == 'testimonials':
                section = self.build_testimonials(block_config)
            else:
                print(f"  ⚠️  Unbekannter Block-Typ: {block_type}")
                continue
            
            sections.append(section)
            print(f"  ✅ Block erstellt: {block_type}")
        
        return sections
    
    def generate_wordpress_xml(self, output_file: str):
        """Generiere WordPress XML mit dynamisch erstellten Elementor-Daten"""
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
        ET.SubElement(channel, 'title').text = site_config.get('title', 'RIMAN GmbH')
        ET.SubElement(channel, 'link').text = site_config.get('url', 'http://localhost:8081')
        ET.SubElement(channel, 'description').text = site_config.get('description', '')
        ET.SubElement(channel, 'language').text = site_config.get('language', 'de-DE')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        
        # Generate pages
        page_id = 3000  # Start bei höherer ID um Konflikte zu vermeiden
        for page_config in self.config.get('pages', []):
            elementor_data = self.assemble_page(page_config)
            self._add_page_to_xml(channel, page_config, elementor_data, page_id)
            page_id += 1
        
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
        
        print(f"✅ XML generiert: {output_file}")
        print(f"📊 {len(self.config.get('pages', []))} Seiten dynamisch erstellt")
        
        return output_file
    
    def _add_page_to_xml(self, channel, page_config: Dict, elementor_data: List, page_id: int):
        """Füge eine Seite zur XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = page_config.get('title', 'Untitled')
        ET.SubElement(item, 'link').text = f"http://localhost:8081/{page_config.get('slug', '')}"
        ET.SubElement(item, 'dc:creator').text = 'admin'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"http://localhost:8081/?page_id={page_id}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, 'content:encoded').text = ''
        ET.SubElement(item, 'wp:post_id').text = str(page_id)
        ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:post_name').text = page_config.get('slug', '')
        ET.SubElement(item, 'wp:status').text = 'publish'
        ET.SubElement(item, 'wp:post_type').text = 'page'
        
        # Page Template
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_wp_page_template'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'elementor_canvas'
        
        # Elementor Data
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_elementor_data'
        ET.SubElement(postmeta, 'wp:meta_value').text = json.dumps(elementor_data, ensure_ascii=False)
        
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
    
    def run(self):
        """Hauptausführung"""
        print("\n🚀 Dynamischer Elementor Prozessor")
        print("="*50)
        
        # Lade Config
        self.load_config()
        
        # Generiere XML
        output_file = self.config.get('output', 'dynamic-elementor-output.xml')
        self.generate_wordpress_xml(output_file)
        
        print("\n✅ Fertig! Seiten wurden dynamisch erstellt.")
        print(f"   Output: {output_file}")
        print("   Keine Templates, keine Platzhalter - nur sauberer Content!")
        
        return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dynamic_elementor_processor.py <yaml_config>")
        print("Example: python dynamic_elementor_processor.py riman-cholot-intelligent.yaml")
        sys.exit(1)
    
    processor = DynamicElementorProcessor(sys.argv[1])
    processor.run()