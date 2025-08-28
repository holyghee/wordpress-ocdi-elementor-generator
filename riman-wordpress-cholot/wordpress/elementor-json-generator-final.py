#!/usr/bin/env python3
"""
FINAL Elementor JSON Generator
Erzeugt aus simpler YAML eine vollständige Elementor JSON
wie elementor-1482-2025-08-27.json
"""

import json
import yaml
import copy
from pathlib import Path
import random
import string

class ElementorJSONGenerator:
    """
    Generiert komplette Elementor JSON aus einfachem Input
    """
    
    def __init__(self):
        # Lade Original Template als Basis
        self.load_template()
    
    def load_template(self):
        """Lädt die funktionierende Elementor JSON als Template"""
        template_path = Path("/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json")
        if template_path.exists():
            with open(template_path, 'r') as f:
                self.template = json.load(f)
            print("✅ Template geladen")
        else:
            print("⚠️ Template nicht gefunden, nutze Fallback")
            self.template = self.create_minimal_template()
    
    def create_minimal_template(self):
        """Minimale Elementor Struktur"""
        return {
            "content": [],
            "page_settings": [],
            "version": "0.4",
            "title": "Generated Page",
            "type": "page"
        }
    
    def generate_id(self):
        """Generiert Elementor-kompatible IDs"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    def generate_from_yaml(self, yaml_input):
        """
        Hauptfunktion: YAML → Elementor JSON
        """
        if isinstance(yaml_input, str):
            config = yaml.safe_load(yaml_input)
        else:
            config = yaml_input
        
        print("\n🔧 Generiere Elementor JSON...")
        
        # Deep copy des Templates
        result = copy.deepcopy(self.template)
        
        # Update Page Settings
        result['title'] = config.get('page_title', 'RIMAN GmbH')
        
        # Ersetze Content in der JSON
        self.replace_content(result, config)
        
        return result
    
    def replace_content(self, json_obj, config):
        """
        Ersetzt Content in der JSON-Struktur
        """
        company = config.get('company', {})
        
        # Text-Replacements
        replacements = {
            # Company Info
            "Cholot": company.get('name', 'RIMAN GmbH'),
            "Retirement Community": company.get('industry', 'Schadstoffsanierung'),
            "WordPress Theme": company.get('tagline', 'Professionelle Sanierung'),
            
            # Services
            "Healthly life": config.get('services', [{}])[0].get('title', 'Asbestsanierung'),
            "Improving life": config.get('services', [{}])[1].get('title', 'PCB-Sanierung') if len(config.get('services', [])) > 1 else 'PCB-Sanierung',
            "Relationship": config.get('services', [{}])[2].get('title', 'Schimmelsanierung') if len(config.get('services', [])) > 2 else 'Schimmelsanierung',
            
            # Team
            "Indah Levi": config.get('team', [{}])[0].get('name', 'Max Mustermann') if config.get('team') else 'Max Mustermann',
            "Director of Health": config.get('team', [{}])[0].get('position', 'Geschäftsführer') if config.get('team') else 'Geschäftsführer',
            
            # Contact
            "Contact form": "Kontaktformular",
            "Learn More": "Mehr erfahren",
            "View More": "Mehr anzeigen"
        }
        
        # Rekursive Ersetzung
        def replace_in_obj(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, str):
                        for old, new in replacements.items():
                            if old in value:
                                obj[key] = value.replace(old, new)
                    else:
                        replace_in_obj(value)
            elif isinstance(obj, list):
                for item in obj:
                    replace_in_obj(item)
        
        replace_in_obj(json_obj)
        
        # Update spezifische Widget-Settings
        self.update_widgets(json_obj, config)
    
    def update_widgets(self, json_obj, config):
        """
        Aktualisiert spezifische Widget-Inhalte
        """
        if 'content' not in json_obj:
            return
        
        for section in json_obj['content']:
            if 'elements' not in section:
                continue
            
            for column in section['elements']:
                if 'elements' not in column:
                    continue
                
                for widget in column['elements']:
                    # Update based on widget type
                    widget_type = widget.get('widgetType', '')
                    
                    if widget_type == 'cholot-texticon':
                        self.update_texticon_widget(widget, config)
                    elif widget_type == 'cholot-title':
                        self.update_title_widget(widget, config)
                    elif widget_type == 'cholot-team':
                        self.update_team_widget(widget, config)
    
    def update_texticon_widget(self, widget, config):
        """Update cholot-texticon widgets"""
        services = config.get('services', [])
        if services and 'settings' in widget:
            # Nutze Service-Daten wenn verfügbar
            service_index = 0  # Könnte dynamisch sein
            if service_index < len(services):
                service = services[service_index]
                if 'title' in service:
                    widget['settings']['title'] = service['title']
                if 'description' in service:
                    widget['settings']['text'] = f"<p>{service['description']}</p>"
    
    def update_title_widget(self, widget, config):
        """Update cholot-title widgets"""
        if 'settings' in widget:
            # Update main title
            if config.get('hero_title'):
                widget['settings']['title'] = config['hero_title']
    
    def update_team_widget(self, widget, config):
        """Update cholot-team widgets"""
        team = config.get('team', [])
        if team and 'settings' in widget:
            # Nutze Team-Daten
            if team:
                member = team[0]  # Erster Team-Member
                widget['settings']['title'] = member.get('name', 'Team Member')
                widget['settings']['text'] = member.get('position', 'Position')


def create_example_input():
    """
    Erstellt eine Beispiel-Input YAML
    """
    example = """# Elementor Page Configuration
