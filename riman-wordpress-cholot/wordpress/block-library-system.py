#!/usr/bin/env python3
"""
Block Library System - Extrahiert und verwaltet wiederverwendbare Design Blocks
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
import hashlib

class ElementorBlockLibrary:
    """
    Extrahiert Design-Blocks aus Elementor Templates und macht sie wiederverwendbar
    """
    
    def __init__(self):
        self.blocks = {}
        self.block_index = {}
        
    def extract_blocks_from_template(self, template_file: str):
        """
        Extrahiert ALLE Sections/Widgets als wiederverwendbare Blocks
        """
        print(f"📦 Extrahiere Blocks aus {template_file}")
        
        with open(template_file, 'r') as f:
            template_data = json.load(f)
        
        blocks_found = []
        
        # Durchlaufe alle Sections
        for section_idx, section in enumerate(template_data):
            # Extrahiere Section als Block
            section_block = self.extract_section_block(section, section_idx)
            blocks_found.append(section_block)
            
            # Extrahiere auch einzelne Widgets
            for column in section.get('elements', []):
                for widget in column.get('elements', []):
                    widget_block = self.extract_widget_block(widget)
                    if widget_block:
                        blocks_found.append(widget_block)
        
        print(f"✅ {len(blocks_found)} Blocks extrahiert")
        return blocks_found
    
    def extract_section_block(self, section: Dict, idx: int) -> Dict:
        """
        Macht eine Section zu einem wiederverwendbaren Block
        """
        # Generiere einzigartige ID basierend auf Structure
        block_id = self.generate_block_id(section)
        
        # Analysiere Section
        analysis = self.analyze_section(section)
        
        block = {
            "id": block_id,
            "type": "section",
            "name": f"section_{analysis['structure']}_{analysis['widget_types'][0] if analysis['widget_types'] else 'empty'}",
            "description": self.generate_description(analysis),
            "metadata": {
                "structure": analysis['structure'],
                "columns": analysis['columns'],
                "widgets": analysis['widget_types'],
                "has_background": analysis['has_background'],
                "responsive": analysis['responsive_settings']
            },
            "variables": self.extract_variables(section),
            "json": section,  # Der komplette JSON Block mit allen Styles
            "usage_example": self.generate_usage_example(analysis)
        }
        
        # Speichere in Library
        self.blocks[block_id] = block
        self.index_block(block)
        
        return block
    
    def analyze_section(self, section: Dict) -> Dict:
        """
        Analysiert eine Section um sie zu kategorisieren
        """
        settings = section.get('settings', {})
        elements = section.get('elements', [])
        
        # Struktur erkennen (33-33-33, 50-50, 100, etc.)
        structure = settings.get('structure', '100')
        
        # Widget-Typen sammeln
        widget_types = []
        for column in elements:
            for widget in column.get('elements', []):
                widget_type = widget.get('widgetType', 'unknown')
                if widget_type not in widget_types:
                    widget_types.append(widget_type)
        
        # Background analysieren
        has_background = bool(settings.get('background_background'))
        
        # Responsive Settings
        responsive_settings = any(
            key.endswith('_tablet') or key.endswith('_mobile') 
            for key in settings.keys()
        )
        
        return {
            "structure": structure,
            "columns": len(elements),
            "widget_types": widget_types,
            "has_background": has_background,
            "responsive_settings": responsive_settings,
            "padding": settings.get('padding'),
            "margin": settings.get('margin')
        }
    
    def extract_variables(self, block: Dict) -> Dict:
        """
        Findet alle Texte/Bilder die als Variablen ersetzt werden können
        """
        variables = {}
        
        def find_text_content(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['title', 'text', 'subtitle', 'description', 'btn_text']:
                        var_name = f"{path}.{key}" if path else key
                        variables[var_name] = {
                            "type": "text",
                            "default": value,
                            "path": f"{path}.{key}"
                        }
                    elif key == 'url' and isinstance(value, str) and (
                        value.endswith('.jpg') or value.endswith('.png')
                    ):
                        var_name = f"{path}.image" if path else "image"
                        variables[var_name] = {
                            "type": "image",
                            "default": value,
                            "path": f"{path}.url"
                        }
                    elif isinstance(value, (dict, list)):
                        find_text_content(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    find_text_content(item, f"{path}[{idx}]")
        
        find_text_content(block)
        return variables
    
    def generate_block_id(self, block: Dict) -> str:
        """Generiert einzigartige ID für Block"""
        # Nutze Structure + Widget Types für ID
        block_str = json.dumps(block.get('settings', {}).get('structure', ''))
        return hashlib.md5(block_str.encode()).hexdigest()[:8]
    
    def generate_description(self, analysis: Dict) -> str:
        """Generiert Beschreibung basierend auf Analyse"""
        desc = f"{analysis['columns']}-column section"
        if analysis['widget_types']:
            desc += f" with {', '.join(analysis['widget_types'][:3])}"
        if analysis['has_background']:
            desc += " (with background)"
        return desc
    
    def generate_usage_example(self, analysis: Dict) -> str:
        """Zeigt wie der Block verwendet werden kann"""
        return f"""
