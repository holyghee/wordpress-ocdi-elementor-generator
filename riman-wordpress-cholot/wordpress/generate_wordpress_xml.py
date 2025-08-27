#!/usr/bin/env python3
"""
Cholot WordPress XML Generator
=============================

A production-ready generator that creates valid WordPress/Elementor XML from simple input formats.
Supports all 13 Cholot widget types with smart defaults and proper XML structure.

Features:
- Multiple input formats: Markdown, YAML, JSON
- Complete Cholot widget factory with all 13 widget types
- Automatic ID generation and linking
- Theme color scheme integration (#b68c2f)
- Responsive settings management
- Proper CDATA handling
- WordPress XML structure compliance

Author: Generator Design Agent
Version: 1.0.0
"""

import json
import yaml
import re
import uuid
import html
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import markdown
import frontmatter


class CholotThemeConfig:
    """Configuration for Cholot theme defaults and color scheme."""
    
    PRIMARY_COLOR = "#b68c2f"  # Cholot's signature golden color
    WHITE = "#ffffff"
    BLACK = "#000000"
    DARK_BG = "#232323"
    LIGHT_BG = "#f4f4f4"
    TEXT_COLOR = "#878787"
    
    FONT_SIZES = {
        'small': '12px',
        'medium': '14px', 
        'large': '18px',
        'xlarge': '24px',
        'xxlarge': '28px'
    }
    
    SPACING_OBJECT = {
        "unit": "px",
        "top": "0",
        "right": "0", 
        "bottom": "0",
        "left": "0",
        "isLinked": False
    }


class ElementorIDGenerator:
    """Generates unique Elementor-style IDs for sections, columns, and widgets."""
    
    @staticmethod
    def generate_id() -> str:
        """Generate a 7-character alphanumeric ID like Elementor uses."""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))


