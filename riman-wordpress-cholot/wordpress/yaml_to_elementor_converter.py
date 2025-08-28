#!/usr/bin/env python3
"""
YAML to Elementor Converter
Converts structured YAML input to complete Elementor JSON with all styling
"""

import yaml
import json
import uuid
from pathlib import Path
from copy import deepcopy
from typing import Dict, List, Any

class YamlToElementorConverter:
    def __init__(self, template_path: str = 'original-template.json'):
        """Initialize with original template for styling reference"""
        self.template_path = Path(template_path)
        if self.template_path.exists():
            with open(self.template_path, 'r', encoding='utf-8') as f:
                self.template = json.load(f)
                self.template_sections = self.template.get('content', [])
        else:
            # Try alternative path
            alt_path = Path('/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json')
            if alt_path.exists():
                with open(alt_path, 'r', encoding='utf-8') as f:
                    self.template = json.load(f)
                    self.template_sections = self.template.get('content', [])
            else:
                self.template_sections = []
                
    def generate_id(self) -> str:
        """Generate Elementor-compatible ID"""
        return ''.join(format(ord(c), 'x')[:2] for c in str(uuid.uuid4())[:8])
    
    def find_template_section(self, section_type: str) -> dict:
        """Find matching section template by type"""
        if section_type == 'hero_slider':
            for section in self.template_sections:
                for col in section.get('elements', []):
                    for widget in col.get('elements', []):
                        if widget.get('widgetType') == 'rdn-slider':
                            return deepcopy(section)
                            
        elif section_type == 'service_cards':
            for section in self.template_sections:
                if len(section.get('elements', [])) >= 3:
                    has_cards = False
                    for col in section['elements']:
                        for elem in col.get('elements', []):
                            if elem.get('elType') == 'section':
                                for subcol in elem.get('elements', []):
                                    for widget in subcol.get('elements', []):
                                        if widget.get('widgetType') == 'cholot-texticon':
                                            has_cards = True
                    if has_cards:
                        return deepcopy(section)
                        
        elif section_type == 'team':
            for section in self.template_sections:
                for col in section.get('elements', []):
                    for widget in col.get('elements', []):
                        if widget.get('widgetType') == 'cholot-team':
                            return deepcopy(section)
                            
        elif section_type == 'testimonials':
            for section in self.template_sections:
                for col in section.get('elements', []):
                    for elem in col.get('elements', []):
                        if elem.get('elType') == 'section':
                            for subcol in elem.get('elements', []):
                                for widget in subcol.get('elements', []):
                                    if widget.get('widgetType') == 'cholot-testimonial-two':
                                        return deepcopy(section)
                                        
        elif section_type == 'contact':
            for section in self.template_sections:
                for col in section.get('elements', []):
                    for widget in col.get('elements', []):
                        if widget.get('widgetType') == 'cholot-contact':
                            return deepcopy(section)
        
        # Default section structure
        return {
            "id": self.generate_id(),
            "settings": {
                "gap": "extended",
                "padding": {"unit": "px", "top": "60", "bottom": "60"}
            },
            "elements": [],
            "isInner": False,
            "elType": "section"
        }
    
    def build_hero_slider(self, section_data: dict) -> dict:
        """Build hero slider section"""
        template = self.find_template_section('hero_slider')
        
        # Find and update slider widget
        for col in template.get('elements', []):
            for widget in col.get('elements', []):
                if widget.get('widgetType') == 'rdn-slider':
                    slides = []
                    for slide_data in section_data.get('slides', []):
                        slide = {
                            "title": slide_data.get('title', ''),
                            "subtitle": slide_data.get('subtitle', ''),
                            "text": slide_data.get('text', ''),
                            "_id": self.generate_id()[:7],
                            "btn_text": slide_data.get('button_text', 'Mehr erfahren'),
                            "btn_link": {"url": slide_data.get('button_link', '#')},
                            "image": {
                                "url": slide_data.get('image', ''),
                                "id": int(self.generate_id()[:4], 16) % 10000,
                                "alt": slide_data.get('title', '').replace('<span>', '').replace('</span>', ''),
                                "source": "library",
                                "size": ""
                            }
                        }
                        slides.append(slide)
                    widget['settings']['slider_list'] = slides
        
        template['id'] = self.generate_id()
        return template
    
    def build_service_cards(self, section_data: dict) -> dict:
        """Build service cards section"""
        template = self.find_template_section('service_cards')
        services = section_data.get('services', [])
        
        # Clear existing columns
        template['elements'] = []
        
        # Create columns for each service
        for service in services[:4]:  # Max 4 services
            column = self.create_service_column(service)
            template['elements'].append(column)
        
        # Adjust column sizes
        col_size = 100 // len(template['elements']) if template['elements'] else 25
        for col in template['elements']:
            col['settings']['_column_size'] = col_size
        
        template['id'] = self.generate_id()
        return template
    
    def create_service_column(self, service: dict) -> dict:
        """Create a service column with image and text"""
        column = {
            "id": self.generate_id(),
            "settings": {
                "_column_size": 25,
                "_inline_size": None,
                "background_background": "classic",
                "background_color": "#fafafa",
                "border_width": {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "10", "isLinked": False},
                "border_color": "#ededed",
                "box_shadow_box_shadow": {"horizontal": 0, "vertical": 4, "blur": 5, "spread": 0, "color": "rgba(196,196,196,0.26)"},
                "box_shadow_box_shadow_type": "yes",
                "margin": {"unit": "px", "top": "15", "right": "15", "bottom": "15", "left": "15", "isLinked": True},
                "animation": "fadeInUp",
                "animation_duration": "fast"
            },
            "elements": [],
            "isInner": False,
            "elType": "column"
        }
        
        # Image section
        image_section = {
            "id": self.generate_id(),
            "settings": {
                "gap": "no",
                "shape_divider_bottom": "curve",
                "shape_divider_bottom_color": "#fafafa",
                "shape_divider_bottom_negative": "yes",
                "shape_divider_bottom_above_content": "yes"
            },
            "elements": [{
                "id": self.generate_id(),
                "settings": {"_column_size": 100, "_inline_size": None},
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {
                        "image": {
                            "url": service.get('image', ''),
                            "id": int(self.generate_id()[:4], 16) % 10000
                        },
                        "opacity": {"unit": "px", "size": 1, "sizes": []},
                        "_border_width": {"unit": "px", "top": "4", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                        "_border_color": "#b68c2f"
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "image",
                    "elType": "widget"
                }],
                "isInner": True,
                "elType": "column"
            }],
            "isInner": True,
            "elType": "section"
        }
        
        # Text content section
        text_section = {
            "id": self.generate_id(),
            "settings": {
                "gap": "no",
                "content_position": "middle",
                "background_background": "classic",
                "margin": {"unit": "px", "top": "-30", "right": 0, "bottom": "0", "left": 0, "isLinked": False},
                "z_index": 2
            },
            "elements": [{
                "id": self.generate_id(),
                "settings": {"_column_size": 100, "_inline_size": None},
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {
                        "icon": "fa fa-child",
                        "title_text_margin": {"unit": "px", "size": 50, "sizes": []},
                        "title": service.get('title', ''),
                        "title_typography_typography": "custom",
                        "title_typography_font_size": {"unit": "px", "size": 28, "sizes": []},
                        "title_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "15", "left": "0", "isLinked": False},
                        "subtitle": service.get('subtitle', ''),
                        "subtitle_typography_typography": "custom",
                        "subtitle_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
                        "subtitle_typography_font_weight": "700",
                        "subtitle_typography_text_transform": "uppercase",
                        "subtitle_typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
                        "subtitle_color": "#b68c2f",
                        "sb_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "-15", "left": "0", "isLinked": False},
                        "icon_size": {"unit": "px", "size": 20, "sizes": []},
                        "icon_bg_size": {"unit": "px", "size": 72, "sizes": []},
                        "selected_icon": {"value": service.get('icon', 'fas fa-check'), "library": "fa-solid"},
                        "__fa4_migrated": {"selected_icon": True},
                        "text": f"<p>{service.get('text', '')}</p>",
                        "text_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
                        "text_typography_font_style": "italic",
                        "text_margin": {"unit": "px", "top": "15", "right": "0", "bottom": "-30", "left": "0", "isLinked": False},
                        "icon_color": "#ffffff",
                        "iconbg_color": "#b68c2f",
                        "icon_bordering_border": "solid",
                        "icon_bordering_color": "#fafafa",
                        "_padding": {"unit": "px", "top": "30", "right": "30", "bottom": "30", "left": "30", "isLinked": True},
                        "_border_width": {"unit": "px", "top": "0", "right": "1", "bottom": "1", "left": "1", "isLinked": False},
                        "_border_color": "#b68c2f",
                        "_border_border": "dashed",
                        "icon_margin": {"unit": "px", "top": "-27", "right": 0, "bottom": "0", "left": 0, "isLinked": False},
                        "icon_bordering_width": {"unit": "px", "top": "7", "right": "7", "bottom": "7", "left": "7", "isLinked": True},
                        "icon_lheight": {"unit": "px", "size": 58, "sizes": []}
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "cholot-texticon",
                    "elType": "widget"
                }],
                "isInner": True,
                "elType": "column"
            }],
            "isInner": True,
            "elType": "section"
        }
        
        column['elements'] = [image_section, text_section]
        return column
    
    def build_team_section(self, section_data: dict) -> dict:
        """Build team section"""
        template = self.find_template_section('team')
        members = section_data.get('members', [])
        
        # Clear and rebuild columns
        template['elements'] = []
        
        for member in members[:3]:  # Max 3 members per row
            column = {
                "id": self.generate_id(),
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None,
                    "animation": "fadeInUp",
                    "animation_duration": "fast"
                },
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {
                        "title": member.get('name', ''),
                        "text": member.get('position', ''),
                        "image": {
                            "url": member.get('image', ''),
                            "id": int(self.generate_id()[:4], 16) % 10000,
                            "alt": member.get('name', ''),
                            "source": "library",
                            "size": ""
                        },
                        "team_height": {"unit": "px", "size": 420, "sizes": []},
                        "content_align": "left",
                        "titlep_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "5", "left": "0", "isLinked": False},
                        "txt_cl": "#b68c2f",
                        "social_icon_list": self.build_social_links(member.get('social', {})),
                        "hover_animation": "shrink",
                        "port_content": {"unit": "px", "top": "-80", "right": "15", "bottom": "0", "left": "15", "isLinked": False},
                        "cport_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
                        "title_cl": "#000000",
                        "bg_icon_color": "#b68c2f",
                        "bg_icon_size": {"unit": "px", "size": 110, "sizes": []},
                        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 8, "blur": 14, "spread": 4, "color": "rgba(175,175,175,0.27)"},
                        "box_shadow_box_shadow_type": "yes",
                        "background_background": "classic",
                        "background_color": "#f4f4f4",
                        "port_border_border": "solid",
                        "port_border_color": "#b68c2f",
                        "port_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "cholot-team",
                    "elType": "widget"
                }],
                "isInner": False,
                "elType": "column"
            }
            template['elements'].append(column)
        
        template['id'] = self.generate_id()
        return template
    
    def build_social_links(self, social_data: dict) -> List[dict]:
        """Build social media links for team member"""
        social_links = []
        
        icon_map = {
            'linkedin': 'fab fa-linkedin-in',
            'xing': 'fab fa-xing',
            'twitter': 'fab fa-twitter',
            'facebook': 'fab fa-facebook-f'
        }
        
        for platform, url in social_data.items():
            if platform in icon_map:
                social_links.append({
                    "social_icon": {"value": icon_map[platform], "library": "fa-brands"},
                    "_id": self.generate_id()[:7],
                    "link": {"url": url, "is_external": "true", "nofollow": ""},
                    "item_icon_color": "custom",
                    "item_icon_primary_color": "rgba(0,0,0,0)",
                    "item_icon_secondary_color": "#000000"
                })
        
        return social_links
    
    def build_testimonials_section(self, section_data: dict) -> dict:
        """Build testimonials section"""
        template = self.find_template_section('testimonials')
        testimonials = section_data.get('testimonials', [])
        
        # Find and update testimonial widget
        for col in template.get('elements', []):
            for elem in col.get('elements', []):
                if elem.get('elType') == 'section':
                    for subcol in elem.get('elements', []):
                        for widget in subcol.get('elements', []):
                            if widget.get('widgetType') == 'cholot-testimonial-two':
                                testi_list = []
                                for testi in testimonials:
                                    testi_list.append({
                                        "title": testi.get('name', ''),
                                        "position": testi.get('position', ''),
                                        "text": testi.get('text', ''),
                                        "_id": self.generate_id()[:7],
                                        "image": {
                                            "url": testi.get('image', ''),
                                            "id": int(self.generate_id()[:4], 16) % 10000
                                        },
                                        "image2_size": "thumbnail"
                                    })
                                widget['settings']['testi_list'] = testi_list
        
        # Update background image if provided
        if section_data.get('background_image'):
            template['settings']['background_image'] = {
                "url": section_data['background_image'],
                "id": int(self.generate_id()[:4], 16) % 10000
            }
        
        template['id'] = self.generate_id()
        return template
    
    def build_contact_section(self, section_data: dict) -> dict:
        """Build contact section"""
        template = self.find_template_section('contact')
        
        # Update contact content
        for col in template.get('elements', []):
            for widget in col.get('elements', []):
                if widget.get('widgetType') == 'cholot-title':
                    widget['settings']['title'] = section_data.get('title', 'Kontakt')
                elif widget.get('widgetType') == 'text-editor':
                    widget['settings']['editor'] = f"<p>{section_data.get('text', '')}</p>"
                elif widget.get('widgetType') == 'cholot-contact':
                    widget['settings']['shortcode'] = f'[contact-form-7 id="{section_data.get("form_id", "1")}" title="Contact form"]'
        
        template['id'] = self.generate_id()
        return template
    
    def build_about_section(self, section_data: dict) -> dict:
        """Build about section"""
        # Use template structure or create custom
        template = {
            "id": self.generate_id(),
            "settings": {
                "gap": "extended",
                "structure": "20",
                "padding": {"unit": "px", "top": "60", "right": "0", "bottom": "60", "left": "0", "isLinked": False},
                "content_position": "bottom"
            },
            "elements": [],
            "isInner": False,
            "elType": "section"
        }
        
        # Text column
        text_column = {
            "id": self.generate_id(),
            "settings": {"_column_size": 50, "_inline_size": None},
            "elements": [
                {
                    "id": self.generate_id(),
                    "settings": {
                        "editor": f"<p>{section_data.get('subtitle', 'Über uns')}</p>",
                        "text_color": "#b68c2f",
                        "typography_typography": "custom",
                        "typography_text_transform": "uppercase",
                        "typography_font_size": {"unit": "px", "size": 15, "sizes": []},
                        "typography_font_weight": "700",
                        "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "-30", "left": "0", "isLinked": False}
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "text-editor",
                    "elType": "widget"
                },
                {
                    "id": self.generate_id(),
                    "settings": {
                        "title": section_data.get('title', ''),
                        "desc_typography_typography": "custom",
                        "desc_typography_font_size": {"unit": "px", "size": 35, "sizes": []},
                        "desc_typography_font_weight": "700",
                        "desc_typography_font_family": "Playfair Display",
                        "desc_typography_line_height": {"unit": "em", "size": 1.1, "sizes": []},
                        "align": "left",
                        "title_color": "#000000",
                        "span_title_typo_typography": "custom",
                        "span_title_typo_font_weight": "400",
                        "span_title_typo_font_style": "italic",
                        "span_title_color": "#000000"
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "cholot-title",
                    "elType": "widget"
                },
                {
                    "id": self.generate_id(),
                    "settings": {
                        "weight": {"unit": "px", "size": 2, "sizes": []},
                        "color": "#b68c2f",
                        "width": {"unit": "px", "size": 50, "sizes": []},
                        "align": "left"
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "divider",
                    "elType": "widget"
                },
                {
                    "id": self.generate_id(),
                    "settings": {
                        "editor": f"<p>{section_data.get('content', '')}</p>",
                        "typography_font_weight": "normal",
                        "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "-30", "left": "0", "isLinked": False}
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "text-editor",
                    "elType": "widget"
                }
            ],
            "isInner": False,
            "elType": "column"
        }
        
        # Image column
        if section_data.get('image'):
            image_column = {
                "id": self.generate_id(),
                "settings": {"_column_size": 50, "_inline_size": None},
                "elements": [{
                    "id": self.generate_id(),
                    "settings": {
                        "image": {
                            "url": section_data.get('image', ''),
                            "id": int(self.generate_id()[:4], 16) % 10000
                        },
                        "image_size": "full",
                        "_animation": "fadeInUp",
                        "animation_duration": "fast"
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "image",
                    "elType": "widget"
                }],
                "isInner": False,
                "elType": "column"
            }
            template['elements'] = [text_column, image_column]
        else:
            text_column['settings']['_column_size'] = 100
            template['elements'] = [text_column]
        
        # Add features if provided
        if section_data.get('features'):
            features_section = self.build_features_grid(section_data['features'])
            text_column['elements'].append(features_section)
        
        return template
    
    def build_features_grid(self, features: List[dict]) -> dict:
        """Build features grid as inner section"""
        section = {
            "id": self.generate_id(),
            "settings": {
                "gap": "no",
                "structure": "20",
                "margin": {"unit": "%", "top": "", "right": 0, "bottom": "", "left": 0, "isLinked": False}
            },
            "elements": [],
            "isInner": True,
            "elType": "section"
        }
        
        # Create 2 columns for features
        left_features = features[:2]
        right_features = features[2:4]
        
        for feature_group in [left_features, right_features]:
            column = {
                "id": self.generate_id(),
                "settings": {"_column_size": 50, "_inline_size": None},
                "elements": [],
                "isInner": True,
                "elType": "column"
            }
            
            for feature in feature_group:
                widget = {
                    "id": self.generate_id(),
                    "settings": {
                        "icon": "fa fa-child",
                        "icon_style": "left",
                        "title": feature.get('title', ''),
                        "subtitle": "",
                        "text": f"<p>{feature.get('text', '')}</p>",
                        "selected_icon": {"value": feature.get('icon', 'fas fa-check'), "library": "fa-solid"},
                        "icon_size": {"unit": "px", "size": 14, "sizes": []},
                        "icon_bg_size": {"unit": "px", "size": 32, "sizes": []},
                        "icon_color": "#ffffff",
                        "iconbg_color": "#b68c2f",
                        "_padding": {"unit": "px", "top": "30", "right": "30", "bottom": "30", "left": "30", "isLinked": True},
                        "_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                        "_border_color": "#b68c2f",
                        "_border_border": "dashed"
                    },
                    "elements": [],
                    "isInner": False,
                    "widgetType": "cholot-texticon",
                    "elType": "widget"
                }
                column['elements'].append(widget)
            
            section['elements'].append(column)
        
        return section
    
    def convert_yaml_to_elementor(self, yaml_path: str) -> dict:
        """Main conversion function"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        elementor_sections = []
        
        # Process each page
        for page_data in data.get('pages', []):
            sections = page_data.get('sections', [])
            
            for section in sections:
                section_type = section.get('type')
                
                if section_type == 'hero_slider':
                    elementor_sections.append(self.build_hero_slider(section))
                elif section_type == 'service_cards':
                    elementor_sections.append(self.build_service_cards(section))
                elif section_type == 'about':
                    elementor_sections.append(self.build_about_section(section))
                elif section_type == 'team':
                    elementor_sections.append(self.build_team_section(section))
                elif section_type == 'testimonials':
                    elementor_sections.append(self.build_testimonials_section(section))
                elif section_type == 'contact':
                    elementor_sections.append(self.build_contact_section(section))
                elif section_type == 'services_grid':
                    # Additional service grid section
                    elementor_sections.append(self.build_services_grid(section))
        
        # Build complete Elementor JSON
        elementor_json = {
            "content": elementor_sections,
            "page_settings": [],
            "version": "0.4",
            "title": page_data.get('title', 'Generated Page'),
            "type": "page"
        }
        
        return elementor_json
    
    def build_services_grid(self, section_data: dict) -> dict:
        """Build services grid section (simplified services)"""
        template = {
            "id": self.generate_id(),
            "settings": {
                "gap": "extended",
                "structure": "30",
                "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "60", "left": "0", "isLinked": False},
                "background_background": "classic",
                "background_color": "#ffffff"
            },
            "elements": [],
            "isInner": False,
            "elType": "section"
        }
        
        services = section_data.get('services', [])
        
        for service in services[:3]:
            column = {
                "id": self.generate_id(),
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None,
                    "animation": "fadeInUp",
                    "animation_duration": "fast"
                },
                "elements": [],
                "isInner": False,
                "elType": "column"
            }
            
            # Icon widget
            icon_widget = {
                "id": self.generate_id(),
                "settings": {
                    "selected_icon": {"value": service.get('icon', 'fas fa-check'), "library": "fa-solid"},
                    "view": "stacked",
                    "primary_color": "#ffffff",
                    "secondary_color": "#b68c2f",
                    "size": {"unit": "px", "size": 20, "sizes": []},
                    "icon_padding": {"unit": "px", "size": 10, "sizes": []},
                    "shape": "square",
                    "align": "right",
                    "_margin": {"unit": "px", "top": "21", "right": "20", "bottom": "-49", "left": "0", "isLinked": False},
                    "_z_index": 5
                },
                "elements": [],
                "isInner": False,
                "widgetType": "icon",
                "elType": "widget"
            }
            
            # Text line widget
            text_widget = {
                "id": self.generate_id(),
                "settings": {
                    "title": service.get('title', ''),
                    "subtitle": "",
                    "line": {"unit": "px", "size": 50, "sizes": []},
                    "line_height": {"unit": "px", "size": 2, "sizes": []},
                    "title_typography_font_size": {"unit": "px", "size": 28, "sizes": []},
                    "subtitle_color": "#b68c2f",
                    "wline_padding": {"unit": "px", "top": "30", "right": "30", "bottom": "30", "left": "30", "isLinked": True},
                    "_margin": {"unit": "px", "top": "-50", "right": "20", "bottom": "0", "left": "20", "isLinked": False},
                    "_background_background": "classic",
                    "_background_color": "#fafafa",
                    "_box_shadow_box_shadow_type": "yes",
                    "_box_shadow_box_shadow": {"horizontal": 0, "vertical": 0, "blur": 7, "spread": 0, "color": "rgba(204,204,204,0.43)"}
                },
                "elements": [],
                "isInner": False,
                "widgetType": "cholot-text-line",
                "elType": "widget"
            }
            
            column['elements'] = [icon_widget, text_widget]
            template['elements'].append(column)
        
        return template
    
    def save_output(self, elementor_json: dict, output_path: str):
        """Save Elementor JSON to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(elementor_json, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved Elementor JSON: {output_path}")
    
    def create_wordpress_format(self, elementor_json: dict, site_data: dict) -> dict:
        """Create WordPress import format"""
        return {
            "site": {
                "title": site_data.get('title', 'Website'),
                "url": site_data.get('base_url', 'http://localhost'),
                "description": site_data.get('description', '')
            },
            "posts": [{
                "title": elementor_json.get('title', 'Page'),
                "slug": "generated-page",
                "type": "page",
                "status": "publish",
                "template": "elementor_canvas",
                "meta": {
                    "_elementor_edit_mode": "builder",
                    "_elementor_template_type": "wp-page",
                    "_elementor_version": "3.14.1",
                    "_elementor_data": json.dumps(elementor_json['content'], ensure_ascii=False)
                }
            }]
        }

def main():
    """Main execution"""
    print("🚀 YAML to Elementor Converter")
    print("=" * 50)
    
    # Initialize converter
    converter = YamlToElementorConverter()
    
    # Convert YAML to Elementor
    yaml_file = 'riman_input.yaml'
    elementor_json = converter.convert_yaml_to_elementor(yaml_file)
    
    # Save Elementor JSON
    converter.save_output(elementor_json, 'riman_generated.json')
    
    # Load YAML for site data
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    
    # Create WordPress format
    wordpress_data = converter.create_wordpress_format(elementor_json, yaml_data.get('site', {}))
    
    # Save WordPress format
    with open('riman_wordpress_import.json', 'w', encoding='utf-8') as f:
        json.dump(wordpress_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved WordPress format: riman_wordpress_import.json")
    print(f"📊 Sections generated: {len(elementor_json['content'])}")
    print(f"📦 Data size: {len(json.dumps(elementor_json['content']))} chars")
    
    return elementor_json

if __name__ == '__main__':
    main()