#!/usr/bin/env python3
"""
Content-Design Separator - Trennt Inhalt von Design sauber
"""

import json
from typing import Dict, List

class ContentDesignSystem:
    """
    Kern-Idee: Design ist FEST, nur Content ist VARIABEL
    """
    
    def demonstrate_the_concept(self):
        """
        Zeigt das Konzept anhand eines echten Cholot Widgets
        """
        
        # Das ist ein ECHTER Cholot Hero-Slider mit 400+ Parametern
        cholot_hero_design = {
            "id": "4a96e0e5",
            "widgetType": "rdn-slider",
            "settings": {
                # ========== DESIGN (bleibt IMMER gleich) ==========
                "align": "left",
                "title_typo_typography": "custom",
                "title_typo_font_size": {"unit": "px", "size": 45},
                "title_typo_font_weight": "700",
                "title_typo_line_height": {"unit": "em", "size": 1.1},
                "subtitle_typo_font_size": {"unit": "px", "size": 15},
                "slider_width": {"unit": "px", "size": 1170},
                "arrow_width": {"unit": "px", "size": 30},
                "linecolor": "#b68c2f",
                "slider_mask": "rgba(0,0,0,0.85)",
                "arrow_color_hover": "#ffffff",
                "btn_border_radius": {"unit": "px", "top": 0, "right": 0},
                # ... noch 380 weitere Design-Parameter ...
                
                # ========== CONTENT (das ändern wir) ==========
                "slider_list": [
                    {
                        "title": "{{TITLE}}",        # <-- Variable!
                        "subtitle": "{{SUBTITLE}}",  # <-- Variable!
                        "text": "{{TEXT}}",          # <-- Variable!
                        "btn_text": "{{BUTTON}}",    # <-- Variable!
                        "image": {
                            "url": "{{IMAGE_URL}}"   # <-- Variable!
                        }
                    }
                ]
            }
        }
        
        print("🎯 Das Konzept:")
        print("\n1️⃣ DESIGN (400+ Parameter) = Vorgefertigt vom Profi")
        print("   - Font-Größen, Abstände, Animationen, Farben...")
        print("   - Bleibt IMMER gleich")
        print("   - Wurde einmal in Elementor perfekt eingestellt")
        
        print("\n2️⃣ CONTENT (5-10 Variablen) = Vom User/KI gefüllt")
        print("   - Titel, Texte, Bilder")
        print("   - Das einzige was sich ändert")
        print("   - Kann jeder ausfüllen")
        
        return cholot_hero_design
    
    def extract_content_structure(self, elementor_json: Dict) -> Dict:
        """
        Extrahiert NUR die Content-Felder aus komplexer JSON
        """
        content_fields = {}
        
        def find_content(obj, path=""):
            """Findet alle Text/Bild-Felder"""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # Text-Content
                    if key in ['title', 'subtitle', 'text', 'description', 
                               'btn_text', 'button_text', 'heading']:
                        content_fields[f"{path}.{key}"] = {
                            "type": "text",
                            "value": value,
                            "path": path
                        }
                    # Bilder
                    elif key == 'url' and isinstance(value, str) and (
                        '.jpg' in value or '.png' in value
                    ):
                        content_fields[f"{path}.image"] = {
                            "type": "image",
                            "value": value,
                            "path": path
                        }
                    # Listen (z.B. Services, Testimonials)
                    elif key in ['slider_list', 'services', 'testimonials', 'items']:
                        content_fields[f"{path}.{key}"] = {
                            "type": "list",
                            "count": len(value) if isinstance(value, list) else 0,
                            "path": path
                        }
                    
                    # Rekursiv weitersuchen
                    if isinstance(value, (dict, list)):
                        find_content(value, f"{path}.{key}" if path else key)
            
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    find_content(item, f"{path}[{idx}]")
        
        find_content(elementor_json)
        return content_fields
    
    def create_content_map(self, template_file: str):
        """
        Erstellt eine Content-Map für ein Template
        """
        print(f"\n📋 Analysiere Template: {template_file}")
        
        with open(template_file, 'r') as f:
            template = json.load(f)
        
        all_content = {}
        
        for section_idx, section in enumerate(template):
            section_content = self.extract_content_structure(section)
            
            # Gruppiere nach Section
            all_content[f"section_{section_idx}"] = {
                "structure": section.get('settings', {}).get('structure', '100'),
                "content_fields": section_content
            }
        
        # Zeige Ergebnisse
        print(f"\n✅ Gefundene Content-Felder:")
        for section, data in all_content.items():
            print(f"\n{section} (Layout: {data['structure']}):")
            for field, info in data['content_fields'].items():
                if info['type'] == 'text':
                    print(f"  📝 {field}: '{info['value'][:50]}...'")
                elif info['type'] == 'image':
                    print(f"  🖼️ {field}: {info['value'].split('/')[-1]}")
                elif info['type'] == 'list':
                    print(f"  📋 {field}: {info['count']} items")
        
        return all_content
    
    def demonstrate_simple_content_file(self):
        """
        Zeigt wie einfach die Content-Datei sein kann
        """
        simple_content = {
            "hero": {
                "title": "RIMAN GmbH - Professionelle Schadstoffsanierung",
                "subtitle": "Seit 1998 Ihr zuverlässiger Partner",
                "text": "Wir bieten fachgerechte Lösungen für Asbest-, PCB- und Schimmelsanierung.",
                "button": "Kostenloses Angebot",
                "image": "riman-hero.jpg"
            },
            "services": [
                {
                    "title": "Asbestsanierung",
                    "text": "Sichere und zertifizierte Entfernung",
                    "icon": "shield"
                },
                {
                    "title": "PCB-Sanierung",
                    "text": "Umweltgerechte Entsorgung",
                    "icon": "recycle"
                },
                {
                    "title": "Schimmelsanierung",
                    "text": "Nachhaltige Beseitigung",
                    "icon": "home"
                }
            ],
            "about": {
                "title": "25 Jahre Erfahrung",
                "text": "Seit 1998 sind wir Ihr Partner für professionelle Schadstoffsanierung..."
            }
        }
        
        print("\n" + "="*60)
        print("💡 So einfach kann die Content-Datei sein:")
        print("="*60)
        print(json.dumps(simple_content, indent=2, ensure_ascii=False))
        
        print("\n✨ Das System:")
        print("1. User schreibt nur diesen simplen Content")
        print("2. System nimmt Cholot-Template mit 400+ Design-Parametern")
        print("3. System ersetzt {{TITLE}} → 'RIMAN GmbH...'")
        print("4. Fertig ist die professionelle Website!")
        
        return simple_content
    
    def show_the_magic(self):
        """
        Zeigt wie Design und Content zusammenkommen
        """
        print("\n" + "="*60)
        print("🎨 DIE MAGIE: Design + Content = Website")
        print("="*60)
        
        print("""
        DESIGN (Cholot Template)           CONTENT (User Input)
        ========================           ====================
        {                                  {
          "settings": {                      "hero": {
            "font_size": 45,                  "title": "RIMAN GmbH"
            "color": "#b68c2f",              }
            "padding": 30,                  }
            "animation": "fadeIn",
            ... 400 Parameter ...
            
            "title": "{{TITLE}}"  <-------- System ersetzt
          }
        }
        
                        ↓
                        
                FERTIGE WEBSITE
                ==============
                {
                  "settings": {
                    "font_size": 45,
                    "color": "#b68c2f",
                    "title": "RIMAN GmbH"  ✅
                  }
                }
        """)
        
        print("\n🚀 Vorteile:")
        print("✅ User muss nur Content schreiben (5 Minuten)")
        print("✅ Design ist immer professionell (vom Template)")
        print("✅ KI kann Content generieren (simple Struktur)")
        print("✅ 1000 Websites aus einem Template möglich")


def main():
    """Demo des Konzepts"""
    
    system = ContentDesignSystem()
    
    # Zeige das Grundkonzept
    system.demonstrate_the_concept()
    
    # Zeige simple Content-Datei
    system.demonstrate_simple_content_file()
    
    # Zeige wie es zusammenkommt
    system.show_the_magic()
    
    # Analysiere echtes Template
    import os
    if os.path.exists("templates/home-page.json"):
        system.create_content_map("templates/home-page.json")
    
    print("\n" + "="*60)
    print("📌 FAZIT:")
    print("="*60)
    print("""
    Wir generieren NICHT die komplexe Elementor JSON!
    Wir FÜLLEN nur Content in professionelle Templates!
    
    Es ist wie ein Formular:
    - Template = Formular-Layout (komplex, vom Designer)
    - Content = Ausgefüllte Felder (simpel, vom User)
    - Generator = Fügt beides zusammen
    
    Das ist realistisch und funktioniert!
    """)


if __name__ == "__main__":
    main()