class CholotComponentFactory:
    """Factory class to create all 13 Cholot widget types with proper defaults."""
    
    def __init__(self):
        self.theme_config = CholotThemeConfig()
        self.id_generator = ElementorIDGenerator()
    
    def create_texticon_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-texticon widget."""
        widget_id = self.id_generator.generate_id()
        
        # Required settings
        title = config.get('title', 'Default Title')
        icon = config.get('icon', 'fas fa-crown')
        
        # Build widget settings with defaults
        settings = {
            "title": title,
            "selected_icon": {
                "value": icon,
                "library": "fa-solid"
            },
            "__fa4_migrated": {
                "selected_icon": True
            },
            # Typography defaults
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": 24, "sizes": []},
            "title_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
            "title_color": self.theme_config.WHITE,
            
            # Subtitle settings
            "subtitle_typography_typography": "custom", 
            "subtitle_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
            "subtitle_typography_font_weight": "700",
            "subtitle_typography_text_transform": "uppercase",
            "subtitle_typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
            "subtitle_color": self.theme_config.PRIMARY_COLOR,
            
            # Icon settings
            "icon_size": {"unit": "px", "size": 15, "sizes": []},
            "icon_bg_size": {"unit": "px", "size": 35, "sizes": []},
            
            # Margins and spacing
            "title_margin": self.theme_config.SPACING_OBJECT.copy(),
            "sb_margin": self.theme_config.SPACING_OBJECT.copy(),
            "sb_padding": self.theme_config.SPACING_OBJECT.copy(),
            "text_margin": self.theme_config.SPACING_OBJECT.copy(),
            "icon_margin": self.theme_config.SPACING_OBJECT.copy(),
            "_margin_mobile": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add optional settings from config
        if 'subtitle' in config:
            settings['subtitle'] = config['subtitle']
            
        if 'text' in config:
            settings['text'] = f"<p>{config['text']}</p>"
            settings['text_typography_typography'] = "custom"
            settings['text_typography_font_size'] = {"unit": "px", "size": 13, "sizes": []}
            settings['text_typography_font_weight'] = "normal"
            settings['text_typography_text_transform'] = "uppercase"
            settings['text_typography_line_height'] = {"unit": "em", "size": 1, "sizes": []}
            settings['text_color'] = self.theme_config.PRIMARY_COLOR
            
        # Override with custom settings
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget", 
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-texticon"
        }
    
    def create_title_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-title widget."""
        widget_id = self.id_generator.generate_id()
        
        title = config.get('title', 'Default Title')
        header_size = config.get('header_size', 'h2')
        
        settings = {
            "title": title,
            "header_size": header_size,
            "desc_typography_typography": "custom",
            "desc_typography_font_size": {"unit": "px", "size": 20, "sizes": []},
            "title_margin": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add alignment if specified
        if 'align' in config:
            settings['align'] = config['align']
            if config.get('responsive', {}).get('tablet'):
                settings['align_tablet'] = config['responsive']['tablet']
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings, 
            "elements": [],
            "widgetType": "cholot-title"
        }
    
    def create_post_widget(self, config: Dict[str, Any], widget_type: str = "three") -> Dict[str, Any]:
        """Create cholot-post-three or cholot-post-four widget."""
        widget_id = self.id_generator.generate_id()
        widget_name = f"cholot-post-{widget_type}"
        
        post_count = config.get('post_count', 2)
        column = config.get('column', 'one' if widget_type == 'three' else 'two')
        
        settings = {
            "blog_post": str(post_count),
            "blog_column": column,
            "sort_cat": "yes",
            "show_excerpt": config.get('show_excerpt', ""),
            "excerpt_after": config.get('excerpt_after', "..."),
            "button": config.get('button_text', "Read More"),
            
            # Typography
            "title_typo_typography": "custom",
            "title_typo_font_size": {"unit": "px", "size": 14, "sizes": []},
            "title_typo_font_weight": "600",
            "meta_typo_typography": "custom", 
            "meta_typo_font_size": {"unit": "px", "size": 14, "sizes": []},
            "meta_typo_font_style": "normal",
            
            # Colors
            "meta_color": self.theme_config.PRIMARY_COLOR,
            "meta_link": self.theme_config.PRIMARY_COLOR,
            "meta_link_hover": "#d8d8d8",
            "meta_icon": self.theme_config.PRIMARY_COLOR,
            "title_color_hover": "rgba(0,0,0,0.61)",
            
            # Margins
            "title_margin": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add category filter if specified
        if 'categories' in config:
            settings['blog_cat'] = config['categories']
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": widget_name
        }
    
    def create_gallery_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-gallery widget."""
        widget_id = self.id_generator.generate_id()
        
        # Gallery images - can be URLs or image objects
        gallery_images = config.get('images', [])
        if isinstance(gallery_images, list) and gallery_images:
            gallery_data = []
            for i, img in enumerate(gallery_images):
                if isinstance(img, str):
                    # Simple URL
                    gallery_data.append({
                        "id": 50 + i,  # Generate sequential IDs
                        "url": img
                    })
                elif isinstance(img, dict):
                    gallery_data.append(img)
        else:
            gallery_data = []
        
        settings = {
            "gallery": gallery_data,
            "port_column": config.get('columns', 'col-md-4'),
            "gallery_height": {"unit": "px", "size": config.get('height', 50), "sizes": []},
            "gallery_margin": {"unit": "px", "size": config.get('margin', 7.5), "sizes": []},
            "title_show": config.get('show_title', ""),
            "caption_show": config.get('show_caption', ""),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Responsive settings
        if 'responsive' in config:
            resp = config['responsive']
            if 'tablet' in resp:
                settings['gallery_height_tablet'] = {"unit": "px", "size": resp['tablet'].get('height', 30), "sizes": []}
                settings['gallery_margin_tablet'] = {"unit": "px", "size": resp['tablet'].get('margin', 3), "sizes": []}
                settings['_margin_tablet'] = self.theme_config.SPACING_OBJECT.copy()
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget", 
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-gallery"
        }
    
    def create_logo_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-logo widget."""
        widget_id = self.id_generator.generate_id()
        
        logo_url = config.get('url', '')
        logo_id = config.get('id', 1)
        
        settings = {
            "logo_img": {
                "url": logo_url,
                "id": logo_id
            },
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
        widget_id = self.id_generator.generate_id()
        
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
            "menu_margin": self.theme_config.SPACING_OBJECT.copy(),
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
    
    def create_button_text_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-button-text widget.""" 
        widget_id = self.id_generator.generate_id()
        
        button_text = config.get('text', 'Click Here')
        link_url = config.get('url', '#')
        
        settings = {
            "btn_text": button_text,
            "link": {
                "url": link_url,
                "is_external": config.get('external', "")
            },
            
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
            "btn_padding": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add subtitle if provided
        if 'subtitle' in config:
            settings['btn_sub'] = config['subtitle']
            settings['btn_sub_typography_typography'] = "custom"
            settings['btn_sub_typography_font_size'] = {"unit": "px", "size": 13, "sizes": []}
            settings['btn_sub_typography_font_weight'] = "normal"
            settings['btn_sub_typography_text_transform'] = "uppercase"
            settings['btn_subcolor'] = "rgba(255,255,255,0.65)"
            settings['btn_subcolor_hover'] = "rgba(255,255,255,0.45)"
        
        # Add icon if provided
        if 'icon' in config:
            settings['selected_icon'] = {
                "value": config['icon'],
                "library": "fa-solid"
            }
            settings['icon_align'] = config.get('icon_align', 'right')
            settings['icn_typography_typography'] = "custom"
            settings['icn_typography_font_size'] = {"unit": "px", "size": 30, "sizes": []}
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-button-text"
        }
    
    def create_team_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-team widget."""
        widget_id = self.id_generator.generate_id()
        
        settings = {
            "title": config.get('name', 'Team Member'),
            "text": config.get('position', 'Team Position'),
            "image": {
                "url": config.get('image_url', ''),
                "id": config.get('image_id', 359)
            },
            "team_height": config.get('height', '420px'),
            "content_align": config.get('align', 'left'),
            "hover_animation": config.get('animation', 'shrink'),
            
            # Colors
            "title_cl": self.theme_config.BLACK,
            "txt_cl": self.theme_config.PRIMARY_COLOR,
            "bg_content": "#1f1f1f",
            "mask_color": self.theme_config.BLACK,
            "mask_color_opacity": {"unit": "px", "size": 0.8, "sizes": []},
            
            # Typography
            "cport_typography_typography": "custom",
            "cport_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "cport_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
            "cport_typography_text_transform": "capitalize",
            "ctext_typography_typography": "custom",
            "ctext_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
            "ctext_typography_font_weight": "normal",
            "ctext_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
            
            # Spacing
            "titlep_margin": self.theme_config.SPACING_OBJECT.copy(),
            "titlep_padding": self.theme_config.SPACING_OBJECT.copy(),
            "tx_margin": self.theme_config.SPACING_OBJECT.copy(),
            "tx_padding": self.theme_config.SPACING_OBJECT.copy(),
            "port_padding": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add social icons if provided
        if 'social_links' in config:
            social_list = []
            for social in config['social_links']:
                social_item = {
                    "_id": self.id_generator.generate_id(),
                    "social_icon": social['icon'],
                    "social_link": social['url']
                }
                social_list.append(social_item)
            settings['social_icon_list'] = social_list
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-team"
        }
    
    def create_testimonial_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-testimonial-two widget."""
        widget_id = self.id_generator.generate_id()
        
        settings = {
            "show_desktop": str(config.get('columns', 3)),
            "testi_list": config.get('testimonials', []),
            
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
            
            # Colors
            "title_color": self.theme_config.WHITE,
            "name_color": self.theme_config.WHITE,
            "post_color": self.theme_config.PRIMARY_COLOR,
            "text_bgcolor": "rgba(255,255,255,0.08)",
            "testi_box_bg": "rgba(255,255,255,0)",
            "testi_box_border_color": self.theme_config.PRIMARY_COLOR,
            "image_border_color": self.theme_config.WHITE,
            
            # Image settings
            "img_size": {"unit": "px", "size": 50, "sizes": []},
            "image_border_border": "solid",
            "image_border_width": self.theme_config.SPACING_OBJECT.copy(),
            "img_radius": self.theme_config.SPACING_OBJECT.copy(),
            
            # Spacing
            "textbox_padding": self.theme_config.SPACING_OBJECT.copy(),
            "textbox_margin": self.theme_config.SPACING_OBJECT.copy(),
            "testi_box_margin": self.theme_config.SPACING_OBJECT.copy(),
            "testi_box_padding": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy(),
            
            # Alignment
            "content-align": config.get('align', 'center')
        }
        
        # Responsive settings
        if 'responsive' in config:
            resp = config['responsive']
            if 'mobile' in resp:
                settings['title_typography_font_size_mobile'] = {"unit": "px", "size": resp['mobile'].get('title_size', 15), "sizes": []}
                settings['name_typography_font_size_mobile'] = {"unit": "px", "size": resp['mobile'].get('name_size', 16), "sizes": []}
                settings['post_typography_font_size_mobile'] = {"unit": "px", "size": resp['mobile'].get('post_size', 12), "sizes": []}
                settings['img_size_mobile'] = {"unit": "px", "size": resp['mobile'].get('image_size', 40), "sizes": []}
                settings['image_border_width_mobile'] = self.theme_config.SPACING_OBJECT.copy()
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-testimonial-two"
        }
    
    def create_text_line_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-text-line widget."""
        widget_id = self.id_generator.generate_id()
        
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
            "title_margin": self.theme_config.SPACING_OBJECT.copy(),
            "sb_margin": self.theme_config.SPACING_OBJECT.copy(),
            "sb_padding": self.theme_config.SPACING_OBJECT.copy(),
            "text_margin": self.theme_config.SPACING_OBJECT.copy(),
            "wline_margin": self.theme_config.SPACING_OBJECT.copy(),
            "wline_padding": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add background image if provided
        if 'background_image' in config:
            settings['_background_image'] = {
                "url": config['background_image'],
                "id": config.get('background_image_id', 1025)
            }
            settings['_background_position'] = config.get('background_position', 'initial')
            settings['_background_repeat'] = config.get('background_repeat', 'no-repeat')
            settings['_background_size'] = config.get('background_size', 'initial')
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings, 
            "elements": [],
            "widgetType": "cholot-text-line"
        }
    
    def create_contact_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-contact widget."""
        widget_id = self.id_generator.generate_id()
        
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
            "btn_bg": "rgba(0,0,0,0)",
            "btn_bg_hover": self.theme_config.PRIMARY_COLOR,
            "btn_border_color": self.theme_config.PRIMARY_COLOR,
            
            # Form styling
            "form_placeholder": self.theme_config.WHITE,
            "form_bg": "rgba(0,0,0,0)",
            "form_border_color": self.theme_config.WHITE,
            "form_border_color_active": self.theme_config.PRIMARY_COLOR,
            "form_text": self.theme_config.WHITE,
            
            # Button settings
            "btn_width": config.get('button_width', '100%'),
            "btn_margin": self.theme_config.SPACING_OBJECT.copy(),
            "btn_padding": self.theme_config.SPACING_OBJECT.copy(),
            "btn_border": self.theme_config.SPACING_OBJECT.copy(),
            "btn_border_radius": self.theme_config.SPACING_OBJECT.copy()
        }
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-contact"
        }
    
    def create_sidebar_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create cholot-sidebar widget."""
        widget_id = self.id_generator.generate_id()
        
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
    
    def create_column(self, size: int = 100, elements: List[Dict] = None) -> Dict[str, Any]:
        """Create an Elementor column."""
        column_id = self.id_generator.generate_id()
        
        return {
            "id": column_id,
            "elType": "column",
            "settings": {
                "_column_size": size,
                "_inline_size": None
            },
            "elements": elements or [],
            "isInner": False
        }
    
    def create_section(self, structure: str = "100", elements: List[Dict] = None, 
                      background_settings: Dict = None) -> Dict[str, Any]:
        """Create an Elementor section."""
        section_id = self.id_generator.generate_id()
        
        settings = {
            "gap": "extended",
            "structure": structure
        }
        
        # Add background settings if provided
        if background_settings:
            settings.update(background_settings)
        
        return {
            "id": section_id,
            "elType": "section",
            "settings": settings,
            "elements": elements or [],
            "isInner": False
        }


