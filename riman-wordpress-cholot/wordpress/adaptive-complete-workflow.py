#!/usr/bin/env python3
"""
Adaptive Complete Workflow
YAML → Adaptive JSON → WordPress XML
"""

import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
# Import the AdaptiveElementorGenerator
import sys
sys.path.append('.')
exec(open('adaptive-elementor-generator.py').read())

class AdaptiveCompleteWorkflow:
    """
    Kompletter adaptiver Workflow mit XML-Generierung
    """
    
    def __init__(self):
        self.generator = AdaptiveElementorGenerator()
    
    def create_config_for_riman(self):
        """
        Erstellt RIMAN-spezifische Config
        """
        return {
            "page_title": "RIMAN GmbH - Schadstoffsanierung Berlin",
            "hero_title": "Professionelle Schadstoffsanierung in Berlin",
            "hero_subtitle": "Seit 1998 Ihr zuverlässiger Partner",
            "company": {
                "name": "RIMAN GmbH",
                "industry": "Schadstoffsanierung"
            },
            "services": [
                {
                    "title": "Asbestsanierung",
                    "description": "Sichere und zertifizierte Asbestentfernung nach TRGS 519",
                    "icon": "shield",
                    "color": "#e74c3c"
                },
                {
                    "title": "PCB-Sanierung", 
                    "description": "Fachgerechte PCB-Sanierung nach aktuellen Umweltstandards",
                    "icon": "flask",
                    "color": "#3498db"
                },
                {
                    "title": "Schimmelsanierung",
                    "description": "Nachhaltige Schimmelbeseitigung und -prävention",
                    "icon": "home",
                    "color": "#2ecc71"
                },
                {
                    "title": "KMF-Sanierung",
                    "description": "Professionelle Entfernung künstlicher Mineralfasern",
                    "icon": "filter",
                    "color": "#f39c12"
                },
                {
                    "title": "PAK-Sanierung",
                    "description": "Sichere Sanierung teerhaltiger Materialien",
                    "icon": "drop",
                    "color": "#9b59b6"
                },
                {
                    "title": "Schadstoffanalyse",
                    "description": "Umfassende Analyse und Bewertung von Schadstoffen",
                    "icon": "search",
                    "color": "#1abc9c"
                }
            ],
            "team": [
                {"name": "Thomas Schmidt", "position": "Geschäftsführer", "bio": "25 Jahre Erfahrung"},
                {"name": "Maria Weber", "position": "Projektleiterin", "bio": "Expertin für Großprojekte"},
                {"name": "Stefan Mueller", "position": "Technischer Leiter", "bio": "Innovationsexperte"}
            ],
            "contact": {
                "email": "info@riman-gmbh.de",
                "phone": "030-12345678",
                "address": "Musterstraße 123, 10115 Berlin"
            }
        }
    
    def generate_wordpress_xml(self, elementor_json, config):
        """
        Generiert WordPress XML mit Elementor JSON
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>{config.get('company', {}).get('name', 'Website')}</title>
    <link>https://riman-gmbh.de</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <item>
        <title>{config.get('page_title', 'Startseite')}</title>
        <link>https://riman-gmbh.de/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://riman-gmbh.de/?page_id=100</guid>
        <description>{config.get('hero_subtitle', '')}</description>
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
            <wp:meta_value><![CDATA[{json.dumps(elementor_json['content'], separators=(',', ':'))}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[elementor_header_footer]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>"""
        
        return xml_content
    
    def run_adaptive_workflow(self):
        """
        Führt den kompletten adaptiven Workflow aus
        """
        print("\n" + "="*60)
        print("🚀 ADAPTIVE WORKFLOW: Dynamic Structure Generation")
        print("="*60)
        
        # Schritt 1: Config erstellen
        print("\n📝 Schritt 1: Erstelle Config...")
        config = self.create_config_for_riman()
        print(f"   ✓ {len(config['services'])} Services")
        print(f"   ✓ {len(config.get('team', []))} Team-Mitglieder")
        
        # Schritt 2: Adaptive JSON generieren
        print("\n🧠 Schritt 2: Generiere adaptive Elementor JSON...")
        elementor_json = self.generator.generate_adaptive(config)
        
        # JSON speichern
        json_file = "adaptive-riman-elementor.json"
        with open(json_file, 'w') as f:
            json.dump(elementor_json, f, indent=2)
        print(f"   ✓ JSON gespeichert: {json_file}")
        print(f"   ✓ {len(elementor_json['content'])} Sections generiert")
        
        # Schritt 3: WordPress XML generieren
        print("\n📦 Schritt 3: Generiere WordPress XML...")
        xml_content = self.generate_wordpress_xml(elementor_json, config)
        
        # XML speichern
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        xml_file = f"adaptive-riman-{timestamp}.xml"
        with open(xml_file, 'w') as f:
            f.write(xml_content)
        print(f"   ✓ XML gespeichert: {xml_file}")
        print(f"   ✓ Größe: {len(xml_content):,} Zeichen")
        
        # Erfolg
        print("\n" + "="*60)
        print("✅ ADAPTIVE WORKFLOW ERFOLGREICH!")
        print("="*60)
        
        print("\n📊 Ergebnis:")
        print(f"   • Elementor JSON: {json_file}")
        print(f"   • WordPress XML: {xml_file}")
        print(f"   • Struktur: Dynamisch angepasst an Content")
        
        print("\n🎯 Vorteile gegenüber statischem System:")
        print("   ✓ Passt Layout an (3 vs 6 Services)")
        print("   ✓ Fügt/entfernt Sections nach Bedarf")
        print("   ✓ Optimiert Spaltenbreiten automatisch")
        print("   ✓ Wählt passende Widgets intelligent")
        
        print("\n📋 Import-Anleitung:")
        print("   1. WordPress Admin → Tools → Import")
        print("   2. WordPress Importer wählen")
        print(f"   3. {xml_file} hochladen")
        print("   4. Import starten")
        
        return xml_file
    
    def generate_seo_pages_batch(self):
        """
        Generiert mehrere SEO-Landing Pages
        """
        districts = [
            "Charlottenburg", "Mitte", "Prenzlauer Berg",
            "Kreuzberg", "Schöneberg", "Neukölln"
        ]
        
        print("\n" + "="*60)
        print("🌐 BATCH SEO PAGES GENERATION")
        print("="*60)
        
        xml_files = []
        
        for district in districts:
            print(f"\n📍 Generiere für {district}...")
            
            # Angepasste Config für District
            config = self.create_config_for_riman()
            config['page_title'] = f"Schadstoffsanierung {district} - RIMAN GmbH"
            config['hero_title'] = f"Schadstoffsanierung in Berlin-{district}"
            config['hero_subtitle'] = f"Ihr lokaler Partner in {district}"
            
            # Reduzierte Services für lokale Pages
            config['services'] = config['services'][:3]  # Nur Top 3
            
            # Generiere adaptive JSON
            elementor_json = self.generator.generate_adaptive(config)
            
            # Generiere XML
            xml_content = self.generate_wordpress_xml(elementor_json, config)
            
            # Speichere
            xml_file = f"seo-{district.lower()}.xml"
            with open(xml_file, 'w') as f:
                f.write(xml_content)
            
            xml_files.append(xml_file)
            print(f"   ✓ {xml_file} erstellt")
        
        print(f"\n✅ {len(xml_files)} SEO Pages generiert!")
        return xml_files


def main():
    """
    Hauptfunktion für adaptive Generierung
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║          ADAPTIVE COMPLETE WORKFLOW                         ║
║                                                              ║
║   Problem gelöst:                                           ║
║   ✓ Dynamische Struktur-Anpassung                         ║
║   ✓ Intelligente Widget-Auswahl                           ║
║   ✓ WordPress XML Generation                              ║
║   ✓ SEO Batch Processing                                  ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    workflow = AdaptiveCompleteWorkflow()
    
    # Single Page generieren
    xml_file = workflow.run_adaptive_workflow()
    
    # Optional: Batch SEO Pages
    print("\n💡 Möchtest du auch SEO Landing Pages generieren?")
    print("   (Uncomment the next line to generate)")
    # workflow.generate_seo_pages_batch()
    
    print("\n🎯 FINALE LÖSUNG:")
    print("✅ Template wird nicht nur befüllt, sondern ANGEPASST")
    print("✅ 3 Services = 1 Reihe, 6 Services = 2 Reihen")
    print("✅ Widgets werden intelligent gewählt")
    print("✅ WordPress XML ready for import")


if __name__ == "__main__":
    main()