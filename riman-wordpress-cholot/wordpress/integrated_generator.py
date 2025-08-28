#!/usr/bin/env python3
import json
from pathlib import Path
from template_based_generator import TemplateBasedFactory
import subprocess
import sys

class IntegratedWordPressGenerator:
    def __init__(self):
        self.factory = TemplateBasedFactory()
    
    def generate_company_page(self, company_data):
        sections = []
        
        hero_section = self.factory.create_section([
            [self.factory.create_title(f"{company_data['name']} - {company_data.get('tagline', 'Ihre Experten')}")]
        ], {
            'background_color': '#b68c2f',
            'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
        })
        sections.append(hero_section)
        
        if 'services' in company_data:
            service_widgets = []
            for service in company_data['services']:
                widget = self.factory.create_texticon(
                    service.get('title', 'Service'),
                    service.get('subtitle', ''),
                    service.get('description', ''),
                    service.get('icon', 'fas fa-check')
                )
                service_widgets.append([widget])
            
            services_section = self.factory.create_section(service_widgets, {
                'gap': 'extended',
                'structure': '30',
                'background_color': '#fafafa',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(services_section)
        
        if 'team' in company_data:
            team_widgets = []
            for member in company_data['team']:
                widget = self.factory.create_team_member(
                    member.get('name'),
                    member.get('position'),
                    member.get('image', 'placeholder.jpg'),
                    member.get('socials', [])
                )
                team_widgets.append([widget])
            
            team_section = self.factory.create_section(team_widgets, {
                'gap': 'extended',
                'background_color': '#ffffff',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(team_section)
        
        if 'about' in company_data:
            about_section = self.factory.create_section([
                [
                    self.factory.create_title(company_data['about'].get('title', 'Über uns')),
                    self.factory.create_text_editor(company_data['about'].get('content', ''))
                ]
            ], {
                'background_color': '#fafafa',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(about_section)
        
        footer_section = self.factory.create_section([
            [self.factory.create_text_editor(f"© 2024 {company_data['name']}. Alle Rechte vorbehalten.")]
        ], {
            'background_color': '#1f1f1f',
            'padding': {'unit': 'px', 'top': '30', 'bottom': '30'}
        })
        sections.append(footer_section)
        
        return self.factory.generate_page(sections)
    
    def save_and_convert(self, page_data, company_name):
        json_file = f"{company_name.replace(' ', '_').lower()}_page.json"
        self.factory.save_to_json(page_data, json_file)
        
        if Path('generate_wordpress_xml.py').exists():
            xml_file = json_file.replace('.json', '.xml')
            try:
                subprocess.run([
                    sys.executable, 'generate_wordpress_xml.py',
                    json_file, xml_file
                ], check=True)
                print(f"✅ WordPress XML generated: {xml_file}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ XML generation failed: {e}")
        else:
            print("ℹ️ generate_wordpress_xml.py not found, skipping XML generation")
        
        return json_file

def main():
    generator = IntegratedWordPressGenerator()
    
    riman_data = {
        'name': 'RIMAN GmbH',
        'tagline': 'Ihre Experten für professionelle Sanierung',
        'services': [
            {
                'title': 'Asbestsanierung',
                'subtitle': 'Sicher & Professionell',
                'description': 'Fachgerechte Entfernung und Entsorgung von Asbest nach allen gesetzlichen Vorgaben.',
                'icon': 'fas fa-shield-alt'
            },
            {
                'title': 'PCB-Sanierung',
                'subtitle': 'Umweltgerecht',
                'description': 'Sichere Beseitigung von PCB-belasteten Materialien mit zertifizierten Verfahren.',
                'icon': 'fas fa-biohazard'
            },
            {
                'title': 'Schimmelsanierung',
                'subtitle': 'Nachhaltig',
                'description': 'Dauerhafte Beseitigung von Schimmelbefall und präventive Maßnahmen.',
                'icon': 'fas fa-home'
            },
            {
                'title': 'Brandschadensanierung',
                'subtitle': '24/7 Notdienst',
                'description': 'Schnelle und professionelle Sanierung nach Brand- und Wasserschäden.',
                'icon': 'fas fa-fire-extinguisher'
            }
        ],
        'about': {
            'title': 'Über RIMAN GmbH',
            'content': 'Mit über 20 Jahren Erfahrung sind wir Ihr zuverlässiger Partner für alle Sanierungsarbeiten. Unsere zertifizierten Experten garantieren höchste Qualität und Sicherheit bei jedem Projekt.'
        },
        'team': [
            {
                'name': 'Michael Ritter',
                'position': 'Geschäftsführer',
                'image': 'team1.jpg',
                'socials': [
                    {'icon': 'fab fa-linkedin-in', 'link': 'https://linkedin.com'}
                ]
            },
            {
                'name': 'Sandra Mann',
                'position': 'Projektleiterin',
                'image': 'team2.jpg',
                'socials': [
                    {'icon': 'fab fa-linkedin-in', 'link': 'https://linkedin.com'}
                ]
            }
        ]
    }
    
    print("🚀 Integrated WordPress Generator")
    print("=" * 50)
    print(f"\n📋 Generating page for: {riman_data['name']}")
    
    page_data = generator.generate_company_page(riman_data)
    json_file = generator.save_and_convert(page_data, riman_data['name'])
    
    print(f"\n✅ Generation complete!")
    print(f"📄 JSON output: {json_file}")
    
    print("\n🎯 Key Features:")
    print("  ✓ Template-based widget generation")
    print("  ✓ Content injection with placeholders")
    print("  ✓ Preserves all styling from original")
    print("  ✓ Modular and extensible architecture")
    print("  ✓ Ready for WordPress XML export")

if __name__ == '__main__':
    main()