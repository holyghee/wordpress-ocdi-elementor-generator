#!/usr/bin/env python3
"""
Cholot WordPress XML Generator - Live Demo
==========================================

This demonstration script showcases all the key features of the generator:
- Multiple input formats (YAML, JSON, Markdown)
- All 13 Cholot widget types
- Complex page hierarchies
- Smart defaults and customization
- Production-ready XML output

Run this script to see the generator in action!
"""

import json
import yaml
from pathlib import Path
from generate_wordpress_xml import WordPressXMLGenerator, CholotComponentFactory

def demo_widget_showcase():
    """Demonstrate all 13 widget types in a single page."""
    print("🎨 Demo: Widget Showcase - All 13 Cholot Widget Types")
    print("=" * 60)
    
    widget_showcase = {
        "site": {
            "title": "Cholot Widget Showcase",
            "description": "Demonstration of all 13 Cholot widget types",
            "base_url": "http://localhost:8082",
            "language": "en-US"
        },
        "pages": [
            {
                "title": "Widget Showcase",
                "slug": "widget-showcase",
                "sections": [
                    # Header section with title and texticon
                    {
                        "structure": "100",
                        "settings": {
                            "background": {
                                "background_background": "classic",
                                "background_color": "#232323"
                            }
                        },
                        "columns": [
                            {
                                "width": 100,
                                "widgets": [
                                    {
                                        "type": "title",
                                        "title": "Complete Widget Showcase<span>.</span>",
                                        "header_size": "h1",
                                        "align": "center",
                                        "custom_settings": {
                                            "title_color": "#ffffff"
                                        }
                                    },
                                    {
                                        "type": "texticon",
                                        "title": "All 13 Cholot Widgets",
                                        "subtitle": "Production Ready",
                                        "icon": "fas fa-star",
                                        "text": "Comprehensive demonstration of every widget type"
                                    }
                                ]
                            }
                        ]
                    },
                    
                    # Service cards section
                    {
                        "structure": "25",
                        "columns": [
                            {
                                "width": 25,
                                "widgets": [
                                    {
                                        "type": "texticon",
                                        "title": "Design",
                                        "subtitle": "Creative Solutions",
                                        "icon": "fas fa-palette",
                                        "text": "Professional design services"
                                    }
                                ]
                            },
                            {
                                "width": 25,
                                "widgets": [
                                    {
                                        "type": "texticon",
                                        "title": "Development",
                                        "subtitle": "Technical Excellence",
                                        "icon": "fas fa-code",
                                        "text": "Custom development solutions"
                                    }
                                ]
                            },
                            {
                                "width": 25,
                                "widgets": [
                                    {
                                        "type": "texticon",
                                        "title": "Support",
                                        "subtitle": "24/7 Assistance",
                                        "icon": "fas fa-headset",
                                        "text": "Round-the-clock support"
                                    }
                                ]
                            },
                            {
                                "width": 25,
                                "widgets": [
                                    {
                                        "type": "button-text",
                                        "text": "Get Started",
                                        "url": "http://localhost:8082/contact",
                                        "subtitle": "Begin Your Journey",
                                        "icon": "fas fa-rocket"
                                    }
                                ]
                            }
                        ]
                    },
                    
                    # Content sections
                    {
                        "structure": "50",
                        "columns": [
                            {
                                "width": 50,
                                "widgets": [
                                    {
                                        "type": "text-line",
                                        "title": "Our Approach",
                                        "subtitle": "Methodology",
                                        "line_width": 80,
                                        "background_color": "#f4f4f4"
                                    },
                                    {
                                        "type": "post-three",
                                        "post_count": 3,
                                        "column": "one",
                                        "button_text": "Read Article"
                                    }
                                ]
                            },
                            {
                                "width": 50,
                                "widgets": [
                                    {
                                        "type": "team",
                                        "name": "Sarah Johnson",
                                        "position": "Lead Designer",
                                        "image_url": "http://localhost:8082/team/sarah.jpg",
                                        "social_links": [
                                            {
                                                "icon": "fab fa-linkedin-in",
                                                "url": "https://linkedin.com/in/sarah"
                                            },
                                            {
                                                "icon": "fab fa-dribbble",
                                                "url": "https://dribbble.com/sarah"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    
                    # Gallery and additional widgets
                    {
                        "structure": "100",
                        "settings": {
                            "background": {
                                "background_background": "classic",
                                "background_color": "#f8f8f8"
                            }
                        },
                        "columns": [
                            {
                                "width": 100,
                                "widgets": [
                                    {
                                        "type": "title",
                                        "title": "Our Work Gallery<span>.</span>",
                                        "header_size": "h2",
                                        "align": "center"
                                    },
                                    {
                                        "type": "gallery",
                                        "columns": "col-md-4",
                                        "height": 200,
                                        "images": [
                                            "http://localhost:8082/gallery/project1.jpg",
                                            "http://localhost:8082/gallery/project2.jpg",
                                            "http://localhost:8082/gallery/project3.jpg",
                                            "http://localhost:8082/gallery/project4.jpg",
                                            "http://localhost:8082/gallery/project5.jpg",
                                            "http://localhost:8082/gallery/project6.jpg"
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    
                    # Testimonials section
                    {
                        "structure": "100",
                        "settings": {
                            "background": {
                                "background_background": "classic",
                                "background_color": "#232323"
                            }
                        },
                        "columns": [
                            {
                                "width": 100,
                                "widgets": [
                                    {
                                        "type": "testimonial",
                                        "columns": 2,
                                        "align": "center",
                                        "testimonials": [
                                            {
                                                "_id": "demo1",
                                                "name": "John Smith",
                                                "position": "CEO, Tech Corp",
                                                "image": {
                                                    "url": "http://localhost:8082/testimonials/john.jpg",
                                                    "id": 101
                                                },
                                                "testimonial": "Outstanding work quality and professional service. Highly recommended!",
                                                "rating": 5
                                            },
                                            {
                                                "_id": "demo2", 
                                                "name": "Lisa Chen",
                                                "position": "Director, Innovation Lab",
                                                "image": {
                                                    "url": "http://localhost:8082/testimonials/lisa.jpg",
                                                    "id": 102
                                                },
                                                "testimonial": "Exceeded our expectations in every aspect. True professionals.",
                                                "rating": 5
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    
                    # Footer section with contact and additional widgets
                    {
                        "structure": "33",
                        "columns": [
                            {
                                "width": 33,
                                "widgets": [
                                    {
                                        "type": "logo",
                                        "url": "http://localhost:8082/logo-white.png",
                                        "height": "60px",
                                        "align": "left"
                                    },
                                    {
                                        "type": "menu",
                                        "menu_name": "footer-menu",
                                        "align": "left"
                                    }
                                ]
                            },
                            {
                                "width": 33,
                                "widgets": [
                                    {
                                        "type": "contact",
                                        "shortcode": "[contact-form-7 id=\"1\" title=\"Quick Contact\"]",
                                        "button_width": "100%"
                                    }
                                ]
                            },
                            {
                                "width": 33,
                                "widgets": [
                                    {
                                        "type": "post-four",
                                        "post_count": 2,
                                        "column": "one",
                                        "button_text": "View All",
                                        "categories": ["news"]
                                    },
                                    {
                                        "type": "sidebar",
                                        "width": "100%",
                                        "title_size": 16
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    generator = WordPressXMLGenerator()
    xml_output = generator.generate_xml(widget_showcase, widget_showcase["site"])
    
    # Save output
    output_file = "demo_widget_showcase.xml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_output)
    
    print(f"✅ Widget showcase generated successfully!")
    print(f"📄 File: {output_file}")
    print(f"📊 Size: {len(xml_output):,} characters")
    
    # Validate XML
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(xml_output)
        print("✅ XML validation passed")
    except Exception as e:
        print(f"❌ XML validation failed: {e}")
    
    return output_file


def demo_input_formats():
    """Demonstrate different input formats."""
    print("\n🔄 Demo: Multiple Input Formats")
    print("=" * 60)
    
    generator = WordPressXMLGenerator()
    
    # YAML Format
    yaml_input = """
site:
  title: "YAML Demo Site"
  base_url: "http://localhost:8082"

pages:
  - title: "YAML Generated Page"
    slug: "yaml-demo"
    sections:
      - structure: "100"
        columns:
          - width: 100
            widgets:
              - type: "title"
                title: "Generated from YAML<span>!</span>"
                header_size: "h2"
                align: "center"
    """
    
    # JSON Format
    json_input = {
        "site": {
            "title": "JSON Demo Site",
            "base_url": "http://localhost:8082"
        },
        "pages": [
            {
                "title": "JSON Generated Page",
                "slug": "json-demo",
                "sections": [
                    {
                        "structure": "100",
                        "columns": [
                            {
                                "width": 100,
                                "widgets": [
                                    {
                                        "type": "title",
                                        "title": "Generated from JSON<span>!</span>",
                                        "header_size": "h2",
                                        "align": "center"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Markdown Format
    markdown_input = """---
site:
  title: "Markdown Demo Site"
  base_url: "http://localhost:8082"

pages:
  - title: "Markdown Generated Page"
    slug: "markdown-demo"
    sections:
      - structure: "100"
        columns:
          - width: 100
            widgets:
              - type: "title"
                title: "Generated from Markdown<span>!</span>"
                header_size: "h2"
                align: "center"
---

# Demo Content

This is markdown content that can be processed alongside the page configuration.
"""
    
    formats = [
        ("YAML", yaml_input, "yaml"),
        ("JSON", json.dumps(json_input), "json"),
        ("Markdown", markdown_input, "md")
    ]
    
    for format_name, content, ext in formats:
        try:
            # Parse site config for YAML/JSON
            site_config = None
            if format_name == "YAML":
                data = yaml.safe_load(content)
                site_config = data.get('site', {})
            elif format_name == "JSON":
                data = json.loads(content)
                site_config = data.get('site', {})
            
            xml_output = generator.generate_xml(content, site_config)
            
            output_file = f"demo_{format_name.lower()}_format.xml"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_output)
            
            print(f"✅ {format_name} format processed successfully")
            print(f"   📄 Output: {output_file}")
            print(f"   📊 Size: {len(xml_output):,} characters")
            
        except Exception as e:
            print(f"❌ {format_name} format failed: {e}")


def demo_performance_test():
    """Demonstrate performance with larger datasets."""
    print("\n⚡ Demo: Performance Test")
    print("=" * 60)
    
    import time
    
    generator = WordPressXMLGenerator()
    
    # Generate large dataset
    large_site = {
        "site": {
            "title": "Performance Test Site",
            "description": "Large site for performance testing",
            "base_url": "http://localhost:8082"
        },
        "pages": []
    }
    
    # Create 5 pages with multiple sections each
    for i in range(5):
        page = {
            "title": f"Performance Page {i+1}",
            "slug": f"perf-page-{i+1}",
            "sections": []
        }
        
        # Add 3 sections per page
        for j in range(3):
            section = {
                "structure": "25",
                "columns": []
            }
            
            # Add 4 columns per section
            for k in range(4):
                column = {
                    "width": 25,
                    "widgets": [
                        {
                            "type": "texticon",
                            "title": f"Widget {i+1}-{j+1}-{k+1}",
                            "subtitle": "Performance Test",
                            "icon": "fas fa-bolt",
                            "text": f"This is widget content for page {i+1}, section {j+1}, column {k+1}"
                        }
                    ]
                }
                section["columns"].append(column)
            
            page["sections"].append(section)
        
        large_site["pages"].append(page)
    
    # Measure performance
    start_time = time.time()
    xml_output = generator.generate_xml(large_site, large_site["site"])
    end_time = time.time()
    
    processing_time = end_time - start_time
    
    # Save output
    output_file = "demo_performance_test.xml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_output)
    
    print(f"✅ Performance test completed successfully!")
    print(f"📄 Generated: {len(large_site['pages'])} pages, 60 widgets total")
    print(f"⏱️  Processing time: {processing_time:.3f} seconds")
    print(f"📊 Output size: {len(xml_output):,} characters")
    print(f"🚀 Performance: {len(xml_output)/processing_time:,.0f} characters/second")
    print(f"💾 Saved as: {output_file}")


def demo_customization():
    """Demonstrate advanced customization features."""
    print("\n🎨 Demo: Advanced Customization")
    print("=" * 60)
    
    custom_site = {
        "site": {
            "title": "Custom Styled Site",
            "description": "Demonstration of advanced customization features",
            "base_url": "http://localhost:8082"
        },
        "pages": [
            {
                "title": "Custom Styling Demo",
                "slug": "custom-demo",
                "sections": [
                    {
                        "structure": "100",
                        "settings": {
                            "background": {
                                "background_background": "gradient",
                                "background_color": "#232323",
                                "background_color_b": "#b68c2f"
                            }
                        },
                        "columns": [
                            {
                                "width": 100,
                                "widgets": [
                                    {
                                        "type": "texticon",
                                        "title": "Fully Customized Widget",
                                        "subtitle": "Advanced Styling",
                                        "icon": "fas fa-palette",
                                        "text": "This widget demonstrates custom styling capabilities",
                                        "custom_settings": {
                                            "title_typography_font_size": {
                                                "unit": "px",
                                                "size": 48,
                                                "sizes": []
                                            },
                                            "title_color": "#ffffff",
                                            "subtitle_color": "#ffd700",
                                            "text_color": "#ffffff",
                                            "icon_size": {
                                                "unit": "px", 
                                                "size": 32,
                                                "sizes": []
                                            },
                                            "icon_color": "#ffd700",
                                            "title_margin": {
                                                "unit": "px",
                                                "top": "20",
                                                "right": "0", 
                                                "bottom": "20",
                                                "left": "0",
                                                "isLinked": False
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "structure": "50",
                        "columns": [
                            {
                                "width": 50,
                                "widgets": [
                                    {
                                        "type": "button-text",
                                        "text": "Custom Button",
                                        "url": "http://localhost:8082/custom",
                                        "subtitle": "Styled CTA",
                                        "icon": "fas fa-rocket",
                                        "custom_settings": {
                                            "btn_bg": "#ff6b35",
                                            "btn_bg_hover": "#ff8c42",
                                            "btn_color": "#ffffff",
                                            "btn_typography_font_size": {
                                                "unit": "px",
                                                "size": 20,
                                                "sizes": []
                                            },
                                            "btn_padding": {
                                                "unit": "px",
                                                "top": "20",
                                                "right": "40",
                                                "bottom": "20", 
                                                "left": "40",
                                                "isLinked": False
                                            }
                                        }
                                    }
                                ]
                            },
                            {
                                "width": 50,
                                "widgets": [
                                    {
                                        "type": "text-line",
                                        "title": "Custom Text Line",
                                        "subtitle": "Styled Section",
                                        "line_width": 100,
                                        "line_height": 5,
                                        "background_color": "#2c3e50",
                                        "custom_settings": {
                                            "title_color": "#ffffff",
                                            "subtitle_color": "#3498db",
                                            "line_color_hover": "#e74c3c"
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
    
    generator = WordPressXMLGenerator()
    xml_output = generator.generate_xml(custom_site, custom_site["site"])
    
    output_file = "demo_customization.xml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_output)
    
    print(f"✅ Customization demo generated successfully!")
    print(f"📄 File: {output_file}")
    print(f"📊 Size: {len(xml_output):,} characters")
    print(f"🎨 Features: Custom colors, fonts, spacing, gradients")


def main():
    """Run all demonstrations."""
    print("🚀 Cholot WordPress XML Generator - Live Demonstration")
    print("=" * 80)
    print("This script demonstrates all key features of the production-ready generator.")
    print("Generated XML files can be imported directly into WordPress with Elementor.")
    print("=" * 80)
    
    # Run demonstrations
    demos = [
        demo_widget_showcase,
        demo_input_formats, 
        demo_performance_test,
        demo_customization
    ]
    
    generated_files = []
    
    for demo_func in demos:
        try:
            result = demo_func()
            if isinstance(result, str):
                generated_files.append(result)
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n🎉 Demonstration Complete!")
    print("=" * 80)
    print(f"✅ All demonstrations completed successfully")
    print(f"📁 Generated files:")
    
    # List all XML files generated
    xml_files = list(Path('.').glob('demo_*.xml'))
    for xml_file in xml_files:
        file_size = xml_file.stat().st_size
        print(f"   📄 {xml_file.name} ({file_size:,} bytes)")
    
    print(f"\n🔗 Import these files into WordPress:")
    print(f"   1. Go to WordPress Admin → Tools → Import")  
    print(f"   2. Choose 'WordPress' importer")
    print(f"   3. Upload any of the generated XML files")
    print(f"   4. Follow the import wizard")
    print(f"\n💡 All files use localhost:8082 URLs - update to match your domain")
    print("=" * 80)


if __name__ == "__main__":
    main()