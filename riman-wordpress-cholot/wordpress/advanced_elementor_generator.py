#!/usr/bin/env python3
"""
Advanced Elementor Generator with Full Styling Support
Generates complex Elementor pages with complete styling, animations, and responsiveness
"""

import json
import uuid
from pathlib import Path
from copy import deepcopy
from typing import Dict, List, Any, Optional

class AdvancedElementorGenerator:
    def __init__(self):
        self.load_template_from_file()
        
    def load_template_from_file(self):
        """Load the complex template from file"""
        template_path = Path('/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json')
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template_data = json.load(f)
                self.sections = self.template_data.get('content', [])
        else:
            # Fallback to loading from local if available
            local_path = Path('elementor-content-only.json')
            if local_path.exists():
                with open(local_path, 'r', encoding='utf-8') as f:
                    self.sections = json.load(f)
            else:
                self.sections = []
    
    def generate_id(self) -> str:
        """Generate unique Elementor-style ID"""
        return ''.join(format(ord(c), 'x')[:2] for c in str(uuid.uuid4())[:8])
    
    def create_hero_slider(self, slides: List[Dict[str, str]]) -> dict:
        """Create a hero slider section with custom slides"""
        # Find the slider template
        slider_template = None
        for section in self.sections:
            for col in section.get('elements', []):
                for widget in col.get('elements', []):
                    if widget.get('widgetType') == 'rdn-slider':
                        slider_template = deepcopy(section)
                        break
        
        if not slider_template:
            return self.create_basic_section([])
        
        # Update slider content
        for col in slider_template['elements']:
            for widget in col['elements']:
                if widget.get('widgetType') == 'rdn-slider':
                    new_slides = []
                    for slide in slides:
                        new_slide = {
                            "title": slide.get('title', ''),
                            "subtitle": slide.get('subtitle', ''),
                            "text": slide.get('text', ''),
                            "_id": self.generate_id()[:7],
                            "btn_text": slide.get('button_text', 'Mehr erfahren'),
                            "btn_link": {"url": slide.get('link', '#')},
                            "image": {
                                "url": slide.get('image', 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1200'),
                                "id": self.generate_id()[:4],
                                "alt": slide.get('alt', ''),
                                "source": "library",
                                "size": ""
                            }
                        }
                        new_slides.append(new_slide)
                    
                    widget['settings']['slider_list'] = new_slides
        
        slider_template['id'] = self.generate_id()
        return slider_template
    
    def create_service_cards(self, services: List[Dict[str, str]]) -> dict:
        """Create service cards section with images and text"""
        # Find the service cards template (the one with 3 columns)
        cards_template = None
        for section in self.sections:
            if len(section.get('elements', [])) == 3:  # 3-column section
                # Check if it has texticon widgets
                has_texticon = False
                for col in section['elements']:
                    for widget in col.get('elements', []):
                        if widget.get('widgetType') == 'cholot-texticon':
                            has_texticon = True
                            break
                if has_texticon:
                    cards_template = deepcopy(section)
                    break
        
        if not cards_template:
            return self.create_basic_section([])
        
        # Clear existing columns and add new ones
        cards_template['elements'] = []
        
        for service in services[:3]:  # Max 3 services per row
            column = {
                "id": self.generate_id(),
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None,
                    "background_background": "classic",
                    "background_color": "#fafafa",
                    "border_width": {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "10"},
                    "border_color": "#ededed",
                    "box_shadow_box_shadow": {"horizontal": 0, "vertical": 4, "blur": 5, "spread": 0, "color": "rgba(196,196,196,0.26)"},
                    "margin": {"unit": "px", "top": "15", "right": "15", "bottom": "15", "left": "15"},
                    "animation": "fadeInUp",
                    "animation_duration": "fast"
                },
                "elements": []
            }
            
            # Add image section
            if service.get('image'):
                image_section = {
                    "id": self.generate_id(),
                    "settings": {"gap": "no", "shape_divider_bottom": "curve", "shape_divider_bottom_color": "#fafafa"},
                    "elements": [{
                        "id": self.generate_id(),
                        "settings": {"_column_size": 100},
                        "elements": [{
                            "id": self.generate_id(),
                            "settings": {
                                "image": {"url": service['image'], "id": self.generate_id()[:4]},
                                "opacity": {"unit": "px", "size": 1}
                            },
                            "widgetType": "image",
                            "elType": "widget"
                        }]
                    }],
                    "isInner": True,
                    "elType": "section"
                }
                column['elements'].append(image_section)
            
            # Add text content
            text_section = {
                "id": self.generate_id(),
                "settings": {"gap": "no", "content_position": "middle", "margin": {"unit": "px", "top": "-30"}},
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {"_column_size": 100},
                    "elements": [{
                        "id": self.generate_id(),
                        "settings": {
                            "title": service.get('title', ''),
                            "subtitle": service.get('subtitle', ''),
                            "text": f"<p>{service.get('text', '')}</p>",
                            "selected_icon": {"value": service.get('icon', 'fas fa-check'), "library": "fa-solid"},
                            "icon_color": "#ffffff",
                            "iconbg_color": "#b68c2f",
                            "icon_size": {"unit": "px", "size": 20},
                            "icon_bg_size": {"unit": "px", "size": 72},
                            "title_typography_font_size": {"unit": "px", "size": 28},
                            "subtitle_color": "#b68c2f",
                            "_padding": {"unit": "px", "top": "30", "right": "30", "bottom": "30", "left": "30"},
                            "_border_width": {"unit": "px", "top": "0", "right": "1", "bottom": "1", "left": "1"},
                            "_border_color": "#b68c2f",
                            "_border_border": "dashed"
                        },
                        "widgetType": "cholot-texticon",
                        "elType": "widget"
                    }]
                }],
                "isInner": True,
                "elType": "section"
            }
            column['elements'].append(text_section)
            
            cards_template['elements'].append(column)
        
        cards_template['id'] = self.generate_id()
        return cards_template
    
    def create_team_section(self, team_members: List[Dict[str, str]]) -> dict:
        """Create team section with member cards"""
        # Find team template
        team_template = None
        for section in self.sections:
            for col in section.get('elements', []):
                for widget in col.get('elements', []):
                    if widget.get('widgetType') == 'cholot-team':
                        team_template = deepcopy(section)
                        break
        
        if not team_template:
            return self.create_basic_section([])
        
        # Clear and rebuild with new team members
        team_template['elements'] = []
        
        for member in team_members[:3]:
            column = {
                "id": self.generate_id(),
                "settings": {"_column_size": 33, "animation": "fadeInUp"},
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {
                        "title": member.get('name', ''),
                        "text": member.get('position', ''),
                        "image": {
                            "url": member.get('image', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400'),
                            "id": self.generate_id()[:4]
                        },
                        "social_icon_list": member.get('socials', [
                            {"social_icon": {"value": "fab fa-linkedin-in"}, "link": {"url": "#"}},
                            {"social_icon": {"value": "fab fa-twitter"}, "link": {"url": "#"}}
                        ]),
                        "team_height": {"unit": "px", "size": 420},
                        "port_border_color": "#b68c2f",
                        "bg_icon_color": "#b68c2f",
                        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 8, "blur": 14, "spread": 4}
                    },
                    "widgetType": "cholot-team",
                    "elType": "widget"
                }]
            }
            team_template['elements'].append(column)
        
        team_template['id'] = self.generate_id()
        return team_template
    
    def create_testimonial_section(self, testimonials: List[Dict[str, str]]) -> dict:
        """Create testimonial carousel section"""
        # Find testimonial template
        test_template = None
        for section in self.sections:
            for col in section.get('elements', []):
                for subsec in col.get('elements', []):
                    if isinstance(subsec, dict) and 'elements' in subsec:
                        for subcol in subsec.get('elements', []):
                            for widget in subcol.get('elements', []):
                                if widget.get('widgetType') == 'cholot-testimonial-two':
                                    test_template = deepcopy(section)
                                    break
        
        if not test_template:
            return self.create_basic_section([])
        
        # Update testimonials
        for col in test_template.get('elements', []):
            for subsec in col.get('elements', []):
                if isinstance(subsec, dict) and 'elements' in subsec:
                    for subcol in subsec.get('elements', []):
                        for widget in subcol.get('elements', []):
                            if widget.get('widgetType') == 'cholot-testimonial-two':
                                new_testimonials = []
                                for test in testimonials:
                                    new_test = {
                                        "title": test.get('name', ''),
                                        "position": test.get('position', 'Kunde'),
                                        "text": test.get('text', ''),
                                        "_id": self.generate_id()[:7],
                                        "image": {
                                            "url": test.get('image', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200'),
                                            "id": self.generate_id()[:4]
                                        }
                                    }
                                    new_testimonials.append(new_test)
                                widget['settings']['testi_list'] = new_testimonials
        
        test_template['id'] = self.generate_id()
        return test_template
    
    def create_contact_section(self, contact_info: Dict[str, str]) -> dict:
        """Create contact section with form"""
        # Find contact template
        contact_template = None
        for section in self.sections:
            for col in section.get('elements', []):
                for widget in col.get('elements', []):
                    if widget.get('widgetType') == 'cholot-contact':
                        contact_template = deepcopy(section)
                        break
        
        if not contact_template:
            # Create basic contact section
            return {
                "id": self.generate_id(),
                "settings": {
                    "gap": "extended",
                    "background_color": "#1f1f1f",
                    "padding": {"unit": "px", "top": "60", "bottom": "60"}
                },
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {"_column_size": 50},
                    "elements": [
                        self.create_title_widget(contact_info.get('title', 'Kontaktieren Sie uns')),
                        self.create_text_widget(contact_info.get('text', ''))
                    ]
                }, {
                    "id": self.generate_id(),
                    "settings": {"_column_size": 50},
                    "elements": [{
                        "id": self.generate_id(),
                        "settings": {"shortcode": contact_info.get('form', '[contact-form-7 id="1"]')},
                        "widgetType": "cholot-contact",
                        "elType": "widget"
                    }]
                }],
                "elType": "section"
            }
        
        # Update contact info
        for col in contact_template['elements']:
            for widget in col.get('elements', []):
                if widget.get('widgetType') == 'cholot-title':
                    widget['settings']['title'] = contact_info.get('title', 'Kontakt')
                elif widget.get('widgetType') == 'text-editor':
                    widget['settings']['editor'] = f"<p>{contact_info.get('text', '')}</p>"
        
        contact_template['id'] = self.generate_id()
        return contact_template
    
    def create_title_widget(self, title: str) -> dict:
        """Create a title widget"""
        return {
            "id": self.generate_id(),
            "settings": {
                "title": title,
                "desc_typography_font_size": {"unit": "px", "size": 35},
                "desc_typography_font_weight": "700",
                "desc_typography_font_family": "Playfair Display",
                "title_color": "#ffffff"
            },
            "widgetType": "cholot-title",
            "elType": "widget"
        }
    
    def create_text_widget(self, text: str) -> dict:
        """Create a text editor widget"""
        return {
            "id": self.generate_id(),
            "settings": {
                "editor": f"<p>{text}</p>",
                "text_color": "rgba(255,255,255,0.8)"
            },
            "widgetType": "text-editor",
            "elType": "widget"
        }
    
    def create_basic_section(self, widgets: List[dict]) -> dict:
        """Create a basic section with widgets"""
        return {
            "id": self.generate_id(),
            "settings": {
                "gap": "extended",
                "padding": {"unit": "px", "top": "60", "bottom": "60"}
            },
            "elements": [{
                "id": self.generate_id(),
                "settings": {"_column_size": 100},
                "elements": widgets
            }],
            "elType": "section"
        }
    
    def generate_complete_page(self, company_data: Dict[str, Any]) -> dict:
        """Generate a complete Elementor page with all sections"""
        sections = []
        
        # Hero Slider
        if company_data.get('hero_slides'):
            sections.append(self.create_hero_slider(company_data['hero_slides']))
        
        # Service Cards
        if company_data.get('services'):
            sections.append(self.create_service_cards(company_data['services']))
        
        # About Section
        if company_data.get('about'):
            about = company_data['about']
            sections.append(self.create_basic_section([
                self.create_title_widget(about.get('title', '')),
                self.create_text_widget(about.get('text', ''))
            ]))
        
        # Team Section
        if company_data.get('team'):
            sections.append(self.create_team_section(company_data['team']))
        
        # Testimonials
        if company_data.get('testimonials'):
            sections.append(self.create_testimonial_section(company_data['testimonials']))
        
        # Contact
        if company_data.get('contact'):
            sections.append(self.create_contact_section(company_data['contact']))
        
        return {
            "content": sections,
            "page_settings": [],
            "version": "0.4",
            "title": company_data.get('name', 'Company') + " - Generated Page",
            "type": "page"
        }

