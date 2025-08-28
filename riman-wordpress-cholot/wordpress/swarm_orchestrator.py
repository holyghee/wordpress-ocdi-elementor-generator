#!/usr/bin/env python3
"""
SWARM Orchestrator for Elementor Template-Based Generation
Optimized workflow for generating WordPress pages using extracted templates
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
from template_based_generator import TemplateBasedFactory

class SwarmOrchestrator:
    def __init__(self):
        self.factory = TemplateBasedFactory()
        self.results = {
            'templates_loaded': len(self.factory.templates),
            'pages_generated': 0,
            'xml_files_created': []
        }
    
    def generate_company_pages(self, companies: List[Dict[str, Any]]):
        """Generate pages for multiple companies in parallel-like fashion"""
        
        for company in companies:
            print(f"\n🏢 Processing: {company['name']}")
            print("-" * 40)
            
            # Generate Elementor JSON
            page_data = self._create_page_structure(company)
            json_file = self._save_elementor_json(page_data, company['name'])
            
            # Format for WordPress
            formatted_file = self._format_for_wordpress(json_file, company['name'])
            
            # Generate XML
            xml_file = self._generate_xml(formatted_file)
            
            if xml_file:
                self.results['pages_generated'] += 1
                self.results['xml_files_created'].append(xml_file)
                print(f"  ✅ Complete: {xml_file}")
    
    def _create_page_structure(self, company: Dict[str, Any]) -> List[dict]:
        """Create complete page structure from company data"""
        sections = []
        
        # Hero Section
        hero = self.factory.create_section([
            [self.factory.create_title(f"{company['name']} - {company.get('tagline', '')}")]
        ], {
            'background_color': company.get('brand_color', '#b68c2f'),
            'padding': {'unit': 'px', 'top': '80', 'bottom': '80'}
        })
        sections.append(hero)
        
        # Services Section
        if 'services' in company:
            service_columns = []
            for service in company['services']:
                widget = self.factory.create_texticon(
                    service['title'],
                    service.get('subtitle', ''),
                    service['description'],
                    service.get('icon', 'fas fa-check-circle')
                )
                service_columns.append([widget])
            
            services_section = self.factory.create_section(service_columns, {
                'gap': 'extended',
                'background_color': '#fafafa',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(services_section)
        
        # About Section
        if 'about' in company:
            about_widgets = [
                self.factory.create_title(company['about']['title']),
                self.factory.create_text_editor(company['about']['content'])
            ]
            
            if 'image' in company['about']:
                about_widgets.append(self.factory.create_image(company['about']['image']))
            
            about_section = self.factory.create_section([about_widgets], {
                'background_color': '#ffffff',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(about_section)
        
        # Team Section
        if 'team' in company:
            team_columns = []
            for member in company['team']:
                widget = self.factory.create_team_member(
                    member['name'],
                    member['position'],
                    member.get('image', 'placeholder.jpg'),
                    member.get('socials', [])
                )
                team_columns.append([widget])
            
            team_section = self.factory.create_section(team_columns, {
                'background_color': '#fafafa',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(team_section)
        
        # Contact Section
        if 'contact' in company:
            contact_widget = self.factory.create_widget('cholot-contact', {
                'shortcode': company['contact'].get('shortcode', '[contact-form-7 id="1"]')
            })
            
            contact_section = self.factory.create_section([[contact_widget]], {
                'background_color': '#1f1f1f',
                'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
            })
            sections.append(contact_section)
        
        # Footer
        footer_text = f"© 2024 {company['name']}. {company.get('footer_text', 'Alle Rechte vorbehalten.')}"
        footer_section = self.factory.create_section([
            [self.factory.create_text_editor(footer_text)]
        ], {
            'background_color': '#1f1f1f',
            'padding': {'unit': 'px', 'top': '30', 'bottom': '30'}
        })
        sections.append(footer_section)
        
        return sections
    
    def _save_elementor_json(self, page_data: List[dict], company_name: str) -> str:
        """Save Elementor page data to JSON file"""
        filename = f"{company_name.replace(' ', '_').lower()}_elementor.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(page_data, f, indent=2, ensure_ascii=False)
        print(f"  📄 Elementor JSON: {filename}")
        return filename
    
    def _format_for_wordpress(self, json_file: str, company_name: str) -> str:
        """Format JSON for WordPress XML generator"""
        try:
            result = subprocess.run(
                [sys.executable, 'format_for_wordpress.py', json_file],
                capture_output=True, text=True, check=True
            )
            formatted_file = json_file.replace('.json', '_formatted.json')
            print(f"  📋 Formatted JSON: {formatted_file}")
            return formatted_file
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Formatting failed: {e}")
            return None
    
    def _generate_xml(self, formatted_file: str) -> str:
        """Generate WordPress XML from formatted JSON"""
        if not formatted_file:
            return None
        
        xml_file = formatted_file.replace('_formatted.json', '.xml')
        try:
            result = subprocess.run(
                [sys.executable, 'generate_wordpress_xml.py', '-i', formatted_file, '-o', xml_file],
                capture_output=True, text=True, check=True
            )
            print(f"  📦 WordPress XML: {xml_file}")
            return xml_file
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ XML generation failed: {e}")
            return None
    
    def print_summary(self):
        """Print orchestration summary"""
        print("\n" + "=" * 50)
        print("🎯 SWARM Orchestration Complete!")
        print("=" * 50)
        print(f"📊 Results:")
        print(f"  • Templates loaded: {self.results['templates_loaded']}")
        print(f"  • Pages generated: {self.results['pages_generated']}")
        print(f"  • XML files created: {len(self.results['xml_files_created'])}")
        
        if self.results['xml_files_created']:
            print(f"\n📁 Generated Files:")
            for xml_file in self.results['xml_files_created']:
                print(f"  • {xml_file}")

def main():
    # Test data - RIMAN GmbH and additional companies
    companies = [
        {
            'name': 'RIMAN GmbH',
            'tagline': 'Ihre Experten für professionelle Sanierung',
            'brand_color': '#b68c2f',
            'services': [
                {
                    'title': 'Asbestsanierung',
                    'subtitle': 'Sicher & Zertifiziert',
                    'description': 'Professionelle Entfernung von Asbest nach TRGS 519',
                    'icon': 'fas fa-shield-alt'
                },
                {
                    'title': 'PCB-Sanierung',
                    'subtitle': 'Umweltgerecht',
                    'description': 'Fachgerechte Entsorgung PCB-belasteter Materialien',
                    'icon': 'fas fa-biohazard'
                },
                {
                    'title': 'Schimmelsanierung',
                    'subtitle': 'Nachhaltig',
                    'description': 'Dauerhafte Beseitigung von Schimmelbefall',
                    'icon': 'fas fa-home'
                }
            ],
            'about': {
                'title': 'Über uns',
                'content': 'Mit über 20 Jahren Erfahrung sind wir Ihr Partner für sichere Sanierungen.'
            },
            'team': [
                {
                    'name': 'Michael Ritter',
                    'position': 'Geschäftsführer',
                    'socials': [{'icon': 'fab fa-linkedin-in', 'link': '#'}]
                }
            ],
            'footer_text': 'Alle Rechte vorbehalten.'
        },
        {
            'name': 'CleanTech Solutions',
            'tagline': 'Saubere Lösungen für eine bessere Zukunft',
            'brand_color': '#2ecc71',
            'services': [
                {
                    'title': 'Industriereinigung',
                    'subtitle': '24/7 Service',
                    'description': 'Professionelle Reinigung für Industrieanlagen',
                    'icon': 'fas fa-industry'
                },
                {
                    'title': 'Gebäudereinigung',
                    'subtitle': 'Gründlich',
                    'description': 'Regelmäßige Reinigung für Bürogebäude',
                    'icon': 'fas fa-building'
                }
            ],
            'about': {
                'title': 'CleanTech Solutions',
                'content': 'Innovative Reinigungslösungen seit 2010.'
            }
        }
    ]
    
    print("🚀 SWARM Orchestrator for Elementor Generator")
    print("=" * 50)
    
    orchestrator = SwarmOrchestrator()
    orchestrator.generate_company_pages(companies)
    orchestrator.print_summary()
    
    # Store results in memory
    try:
        subprocess.run([
            'npx', 'claude-flow', 'memory', 'store',
            'elementor_generation_complete',
            json.dumps(orchestrator.results)
        ], check=True)
        print("\n💾 Results stored in Claude Flow memory")
    except:
        pass

if __name__ == '__main__':
    main()