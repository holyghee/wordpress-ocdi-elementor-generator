#!/usr/bin/env python3
"""
Section-Based Processor - Uses classic Section/Column structure for maximum compatibility
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List
from copy import deepcopy
import uuid

class SectionBasedProcessor:
    def __init__(self):
        pass
    
    def generate_unique_id(self) -> str:
        """Generate unique Elementor element ID"""
        return uuid.uuid4().hex[:7]
    
    def process_yaml_to_elementor(self, yaml_path: str) -> tuple:
        """Convert YAML to classic Section/Column Elementor structure"""
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Create classic Elementor structure with sections
        elementor_data = self._create_sections_page(config)
        
        return config, elementor_data
    
    def _create_sections_page(self, config: Dict) -> List:
        """Create page using classic sections/columns structure"""
        page = config.get('pages', [{}])[0]
        sections = page.get('sections', [])
        
        elementor_sections = []
        
        # Process each section from config
        for section_config in sections:
            section = self._create_section(section_config)
            if section:
                # Handle both single sections and lists of sections
                if isinstance(section, list):
                    elementor_sections.extend(section)
                else:
                    elementor_sections.append(section)
        
        return elementor_sections
    
    def _create_section(self, config: Dict):
        """Create a section with columns"""
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
        """Create hero section with classic structure"""
        slides = config.get('slides', [])
        if not slides:
            return None
        
        slide = slides[0]
        
        return {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "height": "min-height",
                "custom_height": {"unit": "vh", "size": 100},
                "background_background": "classic",
                "background_image": {"url": slide.get('image', '')},
                "background_position": "center center",
                "background_repeat": "no-repeat",
                "background_size": "cover",
                "background_overlay_background": "classic",
                "background_overlay_color": "rgba(0,0,0,0.4)",
                "content_position": "middle",
                "align": "center"
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 100
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
                        "title_color": "#ffffff"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='text-align: center;'>{slide.get('text', '')}</p>",
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
                        "button_background_color": "#b68c2f",
                        "border_radius": {"unit": "px", "size": 5}
                    }
                }]
            }]
        }
    
    def _create_services_section(self, config: Dict) -> List[Dict]:
        """Create services section - returns TWO sections: title section + services section"""
        services = config.get('services', [])
        if not services:
            return []
        
        # Section 1: Title and subtitle (separate section)
        title_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "content_width": {"unit": "px", "size": 1140},
                "margin": {"unit": "px", "top": 80, "bottom": 40},
                "padding": {"unit": "px", "top": 0, "bottom": 0}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'Our Services'),
                        "size": "xl",
                        "align": "center",
                        "title_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='text-align: center;'>{config.get('subtitle', '')}</p>",
                        "text_color": "#666666"
                    }
                }]
            }]
        }
        
        # Section 2: Service cards (separate section) 
        service_columns = []
        for service in services[:4]:  # Max 4 services
            column = {
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 25 if len(services) >= 4 else 100 // min(len(services), 3)
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "icon-box",
                    "settings": {
                        "selected_icon": {
                            "value": service.get('icon', 'fas fa-check'),
                            "library": "fa-solid"
                        },
                        "title_text": service.get('title', ''),
                        "description_text": f"<strong>{service.get('subtitle', '')}</strong><br>{service.get('text', '')}",
                        "title_size": "medium",
                        "position": "top",
                        "icon_primary_color": "#b68c2f",
                        "title_color": "#232323",
                        "description_color": "#666666",
                        "content_vertical_alignment": "top",
                        "link": {"url": ""} if not service.get('link') else {"url": service.get('link', '')}
                    }
                }]
            }
            service_columns.append(column)
        
        services_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "content_width": {"unit": "px", "size": 1140},
                "margin": {"unit": "px", "top": 0, "bottom": 80},
                "padding": {"unit": "px", "top": 0, "bottom": 0}
            },
            "elements": service_columns
        }
        
        # Return both sections as a list
        return [title_section, services_section]
    
    def _create_team_section(self, config: Dict) -> List[Dict]:
        """Create team section - returns TWO sections: title section + team members section"""
        members = config.get('members', [])
        if not members:
            return []
        
        # Section 1: Title (separate section)
        title_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 40}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'Our Team'),
                        "size": "xl",
                        "align": "center",
                        "title_color": "#232323"
                    }
                }]
            }]
        }
        
        # Section 2: Team members (separate section)
        team_columns = []
        for member in members[:3]:  # Max 3 members
            column = {
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 33.33
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": member.get('image', '')},
                        "image_size": "medium",
                        "align": "center",
                        "border_radius": {"unit": "%", "size": 50}
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": member.get('name', ''),
                        "size": "medium",
                        "align": "center",
                        "title_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='text-align: center;'><em>{member.get('position', '')}</em></p><p style='text-align: center;'>{member.get('bio', '')}</p>",
                        "text_color": "#666666"
                    }
                }]
            }
            team_columns.append(column)
        
        team_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 0, "bottom": 80}
            },
            "elements": team_columns
        }
        
        # Return both sections
        return [title_section, team_section]
    
    def _create_about_section(self, config: Dict) -> Dict:
        """Create about section with text and image"""
        return {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 80}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 50
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'About Us'),
                        "size": "xl",
                        "title_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p>{config.get('content', '')}</p>",
                        "text_color": "#666666"
                    }
                }]
            }, {
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 50
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": config.get('image', '')},
                        "image_size": "large",
                        "border_radius": {"unit": "px", "size": 8}
                    }
                }]
            }]
        }
    
    def _create_testimonials_section(self, config: Dict) -> List[Dict]:
        """Create testimonials section - returns TWO sections: title section + testimonials section"""
        testimonials = config.get('testimonials', [])
        if not testimonials:
            return []
        
        # Section 1: Title and subtitle (separate section)
        title_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 40},
                "background_background": "classic",
                "background_color": "#f8f9fa",
                "padding": {"unit": "px", "top": 60, "bottom": 20}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'What Our Clients Say'),
                        "size": "xl",
                        "align": "center",
                        "title_color": "#232323"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='text-align: center;'>{config.get('subtitle', '')}</p>",
                        "text_color": "#666666"
                    }
                }]
            }]
        }
        
        # Section 2: Testimonial cards (separate section)
        testimonial_columns = []
        for testimonial in testimonials[:3]:  # Max 3 testimonials
            column = {
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {
                    "_column_size": 33.33 if len(testimonials) >= 3 else 50 if len(testimonials) == 2 else 100
                },
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "testimonial",
                    "settings": {
                        "testimonial_content": testimonial.get('text', ''),
                        "testimonial_name": testimonial.get('name', ''),
                        "testimonial_job": testimonial.get('position', ''),
                        "testimonial_image": {"url": testimonial.get('image', '')},
                        "testimonial_alignment": "center",
                        "testimonial_image_size": "custom",
                        "testimonial_image_custom_dimension": {"width": 80, "height": 80},
                        "testimonial_name_color": "#232323",
                        "testimonial_job_color": "#666666",
                        "testimonial_content_color": "#333333"
                    }
                }]
            }
            testimonial_columns.append(column)
        
        testimonials_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 0, "bottom": 80},
                "background_background": "classic",
                "background_color": "#f8f9fa",
                "padding": {"unit": "px", "top": 20, "bottom": 60}
            },
            "elements": testimonial_columns
        }
        
        # Return both sections
        return [title_section, testimonials_section]
    
    def _create_services_grid_section(self, config: Dict) -> List[Dict]:
        """Create additional services grid - returns TWO sections: title section + services grid section"""
        services = config.get('services', [])
        if not services:
            return []
        
        # Section 1: Title (separate section)
        title_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 40}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'Additional Services'),
                        "size": "xl",
                        "align": "center",
                        "title_color": "#232323"
                    }
                }]
            }]
        }
        
        # Section 2: Services grid (separate section)
        grid_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 0, "bottom": 80}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
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
                        "text_color": "#232323",
                        "divider": "yes",
                        "divider_style": "solid",
                        "divider_weight": {"unit": "px", "size": 1},
                        "divider_color": "#e6e6e6"
                    }
                }]
            }]
        }
        
        # Return both sections
        return [title_section, grid_section]
    
    def _create_contact_section(self, config: Dict) -> List[Dict]:
        """Create contact section - returns TWO sections: title section + contact info section"""
        info = config.get('info', [])
        
        # Section 1: Title and text (separate section)
        title_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 80, "bottom": 40},
                "background_background": "classic",
                "background_color": config.get('background_color', '#1f1f1f'),
                "padding": {"unit": "px", "top": 80, "bottom": 20}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": config.get('title', 'Contact Us'),
                        "size": "xl",
                        "align": "center",
                        "title_color": "#ffffff"
                    }
                }, {
                    "id": self.generate_unique_id(),
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='text-align: center;'>{config.get('text', '')}</p>",
                        "text_color": "#cccccc"
                    }
                }]
            }]
        }
        
        # Section 2: Contact info (separate section)
        info_widgets = []
        for item in info:
            info_widgets.append({
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
            })
        
        contact_section = {
            "id": self.generate_unique_id(),
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "margin": {"unit": "px", "top": 0, "bottom": 80},
                "background_background": "classic",
                "background_color": config.get('background_color', '#1f1f1f'),
                "padding": {"unit": "px", "top": 20, "bottom": 80}
            },
            "elements": [{
                "id": self.generate_unique_id(),
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": info_widgets
            }]
        }
        
        # Return both sections
        return [title_section, contact_section]
    
    def generate_wordpress_xml(self, config: Dict, elementor_data: List, output_path: str):
        """Generate WordPress XML with section-based structure"""
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
        
        # Add categories
        category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = '1'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = 'uncategorized'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = 'Uncategorized'
        
        # Add page
        self._add_page_item(channel, config, elementor_data)
        
        # Format and save XML
        xml_string = ET.tostring(rss, encoding='unicode')
        
        try:
            dom = minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
            
            lines = pretty_xml.decode('utf-8').split('\n')
            clean_lines = [line for line in lines if line.strip()]
            clean_xml = '\n'.join(clean_lines)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_xml)
        except Exception as e:
            print(f"Warning: Using fallback XML formatting: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                f.write(xml_string)
        
        return output_path
    
    def _add_page_item(self, channel, config, elementor_data):
        """Add page item with section-based Elementor data"""
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
        
        # Clean JSON
        clean_json = json.dumps(elementor_data, separators=(',', ':'))
        
        # Elementor meta - minimal set
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
    print("🚀 Section-Based Processor (Maximum Compatibility)")
    print("=" * 60)
    
    processor = SectionBasedProcessor()
    
    # Process YAML to section-based Elementor structure
    config, elementor_data = processor.process_yaml_to_elementor('riman_input.yaml')
    
    # Save Elementor JSON
    with open('riman_sections.json', 'w') as f:
        json.dump({'content': elementor_data}, f, indent=2)
    
    print(f"✅ Generated section-based Elementor JSON: {len(json.dumps(elementor_data))} characters")
    
    # Generate WordPress XML
    output_path = processor.generate_wordpress_xml(config, elementor_data, 'riman_sections.xml')
    
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
    print(f"✅ Compatible WordPress XML generated: {output_path}")
    print("\n💡 This uses classic Section/Column structure for maximum compatibility!")


if __name__ == "__main__":
    main()