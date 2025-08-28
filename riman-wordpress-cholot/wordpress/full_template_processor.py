#!/usr/bin/env python3
"""
Full Template Processor - Uses complete Elementor template to generate 80KB WordPress XML
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List
from copy import deepcopy
import re

class FullTemplateProcessor:
    def __init__(self):
        self.template_path = '/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json'
        
    def load_template(self) -> dict:
        """Load the full Elementor template"""
        with open(self.template_path, 'r') as f:
            return json.load(f)
    
    def process_yaml_to_elementor(self, yaml_path: str) -> tuple[Dict, Dict]:
        """Convert YAML to full Elementor structure using complete template"""
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Load full template
        template = self.load_template()
        elementor_data = deepcopy(template['content'])
        
        # Update content while preserving ALL structure and styling
        self._update_hero_section(elementor_data, config)
        self._update_services_section(elementor_data, config)
        self._update_about_section(elementor_data, config)
        self._update_team_section(elementor_data, config)
        self._update_testimonials_section(elementor_data, config)
        self._update_contact_section(elementor_data, config)
        
        return config, elementor_data
    
    def _find_widget_by_type(self, elements: List, widget_type: str):
        """Recursively find widgets by type"""
        widgets = []
        for element in elements:
            if isinstance(element, dict):
                if element.get('widgetType') == widget_type:
                    widgets.append(element)
                if 'elements' in element:
                    widgets.extend(self._find_widget_by_type(element['elements'], widget_type))
        return widgets
    
    def _update_hero_section(self, data: List, config: Dict):
        """Update hero slider content"""
        pages = config.get('pages', [])
        if not pages:
            return
            
        page = pages[0]
        sections = page.get('sections', [])
        hero = next((s for s in sections if s['type'] == 'hero_slider'), None)
        
        if hero and hero.get('slides'):
            # Find cholot-slider widgets
            sliders = self._find_widget_by_type(data, 'cholot-slider')
            
            if sliders:
                slider = sliders[0]
                slide_data = hero['slides'][0]
                
                # Update settings with new content
                settings = slider.get('settings', {})
                settings['title'] = slide_data.get('title', '')
                settings['editor'] = slide_data.get('text', '')
                settings['cholot_btn_text'] = slide_data.get('button_text', 'Learn More')
                settings['cholot_btn_link'] = {'url': slide_data.get('button_link', '#')}
                
                # Keep all other styling intact
    
    def _update_services_section(self, data: List, config: Dict):
        """Update services cards"""
        pages = config.get('pages', [])
        if not pages:
            return
            
        page = pages[0]
        sections = page.get('sections', [])
        services = next((s for s in sections if s['type'] == 'service_cards'), None)
        
        if services and services.get('services'):
            # Find cholot-texticon widgets
            texticons = self._find_widget_by_type(data, 'cholot-texticon')
            
            for i, (widget, service) in enumerate(zip(texticons[:4], services['services'][:4])):
                settings = widget.get('settings', {})
                settings['title'] = service.get('title', '')
                settings['subtitle'] = service.get('subtitle', '')
                settings['text'] = service.get('text', '')
                
                # Update icon
                if service.get('icon'):
                    settings['selected_icon'] = {
                        'value': service['icon'],
                        'library': 'fa-solid'
                    }
    
    def _update_about_section(self, data: List, config: Dict):
        """Update about section"""
        pages = config.get('pages', [])
        if not pages:
            return
            
        page = pages[0]
        sections = page.get('sections', [])
        about = next((s for s in sections if s['type'] == 'about'), None)
        
        if about:
            # Find cholot-title widgets in about section
            titles = self._find_widget_by_type(data, 'cholot-title')
            
            for title_widget in titles:
                settings = title_widget.get('settings', {})
                if 'about' in settings.get('title', '').lower() or 'über' in settings.get('title', '').lower():
                    settings['title'] = about.get('title', 'About Us')
                    settings['editor'] = about.get('content', '')
    
    def _update_team_section(self, data: List, config: Dict):
        """Update team members"""
        pages = config.get('pages', [])
        if not pages:
            return
            
        page = pages[0]
        sections = page.get('sections', [])
        team = next((s for s in sections if s['type'] == 'team'), None)
        
        if team and team.get('members'):
            # Find cholot-team widgets
            team_widgets = self._find_widget_by_type(data, 'cholot-team')
            
            for widget, member in zip(team_widgets[:3], team['members'][:3]):
                settings = widget.get('settings', {})
                settings['title'] = member.get('name', '')
                settings['text'] = member.get('position', '')
                
                if member.get('image'):
                    settings['image'] = {
                        'url': member['image'],
                        'id': ''
                    }
    
    def _update_testimonials_section(self, data: List, config: Dict):
        """Update testimonials"""
        pages = config.get('pages', [])
        if not pages:
            return
            
        page = pages[0]
        sections = page.get('sections', [])
        testimonials = next((s for s in sections if s['type'] == 'testimonials'), None)
        
        if testimonials and testimonials.get('testimonials'):
            # Find cholot-testimonial widgets
            test_widgets = self._find_widget_by_type(data, 'cholot-testimonial')
            
            for widget, testimonial in zip(test_widgets[:3], testimonials['testimonials'][:3]):
                settings = widget.get('settings', {})
                settings['text'] = testimonial.get('text', '')
                settings['name'] = testimonial.get('name', '')
                settings['subtitle'] = testimonial.get('position', '')
                
                if testimonial.get('image'):
                    settings['image'] = {
                        'url': testimonial['image'],
                        'id': ''
                    }
    
    def _update_contact_section(self, data: List, config: Dict):
        """Update contact information"""
        company = config.get('company', {})
        
        # Find contact-related widgets
        contact_widgets = self._find_widget_by_type(data, 'cholot-contact')
        
        for widget in contact_widgets:
            settings = widget.get('settings', {})
            settings['phone'] = company.get('phone', '')
            settings['email'] = company.get('email', '')
            settings['address'] = company.get('address', '')
    
    def generate_wordpress_xml(self, config: Dict, elementor_data: List, output_path: str):
        """Generate WordPress XML with full content"""
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
        
        # Add Page with full Elementor data
        self._add_page_with_full_data(channel, config, elementor_data)
        
        # Format and save XML
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Pretty print
        dom = minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
        
        # Clean up and write
        lines = pretty_xml.decode('utf-8').split('\n')
        clean_lines = [line for line in lines if line.strip()]
        clean_xml = '\n'.join(clean_lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_xml)
        
        return output_path
    
    def _add_categories_and_terms(self, channel):
        """Add WordPress categories and Elementor terms"""
        # Add default category
        category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = '1'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = 'uncategorized'
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = 'Uncategorized'
        
        # Add Elementor library terms
        for term_id, slug in [('2', 'page'), ('3', 'kit')]:
            term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_id').text = term_id
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'elementor_library_type'
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_slug').text = slug
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_parent').text = ''
            ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_name').text = slug
    
    def _add_default_kit(self, channel, config):
        """Add Default Kit with settings"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = 'Default Kit'
        ET.SubElement(item, 'link').text = 'http://localhost:8082/?elementor_library=default-kit'
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = 'http://localhost:8082/?post_type=elementor_library&p=99'
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = '99'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = 'default-kit'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'elementor_library'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # Category
        cat = ET.SubElement(item, 'category', domain='elementor_library_type', nicename='kit')
        cat.text = 'kit'
        
        # Kit settings meta
        page = config.get('pages', [{}])[0]
        elementor_settings = page.get('elementor_settings', {})
        
        kit_settings = {
            "system_colors": [
                {"_id": "primary", "title": "Primary", "color": elementor_settings.get('primary_color', '#b68c2f')},
                {"_id": "secondary", "title": "Secondary", "color": elementor_settings.get('secondary_color', '#232323')},
                {"_id": "text", "title": "Text", "color": elementor_settings.get('text_color', '#7A7A7A')},
                {"_id": "accent", "title": "Accent", "color": "#61CE70"}
            ],
            "custom_colors": [],
            "system_typography": [
                {"_id": "primary", "title": "Primary", "typography_typography": "custom"},
                {"_id": "secondary", "title": "Secondary", "typography_typography": "custom"},
                {"_id": "text", "title": "Text", "typography_typography": "custom"},
                {"_id": "accent", "title": "Accent", "typography_typography": "custom"}
            ],
            "custom_typography": [],
            "default_generic_fonts": "Sans-serif",
            "site_name": config.get('site', {}).get('title', 'Website'),
            "site_description": config.get('site', {}).get('description', ''),
            "container_width": {"size": elementor_settings.get('container_width', 1140), "unit": "px"},
            "space_between_widgets": {"size": 20, "unit": "px"}
        }
        
        # Add post meta
        for key, value in [
            ('_elementor_edit_mode', 'builder'),
            ('_elementor_template_type', 'kit'),
            ('_elementor_version', '3.15.0'),
            ('_elementor_page_settings', json.dumps(kit_settings))
        ]:
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
    
    def _add_page_with_full_data(self, channel, config, elementor_data):
        """Add page with complete Elementor data from template"""
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
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = '100'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_modified_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page.get('slug', 'homepage')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = page.get('status', 'publish')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # Category
        cat = ET.SubElement(item, 'category', domain='category', nicename='uncategorized')
        cat.text = 'Uncategorized'
        
        # SEO meta
        seo = page.get('seo', {})
        for key, value in [
            ('_yoast_wpseo_title', seo.get('meta_title', page.get('title', 'Homepage'))),
            ('_yoast_wpseo_metadesc', seo.get('meta_description', '')),
            ('_yoast_wpseo_focuskw', ', '.join(seo.get('keywords', [])))
        ]:
            if value:
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
        
        # Add Elementor meta with FULL template data
        for key, value in [
            ('_elementor_edit_mode', 'builder'),
            ('_elementor_template_type', 'wp-page'),
            ('_elementor_version', '3.15.0'),
            ('_elementor_pro_version', '3.15.0'),
            ('_elementor_data', json.dumps(elementor_data)),  # Full template data
            ('_elementor_page_settings', '{}')
        ]:
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
        
        # WordPress page template
        meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_page_template'
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = page.get('template', 'elementor_canvas')


def main():
    print("🚀 Full Template Processor")
    print("=" * 50)
    
    processor = FullTemplateProcessor()
    
    # Process YAML to Elementor
    config, elementor_data = processor.process_yaml_to_elementor('riman_input.yaml')
    
    # Save Elementor JSON for debugging
    with open('riman_full_template.json', 'w') as f:
        json.dump({'content': elementor_data}, f, indent=2)
    
    print(f"✅ Generated Elementor JSON: {len(json.dumps(elementor_data))} characters")
    
    # Generate WordPress XML
    output_path = processor.generate_wordpress_xml(config, elementor_data, 'riman_full_output.xml')
    
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
    print(f"✅ WordPress XML generated: {output_path}")


if __name__ == "__main__":
    main()