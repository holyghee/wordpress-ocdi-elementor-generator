#!/usr/bin/env python3
"""
Elementor Structure Fix
Korrigiert die Column-Struktur für Elementor-Kompatibilität
"""

import json
import yaml
from datetime import datetime

def fix_elementor_structure():
    """
    Erstellt eine korrekte Elementor-Struktur die funktioniert
    """
    
    # Korrekte Elementor-Struktur basierend auf dem working template
    structure = [
        {
            "id": "hero_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "background_background": "classic",
                "background_color": "#ffffff",
                "padding": {
                    "unit": "px",
                    "top": "60",
                    "right": "0",
                    "bottom": "60",
                    "left": "0"
                }
            },
            "elements": [
                {
                    "id": "hero_column",
                    "elType": "column",
                    "settings": {
                        "_column_size": 100,  # WICHTIG: _column_size muss gesetzt sein!
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "hero_title",
                            "elType": "widget",
                            "widgetType": "cholot-title",
                            "settings": {
                                "title": "Professionelle Schadstoffsanierung in Berlin",
                                "align": "center",
                                "title_color": "#000000",
                                "desc_typography_typography": "custom",
                                "desc_typography_font_size": {
                                    "unit": "px",
                                    "size": 35
                                }
                            }
                        },
                        {
                            "id": "hero_text",
                            "elType": "widget",
                            "widgetType": "text-editor",
                            "settings": {
                                "editor": "<p>Seit 1998 Ihr zuverlässiger Partner</p>",
                                "align": "center"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "id": "services_section",
            "elType": "section", 
            "settings": {
                "layout": "boxed",
                "padding": {
                    "unit": "px", 
                    "top": "60",
                    "bottom": "60"
                }
            },
            "elements": [
                # Service 1
                {
                    "id": "service_col_1",
                    "elType": "column",
                    "settings": {
                        "_column_size": 33,  # 3 Spalten = je 33%
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "service_1",
                            "elType": "widget",
                            "widgetType": "cholot-texticon",
                            "settings": {
                                "title": "Asbestsanierung",
                                "text": "<p>Sichere und zertifizierte Asbestentfernung nach TRGS 519</p>",
                                "icon": "fa fa-shield",
                                "icon_color": "#e74c3c",
                                "title_color": "#232323",
                                "text_color": "#666666",
                                "icon_size": {
                                    "size": 60,
                                    "unit": "px"
                                }
                            }
                        }
                    ]
                },
                # Service 2
                {
                    "id": "service_col_2", 
                    "elType": "column",
                    "settings": {
                        "_column_size": 33,
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "service_2",
                            "elType": "widget", 
                            "widgetType": "cholot-texticon",
                            "settings": {
                                "title": "PCB-Sanierung",
                                "text": "<p>Fachgerechte PCB-Sanierung nach aktuellen Umweltstandards</p>",
                                "icon": "fa fa-flask",
                                "icon_color": "#3498db", 
                                "title_color": "#232323",
                                "text_color": "#666666",
                                "icon_size": {
                                    "size": 60,
                                    "unit": "px"
                                }
                            }
                        }
                    ]
                },
                # Service 3
                {
                    "id": "service_col_3",
                    "elType": "column",
                    "settings": {
                        "_column_size": 33,
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "service_3",
                            "elType": "widget",
                            "widgetType": "cholot-texticon", 
                            "settings": {
                                "title": "Schimmelsanierung",
                                "text": "<p>Nachhaltige Schimmelbeseitigung und -prävention</p>",
                                "icon": "fa fa-home",
                                "icon_color": "#2ecc71",
                                "title_color": "#232323", 
                                "text_color": "#666666",
                                "icon_size": {
                                    "size": 60,
                                    "unit": "px"
                                }
                            }
                        }
                    ]
                }
            ]
        },
        {
            "id": "contact_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "background_background": "classic",
                "background_color": "#232323",
                "padding": {
                    "unit": "px",
                    "top": "60", 
                    "bottom": "60"
                }
            },
            "elements": [
                {
                    "id": "contact_column",
                    "elType": "column",
                    "settings": {
                        "_column_size": 100,
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "contact_heading",
                            "elType": "widget",
                            "widgetType": "heading",
                            "settings": {
                                "title": "Kontakt",
                                "header_size": "h2",
                                "align": "center",
                                "title_color": "#ffffff"
                            }
                        },
                        {
                            "id": "contact_info",
                            "elType": "widget",
                            "widgetType": "text-editor",
                            "settings": {
                                "editor": "<p style='color: white; text-align: center;'>📧 info@riman-gmbh.de<br>📞 030-12345678<br>📍 Musterstraße 123, 10115 Berlin</p>"
                            }
                        }
                    ]
                }
            ]
        }
    ]
    
    return structure

def generate_fixed_xml():
    """
    Generiert korrigierte WordPress XML
    """
    structure = fix_elementor_structure()
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>RIMAN GmbH</title>
    <link>https://riman-gmbh.de</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <item>
        <title>RIMAN GmbH - Schadstoffsanierung Berlin</title>
        <link>https://riman-gmbh.de/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://riman-gmbh.de/?page_id=100</guid>
        <description>Seit 1998 Ihr zuverlässiger Partner</description>
        <content:encoded><![CDATA[]]></content:encoded>
        <wp:post_id>100</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_name><![CDATA[home]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:is_sticky>0</wp:is_sticky>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_template_type]]></wp:meta_key>
            <wp:meta_value><![CDATA[wp-page]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_version]]></wp:meta_key>
            <wp:meta_value><![CDATA[3.17.0]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
            <wp:meta_value><![CDATA[{json.dumps(structure, separators=(',', ':'))}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[elementor_header_footer]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>"""
    
    return xml_content

def main():
    """
    Erzeugt korrigierte Version
    """
    print("🔧 ELEMENTOR STRUCTURE FIX")
    print("=" * 50)
    print("Repariert die Column-Struktur für Elementor")
    
    # Generiere korrekte Struktur
    structure = fix_elementor_structure()
    
    # Speichere JSON
    with open("fixed-elementor-structure.json", "w") as f:
        json.dump(structure, f, indent=2)
    
    # Generiere XML
    xml = generate_fixed_xml()
    with open("fixed-riman-elementor.xml", "w") as f:
        f.write(xml)
    
    print("✅ Dateien erstellt:")
    print("   • fixed-elementor-structure.json")
    print("   • fixed-riman-elementor.xml")
    
    print("\n🎯 Wichtige Fixes:")
    print("   ✓ _column_size für alle Columns gesetzt")
    print("   ✓ Korrekte elType: column (nicht container)")
    print("   ✓ Korrekte Cholot-Widget Settings")
    print("   ✓ Proper nesting: section → column → widget")
    
    print("\n📋 Testen:")
    print("   1. fixed-riman-elementor.xml in WordPress importieren")
    print("   2. Seite öffnen - sollte keine PHP Warnings haben")
    print("   3. Services sollten korrekt in 3 Spalten angezeigt werden")

if __name__ == "__main__":
    main()