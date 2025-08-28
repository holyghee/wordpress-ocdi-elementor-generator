#!/usr/bin/env python3
"""
Block Library Extractor
Extrahiert wiederverwendbare Komponenten aus Elementor-Templates
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
import hashlib

class BlockLibraryExtractor:
    def __init__(self, source_dir: str = "elementor_structures", output_dir: str = "block_library"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.blocks = {}
        self.block_patterns = {}
        
    def extract_blocks(self):
        """Extrahiere alle einzigartigen Block-Patterns aus Elementor-Templates"""
        print("🔍 Analysiere Elementor-Templates...")
        
        for template_file in self.source_dir.glob("*.json"):
            print(f"\n📄 Verarbeite: {template_file.name}")
            
            with open(template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extrahiere Elementor-Sections
            if isinstance(data, dict):
                if '_elementor_data' in data:
                    elementor_data = data['_elementor_data']
                    if isinstance(elementor_data, str):
                        elementor_data = json.loads(elementor_data)
                elif '_elementor_data_parsed' in data:
                    elementor_data = data['_elementor_data_parsed']
                else:
                    elementor_data = data
            else:
                elementor_data = data
            
            # Analysiere Sections
            if isinstance(elementor_data, list):
                for section in elementor_data:
                    self._analyze_section(section, template_file.stem)
    
    def _analyze_section(self, section: Dict, source_template: str):
        """Analysiere eine Section und extrahiere als wiederverwendbaren Block"""
        if not isinstance(section, dict):
            return
            
        # Identifiziere Block-Typ basierend auf Widgets
        block_type = self._identify_block_type(section)
        if not block_type:
            return
        
        # Erstelle Block-Signatur für Deduplizierung
        signature = self._create_block_signature(section)
        
        if signature not in self.block_patterns:
            # Neues Pattern gefunden
            block_id = f"{block_type}_{len(self.block_patterns) + 1}"
            
            # Extrahiere Block-Struktur mit Platzhaltern
            block_template = self._create_block_template(section, block_type)
            
            self.block_patterns[signature] = {
                'id': block_id,
                'type': block_type,
                'source': source_template,
                'structure': block_template,
                'configurable_fields': self._extract_configurable_fields(section)
            }
            
            print(f"  ✅ Neuer Block extrahiert: {block_id} ({block_type})")
    
    def _identify_block_type(self, section: Dict) -> str:
        """Identifiziere den Typ eines Blocks basierend auf seinen Widgets"""
        widget_types = []
        
        # Sammle alle Widget-Typen in dieser Section
        def collect_widgets(element):
            if isinstance(element, dict):
                if 'widgetType' in element:
                    widget_types.append(element['widgetType'])
                if 'elements' in element:
                    for el in element['elements']:
                        collect_widgets(el)
        
        collect_widgets(section)
        
        # Bestimme Block-Typ basierend auf Widgets
        if 'rdn-slider' in widget_types:
            return 'hero-slider'
        elif 'cholot-texticon' in widget_types:
            return 'service-cards'
        elif 'cholot-team' in widget_types:
            return 'team-section'
        elif 'cholot-testimonial' in widget_types or 'cholot-testimonial-two' in widget_types:
            return 'testimonials'
        elif 'cholot-contact' in widget_types:
            return 'contact-form'
        elif 'cholot-title' in widget_types:
            return 'title-section'
        elif 'video' in widget_types:
            return 'video-section'
        elif 'image' in widget_types and len(widget_types) > 2:
            return 'gallery-section'
        elif 'text-editor' in widget_types:
            return 'text-content'
        else:
            return None
    
    def _create_block_signature(self, section: Dict) -> str:
        """Erstelle eine eindeutige Signatur für einen Block"""
        # Erstelle Signatur basierend auf Struktur, nicht auf Inhalten
        structure = self._extract_structure_only(section)
        return hashlib.md5(json.dumps(structure, sort_keys=True).encode()).hexdigest()
    
    def _extract_structure_only(self, element: Any) -> Any:
        """Extrahiere nur die Struktur ohne spezifische Inhalte"""
        if isinstance(element, dict):
            result = {}
            for key, value in element.items():
                if key in ['elType', 'widgetType', 'elements']:
                    result[key] = self._extract_structure_only(value)
                elif key == 'settings':
                    # Behalte nur strukturelle Settings
                    result[key] = {k: 'PLACEHOLDER' for k in value.keys() 
                                  if k in ['columns', 'structure', 'gap', 'layout']}
            return result
        elif isinstance(element, list):
            return [self._extract_structure_only(item) for item in element]
        else:
            return 'PLACEHOLDER'
    
    def _create_block_template(self, section: Dict, block_type: str) -> Dict:
        """Erstelle ein Template mit Platzhaltern für konfigurierbare Inhalte"""
        template = json.loads(json.dumps(section))  # Deep copy
        
        # Ersetze spezifische Inhalte mit Platzhaltern
        def add_placeholders(element, path=""):
            if isinstance(element, dict):
                if 'widgetType' in element and 'settings' in element:
                    widget_type = element['widgetType']
                    settings = element['settings']
                    
                    # Definiere Platzhalter basierend auf Widget-Typ
                    if widget_type == 'cholot-title':
                        if 'title' in settings:
                            settings['title'] = "{{TITLE}}"
                        if 'subtitle' in settings:
                            settings['subtitle'] = "{{SUBTITLE}}"
                    
                    elif widget_type == 'cholot-texticon':
                        if 'title' in settings:
                            settings['title'] = "{{SERVICE_TITLE}}"
                        if 'text' in settings:
                            settings['text'] = "{{SERVICE_TEXT}}"
                        if 'icon' in settings:
                            settings['icon'] = "{{SERVICE_ICON}}"
                    
                    elif widget_type == 'rdn-slider':
                        if 'slider_list' in settings:
                            for i, slide in enumerate(settings['slider_list']):
                                slide['title'] = f"{{{{SLIDE_{i}_TITLE}}}}"
                                slide['subtitle'] = f"{{{{SLIDE_{i}_SUBTITLE}}}}"
                                slide['btn_text'] = f"{{{{SLIDE_{i}_BUTTON}}}}"
                
                if 'elements' in element:
                    for el in element['elements']:
                        add_placeholders(el, path + "/" + element.get('id', ''))
        
        add_placeholders(template)
        return template
    
    def _extract_configurable_fields(self, section: Dict) -> List[Dict]:
        """Extrahiere Liste der konfigurierbaren Felder"""
        fields = []
        
        def extract_fields(element, path=""):
            if isinstance(element, dict):
                if 'widgetType' in element and 'settings' in element:
                    widget_type = element['widgetType']
                    widget_id = element.get('id', 'unknown')
                    
                    # Definiere konfigurierbare Felder pro Widget-Typ
                    if widget_type == 'cholot-title':
                        fields.append({
                            'field': 'title',
                            'type': 'text',
                            'widget': widget_id,
                            'placeholder': '{{TITLE}}'
                        })
                        fields.append({
                            'field': 'subtitle',
                            'type': 'text',
                            'widget': widget_id,
                            'placeholder': '{{SUBTITLE}}'
                        })
                    
                    elif widget_type == 'cholot-texticon':
                        fields.append({
                            'field': 'service_title',
                            'type': 'text',
                            'widget': widget_id,
                            'placeholder': '{{SERVICE_TITLE}}'
                        })
                        fields.append({
                            'field': 'service_text',
                            'type': 'text',
                            'widget': widget_id,
                            'placeholder': '{{SERVICE_TEXT}}'
                        })
                        fields.append({
                            'field': 'service_icon',
                            'type': 'icon',
                            'widget': widget_id,
                            'placeholder': '{{SERVICE_ICON}}'
                        })
                
                if 'elements' in element:
                    for el in element['elements']:
                        extract_fields(el, path + "/" + element.get('id', ''))
        
        extract_fields(section)
        return fields
    
    def save_library(self):
        """Speichere die extrahierte Block-Library"""
        # Speichere jeden Block als separate JSON
        for signature, block_data in self.block_patterns.items():
            block_file = self.output_dir / f"{block_data['id']}.json"
            with open(block_file, 'w', encoding='utf-8') as f:
                json.dump(block_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Gespeichert: {block_file.name}")
        
        # Erstelle Index-Datei
        index = {
            'blocks': [
                {
                    'id': block['id'],
                    'type': block['type'],
                    'source': block['source'],
                    'configurable_fields': len(block['configurable_fields'])
                }
                for block in self.block_patterns.values()
            ],
            'total': len(self.block_patterns)
        }
        
        index_file = self.output_dir / "index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"\n📚 Block-Library erstellt: {len(self.block_patterns)} Blocks")
        print(f"📁 Gespeichert in: {self.output_dir}/")
        
        return self.output_dir
    
    def analyze_and_report(self):
        """Erstelle einen Analyse-Report"""
        report = []
        report.append("\n" + "="*60)
        report.append("📊 BLOCK LIBRARY ANALYSE")
        report.append("="*60)
        
        # Gruppiere Blocks nach Typ
        by_type = {}
        for block in self.block_patterns.values():
            block_type = block['type']
            if block_type not in by_type:
                by_type[block_type] = []
            by_type[block_type].append(block)
        
        report.append(f"\n🎨 Gefundene Block-Typen: {len(by_type)}")
        for block_type, blocks in by_type.items():
            report.append(f"  • {block_type}: {len(blocks)} Varianten")
        
        report.append(f"\n📝 Konfigurierbare Felder insgesamt:")
        total_fields = sum(len(b['configurable_fields']) for b in self.block_patterns.values())
        report.append(f"  • {total_fields} Felder")
        
        report.append("\n✅ Block-Library bereit zur Verwendung!")
        report.append("="*60)
        
        return "\n".join(report)

def main():
    """Hauptausführung"""
    print("\n🚀 Block Library Extractor")
    print("="*50)
    
    extractor = BlockLibraryExtractor()
    
    # Extrahiere Blocks
    extractor.extract_blocks()
    
    # Speichere Library
    extractor.save_library()
    
    # Zeige Report
    print(extractor.analyze_and_report())
    
    return True

if __name__ == "__main__":
    main()