class InputFormatParser:
    """Parser for different input formats: Markdown, YAML, JSON."""
    
    @staticmethod
    def parse_markdown(content: str) -> Dict[str, Any]:
        """Parse Markdown with frontmatter."""
        post = frontmatter.loads(content)
        
        # Extract metadata from frontmatter
        metadata = post.metadata
        
        # Convert markdown content to HTML
        html_content = markdown.markdown(post.content)
        
        return {
            'metadata': metadata,
            'content': html_content,
            'format': 'markdown'
        }
    
    @staticmethod
    def parse_yaml(content: str) -> Dict[str, Any]:
        """Parse YAML content."""
        data = yaml.safe_load(content)
        return {
            'data': data,
            'format': 'yaml'
        }
    
    @staticmethod
    def parse_json(content: str) -> Dict[str, Any]:
        """Parse JSON content."""
        data = json.loads(content)
        return {
            'data': data,
            'format': 'json'
        }
    
    @classmethod
    def auto_detect_and_parse(cls, content: str) -> Dict[str, Any]:
        """Auto-detect format and parse accordingly."""
        content = content.strip()
        
        # Try JSON first (strict format)
        if content.startswith('{') or content.startswith('['):
            try:
                return cls.parse_json(content)
            except json.JSONDecodeError:
                pass
        
        # Check if it's pure YAML (starts with --- and has yaml structure)
        if content.startswith('---'):
            # Try as pure YAML first
            try:
                return cls.parse_yaml(content)
            except yaml.YAMLError:
                pass
            
            # Then try as Markdown with frontmatter
            try:
                return cls.parse_markdown(content)
            except Exception:
                pass
        
        # Try YAML for other patterns
        if ':' in content:
            try:
                return cls.parse_yaml(content)
            except yaml.YAMLError:
                pass
        
        # Default to plain text as Markdown
        try:
            return cls.parse_markdown(content)
        except Exception:
            raise ValueError("Unable to parse input format")


