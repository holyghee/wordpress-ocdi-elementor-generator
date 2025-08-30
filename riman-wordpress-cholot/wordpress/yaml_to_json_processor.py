#!/usr/bin/env python3
"""
YAML to Elementor JSON Processor
================================
Robust processor that converts simplified YAML to Elementor JSON structure.
Handles all 13 Cholot widget types with proper ID generation, nesting, and settings.

Features:
- Widget factory pattern for different widget types
- Template system for reusable components
- Dynamic ID generation for Elementor elements
- Proper nesting of sections, columns, and inner sections
- Shape divider configurations
- Responsive settings preservation
- Comprehensive error handling
"""

import yaml
import json
import logging
import uuid
import random
import string
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProcessingContext:
    """Context for tracking processing state and IDs"""
    page_id: int
    element_counter: int = 0
    generated_ids: List[str] = field(default_factory=list)
    base_url: str = "http://localhost:8080"
    language: str = "en-US"
    
    def generate_element_id(self) -> str:
        """Generate unique Elementor element ID"""
        # Elementor uses 8-character hex IDs
        element_id = ''.join(random.choices('0123456789abcdef', k=8))
        while element_id in self.generated_ids:
            element_id = ''.join(random.choices('0123456789abcdef', k=8))
        self.generated_ids.append(element_id)
        return element_id