def demo_riman_complete():
    """Generate a complete RIMAN GmbH page with all features"""
    
    generator = AdvancedElementorGenerator()
    
    riman_data = {
        'name': 'RIMAN GmbH',
        'hero_slides': [
            {
                'title': 'RIMAN GmbH - <span>Professionelle</span> Sanierung',
                'subtitle': 'Seit über 20 Jahren',
                'text': 'Ihr zuverlässiger Partner für Asbest-, PCB- und Schimmelsanierung. Wir arbeiten nach höchsten Sicherheitsstandards.',
                'button_text': 'Kontakt aufnehmen',
                'link': '#contact',
                'image': 'https://images.unsplash.com/photo-1581094794329-c8112c50c0d7?w=1200'
            },
            {
                'title': 'Zertifizierte <span>Asbestsanierung</span>',
                'subtitle': 'Nach TRGS 519',
                'text': 'Sichere und fachgerechte Entfernung von Asbest mit modernster Ausrüstung und geschultem Personal.',
                'button_text': 'Mehr erfahren',
                'link': '#services',
                'image': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=1200'
            }
        ],
        'services': [
            {
                'title': 'Asbestsanierung',
                'subtitle': 'TRGS 519 zertifiziert',
                'text': 'Professionelle Asbestentfernung mit höchsten Sicherheitsstandards und umweltgerechter Entsorgung.',
                'icon': 'fas fa-shield-alt',
                'image': 'https://images.unsplash.com/photo-1581094271901-8022df4466f9?w=600'
            },
            {
                'title': 'PCB-Sanierung',
                'subtitle': 'Umweltgerecht',
                'text': 'Sichere Beseitigung PCB-belasteter Materialien nach aktuellen Vorschriften und Richtlinien.',
                'icon': 'fas fa-biohazard',
                'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600'
            },
            {
                'title': 'Schimmelsanierung',
                'subtitle': 'Nachhaltig & Effektiv',
                'text': 'Dauerhafte Schimmelbeseitigung mit Ursachenanalyse und präventiven Maßnahmen.',
                'icon': 'fas fa-home',
                'image': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=600'
            }
        ],
        'about': {
            'title': 'Über RIMAN GmbH',
            'text': 'Mit über 20 Jahren Erfahrung sind wir Ihr kompetenter Partner für alle Sanierungsarbeiten. Unsere zertifizierten Mitarbeiter garantieren höchste Qualität und Sicherheit.'
        },
        'team': [
            {
                'name': 'Michael Ritter',
                'position': 'Geschäftsführer',
                'image': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400',
                'socials': [
                    {"social_icon": {"value": "fab fa-linkedin-in"}, "link": {"url": "https://linkedin.com"}},
                    {"social_icon": {"value": "fab fa-xing"}, "link": {"url": "https://xing.com"}}
                ]
            },
            {
                'name': 'Sandra Mann',
                'position': 'Projektleiterin',
                'image': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400',
                'socials': [
                    {"social_icon": {"value": "fab fa-linkedin-in"}, "link": {"url": "https://linkedin.com"}}
                ]
            },
            {
                'name': 'Thomas Weber',
                'position': 'Technischer Leiter',
                'image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400',
                'socials': [
                    {"social_icon": {"value": "fab fa-linkedin-in"}, "link": {"url": "https://linkedin.com"}}
                ]
            }
        ],
        'testimonials': [
            {
                'name': 'Hans Müller',
                'position': 'Hausverwaltung München',
                'text': 'RIMAN GmbH hat die Asbestsanierung in unserem Gebäude professionell und termingerecht durchgeführt. Sehr zu empfehlen!',
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200'
            },
            {
                'name': 'Maria Schmidt',
                'position': 'Immobilien Schmidt GmbH',
                'text': 'Kompetente Beratung und saubere Ausführung. Die Schimmelsanierung wurde perfekt umgesetzt.',
                'image': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200'
            },
            {
                'name': 'Peter Wagner',
                'position': 'Bauunternehmen Wagner',
                'text': 'Zuverlässiger Partner für alle Sanierungsarbeiten. Die Zusammenarbeit klappt seit Jahren hervorragend.',
                'image': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200'
            }
        ],
        'contact': {
            'title': 'Kontaktieren Sie uns für ein <span>unverbindliches</span> Angebot',
            'text': 'Wir beraten Sie gerne zu allen Fragen rund um Sanierungsarbeiten. Rufen Sie uns an oder nutzen Sie unser Kontaktformular.',
            'form': '[contact-form-7 id="5" title="Kontaktformular"]'
        }
    }
    
    page_data = generator.generate_complete_page(riman_data)
    
    # Save the generated page
    output_file = 'riman_complete_page.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(page_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Complete RIMAN page generated: {output_file}")
    print(f"📦 Sections: {len(page_data['content'])}")
    print(f"🎨 With full styling, animations, and responsive settings")
    
    return page_data

if __name__ == '__main__':
    print("🚀 Advanced Elementor Generator")
    print("=" * 50)
    demo_riman_complete()