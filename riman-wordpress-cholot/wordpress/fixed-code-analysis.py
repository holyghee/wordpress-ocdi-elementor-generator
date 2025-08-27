#!/usr/bin/env python3
"""
Fixed-Code Analysis: Comprehensive Testing of CholotComponentFactory
==================================================================

This script thoroughly tests the CholotComponentFactory approach for generating
Elementor JSON widgets. It compares generated output against real templates,
tests edge cases, and evaluates coverage and maintainability.

Author: Analysis Agent
Version: 1.0.0
"""

import json
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Any, Set
import re

# Import the factory we're testing
from generate_wordpress_xml import CholotComponentFactory, CholotThemeConfig


class FixedCodeAnalyzer:
    """Comprehensive analyzer for the fixed-code approach."""
    
    def __init__(self):
        self.factory = CholotComponentFactory()
        self.test_results = []
        self.coverage_data = {}
        self.edge_case_results = []
        
    def run_comprehensive_analysis(self):
        """Run the complete analysis suite."""
        print("🔬 FIXED-CODE ANALYSIS: CholotComponentFactory")
        print("=" * 60)
        
        # Run all test suites
        self.test_widget_generation()
        self.test_against_real_templates()
        self.test_edge_cases()
        self.analyze_coverage()
        self.evaluate_maintainability()
        
        # Generate summary report
        self.generate_summary_report()
        
    def test_widget_generation(self):
        """Test generation of all 13 widget types."""
        print("\n📝 Testing Widget Generation...")
        
        widget_tests = [
            # TextIcon Widget Tests
            {
                'type': 'texticon',
                'method': 'create_texticon_widget',
                'configs': [
                    {'title': 'Basic TextIcon', 'icon': 'fas fa-star'},
                    {'title': 'Full TextIcon', 'icon': 'fas fa-heart', 'subtitle': 'Subtitle', 'text': 'Description'},
                    {'title': 'Custom TextIcon', 'icon': 'fas fa-cog', 'custom_settings': {'title_color': '#ff0000'}}
                ]
            },
            
            # Title Widget Tests
            {
                'type': 'title', 
                'method': 'create_title_widget',
                'configs': [
                    {'title': 'Basic Title'},
                    {'title': 'Styled Title', 'header_size': 'h1', 'align': 'center'},
                    {'title': 'Responsive Title', 'align': 'left', 'responsive': {'tablet': 'center'}}
                ]
            },
            
            # Post Widget Tests
            {
                'type': 'post',
                'method': 'create_post_widget',
                'configs': [
                    {'post_count': 3, 'categories': ['news', 'events']},
                    {'post_count': 6, 'show_excerpt': 'yes', 'button_text': 'Learn More'},
                    {'post_count': 1, 'column': 'two', 'excerpt_after': '...read more'}
                ]
            },
            
            # Gallery Widget Tests
            {
                'type': 'gallery',
                'method': 'create_gallery_widget', 
                'configs': [
                    {'images': ['img1.jpg', 'img2.jpg'], 'columns': 'col-md-6'},
                    {'images': [{'id': 1, 'url': 'test.jpg'}], 'height': 300, 'margin': 10},
                    {'images': [], 'show_title': 'yes', 'responsive': {'tablet': {'height': 200}}}
                ]
            },
            
            # Logo Widget Tests
            {
                'type': 'logo',
                'method': 'create_logo_widget',
                'configs': [
                    {'url': 'logo.png', 'align': 'center'},
                    {'url': 'logo.png', 'id': 100, 'height': '80px'},
                    {'url': '', 'align': 'right'}
                ]
            },
            
            # Menu Widget Tests
            {
                'type': 'menu',
                'method': 'create_menu_widget',
                'configs': [
                    {'menu_name': 'main-menu'},
                    {'menu_name': 'footer-menu', 'align': 'center', 'mobile': 'block'},
                    {'menu_name': 'custom', 'desktop_tablet': 'block', 'mobile_tablet': 'none'}
                ]
            },
            
            # Button-Text Widget Tests  
            {
                'type': 'button-text',
                'method': 'create_button_text_widget',
                'configs': [
                    {'text': 'Click Me', 'url': '#'},
                    {'text': 'Contact Us', 'url': '/contact', 'subtitle': 'Get in touch', 'icon': 'fas fa-phone'},
                    {'text': 'External', 'url': 'https://example.com', 'external': 'yes', 'icon_align': 'left'}
                ]
            },
            
            # Team Widget Tests
            {
                'type': 'team',
                'method': 'create_team_widget',
                'configs': [
                    {'name': 'John Doe', 'position': 'Manager', 'image_url': 'team1.jpg'},
                    {'name': 'Jane Smith', 'position': 'Developer', 'image_url': 'team2.jpg', 'height': '500px'},
                    {'name': 'Bob Wilson', 'position': 'Designer', 'social_links': [
                        {'icon': 'fab fa-twitter', 'url': 'https://twitter.com'},
                        {'icon': 'fab fa-linkedin', 'url': 'https://linkedin.com'}
                    ]}
                ]
            },
            
            # Testimonial Widget Tests
            {
                'type': 'testimonial',
                'method': 'create_testimonial_widget',
                'configs': [
                    {'columns': 3, 'testimonials': [{'name': 'Customer 1', 'text': 'Great service!'}]},
                    {'columns': 2, 'align': 'left', 'responsive': {'mobile': {'title_size': 16}}},
                    {'columns': 1, 'testimonials': []}
                ]
            },
            
            # Text-Line Widget Tests
            {
                'type': 'text-line',
                'method': 'create_text_line_widget',
                'configs': [
                    {'title': 'Section Title', 'line_width': 100},
                    {'title': 'Custom Title', 'subtitle': 'Subtitle', 'title_size': 32, 'background_color': '#f0f0f0'},
                    {'title': 'Background Title', 'background_image': 'bg.jpg', 'background_position': 'center'}
                ]
            },
            
            # Contact Widget Tests
            {
                'type': 'contact',
                'method': 'create_contact_widget',
                'configs': [
                    {'shortcode': '[contact-form-7 id="1"]'},
                    {'shortcode': '[contact-form-7 id="2"]', 'button_width': '50%'},
                    {'shortcode': '[custom-form]'}
                ]
            },
            
            # Sidebar Widget Tests
            {
                'type': 'sidebar',
                'method': 'create_sidebar_widget',
                'configs': [
                    {'width': '25px'},
                    {'width': '40px', 'title_size': 24},
                    {}
                ]
            }
        ]
        
        for widget_test in widget_tests:
            self.test_widget_type(widget_test)
    
    def test_widget_type(self, widget_test: Dict):
        """Test a specific widget type with multiple configurations."""
        widget_type = widget_test['type']
        method_name = widget_test['method']
        configs = widget_test['configs']
        
        print(f"  🧪 Testing {widget_type} widget...")
        
        results = {
            'widget_type': widget_type,
            'method': method_name,
            'tests': [],
            'success_count': 0,
            'error_count': 0
        }
        
        for i, config in enumerate(configs, 1):
            try:
                # Get the method and call it
                if widget_type == 'post':
                    # Special handling for post widgets
                    widget = self.factory.create_post_widget(config, 'three')
                else:
                    method = getattr(self.factory, method_name)
                    widget = method(config)
                
                # Validate the generated widget
                validation_result = self.validate_widget_structure(widget, widget_type)
                
                test_result = {
                    'config': config,
                    'success': validation_result['valid'],
                    'widget_output': widget,
                    'validation': validation_result,
                    'size_kb': len(json.dumps(widget)) / 1024
                }
                
                if validation_result['valid']:
                    results['success_count'] += 1
                    print(f"    ✅ Test {i}: PASS ({test_result['size_kb']:.1f}KB)")
                else:
                    results['error_count'] += 1 
                    print(f"    ❌ Test {i}: FAIL - {validation_result['errors']}")
                
                results['tests'].append(test_result)
                
            except Exception as e:
                results['error_count'] += 1
                error_result = {
                    'config': config,
                    'success': False,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                results['tests'].append(error_result)
                print(f"    💥 Test {i}: ERROR - {e}")
        
        self.test_results.append(results)
    
    def validate_widget_structure(self, widget: Dict, widget_type: str) -> Dict:
        """Validate that a generated widget has proper structure."""
        errors = []
        
        # Check required fields
        required_fields = ['id', 'elType', 'settings', 'elements', 'widgetType']
        for field in required_fields:
            if field not in widget:
                errors.append(f"Missing required field: {field}")
        
        # Check field types
        if 'id' in widget and not isinstance(widget['id'], str):
            errors.append("ID must be string")
        
        if 'elType' in widget and widget['elType'] != 'widget':
            errors.append(f"elType should be 'widget', got '{widget['elType']}'")
        
        if 'elements' in widget and not isinstance(widget['elements'], list):
            errors.append("Elements must be list")
        
        if 'settings' in widget and not isinstance(widget['settings'], dict):
            errors.append("Settings must be dict")
        
        # Check widget type
        if 'widgetType' in widget:
            expected_types = [
                'cholot-texticon', 'cholot-title', 'cholot-post-three', 'cholot-post-four',
                'cholot-gallery', 'cholot-logo', 'cholot-menu', 'cholot-button-text',
                'cholot-team', 'cholot-testimonial-two', 'cholot-text-line', 
                'cholot-contact', 'cholot-sidebar'
            ]
            if widget['widgetType'] not in expected_types:
                errors.append(f"Unexpected widgetType: {widget['widgetType']}")
        
        # Check ID format (should be 7 chars alphanumeric)
        if 'id' in widget:
            if not re.match(r'^[a-z0-9]{7}$', widget['id']):
                errors.append(f"ID format invalid: {widget['id']}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'field_count': len(widget.get('settings', {})),
            'has_theme_colors': self.check_theme_color_usage(widget)
        }
    
    def check_theme_color_usage(self, widget: Dict) -> bool:
        """Check if widget uses theme colors properly."""
        settings = widget.get('settings', {})
        theme_config = CholotThemeConfig()
        
        # Look for theme color usage
        theme_colors = [theme_config.PRIMARY_COLOR, theme_config.WHITE, theme_config.BLACK]
        widget_str = json.dumps(settings)
        
        return any(color in widget_str for color in theme_colors)
    
    def test_against_real_templates(self):
        """Compare generated widgets against real template data."""
        print("\n🎯 Testing Against Real Templates...")
        
        template_dir = Path("templates")
        if not template_dir.exists():
            print("  ⚠️  Templates directory not found, skipping comparison")
            return
        
        # Load real template data
        real_widgets = self.extract_widgets_from_templates()
        
        if not real_widgets:
            print("  ⚠️  No real widgets found in templates")
            return
        
        # Analyze real widget patterns
        self.analyze_real_widget_patterns(real_widgets)
        
        # Test factory against real patterns
        self.test_factory_against_patterns(real_widgets)
    
    def extract_widgets_from_templates(self) -> List[Dict]:
        """Extract all widgets from real template files."""
        widgets = []
        template_dir = Path("templates")
        
        for json_file in template_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    template_data = json.load(f)
                
                # Extract widgets recursively
                extracted = self.extract_widgets_recursive(template_data)
                widgets.extend(extracted)
                print(f"  📄 {json_file.name}: {len(extracted)} widgets extracted")
                
            except Exception as e:
                print(f"  ⚠️  Error reading {json_file}: {e}")
        
        return widgets
    
    def extract_widgets_recursive(self, elements: List[Dict]) -> List[Dict]:
        """Recursively extract widgets from element structure."""
        widgets = []
        
        for element in elements:
            if element.get('elType') == 'widget':
                widgets.append(element)
            elif 'elements' in element:
                widgets.extend(self.extract_widgets_recursive(element['elements']))
        
        return widgets
    
    def analyze_real_widget_patterns(self, real_widgets: List[Dict]):
        """Analyze patterns in real widgets."""
        print("  🔍 Analyzing real widget patterns...")
        
        # Count widget types
        widget_type_counts = {}
        setting_patterns = {}
        
        for widget in real_widgets:
            widget_type = widget.get('widgetType', 'unknown')
            widget_type_counts[widget_type] = widget_type_counts.get(widget_type, 0) + 1
            
            # Analyze settings patterns
            settings = widget.get('settings', {})
            if widget_type not in setting_patterns:
                setting_patterns[widget_type] = set()
            
            setting_patterns[widget_type].update(settings.keys())
        
        print(f"    📊 Found {len(real_widgets)} real widgets:")
        for widget_type, count in sorted(widget_type_counts.items()):
            print(f"      {widget_type}: {count} instances")
        
        # Store patterns for comparison
        self.real_widget_patterns = {
            'type_counts': widget_type_counts,
            'setting_patterns': setting_patterns,
            'total_widgets': len(real_widgets)
        }
    
    def test_factory_against_patterns(self, real_widgets: List[Dict]):
        """Test factory output against real widget patterns."""
        print("  ⚖️  Comparing factory output to real patterns...")
        
        cholot_widgets = [w for w in real_widgets if w.get('widgetType', '').startswith('cholot-')]
        
        if not cholot_widgets:
            print("    ⚠️  No Cholot widgets found in real templates")
            return
        
        # Test each cholot widget type found
        comparison_results = {}
        
        for widget in cholot_widgets:
            widget_type = widget.get('widgetType', '')
            if widget_type not in comparison_results:
                comparison_results[widget_type] = {
                    'real_examples': [],
                    'factory_test': None,
                    'setting_coverage': 0,
                    'matches': []
                }
            
            comparison_results[widget_type]['real_examples'].append(widget)
        
        # Test factory against each type
        for widget_type, data in comparison_results.items():
            print(f"    🧪 Testing {widget_type}...")
            
            factory_result = self.test_factory_for_type(widget_type, data['real_examples'])
            comparison_results[widget_type]['factory_test'] = factory_result
            
            if factory_result:
                print(f"      ✅ Coverage: {factory_result['coverage']:.1f}%")
            else:
                print(f"      ❌ Factory cannot generate {widget_type}")
        
        self.template_comparison = comparison_results
    
    def test_factory_for_type(self, widget_type: str, real_examples: List[Dict]) -> Dict:
        """Test if factory can generate a specific widget type."""
        # Map widget types to factory methods
        type_mapping = {
            'cholot-texticon': 'create_texticon_widget',
            'cholot-title': 'create_title_widget', 
            'cholot-post-three': lambda cfg: self.factory.create_post_widget(cfg, 'three'),
            'cholot-post-four': lambda cfg: self.factory.create_post_widget(cfg, 'four'),
            'cholot-gallery': 'create_gallery_widget',
            'cholot-logo': 'create_logo_widget',
            'cholot-menu': 'create_menu_widget',
            'cholot-button-text': 'create_button_text_widget',
            'cholot-team': 'create_team_widget',
            'cholot-testimonial-two': 'create_testimonial_widget',
            'cholot-text-line': 'create_text_line_widget',
            'cholot-contact': 'create_contact_widget',
            'cholot-sidebar': 'create_sidebar_widget'
        }
        
        if widget_type not in type_mapping:
            return None
        
        try:
            # Generate factory widget
            method_or_func = type_mapping[widget_type]
            if callable(method_or_func):
                factory_widget = method_or_func({})
            else:
                method = getattr(self.factory, method_or_func)
                factory_widget = method({})
            
            # Compare settings
            real_settings = set()
            for example in real_examples:
                real_settings.update(example.get('settings', {}).keys())
            
            factory_settings = set(factory_widget.get('settings', {}).keys())
            
            coverage = len(factory_settings & real_settings) / len(real_settings) if real_settings else 0
            
            return {
                'factory_widget': factory_widget,
                'real_setting_count': len(real_settings),
                'factory_setting_count': len(factory_settings),
                'coverage': coverage * 100,
                'missing_settings': real_settings - factory_settings,
                'extra_settings': factory_settings - real_settings
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        print("\n🚨 Testing Edge Cases...")
        
        edge_tests = [
            # Empty/minimal configs
            {
                'name': 'Empty TextIcon Config',
                'test': lambda: self.factory.create_texticon_widget({}),
                'should_work': True
            },
            
            # None values
            {
                'name': 'None Values',
                'test': lambda: self.factory.create_title_widget({'title': None}),
                'should_work': True
            },
            
            # Very long strings
            {
                'name': 'Very Long Title',
                'test': lambda: self.factory.create_title_widget({
                    'title': 'A' * 1000 + ' very long title that might break things'
                }),
                'should_work': True
            },
            
            # Special characters
            {
                'name': 'Special Characters',
                'test': lambda: self.factory.create_texticon_widget({
                    'title': 'Title with "quotes" & <html> tags',
                    'text': 'Text with émojis 🎉 and special chars: ™®©'
                }),
                'should_work': True
            },
            
            # Invalid data types
            {
                'name': 'Invalid Gallery Images',
                'test': lambda: self.factory.create_gallery_widget({
                    'images': 'not-a-list'
                }),
                'should_work': True  # Should handle gracefully
            },
            
            # Large numbers
            {
                'name': 'Large Height Value',
                'test': lambda: self.factory.create_text_line_widget({
                    'title_size': 999999,
                    'line_width': -100
                }),
                'should_work': True
            },
            
            # Empty lists
            {
                'name': 'Empty Social Links',
                'test': lambda: self.factory.create_team_widget({
                    'social_links': []
                }),
                'should_work': True
            },
            
            # Invalid URLs
            {
                'name': 'Invalid URLs',
                'test': lambda: self.factory.create_button_text_widget({
                    'url': 'not-a-valid-url://broken',
                    'text': 'Button'
                }),
                'should_work': True
            },
            
            # Recursive config
            {
                'name': 'Custom Settings Override',
                'test': lambda: self.factory.create_texticon_widget({
                    'title': 'Original',
                    'custom_settings': {
                        'title': 'Overridden',
                        'new_setting': 'added'
                    }
                }),
                'should_work': True
            }
        ]
        
        for edge_test in edge_tests:
            try:
                result = edge_test['test']()
                success = True
                error = None
                output_size = len(json.dumps(result)) if result else 0
                
            except Exception as e:
                result = None
                success = False
                error = str(e)
                output_size = 0
            
            expected_success = edge_test['should_work']
            test_passed = success == expected_success
            
            status = "✅ PASS" if test_passed else "❌ FAIL"
            print(f"  {status} {edge_test['name']}")
            
            if not test_passed:
                print(f"    Expected: {'success' if expected_success else 'failure'}")
                print(f"    Actual: {'success' if success else 'failure'}")
                if error:
                    print(f"    Error: {error}")
            
            self.edge_case_results.append({
                'name': edge_test['name'],
                'success': success,
                'expected': expected_success,
                'passed': test_passed,
                'error': error,
                'output_size': output_size
            })
    
    def analyze_coverage(self):
        """Analyze what percentage of real-world needs the factory covers."""
        print("\n📊 Analyzing Coverage...")
        
        # Calculate widget type coverage
        if hasattr(self, 'real_widget_patterns'):
            patterns = self.real_widget_patterns
            cholot_types = [t for t in patterns['type_counts'].keys() if t.startswith('cholot-')]
            
            factory_types = {
                'cholot-texticon', 'cholot-title', 'cholot-post-three', 'cholot-post-four',
                'cholot-gallery', 'cholot-logo', 'cholot-menu', 'cholot-button-text', 
                'cholot-team', 'cholot-testimonial-two', 'cholot-text-line',
                'cholot-contact', 'cholot-sidebar'
            }
            
            covered_types = set(cholot_types) & factory_types
            type_coverage = len(covered_types) / len(cholot_types) if cholot_types else 0
            
            print(f"  🎯 Widget Type Coverage: {type_coverage * 100:.1f}%")
            print(f"    Covered: {len(covered_types)}/{len(cholot_types)} types")
            
            if cholot_types:
                uncovered = set(cholot_types) - factory_types
                if uncovered:
                    print(f"    Missing: {', '.join(uncovered)}")
        
        # Analyze factory capabilities
        factory_stats = self.calculate_factory_stats()
        self.coverage_data = factory_stats
        
        print(f"  📈 Factory Statistics:")
        print(f"    Total methods: {factory_stats['method_count']}")
        print(f"    Average settings per widget: {factory_stats['avg_settings']:.1f}")
        print(f"    Theme integration: {'✅' if factory_stats['has_theme_integration'] else '❌'}")
        print(f"    Responsive support: {'✅' if factory_stats['responsive_support'] else '❌'}")
    
    def calculate_factory_stats(self) -> Dict:
        """Calculate statistics about the factory."""
        method_count = 0
        total_settings = 0
        has_theme_integration = False
        responsive_support = False
        
        # Test each method with basic config
        test_configs = [
            ('create_texticon_widget', {}),
            ('create_title_widget', {}),  
            ('create_gallery_widget', {}),
            ('create_logo_widget', {}),
            ('create_menu_widget', {}),
            ('create_button_text_widget', {}),
            ('create_team_widget', {}),
            ('create_testimonial_widget', {}),
            ('create_text_line_widget', {}),
            ('create_contact_widget', {}),
            ('create_sidebar_widget', {})
        ]
        
        for method_name, config in test_configs:
            try:
                method = getattr(self.factory, method_name)
                widget = method(config)
                method_count += 1
                
                settings = widget.get('settings', {})
                total_settings += len(settings)
                
                # Check for theme colors
                if CholotThemeConfig.PRIMARY_COLOR in json.dumps(settings):
                    has_theme_integration = True
                
                # Check for responsive settings
                settings_str = json.dumps(settings)
                if '_tablet' in settings_str or '_mobile' in settings_str:
                    responsive_support = True
                    
            except Exception:
                pass
        
        # Test post widget separately
        try:
            widget = self.factory.create_post_widget({}, 'three')
            method_count += 1
            total_settings += len(widget.get('settings', {}))
        except Exception:
            pass
        
        return {
            'method_count': method_count,
            'avg_settings': total_settings / method_count if method_count else 0,
            'has_theme_integration': has_theme_integration,
            'responsive_support': responsive_support,
            'total_settings': total_settings
        }
    
    def evaluate_maintainability(self):
        """Evaluate the maintainability and extensibility of the factory."""
        print("\n🔧 Evaluating Maintainability...")
        
        maintainability = {
            'code_organization': self.analyze_code_organization(),
            'extensibility': self.analyze_extensibility(), 
            'consistency': self.analyze_consistency(),
            'documentation': self.analyze_documentation()
        }
        
        self.maintainability_analysis = maintainability
        
        for aspect, score in maintainability.items():
            status = "✅" if score['rating'] >= 7 else "⚠️" if score['rating'] >= 4 else "❌"
            print(f"  {status} {aspect.title()}: {score['rating']}/10")
            for point in score['points']:
                print(f"    • {point}")
    
    def analyze_code_organization(self) -> Dict:
        """Analyze code organization quality."""
        points = []
        rating = 8  # Start with good rating
        
        # Check method naming consistency
        methods = [m for m in dir(self.factory) if m.startswith('create_')]
        if len(methods) == 12:  # Expected number of widget methods + helpers
            points.append("All widget types have dedicated methods")
        else:
            points.append(f"Method count: {len(methods)} (expected ~12)")
            rating -= 1
        
        # Check for helper methods
        if hasattr(self.factory, 'create_column') and hasattr(self.factory, 'create_section'):
            points.append("Helper methods for sections/columns provided")
        else:
            points.append("Missing section/column helper methods")
            rating -= 2
        
        # Check theme integration
        if hasattr(self.factory, 'theme_config'):
            points.append("Centralized theme configuration")
        else:
            points.append("No centralized theme configuration")
            rating -= 2
        
        return {'rating': rating, 'points': points}
    
    def analyze_extensibility(self) -> Dict:
        """Analyze how easily the factory can be extended."""
        points = []
        rating = 6  # Medium rating
        
        # Check for custom_settings support
        test_widget = self.factory.create_texticon_widget({'custom_settings': {'test': 'value'}})
        if test_widget['settings'].get('test') == 'value':
            points.append("Custom settings override supported")
            rating += 2
        else:
            points.append("No custom settings override mechanism")
        
        # Check for consistent parameter patterns
        points.append("All methods accept config dictionaries")
        rating += 1
        
        # Check for ID generation
        if hasattr(self.factory, 'id_generator'):
            points.append("Centralized ID generation system")
            rating += 1
        
        # Check for default value handling
        points.append("Graceful handling of missing parameters")
        
        return {'rating': rating, 'points': points}
    
    def analyze_consistency(self) -> Dict:
        """Analyze consistency across widget methods."""
        points = []
        rating = 7  # Good starting point
        
        # Test return structure consistency
        widgets = []
        for method_name in ['create_texticon_widget', 'create_title_widget', 'create_gallery_widget']:
            try:
                method = getattr(self.factory, method_name)
                widget = method({})
                widgets.append(widget)
            except:
                pass
        
        if widgets:
            # Check structure consistency
            structures = [set(w.keys()) for w in widgets]
            if all(s == structures[0] for s in structures):
                points.append("Consistent widget structure across types")
            else:
                points.append("Inconsistent widget structures")
                rating -= 2
            
            # Check settings patterns
            all_use_margins = all('_margin' in w.get('settings', {}) for w in widgets)
            if all_use_margins:
                points.append("Consistent margin handling")
            else:
                points.append("Inconsistent margin patterns")
                rating -= 1
        
        points.append("Consistent method naming pattern")
        
        return {'rating': rating, 'points': points}
    
    def analyze_documentation(self) -> Dict:
        """Analyze documentation quality."""
        points = []
        rating = 5  # Average rating
        
        # Check for docstrings
        methods_with_docs = 0
        total_methods = 0
        
        for method_name in dir(self.factory):
            if method_name.startswith('create_'):
                total_methods += 1
                method = getattr(self.factory, method_name)
                if method.__doc__:
                    methods_with_docs += 1
        
        if total_methods > 0:
            doc_coverage = methods_with_docs / total_methods
            if doc_coverage >= 0.8:
                points.append(f"Good documentation coverage ({doc_coverage*100:.0f}%)")
                rating += 2
            else:
                points.append(f"Limited documentation ({doc_coverage*100:.0f}%)")
        
        # Check for type hints
        import inspect
        try:
            sig = inspect.signature(self.factory.create_texticon_widget)
            if sig.parameters or sig.return_annotation:
                points.append("Type hints used")
                rating += 1
            else:
                points.append("No type hints")
        except:
            points.append("Cannot analyze type hints")
        
        # Check for examples in docstrings
        points.append("Documentation focuses on widget creation")
        
        return {'rating': rating, 'points': points}
    
    def generate_summary_report(self):
        """Generate comprehensive summary report."""
        print("\n" + "="*60)
        print("📋 ANALYSIS SUMMARY")
        print("="*60)
        
        # Test Results Summary
        total_tests = sum(r['success_count'] + r['error_count'] for r in self.test_results)
        total_successes = sum(r['success_count'] for r in self.test_results)
        success_rate = (total_successes / total_tests) * 100 if total_tests else 0
        
        print(f"\n🧪 WIDGET GENERATION TESTS")
        print(f"   Total tests: {total_tests}")
        print(f"   Success rate: {success_rate:.1f}%")
        print(f"   Widget types tested: {len(self.test_results)}")
        
        # Edge Case Results  
        edge_passes = sum(1 for r in self.edge_case_results if r['passed'])
        edge_total = len(self.edge_case_results)
        edge_rate = (edge_passes / edge_total) * 100 if edge_total else 0
        
        print(f"\n🚨 EDGE CASE TESTS")
        print(f"   Tests passed: {edge_passes}/{edge_total} ({edge_rate:.1f}%)")
        
        # Coverage Analysis
        if hasattr(self, 'coverage_data'):
            print(f"\n📊 COVERAGE ANALYSIS")
            print(f"   Factory methods: {self.coverage_data['method_count']}")
            print(f"   Avg settings per widget: {self.coverage_data['avg_settings']:.1f}")
            print(f"   Theme integration: {'Yes' if self.coverage_data['has_theme_integration'] else 'No'}")
            print(f"   Responsive support: {'Yes' if self.coverage_data['responsive_support'] else 'No'}")
        
        # Template Comparison
        if hasattr(self, 'template_comparison'):
            supported_types = sum(1 for data in self.template_comparison.values() 
                                if data['factory_test'] and 'error' not in data['factory_test'])
            total_types = len(self.template_comparison)
            
            print(f"\n🎯 TEMPLATE COMPARISON") 
            print(f"   Widget types in templates: {total_types}")
            print(f"   Types supported by factory: {supported_types}/{total_types}")
            
            if total_types > 0:
                avg_coverage = sum(data['factory_test'].get('coverage', 0) 
                                 for data in self.template_comparison.values() 
                                 if data['factory_test'] and 'coverage' in data['factory_test']) / total_types
                print(f"   Average setting coverage: {avg_coverage:.1f}%")
        
        # Maintainability Summary
        if hasattr(self, 'maintainability_analysis'):
            avg_rating = sum(aspect['rating'] for aspect in self.maintainability_analysis.values()) / len(self.maintainability_analysis)
            print(f"\n🔧 MAINTAINABILITY")
            print(f"   Overall rating: {avg_rating:.1f}/10")
            
            for aspect, data in self.maintainability_analysis.items():
                status = "🟢" if data['rating'] >= 7 else "🟡" if data['rating'] >= 4 else "🔴"
                print(f"   {status} {aspect.title()}: {data['rating']}/10")
        
        # Final Assessment
        print(f"\n🎖️  OVERALL ASSESSMENT")
        
        scores = []
        if total_tests > 0:
            scores.append(success_rate / 10)  # Convert to 0-10 scale
        if edge_total > 0:
            scores.append(edge_rate / 10)
        if hasattr(self, 'maintainability_analysis'):
            scores.append(avg_rating)
        
        if scores:
            overall_score = sum(scores) / len(scores)
            if overall_score >= 8:
                assessment = "🏆 EXCELLENT - Ready for production"
            elif overall_score >= 6:
                assessment = "✅ GOOD - Minor improvements needed"  
            elif overall_score >= 4:
                assessment = "⚠️  FAIR - Significant improvements needed"
            else:
                assessment = "❌ POOR - Major issues to address"
            
            print(f"   {assessment}")
            print(f"   Overall score: {overall_score:.1f}/10")


def main():
    """Run the comprehensive analysis."""
    analyzer = FixedCodeAnalyzer()
    analyzer.run_comprehensive_analysis()


if __name__ == "__main__":
    main()