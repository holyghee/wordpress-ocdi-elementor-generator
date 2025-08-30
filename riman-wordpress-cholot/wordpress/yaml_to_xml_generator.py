#!/usr/bin/env python3
"""
YAML zu WordPress XML Generator
Generiert aus einfacher YAML-Config eine importierbare WordPress XML mit Elementor-Daten
"""

import yaml
import json
from pathlib import Path
from datetime import datetime
from elementor_generator_v2 import ElementorGeneratorV2

def yaml_to_wordpress_xml(yaml_file: str, output_xml: str = 'generated_from_yaml.xml'):
    """Konvertiert YAML Config zu WordPress XML"""
    
    # Lade YAML
    with open(yaml_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"📖 Lade YAML Config: {yaml_file}")
    
    # Initialisiere Generator
    generator = ElementorGeneratorV2()
    
    site_info = config.get('site', {})
    pages = config.get('pages', [])
    
    # Erstelle XML Struktur
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/">

<channel>
    <title>{site_info.get('name', 'Website')}</title>
    <link>{site_info.get('url', 'http://localhost:8081')}</link>
    <description>{site_info.get('tagline', '')}</description>
    <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>{site_info.get('url', 'http://localhost:8081')}</wp:base_site_url>
    <wp:base_blog_url>{site_info.get('url', 'http://localhost:8081')}</wp:base_blog_url>
'''
    
    # Verarbeite jede Seite
    post_id = 6000
    for page_config in pages:
        post_id += 1
        
        # Generiere Elementor Sections
        sections = []
        
        for section_config in page_config.get('sections', []):
            section_type = section_config.get('type')
            
            if section_type == 'hero':
                # Hero Section
                section = {
                    "id": generator.generate_unique_id(),
                    "elType": "section",
                    "settings": {
                        "stretch_section": "section-stretched",
                        "layout": "full_width"
                    },
                    "elements": [{
                        "id": generator.generate_unique_id(),
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [{
                            "id": generator.generate_unique_id(),
                            "elType": "widget",
                            "widgetType": "heading",
                            "settings": {
                                "title": section_config.get('title', ''),
                                "header_size": "h1",
                                "align": "center"
                            }
                        }]
                    }]
                }
                sections.append(section)
                
            elif section_type == 'service_cards':
                # Service Cards Section
                cards = section_config.get('cards', [])
                service_section = generator.generate_service_cards_section(cards)
                sections.append(service_section)
                
            elif section_type == 'contact':
                # Contact Section
                contact_section = {
                    "id": generator.generate_unique_id(),
                    "elType": "section",
                    "settings": {
                        "background_background": "classic",
                        "background_color": "#1a1a1a",
                        "padding": {"unit": "px", "top": 80, "bottom": 80}
                    },
                    "elements": [{
                        "id": generator.generate_unique_id(),
                        "elType": "column",
                        "settings": {"_column_size": 100},
                        "elements": [
                            {
                                "id": generator.generate_unique_id(),
                                "elType": "widget",
                                "widgetType": "heading",
                                "settings": {
                                    "title": section_config.get('title', 'Kontakt'),
                                    "header_size": "h2",
                                    "align": "center",
                                    "title_color": "#ffffff"
                                }
                            },
                            {
                                "id": generator.generate_unique_id(),
                                "elType": "widget",
                                "widgetType": "shortcode",
                                "settings": {
                                    "shortcode": f'[contact-form-7 id="{section_config.get("form_id", "1")}" title="Contact form 1"]'
                                }
                            }
                        ]
                    }]
                }
                sections.append(contact_section)
        
        # Konvertiere zu Elementor JSON
        elementor_data = json.dumps(sections, ensure_ascii=False)
        
        # Escape für XML
        elementor_data = elementor_data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Füge Page Item zu XML hinzu
        xml_content += f'''
    <item>
        <title><![CDATA[{page_config.get('title', 'Untitled')}]]></title>
        <link>{site_info.get('url', 'http://localhost:8081')}/?page_id={post_id}</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">{site_info.get('url', 'http://localhost:8081')}/?page_id={post_id}</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>{post_id}</wp:post_id>
        <wp:post_date><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[{page_config.get('slug', 'page-' + str(post_id))}]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[elementor_header_footer]]></wp:meta_value>
        </wp:postmeta>
        
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_version]]></wp:meta_key>
            <wp:meta_value><![CDATA[3.18.3]]></wp:meta_value>
        </wp:postmeta>
        
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
            <wp:meta_value><![CDATA[{elementor_data}]]></wp:meta_value>
        </wp:postmeta>
    </item>
'''
    
    # Schließe XML
    xml_content += '''
</channel>
</rss>'''
    
    # Speichere XML
    with open(output_xml, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"\n✅ XML generiert: {output_xml}")
    print(f"📦 Enthält {len(pages)} Seite(n)")
    print(f"\n🎯 Import in WordPress:")
    print(f"   1. WordPress Admin → Werkzeuge → Importieren")
    print(f"   2. WordPress Importer wählen")
    print(f"   3. Datei '{output_xml}' hochladen")
    print(f"   4. Seite erscheint unter: {site_info.get('url', 'http://localhost:8081')}/?page_id={post_id}")
    
    return output_xml


def main():
    """Hauptfunktion"""
    import sys
    
    yaml_file = 'riman_simple.yaml'
    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
    
    output_file = yaml_to_wordpress_xml(yaml_file, 'riman_from_yaml.xml')
    
    print(f"\n🎉 Fertig!")
    print(f"   YAML Config: {yaml_file}")
    print(f"   → WordPress XML: {output_file}")


if __name__ == "__main__":
    main()