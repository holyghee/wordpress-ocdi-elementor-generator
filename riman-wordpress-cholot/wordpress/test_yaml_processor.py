#!/usr/bin/env python3
"""
Test script for YAML to JSON Processor
======================================
Tests the processor with various YAML configurations to ensure proper conversion.
"""

import json
import yaml
from pathlib import Path
from yaml_to_json_processor import YAMLToJSONProcessor


def create_test_yaml():
    """Create test YAML configuration"""
    test_yaml = {
        'site': {
            'title': 'Test Cholot Site',
            'description': 'Testing YAML to JSON processor',
            'base_url': 'http://localhost:8080',
            'language': 'en-US'
        },
        'pages': [
            {
                'title': 'Home',
                'slug': 'home',
                'status': 'publish',
                'sections': [
                    {
                        'structure': '100',
                        'settings': {
                            'background': {
                                'background_background': 'classic',
                                'background_color': '#232323',
                                'background_image': {
                                    'url': 'http://localhost:8080/hero-bg.jpg',
                                    'id': 100
                                },
                                'background_position': 'center center',
                                'background_size': 'cover'
                            },
                            'shape_divider_bottom': {
                                'type': 'waves',
                                'color': '#b68c2f',
                                'height': {'unit': 'px', 'size': 80, 'sizes': []},
                                'flip': False,
                                'invert': True
                            },
                            'padding': {
                                'desktop': {'top': 100, 'bottom': 100},
                                'tablet': {'top': 80, 'bottom': 80},
                                'mobile': {'top': 60, 'bottom': 60}
                            }
                        },
                        'columns': [
                            {
                                'width': 100,
                                'widgets': [
                                    {
                                        'type': 'title',
                                        'title': 'Welcome to Our <span>Business</span>',
                                        'header_size': 'h1',
                                        'align': 'center',
                                        'custom_settings': {
                                            'title_color': '#ffffff',
                                            'span_title_color': '#b68c2f'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'structure': '33',
                        'settings': {
                            'background': {
                                'background_background': 'classic',
                                'background_color': '#f4f4f4'
                            }
                        },
                        'columns': [
                            {
                                'width': 33,
                                'widgets': [
                                    {
                                        'type': 'texticon',
                                        'title': 'Consulting',
                                        'subtitle': 'Expert Advice',
                                        'icon': 'fas fa-lightbulb',
                                        'text': 'Strategic consulting for your business growth'
                                    }
                                ]
                            },
                            {
                                'width': 33,
                                'widgets': [
                                    {
                                        'type': 'texticon',
                                        'title': 'Implementation',
                                        'subtitle': 'Hands-on Support',
                                        'icon': 'fas fa-cogs',
                                        'text': 'Complete implementation of solutions'
                                    }
                                ]
                            },
                            {
                                'width': 33,
                                'widgets': [
                                    {
                                        'type': 'texticon',
                                        'title': 'Support',
                                        'subtitle': '24/7 Assistance',
                                        'icon': 'fas fa-headset',
                                        'text': 'Round-the-clock support for your peace of mind'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'structure': '50',
                        'columns': [
                            {
                                'width': 50,
                                'widgets': [
                                    {
                                        'type': 'team',
                                        'name': 'Sarah Johnson',
                                        'position': 'CEO & Founder',
                                        'image_url': 'http://localhost:8080/team-ceo.jpg',
                                        'image_id': 200,
                                        'height': '400px',
                                        'align': 'center',
                                        'social_links': [
                                            {
                                                'icon': 'fab fa-linkedin-in',
                                                'url': 'https://linkedin.com/in/sarahjohnson'
                                            },
                                            {
                                                'icon': 'fab fa-twitter',
                                                'url': 'https://twitter.com/sarahjohnson'
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                'width': 50,
                                'widgets': [
                                    {
                                        'type': 'text-line',
                                        'title': 'Our Leadership Team',
                                        'subtitle': 'Meet Our Leaders',
                                        'line_width': 60,
                                        'line_height': 3,
                                        'background_color': '#ffffff'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'structure': '100',
                        'settings': {
                            'background': {
                                'background_background': 'classic',
                                'background_color': '#232323'
                            }
                        },
                        'columns': [
                            {
                                'width': 100,
                                'widgets': [
                                    {
                                        'type': 'contact',
                                        'shortcode': '[contact-form-7 id="1" title="Contact form"]',
                                        'button_width': '200px',
                                        'custom_settings': {
                                            'form_bg': 'rgba(255,255,255,0.1)'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    return test_yaml


def test_basic_processing():
    """Test basic YAML processing functionality"""
    print("Testing basic YAML processing...")
    
    processor = YAMLToJSONProcessor(debug=True)
    test_data = create_test_yaml()
    
    try:
        result = processor.process_yaml_data(test_data)
        
        # Verify structure
        assert 'pages' in result
        assert len(result['pages']) == 1
        
        page = result['pages'][0]
        assert page['title'] == 'Home'
        assert 'elementor_data' in page
        
        # Check sections
        sections = page['elementor_data']
        assert len(sections) == 4
        
        for section in sections:
            assert section['elType'] == 'section'
            assert 'id' in section
            assert 'settings' in section
            assert 'elements' in section
        
        # Check first section (hero)
        hero_section = sections[0]
        assert len(hero_section['elements']) == 1  # 1 column
        assert hero_section['settings']['background_background'] == 'classic'
        assert 'shape_divider_bottom' in hero_section['settings']
        
        # Check column structure
        column = hero_section['elements'][0]
        assert column['elType'] == 'column'
        assert column['settings']['_column_size'] == '100'
        
        # Check widget
        widget = column['elements'][0]
        assert widget['elType'] == 'widget'
        assert widget['widgetType'] == 'cholot-title'
        assert 'Welcome to Our' in widget['settings']['title']
        
        print("✓ Basic processing test passed")
        return result
        
    except Exception as e:
        print(f"✗ Basic processing test failed: {str(e)}")
        raise


def test_widget_types():
    """Test different widget type processing"""
    print("Testing widget type processing...")
    
    processor = YAMLToJSONProcessor()
    
    # Test each widget type
    widget_tests = [
        {'type': 'texticon', 'title': 'Test', 'icon': 'fas fa-star'},
        {'type': 'title', 'title': 'Test Title', 'header_size': 'h2'},
        {'type': 'team', 'name': 'John Doe', 'position': 'Developer'},
        {'type': 'text-line', 'title': 'Test Line', 'line_width': 50},
        {'type': 'contact', 'shortcode': '[contact-form-7 id="1"]'},
        {'type': 'button-text', 'text': 'Click Me', 'link': 'https://example.com'},
        {'type': 'gallery', 'images': [1, 2, 3], 'columns': 3},
        {'type': 'post-three', 'count': 3, 'columns': 1},
        {'type': 'post-four', 'count': 4, 'columns': 2}
    ]
    
    for widget_test in widget_tests:
        test_yaml = {
            'site': {'title': 'Test'},
            'pages': [{
                'title': 'Test Page',
                'slug': 'test',
                'sections': [{
                    'structure': '100',
                    'columns': [{
                        'width': 100,
                        'widgets': [widget_test]
                    }]
                }]
            }]
        }
        
        try:
            result = processor.process_yaml_data(test_yaml)
            page = result['pages'][0]
            section = page['elementor_data'][0]
            column = section['elements'][0]
            widget = column['elements'][0]
            
            expected_widget_type = f"cholot-{widget_test['type']}"
            assert widget['widgetType'] == expected_widget_type
            
            print(f"✓ Widget type '{widget_test['type']}' processed correctly")
            
        except Exception as e:
            print(f"✗ Widget type '{widget_test['type']}' failed: {str(e)}")
            raise
    
    print("✓ Widget type processing tests passed")


def test_structure_validation():
    """Test structure validation"""
    print("Testing structure validation...")
    
    processor = YAMLToJSONProcessor()
    test_data = create_test_yaml()
    result = processor.process_yaml_data(test_data)
    
    try:
        is_valid = processor.validate_structure(result)
        assert is_valid, "Structure validation should pass"
        
        print("✓ Structure validation test passed")
        
    except Exception as e:
        print(f"✗ Structure validation test failed: {str(e)}")
        raise


def test_file_operations():
    """Test file save/load operations"""
    print("Testing file operations...")
    
    processor = YAMLToJSONProcessor()
    test_data = create_test_yaml()
    
    try:
        # Save test YAML
        yaml_file = 'test_input.yaml'
        with open(yaml_file, 'w') as f:
            yaml.dump(test_data, f, default_flow_style=False)
        
        # Process from file
        result = processor.process_yaml_file(yaml_file)
        
        # Save result
        json_file = 'test_output.json'
        processor.save_json(result, json_file)
        
        # Verify saved file exists and can be loaded
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data == result
        
        # Cleanup
        Path(yaml_file).unlink(missing_ok=True)
        Path(json_file).unlink(missing_ok=True)
        
        print("✓ File operations test passed")
        
    except Exception as e:
        print(f"✗ File operations test failed: {str(e)}")
        raise


def main():
    """Run all tests"""
    print("Running YAML to JSON Processor Tests")
    print("=" * 50)
    
    try:
        result = test_basic_processing()
        test_widget_types()
        test_structure_validation()
        test_file_operations()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        
        # Save a sample output for inspection
        processor = YAMLToJSONProcessor()
        processor.save_json(result, 'sample_output.json')
        print("Sample output saved to: sample_output.json")
        
        return 0
        
    except Exception as e:
        print(f"\nTest suite failed: {str(e)}")
        return 1


if __name__ == '__main__':
    exit(main())