blocks:
  - use: "{analysis['structure']}_section"
    content:
      title: "Your Title"
      services: ["Service 1", "Service 2", "Service 3"]
"""
    
    def index_block(self, block: Dict):
        """Indexiert Block für schnelle Suche"""
        # Nach Typ
        block_type = block['metadata']['structure']
        if block_type not in self.block_index:
            self.block_index[block_type] = []
        self.block_index[block_type].append(block['id'])
        
        # Nach Widgets
        for widget in block['metadata']['widgets']:
            if widget not in self.block_index:
                self.block_index[widget] = []
            self.block_index[widget].append(block['id'])
    
    def extract_widget_block(self, widget: Dict) -> Dict:
        """Extrahiert einzelnes Widget als Block"""
        widget_type = widget.get('widgetType', 'unknown')
        
        # Nur interessante Widgets
        if widget_type in ['cholot-texticon', 'cholot-title', 'cholot-team']:
            return {
                "id": self.generate_block_id(widget),
                "type": "widget",
                "name": widget_type,
                "widget_type": widget_type,
                "variables": self.extract_variables(widget),
                "json": widget
            }
        return None
    
    def save_library(self, output_file: str):
        """Speichert die Block-Library"""
        library = {
            "blocks": list(self.blocks.values()),
            "index": self.block_index,
            "stats": {
                "total_blocks": len(self.blocks),
                "sections": len([b for b in self.blocks.values() if b['type'] == 'section']),
                "widgets": len([b for b in self.blocks.values() if b['type'] == 'widget'])
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"\n📚 Block Library gespeichert: {output_file}")
        print(f"   - {library['stats']['total_blocks']} Blocks total")
        print(f"   - {library['stats']['sections']} Sections")
        print(f"   - {library['stats']['widgets']} Widgets")


class SimplePageBuilder:
    """
    Baut Pages aus einfachen YAML Definitionen mit der Block Library
    """
    
    def __init__(self, block_library_file: str):
        with open(block_library_file, 'r') as f:
            self.library = json.load(f)
        self.blocks_by_id = {b['id']: b for b in self.library['blocks']}
    
    def build_from_yaml(self, yaml_file: str):
        """
        Baut komplexe Elementor JSON aus simpler YAML
        """
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"\n🏗️ Baue Page aus {yaml_file}")
        
        page_json = []
        
        for section_config in config['sections']:
            if 'use_block' in section_config:
                # Verwende existierenden Block
                block = self.get_block(section_config['use_block'])
                if block:
                    # Injiziere Content
                    modified_block = self.inject_content(
                        block['json'], 
                        section_config.get('content', {})
                    )
                    page_json.append(modified_block)
                    print(f"  ✅ Block '{section_config['use_block']}' hinzugefügt")
            
            elif 'type' in section_config:
                # Finde passenden Block nach Typ
                block = self.find_block_by_type(section_config['type'])
                if block:
                    modified_block = self.inject_content(
                        block['json'],
                        section_config.get('content', {})
                    )
                    page_json.append(modified_block)
                    print(f"  ✅ Block vom Typ '{section_config['type']}' gefunden")
        
        return page_json
    
    def get_block(self, block_id: str) -> Dict:
        """Holt Block aus Library"""
        return self.blocks_by_id.get(block_id)
    
    def find_block_by_type(self, block_type: str) -> Dict:
        """Findet passenden Block nach Typ"""
        # Suche nach Structure (33, 50, 100)
        if block_type in self.library['index']:
            block_ids = self.library['index'][block_type]
            if block_ids:
                return self.blocks_by_id[block_ids[0]]
        
        # Suche nach Widget Type
        for block in self.library['blocks']:
            if block_type in block.get('metadata', {}).get('widgets', []):
                return block
        
        return None
    
    def inject_content(self, block_json: Dict, content: Dict) -> Dict:
        """
        Injiziert Content in Block JSON
        """
        import copy
        modified = copy.deepcopy(block_json)
        
        # Simple Text Replacement
        json_str = json.dumps(modified)
        for key, value in content.items():
            if isinstance(value, str):
                # Ersetze Platzhalter oder Default-Texte
                json_str = json_str.replace(f"{{{key}}}", value)
        
        return json.loads(json_str)


def create_simple_yaml_example():
    """
    Zeigt wie einfach die YAML sein kann
    """
    return """# Super Simple Page Definition
