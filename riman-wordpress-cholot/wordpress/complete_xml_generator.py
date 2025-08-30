#!/usr/bin/env python3
"""
Vollständiger WordPress/Elementor XML Generator
Erstellt eine komplette WordPress Export-Datei wie demo-data-fixed.xml
"""

import yaml
import json
import hashlib
from datetime import datetime
import html

class CompleteWordPressXMLGenerator:
    def __init__(self):
        self.init_design_tokens()
        
    def init_design_tokens(self):
        """Standard Design-Tokens"""
        self.design_tokens = {
            'colors': {
                'primary': '#b68c2f',
                'text_dark': '#000000', 
                'text_light': '#ffffff',
                'background_light': '#fafafa',
                'background_dark': '#1f1f1f'
            }
        }
    
    def generate_id(self, length=7):
        """Generiert unique IDs"""
        return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:length]
    
    def generate_complete_xml(self, yaml_config):
        """Generiert eine vollständige WordPress XML wie demo-data-fixed.xml"""
        
        company = yaml_config.get('company', {})
        page_config = yaml_config.get('page', {})
        
        # Generiere Elementor JSON
        elementor_data = self.generate_elementor_structure(yaml_config)
        elementor_json = json.dumps(elementor_data, ensure_ascii=False)
        
        # Baue komplette XML-Struktur
        xml_content = f'''<?xml version="1.0" encoding="UTF-8" ?>
<!-- WordPress Export Generator - Cholot Theme Compatible -->
<!-- Generator: Elementor/WordPress YAML to XML Converter -->
<!-- This file can be imported directly into WordPress using Tools -> Import -->

<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
    <title>{company.get('name', 'Website')}</title>
    <link>http://localhost:8081</link>
    <description>{company.get('tagline', 'Professional Services')}</description>
    <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>http://localhost:8081</wp:base_site_url>
    <wp:base_blog_url>http://localhost:8081</wp:base_blog_url>

    <!-- Author -->
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[admin]]></wp:author_login>
        <wp:author_email><![CDATA[admin@{company.get('name', 'company').lower().replace(' ', '')}.de]]></wp:author_email>
        <wp:author_display_name><![CDATA[Admin]]></wp:author_display_name>
        <wp:author_first_name><![CDATA[]]></wp:author_first_name>
        <wp:author_last_name><![CDATA[]]></wp:author_last_name>
    </wp:author>

    <!-- Categories -->
    <wp:category>
        <wp:term_id>1</wp:term_id>
        <wp:category_nicename><![CDATA[uncategorized]]></wp:category_nicename>
        <wp:category_parent><![CDATA[]]></wp:category_parent>
        <wp:cat_name><![CDATA[Uncategorized]]></wp:cat_name>
    </wp:category>

    <!-- Tags -->
    <wp:tag>
        <wp:term_id>2</wp:term_id>
        <wp:tag_slug><![CDATA[cholot]]></wp:tag_slug>
        <wp:tag_name><![CDATA[Cholot]]></wp:tag_name>
    </wp:tag>

    <generator>https://wordpress.org/?v=6.8.2</generator>

    <!-- Main Homepage -->
    <item>
        <title>{page_config.get('name', 'Homepage')}</title>
        <link>http://localhost:8081/?page_id=3000</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">http://localhost:8081/?page_id=3000</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>3000</wp:post_id>
        <wp:post_date><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:post_modified><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_modified>
        <wp:post_modified_gmt><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_modified_gmt>
        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[{page_config.get('slug', 'homepage')}]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        
        <!-- Elementor Page Settings -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_page_settings]]></wp:meta_key>
            <wp:meta_value><![CDATA[{{"page_title":"hide","hide_title":"yes"}}]]></wp:meta_value>
        </wp:postmeta>
        
        <!-- Elementor Version -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_version]]></wp:meta_key>
            <wp:meta_value><![CDATA[3.18.3]]></wp:meta_value>
        </wp:postmeta>
        
        <!-- Elementor Edit Mode -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        
        <!-- Page Template -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[elementor_header_footer]]></wp:meta_value>
        </wp:postmeta>
        
        <!-- Elementor Template Type -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_template_type]]></wp:meta_key>
            <wp:meta_value><![CDATA[wp-page]]></wp:meta_value>
        </wp:postmeta>
        
        <!-- Elementor Data (Main Content) -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
            <wp:meta_value><![CDATA[{html.escape(elementor_json)}]]></wp:meta_value>
        </wp:postmeta>
        
        <!-- Elementor Controls Usage -->
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_controls_usage]]></wp:meta_key>
            <wp:meta_value><![CDATA[{{"column":{{"count":10,"control_percent":0}},"section":{{"count":8,"control_percent":1}},"image":{{"count":4,"control_percent":1,"controls":{{"content":{{"section_image":{{"image":4,"link_to":1}}}}}}}},"cholot-texticon":{{"count":3,"control_percent":4}},"text-editor":{{"count":2,"control_percent":1}},"divider":{{"count":2,"control_percent":1}}}}]]></wp:meta_value>
        </wp:postmeta>
    </item>
    
    <!-- Additional Service Pages -->
'''
        
        # Füge Service-Seiten hinzu
        services = yaml_config.get('page', {}).get('sections', [])
        for section in services:
            if section.get('type') == 'service_cards':
                for idx, service in enumerate(section.get('config', {}).get('items', [])):
                    xml_content += f'''
    <item>
        <title>{service.get('title', 'Service')}</title>
        <link>http://localhost:8081/?page_id={3001 + idx}</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">http://localhost:8081/?page_id={3001 + idx}</guid>
        <content:encoded><![CDATA[{service.get('text', '')}]]></content:encoded>
        <wp:post_id>{3001 + idx}</wp:post_id>
        <wp:post_date><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:post_name><![CDATA[{service.get('title', '').lower().replace(' ', '-')}]]></wp:post_name>
    </item>
'''
        
        xml_content += '''
</channel>
</rss>'''
        
        return xml_content
    
    def generate_elementor_structure(self, yaml_config):
        """Generiert die Elementor JSON-Struktur"""
        sections = []
        
        for section in yaml_config.get('page', {}).get('sections', []):
            if section['type'] == 'hero_slider':
                sections.append(self.generate_hero_section(section['config']))
            elif section['type'] == 'service_cards':
                sections.append(self.generate_service_cards_section(section['config']))
        
        return sections
    
    def generate_hero_section(self, config):
        """Hero Slider Section mit mountains divider"""
        return {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "gap": "no",
                "layout": "full_width", 
                "background_color": "rgba(0,0,0,0.6)",
                "shape_divider_bottom": "mountains",
                "shape_divider_bottom_color": "#ffffff",
                "shape_divider_bottom_width": {"unit": "%", "size": 105},
                "shape_divider_bottom_height": {"unit": "px", "size": 88},
                "shape_divider_bottom_above_content": "yes"
            },
            "elements": [{
                "id": self.generate_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_id(),
                    "elType": "widget",
                    "settings": {
                        "slider_list": [
                            {
                                "_id": self.generate_id(),
                                "title": slide.get('title', ''),
                                "subtitle": slide.get('subtitle', ''),
                                "text": slide.get('text', ''),
                                "btn_text": slide.get('button_text', ''),
                                "btn_link": {"url": slide.get('button_link', '#')},
                                "image": {"url": slide.get('background_image', ''), "id": ""}
                            }
                            for slide in config.get('slides', [])
                        ],
                        "align": "left",
                        "title_typo_typography": "custom",
                        "title_typo_font_size": {"unit": "px", "size": 45},
                        "title_typo_font_weight": "700",
                        "subtitle_color": "#b68c2f",
                        "btn_color": "#ffffff",
                        "btn_bg": "rgba(96,22,174,0)",
                        "btn_bg_hover": "#b68c2f"
                    },
                    "elements": [],
                    "widgetType": "rdn-slider"
                }]
            }],
            "isInner": False
        }
    
    def generate_service_cards_section(self, config):
        """Service Cards mit curved shape dividers"""
        section = {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "gap": "extended",
                "custom_height": {"unit": "px", "size": 300},
                "content_position": "middle",
                "structure": "30",
                "background_color": "#b68c2f",
                "box_shadow_box_shadow": {
                    "horizontal": 10,
                    "vertical": 0,
                    "blur": 0,
                    "spread": 4,
                    "color": "#ededed"
                },
                "margin": {"unit": "px", "top": -100, "right": 0, "bottom": 0, "left": 0}
            },
            "elements": [],
            "isInner": False
        }
        
        for idx, item in enumerate(config.get('items', [])):
            column = {
                "id": self.generate_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 33,
                    "background_color": "#fafafa",
                    "border_width": {"unit": "px", "top": 10, "right": 0, "bottom": 10, "left": 10},
                    "border_color": "#ededed",
                    "animation": "fadeInUp",
                    "animation_delay": idx * 200
                },
                "elements": [
                    # Inner Section 1: Image with shape divider
                    {
                        "id": self.generate_id(),
                        "elType": "section",
                        "settings": {
                            "gap": "no",
                            "shape_divider_bottom": "curve",
                            "shape_divider_bottom_color": "#fafafa",
                            "shape_divider_bottom_negative": "yes",
                            "shape_divider_bottom_above_content": "yes"
                        },
                        "elements": [{
                            "id": self.generate_id(),
                            "elType": "column",
                            "settings": {"_column_size": 100},
                            "elements": [{
                                "id": self.generate_id(),
                                "elType": "widget",
                                "settings": {
                                    "image": {"url": item.get('image', ''), "id": ""},
                                    "_border_width": {"unit": "px", "top": 4, "right": 0, "bottom": 0, "left": 0},
                                    "_border_color": "#b68c2f"
                                },
                                "elements": [],
                                "widgetType": "image"
                            }],
                            "isInner": True
                        }],
                        "isInner": True
                    },
                    # Inner Section 2: cholot-texticon
                    {
                        "id": self.generate_id(),
                        "elType": "section",
                        "settings": {
                            "gap": "no",
                            "margin": {"unit": "px", "top": -30, "right": 0, "bottom": 0, "left": 0},
                            "z_index": 2
                        },
                        "elements": [{
                            "id": self.generate_id(),
                            "elType": "column",
                            "settings": {"_column_size": 100},
                            "elements": [{
                                "id": self.generate_id(),
                                "elType": "widget",
                                "settings": {
                                    "title": item.get('title', ''),
                                    "subtitle": item.get('subtitle', ''),
                                    "text": f"<p>{item.get('text', '')}</p>",
                                    "selected_icon": {
                                        "value": item.get('icon', 'fas fa-star'),
                                        "library": "fa-solid"
                                    },
                                    "icon_color": "#ffffff",
                                    "iconbg_color": "#b68c2f",
                                    "subtitle_color": "#b68c2f",
                                    "_border_color": "#b68c2f",
                                    "_border_border": "dashed",
                                    "_padding": {"unit": "px", "top": 30, "right": 30, "bottom": 30, "left": 30}
                                },
                                "elements": [],
                                "widgetType": "cholot-texticon"
                            }],
                            "isInner": True
                        }],
                        "isInner": True
                    }
                ],
                "isInner": False
            }
            section['elements'].append(column)
        
        return section

def main():
    # YAML laden
    with open('config_riman.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Generator initialisieren
    generator = CompleteWordPressXMLGenerator()
    
    # Vollständige XML generieren
    xml_content = generator.generate_complete_xml(config)
    
    # XML speichern
    with open('complete_riman_export.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ Vollständige WordPress/Elementor XML generiert: complete_riman_export.xml")
    print("📋 Diese Datei enthält:")
    print("   → Vollständige WordPress-Struktur")
    print("   → Elementor Page Settings")
    print("   → Hero Slider mit mountains divider")
    print("   → Service Cards mit curved shape dividers")
    print("   → Alle notwendigen Meta-Daten")
    print("\n💡 Import über: WordPress Admin → Werkzeuge → Daten importieren")

if __name__ == "__main__":
    main()