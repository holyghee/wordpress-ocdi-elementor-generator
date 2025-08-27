#!/usr/bin/env python3
"""
Test Script for Cholot WordPress XML Generator
==============================================

This script demonstrates all the features and capabilities of the XML generator:
- Multiple input formats (YAML, JSON, Markdown)
- All 13 Cholot widget types
- Complex page hierarchies  
- Responsive settings
- Custom styling options
- XML validation

Run this script to generate test XML files and verify functionality.
"""

import sys
from pathlib import Path
import json
import yaml
import time

# Add the current directory to Python path to import our generator
sys.path.insert(0, str(Path(__file__).parent))

from generate_wordpress_xml import WordPressXMLGenerator, CholotComponentFactory


def test_basic_functionality():
    """Test basic generator functionality with simple data."""
    print("🧪 Testing Basic Functionality...")
    
    generator = WordPressXMLGenerator()
    
    # Simple test data
    test_data = {
        'pages': [
            {
                'title': 'Test Page',
                'slug': 'test-page',
                'sections': [
                    {
                        'structure': '100',
                        'columns': [
                            {
                                'width': 100,
                                'widgets': [
                                    {
                                        'type': 'title',
                                        'title': 'Test Title',
                                        'header_size': 'h2'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    site_config = {
        'title': 'Test Site',
        'description': 'Test Description',
        'base_url': 'http://localhost:8082'
    }
    
    xml_output = generator.generate_xml(test_data, site_config)
    
    # Validate XML
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(xml_output)
        print("✅ Basic functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_all_widget_types():
    """Test all 13 Cholot widget types."""
    print("🧪 Testing All Widget Types...")
    
    factory = CholotComponentFactory()
    
    # Test configurations for each widget type
    widget_tests = {
        'texticon': {
            'title': 'Test TextIcon',
            'icon': 'fas fa-star',
            'subtitle': 'Test Subtitle',
            'text': 'Test content'
        },
        'title': {
            'title': 'Test Title<span>.</span>',
            'header_size': 'h2',
            'align': 'center'
        },
        'post-three': {
            'post_count': 3,
            'column': 'one',
            'button_text': 'Read More'
        },
        'post-four': {
            'post_count': 4,
            'column': 'two',
            'categories': ['news']
        },
        'gallery': {
            'images': [
                'http://localhost:8082/image1.jpg',
                'http://localhost:8082/image2.jpg'
            ],
            'columns': 'col-md-4',
            'height': 200
        },
        'logo': {
            'url': 'http://localhost:8082/logo.png',
            'height': '80px',
            'align': 'center'
        },
        'menu': {
            'menu_name': 'main-menu',
            'align': 'right'
        },
        'button-text': {
            'text': 'Click Me',
            'url': 'http://example.com',
            'subtitle': 'Call to Action'
        },
        'team': {
            'name': 'John Doe',
            'position': 'CEO',
            'image_url': 'http://localhost:8082/team.jpg',
            'social_links': [
                {'icon': 'fab fa-linkedin', 'url': 'https://linkedin.com'}
            ]
        },
        'testimonial': {
            'columns': 3,
            'testimonials': [
                {
                    '_id': 'test1',
                    'name': 'Client Name',
                    'position': 'CEO',
                    'testimonial': 'Great service!'
                }
            ]
        },
        'text-line': {
            'title': 'Text Line Title',
            'subtitle': 'Subtitle',
            'line_width': 50
        },
        'contact': {
            'shortcode': '[contact-form-7 id="1"]'
        },
        'sidebar': {
            'width': '300px'
        }
    }
    
    # Test each widget type
    failed_widgets = []
    
    for widget_type, config in widget_tests.items():
        try:
            if widget_type == 'texticon':
                widget = factory.create_texticon_widget(config)
            elif widget_type == 'title':
                widget = factory.create_title_widget(config)
            elif widget_type in ['post-three', 'post-four']:
                post_type = widget_type.split('-')[1]
                widget = factory.create_post_widget(config, post_type)
            elif widget_type == 'gallery':
                widget = factory.create_gallery_widget(config)
            elif widget_type == 'logo':
                widget = factory.create_logo_widget(config)
            elif widget_type == 'menu':
                widget = factory.create_menu_widget(config)
            elif widget_type == 'button-text':
                widget = factory.create_button_text_widget(config)
            elif widget_type == 'team':
                widget = factory.create_team_widget(config)
            elif widget_type == 'testimonial':
                widget = factory.create_testimonial_widget(config)
            elif widget_type == 'text-line':
                widget = factory.create_text_line_widget(config)
            elif widget_type == 'contact':
                widget = factory.create_contact_widget(config)
            elif widget_type == 'sidebar':
                widget = factory.create_sidebar_widget(config)
            
            # Validate widget structure
            assert 'id' in widget
            assert 'widgetType' in widget
            assert widget['widgetType'].startswith('cholot-')
            assert 'settings' in widget
            
            print(f"  ✅ {widget_type} widget created successfully")
            
        except Exception as e:
            print(f"  ❌ {widget_type} widget failed: {e}")
            failed_widgets.append(widget_type)
    
    if failed_widgets:
        print(f"❌ Widget type tests failed for: {', '.join(failed_widgets)}")
        return False
    else:
        print("✅ All widget type tests passed")
        return True


def test_input_formats():
    """Test all supported input formats."""
    print("🧪 Testing Input Formats...")
    
    generator = WordPressXMLGenerator()
    
    # Test YAML
    yaml_content = """
    pages:
      - title: "YAML Test"
        slug: "yaml-test"
        sections:
          - structure: "100"
            columns:
              - width: 100
                widgets:
                  - type: "title"
                    title: "YAML Generated"
    """
    
    # Test JSON
    json_content = '''
    {
        "pages": [
            {
                "title": "JSON Test",
                "slug": "json-test",
                "sections": [
                    {
                        "structure": "100",
                        "columns": [
                            {
                                "width": 100,
                                "widgets": [
                                    {
                                        "type": "title",
                                        "title": "JSON Generated"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    '''
    
    # Test Markdown
    markdown_content = """---
pages:
  - title: "Markdown Test"
    slug: "markdown-test"
    sections:
      - structure: "100"
        columns:
          - width: 100
            widgets:
              - type: "title"
                title: "Markdown Generated"
---

# Test Content

This is markdown content that gets parsed.
"""
    
    formats = [
        ('YAML', yaml_content),
        ('JSON', json_content), 
        ('Markdown', markdown_content)
    ]
    
    failed_formats = []
    
    for format_name, content in formats:
        try:
            xml_output = generator.generate_xml(content)
            
            # Validate XML
            import xml.etree.ElementTree as ET
            ET.fromstring(xml_output)
            
            # Check that content was generated
            assert len(xml_output) > 1000  # Should be substantial XML
            assert f'{format_name.lower()}-test' in xml_output
            
            print(f"  ✅ {format_name} format processed successfully")
            
        except Exception as e:
            print(f"  ❌ {format_name} format failed: {e}")
            failed_formats.append(format_name)
    
    if failed_formats:
        print(f"❌ Input format tests failed for: {', '.join(failed_formats)}")
        return False
    else:
        print("✅ All input format tests passed")
        return True


def test_example_files():
    """Test the provided example files."""
    print("🧪 Testing Example Files...")
    
    generator = WordPressXMLGenerator()
    examples_dir = Path(__file__).parent / "examples"
    
    if not examples_dir.exists():
        print("⚠️  Examples directory not found, skipping example file tests")
        return True
    
    example_files = [
        ("YAML Example", "simple_page_example.yaml"),
        ("JSON Example", "complex_hierarchy_example.json"),
        ("Markdown Example", "markdown_content_example.md")
    ]
    
    failed_examples = []
    
    for example_name, filename in example_files:
        try:
            file_path = examples_dir / filename
            
            if not file_path.exists():
                print(f"  ⚠️  {filename} not found, skipping")
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract site config for YAML/JSON
            site_config = None
            if filename.endswith('.yaml'):
                data = yaml.safe_load(content)
                site_config = data.get('site', {})
            elif filename.endswith('.json'):
                data = json.loads(content)
                site_config = data.get('site', {})
            
            xml_output = generator.generate_xml(content, site_config)
            
            # Validate XML
            import xml.etree.ElementTree as ET
            ET.fromstring(xml_output)
            
            # Save test output
            output_path = Path(__file__).parent / f"test_output_{filename.split('.')[0]}.xml"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xml_output)
            
            print(f"  ✅ {example_name} processed successfully")
            print(f"     Output: {output_path}")
            
        except Exception as e:
            print(f"  ❌ {example_name} failed: {e}")
            failed_examples.append(example_name)
    
    if failed_examples:
        print(f"❌ Example file tests failed for: {', '.join(failed_examples)}")
        return False
    else:
        print("✅ All example file tests passed")
        return True


def test_xml_structure_compliance():
    """Test WordPress XML structure compliance."""
    print("🧪 Testing WordPress XML Structure Compliance...")
    
    generator = WordPressXMLGenerator()
    
    test_data = {
        'pages': [
            {
                'title': 'Structure Test',
                'slug': 'structure-test',
                'sections': [
                    {
                        'structure': '50',
                        'columns': [
                            {
                                'width': 50,
                                'widgets': [
                                    {
                                        'type': 'texticon',
                                        'title': 'Left Column',
                                        'icon': 'fas fa-left'
                                    }
                                ]
                            },
                            {
                                'width': 50,
                                'widgets': [
                                    {
                                        'type': 'texticon',
                                        'title': 'Right Column',
                                        'icon': 'fas fa-right'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    xml_output = generator.generate_xml(test_data)
    
    try:
        # Parse and validate XML structure
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_output)
        
        # Check basic WordPress XML structure
        assert root.tag == 'rss'
        assert root.get('version') == '2.0'
        
        # Check namespaces
        required_namespaces = [
            'http://wordpress.org/export/1.2/',
            'http://purl.org/rss/1.0/modules/content/',
            'http://wellformedweb.org/CommentAPI/',
            'http://purl.org/dc/elements/1.1/'
        ]
        
        for ns in required_namespaces:
            found = any(ns in attr for attr in root.attrib.values())
            assert found, f"Missing namespace: {ns}"
        
        # Check channel structure
        channel = root.find('channel')
        assert channel is not None
        
        # Check required channel elements
        required_elements = ['title', 'link', 'description', 'language']
        for element in required_elements:
            assert channel.find(element) is not None, f"Missing channel element: {element}"
        
        # Check for item (page) elements
        items = channel.findall('item')
        assert len(items) > 0, "No page items found"
        
        # Check item structure
        item = items[0]
        required_item_elements = ['title', 'guid', 'wp:post_type', 'wp:post_id']
        for element in required_item_elements:
            if ':' in element:
                # Handle namespaced elements
                ns, tag = element.split(':')
                ns_uri = f"{{{next(v for k, v in root.attrib.items() if k.endswith(ns))}}}"
                full_tag = f"{ns_uri}{tag}"
                assert item.find(full_tag) is not None, f"Missing item element: {element}"
            else:
                assert item.find(element) is not None, f"Missing item element: {element}"
        
        # Check for Elementor data
        elementor_data_found = False
        for postmeta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
            meta_key = postmeta.find('.//{http://wordpress.org/export/1.2/}meta_key')
            if meta_key is not None and meta_key.text == '_elementor_data':
                elementor_data_found = True
                break
        
        assert elementor_data_found, "Elementor data not found in postmeta"
        
        print("✅ WordPress XML structure compliance test passed")
        return True
        
    except Exception as e:
        print(f"❌ WordPress XML structure compliance test failed: {e}")
        return False


def run_performance_test():
    """Test performance with large datasets."""
    print("🧪 Running Performance Test...")
    
    generator = WordPressXMLGenerator()
    
    # Create large test dataset
    large_dataset = {
        'pages': []
    }
    
    # Generate 10 pages with multiple sections and widgets
    for i in range(10):
        page = {
            'title': f'Performance Test Page {i+1}',
            'slug': f'perf-test-{i+1}',
            'sections': []
        }
        
        # Add 5 sections per page
        for j in range(5):
            section = {
                'structure': '25',
                'columns': []
            }
            
            # Add 4 columns per section
            for k in range(4):
                column = {
                    'width': 25,
                    'widgets': [
                        {
                            'type': 'texticon',
                            'title': f'Widget {i+1}-{j+1}-{k+1}',
                            'icon': 'fas fa-star',
                            'text': f'Content for widget {i+1}-{j+1}-{k+1}'
                        }
                    ]
                }
                section['columns'].append(column)
            
            page['sections'].append(section)
        
        large_dataset['pages'].append(page)
    
    try:
        start_time = time.time()
        xml_output = generator.generate_xml(large_dataset)
        end_time = time.time()
        
        # Validate output
        import xml.etree.ElementTree as ET
        ET.fromstring(xml_output)
        
        processing_time = end_time - start_time
        output_size = len(xml_output)
        
        print(f"  ✅ Generated {len(large_dataset['pages'])} pages with 200 widgets")
        print(f"  ⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"  📄 Output size: {output_size:,} characters")
        
        # Performance thresholds
        if processing_time > 10.0:  # Should complete within 10 seconds
            print(f"  ⚠️  Performance warning: Processing took {processing_time:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting Cholot WordPress XML Generator Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("All Widget Types", test_all_widget_types),
        ("Input Formats", test_input_formats),
        ("Example Files", test_example_files),
        ("XML Structure Compliance", test_xml_structure_compliance),
        ("Performance", run_performance_test)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed_tests += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests / total_tests) * 100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The generator is ready for production use.")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)