page_title: "RIMAN GmbH - Startseite"

company:
  name: "RIMAN GmbH"
  industry: "Schadstoffsanierung"
  tagline: "Professionelle Sanierung seit 1998"

hero_title: "Professionelle Schadstoffsanierung in Berlin"

services:
  - title: "Asbestsanierung"
    description: "Sichere und zertifizierte Asbestentfernung nach TRGS 519"
    icon: "shield"
  
  - title: "PCB-Sanierung"
    description: "Fachgerechte PCB-Sanierung nach aktuellen Umweltstandards"
    icon: "flask"
  
  - title: "Schimmelsanierung"
    description: "Nachhaltige Schimmelbeseitigung und -prävention"
    icon: "home"

team:
  - name: "Thomas Schmidt"
    position: "Geschäftsführer"
  
  - name: "Maria Weber"
    position: "Projektleiterin"
  
  - name: "Stefan Mueller"
    position: "Technischer Leiter"

contact:
  email: "info@riman-gmbh.de"
  phone: "030-12345678"
  address: "Musterstraße 123, 10115 Berlin"
"""
    return example


def main():
    """
    Hauptfunktion zum Testen
    """
    print("🚀 ELEMENTOR JSON GENERATOR")
    print("=" * 50)
    
    # Beispiel-Input
    yaml_input = create_example_input()
    
    print("\n📝 Input YAML:")
    print(yaml_input[:300] + "...")
    
    # Generiere JSON
    generator = ElementorJSONGenerator()
    elementor_json = generator.generate_from_yaml(yaml_input)
    
    # Speichere Output - nur content array für Kompatibilität
    output_file = "riman-elementor-generated.json"
    with open(output_file, 'w') as f:
        # Nur den content array speichern, nicht das ganze Objekt
        if 'content' in elementor_json:
            json.dump(elementor_json['content'], f, indent=2)
        else:
            json.dump(elementor_json, f, indent=2)
    
    print(f"\n✅ Elementor JSON generiert!")
    print(f"📄 Datei: {output_file}")
    print(f"📊 Größe: {len(json.dumps(elementor_json)):,} Zeichen")
    
    # Jetzt kann diese JSON in WordPress XML eingebettet werden
    print("\n🎯 Nächster Schritt:")
    print("Diese JSON kann jetzt mit generate_wordpress_xml.py")
    print("in eine WordPress XML eingebettet werden!")
    
    # Erstelle auch direkt die YAML für den XML Generator
    xml_config = f"""site:
  title: "RIMAN GmbH Website"
  url: "https://riman-gmbh.de"

pages:
  - title: "Startseite"
    slug: "home"
    template: "elementor_header_footer"
    elementor_data_file: "{output_file}"
"""
    
    with open("riman-xml-config.yaml", 'w') as f:
        f.write(xml_config)
    
    print("\n📝 XML Config erstellt: riman-xml-config.yaml")
    print("\n✨ Komplett-Workflow:")
    print("1. ✅ YAML Input → Elementor JSON")
    print("2. → python generate_wordpress_xml.py -i riman-xml-config.yaml -o riman-complete.xml")
    print("3. → Import in WordPress")


if __name__ == "__main__":
    main()