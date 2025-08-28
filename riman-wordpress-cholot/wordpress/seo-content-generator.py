#!/usr/bin/env python3
"""
SEO Content Generator für WordPress/Elementor
Generiert MEHRERE Seiten auf einmal aus einer einfachen CSV/YAML
"""

import yaml
import json
import copy
from pathlib import Path
from datetime import datetime

class SEOContentGenerator:
    """
    Generiert SEO-optimierte Seiten im Batch
    """
    
    def __init__(self):
        # Lade funktionierende Basis-Template
        self.load_base_template()
    
    def load_base_template(self):
        """Lädt die FUNKTIONIERENDE demo-data-fixed.xml als Basis"""
        demo_path = Path("/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml")
        if demo_path.exists():
            with open(demo_path, 'r') as f:
                self.base_xml = f.read()
            print("✅ Basis-Template geladen")
        else:
            print("❌ demo-data-fixed.xml nicht gefunden")
            # Fallback zu minimal template
            self.base_xml = self.create_minimal_template()
    
    def create_minimal_template(self):
        """Minimales funktionierendes Template"""
        return """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>SEO Content Site</title>
    <link>https://example.com</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    {PAGES}
</channel>
</rss>"""
    
    def generate_from_yaml(self, yaml_file: str):
        """
        Generiert MEHRERE Seiten aus einer YAML Datei
        """
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"\n🚀 Generiere {len(config['pages'])} SEO-optimierte Seiten...")
        
        all_pages_xml = []
        
        for page_data in config['pages']:
            page_xml = self.generate_page(page_data)
            all_pages_xml.append(page_xml)
            print(f"   ✅ {page_data['title']} - {page_data['slug']}")
        
        # Kombiniere alle Seiten in eine XML
        final_xml = self.base_xml
        if "{PAGES}" in final_xml:
            final_xml = final_xml.replace("{PAGES}", "\n".join(all_pages_xml))
        else:
            # Insert pages into existing XML
            final_xml = self.insert_pages_into_xml(final_xml, all_pages_xml)
        
        # Speichere Output
        output_file = f"seo-content-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xml"
        with open(output_file, 'w') as f:
            f.write(final_xml)
        
        print(f"\n✅ Fertig! {output_file} erstellt")
        print(f"📊 {len(all_pages_xml)} Seiten generiert")
        return output_file
    
    def generate_page(self, page_data: dict) -> str:
        """
        Generiert eine einzelne SEO-optimierte Seite
        """
        # SEO-optimierte URL
        slug = page_data.get('slug', page_data['title'].lower().replace(' ', '-'))
        
        # Meta Description für SEO
        meta_desc = page_data.get('meta_description', f"{page_data['title']} - Professionelle Dienstleistungen")
        
        # Elementor Content mit SEO-Struktur
        elementor_data = self.create_seo_elementor_structure(page_data)
        
        page_xml = f"""
    <item>
        <title>{page_data['title']}</title>
        <link>https://example.com/{slug}/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://example.com/?page_id={page_data.get('id', 100)}</guid>
        <description>{meta_desc}</description>
        <content:encoded><![CDATA[{page_data.get('content', '')}]]></content:encoded>
        <excerpt:encoded><![CDATA[{meta_desc}]]></excerpt:encoded>
        <wp:post_id>{page_data.get('id', 100)}</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_name><![CDATA[{slug}]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
            <wp:meta_value><![CDATA[{elementor_data}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_yoast_wpseo_metadesc]]></wp:meta_key>
            <wp:meta_value><![CDATA[{meta_desc}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_yoast_wpseo_title]]></wp:meta_key>
            <wp:meta_value><![CDATA[{page_data['title']} | RIMAN GmbH]]></wp:meta_value>
        </wp:postmeta>
    </item>"""
        return page_xml
    
    def create_seo_elementor_structure(self, page_data: dict) -> str:
        """
        Erstellt SEO-optimierte Elementor-Struktur
        H1, H2, Schema Markup ready
        """
        sections = []
        
        # Hero Section mit H1
        hero = {
            "id": "hero123",
            "elType": "section",
            "settings": {"background_color": "#232323"},
            "elements": [{
                "id": "col123",
                "elType": "column",
                "elements": [
                    {
                        "id": "h1_123",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": page_data.get('h1', page_data['title']),
                            "header_size": "h1"
                        }
                    },
                    {
                        "id": "desc123",
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"<p>{page_data.get('description', '')}</p>"
                        }
                    }
                ]
            }]
        }
        sections.append(hero)
        
        # Content Sections mit H2s für SEO
        if 'sections' in page_data:
            for idx, section in enumerate(page_data['sections']):
                content_section = {
                    "id": f"section_{idx}",
                    "elType": "section",
                    "elements": [{
                        "id": f"col_{idx}",
                        "elType": "column",
                        "elements": [
                            {
                                "id": f"h2_{idx}",
                                "elType": "widget",
                                "widgetType": "heading",
                                "settings": {
                                    "title": section.get('h2', section.get('title', '')),
                                    "header_size": "h2"
                                }
                            },
                            {
                                "id": f"content_{idx}",
                                "elType": "widget",
                                "widgetType": "text-editor",
                                "settings": {
                                    "editor": f"<p>{section.get('content', '')}</p>"
                                }
                            }
                        ]
                    }]
                }
                sections.append(content_section)
        
        return json.dumps(sections, separators=(',', ':'))
    
    def insert_pages_into_xml(self, xml: str, pages: list) -> str:
        """Fügt Seiten in existierende XML ein"""
        # Find insertion point (before </channel>)
        insertion_point = xml.rfind('</channel>')
        if insertion_point > 0:
            return xml[:insertion_point] + "\n".join(pages) + "\n" + xml[insertion_point:]
        return xml