class WordPressXMLGenerator:
    """Main generator class that creates complete WordPress XML files."""
    
    def __init__(self):
        self.factory = CholotComponentFactory()
        self.parser = InputFormatParser()
        self.base_url = "http://localhost:8082"
        self.site_title = "Generated Site"
        self.site_description = "Generated WordPress site"
        self.language = "en-US"
        
    def generate_xml(self, input_data: Union[str, Dict], site_config: Dict = None) -> str:
        """Generate complete WordPress XML from input data."""
        
        # Parse input if it's a string
        if isinstance(input_data, str):
            parsed_data = self.parser.auto_detect_and_parse(input_data)
        else:
            parsed_data = {'data': input_data, 'format': 'dict'}
        
        # Apply site configuration
        if site_config:
            self.site_title = site_config.get('title', self.site_title)
            self.site_description = site_config.get('description', self.site_description)
            self.base_url = site_config.get('base_url', self.base_url)
            self.language = site_config.get('language', self.language)
        
        # Generate XML structure
        xml_content = self._build_xml_structure(parsed_data)
        
        return xml_content
    
    def _build_xml_structure(self, parsed_data: Dict) -> str:
        """Build the complete WordPress XML structure."""
        
        # Extract data based on format
        if parsed_data['format'] in ['yaml', 'json', 'dict']:
            data = parsed_data.get('data', {})
        elif parsed_data['format'] == 'markdown':
            data = parsed_data.get('metadata', {})
            data['content'] = parsed_data.get('content', '')
        else:
            data = {}
        
        # Generate pages from data
        pages_xml = self._generate_pages(data.get('pages', []))
        
        # Build complete XML
        xml_template = f'''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Generated WordPress XML using Cholot Theme Generator -->
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>

<channel>
    <title>{html.escape(self.site_title)}</title>
    <link>{self.base_url}</link>
    <description>{html.escape(self.site_description)}</description>
    <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>
    <language>{self.language}</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>{self.base_url}</wp:base_site_url>
    <wp:base_blog_url>{self.base_url}</wp:base_blog_url>

    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[admin]]></wp:author_login>
        <wp:author_email><![CDATA[admin@example.com]]></wp:author_email>
        <wp:author_display_name><![CDATA[Administrator]]></wp:author_display_name>
        <wp:author_first_name><![CDATA[]]></wp:author_first_name>
        <wp:author_last_name><![CDATA[]]></wp:author_last_name>
    </wp:author>

    {self._generate_terms()}
    
    {pages_xml}

</channel>
</rss>'''
        
        return xml_template
    
    def _generate_terms(self) -> str:
        """Generate taxonomy terms (categories, tags, etc.)."""
        return '''
    <wp:category>
        <wp:term_id>1</wp:term_id>
        <wp:category_nicename><![CDATA[uncategorized]]></wp:category_nicename>
        <wp:category_parent><![CDATA[]]></wp:category_parent>
        <wp:cat_name><![CDATA[Uncategorized]]></wp:cat_name>
    </wp:category>
    
    <wp:term>
        <wp:term_id><![CDATA[2]]></wp:term_id>
        <wp:term_taxonomy><![CDATA[elementor_library_type]]></wp:term_taxonomy>
        <wp:term_slug><![CDATA[page]]></wp:term_slug>
        <wp:term_parent><![CDATA[]]></wp:term_parent>
        <wp:term_name><![CDATA[page]]></wp:term_name>
    </wp:term>
    
    <wp:term>
        <wp:term_id><![CDATA[3]]></wp:term_id>
        <wp:term_taxonomy><![CDATA[elementor_library_type]]></wp:term_taxonomy>
        <wp:term_slug><![CDATA[kit]]></wp:term_slug>
        <wp:term_parent><![CDATA[]]></wp:term_parent>
        <wp:term_name><![CDATA[kit]]></wp:term_name>
    </wp:term>'''
    
    def _generate_pages(self, pages_data: List[Dict]) -> str:
        """Generate page items from data."""
        pages_xml = []
        
        # First, generate the Elementor Kit
        kit_xml = self._generate_elementor_kit()
        pages_xml.append(kit_xml)
        
        # Then generate regular pages
        for i, page_data in enumerate(pages_data, 1):
            page_xml = self._generate_single_page(page_data, i + 100)  # Start page IDs at 101
            pages_xml.append(page_xml)
        
        return '\n'.join(pages_xml)
    
    def _generate_single_page(self, page_data: Dict, page_id: int) -> str:
        """Generate a single page XML."""
        
        title = page_data.get('title', f'Page {page_id}')
        slug = page_data.get('slug', f'page-{page_id}')
        status = page_data.get('status', 'publish')
        
        # Use custom post_id if provided
        if 'post_id' in page_data:
            page_id = page_data['post_id']
        
        # Handle raw elementor_data or generate from sections
        if 'elementor_data_file' in page_data:
            # Load elementor data from file
            with open(page_data['elementor_data_file'], 'r') as f:
                elementor_data = json.load(f)
            elementor_json = json.dumps(elementor_data, separators=(',', ':'))
            elements_usage = self._calculate_elements_usage(elementor_data)
        elif 'elementor_data' in page_data:
            # Use raw elementor data exactly as provided
            elementor_json = page_data['elementor_data']
            # Try to parse and calculate elements usage
            try:
                elementor_data = json.loads(elementor_json)
                elements_usage = self._calculate_elements_usage(elementor_data)
            except:
                elements_usage = {}
        else:
            # Generate Elementor data from sections (legacy support)
            elementor_data = self._generate_elementor_data(page_data.get('sections', []))
            elementor_json = json.dumps(elementor_data, separators=(',', ':'))
            elements_usage = self._calculate_elements_usage(elementor_data)
        
        elements_usage_serialized = self._php_serialize_array(elements_usage)
        
        # Handle custom content
        content = page_data.get('content', ' ')
        
        # Handle custom template
        template = page_data.get('template', 'blank-builder.php')
        
        # Generate meta fields
        meta_fields = page_data.get('meta_fields', {})
        additional_meta = page_data.get('additional_meta', {})
        
        page_xml = f'''
    <item>
        <title>{html.escape(title)}</title>
        <link>{self.base_url}/{slug}/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">{self.base_url}/?page_id={page_id}</guid>
        <description></description>
        <content:encoded><![CDATA[{content}]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>{page_id}</wp:post_id>
        <wp:post_date><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[{slug}]]></wp:post_name>
        <wp:status><![CDATA[{status}]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[{meta_fields.get('_elementor_edit_mode', 'builder')}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_template_type]]></wp:meta_key>
            <wp:meta_value><![CDATA[{meta_fields.get('_elementor_template_type', 'post')}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_version]]></wp:meta_key>
            <wp:meta_value><![CDATA[{meta_fields.get('_elementor_version', '2.6.2')}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[{meta_fields.get('_wp_page_template', template)}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
            <wp:meta_value><![CDATA[{elementor_json}]]></wp:meta_value>
        </wp:postmeta>'''

        # Add additional meta fields
        for key, value in additional_meta.items():
            page_xml += f'''
        <wp:postmeta>
            <wp:meta_key><![CDATA[{key}]]></wp:meta_key>
            <wp:meta_value><![CDATA[{value}]]></wp:meta_value>
        </wp:postmeta>'''

        page_xml += '''
    </item>'''
        
        return page_xml
    
    def _generate_elementor_kit(self) -> str:
        """Generate Elementor Kit post."""
        kit_settings = {
            "system_colors": [
                {"_id": "primary", "title": "Primary", "color": "#b68c2f"},
                {"_id": "secondary", "title": "Secondary", "color": "#232323"},
                {"_id": "text", "title": "Text", "color": "#7A7A7A"},
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
            "site_name": self.site_title,
            "site_description": self.site_description,
            "container_width": {"size": 1140, "unit": "px"},
            "space_between_widgets": {"size": 20, "unit": "px"}
        }
        
        kit_json = json.dumps(kit_settings, separators=(',', ':'))
        
        return f'''    <item>
        <title>Default Kit</title>
        <link>{self.base_url}/?elementor_library=default-kit</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">{self.base_url}/?post_type=elementor_library&#038;p=99</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>99</wp:post_id>
        <wp:post_date><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_date_gmt>
        <wp:post_modified><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_modified>
        <wp:post_modified_gmt><![CDATA[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]]></wp:post_modified_gmt>
        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[default-kit]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[elementor_library]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        <category domain="elementor_library_type" nicename="kit"><![CDATA[kit]]></category>
        
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_template_type]]></wp:meta_key>
            <wp:meta_value><![CDATA[kit]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_version]]></wp:meta_key>
            <wp:meta_value><![CDATA[3.15.0]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_page_settings]]></wp:meta_key>
            <wp:meta_value><![CDATA[{kit_json}]]></wp:meta_value>
        </wp:postmeta>
    </item>'''
    
    def _generate_elementor_data(self, sections_data: List[Dict]) -> List[Dict]:
        """Generate Elementor data structure from sections."""
        elementor_sections = []
        
        for section_data in sections_data:
            section_elements = []
            
            # Process columns
            columns = section_data.get('columns', [])
            if not columns:
                # Default single column
                columns = [{'width': 100, 'widgets': section_data.get('widgets', [])}]
            
            for column_data in columns:
                column_widgets = []
                
                # Process widgets in column
                for widget_data in column_data.get('widgets', []):
                    widget = self._create_widget_from_data(widget_data)
                    if widget:
                        column_widgets.append(widget)
                
                # Create column
                column = self.factory.create_column(
                    size=column_data.get('width', 100),
                    elements=column_widgets
                )
                section_elements.append(column)
            
            # Create section
            section_settings = section_data.get('settings', {})
            background_settings = section_settings.get('background', {})
            
            section = self.factory.create_section(
                structure=section_data.get('structure', '100'),
                elements=section_elements,
                background_settings=background_settings
            )
            
            elementor_sections.append(section)
        
        return elementor_sections
    
    def _create_widget_from_data(self, widget_data: Dict) -> Optional[Dict]:
        """Create widget from configuration data."""
        widget_type = widget_data.get('type', '')
        
        if widget_type == 'texticon':
            return self.factory.create_texticon_widget(widget_data)
        elif widget_type == 'title':
            return self.factory.create_title_widget(widget_data)
        elif widget_type in ['post-three', 'post-four']:
            post_type = widget_type.split('-')[1]
            return self.factory.create_post_widget(widget_data, post_type)
        elif widget_type == 'gallery':
            return self.factory.create_gallery_widget(widget_data)
        elif widget_type == 'logo':
            return self.factory.create_logo_widget(widget_data)
        elif widget_type == 'menu':
            return self.factory.create_menu_widget(widget_data)
        elif widget_type == 'button-text':
            return self.factory.create_button_text_widget(widget_data)
        elif widget_type == 'team':
            return self.factory.create_team_widget(widget_data)
        elif widget_type == 'testimonial':
            return self.factory.create_testimonial_widget(widget_data)
        elif widget_type == 'text-line':
            return self.factory.create_text_line_widget(widget_data)
        elif widget_type == 'contact':
            return self.factory.create_contact_widget(widget_data)
        elif widget_type == 'sidebar':
            return self.factory.create_sidebar_widget(widget_data)
        else:
            print(f"Warning: Unknown widget type '{widget_type}' - skipping")
            return None
    
    def _calculate_elements_usage(self, elementor_data: List[Dict]) -> Dict[str, int]:
        """Calculate element usage statistics."""
        usage = {}
        
        def count_elements(elements):
            for element in elements:
                el_type = element.get('elType', '')
                widget_type = element.get('widgetType', '')
                
                if el_type == 'widget' and widget_type:
                    usage[widget_type] = usage.get(widget_type, 0) + 1
                elif el_type in ['section', 'column']:
                    usage[el_type] = usage.get(el_type, 0) + 1
                
                # Recursively count nested elements
                if 'elements' in element:
                    count_elements(element['elements'])
        
        count_elements(elementor_data)
        return usage
    
    def _php_serialize_array(self, data: Dict[str, int]) -> str:
        """Create PHP-serialized array format for WordPress."""
        items = []
        for key, value in data.items():
            items.append(f's:{len(key)}:"{key}";i:{value}')
        
        array_content = ''.join(items)
        return f'a:{len(data)}:{{{array_content}}}'


def main():
    """Main function for CLI usage."""
    import argparse
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Generate WordPress XML from YAML/JSON/Markdown')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output XML file path')
    
    args = parser.parse_args()
    
    # Read input file
    with open(args.input, 'r', encoding='utf-8') as f:
        yaml_input = f.read()
    
    # Create generator and generate XML
    generator = WordPressXMLGenerator()
    
    # Parse YAML and extract site config
    parsed = yaml.safe_load(yaml_input)
    site_config = parsed.get('site', {})
    
    # Generate XML
    xml_output = generator.generate_xml(yaml_input, site_config)
    
    # Save to file
    output_path = Path(args.output).resolve()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_output)
    
    print(f"✅ Generated WordPress XML: {output_path}")
    print(f"📄 File size: {len(xml_output):,} characters")
    
    # Validate XML
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(xml_output)
        print("✅ XML validation successful - file is well-formed")
    except ET.ParseError as e:
        print(f"❌ XML validation failed: {e}")


if __name__ == "__main__":
    main()