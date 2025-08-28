#!/usr/bin/env python3
"""
Simple RIMAN Content Generator - OHNE KI!
Nutzt die Templates und ersetzt nur die Texte
"""

import json
import copy
from pathlib import Path

def generate_riman_content():
    """
    Generiert RIMAN GmbH Content ohne KI
    """
    
    # Lade das vorhandene Template
    with open('elementor-content-only.json', 'r') as f:
        template = json.load(f)
    
    # Deep copy um Original zu behalten
    riman_page = copy.deepcopy(template)
    
    # EINFACHE TEXT-ERSETZUNGEN (keine KI nötig!)
    replacements = {
        # Hero Section
        "Cholot": "RIMAN GmbH",
        "Retirement Community": "Schadstoffsanierung",
        "WordPress Theme": "Professionelle Sanierung",
        "Welcome to": "Willkommen bei",
        "Learn More": "Mehr erfahren",
        "Contact Us": "Kontakt aufnehmen",
        
        # Services
        "Service 1": "Asbestsanierung",
        "Service 2": "PCB-Sanierung", 
        "Service 3": "Schimmelsanierung",
        "Service 4": "PAK-Sanierung",
        "Service 5": "KMF-Sanierung",
        "Service 6": "Bleisanierung",
        
        # About
        "About Us": "Über uns",
        "Our Story": "Unsere Geschichte",
        "Lorem ipsum": "Seit 1998 sind wir Ihr zuverlässiger Partner für professionelle Schadstoffsanierung",
        
        # Contact
        "Get in Touch": "Kontaktieren Sie uns",
        "123-456-7890": "030-12345678",
        "info@example.com": "info@riman-gmbh.de",
        "123 Main St": "Musterstraße 123, 10115 Berlin"
    }
    
    # Ersetze im gesamten JSON
    json_str = json.dumps(riman_page)
    
    for old_text, new_text in replacements.items():
        json_str = json_str.replace(old_text, new_text)
    
    riman_page = json.loads(json_str)
    
    # Speichere das Ergebnis
    with open('riman-homepage.json', 'w') as f:
        json.dump(riman_page, f, indent=2)
    
    print("✅ RIMAN Homepage generiert!")
    print("📄 Datei: riman-homepage.json")
    print("🚀 Bereit für WordPress Import!")
    
    # Erstelle auch die YAML für generate_wordpress_xml.py
    yaml_content = """site:
  title: "RIMAN GmbH - Professionelle Schadstoffsanierung"
  url: "https://riman-gmbh.de"

pages:
  - title: "Startseite"
    slug: "home"
    template: "elementor_header_footer"
    elementor_data_file: "riman-homepage.json"
"""
    
    with open('riman-config.yaml', 'w') as f:
        f.write(yaml_content)
    
    print("\n📝 Config erstellt: riman-config.yaml")
    print("\nNächster Schritt:")
    print("python generate_wordpress_xml.py -i riman-config.yaml -o riman-final.xml")

if __name__ == "__main__":
    generate_riman_content()