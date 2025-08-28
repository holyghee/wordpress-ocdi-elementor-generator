#!/usr/bin/env python3
"""
Full Page Generator - Preserves ALL styling from original template
"""

import json
from copy import deepcopy
from pathlib import Path

def generate_riman_full_page():
    """Generate RIMAN page using the complete original template"""
    
    # Load original template
    with open('original-template.json', 'r') as f:
        template = json.load(f)
    
    # Deep copy to preserve original
    page_data = deepcopy(template['content'])
    
    # Modify content while preserving ALL styling
    for section_idx, section in enumerate(page_data):
        
        # Hero Slider - First section
        if section_idx == 0:
            for col in section.get('elements', []):
                for widget in col.get('elements', []):
                    if widget.get('widgetType') == 'rdn-slider':
                        # Update slider content
                        widget['settings']['slider_list'] = [
                            {
                                **widget['settings']['slider_list'][0],  # Keep ALL original settings
                                "title": "RIMAN GmbH - Ihre <span>Experten</span> für professionelle Sanierung",
                                "subtitle": "Seit über 20 Jahren",
                                "text": "Zertifizierte Asbest-, PCB- und Schimmelsanierung nach höchsten Sicherheitsstandards. Wir sind Ihr zuverlässiger Partner.",
                                "btn_text": "Kostenlose Beratung",
                                "image": {
                                    "url": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?ixlib=rb-4.0.3&w=1920&q=80",
                                    "id": 9001,
                                    "alt": "RIMAN Sanierung Team",
                                    "source": "library"
                                }
                            },
                            {
                                **widget['settings']['slider_list'][0],  # Keep ALL original settings
                                "title": "Asbestsanierung nach <span>TRGS 519</span>",
                                "subtitle": "Zertifiziert & Sicher",
                                "text": "Professionelle Asbestentfernung mit modernster Ausrüstung. Geschultes Personal und umweltgerechte Entsorgung garantiert.",
                                "btn_text": "Mehr erfahren",
                                "image": {
                                    "url": "https://images.unsplash.com/photo-1581094271901-8022df4466f9?ixlib=rb-4.0.3&w=1920&q=80",
                                    "id": 9002,
                                    "alt": "Asbestsanierung",
                                    "source": "library"
                                }
                            }
                        ]
        
        # Service Cards - Second section
        elif section_idx == 1:
            service_data = [
                {
                    "title": "Asbestsanierung",
                    "subtitle": "TRGS 519 Zertifiziert",
                    "text": "Sichere und fachgerechte Asbestentfernung mit modernster Technik.",
                    "icon": "fas fa-shield-alt",
                    "image": "https://images.unsplash.com/photo-1581094794329-c8112a50cc0d7?w=600&q=80"
                },
                {
                    "title": "PCB-Sanierung",
                    "subtitle": "Umweltgerecht",
                    "text": "Professionelle Entsorgung PCB-belasteter Materialien.",
                    "icon": "fas fa-biohazard",
                    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80"
                },
                {
                    "title": "Schimmelsanierung",
                    "subtitle": "Nachhaltig",
                    "text": "Dauerhafte Schimmelbeseitigung mit Ursachenanalyse.",
                    "icon": "fas fa-home",
                    "image": "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=600&q=80"
                }
            ]
            
            for col_idx, col in enumerate(section.get('elements', [])):
                if col_idx < len(service_data):
                    service = service_data[col_idx]
                    
                    # Update image in nested section
                    for subsection in col.get('elements', []):
                        if subsection.get('elType') == 'section':
                            for subcol in subsection.get('elements', []):
                                for widget in subcol.get('elements', []):
                                    if widget.get('widgetType') == 'image':
                                        widget['settings']['image']['url'] = service['image']
                                    elif widget.get('widgetType') == 'cholot-texticon':
                                        widget['settings']['title'] = service['title']
                                        widget['settings']['subtitle'] = service['subtitle']
                                        widget['settings']['text'] = f"<p>{service['text']}</p>"
                                        widget['settings']['selected_icon']['value'] = service['icon']
        
        # About Section - Third section
        elif section_idx == 2:
            for col in section.get('elements', []):
                for widget in col.get('elements', []):
                    if widget.get('widgetType') == 'cholot-title':
                        widget['settings']['title'] = "RIMAN GmbH - Über <span>uns</span><br>Ihre Sanierungsexperten"
                    elif widget.get('widgetType') == 'text-editor' and 'Building with' in widget['settings'].get('editor', ''):
                        widget['settings']['editor'] = "<p>Seit über 20 Jahren sind wir Ihr zuverlässiger Partner für professionelle Sanierungsarbeiten. Mit einem Team aus zertifizierten Experten garantieren wir höchste Qualität und Sicherheit bei jedem Projekt.</p>"
        
        # Team Section - Fourth section  
        elif section_idx == 3:
            team_data = [
                {
                    "name": "Michael Ritter",
                    "position": "Geschäftsführer",
                    "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=600&q=80"
                },
                {
                    "name": "Sandra Mann",
                    "position": "Projektleiterin",
                    "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&q=80"
                },
                {
                    "name": "Thomas Weber",
                    "position": "Technischer Leiter",
                    "image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=600&q=80"
                }
            ]
            
            for col_idx, col in enumerate(section.get('elements', [])):
                if col_idx < len(team_data):
                    member = team_data[col_idx]
                    for widget in col.get('elements', []):
                        if widget.get('widgetType') == 'cholot-team':
                            widget['settings']['title'] = member['name']
                            widget['settings']['text'] = member['position']
                            widget['settings']['image']['url'] = member['image']
        
        # Testimonial Section - Fifth section
        elif section_idx == 4:
            for col in section.get('elements', []):
                for subsection in col.get('elements', []):
                    if isinstance(subsection, dict) and subsection.get('elType') == 'section':
                        for subcol in subsection.get('elements', []):
                            for widget in subcol.get('elements', []):
                                if widget.get('widgetType') == 'cholot-testimonial-two':
                                    widget['settings']['testi_list'] = [
                                        {
                                            **widget['settings']['testi_list'][0],
                                            "title": "Klaus Hoffmann",
                                            "position": "Hausverwaltung Berlin",
                                            "text": "RIMAN GmbH hat unsere Asbestsanierung absolut professionell durchgeführt. Sehr empfehlenswert!",
                                            "image": {"url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&q=80", "id": 5001}
                                        },
                                        {
                                            **widget['settings']['testi_list'][0],
                                            "title": "Andrea Meyer",
                                            "position": "Meyer Immobilien GmbH",
                                            "text": "Schnelle und saubere Arbeit bei der Schimmelsanierung. Das Team war sehr kompetent.",
                                            "image": {"url": "https://images.unsplash.com/photo-1594744803329-e58b31de8bf5?w=200&q=80", "id": 5002}
                                        },
                                        {
                                            **widget['settings']['testi_list'][0],
                                            "title": "Peter Schmidt",
                                            "position": "Architekturbüro Schmidt",
                                            "text": "Zuverlässiger Partner für alle Sanierungsarbeiten. Klare Empfehlung!",
                                            "image": {"url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&q=80", "id": 5003}
                                        }
                                    ]
        
        # Contact Section - Last section
        elif section_idx == len(page_data) - 1:
            for col in section.get('elements', []):
                for widget in col.get('elements', []):
                    if widget.get('widgetType') == 'cholot-title':
                        widget['settings']['title'] = "Kontaktieren Sie uns für eine <br>kostenlose <span>Beratung</span>"
                    elif widget.get('widgetType') == 'text-editor' and 'Donec quam' in widget['settings'].get('editor', ''):
                        widget['settings']['editor'] = "<p>24/7 Notfallservice verfügbar. Rufen Sie uns an: +49 (0) 30 123456789 oder nutzen Sie unser Kontaktformular.</p>"
    
    # Create complete page structure
    complete_page = {
        "content": page_data,
        "page_settings": template.get('page_settings', []),
        "version": template.get('version', '0.4'),
        "title": "RIMAN GmbH - Professionelle Sanierung",
        "type": "page"
    }
    
    # Save Elementor JSON
    with open('riman_complete_elementor.json', 'w', encoding='utf-8') as f:
        json.dump(complete_page, f, indent=2, ensure_ascii=False)
    
    # Create WordPress format
    wordpress_format = {
        "site": {
            "title": "RIMAN GmbH",
            "url": "https://riman-sanierung.de",
            "description": "Professionelle Sanierungsdienstleistungen"
        },
        "posts": [{
            "title": "RIMAN GmbH - Startseite",
            "slug": "startseite",
            "type": "page",
            "status": "publish",
            "template": "elementor_canvas",
            "meta": {
                "_elementor_edit_mode": "builder",
                "_elementor_template_type": "wp-page",
                "_elementor_version": "3.14.1",
                "_elementor_data": json.dumps(page_data, ensure_ascii=False)
            }
        }]
    }
    
    # Save WordPress format
    with open('riman_complete_wordpress.json', 'w', encoding='utf-8') as f:
        json.dump(wordpress_format, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated complete RIMAN page")
    print(f"📦 Elementor JSON size: {len(json.dumps(page_data))} chars")
    print(f"📊 Sections: {len(page_data)}")
    
    # Count widgets
    widget_count = 0
    for section in page_data:
        for col in section.get('elements', []):
            for elem in col.get('elements', []):
                if elem.get('widgetType'):
                    widget_count += 1
                elif elem.get('elType') == 'section':
                    for subcol in elem.get('elements', []):
                        for widget in subcol.get('elements', []):
                            if widget.get('widgetType'):
                                widget_count += 1
    
    print(f"🎨 Total widgets: {widget_count}")
    print(f"✅ Files created:")
    print(f"  - riman_complete_elementor.json (Elementor format)")
    print(f"  - riman_complete_wordpress.json (WordPress import format)")

if __name__ == '__main__':
    generate_riman_full_page()