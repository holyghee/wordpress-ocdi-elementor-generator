#!/usr/bin/env python3
"""
Fixed Template Processor - Generates valid Elementor data that WordPress can import
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List
from copy import deepcopy
import uuid

class FixedTemplateProcessor:
    def __init__(self):
        pass
    
    def generate_unique_id(self) -> str:
        """Generate unique Elementor element ID"""
        return uuid.uuid4().hex[:7]
    
    def process_yaml_to_elementor(self, yaml_path: str) -> tuple[Dict, List]:
        """Convert YAML to clean Elementor structure"""
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Create clean Elementor structure
        elementor_data = self._create_elementor_page(config)
        
        return config, elementor_data
    
    def _create_elementor_page(self, config: Dict) -> List:
        """Create complete Elementor page from YAML config"""
        page = config.get('pages', [{}])[0]
        sections = page.get('sections', [])
        
        # Main container
        container = {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "flex_direction": "column",
                "flex_wrap": "nowrap"
            },
            "elements": []
        }
        
        # Process each section
        for section_config in sections:
            section_element = self._create_section(section_config)
            if section_element:
                container["elements"].append(section_element)
        
        return [container]
    
    def _create_section(self, config: Dict) -> Dict:
        """Create a section based on config"""
        section_type = config.get('type')
        
        if section_type == 'hero_slider':
            return self._create_hero_section(config)
        elif section_type == 'service_cards':
            return self._create_services_section(config)
        elif section_type == 'team':
            return self._create_team_section(config)
        elif section_type == 'testimonials':
            return self._create_testimonials_section(config)
        elif section_type == 'about':
            return self._create_about_section(config)
        elif section_type == 'services_grid':
            return self._create_services_grid_section(config)
        elif section_type == 'contact':
            return self._create_contact_section(config)
        
        return None
    
    def _create_hero_section(self, config: Dict) -> Dict:
        """Create hero slider section"""
        slides = config.get('slides', [])
        if not slides:
            return None
        
        slide = slides[0]  # Use first slide
        
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "full_width",
                "height": "min-height",
                "custom_height": {"unit": "vh", "size": 100},
                "background_background": "classic",
                "background_image": {"url": slide.get('image', '')},
                "background_position": "center center",
                "background_repeat": "no-repeat",
                "background_size": "cover",
                "background_overlay_background": "classic",
                "background_overlay_color": "rgba(0,0,0,0.4)"
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": slide.get('title', ''),
                    "size": "xxl",
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 60},
                    "typography_font_weight": "700",
                    "text_color": "#ffffff"
                }
            }, {
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "settings": {
                    "editor": slide.get('text', ''),
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 18},
                    "text_color": "#ffffff"
                }
            }, {
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "button",
                "settings": {
                    "text": slide.get('button_text', 'Learn More'),
                    "link": {"url": slide.get('button_link', '#')},
                    "align": "center",
                    "size": "lg",
                    "typography_typography": "custom",
                    "typography_font_weight": "600",
                    "background_color": "#b68c2f",
                    "border_radius": {"unit": "px", "size": 5},
                    "box_shadow_box_shadow_type": "yes",
                    "box_shadow_box_shadow": {
                        "horizontal": 0,
                        "vertical": 4,
                        "blur": 8,
                        "spread": 0,
                        "color": "rgba(0,0,0,0.2)"
                    }
                }
            }]
        }
    
    def _create_services_section(self, config: Dict) -> Dict:
        """Create services section"""
        services = config.get('services', [])
        if not services:
            return None
        
        # Create title container
        title_container = {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 40}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config.get('title', 'Our Services'),
                    "size": "xl",
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 42},
                    "typography_font_weight": "700",
                    "text_color": "#232323"
                }
            }, {
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "settings": {
                    "editor": config.get('subtitle', ''),
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 16},
                    "text_color": "#666666"
                }
            }]
        }
        
        # Create services grid
        services_container = {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "flex_direction": "row",
                "flex_wrap": "wrap"
            },
            "elements": []
        }
        
        # Add service cards
        for service in services:
            service_card = {
                "id": self.generate_unique_id(),
                "elType": "container",
                "settings": {
                    "content_width": "full_width",
                    "width": {"unit": "%", "size": 25},
                    "padding": {"unit": "px", "top": 20, "right": 20, "bottom": 20, "left": 20},
                    "background_background": "classic",
                    "background_color": "#ffffff",
                    "border_radius": {"unit": "px", "size": 8},
                    "box_shadow_box_shadow_type": "yes",
                    "box_shadow_box_shadow": {
                        "horizontal": 0,
                        "vertical": 4,
                        "blur": 12,
                        "spread": 0,
                        "color": "rgba(0,0,0,0.1)"
                    }
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "icon",
                    "settings": {
                        "selected_icon": {
                            "value": service.get('icon', 'fas fa-check'),
                            "library": "fa-solid"
                        },
                        "size": "large",
                        "primary_color": "#b68c2f",
                        "align": "center"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": service.get('title', ''),
                        "size": "medium",
                        "align": "center",
                        "typography_typography": "custom",
                        "typography_font_size": {"unit": "px", "size": 24},
                        "typography_font_weight": "600",
                        "text_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p><strong>{service.get('subtitle', '')}</strong></p><p>{service.get('text', '')}</p>",
                        "align": "center",
                        "typography_typography": "custom",
                        "typography_font_size": {"unit": "px", "size": 14},
                        "text_color": "#666666"
                    }
                }]
            }
            services_container["elements"].append(service_card)
        
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed"
            },
            "elements": [title_container, services_container]
        }
    
    def _create_team_section(self, config: Dict) -> Dict:
        """Create team section"""
        members = config.get('members', [])
        if not members:
            return None
        
        # Create title
        title_container = {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 40}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config.get('title', 'Our Team'),
                    "size": "xl",
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 42},
                    "typography_font_weight": "700",
                    "text_color": "#232323"
                }
            }]
        }
        
        # Create team grid
        team_container = {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "flex_direction": "row",
                "flex_wrap": "wrap"
            },
            "elements": []
        }
        
        # Add team members
        for member in members[:3]:  # Limit to 3 members
            member_card = {
                "id": self.generate_unique_id(),
                "elType": "container",
                "settings": {
                    "content_width": "full_width",
                    "width": {"unit": "%", "size": 33.33},
                    "padding": {"unit": "px", "top": 20, "right": 20, "bottom": 20, "left": 20}
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": member.get('image', '')},
                        "align": "center",
                        "border_radius": {"unit": "px", "size": 50}
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": member.get('name', ''),
                        "size": "medium",
                        "align": "center",
                        "typography_typography": "custom",
                        "typography_font_size": {"unit": "px", "size": 22},
                        "typography_font_weight": "600",
                        "text_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p><em>{member.get('position', '')}</em></p><p>{member.get('bio', '')}</p>",
                        "align": "center",
                        "typography_typography": "custom",
                        "typography_font_size": {"unit": "px", "size": 14},
                        "text_color": "#666666"
                    }
                }]
            }
            team_container["elements"].append(member_card)
        
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed"
            },
            "elements": [title_container, team_container]
        }
    
    def _create_testimonials_section(self, config: Dict) -> Dict:
        """Create testimonials section"""
        testimonials = config.get('testimonials', [])
        if not testimonials:
            return None
        
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 80},
                "background_background": "classic",
                "background_color": "#f8f9fa",
                "padding": {"unit": "px", "top": 60, "bottom": 60}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config.get('title', 'What Our Clients Say'),
                    "size": "xl",
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 42},
                    "typography_font_weight": "700",
                    "text_color": "#232323"
                }
            }, {
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "testimonial",
                "settings": {
                    "testimonial_content": testimonials[0].get('text', ''),
                    "testimonial_name": testimonials[0].get('name', ''),
                    "testimonial_job": testimonials[0].get('position', ''),
                    "testimonial_image": {"url": testimonials[0].get('image', '')},
                    "testimonial_alignment": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 16},
                    "text_color": "#666666"
                }
            }]
        }
    
    def _create_about_section(self, config: Dict) -> Dict:
        """Create about section"""
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 80},
                "flex_direction": "row"
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "container",
                "settings": {
                    "content_width": "full_width",
                    "width": {"unit": "%", "size": 50},
                    "padding": {"unit": "px", "right": 40}
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'About Us'),
                        "size": "xl",
                        "typography_typography": "custom",
                        "typography_font_size": {"unit": "px", "size": 42},
                        "typography_font_weight": "700",
                        "text_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p>{config.get('content', '')}</p>",
                        "typography_typography": "custom",
                        "typography_font_size": {"unit": "px", "size": 16},
                        "text_color": "#666666"
                    }
                }]
            }, {
                "id": self.generate_unique_id(),
                "elType": "container",
                "settings": {
                    "content_width": "full_width",
                    "width": {"unit": "%", "size": 50}
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": config.get('image', '')},
                        "border_radius": {"unit": "px", "size": 8}
                    }
                }]
            }]
        }
    
    def _create_services_grid_section(self, config: Dict) -> Dict:
        """Create services grid section"""
        services = config.get('services', [])
        if not services:
            return None
        
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 80}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config.get('title', 'Additional Services'),
                    "size": "xl",
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 36},
                    "typography_font_weight": "600",
                    "text_color": "#232323"
                }
            }, {
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "icon-list",
                "settings": {
                    "icon_list": [
                        {
                            "_id": self.generate_unique_id(),
                            "text": service.get('title', ''),
                            "selected_icon": {
                                "value": service.get('icon', 'fas fa-check'),
                                "library": "fa-solid"
                            }
                        } for service in services
                    ],
                    "space_between": {"unit": "px", "size": 15},
                    "icon_color": "#b68c2f",
                    "text_color": "#232323"
                }
            }]
        }
    
    def _create_contact_section(self, config: Dict) -> Dict:
        """Create contact section"""
        info = config.get('info', [])
        
        return {
            "id": self.generate_unique_id(),
            "elType": "container",
            "settings": {
                "content_width": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 80},
                "background_background": "classic",
                "background_color": config.get('background_color', '#1f1f1f'),
                "padding": {"unit": "px", "top": 80, "bottom": 80}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config.get('title', 'Contact Us'),
                    "size": "xl",
                    "align": "center",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 42},
                    "typography_font_weight": "700",
                    "text_color": "#ffffff"
                }
            }, {
                "id": self.generate_unique_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "settings": {
                    "editor": f"<p style='text-align: center;'>{config.get('text', '')}</p>",
                    "typography_typography": "custom",
                    "typography_font_size": {"unit": "px", "size": 16},
                    "text_color": "#cccccc"
                }
            }] + [
                {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "icon-box",
                    "settings": {
                        "selected_icon": {
                            "value": item.get('icon', 'fas fa-info'),
                            "library": "fa-solid"
                        },
                        "title_text": item.get('label', ''),
                        "description_text": item.get('value', ''),
                        "position": "left",
                        "icon_primary_color": "#b68c2f",
                        "title_color": "#ffffff",
                        "description_color": "#cccccc"
                    }
                } for item in info
            ]
        }
    
    def generate_wordpress_xml(self, config: Dict, elementor_data: List, output_path: str):
        """Generate clean WordPress XML"""
        # Register namespaces
        ET.register_namespace('excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
        ET.register_namespace('wfw', 'http://wellformedweb.org/CommentAPI/')
        ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
        ET.register_namespace('wp', 'http://wordpress.org/export/1.2/')
        
        # Create XML structure
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Site info
        site = config.get('site', {})
        ET.SubElement(channel, 'title').text = site.get('title', 'Website')
        ET.SubElement(channel, 'link').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site.get('description', '')
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = site.get('language', 'en-US')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = site.get('base_url', 'http://localhost')
        
        # Add author
        author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = '1'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = 'admin@example.com'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = 'Administrator'
        
        # Add minimal categories and terms
        self._add_categories_and_terms(channel)
        
        # Add page
        self._add_page_item(channel, config, elementor_data)
        
        # Format and save XML
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Clean formatting without minidom to avoid parsing issues
        # Write directly
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            f.write(xml_string)
        
        return output_path
    
    def _add_categories_and_terms(self, channel):
        """Add minimal required categories"""
        category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = '1'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = 'uncategorized'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = 'Uncategorized'
    
    def _add_page_item(self, channel, config, elementor_data):
        """Add page item with clean Elementor data"""
        page = config.get('pages', [{}])[0]
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = page.get('title', 'Homepage')
        ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url', 'http://localhost')}/{page.get('slug', 'homepage')}"
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"{config.get('site', {}).get('base_url', 'http://localhost')}/?page_id=100"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        for key, value in [
            ('post_id', '100'),
            ('post_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('post_date_gmt', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('post_modified', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('post_modified_gmt', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('comment_status', 'closed'),
            ('ping_status', 'closed'),
            ('post_name', page.get('slug', 'homepage')),
            ('status', page.get('status', 'publish')),
            ('post_parent', '0'),
            ('menu_order', '0'),
            ('post_type', 'page'),
            ('post_password', ''),
            ('is_sticky', '0')
        ]:
            ET.SubElement(item, f'{{http://wordpress.org/export/1.2/}}{key}').text = value
        
        # Category
        cat = ET.SubElement(item, 'category', domain='category', nicename='uncategorized')
        cat.text = 'Uncategorized'
        
        # Clean JSON without special characters that could break XML
        clean_json = json.dumps(elementor_data, separators=(',', ':'))
        
        # Elementor meta
        for key, value in [
            ('_elementor_edit_mode', 'builder'),
            ('_elementor_template_type', 'wp-page'),
            ('_elementor_version', '3.15.0'),
            ('_elementor_data', clean_json),
            ('_wp_page_template', page.get('template', 'elementor_canvas'))
        ]:
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value


def main():
    print("🚀 Fixed Template Processor")
    print("=" * 50)
    
    processor = FixedTemplateProcessor()
    
    # Process YAML to clean Elementor structure
    config, elementor_data = processor.process_yaml_to_elementor('riman_input.yaml')
    
    # Save Elementor JSON
    with open('riman_fixed.json', 'w') as f:
        json.dump({'content': elementor_data}, f, indent=2)
    
    print(f"✅ Generated clean Elementor JSON: {len(json.dumps(elementor_data))} characters")
    
    # Generate WordPress XML
    output_path = processor.generate_wordpress_xml(config, elementor_data, 'riman_fixed.xml')
    
    # Check file size
    import os
    file_size = os.path.getsize(output_path)
    print(f"📄 XML file size: {file_size / 1024:.1f} KB")
    
    # Count widgets
    def count_widgets(data, count=0):
        if isinstance(data, dict):
            if 'widgetType' in data:
                count += 1
            for v in data.values():
                count = count_widgets(v, count)
        elif isinstance(data, list):
            for item in data:
                count = count_widgets(item, count)
        return count
    
    widget_count = count_widgets(elementor_data)
    print(f"🎨 Total widgets: {widget_count}")
    print(f"✅ Clean WordPress XML generated: {output_path}")


if __name__ == "__main__":
    main()