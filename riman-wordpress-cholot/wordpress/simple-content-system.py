#!/usr/bin/env python3
"""
Simplified Content System - Just change the content, keep the design!
"""

import json
import re
from typing import Dict, List

class SimpleContentInjector:
    """
    Instead of generating complex Elementor JSON, we just replace content
    in existing, working templates.
    """
    
    def __init__(self, template_file: str):
        """Load a working Elementor template."""
        with open(template_file, 'r') as f:
            self.template = json.load(f)
    
    def replace_text_content(self, replacements: Dict[str, str]):
        """
        Simple text replacement throughout the template.
        
        Example:
        replacements = {
            "Cholot Retirement Community": "RIMAN GmbH",
            "senior living": "Schadstoffsanierung",
            "retirement": "Sanierung"
        }
        """
        template_str = json.dumps(self.template)
        
        for old_text, new_text in replacements.items():
            template_str = template_str.replace(old_text, new_text)
        
        self.template = json.loads(template_str)
        return self
    
    def replace_hero_section(self, title: str, subtitle: str, description: str, button_text: str = "Mehr erfahren"):
        """
        Replace just the CONTENT of the hero section, keep all styling.
        """
        # Find the slider widget (first major section usually)
        for section in self.template:
            for element in section.get('elements', []):
                for column in element.get('elements', []):
                    for widget in column.get('elements', []):
                        if 'slider_list' in widget.get('settings', {}):
                            # Found the slider!
                            widget['settings']['slider_list'][0].update({
                                'title': title,
                                'subtitle': subtitle,
                                'text': description,
                                'btn_text': button_text
                            })
                            return self
        return self
    
    def replace_service_boxes(self, services: List[Dict]):
        """
        Replace service box content.
        
        Example:
        services = [
            {"title": "Asbestsanierung", "subtitle": "Professionell", "text": "Sichere Entfernung..."},
            {"title": "PCB-Sanierung", "subtitle": "Fachgerecht", "text": "Kompetente Beratung..."},
        ]
        """
        # Find texticon widgets and replace content
        widget_index = 0
        for section in self.template:
            for element in section.get('elements', []):
                for column in element.get('elements', []):
                    for widget in column.get('elements', []):
                        if widget.get('widgetType') == 'cholot-texticon':
                            if widget_index < len(services):
                                service = services[widget_index]
                                widget['settings'].update({
                                    'title': service.get('title', ''),
                                    'subtitle': service.get('subtitle', ''),
                                    'text': f"<p>{service.get('text', '')}</p>"
                                })
                                widget_index += 1
        return self
    
    def save(self, output_file: str):
        """Save the modified template."""
        with open(output_file, 'w') as f:
            json.dump(self.template, f, separators=(',', ':'))
        return output_file


# SUPER SIMPLE YAML FORMAT
def create_simple_yaml_format():
    """
    This is what users would actually write - SUPER SIMPLE!
    """
    return """
# RIMAN Homepage - Simplified Content Definition
# No styling! Just content that gets injected into professional templates

use_template: "cholot-home"  # Use existing professional template

content:
  # Simple text replacements everywhere
  replace_globally:
    "Cholot Retirement Community": "RIMAN GmbH"
    "retirement": "Sanierung"
    "senior": "Schadstoff"
    
  hero:
    title: "RIMAN GmbH - Professionelle Schadstoffsanierung"
    subtitle: "Seit 1998 Ihr Partner"
    description: "Wir bieten umfassende Lösungen für Schadstoffsanierung"
    button: "Kostenloses Angebot"
    
  services:
    - title: "Asbestsanierung"
      subtitle: "Sicher & Professionell"
      text: "Fachgerechte Entfernung von Asbest"
      icon: "shield"  # Just the concept, template handles the rest
      
    - title: "PCB-Sanierung"
      subtitle: "Umweltgerecht"
      text: "Sichere Entsorgung von PCB-haltigen Materialien"
      icon: "recycle"
      
    - title: "Schimmelsanierung"
      subtitle: "Nachhaltig"
      text: "Dauerhafte Beseitigung von Schimmelbefall"
      icon: "home"
      
  testimonials:
    - name: "Max Mustermann"
      company: "Bauunternehmen XY"
      text: "Sehr professionelle Arbeit!"
      
    - name: "Erika Beispiel"
      company: "Hausverwaltung Z"
      text: "Kompetent und zuverlässig"
      
  team:
    - name: "Holger Müller"
      position: "Geschäftsführer"
      image: "team/mueller.jpg"  # Relative path, system handles the rest
      
  contact:
    email: "info@riman.de"
    phone: "+49 123 456789"
    address: "Musterstraße 1, 12345 Hamburg"
"""


# EVEN SIMPLER: AI PROMPT TO CONTENT
class AIContentGenerator:
    """
    Let AI handle it with a simple prompt!
    """
    
    def generate_from_prompt(self, prompt: str):
        """
        User just says:
        "Create a page for RIMAN GmbH, a company doing asbestos removal since 1998"
        
        AI fills the simple YAML format above.
        """
        # This would call GPT/Claude to generate the simple YAML
        pass


# THE ULTIMATE SIMPLE INTERFACE
def create_page_with_one_line():
    """
    The dream interface - one line to full page!
    """
    
    # User types:
    command = "Create sanierung page for RIMAN using modern-business template"
    
    # System:
    # 1. Picks template (modern-business)
    # 2. Understands domain (sanierung/renovation)
    # 3. Generates appropriate content
    # 4. Injects into template
    # 5. Done!
    
    return "riman-sanierung-page.xml"


if __name__ == "__main__":
    # Example: Super simple content replacement
    injector = SimpleContentInjector("templates/home-page.json")
    
    injector.replace_text_content({
        "Discover the best community": "Entdecken Sie professionelle Sanierung",
        "retirement": "Sanierung",
        "senior living": "Schadstoffbeseitigung"
    })
    
    injector.replace_hero_section(
        title="RIMAN GmbH - Ihre Experten für Schadstoffsanierung",
        subtitle="Seit 1998 für Sie da",
        description="Professionelle Lösungen für Asbest, PCB und Schimmelsanierung",
        button_text="Jetzt anfragen"
    )
    
    injector.save("riman-homepage-simple.json")
    
    print("✅ Created RIMAN page by just changing content!")
    print("   All complex styling preserved from template!")