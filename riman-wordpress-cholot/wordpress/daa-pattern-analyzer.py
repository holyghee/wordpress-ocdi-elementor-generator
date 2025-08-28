#!/usr/bin/env python3
"""
DAA Pattern Analysis System for Elementor Widgets
Distributed Agent Architecture for comprehensive widget pattern extraction
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import defaultdict, Counter
from datetime import datetime
import re

class WidgetPatternAnalyzer:
    """Agent 1: Extract and analyze widget patterns across templates"""
    
    def __init__(self):
        self.widget_instances = defaultdict(list)
        self.parameter_variations = defaultdict(lambda: defaultdict(set))
        self.parameter_frequencies = defaultdict(Counter)
        self.golden_patterns = {}
        
    def load_template(self, filepath: str) -> Dict[str, Any]:
        """Load JSON template file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_widgets(self, data: Any, parent_type: str = None, depth: int = 0) -> None:
        """Recursively extract widget instances from nested structures"""
        if isinstance(data, dict):
            widget_type = data.get('widgetType')
            if widget_type:
                # Capture widget instance with context
                instance = {
                    'type': widget_type,
                    'parent': parent_type,
                    'depth': depth,
                    'settings': data.get('settings', {}),
                    'elements': data.get('elements', [])
                }
                self.widget_instances[widget_type].append(instance)
                
                # Track parameter usage
                for param, value in instance['settings'].items():
                    self.parameter_frequencies[widget_type][param] += 1
                    if isinstance(value, (str, int, float, bool)):
                        self.parameter_variations[widget_type][param].add(str(value))
            
            # Process nested elements
            for key, value in data.items():
                if key == 'elements' and isinstance(value, list):
                    for element in value:
                        self.extract_widgets(element, widget_type, depth + 1)
                elif isinstance(value, (dict, list)):
                    self.extract_widgets(value, parent_type, depth)
                    
        elif isinstance(data, list):
            for item in data:
                self.extract_widgets(item, parent_type, depth)
    
    def identify_core_parameters(self, widget_type: str) -> Dict[str, Any]:
        """Identify core vs optional parameters for a widget type"""
        instances = self.widget_instances[widget_type]
        if not instances:
            return {}
        
        total_instances = len(instances)
        core_params = {}
        optional_params = {}
        
        for param, count in self.parameter_frequencies[widget_type].items():
            usage_ratio = count / total_instances
            variations = self.parameter_variations[widget_type][param]
            
            param_info = {
                'usage_ratio': usage_ratio,
                'occurrence_count': count,
                'unique_values': len(variations),
                'common_values': list(variations)[:5] if variations else []
            }
            
            if usage_ratio >= 0.8:  # Present in 80% or more instances
                core_params[param] = param_info
            else:
                optional_params[param] = param_info
        
        return {
            'core': core_params,
            'optional': optional_params,
            'total_instances': total_instances
        }
    
    def find_golden_patterns(self) -> Dict[str, Any]:
        """Find the most common parameter combinations for each widget"""
        for widget_type, instances in self.widget_instances.items():
            if not instances:
                continue
            
            # Group similar parameter sets
            param_combinations = Counter()
            for instance in instances:
                # Create a hashable representation of parameters
                params = instance['settings']
                param_set = tuple(sorted(params.keys()))
                param_combinations[param_set] += 1
            
            # Find most common combination
            if param_combinations:
                golden_set = param_combinations.most_common(1)[0][0]
                
                # Extract typical values for golden parameters
                golden_values = {}
                for param in golden_set:
                    values = []
                    for instance in instances:
                        if param in instance['settings']:
                            values.append(instance['settings'][param])
                    
                    # Find most common value
                    if values:
                        value_counter = Counter(str(v) for v in values)
                        most_common = value_counter.most_common(1)[0][0]
                        golden_values[param] = most_common
                
                self.golden_patterns[widget_type] = {
                    'parameters': list(golden_set),
                    'typical_values': golden_values,
                    'frequency': param_combinations[golden_set]
                }
        
        return self.golden_patterns


