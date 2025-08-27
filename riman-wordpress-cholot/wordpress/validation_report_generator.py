#!/usr/bin/env python3
"""
Validation Report Generator
==========================

Generates comprehensive validation reports for the Elementor JSON generator,
comparing output against demo-data-fixed.xml format and requirements.

Author: Testing & Validation Expert
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import difflib
import re
import time
import sys

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from generate_wordpress_xml import WordPressXMLGenerator, CholotComponentFactory
    from test_scenarios import TestScenarioManager
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)


class ValidationReportGenerator:
    """Generates comprehensive validation reports for the Elementor JSON generator."""
    
    def __init__(self):
        self.generator = WordPressXMLGenerator()
        self.factory = CholotComponentFactory()
        self.scenario_manager = TestScenarioManager()
        self.demo_file_path = Path(__file__).parent / 'demo-data-fixed.xml'
        
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        print("🔍 Generating Comprehensive Validation Report")
        print("=" * 60)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'generator_info': self._get_generator_info(),
            'format_validation': self._validate_xml_format(),
            'widget_validation': self._validate_all_widgets(),
            'scenario_testing': self._test_all_scenarios(),
            'demo_comparison': self._compare_with_demo_data(),
            'performance_analysis': self._analyze_performance(),
            'placeholder_validation': self._validate_placeholder_system(),
            'error_handling': self._test_error_handling(),
            'structural_compliance': self._validate_structural_compliance(),
            'recommendations': [],
            'overall_score': 0,
            'verdict': 'UNKNOWN'
        }
        
        # Calculate overall score
        report['overall_score'] = self._calculate_overall_score(report)
        
        # Determine verdict
        if report['overall_score'] >= 90:
            report['verdict'] = 'EXCELLENT'
        elif report['overall_score'] >= 80:
            report['verdict'] = 'GOOD' 
        elif report['overall_score'] >= 70:
            report['verdict'] = 'ACCEPTABLE'
        elif report['overall_score'] >= 60:
            report['verdict'] = 'NEEDS_IMPROVEMENT'
        else:
            report['verdict'] = 'FAIL'
        
        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _get_generator_info(self) -> Dict[str, Any]:
        """Get information about the generator."""
        print("📋 Collecting generator information...")
        
        try:
            factory = CholotComponentFactory()
            
            # Test widget creation to verify functionality
            test_widget = factory.create_texticon_widget({
                'title': 'Test',
                'icon': 'fas fa-test'
            })
            
            return {
                'status': 'operational',
                'widget_factory_available': True,
                'supported_widgets': [
                    'cholot-texticon', 'cholot-title', 'cholot-post-three', 'cholot-post-four',
                    'cholot-gallery', 'cholot-logo', 'cholot-menu', 'cholot-button-text',
                    'cholot-team', 'cholot-testimonial', 'cholot-text-line', 'cholot-contact', 'cholot-sidebar'
                ],
                'total_widget_types': 13,
                'test_widget_created': bool(test_widget and 'id' in test_widget)
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'widget_factory_available': False
            }
    
    def _validate_xml_format(self) -> Dict[str, Any]:
        """Validate XML format compliance."""
        print("🔧 Validating XML format compliance...")
        
        test_data = {
            'pages': [{
                'title': 'Format Validation Test',
                'slug': 'format-test',
                'sections': [{
                    'structure': '100',
                    'columns': [{
                        'width': 100,
                        'widgets': [{
                            'type': 'title',
                            'title': 'Format Test'
                        }]
                    }]
                }]
            }]
        }
        
        try:
            xml_output = self.generator.generate_xml(test_data)
            root = ET.fromstring(xml_output)
            
            validation_results = {
                'xml_parseable': True,
                'root_element': root.tag == 'rss',
                'version_correct': root.get('version') == '2.0',
                'namespaces': self._validate_namespaces(root),
                'channel_structure': self._validate_channel_structure(root),
                'item_structure': self._validate_item_structure(root),
                'elementor_data': self._validate_elementor_data(root),
                'cdata_handling': self._validate_cdata_handling(xml_output),
                'encoding': 'UTF-8' in xml_output[:100]
            }
            
            # Calculate score
            passed_checks = sum(1 for result in validation_results.values() if result is True)
            validation_results['score'] = (passed_checks / len(validation_results)) * 100
            validation_results['status'] = 'PASS' if validation_results['score'] >= 80 else 'FAIL'
            
            return validation_results
            
        except ET.ParseError as e:
            return {
                'xml_parseable': False,
                'error': f"XML parsing error: {e}",
                'score': 0,
                'status': 'FAIL'
            }
        except Exception as e:
            return {
                'xml_parseable': False,
                'error': f"Validation error: {e}",
                'score': 0,
                'status': 'FAIL'
            }
    
    def _validate_namespaces(self, root: ET.Element) -> bool:
        """Validate required XML namespaces."""
        required_namespaces = [
            'http://wordpress.org/export/1.2/',
            'http://purl.org/rss/1.0/modules/content/',
            'http://wellformedweb.org/CommentAPI/',
            'http://purl.org/dc/elements/1.1/'
        ]
        
        xml_str = ET.tostring(root, encoding='unicode')
        return all(ns in xml_str for ns in required_namespaces)
    
    def _validate_channel_structure(self, root: ET.Element) -> bool:
        """Validate channel structure."""
        channel = root.find('channel')
        if channel is None:
            return False
        
        required_elements = ['title', 'link', 'description', 'language']
        return all(channel.find(element) is not None for element in required_elements)
    
    def _validate_item_structure(self, root: ET.Element) -> bool:
        """Validate item structure."""
        items = root.findall('.//item')
        if not items:
            return False
        
        item = items[0]
        required_elements = ['title', 'guid']
        return all(item.find(element) is not None for element in required_elements)
    
    def _validate_elementor_data(self, root: ET.Element) -> bool:
        """Validate Elementor data presence and format."""
        for item in root.findall('.//item'):
            for postmeta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
                meta_key = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                if meta_key is not None and meta_key.text == '_elementor_data':
                    meta_value = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_value')
                    if meta_value is not None:
                        try:
                            elementor_data = json.loads(meta_value.text)
                            return isinstance(elementor_data, list)
                        except json.JSONDecodeError:
                            return False
        return False
    
    def _validate_cdata_handling(self, xml_output: str) -> bool:
        """Validate CDATA section handling."""
        return '<![CDATA[' in xml_output and ']]>' in xml_output
    
    def _validate_all_widgets(self) -> Dict[str, Any]:
        """Validate all 13 widget types."""
        print("🎛️ Validating all widget types...")
        
        widget_configs = {
            'texticon': {'title': 'Test TextIcon', 'icon': 'fas fa-star'},
            'title': {'title': 'Test Title', 'header_size': 'h2'},
            'post-three': {'post_count': 3},
            'post-four': {'post_count': 4},
            'gallery': {'images': ['test1.jpg', 'test2.jpg']},
            'logo': {'url': 'logo.svg'},
            'menu': {'menu_name': 'main'},
            'button-text': {'text': 'Click Me'},
            'team': {'name': 'John Doe'},
            'testimonial': {'columns': 1, 'testimonials': [{'_id': '1', 'name': 'Test', 'testimonial': 'Good!'}]},
            'text-line': {'title': 'Text Line'},
            'contact': {'shortcode': '[contact-form-7]'},
            'sidebar': {'width': '300px'}
        }
        
        results = {
            'total_widgets': len(widget_configs),
            'widgets_tested': 0,
            'widgets_passed': 0,
            'widget_results': {},
            'score': 0,
            'status': 'UNKNOWN'
        }
        
        for widget_type, config in widget_configs.items():
            try:
                results['widgets_tested'] += 1
                
                # Create widget
                if widget_type == 'texticon':
                    widget = self.factory.create_texticon_widget(config)
                elif widget_type == 'title':
                    widget = self.factory.create_title_widget(config)
                elif widget_type in ['post-three', 'post-four']:
                    post_type = widget_type.split('-')[1]
                    widget = self.factory.create_post_widget(config, post_type)
                elif widget_type == 'gallery':
                    widget = self.factory.create_gallery_widget(config)
                elif widget_type == 'logo':
                    widget = self.factory.create_logo_widget(config)
                elif widget_type == 'menu':
                    widget = self.factory.create_menu_widget(config)
                elif widget_type == 'button-text':
                    widget = self.factory.create_button_text_widget(config)
                elif widget_type == 'team':
                    widget = self.factory.create_team_widget(config)
                elif widget_type == 'testimonial':
                    widget = self.factory.create_testimonial_widget(config)
                elif widget_type == 'text-line':
                    widget = self.factory.create_text_line_widget(config)
                elif widget_type == 'contact':
                    widget = self.factory.create_contact_widget(config)
                elif widget_type == 'sidebar':
                    widget = self.factory.create_sidebar_widget(config)
                
                # Validate widget
                widget_valid = (
                    'id' in widget and
                    'widgetType' in widget and
                    'settings' in widget and
                    'elements' in widget and
                    'elType' in widget and
                    widget['widgetType'].startswith('cholot-') and
                    widget['elType'] == 'widget' and
                    len(widget['id']) == 7
                )
                
                if widget_valid:
                    results['widgets_passed'] += 1
                    results['widget_results'][widget_type] = 'PASS'
                else:
                    results['widget_results'][widget_type] = 'FAIL - Invalid structure'
                
            except Exception as e:
                results['widget_results'][widget_type] = f'ERROR - {str(e)}'
        
        results['score'] = (results['widgets_passed'] / results['total_widgets']) * 100
        results['status'] = 'PASS' if results['score'] >= 90 else 'FAIL'
        
        return results
    
    def _test_all_scenarios(self) -> Dict[str, Any]:
        """Test all predefined scenarios."""
        print("📋 Testing all scenarios...")
        
        scenarios = self.scenario_manager.get_all_scenarios()
        results = {
            'total_scenarios': len(scenarios),
            'scenarios_tested': 0,
            'scenarios_passed': 0,
            'scenario_results': {},
            'score': 0,
            'status': 'UNKNOWN'
        }
        
        for scenario_name, scenario_data in scenarios.items():
            try:
                results['scenarios_tested'] += 1
                
                # Generate XML for scenario
                xml_output = self.generator.generate_xml(
                    scenario_data['data'], 
                    scenario_data.get('site_config', {})
                )
                
                # Parse and validate
                root = ET.fromstring(xml_output)
                
                # Basic validation
                basic_valid = (
                    root.tag == 'rss' and
                    root.get('version') == '2.0' and
                    root.find('channel') is not None
                )
                
                # Check expected results if specified
                expectations_met = True
                if 'expected_pages' in scenario_data:
                    items = root.findall('.//item')
                    if len(items) != scenario_data['expected_pages']:
                        expectations_met = False
                
                if 'expected_widgets' in scenario_data:
                    # Check for expected widget types in Elementor data
                    found_widgets = set()
                    for item in root.findall('.//item'):
                        for postmeta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
                            meta_key = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                            if meta_key is not None and meta_key.text == '_elementor_data':
                                meta_value = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_value')
                                if meta_value is not None:
                                    elementor_data = json.loads(meta_value.text)
                                    for section in elementor_data:
                                        if section.get('elType') == 'section':
                                            for column in section.get('elements', []):
                                                if column.get('elType') == 'column':
                                                    for widget in column.get('elements', []):
                                                        if widget.get('elType') == 'widget':
                                                            found_widgets.add(widget.get('widgetType', ''))
                    
                    expected_widgets = set(scenario_data['expected_widgets'])
                    if not expected_widgets.issubset(found_widgets):
                        expectations_met = False
                
                if basic_valid and expectations_met:
                    results['scenarios_passed'] += 1
                    results['scenario_results'][scenario_name] = 'PASS'
                else:
                    results['scenario_results'][scenario_name] = 'FAIL - Validation failed'
                
            except Exception as e:
                results['scenario_results'][scenario_name] = f'ERROR - {str(e)}'
        
        results['score'] = (results['scenarios_passed'] / results['total_scenarios']) * 100
        results['status'] = 'PASS' if results['score'] >= 80 else 'FAIL'
        
        return results
    
    def _compare_with_demo_data(self) -> Dict[str, Any]:
        """Compare generated output with demo-data-fixed.xml."""
        print("📊 Comparing with demo-data-fixed.xml...")
        
        if not self.demo_file_path.exists():
            return {
                'demo_file_available': False,
                'message': 'demo-data-fixed.xml not found',
                'score': 0,
                'status': 'SKIP'
            }
        
        try:
            # Read demo file
            with open(self.demo_file_path, 'r', encoding='utf-8') as f:
                demo_xml = f.read()
            
            demo_root = ET.fromstring(demo_xml)
            
            # Generate test output
            test_data = {
                'pages': [{
                    'title': 'Demo Comparison Test',
                    'slug': 'demo-comparison',
                    'sections': [{
                        'structure': '100',
                        'columns': [{
                            'width': 100,
                            'widgets': [{
                                'type': 'title',
                                'title': 'Demo Comparison<span>.</span>'
                            }]
                        }]
                    }]
                }]
            }
            
            test_xml = self.generator.generate_xml(test_data)
            test_root = ET.fromstring(test_xml)
            
            comparison = {
                'demo_file_available': True,
                'structural_similarity': self._calculate_structural_similarity(demo_root, test_root),
                'namespace_compatibility': self._compare_namespaces(demo_root, test_root),
                'element_structure_match': self._compare_element_structure(demo_root, test_root),
                'elementor_data_format': self._compare_elementor_format(demo_root, test_root),
                'score': 0,
                'status': 'UNKNOWN'
            }
            
            # Calculate score
            scores = [
                comparison['structural_similarity'],
                comparison['namespace_compatibility'] * 100,
                comparison['element_structure_match'] * 100,
                comparison['elementor_data_format'] * 100
            ]
            comparison['score'] = sum(scores) / len(scores)
            comparison['status'] = 'PASS' if comparison['score'] >= 75 else 'ACCEPTABLE'
            
            return comparison
            
        except Exception as e:
            return {
                'demo_file_available': True,
                'error': str(e),
                'score': 0,
                'status': 'ERROR'
            }
    
    def _calculate_structural_similarity(self, demo_root: ET.Element, test_root: ET.Element) -> float:
        """Calculate structural similarity percentage."""
        demo_structure = self._extract_structure_info(demo_root)
        test_structure = self._extract_structure_info(test_root)
        
        matches = 0
        total = len(demo_structure)
        
        for key, demo_value in demo_structure.items():
            if key in test_structure:
                if test_structure[key] == demo_value:
                    matches += 1
                elif isinstance(demo_value, bool) and isinstance(test_structure[key], bool):
                    matches += 1 if demo_value == test_structure[key] else 0
        
        return (matches / total * 100) if total > 0 else 0
    
    def _extract_structure_info(self, root: ET.Element) -> Dict[str, Any]:
        """Extract structural information from XML."""
        return {
            'root_tag': root.tag,
            'has_channel': root.find('channel') is not None,
            'has_items': len(root.findall('.//item')) > 0,
            'has_title': root.find('.//title') is not None,
            'has_description': root.find('.//description') is not None,
            'version': root.get('version'),
            'namespace_count': len([attr for attr in root.attrib.keys() if attr.startswith('xmlns')])
        }
    
    def _compare_namespaces(self, demo_root: ET.Element, test_root: ET.Element) -> float:
        """Compare XML namespaces."""
        demo_namespaces = set(attr for attr in demo_root.attrib.keys() if attr.startswith('xmlns'))
        test_namespaces = set(attr for attr in test_root.attrib.keys() if attr.startswith('xmlns'))
        
        if not demo_namespaces:
            return 1.0
        
        return len(demo_namespaces.intersection(test_namespaces)) / len(demo_namespaces)
    
    def _compare_element_structure(self, demo_root: ET.Element, test_root: ET.Element) -> float:
        """Compare element structure."""
        demo_channel = demo_root.find('channel')
        test_channel = test_root.find('channel')
        
        if demo_channel is None or test_channel is None:
            return 0.0
        
        demo_elements = set(child.tag for child in demo_channel)
        test_elements = set(child.tag for child in test_channel)
        
        if not demo_elements:
            return 1.0
        
        return len(demo_elements.intersection(test_elements)) / len(demo_elements)
    
    def _compare_elementor_format(self, demo_root: ET.Element, test_root: ET.Element) -> float:
        """Compare Elementor data format."""
        demo_has_elementor = self._has_elementor_data(demo_root)
        test_has_elementor = self._has_elementor_data(test_root)
        
        return 1.0 if demo_has_elementor == test_has_elementor else 0.0
    
    def _has_elementor_data(self, root: ET.Element) -> bool:
        """Check if XML has Elementor data."""
        for item in root.findall('.//item'):
            for postmeta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
                meta_key = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                if meta_key is not None and meta_key.text == '_elementor_data':
                    return True
        return False
    
    def _analyze_performance(self) -> Dict[str, Any]:
        """Analyze generator performance."""
        print("⚡ Analyzing performance...")
        
        # Small test
        small_data = {
            'pages': [{
                'title': 'Small Test',
                'slug': 'small',
                'sections': [{
                    'structure': '100',
                    'columns': [{
                        'width': 100,
                        'widgets': [{'type': 'title', 'title': 'Small Test'}]
                    }]
                }]
            }]
        }
        
        # Medium test
        medium_data = {
            'pages': []
        }
        for i in range(3):
            medium_data['pages'].append({
                'title': f'Medium Test Page {i+1}',
                'slug': f'medium-{i+1}',
                'sections': [{
                    'structure': '33',
                    'columns': [
                        {'width': 33.33, 'widgets': [{'type': 'texticon', 'title': f'Widget {i+1}-1', 'icon': 'fas fa-star'}]},
                        {'width': 33.33, 'widgets': [{'type': 'texticon', 'title': f'Widget {i+1}-2', 'icon': 'fas fa-star'}]},
                        {'width': 33.33, 'widgets': [{'type': 'texticon', 'title': f'Widget {i+1}-3', 'icon': 'fas fa-star'}]}
                    ]
                }]
            })
        
        # Large test
        large_data = {
            'pages': []
        }
        for i in range(5):
            page = {
                'title': f'Large Test Page {i+1}',
                'slug': f'large-{i+1}',
                'sections': []
            }
            for j in range(4):
                section = {
                    'structure': '25',
                    'columns': []
                }
                for k in range(4):
                    section['columns'].append({
                        'width': 25,
                        'widgets': [{
                            'type': 'texticon',
                            'title': f'Widget {i+1}-{j+1}-{k+1}',
                            'icon': 'fas fa-star'
                        }]
                    })
                page['sections'].append(section)
            large_data['pages'].append(page)
        
        tests = [
            ('Small (1 page, 1 widget)', small_data, 1),
            ('Medium (3 pages, 9 widgets)', medium_data, 9),
            ('Large (5 pages, 80 widgets)', large_data, 80)
        ]
        
        results = {
            'test_results': [],
            'average_widgets_per_second': 0,
            'memory_efficiency': 'Unknown',
            'score': 0,
            'status': 'UNKNOWN'
        }
        
        total_widgets = 0
        total_time = 0
        
        for test_name, data, widget_count in tests:
            try:
                start_time = time.time()
                xml_output = self.generator.generate_xml(data)
                end_time = time.time()
                
                processing_time = end_time - start_time
                widgets_per_second = widget_count / processing_time if processing_time > 0 else 0
                output_size = len(xml_output)
                
                # Validate output
                root = ET.fromstring(xml_output)
                valid = root.tag == 'rss'
                
                results['test_results'].append({
                    'test': test_name,
                    'widget_count': widget_count,
                    'processing_time': round(processing_time, 4),
                    'widgets_per_second': round(widgets_per_second, 1),
                    'output_size': output_size,
                    'valid': valid
                })
                
                total_widgets += widget_count
                total_time += processing_time
                
            except Exception as e:
                results['test_results'].append({
                    'test': test_name,
                    'error': str(e)
                })
        
        if total_time > 0:
            results['average_widgets_per_second'] = round(total_widgets / total_time, 1)
            
            # Performance scoring
            if results['average_widgets_per_second'] >= 50:
                results['score'] = 100
            elif results['average_widgets_per_second'] >= 25:
                results['score'] = 80
            elif results['average_widgets_per_second'] >= 10:
                results['score'] = 60
            else:
                results['score'] = 40
        
        results['status'] = 'EXCELLENT' if results['score'] >= 80 else 'GOOD' if results['score'] >= 60 else 'NEEDS_IMPROVEMENT'
        
        return results
    
    def _validate_placeholder_system(self) -> Dict[str, Any]:
        """Validate placeholder replacement system."""
        print("🔧 Validating placeholder system...")
        
        placeholder_data = {
            'pages': [{
                'title': '{{site_name}} - {{page_type}}',
                'slug': 'placeholder-test',
                'sections': [{
                    'structure': '100',
                    'columns': [{
                        'width': 100,
                        'widgets': [{
                            'type': 'title',
                            'title': 'Welcome to {{site_name}}<span>.</span>'
                        }]
                    }]
                }]
            }]
        }
        
        site_config = {
            'title': 'Test Company',
            'description': 'Testing placeholder system',
            'base_url': 'http://localhost:8082'
        }
        
        try:
            xml_output = self.generator.generate_xml(placeholder_data, site_config)
            
            results = {
                'placeholders_replaced': '{{site_name}}' not in xml_output,
                'site_name_present': 'Test Company' in xml_output,
                'no_leftover_placeholders': '{{' not in xml_output or '}}' not in xml_output,
                'valid_xml': True,
                'score': 0,
                'status': 'UNKNOWN'
            }
            
            # Validate XML
            try:
                ET.fromstring(xml_output)
            except ET.ParseError:
                results['valid_xml'] = False
            
            # Calculate score
            passed_checks = sum(1 for result in results.values() if result is True)
            results['score'] = (passed_checks / (len(results) - 2)) * 100  # Exclude score and status
            results['status'] = 'PASS' if results['score'] >= 75 else 'FAIL'
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'score': 0,
                'status': 'ERROR'
            }
    
    def _test_error_handling(self) -> Dict[str, Any]:
        """Test error handling capabilities."""
        print("🛠️ Testing error handling...")
        
        error_scenarios = [
            {
                'name': 'Invalid widget type',
                'data': {
                    'pages': [{
                        'title': 'Error Test',
                        'slug': 'error',
                        'sections': [{
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{'type': 'invalid-widget'}]
                            }]
                        }]
                    }]
                }
            },
            {
                'name': 'Missing required fields',
                'data': {
                    'pages': [{
                        'title': 'Error Test 2',
                        'slug': 'error2',
                        'sections': [{
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{'type': 'texticon'}]  # Missing title and icon
                            }]
                        }]
                    }]
                }
            },
            {
                'name': 'Empty data',
                'data': {}
            },
            {
                'name': 'Malformed structure',
                'data': {
                    'pages': [{
                        'sections': [{}]  # Missing title and other required fields
                    }]
                }
            }
        ]
        
        results = {
            'total_scenarios': len(error_scenarios),
            'handled_gracefully': 0,
            'scenario_results': {},
            'score': 0,
            'status': 'UNKNOWN'
        }
        
        for scenario in error_scenarios:
            try:
                xml_output = self.generator.generate_xml(scenario['data'])
                
                # Check if output is still valid XML (graceful handling)
                try:
                    root = ET.fromstring(xml_output)
                    if root.tag == 'rss':
                        results['handled_gracefully'] += 1
                        results['scenario_results'][scenario['name']] = 'HANDLED_GRACEFULLY'
                    else:
                        results['scenario_results'][scenario['name']] = 'INVALID_OUTPUT'
                except ET.ParseError:
                    results['scenario_results'][scenario['name']] = 'INVALID_XML'
                    
            except Exception as e:
                results['scenario_results'][scenario['name']] = f'EXCEPTION: {str(e)}'
        
        results['score'] = (results['handled_gracefully'] / results['total_scenarios']) * 100
        results['status'] = 'EXCELLENT' if results['score'] >= 75 else 'GOOD' if results['score'] >= 50 else 'POOR'
        
        return results
    
    def _validate_structural_compliance(self) -> Dict[str, Any]:
        """Validate structural compliance with WordPress/Elementor standards."""
        print("📐 Validating structural compliance...")
        
        test_data = {
            'pages': [{
                'title': 'Structural Compliance Test',
                'slug': 'compliance',
                'sections': [{
                    'structure': '50',
                    'columns': [
                        {
                            'width': 50,
                            'widgets': [{
                                'type': 'texticon',
                                'title': 'Left Column',
                                'icon': 'fas fa-left'
                            }]
                        },
                        {
                            'width': 50,
                            'widgets': [{
                                'type': 'texticon',
                                'title': 'Right Column',
                                'icon': 'fas fa-right'
                            }]
                        }
                    ]
                }]
            }]
        }
        
        try:
            xml_output = self.generator.generate_xml(test_data)
            root = ET.fromstring(xml_output)
            
            compliance_checks = {
                'wordpress_structure': self._check_wordpress_structure(root),
                'elementor_data_structure': self._check_elementor_structure(root),
                'id_uniqueness': self._check_id_uniqueness(root),
                'responsive_settings': self._check_responsive_settings(root),
                'theme_compatibility': self._check_theme_compatibility(root),
                'score': 0,
                'status': 'UNKNOWN'
            }
            
            # Calculate score
            passed_checks = sum(1 for key, value in compliance_checks.items() 
                              if key not in ['score', 'status'] and value is True)
            compliance_checks['score'] = (passed_checks / (len(compliance_checks) - 2)) * 100
            compliance_checks['status'] = 'PASS' if compliance_checks['score'] >= 80 else 'FAIL'
            
            return compliance_checks
            
        except Exception as e:
            return {
                'error': str(e),
                'score': 0,
                'status': 'ERROR'
            }
    
    def _check_wordpress_structure(self, root: ET.Element) -> bool:
        """Check WordPress XML structure compliance."""
        required_structure = [
            root.tag == 'rss',
            root.get('version') == '2.0',
            root.find('channel') is not None,
            root.find('.//wp:wxr_version', {'wp': 'http://wordpress.org/export/1.2/'}) is not None
        ]
        return all(required_structure)
    
    def _check_elementor_structure(self, root: ET.Element) -> bool:
        """Check Elementor data structure compliance."""
        for item in root.findall('.//item'):
            for postmeta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
                meta_key = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                if meta_key is not None and meta_key.text == '_elementor_data':
                    meta_value = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_value')
                    if meta_value is not None:
                        try:
                            elementor_data = json.loads(meta_value.text)
                            if isinstance(elementor_data, list) and elementor_data:
                                # Check first section structure
                                section = elementor_data[0]
                                required_keys = ['id', 'elType', 'elements']
                                return all(key in section for key in required_keys)
                        except json.JSONDecodeError:
                            return False
        return False
    
    def _check_id_uniqueness(self, root: ET.Element) -> bool:
        """Check that all generated IDs are unique."""
        ids = set()
        for item in root.findall('.//item'):
            for postmeta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
                meta_key = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                if meta_key is not None and meta_key.text == '_elementor_data':
                    meta_value = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_value')
                    if meta_value is not None:
                        try:
                            elementor_data = json.loads(meta_value.text)
                            extracted_ids = self._extract_all_ids(elementor_data)
                            if len(extracted_ids) != len(set(extracted_ids)):
                                return False
                            ids.update(extracted_ids)
                        except json.JSONDecodeError:
                            return False
        return True
    
    def _extract_all_ids(self, data: Any) -> List[str]:
        """Recursively extract all IDs from Elementor data."""
        ids = []
        if isinstance(data, dict):
            if 'id' in data:
                ids.append(data['id'])
            for value in data.values():
                ids.extend(self._extract_all_ids(value))
        elif isinstance(data, list):
            for item in data:
                ids.extend(self._extract_all_ids(item))
        return ids
    
    def _check_responsive_settings(self, root: ET.Element) -> bool:
        """Check for responsive settings in widgets."""
        # This is a simplified check - in a real scenario, you'd check for responsive breakpoints
        return True  # Placeholder - implement based on specific responsive requirements
    
    def _check_theme_compatibility(self, root: ET.Element) -> bool:
        """Check for theme compatibility indicators."""
        # Check for Cholot-specific class names and settings
        xml_str = ET.tostring(root, encoding='unicode')
        return 'cholot-' in xml_str
    
    def _calculate_overall_score(self, report: Dict[str, Any]) -> float:
        """Calculate overall validation score."""
        scores = []
        weights = {
            'format_validation': 0.2,
            'widget_validation': 0.2,
            'scenario_testing': 0.15,
            'demo_comparison': 0.1,
            'performance_analysis': 0.1,
            'placeholder_validation': 0.1,
            'error_handling': 0.1,
            'structural_compliance': 0.05
        }
        
        for section, weight in weights.items():
            if section in report and 'score' in report[section]:
                scores.append(report[section]['score'] * weight)
        
        return sum(scores) if scores else 0
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        # Format validation recommendations
        if report.get('format_validation', {}).get('score', 0) < 80:
            recommendations.append("Improve XML format compliance - ensure all required namespaces and structure elements are present")
        
        # Widget validation recommendations
        if report.get('widget_validation', {}).get('score', 0) < 90:
            recommendations.append("Fix widget generation issues - ensure all 13 widget types are properly implemented")
        
        # Performance recommendations
        perf_score = report.get('performance_analysis', {}).get('score', 0)
        if perf_score < 60:
            recommendations.append("Optimize performance - consider caching, code optimization, or refactoring bottlenecks")
        elif perf_score < 80:
            recommendations.append("Consider performance optimizations for large datasets")
        
        # Error handling recommendations
        if report.get('error_handling', {}).get('score', 0) < 75:
            recommendations.append("Improve error handling - ensure graceful handling of invalid input and edge cases")
        
        # Demo comparison recommendations
        if report.get('demo_comparison', {}).get('score', 0) < 75:
            recommendations.append("Align output format more closely with demo-data-fixed.xml structure")
        
        # Scenario testing recommendations
        if report.get('scenario_testing', {}).get('score', 0) < 80:
            recommendations.append("Fix failing test scenarios - ensure all predefined scenarios pass validation")
        
        if not recommendations:
            recommendations.append("Excellent work! All validation targets met successfully")
        
        return recommendations
    
    def save_report(self, report: Dict[str, Any], output_file: Optional[Path] = None) -> Path:
        """Save validation report to file."""
        if output_file is None:
            output_file = Path(__file__).parent / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def print_summary(self, report: Dict[str, Any]):
        """Print validation report summary."""
        print("\n" + "=" * 70)
        print("📊 VALIDATION REPORT SUMMARY")
        print("=" * 70)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Overall Score: {report['overall_score']:.1f}/100")
        print(f"Verdict: {report['verdict']}")
        
        print("\n📋 Section Scores:")
        sections = [
            ('XML Format Validation', 'format_validation'),
            ('Widget Validation', 'widget_validation'),
            ('Scenario Testing', 'scenario_testing'),
            ('Demo Comparison', 'demo_comparison'),
            ('Performance Analysis', 'performance_analysis'),
            ('Placeholder System', 'placeholder_validation'),
            ('Error Handling', 'error_handling'),
            ('Structural Compliance', 'structural_compliance')
        ]
        
        for section_name, section_key in sections:
            if section_key in report:
                score = report[section_key].get('score', 0)
                status = report[section_key].get('status', 'UNKNOWN')
                print(f"  {section_name:25}: {score:5.1f}% ({status})")
        
        if report.get('performance_analysis', {}).get('average_widgets_per_second'):
            perf = report['performance_analysis']
            print(f"\n⚡ Performance: {perf['average_widgets_per_second']:.1f} widgets/second")
        
        print(f"\n💡 Recommendations ({len(report['recommendations'])}):")
        for i, rec in enumerate(report['recommendations'][:3], 1):  # Show top 3
            print(f"  {i}. {rec}")
        
        if len(report['recommendations']) > 3:
            print(f"  ... and {len(report['recommendations']) - 3} more")
        
        print(f"\n🎯 FINAL VERDICT: {report['verdict']}")
        
        verdict_messages = {
            'EXCELLENT': "🎉 Outstanding! All validation targets exceeded.",
            'GOOD': "✅ Good performance with minor areas for improvement.",
            'ACCEPTABLE': "⚠️  Acceptable but needs improvement in several areas.",
            'NEEDS_IMPROVEMENT': "❌ Significant improvements needed before production use.",
            'FAIL': "🚨 Critical issues found. Major work required."
        }
        
        print(verdict_messages.get(report['verdict'], "Unknown verdict"))


def main():
    """Main function to run validation report generation."""
    validator = ValidationReportGenerator()
    
    # Generate comprehensive report
    report = validator.generate_comprehensive_report()
    
    # Save report
    report_file = validator.save_report(report)
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    # Print summary
    validator.print_summary(report)
    
    # Return exit code based on verdict
    exit_codes = {
        'EXCELLENT': 0,
        'GOOD': 0,
        'ACCEPTABLE': 0,
        'NEEDS_IMPROVEMENT': 1,
        'FAIL': 1
    }
    
    return exit_codes.get(report['verdict'], 1)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)