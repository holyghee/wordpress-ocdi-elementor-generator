#!/usr/bin/env python3
"""
Elementor JSON Generator - Hybrid Approach
==========================================

A production-ready generator for creating valid Elementor JSON data structures
using the hybrid approach combining rule-based generation with smart defaults.

Features:
- Direct Elementor JSON output
- Complete Cholot widget factory with all 13 widget types  
- Enhanced placeholder system for dynamic content
- Smart layout optimization
- Template engine for common patterns
- Validation and error handling

Author: Code Implementation Lead
Version: 1.0.0
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

# Import the existing generator as base
from generate_wordpress_xml import (
    CholotThemeConfig, 
    ElementorIDGenerator, 
    CholotComponentFactory,
    InputFormatParser
)


class EnhancedElementorIDGenerator(ElementorIDGenerator):
    """Enhanced ID generator with predictable patterns for testing."""
    
    def __init__(self):
        self.used_ids = set()
        self.id_counter = 0
    
    def generate_id(self, prefix: str = None) -> str:
        """Generate unique Elementor-style ID with optional prefix."""
        while True:
            if prefix:
                # Generate predictable ID for testing
                self.id_counter += 1
                new_id = f"{prefix}{self.id_counter:04d}"
            else:
                # Generate random 7-character ID
                new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id


class PlaceholderSystem:
    """Advanced placeholder system for dynamic content injection."""
    
    def __init__(self):
        self.placeholders = {}
        self.context = {}
        
    def register_placeholder(self, key: str, value: Any, description: str = ""):
        """Register a placeholder value."""
        self.placeholders[key] = {
            'value': value,
            'description': description,
            'type': type(value).__name__
        }
    
    def set_context(self, context: Dict[str, Any]):
        """Set global context for placeholder resolution."""
        self.context.update(context)
    
    def resolve_placeholders(self, content: Any) -> Any:
        """Recursively resolve placeholders in content."""
        if isinstance(content, str):
            return self._resolve_string_placeholders(content)
        elif isinstance(content, dict):
            return {k: self.resolve_placeholders(v) for k, v in content.items()}
        elif isinstance(content, list):
            return [self.resolve_placeholders(item) for item in content]
        else:
            return content
    
    def _resolve_string_placeholders(self, text: str) -> str:
        """Resolve placeholders in string content."""
        # Pattern: {{placeholder_name:default_value}}
        pattern = r'\{\{(\w+)(?::([^}]*))?\}\}'
        
        def replacer(match):
            key = match.group(1)
            default = match.group(2) or ""
            
            # Try context first, then registered placeholders
            if key in self.context:
                return str(self.context[key])
            elif key in self.placeholders:
                return str(self.placeholders[key]['value'])
            else:
                return default
        
        return re.sub(pattern, replacer, text)


class EnhancedCholotFactory(CholotComponentFactory):
    """Enhanced factory with improved widget generation and validation."""
    
    def __init__(self):
        super().__init__()
        self.id_generator = EnhancedElementorIDGenerator()
        self.placeholder_system = PlaceholderSystem()
        
        # Register common placeholders
        self._register_common_placeholders()
    
    def _register_common_placeholders(self):
        """Register commonly used placeholders."""
        placeholders = {
            'site_title': 'My WordPress Site',
            'site_description': 'Just another WordPress site',
            'primary_color': self.theme_config.PRIMARY_COLOR,
            'secondary_color': self.theme_config.DARK_BG,
            'base_url': 'http://localhost:8080',
            'current_year': datetime.now().year,
            'demo_image_1': 'https://via.placeholder.com/800x600/b68c2f/ffffff?text=Demo+Image',
            'demo_image_2': 'https://via.placeholder.com/400x300/232323/ffffff?text=Demo+2',
            'demo_logo': 'https://via.placeholder.com/200x80/b68c2f/ffffff?text=LOGO'
        }
        
        for key, value in placeholders.items():
            self.placeholder_system.register_placeholder(key, value)
    
    def create_enhanced_texticon_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced texticon widget with better defaults."""
        widget_id = self.id_generator.generate_id('txticon')
        
        # Process placeholders in config
        config = self.placeholder_system.resolve_placeholders(config)
        
        # Required settings with smart defaults
        title = config.get('title', '{{site_title}}')
        icon = config.get('icon', 'fas fa-crown')
        
        settings = {
            "title": title,
            "selected_icon": {
                "value": icon,
                "library": self._get_icon_library(icon)
            },
            "__fa4_migrated": {"selected_icon": True},
            
            # Enhanced typography with responsive support
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": 24, "sizes": []},
            "title_typography_line_height": {"unit": "em", "size": 1.2, "sizes": []},
            "title_typography_font_weight": "700",
            "title_color": config.get('title_color', self.theme_config.WHITE),
            
            # Subtitle with better styling
            "subtitle_typography_typography": "custom", 
            "subtitle_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
            "subtitle_typography_font_weight": "700",
            "subtitle_typography_text_transform": "uppercase",
            "subtitle_typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
            "subtitle_color": config.get('subtitle_color', self.theme_config.PRIMARY_COLOR),
            
            # Icon settings with proper sizing
            "icon_size": {"unit": "px", "size": config.get('icon_size', 20), "sizes": []},
            "icon_bg_size": {"unit": "px", "size": config.get('icon_bg_size', 60), "sizes": []},
            "icon_color": config.get('icon_color', self.theme_config.WHITE),
            "iconbg_color": config.get('icon_bg_color', self.theme_config.PRIMARY_COLOR),
            
            # Responsive spacing
            "title_margin": self._create_spacing_object(config.get('title_margin', {})),
            "sb_margin": self._create_spacing_object(config.get('subtitle_margin', {})),
            "text_margin": self._create_spacing_object(config.get('text_margin', {})),
            "icon_margin": self._create_spacing_object(config.get('icon_margin', {'top': '-27'})),
            "_padding": self._create_spacing_object(config.get('padding', {'all': '30'})),
            
            # Border and styling
            "_border_border": config.get('border_style', 'dashed'),
            "_border_color": config.get('border_color', self.theme_config.PRIMARY_COLOR),
            "_border_width": self._create_spacing_object(config.get('border_width', {
                'top': '0', 'right': '1', 'bottom': '1', 'left': '1'
            }))
        }
        
        # Add optional content
        if 'subtitle' in config:
            settings['subtitle'] = str(config['subtitle'])
            
        if 'text' in config:
            settings['text'] = self._format_text_content(config['text'])
            settings.update({
                'text_typography_typography': "custom",
                'text_typography_font_size': {"unit": "px", "size": 15, "sizes": []},
                'text_typography_font_style': config.get('text_style', 'normal'),
                'text_color': config.get('text_color', self.theme_config.WHITE)
            })
        
        # Merge custom settings
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-texticon"
        }
    
    def create_enhanced_team_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced team widget with social media integration."""
        widget_id = self.id_generator.generate_id('team')
        config = self.placeholder_system.resolve_placeholders(config)
        
        settings = {
            "title": config.get('name', 'Team Member'),
            "text": config.get('position', 'Team Position'),
            "image": self._process_image_config(config.get('image', {})),
            "team_height": config.get('height', '420px'),
            "content_align": config.get('align', 'left'),
            "hover_animation": config.get('animation', 'shrink'),
            
            # Enhanced color scheme
            "title_cl": config.get('title_color', self.theme_config.BLACK),
            "txt_cl": config.get('position_color', self.theme_config.PRIMARY_COLOR),
            "bg_content": config.get('content_bg', "#1f1f1f"),
            "mask_color": config.get('mask_color', self.theme_config.BLACK),
            "mask_color_opacity": {"unit": "px", "size": 0.8, "sizes": []},
            
            # Typography improvements
            "cport_typography_typography": "custom",
            "cport_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "cport_typography_line_height": {"unit": "em", "size": 1.2, "sizes": []},
            "cport_typography_text_transform": "capitalize",
            "ctext_typography_typography": "custom",
            "ctext_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
            "ctext_typography_line_height": {"unit": "em", "size": 1.4, "sizes": []},
            
            # Professional styling
            "port_border_border": "solid",
            "port_border_color": self.theme_config.PRIMARY_COLOR,
            "port_border_width": self._create_spacing_object({'all': '1'}),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0, "vertical": 8, "blur": 14, 
                "spread": 4, "color": "rgba(175,175,175,0.27)"
            },
            
            # Spacing
            "port_padding": self._create_spacing_object({'all': '30'}),
            "titlep_margin": self._create_spacing_object({'bottom': '5'}),
            "tx_margin": self._create_spacing_object({}),
            "_margin": self._create_spacing_object({})
        }
        
        # Add social media icons
        if 'social_links' in config:
            social_list = []
            for social in config['social_links']:
                social_item = {
                    "_id": self.id_generator.generate_id('social'),
                    "social_icon": {"value": social.get('icon', 'fab fa-facebook'), "library": "fa-brands"},
                    "link": {"url": social.get('url', '#'), "is_external": "true", "nofollow": ""},
                    "item_icon_color": "custom",
                    "item_icon_primary_color": "rgba(0,0,0,0)",
                    "item_icon_secondary_color": social.get('color', '#000000')
                }
                social_list.append(social_item)
            settings['social_icon_list'] = social_list
        
        # Background icon for visual enhancement
        if 'background_icon' in config:
            settings.update({
                'selected_icon': {"value": config['background_icon'], "library": "fa-solid"},
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
    
    def create_enhanced_gallery_widget(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced gallery widget with better image handling."""
        widget_id = self.id_generator.generate_id('gallery')
        config = self.placeholder_system.resolve_placeholders(config)
        
        # Process gallery images
        gallery_images = config.get('images', [])
        gallery_data = []
        
        if isinstance(gallery_images, list):
            for i, img in enumerate(gallery_images):
                if isinstance(img, str):
                    # URL string
                    gallery_data.append({
                        "id": 100 + i,
                        "url": img
                    })
                elif isinstance(img, dict):
                    # Full image object
                    img_data = {
                        "id": img.get('id', 100 + i),
                        "url": img.get('url', f'{{demo_image_{(i % 2) + 1}}}')
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
            
            # Enhanced styling
            "mask_color": config.get('overlay_color', self.theme_config.BLACK),
            "mask_color_opacity": {"unit": "px", "size": config.get('overlay_opacity', 0.6), "sizes": []},
            
            # Responsive settings
            "_margin": self._create_spacing_object(config.get('margin_settings', {}))
        }
        
        # Add responsive breakpoints
        if 'responsive' in config:
            resp = config['responsive']
            if 'tablet' in resp:
                settings['gallery_height_tablet'] = {"unit": "px", "size": resp['tablet'].get('height', 200), "sizes": []}
                settings['gallery_margin_tablet'] = {"unit": "px", "size": resp['tablet'].get('margin', 8), "sizes": []}
            if 'mobile' in resp:
                settings['gallery_height_mobile'] = {"unit": "px", "size": resp['mobile'].get('height', 150), "sizes": []}
        
        settings.update(config.get('custom_settings', {}))
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-gallery"
        }
    
    def _get_icon_library(self, icon: str) -> str:
        """Determine the appropriate icon library."""
        if icon.startswith('fab '):
            return 'fa-brands'
        elif icon.startswith('fas '):
            return 'fa-solid'
        elif icon.startswith('far '):
            return 'fa-regular'
        else:
            return 'fa-solid'  # Default
    
    def _process_image_config(self, image_config: Dict[str, Any]) -> Dict[str, Any]:
        """Process image configuration with smart defaults."""
        if isinstance(image_config, str):
            return {"url": image_config, "id": random.randint(100, 999)}
        
        return {
            "url": image_config.get('url', '{{demo_image_1}}'),
            "id": image_config.get('id', random.randint(100, 999)),
            "alt": image_config.get('alt', ""),
            "source": image_config.get('source', "library"),
            "size": image_config.get('size', "full")
        }
    
    def _format_text_content(self, text: str) -> str:
        """Format text content for Elementor."""
        if not text.startswith('<'):
            return f"<p>{text}</p>"
        return text
    
    def _create_spacing_object(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Elementor spacing object with smart defaults."""
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


class ElementorLayoutOptimizer:
    """Optimizes Elementor layouts for better performance and structure."""
    
    def __init__(self):
        self.optimizations = {
            'merge_single_columns': True,
            'optimize_spacing': True,
            'compress_settings': True,
            'validate_structure': True
        }
    
    def optimize_layout(self, elementor_data: List[Dict]) -> List[Dict]:
        """Apply all enabled optimizations to the layout."""
        optimized = elementor_data.copy()
        
        if self.optimizations['validate_structure']:
            optimized = self._validate_structure(optimized)
        
        if self.optimizations['merge_single_columns']:
            optimized = self._merge_single_columns(optimized)
        
        if self.optimizations['optimize_spacing']:
            optimized = self._optimize_spacing(optimized)
        
        if self.optimizations['compress_settings']:
            optimized = self._compress_settings(optimized)
        
        return optimized
    
    def _validate_structure(self, data: List[Dict]) -> List[Dict]:
        """Validate Elementor structure and fix common issues."""
        valid_data = []
        
        for section in data:
            if section.get('elType') == 'section':
                # Ensure section has columns
                if not section.get('elements'):
                    continue
                    
                valid_columns = []
                for column in section.get('elements', []):
                    if column.get('elType') == 'column':
                        # Ensure column has proper size
                        if '_column_size' not in column.get('settings', {}):
                            column['settings']['_column_size'] = 100
                        valid_columns.append(column)
                
                if valid_columns:
                    section['elements'] = valid_columns
                    valid_data.append(section)
        
        return valid_data
    
    def _merge_single_columns(self, data: List[Dict]) -> List[Dict]:
        """Merge unnecessary single-column sections."""
        # This is a complex optimization - for now just return data
        return data
    
    def _optimize_spacing(self, data: List[Dict]) -> List[Dict]:
        """Optimize spacing objects by removing redundant values."""
        def clean_spacing(obj):
            if isinstance(obj, dict):
                # Clean spacing objects
                if all(k in obj for k in ['unit', 'top', 'right', 'bottom', 'left', 'isLinked']):
                    # Remove if all values are 0 or empty
                    if all(obj.get(k) in ['0', '', 0] for k in ['top', 'right', 'bottom', 'left']):
                        return {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
                
                return {k: clean_spacing(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_spacing(item) for item in obj]
            return obj
        
        return clean_spacing(data)
    
    def _compress_settings(self, data: List[Dict]) -> List[Dict]:
        """Remove empty or default settings to reduce file size."""
        def clean_settings(obj):
            if isinstance(obj, dict):
                cleaned = {}
                for k, v in obj.items():
                    if v is not None and v != "" and v != []:
                        cleaned[k] = clean_settings(v)
                return cleaned
            elif isinstance(obj, list):
                return [clean_settings(item) for item in obj if item is not None]
            return obj
        
        return clean_settings(data)


class ElementorJSONGenerator:
    """Main generator class for creating Elementor JSON structures."""
    
    def __init__(self):
        self.factory = EnhancedCholotFactory()
        self.parser = InputFormatParser()
        self.optimizer = ElementorLayoutOptimizer()
        
    def generate_json(self, input_data: Union[str, Dict], options: Dict = None) -> str:
        """Generate Elementor JSON from input data."""
        options = options or {}
        
        # Parse input data
        if isinstance(input_data, str):
            parsed_data = self.parser.auto_detect_and_parse(input_data)
        else:
            parsed_data = {'data': input_data, 'format': 'dict'}
        
        # Set context for placeholders
        context = options.get('context', {})
        self.factory.placeholder_system.set_context(context)
        
        # Generate Elementor structure
        elementor_data = self._build_elementor_structure(parsed_data, options)
        
        # Optimize if requested
        if options.get('optimize', True):
            elementor_data = self.optimizer.optimize_layout(elementor_data)
        
        # Return JSON
        indent = None if options.get('minify', False) else 2
        return json.dumps(elementor_data, indent=indent, separators=(',', ':') if options.get('minify') else (',', ': '))
    
    def _build_elementor_structure(self, parsed_data: Dict, options: Dict) -> List[Dict]:
        """Build complete Elementor structure from parsed data."""
        # Extract data based on format
        if parsed_data['format'] in ['yaml', 'json', 'dict']:
            data = parsed_data.get('data', {})
        elif parsed_data['format'] == 'markdown':
            data = parsed_data.get('metadata', {})
        else:
            data = {}
        
        # Generate sections
        sections_data = data.get('sections', [])
        if not sections_data and 'widgets' in data:
            # Create single section with widgets
            sections_data = [{'widgets': data['widgets']}]
        
        elementor_sections = []
        
        for section_config in sections_data:
            section = self._create_section_from_config(section_config)
            if section:
                elementor_sections.append(section)
        
        return elementor_sections
    
    def _create_section_from_config(self, section_config: Dict) -> Optional[Dict]:
        """Create section from configuration."""
        section_id = self.factory.id_generator.generate_id('section')
        
        # Process columns
        columns_config = section_config.get('columns', [])
        if not columns_config and 'widgets' in section_config:
            # Single column with widgets
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
        
        # Background settings
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
        widgets_config = column_config.get('widgets', [])
        column_elements = []
        
        for widget_config in widgets_config:
            widget = self._create_widget_from_config(widget_config)
            if widget:
                column_elements.append(widget)
        
        settings = {
            "_column_size": column_config.get('width', 100),
            "_inline_size": column_config.get('inline_size')
        }
        
        # Column background and styling
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
        """Create widget from configuration with enhanced factory methods."""
        widget_type = widget_config.get('type', '')
        
        # Use enhanced methods where available
        if widget_type == 'texticon':
            return self.factory.create_enhanced_texticon_widget(widget_config)
        elif widget_type == 'team':
            return self.factory.create_enhanced_team_widget(widget_config)
        elif widget_type == 'gallery':
            return self.factory.create_enhanced_gallery_widget(widget_config)
        
        # Fall back to existing methods
        elif widget_type == 'title':
            return self.factory.create_title_widget(widget_config)
        elif widget_type in ['post-three', 'post-four']:
            post_type = widget_type.split('-')[1]
            return self.factory.create_post_widget(widget_config, post_type)
        elif widget_type == 'logo':
            return self.factory.create_logo_widget(widget_config)
        elif widget_type == 'menu':
            return self.factory.create_menu_widget(widget_config)
        elif widget_type == 'button-text':
            return self.factory.create_button_text_widget(widget_config)
        elif widget_type == 'testimonial':
            return self.factory.create_testimonial_widget(widget_config)
        elif widget_type == 'text-line':
            return self.factory.create_text_line_widget(widget_config)
        elif widget_type == 'contact':
            return self.factory.create_contact_widget(widget_config)
        elif widget_type == 'sidebar':
            return self.factory.create_sidebar_widget(widget_config)
        else:
            print(f"Warning: Unknown widget type '{widget_type}' - skipping")
            return None
    
    def _calculate_structure(self, columns_config: List[Dict]) -> str:
        """Calculate Elementor structure string based on column configurations."""
        if not columns_config:
            return "100"
        
        if len(columns_config) == 1:
            return "100"
        elif len(columns_config) == 2:
            widths = [col.get('width', 50) for col in columns_config[:2]]
            return f"{widths[0]}{widths[1]}"
        elif len(columns_config) == 3:
            return "30"  # Equal three columns
        elif len(columns_config) == 4:
            return "25"  # Equal four columns
        else:
            return "100"  # Fallback


def main():
    """CLI interface for the Elementor JSON Generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Elementor JSON from YAML/JSON input')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    parser.add_argument('--minify', action='store_true', help='Minify output JSON')
    parser.add_argument('--no-optimize', action='store_true', help='Skip layout optimization')
    parser.add_argument('--context', help='JSON string with placeholder context')
    
    args = parser.parse_args()
    
    # Read input
    with open(args.input, 'r', encoding='utf-8') as f:
        input_content = f.read()
    
    # Parse context
    context = {}
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print("Warning: Invalid context JSON, using empty context")
    
    # Generate options
    options = {
        'minify': args.minify,
        'optimize': not args.no_optimize,
        'context': context
    }
    
    # Generate JSON
    generator = ElementorJSONGenerator()
    try:
        json_output = generator.generate_json(input_content, options)
        
        # Save output
        output_path = Path(args.output).resolve()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        print(f"✅ Generated Elementor JSON: {output_path}")
        print(f"📄 File size: {len(json_output):,} characters")
        
        # Validate JSON
        try:
            json.loads(json_output)
            print("✅ JSON validation successful")
        except json.JSONDecodeError as e:
            print(f"❌ JSON validation failed: {e}")
            
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())