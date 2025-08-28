#!/usr/bin/env python3
"""
Dynamic Template Processor - Adapts template structure based on input data
Can add/remove/duplicate widgets as needed
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List
from copy import deepcopy
import uuid
import re

class DynamicTemplateProcessor:
    def __init__(self):
        self.template_path = '/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json'
        
    def load_template(self) -> dict:
        """Load the full Elementor template"""
        with open(self.template_path, 'r') as f:
            return json.load(f)
    
    def generate_unique_id(self) -> str:
        """Generate unique Elementor element ID"""
        return uuid.uuid4().hex[:7]
    
    def clone_widget(self, widget: dict) -> dict:
        """Clone a widget with new unique IDs"""
        cloned = deepcopy(widget)
        cloned['id'] = self.generate_unique_id()
        
        # Recursively update IDs in nested elements
        if 'elements' in cloned:
            for element in cloned['elements']:
                self._update_element_ids(element)
        
        return cloned
    
    def _update_element_ids(self, element: dict):
        """Recursively update element IDs"""
        element['id'] = self.generate_unique_id()
        if 'elements' in element:
            for child in element['elements']:
                self._update_element_ids(child)
    
    def find_section_by_content(self, sections: List, content_type: str) -> tuple:
        """Find a section that contains specific widget types"""
        widget_map = {
            'hero': ['cholot-slider'],
            'services': ['cholot-texticon', 'cholot-iconbox'],
            'team': ['cholot-team'],
            'testimonials': ['cholot-testimonial'],
            'about': ['cholot-title', 'text-editor'],
            'contact': ['cholot-contact', 'contact-form']
        }
        
        target_widgets = widget_map.get(content_type, [])
        
        for i, section in enumerate(sections):
            if self._section_contains_widgets(section, target_widgets):
                return i, section
        
        return None, None
    
    def _section_contains_widgets(self, section: dict, widget_types: List[str]) -> bool:
        """Check if section contains any of the specified widget types"""
        def search_widgets(element):
            if isinstance(element, dict):
                if element.get('widgetType') in widget_types:
                    return True
                if 'elements' in element:
                    for child in element['elements']:
                        if search_widgets(child):
                            return True
            elif isinstance(element, list):
                for item in element:
                    if search_widgets(item):
                        return True
            return False
        
        return search_widgets(section)
    
    def process_yaml_to_elementor(self, yaml_path: str) -> tuple[Dict, List]:
        """Dynamically convert YAML to Elementor structure"""
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Load template
        template = self.load_template()
        
        # Start with basic structure
        if 'content' not in template or not template['content']:
            elementor_data = self._create_basic_structure()
        else:
            elementor_data = deepcopy(template['content'])
        
        # Get main container sections
        if elementor_data and 'elements' in elementor_data[0]:
            main_sections = elementor_data[0]['elements']
        else:
            main_sections = []
        
        # Process each section type from YAML
        pages = config.get('pages', [])
        if pages:
            page = pages[0]
            for section_config in page.get('sections', []):
                self._process_section(main_sections, section_config, template)
        
        return config, elementor_data
    
    def _create_basic_structure(self) -> List:
        """Create basic Elementor structure if template is empty"""
        return [{
            'id': self.generate_unique_id(),
            'elType': 'section',
            'settings': {},
            'elements': []
        }]
    
    def _process_section(self, sections: List, section_config: Dict, template: Dict):
        """Process a section from config and adapt template accordingly"""
        section_type = section_config.get('type')
        
        if section_type == 'hero_slider':
            self._process_hero_section(sections, section_config, template)
        elif section_type == 'service_cards':
            self._process_services_section(sections, section_config, template)
        elif section_type == 'team':
            self._process_team_section(sections, section_config, template)
        elif section_type == 'testimonials':
            self._process_testimonials_section(sections, section_config, template)
        elif section_type == 'about':
            self._process_about_section(sections, section_config, template)
        elif section_type == 'services_grid':
            self._process_services_grid(sections, section_config, template)
        elif section_type == 'contact':
            self._process_contact_section(sections, section_config, template)
    
    def _process_services_section(self, sections: List, config: Dict, template: Dict):
        """Dynamically process services - add more if needed"""
        services = config.get('services', [])
        if not services:
            return
        
        # Find existing services section
        section_idx, section = self.find_section_by_content(sections, 'services')
        
        if section is None:
            # Create new services section if not found
            section = self._create_services_section_structure(len(services))
            sections.append(section)
            section_idx = len(sections) - 1
        
        # Find service widgets in the section
        service_widgets = self._find_widgets_in_section(section, ['cholot-texticon', 'cholot-iconbox'])
        
        # If we need more widgets than exist, clone them
        if len(services) > len(service_widgets):
            # Find a template widget to clone
            if service_widgets:
                template_widget = service_widgets[0]
                parent_column = self._find_widget_parent(section, template_widget)
                
                # Calculate how many columns we need
                columns_needed = (len(services) + 1) // 2  # 2 widgets per column
                current_columns = self._count_columns_in_section(section)
                
                if columns_needed > current_columns:
                    # Need to add more columns
                    self._add_columns_to_section(section, columns_needed - current_columns, template_widget)
                
                # Now distribute widgets across columns
                self._distribute_service_widgets(section, services, template_widget)
            else:
                # No template widgets found, create from scratch
                self._create_service_widgets_from_scratch(section, services)
        else:
            # Just update existing widgets
            for widget, service in zip(service_widgets[:len(services)], services):
                self._update_service_widget(widget, service)
    
    def _find_widgets_in_section(self, section: dict, widget_types: List[str]) -> List[dict]:
        """Find all widgets of specified types in a section"""
        widgets = []
        
        def search(element):
            if isinstance(element, dict):
                if element.get('widgetType') in widget_types:
                    widgets.append(element)
                if 'elements' in element:
                    for child in element['elements']:
                        search(child)
            elif isinstance(element, list):
                for item in element:
                    search(item)
        
        search(section)
        return widgets
    
    def _find_widget_parent(self, root: dict, target_widget: dict) -> dict:
        """Find the parent element of a widget"""
        def search(element, parent=None):
            if element == target_widget:
                return parent
            if isinstance(element, dict) and 'elements' in element:
                for child in element['elements']:
                    result = search(child, element)
                    if result:
                        return result
            return None
        
        return search(root)
    
    def _count_columns_in_section(self, section: dict) -> int:
        """Count columns in a section"""
        if 'elements' in section:
            # First level elements in a section are usually columns
            return len([e for e in section['elements'] if e.get('elType') == 'column'])
        return 0
    
    def _add_columns_to_section(self, section: dict, count: int, template_widget: dict):
        """Add more columns to a section"""
        if 'elements' not in section:
            section['elements'] = []
        
        # Find existing column structure
        existing_columns = [e for e in section['elements'] if e.get('elType') == 'column']
        
        if existing_columns:
            # Clone existing column
            template_column = existing_columns[0]
            for _ in range(count):
                new_column = self.clone_widget(template_column)
                section['elements'].append(new_column)
        else:
            # Create new columns
            for _ in range(count):
                column = {
                    'id': self.generate_unique_id(),
                    'elType': 'column',
                    'settings': {
                        '_column_size': 50 if count == 1 else 33
                    },
                    'elements': []
                }
                section['elements'].append(column)
    
    def _distribute_service_widgets(self, section: dict, services: List[Dict], template_widget: dict):
        """Distribute service widgets across columns"""
        columns = [e for e in section.get('elements', []) if e.get('elType') == 'column']
        
        if not columns:
            return
        
        # Clear existing widgets
        for column in columns:
            column['elements'] = []
        
        # Distribute services across columns
        services_per_column = max(1, (len(services) + len(columns) - 1) // len(columns))
        
        for i, service in enumerate(services):
            column_idx = min(i // services_per_column, len(columns) - 1)
            column = columns[column_idx]
            
            # Clone template widget
            new_widget = self.clone_widget(template_widget)
            self._update_service_widget(new_widget, service)
            column['elements'].append(new_widget)
    
    def _update_service_widget(self, widget: dict, service: Dict):
        """Update a service widget with content"""
        settings = widget.get('settings', {})
        
        settings['title'] = service.get('title', '')
        settings['subtitle'] = service.get('subtitle', '')
        settings['text'] = service.get('text', '')
        
        if service.get('icon'):
            settings['selected_icon'] = {
                'value': service['icon'],
                'library': 'fa-solid'
            }
        
        if service.get('image'):
            settings['image'] = {
                'url': service['image'],
                'id': ''
            }
        
        widget['settings'] = settings
    
    def _create_services_section_structure(self, service_count: int) -> dict:
        """Create a services section structure from scratch"""
        columns_needed = min(4, max(2, (service_count + 1) // 2))
        column_width = 100 // columns_needed
        
        section = {
            'id': self.generate_unique_id(),
            'elType': 'section',
            'settings': {
                'structure': f'{columns_needed}',
                'layout': 'boxed',
                'gap': 'default'
            },
            'elements': []
        }
        
        # Add columns
        for _ in range(columns_needed):
            column = {
                'id': self.generate_unique_id(),
                'elType': 'column',
                'settings': {
                    '_column_size': column_width
                },
                'elements': []
            }
            section['elements'].append(column)
        
        return section
    
    def _create_service_widgets_from_scratch(self, section: dict, services: List[Dict]):
        """Create service widgets from scratch when no template exists"""
        columns = [e for e in section.get('elements', []) if e.get('elType') == 'column']
        
        services_per_column = max(1, (len(services) + len(columns) - 1) // len(columns))
        
        for i, service in enumerate(services):
            column_idx = min(i // services_per_column, len(columns) - 1)
            column = columns[column_idx]
            
            widget = {
                'id': self.generate_unique_id(),
                'elType': 'widget',
                'widgetType': 'cholot-texticon',
                'settings': {
                    'title': service.get('title', ''),
                    'subtitle': service.get('subtitle', ''),
                    'text': service.get('text', ''),
                    'selected_icon': {
                        'value': service.get('icon', 'fas fa-check'),
                        'library': 'fa-solid'
                    }
                }
            }
            
            if service.get('image'):
                widget['settings']['image'] = {
                    'url': service['image'],
                    'id': ''
                }
            
            column['elements'].append(widget)
    
    def _process_team_section(self, sections: List, config: Dict, template: Dict):
        """Dynamically process team members"""
        members = config.get('members', [])
        if not members:
            return
        
        section_idx, section = self.find_section_by_content(sections, 'team')
        
        if section is None:
            section = self._create_team_section_structure(len(members))
            sections.append(section)
        else:
            # Adapt existing section
            team_widgets = self._find_widgets_in_section(section, ['cholot-team'])
            
            if len(members) > len(team_widgets) and team_widgets:
                # Clone widgets as needed
                template_widget = team_widgets[0]
                parent = self._find_widget_parent(section, template_widget)
                
                for _ in range(len(members) - len(team_widgets)):
                    new_widget = self.clone_widget(template_widget)
                    if parent and 'elements' in parent:
                        parent['elements'].append(new_widget)
            
            # Update all team widgets
            team_widgets = self._find_widgets_in_section(section, ['cholot-team'])
            for widget, member in zip(team_widgets[:len(members)], members):
                self._update_team_widget(widget, member)
    
    def _update_team_widget(self, widget: dict, member: Dict):
        """Update team widget with member data"""
        settings = widget.get('settings', {})
        
        settings['title'] = member.get('name', '')
        settings['text'] = member.get('position', '')
        
        if member.get('image'):
            settings['image'] = {
                'url': member['image'],
                'id': ''
            }
        
        if member.get('bio'):
            settings['description'] = member['bio']
        
        # Social links
        if member.get('social'):
            social_list = []
            for platform, url in member['social'].items():
                icon_map = {
                    'linkedin': 'fab fa-linkedin',
                    'twitter': 'fab fa-twitter',
                    'xing': 'fab fa-xing',
                    'facebook': 'fab fa-facebook'
                }
                social_list.append({
                    '_id': self.generate_unique_id(),
                    'social_icon': {
                        'value': icon_map.get(platform, 'fas fa-link'),
                        'library': 'fa-brands' if platform in icon_map else 'fa-solid'
                    },
                    'link': {'url': url}
                })
            settings['social_icon_list'] = social_list
        
        widget['settings'] = settings
    
    def _create_team_section_structure(self, member_count: int) -> dict:
        """Create team section from scratch"""
        columns_needed = min(4, max(2, member_count))
        
        section = {
            'id': self.generate_unique_id(),
            'elType': 'section',
            'settings': {
                'structure': f'{columns_needed}',
                'layout': 'boxed'
            },
            'elements': []
        }
        
        # Add columns with team widgets
        for _ in range(columns_needed):
            column = {
                'id': self.generate_unique_id(),
                'elType': 'column',
                'settings': {
                    '_column_size': 100 // columns_needed
                },
                'elements': []
            }
            section['elements'].append(column)
        
        return section
    
    def _process_testimonials_section(self, sections: List, config: Dict, template: Dict):
        """Process testimonials dynamically"""
        testimonials = config.get('testimonials', [])
        if not testimonials:
            return
        
        section_idx, section = self.find_section_by_content(sections, 'testimonials')
        
        if section:
            test_widgets = self._find_widgets_in_section(section, ['cholot-testimonial'])
            
            # Clone or create widgets as needed
            if len(testimonials) > len(test_widgets) and test_widgets:
                template_widget = test_widgets[0]
                parent = self._find_widget_parent(section, template_widget)
                
                for _ in range(len(testimonials) - len(test_widgets)):
                    new_widget = self.clone_widget(template_widget)
                    if parent and 'elements' in parent:
                        parent['elements'].append(new_widget)
            
            # Update widgets
            test_widgets = self._find_widgets_in_section(section, ['cholot-testimonial'])
            for widget, testimonial in zip(test_widgets[:len(testimonials)], testimonials):
                self._update_testimonial_widget(widget, testimonial)
    
    def _update_testimonial_widget(self, widget: dict, testimonial: Dict):
        """Update testimonial widget"""
        settings = widget.get('settings', {})
        
        settings['text'] = testimonial.get('text', '')
        settings['name'] = testimonial.get('name', '')
        settings['subtitle'] = testimonial.get('position', '')
        
        if testimonial.get('image'):
            settings['image'] = {
                'url': testimonial['image'],
                'id': ''
            }
        
        if testimonial.get('rating'):
            settings['rating'] = testimonial['rating']
        
        widget['settings'] = settings
    
    def _process_hero_section(self, sections: List, config: Dict, template: Dict):
        """Process hero slider section"""
        slides = config.get('slides', [])
        if not slides:
            return
        
        section_idx, section = self.find_section_by_content(sections, 'hero')
        
        if section:
            slider_widgets = self._find_widgets_in_section(section, ['cholot-slider'])
            
            for slider in slider_widgets:
                if slides:
                    slide = slides[0]  # Use first slide for now
                    settings = slider.get('settings', {})
                    settings['title'] = slide.get('title', '')
                    settings['editor'] = slide.get('text', '')
                    settings['cholot_btn_text'] = slide.get('button_text', '')
                    settings['cholot_btn_link'] = {'url': slide.get('button_link', '#')}
                    
                    if slide.get('image'):
                        settings['background_image'] = {
                            'url': slide['image'],
                            'id': ''
                        }
                    
                    slider['settings'] = settings
    
    def _process_about_section(self, sections: List, config: Dict, template: Dict):
        """Process about section"""
        section_idx, section = self.find_section_by_content(sections, 'about')
        
        if section:
            title_widgets = self._find_widgets_in_section(section, ['cholot-title', 'heading'])
            text_widgets = self._find_widgets_in_section(section, ['text-editor'])
            
            if config.get('title'):
                for widget in title_widgets:
                    widget['settings']['title'] = config['title']
            
            if config.get('content'):
                for widget in text_widgets:
                    widget['settings']['editor'] = config['content']
            
            # Process features if present
            if config.get('features'):
                self._process_features(section, config['features'])
    
    def _process_features(self, section: dict, features: List[Dict]):
        """Process feature items within a section"""
        icon_widgets = self._find_widgets_in_section(section, ['icon-box', 'cholot-iconbox'])
        
        if len(features) > len(icon_widgets) and icon_widgets:
            # Clone widgets
            template_widget = icon_widgets[0]
            parent = self._find_widget_parent(section, template_widget)
            
            for _ in range(len(features) - len(icon_widgets)):
                new_widget = self.clone_widget(template_widget)
                if parent and 'elements' in parent:
                    parent['elements'].append(new_widget)
        
        # Update widgets
        icon_widgets = self._find_widgets_in_section(section, ['icon-box', 'cholot-iconbox'])
        for widget, feature in zip(icon_widgets[:len(features)], features):
            settings = widget.get('settings', {})
            settings['title_text'] = feature.get('title', '')
            settings['description_text'] = feature.get('text', '')
            
            if feature.get('icon'):
                settings['selected_icon'] = {
                    'value': feature['icon'],
                    'library': 'fa-solid'
                }
            
            widget['settings'] = settings
    
    def _process_services_grid(self, sections: List, config: Dict, template: Dict):
        """Process grid-style services"""
        services = config.get('services', [])
        if not services:
            return
        
        # Create a grid section
        grid_section = {
            'id': self.generate_unique_id(),
            'elType': 'section',
            'settings': {
                'layout': 'boxed',
                'content_width': {'unit': 'px', 'size': 1140}
            },
            'elements': [{
                'id': self.generate_unique_id(),
                'elType': 'column',
                'settings': {'_column_size': 100},
                'elements': []
            }]
        }
        
        # Add title if provided
        if config.get('title'):
            title_widget = {
                'id': self.generate_unique_id(),
                'elType': 'widget',
                'widgetType': 'heading',
                'settings': {
                    'title': config['title'],
                    'align': 'center',
                    'header_size': 'h2'
                }
            }
            grid_section['elements'][0]['elements'].append(title_widget)
        
        # Create icon grid
        icon_list = {
            'id': self.generate_unique_id(),
            'elType': 'widget',
            'widgetType': 'icon-list',
            'settings': {
                'icon_list': []
            }
        }
        
        for service in services:
            item = {
                '_id': self.generate_unique_id(),
                'text': service.get('title', ''),
                'selected_icon': {
                    'value': service.get('icon', 'fas fa-check'),
                    'library': 'fa-solid'
                }
            }
            icon_list['settings']['icon_list'].append(item)
        
        grid_section['elements'][0]['elements'].append(icon_list)
        sections.append(grid_section)
    
    def _process_contact_section(self, sections: List, config: Dict, template: Dict):
        """Process contact section"""
        section_idx, section = self.find_section_by_content(sections, 'contact')
        
        if section:
            # Update contact widgets
            contact_widgets = self._find_widgets_in_section(section, ['cholot-contact'])
            
            for widget in contact_widgets:
                settings = widget.get('settings', {})
                
                if config.get('info'):
                    for info_item in config['info']:
                        if 'phone' in info_item.get('label', '').lower():
                            settings['phone'] = info_item.get('value', '')
                        elif 'email' in info_item.get('label', '').lower():
                            settings['email'] = info_item.get('value', '')
                        elif 'address' in info_item.get('label', '').lower():
                            settings['address'] = info_item.get('value', '')
                
                widget['settings'] = settings
    
    def generate_wordpress_xml(self, config: Dict, elementor_data: List, output_path: str):
        """Generate WordPress XML with dynamic content"""
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
        
        # Add categories and terms
        self._add_categories_and_terms(channel)
        
        # Add Default Kit
        self._add_default_kit(channel, config)
        
        # Add Page with Elementor data
        self._add_page_item(channel, config, elementor_data)
        
        # Format and save XML
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Pretty print
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
        
        # Clean and write
        lines = pretty_xml.decode('utf-8').split('\n')
        clean_lines = [line for line in lines if line.strip()]
        clean_xml = '\n'.join(clean_lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_xml)
        
        return output_path
    
    def _add_categories_and_terms(self, channel):
        """Add WordPress categories and Elementor terms"""
        category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = '1'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = 'uncategorized'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = 'Uncategorized'
        
        for term_id, slug in [('2', 'page'), ('3', 'kit')]:
            term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_id').text = term_id
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'elementor_library_type'
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_slug').text = slug
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_parent').text = ''
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_name').text = slug
    
    def _add_default_kit(self, channel, config):
        """Add Default Kit item"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = 'Default Kit'
        ET.SubElement(item, 'link').text = 'http://localhost/?elementor_library=default-kit'
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = 'http://localhost/?post_type=elementor_library&p=99'
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        for key, value in [
            ('post_id', '99'),
            ('post_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('post_date_gmt', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('post_modified', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('post_modified_gmt', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('comment_status', 'closed'),
            ('ping_status', 'closed'),
            ('post_name', 'default-kit'),
            ('status', 'publish'),
            ('post_parent', '0'),
            ('menu_order', '0'),
            ('post_type', 'elementor_library'),
            ('post_password', ''),
            ('is_sticky', '0')
        ]:
            ET.SubElement(item, f'{{http://wordpress.org/export/1.2/}}{key}').text = value
        
        # Category
        cat = ET.SubElement(item, 'category', domain='elementor_library_type', nicename='kit')
        cat.text = 'kit'
        
        # Kit settings
        page = config.get('pages', [{}])[0]
        elementor_settings = page.get('elementor_settings', {})
        
        kit_settings = {
            "system_colors": [
                {"_id": "primary", "title": "Primary", "color": elementor_settings.get('primary_color', '#b68c2f')},
                {"_id": "secondary", "title": "Secondary", "color": elementor_settings.get('secondary_color', '#232323')},
                {"_id": "text", "title": "Text", "color": elementor_settings.get('text_color', '#7A7A7A')},
                {"_id": "accent", "title": "Accent", "color": "#61CE70"}
            ],
            "system_typography": [
                {"_id": "primary", "title": "Primary", "typography_typography": "custom"},
                {"_id": "secondary", "title": "Secondary", "typography_typography": "custom"},
                {"_id": "text", "title": "Text", "typography_typography": "custom"},
                {"_id": "accent", "title": "Accent", "typography_typography": "custom"}
            ],
            "default_generic_fonts": "Sans-serif",
            "site_name": config.get('site', {}).get('title', 'Website'),
            "site_description": config.get('site', {}).get('description', ''),
            "container_width": {"size": elementor_settings.get('container_width', 1140), "unit": "px"}
        }
        
        # Add meta
        for key, value in [
            ('_elementor_edit_mode', 'builder'),
            ('_elementor_template_type', 'kit'),
            ('_elementor_version', '3.15.0'),
            ('_elementor_page_settings', json.dumps(kit_settings))
        ]:
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
    
    def _add_page_item(self, channel, config, elementor_data):
        """Add page item with Elementor data"""
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
        
        # Elementor meta
        for key, value in [
            ('_elementor_edit_mode', 'builder'),
            ('_elementor_template_type', 'wp-page'),
            ('_elementor_version', '3.15.0'),
            ('_elementor_pro_version', '3.15.0'),
            ('_elementor_data', json.dumps(elementor_data)),
            ('_elementor_page_settings', '{}'),
            ('_wp_page_template', page.get('template', 'elementor_canvas'))
        ]:
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value


def main():
    print("🚀 Dynamic Template Processor")
    print("=" * 50)
    
    processor = DynamicTemplateProcessor()
    
    # Process YAML dynamically
    config, elementor_data = processor.process_yaml_to_elementor('riman_input.yaml')
    
    # Save Elementor JSON
    with open('riman_dynamic.json', 'w') as f:
        json.dump({'content': elementor_data}, f, indent=2)
    
    print(f"✅ Generated dynamic Elementor JSON: {len(json.dumps(elementor_data))} characters")
    
    # Generate WordPress XML
    output_path = processor.generate_wordpress_xml(config, elementor_data, 'riman_dynamic.xml')
    
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
    print(f"✅ Dynamic WordPress XML generated: {output_path}")


if __name__ == "__main__":
    main()