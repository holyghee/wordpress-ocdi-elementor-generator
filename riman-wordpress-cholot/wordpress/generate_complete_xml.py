#!/usr/bin/env python3
"""
Generiert eine komplette WordPress XML mit Service Cards aus Templates
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from elementor_generator_v2 import ElementorGeneratorV2

def create_wordpress_xml():
    """Erstellt komplette WordPress XML mit Elementor Daten"""
    
    # Initialisiere Generator
    generator = ElementorGeneratorV2()
    
    # Generiere Service Cards Section
    service_cards_config = [
        {
            'title': 'Asbestsanierung',
            'subtitle': 'ZERTIFIZIERT',
            'description': 'Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.',
            'icon': 'fas fa-shield-alt',
            'image': 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg'
        },
        {
            'title': 'PCB-Sanierung',
            'subtitle': 'FACHGERECHT',
            'description': 'Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.',
            'icon': 'fas fa-industry',
            'image': 'http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung-fachgerechte-entsorgung.jpg'
        },
        {
            'title': 'Schimmelsanierung',
            'subtitle': 'NACHHALTIG',
            'description': 'Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.',
            'icon': 'fas fa-home',
            'image': 'http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung-praevention-nachhaltig.jpg'
        }
    ]
    
    # Generiere Sections
    sections = []
    
    # 1. Hero Section (wenn Template vorhanden)
    if 'hero' in generator.templates and 'hero_home' in generator.templates['hero']:
        hero_template = generator.templates['hero']['hero_home']
        hero_section = generator.process_template(hero_template, {
            'title': 'Professionelle Mediation & Sanierung',
            'subtitle': 'Ihr Partner für Konfliktlösung und Schadstoffsanierung'
        })
        sections.append(hero_section)
    
    # 2. Service Cards Section
    service_cards_section = generator.generate_service_cards_section(service_cards_config)
    sections.append(service_cards_section)
    
    # 3. Contact Section
    contact_section = {
        "id": generator.generate_unique_id(),
        "elType": "section",
        "settings": {
            "background_background": "classic",
            "background_color": "#1a1a1a",
            "padding": {"unit": "px", "top": 80, "bottom": 80}
        },
        "elements": [
            {
                "id": generator.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": generator.generate_unique_id(),
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "Kontaktieren Sie uns",
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
                            "shortcode": '[contact-form-7 id="1" title="Contact form 1"]'
                        }
                    }
                ]
            }
        ]
    }
    sections.append(contact_section)
    
    # Konvertiere zu Elementor JSON
    elementor_data = json.dumps(sections, ensure_ascii=False)
    
    # Erstelle XML Struktur
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
    
    channel = ET.SubElement(rss, 'channel')
    
    # Site Info
    ET.SubElement(channel, 'title').text = 'RIMAN GmbH'
    ET.SubElement(channel, 'link').text = 'http://localhost:8081'
    ET.SubElement(channel, 'description').text = 'Professionelle Mediation und Sanierung'
    ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    ET.SubElement(channel, 'language').text = 'de-DE'
    ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
    ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = 'http://localhost:8081'
    ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = 'http://localhost:8081'
    
    # Page Item
    item = ET.SubElement(channel, 'item')
    
    ET.SubElement(item, 'title').text = 'RIMAN Startseite - Mit Service Cards'
    ET.SubElement(item, 'link').text = 'http://localhost:8081/?page_id=5000'
    ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
    
    guid = ET.SubElement(item, 'guid', isPermaLink='false')
    guid.text = 'http://localhost:8081/?page_id=5000'
    
    ET.SubElement(item, 'description').text = ''
    ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
    ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
    
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = '5000'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = 'riman-startseite-complete'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
    ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
    
    # Postmeta
    postmeta1 = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
    ET.SubElement(postmeta1, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_page_template'
    ET.SubElement(postmeta1, '{http://wordpress.org/export/1.2/}meta_value').text = 'elementor_header_footer'
    
    postmeta2 = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
    ET.SubElement(postmeta2, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_version'
    ET.SubElement(postmeta2, '{http://wordpress.org/export/1.2/}meta_value').text = '3.18.3'
    
    postmeta3 = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
    ET.SubElement(postmeta3, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_edit_mode'
    ET.SubElement(postmeta3, '{http://wordpress.org/export/1.2/}meta_value').text = 'builder'
    
    postmeta4 = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
    ET.SubElement(postmeta4, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
    meta_value = ET.SubElement(postmeta4, '{http://wordpress.org/export/1.2/}meta_value')
    meta_value.text = elementor_data
    
    # Pretty print
    xml_str = ET.tostring(rss, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    # Entferne leere Zeilen
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    pretty_xml = '\n'.join(lines)
    
    # Speichere XML
    output_file = 'riman_complete_with_service_cards.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"✅ XML generiert: {output_file}")
    print(f"📦 Enthält:")
    print(f"   - Hero Section (falls Template vorhanden)")
    print(f"   - {len(service_cards_config)} Service Cards mit Curved Shape Dividers")
    print(f"   - Contact Section")
    print(f"\n🎯 Importiere in WordPress:")
    print(f"   1. WordPress Admin → Werkzeuge → Importieren")
    print(f"   2. Wähle '{output_file}'")
    print(f"   3. Die Seite erscheint unter: http://localhost:8081/?page_id=5000")
    
    return output_file

if __name__ == "__main__":
    create_wordpress_xml()