class CholotWidgetFactory:
    """Factory for creating Cholot widgets with proper settings"""
    
    # Default Cholot theme colors and settings
    CHOLOT_COLORS = {
        'primary': '#b68c2f',
        'secondary': '#ffffff', 
        'dark': '#232323',
        'light': '#fafafa',
        'text': '#000000',
        'text_light': '#ffffff',
        'border': 'rgba(182,140,47,0.3)'
    }
    
    # Widget templates with default settings
    WIDGET_TEMPLATES = {
        'texticon': {
            'widgetType': 'cholot-texticon',
            'defaults': {
                'icon': 'fas fa-crown',
                'title_typography_typography': 'custom',
                'title_typography_font_size': {'unit': 'px', 'size': 24, 'sizes': []},
                'title_color': '#ffffff',
                'subtitle_typography_typography': 'custom',
                'subtitle_typography_font_size': {'unit': 'px', 'size': 13, 'sizes': []},
                'subtitle_typography_font_weight': '700',
                'subtitle_typography_text_transform': 'uppercase',
                'subtitle_typography_letter_spacing': {'unit': 'px', 'size': 1, 'sizes': []},
                'subtitle_color': '#b68c2f',
                'icon_size': {'unit': 'px', 'size': 20, 'sizes': []},
                'icon_bg_size': {'unit': 'px', 'size': 72, 'sizes': []},
                'icon_color': '#ffffff',
                'iconbg_color': '#b68c2f',
                'text_typography_font_size': {'unit': 'px', 'size': 15, 'sizes': []},
                'text_color': '#666666',
                '_padding': {'unit': 'px', 'top': '30', 'right': '30', 'bottom': '30', 'left': '30', 'isLinked': True}
            }
        },
        'title': {
            'widgetType': 'cholot-title',
            'defaults': {
                'header_size': 'h2',
                'align': 'left',
                'title_color': '#000000',
                'desc_typography_typography': 'custom',
                'desc_typography_font_size': {'unit': 'px', 'size': 32, 'sizes': []},
                'desc_typography_font_weight': '700',
                'desc_typography_line_height': {'unit': 'em', 'size': 1.2, 'sizes': []},
                'span_title_typo_typography': 'custom',
                'span_title_color': '#b68c2f'
            }
        },
        'team': {
            'widgetType': 'cholot-team',
            'defaults': {
                'team_height': {'unit': 'px', 'size': 420, 'sizes': []},
                'content_align': 'left',
                'hover_animation': 'shrink',
                'mask_color': '#000000',
                'mask_color_opacity': {'unit': 'px', 'size': 0.8, 'sizes': []},
                'cport_typography_typography': 'custom',
                'cport_typography_font_size': {'unit': 'px', 'size': 18, 'sizes': []},
                'ctext_typography_typography': 'custom',
                'ctext_typography_font_size': {'unit': 'px', 'size': 15, 'sizes': []},
                'port_padding': {'unit': 'px', 'top': '30', 'right': '30', 'bottom': '30', 'left': '30', 'isLinked': True},
                'bg_content': '#f4f4f4',
                'title_cl': '#000000',
                'txt_cl': '#b68c2f'
            }
        },
        'testimonial-two': {
            'widgetType': 'cholot-testimonial-two',
            'defaults': {
                'show_desktop': 3,
                'content-align': 'center',
                'title_typography_typography': 'custom',
                'title_typography_font_size': {'unit': 'px', 'size': 16, 'sizes': []},
                'name_typography_typography': 'custom',
                'name_typography_font_size': {'unit': 'px', 'size': 17, 'sizes': []},
                'name_typography_font_weight': '700',
                'name_color': '#ffffff',
                'post_typography_typography': 'custom',
                'post_typography_font_size': {'unit': 'px', 'size': 14, 'sizes': []},
                'post_color': '#b68c2f',
                'image_border_border': 'solid',
                'image_border_color': '#ffffff',
                'img_size': {'unit': 'px', 'size': 50, 'sizes': []}
            }
        },
        'text-line': {
            'widgetType': 'cholot-text-line',
            'defaults': {
                'title_typography_typography': 'custom',
                'title_typography_font_size': {'unit': 'px', 'size': 28, 'sizes': []},
                'subtitle_typography_typography': 'custom',
                'subtitle_typography_font_size': {'unit': 'px', 'size': 14, 'sizes': []},
                'subtitle_typography_font_weight': 'bold',
                'subtitle_typography_text_transform': 'uppercase',
                'subtitle_color': '#b68c2f',
                'line_color_hover': '#b68c2f',
                '_background_background': 'classic',
                '_background_color': '#fafafa'
            }
        },
        'contact': {
            'widgetType': 'cholot-contact',
            'defaults': {
                'btn_typography_typography': 'custom',
                'btn_typography_font_weight': '700',
                'btn_typography_text_transform': 'uppercase',
                'btn_typography_font_size': {'unit': 'px', 'size': 14, 'sizes': []},
                'btn_color': '#ffffff',
                'btn_color_hover': '#ffffff',
                'btn_bg': 'rgba(0,0,0,0)',
                'btn_bg_hover': '#b68c2f',
                'btn_border_color': '#b68c2f',
                'form_placeholder': '#ffffff',
                'form_bg': 'rgba(0,0,0,0)',
                'form_border_color': '#ffffff',
                'form_border_color_active': '#b68c2f'
            }
        },
        'button-text': {
            'widgetType': 'cholot-button-text',
            'defaults': {
                'btn_typography_typography': 'custom',
                'btn_typography_font_size': {'unit': 'px', 'size': 18, 'sizes': []},
                'btn_typography_font_weight': '700',
                'btn_typography_text_transform': 'uppercase',
                'btn_color': '#ffffff',
                'btn_bg': '#b68c2f',
                'btn_bg_hover': '#000000',
                'align': 'left'
            }
        },
        'gallery': {
            'widgetType': 'cholot-gallery',
            'defaults': {
                'port_column': 'col-md-4',
                'gallery_height': {'unit': 'px', 'size': 250, 'sizes': []},
                'gallery_margin': {'unit': 'px', 'size': 15, 'sizes': []},
                'title_show': '',
                'caption_show': ''
            }
        },
        'post-three': {
            'widgetType': 'cholot-post-three',
            'defaults': {
                'blog_post': '3',
                'blog_column': 'one',
                'show_excerpt': '',
                'excerpt_after': '...',
                'button': 'Read More'
            }
        },
        'post-four': {
            'widgetType': 'cholot-post-four',
            'defaults': {
                'blog_post': '4',
                'blog_column': 'two',
                'excerpt': '100',
                'button': 'Read More',
                'page_show': 'yes'
            }
        }
    }
    
    @classmethod
    def create_widget(cls, widget_type: str, content: Dict[str, Any], context: ProcessingContext) -> Dict[str, Any]:
        """Create a Cholot widget with proper settings"""
        try:
            # Get template for widget type
            template_key = widget_type.replace('cholot-', '') if widget_type.startswith('cholot-') else widget_type
            template = cls.WIDGET_TEMPLATES.get(template_key, {})
            
            if not template:
                logger.warning(f"Unknown widget type: {widget_type}")
                return cls._create_fallback_widget(widget_type, content, context)
            
            # Create base widget structure
            widget = {
                'id': context.generate_element_id(),
                'settings': template.get('defaults', {}).copy(),
                'elements': [],
                'isInner': False,
                'widgetType': template['widgetType'],
                'elType': 'widget'
            }
            
            # Apply content-specific settings
            cls._apply_content_settings(widget, content, template_key)
            
            # Apply custom settings if provided
            if 'custom_settings' in content:
                widget['settings'].update(content['custom_settings'])
            
            logger.debug(f"Created {widget_type} widget with ID: {widget['id']}")
            return widget
            
        except Exception as e:
            logger.error(f"Error creating widget {widget_type}: {str(e)}")
            return cls._create_fallback_widget(widget_type, content, context)
    
    @classmethod
    def _apply_content_settings(cls, widget: Dict[str, Any], content: Dict[str, Any], template_key: str):
        """Apply content-specific settings to widget"""
        
        if template_key == 'texticon':
            cls._apply_texticon_settings(widget, content)
        elif template_key == 'title':
            cls._apply_title_settings(widget, content)
        elif template_key == 'team':
            cls._apply_team_settings(widget, content)
        elif template_key == 'testimonial-two':
            cls._apply_testimonial_settings(widget, content)
        elif template_key == 'text-line':
            cls._apply_text_line_settings(widget, content)
        elif template_key == 'contact':
            cls._apply_contact_settings(widget, content)
        elif template_key == 'button-text':
            cls._apply_button_text_settings(widget, content)
        elif template_key == 'gallery':
            cls._apply_gallery_settings(widget, content)
        elif template_key == 'post-three':
            cls._apply_post_settings(widget, content)
        elif template_key == 'post-four':
            cls._apply_post_settings(widget, content)
    
    @classmethod
    def _apply_texticon_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply texticon-specific settings"""
        settings = widget['settings']
        
        if 'title' in content:
            settings['title'] = content['title']
        if 'subtitle' in content:
            settings['subtitle'] = content['subtitle']
        if 'text' in content:
            settings['text'] = f"<p>{content['text']}</p>"
        if 'icon' in content:
            settings['selected_icon'] = {
                'value': content['icon'],
                'library': 'fa-solid' if content['icon'].startswith('fas') else 'fa-brands'
            }
            settings['__fa4_migrated'] = {'selected_icon': True}
    
    @classmethod
    def _apply_title_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply title-specific settings"""
        settings = widget['settings']
        
        if 'title' in content:
            settings['title'] = content['title']
        if 'header_size' in content:
            settings['header_size'] = content['header_size']
        if 'align' in content:
            settings['align'] = content['align']
    
    @classmethod
    def _apply_team_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply team-specific settings"""
        settings = widget['settings']
        
        if 'name' in content:
            settings['title'] = content['name']
        if 'position' in content:
            settings['text'] = content['position']
        if 'image_url' in content and 'image_id' in content:
            settings['image'] = {
                'url': content['image_url'],
                'id': content['image_id'],
                'alt': content.get('name', ''),
                'source': 'library',
                'size': ''
            }
        if 'height' in content:
            height_value = int(content['height'].replace('px', '')) if isinstance(content['height'], str) else content['height']
            settings['team_height'] = {'unit': 'px', 'size': height_value, 'sizes': []}
        if 'align' in content:
            settings['content_align'] = content['align']
        if 'social_links' in content:
            settings['social_icon_list'] = cls._create_social_links(content['social_links'])
    
    @classmethod
    def _apply_testimonial_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply testimonial-specific settings"""
        settings = widget['settings']
        
        if 'testimonials' in content:
            settings['testi_list'] = []
            for i, testimonial in enumerate(content['testimonials']):
                testi_item = {
                    'title': testimonial.get('name', ''),
                    'position': testimonial.get('position', ''),
                    'text': testimonial.get('text', ''),
                    '_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=7)),
                    'image2_size': 'thumbnail'
                }
                if 'image_url' in testimonial and 'image_id' in testimonial:
                    testi_item['image'] = {
                        'url': testimonial['image_url'],
                        'id': testimonial['image_id']
                    }
                settings['testi_list'].append(testi_item)
    
    @classmethod
    def _apply_text_line_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply text-line-specific settings"""
        settings = widget['settings']
        
        if 'title' in content:
            settings['title'] = content['title']
        if 'subtitle' in content:
            settings['subtitle'] = content['subtitle']
        if 'line_width' in content:
            settings['line'] = {'unit': 'px', 'size': content['line_width'], 'sizes': []}
        if 'line_height' in content:
            settings['line_height'] = {'unit': 'px', 'size': content['line_height'], 'sizes': []}
        if 'background_color' in content:
            settings['_background_color'] = content['background_color']
    
    @classmethod
    def _apply_contact_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply contact-specific settings"""
        settings = widget['settings']
        
        if 'shortcode' in content:
            settings['shortcode'] = content['shortcode']
        if 'button_width' in content:
            settings['btn_width'] = content['button_width']
    
    @classmethod
    def _apply_button_text_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply button-text-specific settings"""
        settings = widget['settings']
        
        if 'text' in content:
            settings['btn_text'] = content['text']
        if 'subtitle' in content:
            settings['btn_sub'] = content['subtitle']
        if 'link' in content:
            settings['link'] = {
                'url': content['link'],
                'is_external': content.get('external', '')
            }
        if 'icon' in content:
            settings['selected_icon'] = {
                'value': content['icon'],
                'library': 'fa-solid' if content['icon'].startswith('fas') else 'fa-brands'
            }
        if 'align' in content:
            settings['align'] = content['align']
    
    @classmethod
    def _apply_gallery_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply gallery-specific settings"""
        settings = widget['settings']
        
        if 'images' in content:
            settings['gallery'] = content['images']  # Array of image IDs
        if 'columns' in content:
            column_map = {'2': 'col-md-6', '3': 'col-md-4', '4': 'col-md-3'}
            settings['port_column'] = column_map.get(str(content['columns']), 'col-md-4')
        if 'height' in content:
            height_value = int(content['height'].replace('px', '')) if isinstance(content['height'], str) else content['height']
            settings['gallery_height'] = {'unit': 'px', 'size': height_value, 'sizes': []}
        if 'spacing' in content:
            spacing_value = int(content['spacing'].replace('px', '')) if isinstance(content['spacing'], str) else content['spacing']
            settings['gallery_margin'] = {'unit': 'px', 'size': spacing_value, 'sizes': []}
    
    @classmethod
    def _apply_post_settings(cls, widget: Dict[str, Any], content: Dict[str, Any]):
        """Apply post widget settings (both post-three and post-four)"""
        settings = widget['settings']
        
        if 'count' in content:
            settings['blog_post'] = str(content['count'])
        if 'columns' in content:
            column_map = {'1': 'one', '2': 'two', '3': 'three', '4': 'four'}
            settings['blog_column'] = column_map.get(str(content['columns']), 'two')
        if 'excerpt_length' in content:
            settings['excerpt'] = str(content['excerpt_length'])
        if 'button_text' in content:
            settings['button'] = content['button_text']
        if 'show_excerpt' in content:
            settings['show_excerpt'] = 'yes' if content['show_excerpt'] else ''
        if 'show_pagination' in content:
            settings['page_show'] = 'yes' if content['show_pagination'] else ''
    
    @classmethod
    def _create_social_links(cls, links: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Create social links array for team widget"""
        social_links = []
        for link in links:
            social_link = {
                'social_icon': {
                    'value': link['icon'],
                    'library': 'fa-brands' if 'fab' in link['icon'] else 'fa-solid'
                },
                '_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=7)),
                'link': {
                    'url': link['url'],
                    'is_external': 'true',
                    'nofollow': ''
                },
                'item_icon_color': 'custom',
                'item_icon_primary_color': 'rgba(0,0,0,0)',
                'item_icon_secondary_color': '#000000'
            }
            social_links.append(social_link)
        return social_links
    
    @classmethod
    def _create_fallback_widget(cls, widget_type: str, content: Dict[str, Any], context: ProcessingContext) -> Dict[str, Any]:
        """Create fallback widget for unknown types"""
        return {
            'id': context.generate_element_id(),
            'settings': content,
            'elements': [],
            'isInner': False,
            'widgetType': widget_type,
            'elType': 'widget'
        }


class ElementorStructureBuilder:
    """Builds proper Elementor section/column/widget structure"""
    
    COLUMN_SIZES = {
        100: '100',
        50: '50',
        33: '33.333',
        66: '66.666',
        25: '25',
        75: '75'
    }
    
    @classmethod
    def create_section(cls, section_data: Dict[str, Any], context: ProcessingContext) -> Dict[str, Any]:
        """Create Elementor section with columns and widgets"""
        try:
            section = {
                'id': context.generate_element_id(),
                'settings': cls._create_section_settings(section_data.get('settings', {})),
                'elements': [],
                'isInner': False,
                'elType': 'section'
            }
            
            # Check if this is a special section type (hero_slider, service_cards, etc.)
            section_type = section_data.get('type')
            if section_type:
                return cls._create_special_section(section_data, context, section)
            
            # Handle section structure (column layout)
            structure = section_data.get('structure', '100')
            columns_config = cls._parse_structure(structure)
            
            # Create columns - handle both 'columns' and 'widgets' directly
            columns = section_data.get('columns', [])
            widgets = section_data.get('widgets', [])
            
            if widgets and not columns:
                # Direct widgets - create single column layout
                column_data = {'widgets': widgets}
                column = cls._create_column(100, column_data, context)
                section['elements'].append(column)
            else:
                # Column-based layout
                for i, column_config in enumerate(columns_config):
                    if i < len(columns):
                        column_data = columns[i]
                        column = cls._create_column(column_config, column_data, context)
                        section['elements'].append(column)
                    else:
                        # Create empty column
                        column = cls._create_empty_column(column_config, context)
                        section['elements'].append(column)
            
            logger.debug(f"Created section with {len(section['elements'])} columns")
            return section
            
        except Exception as e:
            logger.error(f"Error creating section: {str(e)}")
            return cls._create_fallback_section(section_data, context)
    
    @classmethod
    def _create_section_settings(cls, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Create section settings with background, layout, and shape dividers"""
        section_settings = {
            'content_width': 'boxed',
            'gap': 'default'
        }
        
        if 'background' in settings:
            bg = settings['background']
            if bg.get('background_background') == 'classic':
                section_settings['background_background'] = 'classic'
                if 'background_color' in bg:
                    section_settings['background_color'] = bg['background_color']
                if 'background_image' in bg:
                    section_settings['background_image'] = bg['background_image']
                    section_settings['background_position'] = bg.get('background_position', 'center center')
                    section_settings['background_size'] = bg.get('background_size', 'cover')
        
        # Add shape dividers
        if 'shape_divider_top' in settings:
            cls._add_shape_divider(section_settings, 'top', settings['shape_divider_top'])
        if 'shape_divider_bottom' in settings:
            cls._add_shape_divider(section_settings, 'bottom', settings['shape_divider_bottom'])
        
        # Add responsive settings
        if 'padding' in settings:
            cls._add_responsive_spacing(section_settings, 'padding', settings['padding'])
        if 'margin' in settings:
            cls._add_responsive_spacing(section_settings, 'margin', settings['margin'])
        
        return section_settings
    
    @classmethod
    def _add_shape_divider(cls, settings: Dict[str, Any], position: str, divider_config: Dict[str, Any]):
        """Add shape divider configuration"""
        settings[f'shape_divider_{position}'] = divider_config.get('type', 'waves')
        settings[f'shape_divider_{position}_color'] = divider_config.get('color', '#b68c2f')
        settings[f'shape_divider_{position}_width'] = divider_config.get('width', {'unit': '%', 'size': 100, 'sizes': []})
        settings[f'shape_divider_{position}_height'] = divider_config.get('height', {'unit': 'px', 'size': 60, 'sizes': []})
        
        if divider_config.get('flip', False):
            settings[f'shape_divider_{position}_flip'] = 'yes'
        if divider_config.get('invert', False):
            settings[f'shape_divider_{position}_invert'] = 'yes'
    
    @classmethod
    def _add_responsive_spacing(cls, settings: Dict[str, Any], spacing_type: str, spacing_config: Dict[str, Any]):
        """Add responsive spacing settings"""
        if isinstance(spacing_config, dict):
            # Handle responsive spacing
            for device in ['desktop', 'tablet', 'mobile']:
                if device in spacing_config:
                    device_suffix = f'_{device}' if device != 'desktop' else ''
                    spacing_value = spacing_config[device]
                    
                    if isinstance(spacing_value, (int, str)):
                        settings[f'{spacing_type}{device_suffix}'] = {
                            'unit': 'px',
                            'top': str(spacing_value),
                            'right': str(spacing_value),
                            'bottom': str(spacing_value),
                            'left': str(spacing_value),
                            'isLinked': True
                        }
                    elif isinstance(spacing_value, dict):
                        settings[f'{spacing_type}{device_suffix}'] = {
                            'unit': spacing_value.get('unit', 'px'),
                            'top': str(spacing_value.get('top', 0)),
                            'right': str(spacing_value.get('right', 0)),
                            'bottom': str(spacing_value.get('bottom', 0)),
                            'left': str(spacing_value.get('left', 0)),
                            'isLinked': spacing_value.get('isLinked', False)
                        }
    
    @classmethod
    def _parse_structure(cls, structure: str) -> List[int]:
        """Parse structure string into column widths"""
        if structure == '100':
            return [100]
        elif structure == '50':
            return [50, 50]
        elif structure == '33':
            return [33, 33, 33]
        elif structure == '66':
            return [66, 33]
        elif structure == '25':
            return [25, 25, 25, 25]
        elif structure == '75':
            return [75, 25]
        else:
            # Try to parse custom structure
            try:
                widths = [int(w) for w in structure.split(',')]
                return widths
            except:
                return [100]  # Fallback
    
    @classmethod
    def _create_column(cls, width: int, column_data: Dict[str, Any], context: ProcessingContext) -> Dict[str, Any]:
        """Create Elementor column with widgets"""
        column = {
            'id': context.generate_element_id(),
            'settings': {
                '_column_size': cls.COLUMN_SIZES.get(width, str(width)),
                '_inline_size': None
            },
            'elements': [],
            'isInner': False,
            'elType': 'column'
        }
        
        # Add widgets to column
        widgets = column_data.get('widgets', [])
        for widget_data in widgets:
            widget_type = widget_data.get('type', 'texticon')
            if widget_type.startswith('cholot-'):
                widget = CholotWidgetFactory.create_widget(widget_type, widget_data, context)
            else:
                # Add cholot- prefix for known widgets
                widget = CholotWidgetFactory.create_widget(f'cholot-{widget_type}', widget_data, context)
            column['elements'].append(widget)
        
        return column
    
    @classmethod
    def _create_empty_column(cls, width: int, context: ProcessingContext) -> Dict[str, Any]:
        """Create empty column"""
        return {
            'id': context.generate_element_id(),
            'settings': {
                '_column_size': cls.COLUMN_SIZES.get(width, str(width)),
                '_inline_size': None
            },
            'elements': [],
            'isInner': False,
            'elType': 'column'
        }
    
    @classmethod
    def _create_special_section(cls, section_data: Dict[str, Any], context: ProcessingContext, base_section: Dict[str, Any]) -> Dict[str, Any]:
        """Create special section types like hero_slider, service_cards"""
        section_type = section_data.get('type')
        
        if section_type == 'hero_slider':
            return cls._create_hero_slider_section(section_data, context, base_section)
        elif section_type == 'service_cards' or section_type == 'services':
            return cls._create_service_cards_section(section_data, context, base_section)
        elif section_type == 'hero':
            return cls._create_hero_section(section_data, context, base_section)
        else:
            logger.warning(f"Unknown special section type: {section_type}")
            return base_section
    
    @classmethod
    def _create_hero_slider_section(cls, section_data: Dict[str, Any], context: ProcessingContext, base_section: Dict[str, Any]) -> Dict[str, Any]:
        """Create hero slider section with slides"""
        slides = section_data.get('slides', [])
        
        # Create column with slider widget
        column = {
            'id': context.generate_element_id(),
            'settings': {'_column_size': '100', '_inline_size': None},
            'elements': [],
            'isInner': False,
            'elType': 'column'
        }
        
        # Create slider widget (using rdn-slider or similar)
        slider_widget = {
            'id': context.generate_element_id(),
            'settings': {
                'slides': []
            },
            'elements': [],
            'isInner': False,
            'widgetType': 'rdn-slider',
            'elType': 'widget'
        }
        
        # Add slides to widget
        for slide in slides:
            slider_widget['settings']['slides'].append({
                'title': slide.get('title', ''),
                'subtitle': slide.get('subtitle', ''),
                'text': slide.get('text', ''),
                'button_text': slide.get('button_text', ''),
                'button_link': slide.get('button_link', ''),
                'image': slide.get('image', '')
            })
        
        column['elements'].append(slider_widget)
        base_section['elements'].append(column)
        return base_section
    
    @classmethod
    def _create_service_cards_section(cls, section_data: Dict[str, Any], context: ProcessingContext, base_section: Dict[str, Any]) -> Dict[str, Any]:
        """Create service cards section with cholot-texticon widgets"""
        services = section_data.get('services', [])
        columns = section_data.get('columns', 4)  # Default to 4 columns
        rows = section_data.get('rows', 2)        # Default to 2 rows
        
        # Calculate column width
        column_width = 100 // columns
        
        # Create columns for service cards
        current_column = 0
        for i, service in enumerate(services):
            if i % columns == 0 and i > 0:
                current_column += 1
            
            # Create or get column
            if len(base_section['elements']) <= (i % columns):
                column = {
                    'id': context.generate_element_id(),
                    'settings': {'_column_size': str(column_width), '_inline_size': None},
                    'elements': [],
                    'isInner': False,
                    'elType': 'column'
                }
                base_section['elements'].append(column)
            else:
                column = base_section['elements'][i % columns]
            
            # Create cholot-texticon widget
            widget_data = {
                'type': 'cholot-texticon',
                'title': service.get('title', ''),
                'subtitle': service.get('subtitle', ''),
                'description': service.get('description', ''),
                'text': service.get('text', service.get('description', '')),
                'icon': service.get('icon', 'fas fa-star'),
                'settings': service.get('settings', {})
            }
            
            widget = CholotWidgetFactory.create_widget('cholot-texticon', widget_data, context)
            column['elements'].append(widget)
        
        return base_section
    
    @classmethod 
    def _create_hero_section(cls, section_data: Dict[str, Any], context: ProcessingContext, base_section: Dict[str, Any]) -> Dict[str, Any]:
        """Create simple hero section with widgets"""
        widgets = section_data.get('widgets', [])
        
        # Create single column
        column = {
            'id': context.generate_element_id(),
            'settings': {'_column_size': '100', '_inline_size': None},
            'elements': [],
            'isInner': False,
            'elType': 'column'
        }
        
        # Add widgets to column
        for widget_data in widgets:
            widget_type = widget_data.get('type', 'texticon')
            if widget_type.startswith('cholot-'):
                widget = CholotWidgetFactory.create_widget(widget_type, widget_data, context)
            else:
                # Add cholot- prefix for known widgets
                widget = CholotWidgetFactory.create_widget(f'cholot-{widget_type}', widget_data, context)
            column['elements'].append(widget)
        
        base_section['elements'].append(column)
        return base_section
    
    @classmethod
    def _create_fallback_section(cls, section_data: Dict[str, Any], context: ProcessingContext) -> Dict[str, Any]:
        """Create fallback section for errors"""
        return {
            'id': context.generate_element_id(),
            'settings': {'content_width': 'boxed', 'gap': 'default'},
            'elements': [cls._create_empty_column(100, context)],
            'isInner': False,
            'elType': 'section'
        }


class YAMLToJSONProcessor:
    """Main processor class for converting YAML to Elementor JSON"""
    
    def __init__(self, base_url: str = "http://localhost:8080", debug: bool = False):
        self.base_url = base_url
        self.debug = debug
        if debug:
            logger.setLevel(logging.DEBUG)
        
        logger.info("YAML to JSON Processor initialized")
    
    def process_yaml_file(self, yaml_file: str) -> Dict[str, Any]:
        """Process YAML file and return Elementor JSON structure"""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            return self.process_yaml_data(yaml_data)
            
        except FileNotFoundError:
            logger.error(f"YAML file not found: {yaml_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing YAML file: {str(e)}")
            raise
    
    def process_yaml_data(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process YAML data and return Elementor JSON structure"""
        try:
            # Extract site information
            site_info = yaml_data.get('site', {})
            pages = yaml_data.get('pages', [])
            
            if not pages:
                raise ValueError("No pages found in YAML data")
            
            # Process each page
            result = {
                'site': site_info,
                'pages': [],
                'metadata': {
                    'processor': 'YAML to JSON Processor v1.0',
                    'total_pages': len(pages),
                    'base_url': self.base_url
                }
            }
            
            for i, page_data in enumerate(pages):
                # Type checking before processing
                if not isinstance(page_data, (dict, str)):
                    logger.warning(f"Unexpected page_data type at index {i}: {type(page_data)}. Converting to dict.")
                    page_data = {'title': f'Page {i+1}', 'sections': []}
                
                processed_page = self._process_page(page_data, i + 1000, site_info)
                result['pages'].append(processed_page)
            
            logger.info(f"Successfully processed {len(pages)} pages")
            return result
            
        except Exception as e:
            logger.error(f"Error processing YAML data: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    def _process_page(self, page_data: Union[Dict[str, Any], str, Any], page_id: int, site_info: Dict[str, Any]) -> Dict[str, Any]:
        """Process individual page"""
        try:
            # Type checking: handle case where page_data is a string instead of dict
            if isinstance(page_data, str):
                logger.warning(f"Expected dict for page_data but got string: {page_data[:100]}...")
                # Convert string to basic page structure
                page_data = {
                    'title': 'Converted Page',
                    'slug': 'converted-page',
                    'status': 'draft',
                    'sections': []
                }
            elif not isinstance(page_data, dict):
                logger.error(f"Invalid page_data type: {type(page_data)}")
                # Fallback to empty dict
                page_data = {}
            
            context = ProcessingContext(
                page_id=page_id,
                base_url=site_info.get('base_url', self.base_url),
                language=site_info.get('language', 'en-US')
            )
            
            # Create page structure with safe access to page_data
            page = {
                'id': page_id,
                'title': page_data.get('title', 'Untitled Page'),
                'slug': page_data.get('slug', 'page'),
                'status': page_data.get('status', 'publish'),
                'elementor_data': [],
                'metadata': {
                    'sections_count': len(page_data.get('sections', [])),
                    'generated_ids': []
                }
            }
            
            # Process sections
            sections = page_data.get('sections', [])
            for section_data in sections:
                section = ElementorStructureBuilder.create_section(section_data, context)
                page['elementor_data'].append(section)
            
            # Store generated IDs for reference
            page['metadata']['generated_ids'] = context.generated_ids
            
            logger.info(f"Processed page '{page['title']}' with {len(sections)} sections")
            return page
            
        except Exception as e:
            logger.error(f"Error processing page: {str(e)}")
            logger.debug(traceback.format_exc())
            
            # Safe access to page_data for fallback
            title = 'Error Page'
            slug = 'error'
            
            if isinstance(page_data, dict):
                title = page_data.get('title', 'Error Page')
                slug = page_data.get('slug', 'error')
            elif isinstance(page_data, str):
                title = f'Error: {page_data[:50]}...' if len(page_data) > 50 else f'Error: {page_data}'
                slug = 'error-string-data'
            
            # Return minimal fallback page
            return {
                'id': page_id,
                'title': title,
                'slug': slug,
                'status': 'draft',
                'elementor_data': [],
                'error': str(e),
                'page_data_type': str(type(page_data))
            }
    
    def save_json(self, json_data: Dict[str, Any], output_file: str):
        """Save processed data to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON data saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving JSON file: {str(e)}")
            raise
    
    def validate_structure(self, json_data: Dict[str, Any]) -> bool:
        """Validate generated JSON structure"""
        try:
            # Basic structure validation
            if 'pages' not in json_data:
                return False
            
            for page in json_data['pages']:
                if not isinstance(page.get('elementor_data'), list):
                    return False
                
                for section in page['elementor_data']:
                    if section.get('elType') != 'section':
                        return False
                    
                    for column in section.get('elements', []):
                        if column.get('elType') != 'column':
                            return False
                        
                        for widget in column.get('elements', []):
                            if widget.get('elType') != 'widget':
                                return False
                            if not widget.get('widgetType', '').startswith('cholot-'):
                                logger.warning(f"Non-Cholot widget found: {widget.get('widgetType')}")
            
            logger.info("JSON structure validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Structure validation failed: {str(e)}")
            return False


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert YAML to Elementor JSON')
    parser.add_argument('input_file', help='Input YAML file')
    parser.add_argument('-o', '--output', help='Output JSON file', default='output.json')
    parser.add_argument('--base-url', help='Base URL for the site', default='http://localhost:8080')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--validate', action='store_true', help='Validate output structure')
    
    args = parser.parse_args()
    
    try:
        processor = YAMLToJSONProcessor(base_url=args.base_url, debug=args.debug)
        result = processor.process_yaml_file(args.input_file)
        
        if args.validate:
            if not processor.validate_structure(result):
                logger.error("Structure validation failed!")
                return 1
        
        processor.save_json(result, args.output)
        logger.info("Processing completed successfully!")
        
        return 0
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return 1


if __name__ == '__main__':
    exit(main())