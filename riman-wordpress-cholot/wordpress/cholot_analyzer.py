#!/usr/bin/env python3
"""
Cholot Theme Analyzer

This script analyzes the Cholot theme structure by examining:
1. Complete page templates (JSON files)
2. Elementor blocks (reusable components)
3. Target XML structure from demo data
4. Creates a mapping configuration for complete reconstruction

Author: Claude Code Assistant
Date: 2025-08-28
"""

import json
import os
import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import re

class CholotAnalyzer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.templates_dir = self.base_path / "templates"
        self.blocks_dir = self.base_path / "elemetor blocks"
        self.target_xml_path = Path("/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml")
        
        self.templates = {}
        self.blocks = {}
        self.xml_structure = {}
        self.widget_analysis = defaultdict(list)
        self.mapping_config = {}
        
    def analyze_json_template(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single JSON template file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            template_info = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'sections': [],
                'widget_types': set(),
                'total_elements': 0,
                'structure': {}
            }
            
            # Analyze sections if it's a list (complete page template)
            if isinstance(data, list):
                template_info['sections'] = self._analyze_sections(data)
                template_info['total_elements'] = len(data)
                for section in data:
                    self._extract_widgets_from_section(section, template_info['widget_types'])
            
            template_info['widget_types'] = list(template_info['widget_types'])
            return template_info
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return {}
    
    def analyze_elementor_block(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Elementor block file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            block_info = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'title': data.get('title', 'Unknown'),
                'type': data.get('type', 'section'),
                'version': data.get('version', '0.4'),
                'content': [],
                'widget_types': set(),
                'total_elements': 0
            }
            
            # Analyze content if available
            if 'content' in data and isinstance(data['content'], list):
                block_info['content'] = self._analyze_sections(data['content'])
                block_info['total_elements'] = len(data['content'])
                for section in data['content']:
                    self._extract_widgets_from_section(section, block_info['widget_types'])
            
            block_info['widget_types'] = list(block_info['widget_types'])
            return block_info
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return {}
    
    def _analyze_sections(self, sections: List[Dict]) -> List[Dict]:
        """Analyze sections structure"""
        analyzed_sections = []
        
        for i, section in enumerate(sections):
            section_info = {
                'index': i,
                'id': section.get('id', f'section_{i}'),
                'type': section.get('elType', 'unknown'),
                'widget_type': section.get('widgetType', None),
                'settings_keys': list(section.get('settings', {}).keys()),
                'elements_count': len(section.get('elements', [])),
                'has_inner_sections': False
            }
            
            # Check for inner sections/columns
            elements = section.get('elements', [])
            for element in elements:
                if element.get('elType') == 'section':
                    section_info['has_inner_sections'] = True
                    break
            
            analyzed_sections.append(section_info)
        
        return analyzed_sections
    
    def _extract_widgets_from_section(self, section: Dict, widget_types: set):
        """Recursively extract all widget types from a section"""
        if 'widgetType' in section:
            widget_types.add(section['widgetType'])
            
            # Store widget analysis for later use
            widget_info = {
                'id': section.get('id'),
                'type': section.get('widgetType'),
                'settings': section.get('settings', {}),
                'el_type': section.get('elType', 'widget')
            }
            self.widget_analysis[section['widgetType']].append(widget_info)
        
        # Recurse through elements
        for element in section.get('elements', []):
            self._extract_widgets_from_section(element, widget_types)
    
    def analyze_xml_structure(self):
        """Analyze the target XML structure"""
        if not self.target_xml_path.exists():
            print(f"XML file not found: {self.target_xml_path}")
            return
        
        try:
            tree = ET.parse(self.target_xml_path)
            root = tree.getroot()
            
            self.xml_structure = {
                'channel': {
                    'title': '',
                    'link': '',
                    'description': ''
                },
                'authors': [],
                'categories': [],
                'tags': [],
                'terms': [],
                'items': []
            }
            
            # Extract basic channel info
            channel = root.find('channel')
            if channel is not None:
                self.xml_structure['channel'] = {
                    'title': self._get_text(channel.find('title')),
                    'link': self._get_text(channel.find('link')),
                    'description': self._get_text(channel.find('description'))
                }
                
                # Extract items (posts/pages)
                items = channel.findall('item')
                for item in items:
                    item_data = self._analyze_xml_item(item)
                    self.xml_structure['items'].append(item_data)
                    
                # Extract categories, tags, terms
                for category in channel.findall('.//{http://wordpress.org/export/1.2/}category'):
                    cat_data = {
                        'term_id': self._get_text(category.find('.//{http://wordpress.org/export/1.2/}term_id')),
                        'name': self._get_text(category.find('.//{http://wordpress.org/export/1.2/}cat_name')),
                        'nicename': self._get_text(category.find('.//{http://wordpress.org/export/1.2/}category_nicename'))
                    }
                    self.xml_structure['categories'].append(cat_data)
                
        except Exception as e:
            print(f"Error analyzing XML: {e}")
    
    def _analyze_xml_item(self, item) -> Dict[str, Any]:
        """Analyze a single XML item (post/page)"""
        item_data = {
            'title': self._get_text(item.find('title')),
            'link': self._get_text(item.find('link')),
            'post_id': self._get_text(item.find('.//{http://wordpress.org/export/1.2/}post_id')),
            'post_type': self._get_text(item.find('.//{http://wordpress.org/export/1.2/}post_type')),
            'status': self._get_text(item.find('.//{http://wordpress.org/export/1.2/}status')),
            'content': self._get_text(item.find('.//{http://purl.org/rss/1.0/modules/content/}encoded')),
            'meta_data': {},
            'elementor_data': None
        }
        
        # Extract post meta
        for meta in item.findall('.//{http://wordpress.org/export/1.2/}postmeta'):
            key = self._get_text(meta.find('.//{http://wordpress.org/export/1.2/}meta_key'))
            value = self._get_text(meta.find('.//{http://wordpress.org/export/1.2/}meta_value'))
            item_data['meta_data'][key] = value
            
            # Special handling for Elementor data
            if key == '_elementor_data':
                try:
                    item_data['elementor_data'] = json.loads(value) if value else None
                except:
                    item_data['elementor_data'] = value
        
        return item_data
    
    def _get_text(self, element) -> str:
        """Safely get text from XML element"""
        return element.text if element is not None else ''
    
    def load_all_templates(self):
        """Load and analyze all template files"""
        print("Loading JSON templates...")
        
        if not self.templates_dir.exists():
            print(f"Templates directory not found: {self.templates_dir}")
            return
        
        for file_path in self.templates_dir.glob("*.json"):
            template_info = self.analyze_json_template(file_path)
            if template_info:
                self.templates[file_path.stem] = template_info
        
        print(f"Loaded {len(self.templates)} templates")
    
    def load_all_blocks(self):
        """Load and analyze all Elementor block files"""
        print("Loading Elementor blocks...")
        
        if not self.blocks_dir.exists():
            print(f"Blocks directory not found: {self.blocks_dir}")
            return
        
        for file_path in self.blocks_dir.glob("*.json"):
            block_info = self.analyze_elementor_block(file_path)
            if block_info:
                self.blocks[file_path.stem] = block_info
        
        print(f"Loaded {len(self.blocks)} blocks")
    
    def create_mapping_configuration(self):
        """Create a comprehensive mapping configuration"""
        print("Creating mapping configuration...")
        
        # Collect all unique widget types
        all_widgets = set()
        for template in self.templates.values():
            all_widgets.update(template.get('widget_types', []))
        for block in self.blocks.values():
            all_widgets.update(block.get('widget_types', []))
        
        # Create mapping structure
        self.mapping_config = {
            'metadata': {
                'generated_at': '2025-08-28',
                'source': 'Cholot Theme Analysis',
                'total_templates': len(self.templates),
                'total_blocks': len(self.blocks),
                'total_widgets': len(all_widgets),
                'xml_items_analyzed': len(self.xml_structure.get('items', []))
            },
            'templates': {
                name: {
                    'file': template['file_name'],
                    'sections': len(template.get('sections', [])),
                    'widgets': template.get('widget_types', []),
                    'elements': template.get('total_elements', 0),
                    'type': 'complete_page'
                }
                for name, template in self.templates.items()
            },
            'blocks': {
                name: {
                    'file': block['file_name'],
                    'title': block.get('title', 'Unknown'),
                    'type': block.get('type', 'section'),
                    'widgets': block.get('widget_types', []),
                    'elements': block.get('total_elements', 0),
                    'reusable_component': True
                }
                for name, block in self.blocks.items()
            },
            'widgets': {
                widget_type: {
                    'instances': len(instances),
                    'settings_patterns': self._analyze_widget_settings(instances),
                    'used_in_templates': [name for name, template in self.templates.items() 
                                        if widget_type in template.get('widget_types', [])],
                    'used_in_blocks': [name for name, block in self.blocks.items() 
                                     if widget_type in block.get('widget_types', [])]
                }
                for widget_type, instances in self.widget_analysis.items()
            },
            'xml_mapping': {
                'pages': [item for item in self.xml_structure.get('items', []) 
                         if item.get('post_type') == 'page'],
                'posts': [item for item in self.xml_structure.get('items', []) 
                         if item.get('post_type') == 'post'],
                'elementor_pages': [item for item in self.xml_structure.get('items', []) 
                                  if item.get('elementor_data') is not None]
            },
            'reconstruction_plan': self._create_reconstruction_plan()
        }
    
    def _analyze_widget_settings(self, instances: List[Dict]) -> Dict[str, Any]:
        """Analyze common settings patterns for a widget type"""
        if not instances:
            return {}
        
        all_settings_keys = set()
        common_settings = {}
        
        for instance in instances:
            settings = instance.get('settings', {})
            all_settings_keys.update(settings.keys())
        
        # Find most common settings patterns
        for key in all_settings_keys:
            values = []
            for instance in instances:
                settings = instance.get('settings', {})
                if key in settings:
                    values.append(settings[key])
            
            if len(values) > 0:
                common_settings[key] = {
                    'frequency': len(values),
                    'unique_values': len(set(str(v) for v in values)),
                    'sample_value': values[0] if values else None
                }
        
        return {
            'total_settings_keys': len(all_settings_keys),
            'common_settings': common_settings
        }
    
    def _create_reconstruction_plan(self) -> Dict[str, Any]:
        """Create a plan for reconstructing the Cholot theme"""
        return {
            'step_1_base_setup': {
                'description': 'Setup WordPress with Elementor and required plugins',
                'requirements': ['elementor', 'cholot-theme-widgets'],
                'action': 'install_base_requirements'
            },
            'step_2_import_media': {
                'description': 'Import all media files and attachments',
                'media_count': len([item for item in self.xml_structure.get('items', []) 
                                  if item.get('post_type') == 'attachment']),
                'action': 'import_media_files'
            },
            'step_3_create_templates': {
                'description': 'Create Elementor templates from JSON files',
                'templates': list(self.templates.keys()),
                'action': 'convert_json_to_elementor'
            },
            'step_4_create_blocks': {
                'description': 'Create reusable Elementor blocks',
                'blocks': list(self.blocks.keys()),
                'action': 'create_elementor_blocks'
            },
            'step_5_setup_pages': {
                'description': 'Create WordPress pages with Elementor layouts',
                'pages': [item for item in self.xml_structure.get('items', []) 
                         if item.get('post_type') == 'page'],
                'action': 'create_wordpress_pages'
            },
            'step_6_configure_settings': {
                'description': 'Configure theme settings and customizations',
                'action': 'apply_theme_settings'
            }
        }
    
    def generate_yaml_config(self, output_path: str = None):
        """Generate a YAML configuration file"""
        if output_path is None:
            output_path = self.base_path / "cholot_reconstruction_config.yaml"
        
        print(f"Generating YAML configuration: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.mapping_config, f, default_flow_style=False, 
                     allow_unicode=True, indent=2, sort_keys=False)
        
        print(f"Configuration saved to: {output_path}")
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        report = []
        report.append("# Cholot Theme Structure Analysis Report")
        report.append(f"Generated: 2025-08-28")
        report.append("")
        
        # Templates Analysis
        report.append("## Templates Analysis")
        report.append(f"Total templates found: {len(self.templates)}")
        report.append("")
        
        for name, template in self.templates.items():
            report.append(f"### {name}")
            report.append(f"- File: {template['file_name']}")
            report.append(f"- Sections: {len(template.get('sections', []))}")
            report.append(f"- Total elements: {template.get('total_elements', 0)}")
            report.append(f"- Widget types: {', '.join(template.get('widget_types', []))}")
            report.append("")
        
        # Blocks Analysis
        report.append("## Elementor Blocks Analysis")
        report.append(f"Total blocks found: {len(self.blocks)}")
        report.append("")
        
        for name, block in self.blocks.items():
            report.append(f"### {name}")
            report.append(f"- Title: {block.get('title', 'Unknown')}")
            report.append(f"- Type: {block.get('type', 'section')}")
            report.append(f"- Elements: {block.get('total_elements', 0)}")
            report.append(f"- Widget types: {', '.join(block.get('widget_types', []))}")
            report.append("")
        
        # Widget Analysis
        report.append("## Widget Types Analysis")
        report.append(f"Total unique widget types: {len(self.widget_analysis)}")
        report.append("")
        
        for widget_type, instances in self.widget_analysis.items():
            report.append(f"### {widget_type}")
            report.append(f"- Instances: {len(instances)}")
            
            # Find templates/blocks using this widget
            used_in_templates = [name for name, template in self.templates.items() 
                               if widget_type in template.get('widget_types', [])]
            used_in_blocks = [name for name, block in self.blocks.items() 
                            if widget_type in block.get('widget_types', [])]
            
            if used_in_templates:
                report.append(f"- Used in templates: {', '.join(used_in_templates)}")
            if used_in_blocks:
                report.append(f"- Used in blocks: {', '.join(used_in_blocks)}")
            report.append("")
        
        # XML Analysis
        report.append("## XML Structure Analysis")
        total_items = len(self.xml_structure.get('items', []))
        pages = [item for item in self.xml_structure.get('items', []) if item.get('post_type') == 'page']
        posts = [item for item in self.xml_structure.get('items', []) if item.get('post_type') == 'post']
        attachments = [item for item in self.xml_structure.get('items', []) if item.get('post_type') == 'attachment']
        elementor_items = [item for item in self.xml_structure.get('items', []) if item.get('elementor_data')]
        
        report.append(f"- Total items: {total_items}")
        report.append(f"- Pages: {len(pages)}")
        report.append(f"- Posts: {len(posts)}")
        report.append(f"- Attachments: {len(attachments)}")
        report.append(f"- Items with Elementor data: {len(elementor_items)}")
        report.append("")
        
        # Reconstruction Strategy
        report.append("## Reconstruction Strategy")
        report.append("")
        
        plan = self.mapping_config.get('reconstruction_plan', {})
        for step_key, step_info in plan.items():
            step_num = step_key.replace('step_', '').replace('_', ' ').title()
            report.append(f"### {step_num}")
            report.append(f"**Description:** {step_info.get('description', '')}")
            report.append(f"**Action:** {step_info.get('action', '')}")
            
            if 'requirements' in step_info:
                report.append(f"**Requirements:** {', '.join(step_info['requirements'])}")
            if 'templates' in step_info:
                report.append(f"**Templates:** {len(step_info['templates'])} files")
            if 'blocks' in step_info:
                report.append(f"**Blocks:** {len(step_info['blocks'])} components")
            if 'pages' in step_info:
                report.append(f"**Pages:** {len(step_info['pages'])} pages")
            if 'media_count' in step_info:
                report.append(f"**Media files:** {step_info['media_count']} files")
            
            report.append("")
        
        return "\n".join(report)
    
    def run_full_analysis(self):
        """Run the complete analysis process"""
        print("Starting Cholot Theme Analysis...")
        print("="*50)
        
        # Load all data
        self.load_all_templates()
        self.load_all_blocks()
        self.analyze_xml_structure()
        
        # Create mapping
        self.create_mapping_configuration()
        
        # Generate outputs
        self.generate_yaml_config()
        
        # Generate and save report
        report = self.generate_report()
        report_path = self.base_path / "cholot_analysis_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Analysis complete!")
        print(f"Report saved to: {report_path}")
        print(f"Configuration saved to: {self.base_path}/cholot_reconstruction_config.yaml")
        
        return {
            'templates': self.templates,
            'blocks': self.blocks,
            'xml_structure': self.xml_structure,
            'mapping_config': self.mapping_config,
            'widget_analysis': dict(self.widget_analysis)
        }

def main():
    """Main function to run the analyzer"""
    base_path = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress"
    
    analyzer = CholotAnalyzer(base_path)
    results = analyzer.run_full_analysis()
    
    print("\nSummary:")
    print(f"- Templates analyzed: {len(results['templates'])}")
    print(f"- Blocks analyzed: {len(results['blocks'])}")
    print(f"- XML items processed: {len(results['xml_structure'].get('items', []))}")
    print(f"- Unique widgets found: {len(results['widget_analysis'])}")

if __name__ == "__main__":
    main()