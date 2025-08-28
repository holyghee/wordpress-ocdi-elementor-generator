#!/usr/bin/env python3
import json
import re
from pathlib import Path
from copy import deepcopy
from typing import Dict, List, Any
import uuid

class TemplateBasedFactory:
    def __init__(self):
        self.templates = self._load_all_templates()
        self.widget_counter = 0
    
    def _load_all_templates(self) -> Dict[str, dict]:
        templates = {}
        templates_dir = Path('templates')
        
        for template_file in templates_dir.glob('*.template.json'):
            widget_type = template_file.stem.replace('.template', '')
            with open(template_file, 'r', encoding='utf-8') as f:
                templates[widget_type] = json.load(f)
        
        return templates
    
    def _generate_id(self) -> str:
        return ''.join(format(ord(c), 'x')[:2] for c in str(uuid.uuid4())[:8])
    
    def _inject_content(self, template: Any, content_data: Dict[str, Any]) -> Any:
        if isinstance(template, str):
            pattern = r'\{\{([^}]+)\}\}'
            matches = re.findall(pattern, template)
            result = template
            for match in matches:
                key = match.strip()
                if key in content_data:
                    result = result.replace(f'{{{{{match}}}}}', str(content_data[key]))
            return result
        elif isinstance(template, dict):
            result = {}
            for key, value in template.items():
                result[key] = self._inject_content(value, content_data)
            return result
        elif isinstance(template, list):
            return [self._inject_content(item, content_data) for item in template]
        else:
            return template
    
    def create_widget(self, widget_type: str, content_data: Dict[str, Any]) -> dict:
        if widget_type not in self.templates:
            raise ValueError(f"Template for widget type '{widget_type}' not found")
        
        template = deepcopy(self.templates[widget_type])
        widget = self._inject_content(template, content_data)
        
        if 'id' not in widget:
            widget['id'] = self._generate_id()
        
        self.widget_counter += 1
        return widget
    
    def create_texticon(self, title: str, subtitle: str, text: str, icon: str = 'fas fa-procedures') -> dict:
        return self.create_widget('cholot-texticon', {
            'title': title,
            'subtitle': subtitle,
            'content': text,
            'icon_value': icon
        })
    
    def create_title(self, title: str) -> dict:
        return self.create_widget('cholot-title', {
            'title': title
        })
    
    def create_text_editor(self, content: str) -> dict:
        return self.create_widget('text-editor', {
            'content': f'<p>{content}</p>'
        })
    
    def create_image(self, image_url: str, image_id: str = '1') -> dict:
        return self.create_widget('image', {
            'image_url': image_url,
            'image_id': image_id
        })
    
    def create_team_member(self, name: str, position: str, image_url: str, socials: List[Dict]) -> dict:
        social_data = {}
        for i, social in enumerate(socials):
            social_data[f'social_icon_{i}'] = social.get('icon', 'fab fa-facebook-f')
            social_data[f'social_link_{i}'] = social.get('link', '#')
        
        return self.create_widget('cholot-team', {
            'title': name,
            'content': position,
            'image_url': image_url,
            'image_id': '1',
            **social_data
        })
    
    def create_section(self, columns: List[dict], section_settings: dict = None) -> dict:
        section = {
            'id': self._generate_id(),
            'elType': 'section',
            'isInner': False,
            'settings': section_settings or {},
            'elements': []
        }
        
        for column_widgets in columns:
            column = {
                'id': self._generate_id(),
                'elType': 'column',
                'isInner': False,
                'settings': {'_column_size': 100 // len(columns)},
                'elements': column_widgets if isinstance(column_widgets, list) else [column_widgets]
            }
            section['elements'].append(column)
        
        return section
    
    def generate_page(self, sections: List[dict]) -> List[dict]:
        return sections
    
    def save_to_json(self, data: Any, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {filename}")

def demo_riman_company():
    factory = TemplateBasedFactory()
    
    sections = []
    
    hero_section = factory.create_section([
        [factory.create_title("RIMAN GmbH - Ihre Experten für Sanierung")]
    ], {
        'background_color': '#b68c2f',
        'padding': {'unit': 'px', 'top': '60', 'bottom': '60'}
    })
    sections.append(hero_section)
    
    services = [
        ('Asbestsanierung', 'Professionell', 'Sichere und fachgerechte Entfernung von Asbest', 'fas fa-shield-alt'),
        ('PCB-Sanierung', 'Zertifiziert', 'Umweltgerechte Entsorgung von PCB-Materialien', 'fas fa-biohazard'),
        ('Schimmelsanierung', 'Gründlich', 'Nachhaltige Beseitigung von Schimmelbefall', 'fas fa-home')
    ]
    
    service_widgets = []
    for title, subtitle, text, icon in services:
        service_widgets.append([factory.create_texticon(title, subtitle, text, icon)])
    
    services_section = factory.create_section(service_widgets, {
        'gap': 'extended',
        'structure': '30',
        'background_color': '#fafafa'
    })
    sections.append(services_section)
    
    footer_section = factory.create_section([
        [factory.create_text_editor("© 2024 RIMAN GmbH. Alle Rechte vorbehalten.")]
    ], {
        'background_color': '#1f1f1f',
        'padding': {'unit': 'px', 'top': '30', 'bottom': '30'}
    })
    sections.append(footer_section)
    
    page_data = factory.generate_page(sections)
    factory.save_to_json(page_data, 'riman_test_output.json')
    
    return page_data

if __name__ == '__main__':
    print("🚀 Template-Based Generator Ready!")
    print("=" * 50)
    print("\n📋 Available widget types:")
    factory = TemplateBasedFactory()
    for widget_type in factory.templates.keys():
        print(f"  - {widget_type}")
    
    print("\n🔧 Generating RIMAN GmbH test page...")
    demo_riman_company()
    print("\n✅ Test page generated successfully!")