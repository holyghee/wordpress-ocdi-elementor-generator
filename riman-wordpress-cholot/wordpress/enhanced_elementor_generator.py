#!/usr/bin/env python3
"""
Enhanced Elementor JSON Generator - Complete Implementation
==========================================================

Production-ready Elementor JSON generator with all 13 Cholot widgets,
advanced placeholder system, and comprehensive validation.

Author: Code Implementation Lead  
Version: 1.1.0
"""

import json
import yaml
import re
import uuid
import html
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import random
import string

# Import base classes
from generate_wordpress_xml import CholotThemeConfig, ElementorIDGenerator


class AdvancedPlaceholderSystem:
    """Advanced placeholder resolution with context inheritance."""
    
    def __init__(self):
        self.global_context = {}
        self.local_context = {}
        self.placeholders = {}
        
    def register_defaults(self):
        """Register default placeholders."""
        defaults = {
            'site_title': 'My WordPress Site',
            'site_name': 'WordPress Site',
            'site_description': 'Just another WordPress site',
            'primary_color': '#b68c2f',
            'secondary_color': '#232323',
            'base_url': 'http://localhost:8080',
            'current_year': str(datetime.now().year),
            'phone': '+1-555-000-0000',
            'email': 'info@example.com',
            'demo_image_1': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=600',
            'demo_image_2': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300',
            'demo_logo': 'https://via.placeholder.com/200x80/b68c2f/ffffff?text=LOGO'
        }
        
        for key, value in defaults.items():
            self.register_placeholder(key, value)
    
    def register_placeholder(self, key: str, value: Any):
        """Register a placeholder."""
        self.placeholders[key] = value
    
    def set_global_context(self, context: Dict[str, Any]):
        """Set global context from configuration."""
        self.global_context.update(context)
    
    def set_local_context(self, context: Dict[str, Any]):
        """Set local context (temporary)."""
        self.local_context.update(context)
    
    def clear_local_context(self):
        """Clear local context."""
        self.local_context = {}
    
    def resolve_content(self, content: Any) -> Any:
        """Recursively resolve placeholders in any content."""
        if isinstance(content, str):
            return self._resolve_string(content)
        elif isinstance(content, dict):
            return {k: self.resolve_content(v) for k, v in content.items()}
        elif isinstance(content, list):
            return [self.resolve_content(item) for item in content]
        else:
            return content
    
    def _resolve_string(self, text: str) -> str:
        """Resolve placeholders in a string."""
        # Pattern: {{key}} or {{key:default}}
        pattern = r'\{\{([^:}]+)(?::([^}]*))?\}\}'
        
        def replace_match(match):
            key = match.group(1).strip()
            default = match.group(2) or ""
            
            # Priority: local context > global context > registered placeholders > default
            if key in self.local_context:
                return str(self.local_context[key])
            elif key in self.global_context:
                return str(self.global_context[key])
            elif key in self.placeholders:
                return str(self.placeholders[key])
            else:
                return default
        
        return re.sub(pattern, replace_match, text)


class PredictableIDGenerator:
    """Generates predictable IDs for testing and consistent output."""
    
    def __init__(self, use_predictable=True):
        self.use_predictable = use_predictable
        self.counters = {}
        self.used_ids = set()
    
    def generate_id(self, prefix: str = None) -> str:
        """Generate ID with optional prefix."""
        if self.use_predictable and prefix:
            if prefix not in self.counters:
                self.counters[prefix] = 0
            self.counters[prefix] += 1
            new_id = f"{prefix}{self.counters[prefix]:04d}"
        else:
            # Generate random 7-character ID like Elementor
            new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        
        # Ensure uniqueness
        while new_id in self.used_ids:
            if self.use_predictable and prefix:
                self.counters[prefix] += 1
                new_id = f"{prefix}{self.counters[prefix]:04d}"
            else:
                new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        
        self.used_ids.add(new_id)
        return new_id