# Verwendet Block Library statt komplexe JSON zu schreiben

sections:
  # Hero Section - nutzt existierenden Block
  - use_block: "hero_slider_dark"
    content:
      title: "RIMAN GmbH"
      subtitle: "Professionelle Schadstoffsanierung"
      button_text: "Kontakt"
  
  # Service Section - System findet passenden Block
  - type: "service_3_columns"
    content:
      services:
        - title: "Asbestsanierung"
          text: "Sicher und zertifiziert"
        - title: "PCB-Sanierung"  
          text: "Umweltgerecht"
        - title: "Schimmelsanierung"
          text: "Nachhaltig"
  
  # About Section - nach Widget-Typ
  - type: "cholot-title"
    content:
      title: "Über uns"
      description: "25 Jahre Erfahrung"
"""


def main():
    """Demo: Extrahiere Blocks und baue neue Page"""
    
    # 1. Extrahiere Blocks aus Templates
    print("🔍 SCHRITT 1: Extrahiere Design Blocks aus Templates")
    print("="*50)
    
    library = ElementorBlockLibrary()
    
    # Aus allen Templates
    templates = [
        "templates/home-page.json",
        "templates/service-page.json",
        "templates/about-page.json"
    ]
    
    for template in templates:
        if Path(template).exists():
            blocks = library.extract_blocks_from_template(template)
    
    # Speichere Library
    library.save_library("block-library.json")
    
    print("\n" + "="*50)
    print("📝 SCHRITT 2: Erstelle neue Page mit simpler YAML")
    print("="*50)
    
    # Erstelle simple YAML
    yaml_content = create_simple_yaml_example()
    with open("simple-page.yaml", 'w') as f:
        f.write(yaml_content)
    
    print("Simple YAML erstellt:")
    print(yaml_content)
    
    # Baue Page
    if Path("block-library.json").exists():
        builder = SimplePageBuilder("block-library.json")
        # page_json = builder.build_from_yaml("simple-page.yaml")
        print("\n✨ Mit Block Library können wir aus simpler YAML komplexe JSON bauen!")


if __name__ == "__main__":
    main()