def create_example_yaml():
    """
    Erstellt eine Beispiel YAML für SEO Content
    """
    example = """# SEO Content Generator Config
# Generiere mehrere SEO-optimierte Seiten auf einmal!

site:
  name: "RIMAN GmbH"
  url: "https://riman-gmbh.de"

pages:
  # Hauptseite
  - title: "Schadstoffsanierung Berlin - RIMAN GmbH"
    slug: "schadstoffsanierung-berlin"
    h1: "Professionelle Schadstoffsanierung in Berlin"
    meta_description: "RIMAN GmbH - Ihr Experte für Schadstoffsanierung in Berlin. ✓ Asbest ✓ PCB ✓ Schimmel. 25 Jahre Erfahrung. Jetzt beraten lassen!"
    description: "Seit 1998 Ihr zuverlässiger Partner für Schadstoffsanierung"
    sections:
      - h2: "Unsere Sanierungsleistungen"
        content: "Wir bieten professionelle Sanierung von Asbest, PCB, PAK, KMF und Schimmelpilzen."
      - h2: "Warum RIMAN GmbH?"
        content: "25 Jahre Erfahrung, zertifizierte Verfahren, 24/7 Notdienst."
    id: 100

  # Service-Seite 1
  - title: "Asbestsanierung Berlin - Sicher & Zertifiziert"
    slug: "asbestsanierung-berlin"
    h1: "Asbestsanierung Berlin - TRGS 519 zertifiziert"
    meta_description: "Professionelle Asbestsanierung in Berlin nach TRGS 519. Sichere Entfernung, fachgerechte Entsorgung. Kostenlose Beratung: 030-12345678"
    description: "Zertifizierte Asbestsanierung nach höchsten Sicherheitsstandards"
    sections:
      - h2: "Asbestsanierung nach TRGS 519"
        content: "Wir sind zertifiziert nach TRGS 519 und führen alle Arbeiten nach gesetzlichen Vorgaben durch."
      - h2: "Ablauf der Asbestsanierung"
        content: "1. Analyse, 2. Abschottung, 3. Fachgerechte Entfernung, 4. Entsorgung, 5. Freimessung"
      - h2: "Kosten Asbestsanierung Berlin"
        content: "Transparente Preise, kostenlose Erstberatung, Festpreisgarantie."
    id: 101

  # Service-Seite 2
  - title: "PCB Sanierung Berlin - Umweltgerecht"
    slug: "pcb-sanierung-berlin"
    h1: "PCB-Sanierung in Berlin - Fachgerecht & Sicher"
    meta_description: "PCB-Sanierung Berlin: Professionelle Entfernung von PCB-belasteten Materialien. Umweltgerechte Entsorgung. Jetzt Angebot anfordern!"
    description: "Sichere PCB-Sanierung nach aktuellen Umweltstandards"
    sections:
      - h2: "Was ist PCB?"
        content: "Polychlorierte Biphenyle wurden bis 1989 in Baustoffen verwendet und sind gesundheitsschädlich."
      - h2: "PCB-Sanierung Verfahren"
        content: "Wir nutzen modernste Verfahren zur sicheren PCB-Entfernung und -Entsorgung."
    id: 102

  # Lokale Landing Pages
  - title: "Schadstoffsanierung Charlottenburg"
    slug: "schadstoffsanierung-charlottenburg"
    h1: "Schadstoffsanierung in Berlin-Charlottenburg"
    meta_description: "Schadstoffsanierung Charlottenburg - Schnell vor Ort. Asbest, PCB, Schimmel. 24h Service."
    id: 103

  - title: "Schadstoffsanierung Mitte"
    slug: "schadstoffsanierung-berlin-mitte"
    h1: "Schadstoffsanierung in Berlin-Mitte"
    meta_description: "Ihr Experte für Schadstoffsanierung in Berlin-Mitte. Schnelle Hilfe bei Asbest, PCB und Schimmel."
    id: 104
"""
    
    with open("seo-content-config.yaml", "w") as f:
        f.write(example)
    
    print("📝 Beispiel-Config erstellt: seo-content-config.yaml")
    return "seo-content-config.yaml"


def main():
    """
    Hauptfunktion
    """
    print("🚀 SEO CONTENT GENERATOR")
    print("=" * 50)
    print("Generiere MEHRERE SEO-optimierte Seiten auf einmal!")
    print("")
    
    # Erstelle Beispiel-Config
    config_file = create_example_yaml()
    
    # Generiere Content
    generator = SEOContentGenerator()
    output = generator.generate_from_yaml(config_file)
    
    print("\n" + "=" * 50)
    print("📋 So geht's weiter:")
    print("1. Bearbeite seo-content-config.yaml")
    print("2. Füge deine Seiten hinzu")
    print("3. python seo-content-generator.py")
    print("4. Import in WordPress")
    print("\n✨ Keine Elementor-Klickerei mehr!")


if __name__ == "__main__":
    main()