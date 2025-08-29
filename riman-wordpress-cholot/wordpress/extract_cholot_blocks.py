#!/usr/bin/env python3
"""
Cholot Block Extractor
Extrahiert wiederverwendbare Blocks aus der Cholot Theme demo-data-fixed.xml
"""

import xml.etree.ElementTree as ET
import json
from pathlib import Path
from typing import Dict, List, Any
import re

class CholotBlockExtractor:
    """Extrahiert und kategorisiert Cholot Theme Blocks"""
    
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.blocks = {}
        self.widgets = {}
        self.patterns = {}
        
    def extract_blocks(self):
        """Hauptfunktion zum Extrahieren aller Blocks"""
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        
        # Namespace handling
        namespaces = {
            'wp': 'http://wordpress.org/export/1.2/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        
        # Finde alle Posts/Pages mit Elementor Data
        for item in root.findall('.//item'):
            post_type = item.find('.//wp:post_type', namespaces)
            if post_type is not None and post_type.text in ['page', 'post']:
                self.extract_elementor_data(item, namespaces)
        
        # Speichere extrahierte Blocks
        self.save_blocks()
    
    def extract_elementor_data(self, item, namespaces):
        """Extrahiert Elementor Data aus einem Post/Page Item"""
        title = item.find('.//title').text or 'Untitled'
        
        # Suche nach Elementor postmeta
        for postmeta in item.findall('.//wp:postmeta', namespaces):
            meta_key = postmeta.find('.//wp:meta_key', namespaces)
            if meta_key is not None and meta_key.text == '_elementor_data':
                meta_value = postmeta.find('.//wp:meta_value', namespaces)
                if meta_value is not None and meta_value.text:
                    try:
                        # Parse Elementor JSON
                        elementor_data = json.loads(meta_value.text)
                        self.analyze_elementor_structure(elementor_data, title)
                    except json.JSONDecodeError:
                        print(f"⚠️ Fehler beim Parsen von Elementor Data in: {title}")
    
    def analyze_elementor_structure(self, data: List[Dict], source: str):
        """Analysiert Elementor Struktur und extrahiert Patterns"""
        for section in data:
            if section.get('elType') == 'section':
                self.extract_section_pattern(section, source)
    
    def extract_section_pattern(self, section: Dict, source: str):
        """Extrahiert Section Patterns"""
        # Identifiziere Section-Typ basierend auf Widgets
        section_type = self.identify_section_type(section)
        
        if section_type:
            # Säubere IDs für Wiederverwendbarkeit
            clean_section = self.clean_ids(section)
            
            if section_type not in self.blocks:
                self.blocks[section_type] = []
            
            self.blocks[section_type].append({
                'source': source,
                'structure': clean_section,
                'widgets': self.extract_widgets(section)
            })
    
    def identify_section_type(self, section: Dict) -> str:
        """Identifiziert Section-Typ basierend auf enthaltenen Widgets"""
        widgets = self.extract_widgets(section)
        
        # Erkenne bekannte Patterns
        if 'rdn-slider' in widgets:
            return 'hero_slider'
        elif 'cholot-texticon' in widgets:
            if self.has_shape_divider(section):
                return 'service_card_with_shape'
            else:
                return 'icon_box'
        elif 'testimonial-carousel' in widgets:
            return 'testimonials'
        elif 'contact-form-7' in str(section):
            return 'contact_form'
        elif 'cholot-contact-shortcode' in widgets:
            return 'contact_custom'
        elif self.has_shape_divider(section):
            return 'shaped_section'
        else:
            # Generischer Typ basierend auf Layout
            columns = len(section.get('elements', []))
            if columns == 1:
                return 'single_column'
            elif columns == 2:
                return 'two_column'
            elif columns == 3:
                return 'three_column'
            elif columns == 4:
                return 'four_column'
            else:
                return 'multi_column'
    
    def has_shape_divider(self, section: Dict) -> bool:
        """Prüft ob Section einen Shape Divider hat"""
        settings = section.get('settings', {})
        return 'shape_divider_bottom' in settings or 'shape_divider_top' in settings
    
    def extract_widgets(self, element: Dict) -> List[str]:
        """Extrahiert alle Widget-Typen aus einem Element"""
        widgets = []
        
        if element.get('widgetType'):
            widgets.append(element['widgetType'])
        
        # Rekursiv durch Elemente
        for child in element.get('elements', []):
            if child.get('elType') == 'column':
                for column_child in child.get('elements', []):
                    widgets.extend(self.extract_widgets(column_child))
            elif child.get('elType') == 'section' and child.get('isInner'):
                # Inner Section
                for inner_col in child.get('elements', []):
                    for inner_elem in inner_col.get('elements', []):
                        widgets.extend(self.extract_widgets(inner_elem))
            else:
                widgets.extend(self.extract_widgets(child))
        
        return widgets
    
    def clean_ids(self, element: Dict) -> Dict:
        """Entfernt IDs für Wiederverwendbarkeit"""
        import copy
        clean = copy.deepcopy(element)
        
        # Entferne oder ersetze IDs
        if 'id' in clean:
            clean['id'] = '__ID__'
        
        # Rekursiv durch Elemente
        if 'elements' in clean:
            for i, child in enumerate(clean['elements']):
                clean['elements'][i] = self.clean_ids(child)
        
        return clean
    
    def save_blocks(self):
        """Speichert extrahierte Blocks in Dateien"""
        output_dir = Path('cholot_theme_library')
        output_dir.mkdir(exist_ok=True)
        
        # Speichere Blocks nach Typ
        for block_type, blocks in self.blocks.items():
            output_file = output_dir / f'{block_type}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(blocks, f, indent=2, ensure_ascii=False)
            print(f"✅ {len(blocks)} {block_type} Blocks gespeichert")
        
        # Speichere Summary
        summary = {
            'total_blocks': sum(len(blocks) for blocks in self.blocks.values()),
            'block_types': list(self.blocks.keys()),
            'widgets_found': list(set(widget for blocks in self.blocks.values() 
                                     for block in blocks 
                                     for widget in block.get('widgets', [])))
        }
        
        with open(output_dir / 'summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Zusammenfassung:")
        print(f"   - {summary['total_blocks']} Blocks extrahiert")
        print(f"   - {len(summary['block_types'])} verschiedene Block-Typen")
        print(f"   - {len(summary['widgets_found'])} verschiedene Widget-Typen gefunden")


def main():
    """Hauptfunktion"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extrahiere Cholot Theme Blocks')
    parser.add_argument('--xml', default='demo-data-fixed.xml', 
                       help='Cholot Theme XML Datei')
    
    args = parser.parse_args()
    
    if not Path(args.xml).exists():
        print(f"❌ Datei nicht gefunden: {args.xml}")
        return
    
    print(f"🔍 Extrahiere Blocks aus: {args.xml}")
    
    extractor = CholotBlockExtractor(args.xml)
    extractor.extract_blocks()
    
    print("\n✅ Extraktion abgeschlossen!")
    print(f"   Blocks gespeichert in: cholot_theme_library/")


if __name__ == "__main__":
    main()