class RelationshipDetective:
    """Agent 2: Detect relationships and dependencies between parameters"""
    
    def __init__(self):
        self.dependencies = defaultdict(lambda: defaultdict(list))
        self.inheritance_patterns = {}
        self.responsive_patterns = defaultdict(dict)
        self.nesting_rules = defaultdict(set)
        
    def analyze_dependencies(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Map parameter dependencies within widget instances"""
        dependencies = {}
        
        for widget_type, widget_instances in instances.items():
            widget_deps = []
            
            for instance in widget_instances:
                settings = instance['settings']
                
                # Check for conditional parameters
                if 'layout' in settings:
                    layout = settings['layout']
                    related_params = []
                    
                    if layout == 'icon-left' or layout == 'icon-right':
                        if 'icon_spacing' in settings:
                            related_params.append('icon_spacing')
                    
                    if related_params:
                        widget_deps.append({
                            'condition': f'layout={layout}',
                            'requires': related_params
                        })
                
                # Check for size dependencies
                if 'size' in settings and 'custom_size' in settings:
                    if settings['size'] == 'custom':
                        widget_deps.append({
                            'condition': 'size=custom',
                            'requires': ['custom_size']
                        })
            
            if widget_deps:
                dependencies[widget_type] = widget_deps
        
        return dependencies
    
    def detect_responsive_patterns(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Find responsive breakpoint patterns (_tablet, _mobile suffixes)"""
        responsive_params = defaultdict(lambda: {'desktop': [], 'tablet': [], 'mobile': []})
        
        for widget_type, widget_instances in instances.items():
            for instance in widget_instances:
                settings = instance['settings']
                
                for param, value in settings.items():
                    if '_tablet' in param:
                        base_param = param.replace('_tablet', '')
                        responsive_params[widget_type]['tablet'].append(base_param)
                    elif '_mobile' in param:
                        base_param = param.replace('_mobile', '')
                        responsive_params[widget_type]['mobile'].append(base_param)
                    elif not any(suffix in param for suffix in ['_tablet', '_mobile']):
                        responsive_params[widget_type]['desktop'].append(param)
        
        # Clean up and deduplicate
        for widget_type in responsive_params:
            for device in ['desktop', 'tablet', 'mobile']:
                responsive_params[widget_type][device] = list(set(responsive_params[widget_type][device]))
        
        return dict(responsive_params)
    
    def map_nesting_hierarchy(self, data: Any, parent_stack: List[str] = None) -> Dict[str, Set]:
        """Map widget nesting rules and hierarchies"""
        if parent_stack is None:
            parent_stack = []
        
        nesting_map = defaultdict(set)
        
        if isinstance(data, dict):
            widget_type = data.get('widgetType')
            if widget_type:
                if parent_stack:
                    parent = parent_stack[-1]
                    nesting_map[parent].add(widget_type)
                
                # Process children
                elements = data.get('elements', [])
                if elements:
                    new_stack = parent_stack + [widget_type]
                    for element in elements:
                        child_map = self.map_nesting_hierarchy(element, new_stack)
                        for parent, children in child_map.items():
                            nesting_map[parent].update(children)
            
            # Process other nested structures
            for key, value in data.items():
                if key != 'elements' and isinstance(value, (dict, list)):
                    child_map = self.map_nesting_hierarchy(value, parent_stack)
                    for parent, children in child_map.items():
                        nesting_map[parent].update(children)
        
        elif isinstance(data, list):
            for item in data:
                child_map = self.map_nesting_hierarchy(item, parent_stack)
                for parent, children in child_map.items():
                    nesting_map[parent].update(children)
        
        return nesting_map
    
    def identify_inheritance(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Identify settings inherited from parent sections"""
        inheritance_patterns = {}
        
        for widget_type, widget_instances in instances.items():
            inherited_settings = set()
            
            for instance in widget_instances:
                if instance.get('parent'):
                    parent_type = instance['parent']
                    
                    # Common inherited settings from sections/containers
                    if parent_type in ['section', 'container', 'column']:
                        potential_inherited = [
                            'padding', 'margin', 'background_color',
                            'background_image', 'border_width', 'border_color'
                        ]
                        
                        for setting in potential_inherited:
                            if setting not in instance['settings']:
                                inherited_settings.add(setting)
            
            if inherited_settings:
                inheritance_patterns[widget_type] = list(inherited_settings)
        
        return inheritance_patterns


class ContentZoneMapper:
    """Agent 3: Map content injection zones and dynamic content areas"""
    
    def __init__(self):
        self.text_zones = defaultdict(list)
        self.media_zones = defaultdict(list)
        self.dynamic_zones = defaultdict(list)
        self.seo_fields = defaultdict(list)
        
    def identify_content_fields(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Identify all text content fields across widgets"""
        content_fields = defaultdict(lambda: {
            'plain_text': [],
            'rich_text': [],
            'translatable': [],
            'dynamic': []
        })
        
        for widget_type, widget_instances in instances.items():
            for instance in widget_instances:
                settings = instance['settings']
                
                for param, value in settings.items():
                    # Text content detection
                    if any(keyword in param.lower() for keyword in ['text', 'title', 'description', 'content', 'label']):
                        if isinstance(value, str):
                            if '<' in str(value) and '>' in str(value):
                                content_fields[widget_type]['rich_text'].append(param)
                            else:
                                content_fields[widget_type]['plain_text'].append(param)
                            
                            # All text fields are potentially translatable
                            content_fields[widget_type]['translatable'].append(param)
                    
                    # Dynamic content detection
                    if isinstance(value, dict) and 'dynamic' in value:
                        content_fields[widget_type]['dynamic'].append(param)
        
        # Deduplicate
        for widget_type in content_fields:
            for field_type in content_fields[widget_type]:
                content_fields[widget_type][field_type] = list(set(content_fields[widget_type][field_type]))
        
        return dict(content_fields)
    
    def map_media_placeholders(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Find image and media placeholder zones"""
        media_zones = defaultdict(list)
        
        media_keywords = ['image', 'video', 'media', 'icon', 'logo', 'gallery', 'background']
        
        for widget_type, widget_instances in instances.items():
            media_params = set()
            
            for instance in widget_instances:
                settings = instance['settings']
                
                for param, value in settings.items():
                    if any(keyword in param.lower() for keyword in media_keywords):
                        media_params.add(param)
                    
                    # Check for URL patterns indicating media
                    if isinstance(value, dict):
                        if 'url' in value or 'id' in value:
                            media_params.add(param)
            
            if media_params:
                media_zones[widget_type] = list(media_params)
        
        return dict(media_zones)
    
    def identify_seo_fields(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Identify SEO-relevant fields"""
        seo_fields = defaultdict(list)
        
        seo_keywords = ['alt', 'meta', 'seo', 'description', 'title', 'heading', 'h1', 'h2', 'h3']
        
        for widget_type, widget_instances in instances.items():
            seo_params = set()
            
            for instance in widget_instances:
                settings = instance['settings']
                
                for param, value in settings.items():
                    if any(keyword in param.lower() for keyword in seo_keywords):
                        seo_params.add(param)
                    
                    # Check for heading tags
                    if param == 'header_size' or param == 'title_size':
                        seo_params.add(param)
            
            if seo_params:
                seo_fields[widget_type] = list(seo_params)
        
        return dict(seo_fields)
    
    def map_injection_points(self, instances: Dict[str, List]) -> Dict[str, Any]:
        """Map dynamic content injection points"""
        injection_points = defaultdict(lambda: {
            'shortcodes': [],
            'dynamic_tags': [],
            'custom_fields': [],
            'api_endpoints': []
        })
        
        for widget_type, widget_instances in instances.items():
            for instance in widget_instances:
                settings = instance['settings']
                
                for param, value in settings.items():
                    # Check for shortcode patterns
                    if isinstance(value, str) and '[' in value and ']' in value:
                        injection_points[widget_type]['shortcodes'].append(param)
                    
                    # Check for dynamic tag patterns
                    if isinstance(value, dict):
                        if 'dynamic' in value or '__dynamic__' in str(value):
                            injection_points[widget_type]['dynamic_tags'].append(param)
                    
                    # Check for custom field references
                    if 'custom' in param.lower() or 'field' in param.lower():
                        injection_points[widget_type]['custom_fields'].append(param)
        
        # Deduplicate
        for widget_type in injection_points:
            for point_type in injection_points[widget_type]:
                injection_points[widget_type][point_type] = list(set(injection_points[widget_type][point_type]))
        
        return dict(injection_points)


class DAAPatternOrchestrator:
    """Main orchestrator for coordinating all DAA agents"""
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.analyzer = WidgetPatternAnalyzer()
        self.detective = RelationshipDetective()
        self.mapper = ContentZoneMapper()
        self.validation_results = {}
        
    def load_catalog(self, catalog_path: str) -> Dict[str, Any]:
        """Load widget catalog for validation"""
        with open(catalog_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def process_templates(self) -> None:
        """Process all template files"""
        template_files = [
            'home-page.json',
            'about-page.json',
            'service-page.json',
            'contact-page.json',
            'blog-page.json',
            'single-service-1.json',
            'single-service-2.json'
        ]
        
        for template_file in template_files:
            filepath = self.template_dir / template_file
            if filepath.exists():
                print(f"Processing: {template_file}")
                data = self.analyzer.load_template(str(filepath))
                self.analyzer.extract_widgets(data)
    
    def validate_patterns(self, catalog: Dict[str, Any]) -> Dict[str, Any]:
        """Validate patterns against catalog definitions"""
        validation_results = {}
        
        for widget_type in self.analyzer.widget_instances:
            if widget_type in catalog:
                catalog_def = catalog[widget_type]
                instances = self.analyzer.widget_instances[widget_type]
                
                # Validate each instance
                valid_count = 0
                invalid_params = set()
                
                for instance in instances:
                    settings = instance['settings']
                    catalog_params = catalog_def.get('properties', {})
                    
                    for param in settings:
                        if param not in catalog_params and not param.endswith(('_tablet', '_mobile')):
                            invalid_params.add(param)
                        else:
                            valid_count += 1
                
                validation_results[widget_type] = {
                    'total_instances': len(instances),
                    'validation_rate': valid_count / max(len(instances), 1),
                    'invalid_parameters': list(invalid_params)
                }
        
        return validation_results
    
    def generate_reports(self) -> None:
        """Generate all analysis reports and deliverables"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Widget Pattern Library
        pattern_library = {
            'generated': timestamp,
            'total_widgets': len(self.analyzer.widget_instances),
            'patterns': {}
        }
        
        for widget_type in self.analyzer.widget_instances:
            core_params = self.analyzer.identify_core_parameters(widget_type)
            pattern_library['patterns'][widget_type] = {
                'instances': len(self.analyzer.widget_instances[widget_type]),
                'core_parameters': core_params.get('core', {}),
                'optional_parameters': core_params.get('optional', {}),
                'golden_pattern': self.analyzer.golden_patterns.get(widget_type, {})
            }
        
        with open('widget_pattern_library.json', 'w', encoding='utf-8') as f:
            json.dump(pattern_library, f, indent=2, default=str)
        
        # 2. Relationship and Dependency Graph
        relationships = {
            'generated': timestamp,
            'dependencies': self.detective.analyze_dependencies(self.analyzer.widget_instances),
            'responsive_patterns': self.detective.detect_responsive_patterns(self.analyzer.widget_instances),
            'nesting_rules': {k: list(v) for k, v in self.detective.map_nesting_hierarchy(self.analyzer.widget_instances).items()},
            'inheritance': self.detective.identify_inheritance(self.analyzer.widget_instances)
        }
        
        with open('parameter_dependency_graph.json', 'w', encoding='utf-8') as f:
            json.dump(relationships, f, indent=2, default=str)
        
        # 3. Content Injection Zones
        content_zones = {
            'generated': timestamp,
            'text_fields': self.mapper.identify_content_fields(self.analyzer.widget_instances),
            'media_zones': self.mapper.map_media_placeholders(self.analyzer.widget_instances),
            'seo_fields': self.mapper.identify_seo_fields(self.analyzer.widget_instances),
            'injection_points': self.mapper.map_injection_points(self.analyzer.widget_instances)
        }
        
        with open('content_injection_zones.json', 'w', encoding='utf-8') as f:
            json.dump(content_zones, f, indent=2, default=str)
        
        # 4. Pattern Insights YAML
        insights = {
            'meta': {
                'generated': timestamp,
                'total_templates_analyzed': 7,
                'total_widget_types': len(self.analyzer.widget_instances),
                'total_widget_instances': sum(len(instances) for instances in self.analyzer.widget_instances.values())
            },
            'key_discoveries': {
                'most_used_widgets': sorted(
                    [(widget, len(instances)) for widget, instances in self.analyzer.widget_instances.items()],
                    key=lambda x: x[1], reverse=True
                )[:5],
                'golden_patterns_found': len(self.analyzer.golden_patterns),
                'responsive_widgets': len(self.detective.detect_responsive_patterns(self.analyzer.widget_instances)),
                'widgets_with_dependencies': len(self.detective.analyze_dependencies(self.analyzer.widget_instances))
            },
            'recommendations': {
                'generator_priorities': [
                    widget for widget, _ in sorted(
                        [(w, len(i)) for w, i in self.analyzer.widget_instances.items()],
                        key=lambda x: x[1], reverse=True
                    )[:10]
                ],
                'required_parameters': {
                    widget: list(params['core'].keys())
                    for widget, params in {
                        w: self.analyzer.identify_core_parameters(w) 
                        for w in self.analyzer.widget_instances
                    }.items()
                    if params.get('core')
                },
                'content_injection_priority': list(self.mapper.identify_content_fields(self.analyzer.widget_instances).keys())
            },
            'validation': self.validation_results
        }
        
        with open('pattern_insights.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(insights, f, default_flow_style=False, sort_keys=False)
        
        # 5. Human-readable report
        self.generate_markdown_report(pattern_library, relationships, content_zones, insights)
    
    def generate_markdown_report(self, patterns, relationships, content, insights):
        """Generate comprehensive markdown report"""
        report = f"""# DAA Pattern Analysis Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Executive Summary

Analyzed **{insights['meta']['total_templates_analyzed']} templates** containing **{insights['meta']['total_widget_instances']} widget instances** across **{insights['meta']['total_widget_types']} unique widget types**.

## Key Findings

### 1. Most Used Widgets
"""
        for widget, count in insights['key_discoveries']['most_used_widgets']:
            report += f"- **{widget}**: {count} instances\n"
        
        report += f"""

### 2. Golden Patterns Identified

Found **{insights['key_discoveries']['golden_patterns_found']} golden patterns** representing the most common parameter combinations for widgets.

### 3. Widget Hierarchy

Top-level containers that can nest other widgets:
"""
        nesting_rules = relationships.get('nesting_rules', {})
        for parent, children in list(nesting_rules.items())[:5]:
            if children:
                report += f"- **{parent}** can contain: {', '.join(children)}\n"
        
        report += """

### 4. Responsive Design Patterns

"""
        responsive_count = insights['key_discoveries']['responsive_widgets']
        report += f"Identified **{responsive_count} widgets** with responsive breakpoint parameters.\n\n"
        
        report += """### 5. Content Injection Zones

Key areas for dynamic content:
"""
        for widget, fields in list(content['text_fields'].items())[:5]:
            total_fields = len(fields.get('plain_text', [])) + len(fields.get('rich_text', []))
            if total_fields > 0:
                report += f"- **{widget}**: {total_fields} text fields\n"
        
        report += """

## Validation Results

"""
        if self.validation_results:
            valid_widgets = sum(1 for w, v in self.validation_results.items() if v['validation_rate'] >= 0.9)
            total_widgets = len(self.validation_results)
            report += f"**{valid_widgets}/{total_widgets} widget types** passed validation (90%+ parameter match with catalog).\n\n"
        
        report += """## Recommendations for Generator

### Priority Implementation Order
"""
        for i, widget in enumerate(insights['recommendations']['generator_priorities'], 1):
            report += f"{i}. {widget}\n"
        
        report += """

### Critical Parameters by Widget

"""
        for widget, params in list(insights['recommendations'].get('required_parameters', {}).items())[:10]:
            if params:
                report += f"**{widget}**:\n"
                for param in params[:5]:
                    report += f"  - {param}\n"
        
        report += """

## Pattern Groups

### Always Together Parameters
"""
        for widget_type, pattern in patterns['patterns'].items():
            golden = pattern.get('golden_pattern', {})
            if golden and golden.get('parameters'):
                report += f"\n**{widget_type}**: {', '.join(golden['parameters'][:5])}\n"
        
        with open('pattern_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
    
    def run(self):
        """Execute complete DAA pattern analysis"""
        print("🚀 Starting DAA Pattern Analysis")
        print("-" * 50)
        
        # Load catalog
        catalog_path = 'cholot_widgets_catalog.json'
        if os.path.exists(catalog_path):
            print("📚 Loading widget catalog...")
            catalog = self.load_catalog(catalog_path)
        else:
            print("⚠️ Widget catalog not found, skipping validation")
            catalog = {}
        
        # Process templates
        print("🔍 Processing templates...")
        self.process_templates()
        
        # Find golden patterns
        print("✨ Identifying golden patterns...")
        self.analyzer.find_golden_patterns()
        
        # Validate if catalog available
        if catalog:
            print("✅ Validating against catalog...")
            self.validation_results = self.validate_patterns(catalog)
        
        # Generate reports
        print("📊 Generating reports...")
        self.generate_reports()
        
        print("-" * 50)
        print("✅ Analysis complete! Generated files:")
        print("  - pattern_analysis_report.md")
        print("  - widget_pattern_library.json")
        print("  - parameter_dependency_graph.json")
        print("  - content_injection_zones.json")
        print("  - pattern_insights.yaml")


if __name__ == "__main__":
    orchestrator = DAAPatternOrchestrator()
    orchestrator.run()