class ComprehensiveCholotFactory:
    """Complete factory for all 13 Cholot widgets with enhancements."""
    
    def __init__(self):
        self.theme_config = CholotThemeConfig()
        self.id_generator = PredictableIDGenerator()
        self.placeholder_system = AdvancedPlaceholderSystem()
        self.placeholder_system.register_defaults()
    
    def set_context(self, context: Dict[str, Any]):
        """Set context for placeholder resolution."""
        self.placeholder_system.set_global_context(context)
    
    # Enhanced Widget Generators
    
    def create_texticon_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-texticon widget."""
        widget_id = self.id_generator.generate_id('txticon')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "title": config.get('title', 'Default Title'),
            "selected_icon": {
                "value": config.get('icon', 'fas fa-crown'),
                "library": self._get_icon_library(config.get('icon', 'fas fa-crown'))
            },
            "__fa4_migrated": {"selected_icon": True},
            
            # Typography
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": config.get('title_font_size', 24), "sizes": []},
            "title_typography_line_height": {"unit": "em", "size": 1.2, "sizes": []},
            "title_typography_font_weight": "700",
            "title_color": config.get('title_color', self.theme_config.WHITE),
            
            # Subtitle
            "subtitle_typography_typography": "custom",
            "subtitle_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
            "subtitle_typography_font_weight": "700", 
            "subtitle_typography_text_transform": "uppercase",
            "subtitle_typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
            "subtitle_color": config.get('subtitle_color', self.theme_config.PRIMARY_COLOR),
            
            # Icon
            "icon_size": {"unit": "px", "size": config.get('icon_size', 20), "sizes": []},
            "icon_bg_size": {"unit": "px", "size": config.get('icon_bg_size', 60), "sizes": []},
            "icon_color": config.get('icon_color', self.theme_config.WHITE),
            "iconbg_color": config.get('icon_bg_color', self.theme_config.PRIMARY_COLOR),
            
            # Spacing
            "title_margin": self._create_spacing_object(config.get('title_margin', {})),
            "sb_margin": self._create_spacing_object(config.get('subtitle_margin', {})),
            "text_margin": self._create_spacing_object(config.get('text_margin', {})),
            "icon_margin": self._create_spacing_object(config.get('icon_margin', {'top': '-27'})),
            "_padding": self._create_spacing_object(config.get('padding', {'all': '30'})),
            
            # Styling
            "_border_border": config.get('border_style', 'dashed'),
            "_border_color": config.get('border_color', self.theme_config.PRIMARY_COLOR),
            "_border_width": self._create_spacing_object(config.get('border_width', {
                'top': '0', 'right': '1', 'bottom': '1', 'left': '1'
            }))
        }
        
        # Optional content
        if 'subtitle' in config:
            settings['subtitle'] = str(config['subtitle'])
            
        if 'text' in config:
            settings['text'] = self._format_text_content(config['text'])
            settings.update({
                'text_typography_typography': "custom",
                'text_typography_font_size': {"unit": "px", "size": 15, "sizes": []},
                'text_typography_font_style': config.get('text_style', 'normal'),
                'text_color': config.get('text_color', self.theme_config.PRIMARY_COLOR)
            })
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-texticon"
        }
    
    def create_title_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-title widget."""
        widget_id = self.id_generator.generate_id('title')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "title": config.get('title', 'Default Title'),
            "header_size": config.get('header_size', 'h2'),
            "align": config.get('align', 'left'),
            
            # Typography
            "desc_typography_typography": "custom",
            "desc_typography_font_family": config.get('font_family', 'Playfair Display'),
            "desc_typography_font_size": {"unit": "px", "size": config.get('font_size', 35), "sizes": []},
            "desc_typography_font_weight": config.get('font_weight', '700'),
            "desc_typography_line_height": {"unit": "em", "size": 1.1, "sizes": []},
            
            # Colors
            "title_color": config.get('title_color', self.theme_config.BLACK),
            "span_title_color": config.get('span_color', self.theme_config.PRIMARY_COLOR),
            
            # Span styling
            "span_title_typo_typography": "custom",
            "span_title_typo_font_weight": config.get('span_font_weight', '400'),
            "span_title_typo_font_style": config.get('span_font_style', 'italic'),
            
            # Spacing
            "title_margin": self._create_spacing_object(config.get('title_margin', {})),
            "_margin": self._create_spacing_object(config.get('margin', {}))
        }
        
        # Responsive settings
        if config.get('responsive'):
            resp = config['responsive']
            if 'mobile' in resp:
                settings['desc_typography_font_size_mobile'] = {
                    "unit": "px", "size": resp['mobile'].get('font_size', 25), "sizes": []
                }
            if 'tablet' in resp:
                settings['align_tablet'] = resp['tablet'].get('align', settings['align'])
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget", 
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-title"
        }
    
    def create_team_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-team widget."""
        widget_id = self.id_generator.generate_id('team')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "title": config.get('name', 'Team Member'),
            "text": config.get('position', 'Position'),
            "image": self._process_image_config(config.get('image', {})),
            "team_height": config.get('height', '420px'),
            "content_align": config.get('align', 'left'),
            "hover_animation": config.get('animation', 'shrink'),
            
            # Colors
            "title_cl": config.get('title_color', self.theme_config.BLACK),
            "txt_cl": config.get('position_color', self.theme_config.PRIMARY_COLOR),
            "bg_content": config.get('content_bg', "#1f1f1f"),
            "mask_color": config.get('mask_color', self.theme_config.BLACK),
            "mask_color_opacity": {"unit": "px", "size": 0.8, "sizes": []},
            
            # Typography
            "cport_typography_typography": "custom",
            "cport_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "cport_typography_line_height": {"unit": "em", "size": 1.2, "sizes": []},
            "cport_typography_text_transform": "capitalize",
            "ctext_typography_typography": "custom",
            "ctext_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
            "ctext_typography_font_weight": "normal",
            "ctext_typography_line_height": {"unit": "em", "size": 1.4, "sizes": []},
            
            # Styling
            "port_border_border": "solid",
            "port_border_color": self.theme_config.PRIMARY_COLOR,
            "port_border_width": self._create_spacing_object({'all': '1'}),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0, "vertical": 8, "blur": 14,
                "spread": 4, "color": "rgba(175,175,175,0.27)"
            },
            
            # Background
            "background_background": "classic",
            "background_color": config.get('background_color', "#f4f4f4"),
            "background_position": "center left",
            "background_repeat": "no-repeat",
            "background_size": "cover",
            "background_bg_width": {"unit": "px", "size": 60, "sizes": []},
            
            # Spacing
            "port_padding": self._create_spacing_object({'all': '30'}),
            "titlep_margin": self._create_spacing_object({'bottom': '5'}),
            "titlep_padding": self._create_spacing_object({}),
            "tx_margin": self._create_spacing_object({}),
            "tx_padding": self._create_spacing_object({}),
            "port_content": self._create_spacing_object({
                'top': '-80', 'right': '15', 'bottom': '0', 'left': '15'
            }),
            "_margin": self._create_spacing_object({})
        }
        
        # Social media icons
        if 'social_links' in config:
            social_list = []
            for social in config['social_links']:
                social_item = {
                    "_id": self.id_generator.generate_id('social'),
                    "social_icon": {
                        "value": social.get('icon', 'fab fa-facebook-f'),
                        "library": "fa-brands"
                    },
                    "link": {
                        "url": social.get('url', '#'),
                        "is_external": "true",
                        "nofollow": ""
                    },
                    "item_icon_color": "custom",
                    "item_icon_primary_color": "rgba(0,0,0,0)",
                    "item_icon_secondary_color": social.get('color', '#000000')
                }
                social_list.append(social_item)
            settings['social_icon_list'] = social_list
        
        # Background icon
        if 'background_icon' in config:
            settings.update({
                'selected_icon': {
                    "value": config['background_icon'],
                    "library": "fa-solid"
                },
                'bg_icon_color': self.theme_config.PRIMARY_COLOR,
                'bg_icon_size': {"unit": "px", "size": 110, "sizes": []},
                'bg_icon_rotate': {"unit": "px", "size": 10, "sizes": []}
            })
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-team"
        }
    
    def create_gallery_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-gallery widget."""
        widget_id = self.id_generator.generate_id('gallery')
        config = self.placeholder_system.resolve_content(config)
        
        # Process images
        gallery_images = config.get('images', [])
        gallery_data = []
        
        for i, img in enumerate(gallery_images):
            if isinstance(img, str):
                gallery_data.append({"id": 100 + i, "url": img})
            elif isinstance(img, dict):
                img_data = {
                    "id": img.get('id', 100 + i),
                    "url": img.get('url', f'https://via.placeholder.com/400x300?text=Image+{i+1}')
                }
                if 'alt' in img:
                    img_data['alt'] = img['alt']
                gallery_data.append(img_data)
        
        settings = {
            "gallery": gallery_data,
            "port_column": config.get('columns', 'col-md-4'),
            "gallery_height": {"unit": "px", "size": config.get('height', 250), "sizes": []},
            "gallery_margin": {"unit": "px", "size": config.get('margin', 10), "sizes": []},
            "title_show": config.get('show_title', ""),
            "caption_show": config.get('show_caption', ""),
            "mask_color": config.get('overlay_color', self.theme_config.BLACK),
            "mask_color_opacity": {"unit": "px", "size": config.get('overlay_opacity', 0.6), "sizes": []},
            "_margin": self._create_spacing_object(config.get('margin_settings', {}))
        }
        
        # Responsive
        if 'responsive' in config:
            resp = config['responsive']
            for device in ['tablet', 'mobile']:
                if device in resp:
                    device_settings = resp[device]
                    if 'height' in device_settings:
                        settings[f'gallery_height_{device}'] = {
                            "unit": "px", "size": device_settings['height'], "sizes": []
                        }
                    if 'margin' in device_settings:
                        settings[f'gallery_margin_{device}'] = {
                            "unit": "px", "size": device_settings['margin'], "sizes": []
                        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-gallery"
        }
    
    def create_testimonial_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-testimonial-two widget."""
        widget_id = self.id_generator.generate_id('testimonial')
        config = self.placeholder_system.resolve_content(config)
        
        # Process testimonials list
        testimonials_list = []
        for i, testimonial in enumerate(config.get('testimonials', [])):
            testi_item = {
                "_id": self.id_generator.generate_id('testi'),
                "title": testimonial.get('title', f'Person {i+1}'),
                "position": testimonial.get('position', 'Customer'),
                "text": testimonial.get('text', 'Great service and experience.'),
                "image": self._process_image_config(testimonial.get('image', {}))
            }
            testimonials_list.append(testi_item)
        
        settings = {
            "show_desktop": str(config.get('columns', 3)),
            "testi_list": testimonials_list,
            
            # Typography
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": 16, "sizes": []},
            "title_typography_line_height": {"unit": "em", "size": 1.6, "sizes": []},
            "name_typography_typography": "custom",
            "name_typography_font_family": "Source Sans Pro",
            "name_typography_font_size": {"unit": "px", "size": 17, "sizes": []},
            "name_typography_font_weight": "700",
            "name_typography_text_transform": "uppercase",
            "post_typography_typography": "custom",
            "post_typography_font_size": {"unit": "px", "size": 14, "sizes": []},
            "post_typography_font_weight": "400",
            "post_typography_font_style": "normal",
            "post_typography_text_transform": "none",
            
            # Colors
            "title_color": config.get('text_color', self.theme_config.WHITE),
            "name_color": config.get('name_color', self.theme_config.WHITE),
            "post_color": config.get('position_color', self.theme_config.PRIMARY_COLOR),
            "text_bgcolor": config.get('text_bg_color', "rgba(255,255,255,0.08)"),
            "testi_box_bg": config.get('box_bg_color', "rgba(255,255,255,0)"),
            "testi_box_border_color": self.theme_config.PRIMARY_COLOR,
            "image_border_color": self.theme_config.WHITE,
            
            # Image settings
            "img_size": {"unit": "px", "size": config.get('image_size', 50), "sizes": []},
            "image_border_border": "solid",
            "image_border_width": self._create_spacing_object({'all': '3'}),
            "img_radius": self._create_spacing_object({'all': '200'}),
            
            # Layout
            "content-align": config.get('align', 'center'),
            "testi_box_border_width": self._create_spacing_object({'all': '1'}),
            "textbox_padding": self._create_spacing_object({'all': '30'}),
            "text_radius": self._create_spacing_object({'all': '10'}),
            "textbox_margin": self._create_spacing_object({'top': '-20', 'bottom': '30'}),
            "testi_box_margin": self._create_spacing_object({'all': '15'}),
            "testi_box_padding": self._create_spacing_object({}),
            "_margin": self._create_spacing_object({})
        }
        
        # Responsive
        if 'responsive' in config:
            resp = config['responsive']
            if 'mobile' in resp:
                mobile_settings = resp['mobile']
                for key, default in [
                    ('title_size', 15), ('name_size', 16), 
                    ('post_size', 12), ('image_size', 40)
                ]:
                    if key in mobile_settings:
                        settings[f'{key.split("_")[0]}_typography_font_size_mobile'] = {
                            "unit": "px", "size": mobile_settings[key], "sizes": []
                        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-testimonial-two"
        }
    
    def create_text_line_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-text-line widget."""
        widget_id = self.id_generator.generate_id('textline')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "title": config.get('title', 'Default Title'),
            "subtitle": config.get('subtitle', ''),
            "line": str(config.get('line_width', 50)),
            "line_height": str(config.get('line_height', 2)),
            
            # Typography
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": config.get('title_size', 28), "sizes": []},
            "subtitle_typography_typography": "custom",
            "subtitle_typography_font_size": {"unit": "px", "size": config.get('subtitle_size', 14), "sizes": []},
            "subtitle_typography_font_weight": "bold",
            "subtitle_typography_text_transform": "uppercase",
            "subtitle_typography_letter_spacing": {"unit": "px", "size": 0, "sizes": []},
            
            # Colors
            "subtitle_color": self.theme_config.PRIMARY_COLOR,
            "line_color_hover": self.theme_config.PRIMARY_COLOR,
            
            # Background
            "_background_background": "classic",
            "_background_color": config.get('background_color', self.theme_config.LIGHT_BG),
            
            # Spacing
            "title_margin": self._create_spacing_object({'bottom': '30'}),
            "sb_margin": self._create_spacing_object({'bottom': '10'}),
            "sb_padding": self._create_spacing_object({}),
            "text_margin": self._create_spacing_object({'top': '30', 'bottom': '-30'}),
            "wline_margin": self._create_spacing_object({'all': '15'}),
            "wline_padding": self._create_spacing_object({'all': '30'}),
            "_margin": self._create_spacing_object({})
        }
        
        # Background image
        if 'background_image' in config:
            bg_img = config['background_image']
            if isinstance(bg_img, str):
                settings['_background_image'] = {"url": bg_img, "id": random.randint(1000, 9999)}
            else:
                settings['_background_image'] = self._process_image_config(bg_img)
            
            settings.update({
                '_background_position': config.get('background_position', 'initial'),
                '_background_repeat': config.get('background_repeat', 'no-repeat'),
                '_background_size': config.get('background_size', 'initial'),
                '_background_xpos': {"unit": "%", "size": 100, "sizes": []},
                '_background_ypos': {"unit": "px", "size": 112, "sizes": []},
                '_background_bg_width': {"unit": "px", "size": 168, "sizes": []}
            })
        
        # Box shadow
        if config.get('box_shadow', True):
            settings.update({
                '_box_shadow_box_shadow_type': "yes",
                '_box_shadow_box_shadow': {
                    "horizontal": 0, "vertical": 0, "blur": 7,
                    "spread": 0, "color": "rgba(204,204,204,0.43)"
                }
            })
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-text-line"
        }
    
    def create_contact_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-contact widget."""
        widget_id = self.id_generator.generate_id('contact')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "shortcode": config.get('shortcode', '[contact-form-7 id="1" title="Contact form"]'),
            
            # Button styling
            "btn_typography_typography": "custom",
            "btn_typography_font_size": {"unit": "px", "size": 14, "sizes": []},
            "btn_typography_font_weight": "700",
            "btn_typography_text_transform": "uppercase",
            "btn_typography_letter_spacing": {"unit": "px", "size": 0, "sizes": []},
            
            # Button colors
            "btn_color": self.theme_config.WHITE,
            "btn_color_hover": self.theme_config.WHITE,
            "btn_bg": config.get('button_bg', "rgba(0,0,0,0)"),
            "btn_bg_hover": self.theme_config.PRIMARY_COLOR,
            "btn_border_color": self.theme_config.PRIMARY_COLOR,
            
            # Form styling
            "form_placeholder": config.get('placeholder_color', self.theme_config.WHITE),
            "form_bg": config.get('form_bg', "rgba(0,0,0,0)"),
            "form_border_color": config.get('border_color', self.theme_config.WHITE),
            "form_border_color_active": self.theme_config.PRIMARY_COLOR,
            "form_text": config.get('text_color', self.theme_config.WHITE),
            
            # Button settings
            "btn_width": config.get('button_width', '100%'),
            "btn_margin": self._create_spacing_object(config.get('button_margin', {})),
            "btn_padding": self._create_spacing_object(config.get('button_padding', {})),
            "btn_border": self._create_spacing_object({'all': '1'}),
            "btn_border_radius": self._create_spacing_object(config.get('button_radius', {}))
        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-contact"
        }
    
    def create_button_text_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced cholot-button-text widget."""
        widget_id = self.id_generator.generate_id('btn')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "btn_text": config.get('text', 'Click Here'),
            "link": {
                "url": config.get('url', '#'),
                "is_external": config.get('external', "")
            },
            "align": config.get('align', 'left'),
            
            # Typography
            "btn_typography_typography": "custom",
            "btn_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "btn_typography_font_weight": "700",
            "btn_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
            "btn_typography_text_transform": "uppercase",
            
            # Colors
            "btn_color": self.theme_config.WHITE,
            "btn_color_hover": self.theme_config.WHITE,
            "btn_bg": self.theme_config.PRIMARY_COLOR,
            "btn_bg_hover": self.theme_config.BLACK,
            
            # Spacing
            "btn_padding": self._create_spacing_object(config.get('padding', {})),
            "_margin": self._create_spacing_object(config.get('margin', {}))
        }
        
        # Subtitle
        if 'subtitle' in config:
            settings.update({
                'btn_sub': config['subtitle'],
                'btn_sub_typography_typography': "custom",
                'btn_sub_typography_font_size': {"unit": "px", "size": 13, "sizes": []},
                'btn_sub_typography_font_weight': "normal",
                'btn_sub_typography_text_transform': "uppercase",
                'btn_subcolor': "rgba(255,255,255,0.65)",
                'btn_subcolor_hover': "rgba(255,255,255,0.45)"
            })
        
        # Icon
        if 'icon' in config:
            settings.update({
                'selected_icon': {
                    "value": config['icon'],
                    "library": self._get_icon_library(config['icon'])
                },
                'icon_align': config.get('icon_align', 'right'),
                'icn_typography_typography': "custom",
                'icn_typography_font_size': {"unit": "px", "size": 30, "sizes": []}
            })
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-button-text"
        }
    
    def create_post_widget(self, config: Dict[str, Any], widget_type: str = "three") -> Dict[str, Any]:
        """Create enhanced cholot-post-three or cholot-post-four widget."""
        widget_id = self.id_generator.generate_id('post')
        widget_name = f"cholot-post-{widget_type}"
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "blog_post": str(config.get('post_count', 2)),
            "blog_column": config.get('column', 'one' if widget_type == 'three' else 'two'),
            "sort_cat": "yes",
            "show_excerpt": config.get('show_excerpt', ""),
            "excerpt_after": config.get('excerpt_after', "..."),
            "button": config.get('button_text', "Read More"),
            
            # Typography
            "title_typo_typography": "custom",
            "title_typo_font_size": {"unit": "px", "size": config.get('title_font_size', 20), "sizes": []},
            "title_typo_font_weight": config.get('title_font_weight', '600'),
            "meta_typo_typography": "custom",
            "meta_typo_font_size": {"unit": "px", "size": 14, "sizes": []},
            "meta_typo_font_style": "normal",
            
            # Colors
            "meta_color": self.theme_config.PRIMARY_COLOR,
            "meta_link": self.theme_config.PRIMARY_COLOR,
            "meta_link_hover": "#d8d8d8",
            "meta_icon": self.theme_config.PRIMARY_COLOR,
            "title_color_hover": "rgba(0,0,0,0.61)",
            
            # Spacing
            "title_margin": self._create_spacing_object({}),
            "_margin": self._create_spacing_object({})
        }
        
        # Categories filter
        if 'categories' in config:
            settings['blog_cat'] = config['categories']
        
        # Post-four specific settings
        if widget_type == 'four':
            settings.update({
                "content_bg": config.get('content_bg', '#fafafa'),
                "btn_typography_typography": "custom",
                "btn_typography_font_size": {"unit": "px", "size": 14, "sizes": []},
                "btn_typography_font_weight": "700",
                "btn_typography_text_transform": "uppercase",
                "btn_color_hover": self.theme_config.WHITE,
                "btn_bg_hover": self.theme_config.PRIMARY_COLOR,
                "btn_border_border": "solid",
                "btn_border_settings_border": "solid",
                "btn_border_settings_width": self._create_spacing_object({'all': '1'}),
                "btn_border_settings_color": self.theme_config.PRIMARY_COLOR,
                "line_width": {"unit": "px", "size": 50, "sizes": []},
                "line_height": {"unit": "px", "size": 1, "sizes": []}
            })
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": widget_name
        }
    
    def create_logo_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-logo widget."""
        widget_id = self.id_generator.generate_id('logo')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "logo_img": self._process_image_config(config),
            "align": config.get('align', 'left'),
            "height": config.get('height', '70px')
        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-logo"
        }
    
    def create_menu_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-menu widget."""
        widget_id = self.id_generator.generate_id('menu')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "cholot_menu": config.get('menu_name', 'default-menu'),
            "align": config.get('align', 'right'),
            "desktop_menu_tablet": config.get('desktop_tablet', 'none'),
            "mobile_menu": config.get('mobile', 'none'),
            "mobile_menu_tablet": config.get('mobile_tablet', 'inline-block'),
            
            # Typography
            "menu_typo_typography": "custom",
            "menu_typo_font_family": "Source Sans Pro",
            "menu_typo_font_weight": "900",
            "menu_typo_text_transform": "uppercase",
            "menu_typo_letter_spacing": {"unit": "px", "size": 0, "sizes": []},
            "menu_typo_font_size": {"unit": "px", "size": 13, "sizes": []},
            
            # Colors
            "menu_color": self.theme_config.WHITE,
            "menu_color_hover": self.theme_config.PRIMARY_COLOR,
            "menu_child_color": self.theme_config.WHITE,
            "menu_child_color_hover": self.theme_config.PRIMARY_COLOR,
            "hamb_color": self.theme_config.WHITE,
            
            # Spacing
            "menu_margin": self._create_spacing_object({}),
            "child_margin": "9px"
        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-menu"
        }
    
    def create_sidebar_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-sidebar widget."""
        widget_id = self.id_generator.generate_id('sidebar')
        config = self.placeholder_system.resolve_content(config)
        
        settings = {
            "width": config.get('width', '33px'),
            "title_typography_font_size": {"unit": "px", "size": config.get('title_size', 20), "sizes": []}
        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-sidebar"
        }
    
    # Helper Methods
    
    def _get_icon_library(self, icon: str) -> str:
        """Determine icon library from icon class."""
        if icon.startswith('fab '):
            return 'fa-brands'
        elif icon.startswith('fas '):
            return 'fa-solid'
        elif icon.startswith('far '):
            return 'fa-regular'
        else:
            return 'fa-solid'
    
    def _process_image_config(self, config: Any) -> Dict[str, Any]:
        """Process image configuration."""
        if isinstance(config, str):
            return {
                "url": config,
                "id": random.randint(100, 999),
                "alt": "",
                "source": "library",
                "size": "full"
            }
        elif isinstance(config, dict):
            return {
                "url": config.get('url', 'https://via.placeholder.com/400x300'),
                "id": config.get('id', random.randint(100, 999)),
                "alt": config.get('alt', ""),
                "source": config.get('source', "library"),
                "size": config.get('size', "full")
            }
        else:
            return {
                "url": 'https://via.placeholder.com/400x300',
                "id": random.randint(100, 999),
                "alt": "",
                "source": "library",
                "size": "full"
            }
    
    def _format_text_content(self, text: str) -> str:
        """Format text content for Elementor."""
        if not text.startswith('<'):
            return f"<p>{text}</p>"
        return text
    
    def _create_spacing_object(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Elementor spacing object."""
        base = self.theme_config.SPACING_OBJECT.copy()
        
        if 'all' in config:
            value = str(config['all'])
            base.update({
                "top": value, "right": value,
                "bottom": value, "left": value,
                "isLinked": True
            })
        else:
            base.update({
                "top": str(config.get('top', base['top'])),
                "right": str(config.get('right', base['right'])),
                "bottom": str(config.get('bottom', base['bottom'])),
                "left": str(config.get('left', base['left'])),
                "isLinked": config.get('linked', base['isLinked'])
            })
        
        if 'unit' in config:
            base['unit'] = config['unit']
            
        return base
    
    def create_column(self, width: int = 100, elements: List[Dict] = None) -> Dict[str, Any]:
        """Create an Elementor column."""
        column_id = self.id_generator.generate_id('column')
        
        return {
            "id": column_id,
            "elType": "column",
            "settings": {
                "_column_size": width,
                "_inline_size": None
            },
            "elements": elements or [],
            "isInner": False
        }
    
    def create_section(self, structure: str = "100", elements: List[Dict] = None,
                      background_settings: Dict = None) -> Dict[str, Any]:
        """Create an Elementor section."""
        section_id = self.id_generator.generate_id('section')
        
        settings = {
            "gap": "extended",
            "structure": structure
        }
        
        if background_settings:
            settings.update(background_settings)
        
        return {
            "id": section_id,
            "elType": "section",
            "settings": settings,
            "elements": elements or [],
            "isInner": False
        }


