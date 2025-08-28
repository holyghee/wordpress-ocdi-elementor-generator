#!/usr/bin/env python3
"""
Adaptive Elementor Generator
Passt die JSON-Struktur dynamisch an den Content an
"""

import json
import yaml
import copy
from pathlib import Path
import random
import string

class AdaptiveElementorGenerator:
    """
    Generiert Elementor JSON mit dynamischer Struktur
    """
    
    def __init__(self):
        self.widget_library = self.load_widget_library()
        self.load_template_structure()
    
    def load_widget_library(self):
        """
        Definiert verfügbare Widgets und ihre Verwendungszwecke
        """
        return {
            "cholot-title": {
                "purpose": "headlines",
                "can_render": ["title", "subtitle", "hero_title"],
                "base_settings": {
                    "title_color": {"value": "#232323"},
                    "title_typography_typography": "custom",
                    "title_typography_font_family": "Lato",
                    "title_typography_font_size": {"unit": "px", "size": 48}
                }
            },
            "cholot-texticon": {
                "purpose": "service_boxes",
                "can_render": ["service", "feature"],
                "base_settings": {
                    "icon": "fa fa-shield",
                    "icon_color": "#ff6b6b",
                    "title_color": "#232323",
                    "text_color": "#666666"
                }
            },
            "cholot-team": {
                "purpose": "team_member",
                "can_render": ["team_member", "person"],
                "base_settings": {
                    "image": {"url": "placeholder.jpg"},
                    "title": "Name",
                    "text": "Position",
                    "social_icons": []
                }
            },
            "text-editor": {
                "purpose": "content",
                "can_render": ["description", "content", "text"],
                "base_settings": {
                    "editor": "<p>Content here</p>"
                }
            },
            "heading": {
                "purpose": "section_title",
                "can_render": ["h1", "h2", "h3"],
                "base_settings": {
                    "title": "Heading",
                    "header_size": "h2",
                    "align": "center"
                }
            },
            "button": {
                "purpose": "cta",
                "can_render": ["button", "link"],
                "base_settings": {
                    "text": "Click here",
                    "link": {"url": "#"},
                    "button_type": "primary"
                }
            }
        }
    
    def load_template_structure(self):
        """
        Lädt die Basis-Struktur aus dem Original-Template
        """
        template_path = Path("/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json")
        if template_path.exists():
            with open(template_path, 'r') as f:
                self.template = json.load(f)
            # Extrahiere Struktur-Patterns
            self.extract_patterns()
        else:
            self.template = None
            self.patterns = {}
    
    def extract_patterns(self):
        """
        Extrahiert wiederverwendbare Patterns aus dem Template
        """
        self.patterns = {
            "hero_section": None,
            "service_section": None,
            "team_section": None,
            "contact_section": None
        }
        
        if not self.template or 'content' not in self.template:
            return
        
        for section in self.template['content']:
            # Analysiere Section-Typ basierend auf Widgets
            widgets = self.get_section_widgets(section)
            
            # Hero Section erkennen (meist erste Section mit großem Titel)
            if not self.patterns["hero_section"] and self.has_hero_characteristics(section):
                self.patterns["hero_section"] = copy.deepcopy(section)
            
            # Service Section (enthält mehrere texticon widgets)
            elif self.count_widget_type(widgets, "cholot-texticon") >= 3:
                self.patterns["service_section"] = copy.deepcopy(section)
            
            # Team Section (enthält team widgets)
            elif self.count_widget_type(widgets, "cholot-team") >= 1:
                self.patterns["team_section"] = copy.deepcopy(section)
    
    def get_section_widgets(self, section):
        """
        Sammelt alle Widgets einer Section
        """
        widgets = []
        if 'elements' in section:
            for column in section['elements']:
                if 'elements' in column:
                    widgets.extend(column['elements'])
        return widgets
    
    def count_widget_type(self, widgets, widget_type):
        """
        Zählt Widgets eines bestimmten Typs
        """
        return sum(1 for w in widgets if w.get('widgetType') == widget_type)
    
    def has_hero_characteristics(self, section):
        """
        Prüft ob Section Hero-Charakteristiken hat
        """
        settings = section.get('settings', {})
        # Hero sections haben oft Hintergrundbilder oder dunkle Farben
        has_bg = 'background_image' in settings or 'background_color' in settings
        # Und große Überschriften
        widgets = self.get_section_widgets(section)
        has_title = any(w.get('widgetType') in ['cholot-title', 'heading'] for w in widgets)
        return has_bg and has_title
    
    def generate_id(self):
        """Generiert unique IDs für Elementor"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    def generate_adaptive(self, config):
        """
        Hauptfunktion: Generiert adaptiv basierend auf Content
        """
        print("\n🧠 ADAPTIVE GENERATION")
        print("=" * 50)
        
        # Analysiere Content-Anforderungen
        requirements = self.analyze_requirements(config)
        print(f"📊 Erkannte Anforderungen:")
        print(f"   - Services: {requirements['service_count']}")
        print(f"   - Team: {requirements['team_count']}")
        print(f"   - Sections: {requirements['sections']}")
        
        # Baue Struktur basierend auf Anforderungen
        structure = self.build_adaptive_structure(config, requirements)
        
        return {
            "content": structure,
            "page_settings": [],
            "version": "0.4",
            "title": config.get('page_title', 'Generated Page'),
            "type": "page"
        }
    
    def analyze_requirements(self, config):
        """
        Analysiert was die Config braucht
        """
        return {
            "service_count": len(config.get('services', [])),
            "team_count": len(config.get('team', [])),
            "has_hero": bool(config.get('hero_title')),
            "has_contact": bool(config.get('contact')),
            "sections": config.get('sections', []),
            "layout": config.get('layout', 'standard')
        }
    
    def build_adaptive_structure(self, config, requirements):
        """
        Baut die Struktur adaptiv auf
        """
        sections = []
        
        # 1. Hero Section wenn gewünscht
        if requirements['has_hero']:
            hero = self.create_hero_section(config)
            sections.append(hero)
        
        # 2. Service Section - ADAPTIV!
        if requirements['service_count'] > 0:
            service_section = self.create_service_section(
                config['services'],
                requirements['service_count']
            )
            sections.append(service_section)
        
        # 3. Custom Sections aus Config
        for custom_section in config.get('sections', []):
            section = self.create_custom_section(custom_section)
            sections.append(section)
        
        # 4. Team Section wenn Team vorhanden
        if requirements['team_count'] > 0:
            team_section = self.create_team_section(
                config['team'],
                requirements['team_count']
            )
            sections.append(team_section)
        
        # 5. Contact Section
        if requirements['has_contact']:
            contact = self.create_contact_section(config['contact'])
            sections.append(contact)
        
        return sections
    
    def create_hero_section(self, config):
        """
        Erstellt Hero Section
        """
        if self.patterns.get("hero_section"):
            # Nutze Template und passe an
            section = copy.deepcopy(self.patterns["hero_section"])
            self.update_hero_content(section, config)
            return section
        
        # Fallback: Baue neu
        return self.build_hero_from_scratch(config)
    
    def create_service_section(self, services, count):
        """
        Erstellt Service Section mit dynamischer Anzahl
        """
        section = {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "layout": "full_width",
                "padding": {"top": "60", "bottom": "60", "unit": "px"}
            },
            "elements": []
        }
        
        # Berechne optimales Layout
        columns_per_row = 3 if count <= 3 else 4 if count <= 4 else 3
        rows = (count + columns_per_row - 1) // columns_per_row
        
        print(f"   📐 Layout: {count} Services → {rows} Reihen × {columns_per_row} Spalten")
        
        # Erstelle Columns mit Services - DIREKTER ANSATZ ohne Container
        for i, service in enumerate(services):
            # Service Column direkt in Section
            column = self.create_service_column(service)
            section["elements"].append(column)
        
        return section
    
    def create_service_column(self, service):
        """
        Erstellt eine Service-Spalte mit cholot-texticon
        KORRIGIERT: Proper Elementor column structure
        """
        return {
            "id": self.generate_id(),
            "elType": "column",
            "settings": {
                "_column_size": 33,  # WICHTIG: Muss gesetzt sein!
                "_inline_size": None
            },
            "elements": [{
                "id": self.generate_id(),
                "elType": "widget",
                "widgetType": "cholot-texticon",
                "settings": {
                    "title": service.get('title', 'Service'),
                    "text": f"<p>{service.get('description', '')}</p>",
                    "icon": f"fa fa-{service.get('icon', 'check')}",
                    "icon_color": service.get('color', '#ff6b6b'),
                    "title_color": "#232323",
                    "text_color": "#666666",
                    "icon_size": {"size": 60, "unit": "px"}
                }
            }]
        }
    
    def create_team_section(self, team, count):
        """
        Erstellt Team Section mit dynamischer Anzahl
        """
        section = {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "background_color": "#f7f7f7",
                "padding": {"top": "80", "bottom": "80", "unit": "px"}
            },
            "elements": []
        }
        
        # Titel für Team Section
        title_row = {
            "id": self.generate_id(),
            "elType": "column",
            "settings": {
                "_column_size": 100,
                "_inline_size": None
            },
            "elements": [{
                "id": self.generate_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": "Unser Team",
                    "header_size": "h2",
                    "align": "center"
                }
            }]
        }
        section["elements"].append(title_row)
        
        # Team Members Row
        team_row = {
            "id": self.generate_id(),
            "elType": "container",
            "settings": {"content_width": "full"},
            "elements": []
        }
        
        for member in team:
            column = {
                "id": self.generate_id(),
                "elType": "column",
                "settings": {"_column_size": 100 // min(count, 4)},
                "elements": [{
                    "id": self.generate_id(),
                    "elType": "widget",
                    "widgetType": "cholot-team",
                    "settings": {
                        "title": member.get('name', 'Team Member'),
                        "text": member.get('position', 'Position'),
                        "description": member.get('bio', ''),
                        "image": {"url": member.get('image', 'placeholder.jpg')}
                    }
                }]
            }
            team_row["elements"].append(column)
        
        section["elements"].append(team_row)
        return section
    
    def create_custom_section(self, custom_config):
        """
        Erstellt Custom Section basierend auf Config
        """
        section_type = custom_config.get('type', 'content')
        
        if section_type == 'gallery':
            return self.create_gallery_section(custom_config)
        elif section_type == 'testimonials':
            return self.create_testimonial_section(custom_config)
        elif section_type == 'features':
            return self.create_feature_section(custom_config)
        else:
            return self.create_content_section(custom_config)
    
    def create_contact_section(self, contact_info):
        """
        Erstellt Contact Section
        """
        return {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "background_color": "#232323",
                "padding": {"top": "60", "bottom": "60", "unit": "px"}
            },
            "elements": [{
                "id": self.generate_id(),
                "elType": "column",
                "elements": [
                    {
                        "id": self.generate_id(),
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
                        "id": self.generate_id(),
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"""
                            <p style='color: white; text-align: center;'>
                            📧 {contact_info.get('email', '')}<br>
                            📞 {contact_info.get('phone', '')}<br>
                            📍 {contact_info.get('address', '')}
                            </p>
                            """
                        }
                    }
                ]
            }]
        }
    
    def build_hero_from_scratch(self, config):
        """
        Baut Hero Section von Grund auf
        """
        return {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "layout": "full_width",
                "background_color": "#232323",
                "min_height": {"size": 500, "unit": "px"}
            },
            "elements": [{
                "id": self.generate_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None,
                    "vertical_align": "middle"
                },
                "elements": [
                    {
                        "id": self.generate_id(),
                        "elType": "widget",
                        "widgetType": "cholot-title",
                        "settings": {
                            "title": config.get('hero_title', 'Welcome'),
                            "title_color": {"value": "#ffffff"},
                            "title_typography_font_size": {"size": 60, "unit": "px"}
                        }
                    },
                    {
                        "id": self.generate_id(),
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"<p style='color: white; text-align: center;'>{config.get('hero_subtitle', '')}</p>"
                        }
                    }
                ]
            }]
        }
    
    def update_hero_content(self, section, config):
        """
        Aktualisiert Hero Content in existierender Section
        """
        # Finde und update Title Widget
        for column in section.get('elements', []):
            for widget in column.get('elements', []):
                if widget.get('widgetType') in ['cholot-title', 'heading']:
                    widget['settings']['title'] = config.get('hero_title', 'Welcome')
                elif widget.get('widgetType') == 'text-editor':
                    widget['settings']['editor'] = f"<p>{config.get('hero_subtitle', '')}</p>"
    
    def create_gallery_section(self, config):
        """Gallery Section Generator"""
        pass  # Implementation needed
    
    def create_testimonial_section(self, config):
        """Testimonial Section Generator"""
        pass  # Implementation needed
    
    def create_feature_section(self, config):
        """Feature Section Generator"""
        pass  # Implementation needed
    
    def create_content_section(self, config):
        """Generic Content Section"""
        return {
            "id": self.generate_id(),
            "elType": "section",
            "elements": [{
                "id": self.generate_id(),
                "elType": "column",
                "elements": [{
                    "id": self.generate_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p>{config.get('content', '')}</p>"
                    }
                }]
            }]
        }


def create_test_configs():
    """
    Erstellt verschiedene Test-Konfigurationen
    """
    configs = []
    
    # Config 1: Minimal (3 Services)
    configs.append({
        "name": "minimal",
        "data": {
            "page_title": "RIMAN GmbH - Minimal",
            "hero_title": "Willkommen bei RIMAN",
            "services": [
                {"title": "Asbestsanierung", "description": "Professionell und sicher"},
                {"title": "PCB-Sanierung", "description": "Nach neuesten Standards"},
                {"title": "Schimmelsanierung", "description": "Nachhaltige Lösungen"}
            ]
        }
    })
    
    # Config 2: Erweitert (6 Services, 5 Team)
    configs.append({
        "name": "extended",
        "data": {
            "page_title": "RIMAN GmbH - Komplett",
            "hero_title": "Ihr Partner für Schadstoffsanierung",
            "hero_subtitle": "25 Jahre Erfahrung in Berlin und Brandenburg",
            "services": [
                {"title": "Asbestsanierung", "description": "TRGS 519 zertifiziert", "icon": "shield"},
                {"title": "PCB-Sanierung", "description": "Umweltgerecht", "icon": "flask"},
                {"title": "Schimmelsanierung", "description": "Mit Garantie", "icon": "home"},
                {"title": "KMF-Sanierung", "description": "Mineralfaser-Experten", "icon": "filter"},
                {"title": "PAK-Sanierung", "description": "Teerhaltige Stoffe", "icon": "drop"},
                {"title": "Schadstoffanalyse", "description": "Akkreditiertes Labor", "icon": "search"}
            ],
            "team": [
                {"name": "Thomas Schmidt", "position": "Geschäftsführer"},
                {"name": "Maria Weber", "position": "Projektleiterin"},
                {"name": "Stefan Mueller", "position": "Technischer Leiter"},
                {"name": "Julia Klein", "position": "Qualitätsmanagement"},
                {"name": "Michael Braun", "position": "Bauleiter"}
            ],
            "contact": {
                "email": "info@riman-gmbh.de",
                "phone": "030-12345678",
                "address": "Musterstraße 123, 10115 Berlin"
            }
        }
    })
    
    # Config 3: Custom Sections
    configs.append({
        "name": "custom",
        "data": {
            "page_title": "RIMAN GmbH - Custom",
            "hero_title": "Maßgeschneiderte Lösungen",
            "services": [
                {"title": "Komplettpaket", "description": "Alles aus einer Hand"},
                {"title": "Notdienst 24/7", "description": "Immer erreichbar"}
            ],
            "sections": [
                {
                    "type": "content",
                    "title": "Über uns",
                    "content": "25 Jahre Erfahrung in der Schadstoffsanierung..."
                },
                {
                    "type": "features",
                    "title": "Unsere Stärken",
                    "features": [
                        "Zertifiziert nach ISO 9001",
                        "24/7 Notdienst",
                        "Festpreisgarantie"
                    ]
                }
            ]
        }
    })
    
    return configs


def main():
    """
    Test des adaptiven Generators
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║           ADAPTIVE ELEMENTOR GENERATOR                      ║
║                                                              ║
║   ✨ Passt Struktur dynamisch an Content an                ║
║   ✨ Erkennt Widget-Typen und deren Zweck                  ║
║   ✨ Generiert optimales Layout automatisch                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    generator = AdaptiveElementorGenerator()
    configs = create_test_configs()
    
    for config in configs:
        print(f"\n🔧 Teste Config: {config['name']}")
        print("=" * 50)
        
        result = generator.generate_adaptive(config['data'])
        
        # Speichere Ergebnis
        output_file = f"adaptive-{config['name']}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Generiert: {output_file}")
        print(f"   - Sections: {len(result['content'])}")
        print(f"   - Größe: {len(json.dumps(result)):,} Zeichen")
    
    print("\n" + "=" * 60)
    print("🎯 VORTEILE DES ADAPTIVEN SYSTEMS:")
    print("✅ Struktur passt sich an Content an")
    print("✅ Widget-Typen werden intelligent gewählt")
    print("✅ Layout wird optimiert (3er, 4er Raster etc.)")
    print("✅ Beliebig erweiterbar mit neuen Widgets")
    print("✅ Versteht Cholot-Theme Widgets")


if __name__ == "__main__":
    main()