class CompleteElementorGenerator:
    """Complete Elementor JSON generator with all features."""
    
    def __init__(self):
        self.factory = ComprehensiveCholotFactory()
        
    def generate_from_config(self, config_path: str, output_path: str, options: Dict = None):
        """Generate Elementor JSON from config file."""
        options = options or {}
        
        # Read configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
        
        # Set context
        if 'context' in config:
            self.factory.set_context(config['context'])
        if 'site' in config:
            self.factory.set_context(config['site'])
        
        # Generate sections
        sections = []
        for section_config in config.get('sections', []):
            section = self._create_section_from_config(section_config)
            if section:
                sections.append(section)
        
        # Save output
        indent = None if options.get('minify', False) else 2
        json_output = json.dumps(sections, indent=indent, separators=(',', ':') if options.get('minify') else (',', ': '))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        return json_output
    
    def _create_section_from_config(self, section_config: Dict) -> Optional[Dict]:
        """Create section from configuration."""
        section_id = self.factory.id_generator.generate_id('section')
        
        # Build columns
        columns_config = section_config.get('columns', [])
        if not columns_config and 'widgets' in section_config:
            columns_config = [{'width': 100, 'widgets': section_config['widgets']}]
        
        section_elements = []
        for column_config in columns_config:
            column = self._create_column_from_config(column_config)
            if column:
                section_elements.append(column)
        
        # Section settings
        settings = {
            "gap": section_config.get('gap', 'extended'),
            "structure": section_config.get('structure', self._calculate_structure(columns_config))
        }
        
        # Background
        if 'background' in section_config:
            bg = section_config['background']
            if bg.get('color'):
                settings['background_background'] = 'classic'
                settings['background_color'] = bg['color']
            if bg.get('image'):
                settings['background_image'] = self.factory._process_image_config(bg['image'])
                settings['background_position'] = bg.get('position', 'center center')
                settings['background_size'] = bg.get('size', 'cover')
        
        # Spacing
        if 'padding' in section_config:
            settings['padding'] = self.factory._create_spacing_object(section_config['padding'])
        if 'margin' in section_config:
            settings['margin'] = self.factory._create_spacing_object(section_config['margin'])
        
        return {
            "id": section_id,
            "elType": "section",
            "settings": settings,
            "elements": section_elements,
            "isInner": False
        }
    
    def _create_column_from_config(self, column_config: Dict) -> Optional[Dict]:
        """Create column from configuration."""
        column_id = self.factory.id_generator.generate_id('column')
        
        # Process widgets
        column_elements = []
        for widget_config in column_config.get('widgets', []):
            widget = self._create_widget_from_config(widget_config)
            if widget:
                column_elements.append(widget)
        
        settings = {
            "_column_size": column_config.get('width', 100),
            "_inline_size": column_config.get('inline_size')
        }
        
        # Column styling
        if 'background' in column_config:
            bg = column_config['background']
            if bg.get('color'):
                settings['background_background'] = 'classic'
                settings['background_color'] = bg['color']
        
        return {
            "id": column_id,
            "elType": "column",
            "settings": settings,
            "elements": column_elements,
            "isInner": False
        }
    
    def _create_widget_from_config(self, widget_config: Dict) -> Optional[Dict]:
        """Create widget from configuration."""
        widget_type = widget_config.get('type', '')
        
        # Route to appropriate factory method
        widget_methods = {
            'texticon': self.factory.create_texticon_widget,
            'title': self.factory.create_title_widget,
            'team': self.factory.create_team_widget,
            'gallery': self.factory.create_gallery_widget,
            'testimonial': self.factory.create_testimonial_widget,
            'text-line': self.factory.create_text_line_widget,
            'contact': self.factory.create_contact_widget,
            'button-text': self.factory.create_button_text_widget,
            'logo': self.factory.create_logo_widget,
            'menu': self.factory.create_menu_widget,
            'sidebar': self.factory.create_sidebar_widget
        }
        
        if widget_type in widget_methods:
            return widget_methods[widget_type](widget_config)
        elif widget_type in ['post-three', 'post-four']:
            post_type = widget_type.split('-')[1]
            return self.factory.create_post_widget(widget_config, post_type)
        else:
            print(f"Warning: Unknown widget type '{widget_type}' - skipping")
            return None
    
    def _calculate_structure(self, columns_config: List[Dict]) -> str:
        """Calculate Elementor structure string."""
        if not columns_config:
            return "100"
        
        column_count = len(columns_config)
        if column_count == 1:
            return "100"
        elif column_count == 2:
            return "50"
        elif column_count == 3:
            return "30"
        elif column_count == 4:
            return "25"
        else:
            return "100"


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Elementor JSON Generator')
    parser.add_argument('-i', '--input', required=True, help='Input YAML/JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file')
    parser.add_argument('--minify', action='store_true', help='Minify output')
    
    args = parser.parse_args()
    
    # Generate
    generator = CompleteElementorGenerator()
    try:
        output = generator.generate_from_config(
            args.input, 
            args.output,
            {'minify': args.minify}
        )
        
        print(f"✅ Generated Elementor JSON: {Path(args.output).resolve()}")
        print(f"📄 File size: {len(output):,} characters")
        
        # Validate
        json.loads(output)
        print("✅ JSON validation successful")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())