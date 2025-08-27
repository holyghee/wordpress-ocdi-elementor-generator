#!/usr/bin/env python3
"""
Placeholder System Design
========================

Advanced placeholder system with validation, content injection, and template management
Based on the hybrid architecture for maximum flexibility with reliability
"""

import re
import json
import copy
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
import logging


class PlaceholderType(Enum):
    """Types of placeholders supported by the system"""
    SIMPLE = "simple"           # {{key}}
    DEFAULT = "default"         # {{key|default_value}}
    CONDITIONAL = "conditional" # {{IF:key}}...{{/IF}}
    LOOP = "loop"              # {{LOOP:key}}...{{/LOOP}}
    FUNCTION = "function"      # {{FUNC:function_name:key}}
    NESTED = "nested"          # {{parent.child.field}}
    TRANSFORM = "transform"    # {{key|transform_name}}


@dataclass
class PlaceholderPattern:
    """Pattern definition for placeholder types"""
    pattern: str
    type: PlaceholderType
    processor: Callable
    description: str


class PlaceholderResolver:
    """
    Advanced placeholder resolution system for widget templates
    """
    
    def __init__(self, theme_config=None):
        self.theme_config = theme_config
        self.logger = logging.getLogger(__name__)
        self.custom_transforms = {}
        self.custom_functions = {}
        
        # Initialize built-in patterns
        self.patterns = self._init_patterns()
        
        # Initialize built-in transforms
        self._init_transforms()
        
        # Initialize built-in functions
        self._init_functions()
    
    def _init_patterns(self) -> List[PlaceholderPattern]:
        """Initialize placeholder patterns with their processors"""
        return [
            PlaceholderPattern(
                pattern=r'\{\{LOOP:(\w+)\}\}(.*?)\{\{/LOOP\}\}',
                type=PlaceholderType.LOOP,
                processor=self._process_loop,
                description="Process array loops: {{LOOP:items}}template{{/LOOP}}"
            ),
            PlaceholderPattern(
                pattern=r'\{\{IF:(\w+)\}\}(.*?)\{\{/IF\}\}',
                type=PlaceholderType.CONDITIONAL,
                processor=self._process_conditional,
                description="Conditional content: {{IF:field}}content{{/IF}}"
            ),
            PlaceholderPattern(
                pattern=r'\{\{FUNC:(\w+):([^}]+)\}\}',
                type=PlaceholderType.FUNCTION,
                processor=self._process_function,
                description="Function calls: {{FUNC:function_name:parameter}}"
            ),
            PlaceholderPattern(
                pattern=r'\{\{([^|}]+)\|([^}]+)\}\}',
                type=PlaceholderType.DEFAULT,
                processor=self._process_default,
                description="Default values: {{key|default_value}}"
            ),
            PlaceholderPattern(
                pattern=r'\{\{([^|}]+)\|(\w+)\((.*?)\)\}\}',
                type=PlaceholderType.TRANSFORM,
                processor=self._process_transform,
                description="Transforms: {{key|transform_name(params)}}"
            ),
            PlaceholderPattern(
                pattern=r'\{\{([^|}]+)\}\}',
                type=PlaceholderType.SIMPLE,
                processor=self._process_simple,
                description="Simple substitution: {{key}}"
            )
        ]
    
    def _init_transforms(self):
        """Initialize built-in transforms"""
        self.custom_transforms.update({
            'uppercase': lambda x, *args: str(x).upper(),
            'lowercase': lambda x, *args: str(x).lower(),
            'capitalize': lambda x, *args: str(x).capitalize(),
            'title': lambda x, *args: str(x).title(),
            'strip': lambda x, *args: str(x).strip(),
            'truncate': lambda x, length=50, *args: str(x)[:int(length)] + ('...' if len(str(x)) > int(length) else ''),
            'default_if_empty': lambda x, default_val, *args: default_val if not x else x,
            'wrap_html': lambda x, tag='p', *args: f'<{tag}>{x}</{tag}>',
            'json_encode': lambda x, *args: json.dumps(x),
            'to_int': lambda x, *args: int(x) if str(x).isdigit() else 0,
            'format_url': lambda x, *args: x if x.startswith(('http://', 'https://')) else f'https://{x}',
        })
    
    def _init_functions(self):
        """Initialize built-in functions"""
        self.custom_functions.update({
            'generate_id': lambda: self._generate_elementor_id(),
            'theme_color': lambda color_name: self._get_theme_color(color_name),
            'spacing_object': lambda: self._get_spacing_object(),
            'current_timestamp': lambda: self._get_current_timestamp(),
            'random_choice': lambda *choices: self._random_choice(*choices),
            'calculate_column_width': lambda column_count: 100 / int(column_count),
        })
    
    def resolve(self, template: Union[str, Dict], content_data: Dict[str, Any]) -> Union[str, Dict]:
        """
        Main resolution method - handles both string templates and dict templates
        """
        try:
            if isinstance(template, dict):
                return self._resolve_dict(template, content_data)
            elif isinstance(template, str):
                return self._resolve_string(template, content_data)
            else:
                return template
        except Exception as e:
            self.logger.error(f"Placeholder resolution failed: {e}")
            raise PlaceholderResolutionError(f"Failed to resolve placeholders: {e}")
    
    def _resolve_dict(self, template: Dict, content_data: Dict[str, Any]) -> Dict:
        """Resolve placeholders in dictionary template"""
        resolved = copy.deepcopy(template)
        
        # Convert to string, resolve, then parse back
        json_str = json.dumps(resolved)
        resolved_str = self._resolve_string(json_str, content_data)
        
        try:
            return json.loads(resolved_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error after placeholder resolution: {e}")
            # Fallback: try to fix common JSON issues
            resolved_str = self._fix_json_issues(resolved_str)
            return json.loads(resolved_str)
    
    def _resolve_string(self, template: str, content_data: Dict[str, Any]) -> str:
        """Resolve placeholders in string template"""
        resolved = template
        
        # Process patterns in order of complexity (most complex first)
        for pattern_def in self.patterns:
            matches = list(re.finditer(pattern_def.pattern, resolved, re.DOTALL))
            # Process matches in reverse order to avoid index shifting
            for match in reversed(matches):
                try:
                    replacement = pattern_def.processor(match, content_data)
                    resolved = resolved[:match.start()] + replacement + resolved[match.end():]
                except Exception as e:
                    self.logger.warning(f"Pattern {pattern_def.type} processing failed: {e}")
                    # Keep original placeholder on error for debugging
                    continue
        
        return resolved
    
    def _process_loop(self, match, content_data: Dict[str, Any]) -> str:
        """Process {{LOOP:items}}template{{/LOOP}} patterns"""
        loop_key = match.group(1).lower()
        template = match.group(2)
        
        items = self._get_nested_value(content_data, loop_key)
        if not isinstance(items, list):
            return ""
        
        results = []
        for i, item in enumerate(items):
            item_template = template
            
            # Create item context
            item_context = content_data.copy()
            if isinstance(item, dict):
                item_context.update(item)
                item_context['item'] = item
            else:
                item_context['item'] = item
            
            item_context['index'] = i
            item_context['index_1'] = i + 1  # 1-based index
            item_context['is_first'] = i == 0
            item_context['is_last'] = i == len(items) - 1
            
            # Resolve nested placeholders in item template
            resolved_item = self._resolve_string(item_template, item_context)
            results.append(resolved_item)
        
        return ','.join(results) if results else ""
    
    def _process_conditional(self, match, content_data: Dict[str, Any]) -> str:
        """Process {{IF:condition}}content{{/IF}} patterns"""
        condition_key = match.group(1).lower()
        content_block = match.group(2)
        
        condition_value = self._get_nested_value(content_data, condition_key)
        
        # Evaluate condition
        if self._is_truthy(condition_value):
            # Resolve nested placeholders in content block
            return self._resolve_string(content_block, content_data)
        else:
            return ""
    
    def _process_function(self, match, content_data: Dict[str, Any]) -> str:
        """Process {{FUNC:function_name:parameter}} patterns"""
        function_name = match.group(1)
        parameter = match.group(2)
        
        if function_name not in self.custom_functions:
            self.logger.warning(f"Unknown function: {function_name}")
            return match.group(0)  # Return original if function not found
        
        try:
            # Get parameter value from content_data
            param_value = self._get_nested_value(content_data, parameter)
            result = self.custom_functions[function_name](param_value)
            return str(result)
        except Exception as e:
            self.logger.error(f"Function {function_name} execution failed: {e}")
            return ""
    
    def _process_transform(self, match, content_data: Dict[str, Any]) -> str:
        """Process {{key|transform_name(params)}} patterns"""
        key = match.group(1).lower()
        transform_name = match.group(2)
        params_str = match.group(3)
        
        # Get value
        value = self._get_nested_value(content_data, key)
        
        if transform_name not in self.custom_transforms:
            self.logger.warning(f"Unknown transform: {transform_name}")
            return str(value)
        
        try:
            # Parse parameters
            params = [p.strip().strip("'\"") for p in params_str.split(',') if p.strip()]
            result = self.custom_transforms[transform_name](value, *params)
            return str(result)
        except Exception as e:
            self.logger.error(f"Transform {transform_name} execution failed: {e}")
            return str(value)
    
    def _process_default(self, match, content_data: Dict[str, Any]) -> str:
        """Process {{key|default_value}} patterns"""
        key = match.group(1).lower()
        default_value = match.group(2)
        
        value = self._get_nested_value(content_data, key)
        
        if value is None or value == "":
            # Handle special default values
            if default_value == "SPACING_OBJECT":
                return json.dumps(self._get_spacing_object())
            elif default_value.startswith("THEME_"):
                color_name = default_value.replace("THEME_", "").lower()
                return self._get_theme_color(color_name)
            else:
                return default_value
        
        return str(value)
    
    def _process_simple(self, match, content_data: Dict[str, Any]) -> str:
        """Process {{key}} patterns"""
        key = match.group(1).lower()
        value = self._get_nested_value(content_data, key)
        
        if value is None:
            self.logger.warning(f"Undefined placeholder: {key}")
            return match.group(0)  # Return original placeholder
        
        # Handle special value types
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value)
        
        return str(value)
    
    def _get_nested_value(self, data: Dict[str, Any], key_path: str) -> Any:
        """Get value from nested dictionary using dot notation"""
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _is_truthy(self, value: Any) -> bool:
        """Evaluate if value is truthy for conditional logic"""
        if value is None or value == "":
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (list, dict)):
            return len(value) > 0
        if isinstance(value, str):
            return value.lower() not in ('false', '0', 'no', 'off', 'none')
        return bool(value)
    
    def _fix_json_issues(self, json_str: str) -> str:
        """Attempt to fix common JSON issues after placeholder resolution"""
        # Remove trailing commas
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Fix double quotes in strings
        json_str = re.sub(r'(?<!\\)"(?=[^,}\]\s])', r'\\"', json_str)
        
        return json_str
    
    def _generate_elementor_id(self) -> str:
        """Generate Elementor-style ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    
    def _get_theme_color(self, color_name: str) -> str:
        """Get color from theme configuration"""
        if not self.theme_config:
            return "#000000"
        
        color_map = {
            'primary': getattr(self.theme_config, 'PRIMARY_COLOR', '#b68c2f'),
            'white': getattr(self.theme_config, 'WHITE', '#ffffff'),
            'black': getattr(self.theme_config, 'BLACK', '#000000'),
            'text': getattr(self.theme_config, 'TEXT_COLOR', '#878787'),
        }
        
        return color_map.get(color_name, "#000000")
    
    def _get_spacing_object(self) -> Dict[str, Any]:
        """Get theme spacing object"""
        if self.theme_config and hasattr(self.theme_config, 'SPACING_OBJECT'):
            return self.theme_config.SPACING_OBJECT.copy()
        
        return {
            "unit": "px",
            "top": "0",
            "right": "0",
            "bottom": "0",
            "left": "0",
            "isLinked": False
        }
    
    def _get_current_timestamp(self) -> int:
        """Get current timestamp"""
        import time
        return int(time.time())
    
    def _random_choice(self, *choices) -> Any:
        """Random choice from options"""
        import random
        return random.choice(choices) if choices else ""
    
    def register_transform(self, name: str, transform_func: Callable):
        """Register custom transform function"""
        self.custom_transforms[name] = transform_func
    
    def register_function(self, name: str, function: Callable):
        """Register custom function"""
        self.custom_functions[name] = function


class TemplateLibrary:
    """
    Library of reusable templates with placeholder patterns
    """
    
    def __init__(self):
        self.templates = {}
        self._load_widget_templates()
        self._load_section_templates()
    
    def _load_widget_templates(self):
        """Load all widget templates"""
        self.templates.update({
            'cholot-texticon': {
                "id": "{{FUNC:generate_id:}}",
                "elType": "widget", 
                "settings": {
                    "title": "{{title}}",
                    "{{IF:subtitle}}subtitle": "{{subtitle}}",{{/IF}}
                    "{{IF:text}}text": "{{text|wrap_html(p)}}",{{/IF}}
                    "selected_icon": {
                        "value": "{{icon|fas fa-crown}}",
                        "library": "fa-solid"
                    },
                    "__fa4_migrated": {"selected_icon": True},
                    
                    # Typography with theme integration
                    "title_typography_typography": "custom",
                    "title_typography_font_size": {"unit": "px", "size": 24, "sizes": []},
                    "title_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
                    "title_color": "{{title_color|THEME_WHITE}}",
                    
                    "subtitle_typography_typography": "custom", 
                    "subtitle_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
                    "subtitle_typography_font_weight": "700",
                    "subtitle_typography_text_transform": "uppercase",
                    "subtitle_typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
                    "subtitle_color": "{{subtitle_color|THEME_PRIMARY}}",
                    
                    # Icon settings
                    "icon_size": {"unit": "px", "size": 15, "sizes": []},
                    "icon_bg_size": {"unit": "px", "size": 35, "sizes": []},
                    
                    # Spacing with defaults
                    "title_margin": "{{title_margin|SPACING_OBJECT}}",
                    "sb_margin": "{{sb_margin|SPACING_OBJECT}}",
                    "sb_padding": "{{sb_padding|SPACING_OBJECT}}",
                    "text_margin": "{{text_margin|SPACING_OBJECT}}",
                    "icon_margin": "{{icon_margin|SPACING_OBJECT}}"
                },
                "elements": [],
                "widgetType": "cholot-texticon"
            },
            
            'cholot-services-section': {
                "id": "{{FUNC:generate_id:}}",
                "elType": "section",
                "settings": {
                    "structure": "{{layout.structure|33}}",
                    "gap": "extended",
                    "padding": {"unit": "px", "top": 60, "right": 0, "bottom": 60, "left": 0},
                    "{{IF:background}}background_background": "{{background.type|classic}}",
                    "background_color": "{{background.color|#ffffff}}"{{/IF}}
                },
                "elements": [
                    "{{LOOP:services}}{\"id\": \"{{FUNC:generate_id:}}\", \"elType\": \"column\", \"settings\": {\"_column_size\": {{FUNC:calculate_column_width:layout.columns}}, \"_inline_size\": null}, \"elements\": [{\"id\": \"{{FUNC:generate_id:}}\", \"elType\": \"widget\", \"widgetType\": \"cholot-texticon\", \"settings\": {\"title\": \"{{title}}\", \"text\": \"{{text|wrap_html(p)}}\", \"selected_icon\": {\"value\": \"{{icon|fas fa-check}}\", \"library\": \"fa-solid\"}}}], \"isInner\": false}{{/LOOP}}"
                ],
                "isInner": False
            }
        })
    
    def _load_section_templates(self):
        """Load section templates"""
        self.templates.update({
            'hero-section': {
                "id": "{{FUNC:generate_id:}}",
                "elType": "section",
                "settings": {
                    "gap": "no",
                    "layout": "full_width",
                    "background_background": "classic",
                    "background_image": {
                        "url": "{{hero.background_image}}",
                        "id": "{{hero.background_image_id|1}}"
                    },
                    "background_overlay_background": "classic",
                    "background_overlay_color": "{{hero.overlay_color|rgba(0,0,0,0.6)}}",
                    "background_overlay_opacity": {"unit": "px", "size": "{{hero.overlay_opacity|0.8}}", "sizes": []},
                    "padding": {"unit": "px", "top": 100, "right": 0, "bottom": 100, "left": 0}
                },
                "elements": [{
                    "id": "{{FUNC:generate_id:}}",
                    "elType": "column",
                    "settings": {"_column_size": 100},
                    "elements": [{
                        "id": "{{FUNC:generate_id:}}",
                        "elType": "widget",
                        "widgetType": "rdn-slider",
                        "settings": {
                            "slider_list": [{
                                "title": "{{hero.title}}",
                                "subtitle": "{{hero.subtitle|}}",
                                "text": "{{hero.text|}}",
                                "btn_text": "{{hero.button_text|Learn More}}",
                                "btn_link": {"url": "{{hero.button_url|#}}"},
                                "image": {
                                    "url": "{{hero.image_url}}",
                                    "id": "{{hero.image_id|1}}"
                                }
                            }]
                        }
                    }]
                }]
            }
        })
    
    def get_template(self, template_name: str) -> Dict[str, Any]:
        """Get template by name"""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
        return copy.deepcopy(self.templates[template_name])
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())
    
    def register_template(self, name: str, template: Dict[str, Any]):
        """Register new template"""
        self.templates[name] = template


class ContentValidator:
    """
    Validates content data against template requirements
    """
    
    def __init__(self, template_library: TemplateLibrary):
        self.template_library = template_library
    
    def validate_content(self, template_name: str, content_data: Dict[str, Any]) -> List[str]:
        """
        Validate content data against template requirements
        """
        errors = []
        template = self.template_library.get_template(template_name)
        
        # Extract placeholders from template
        required_placeholders = self._extract_required_placeholders(template)
        optional_placeholders = self._extract_optional_placeholders(template)
        
        # Check required placeholders
        for placeholder in required_placeholders:
            if not self._has_content_for_placeholder(placeholder, content_data):
                errors.append(f"Required content missing for: {placeholder}")
        
        # Validate data types where possible
        type_errors = self._validate_data_types(content_data)
        errors.extend(type_errors)
        
        return errors
    
    def _extract_required_placeholders(self, template: Any) -> List[str]:
        """Extract required placeholders (those not in IF blocks)"""
        template_str = json.dumps(template)
        
        # Find all placeholders
        all_placeholders = re.findall(r'\{\{([^|}]+)(?:\|[^}]*)?\}\}', template_str)
        
        # Filter out conditional ones
        conditional_blocks = re.findall(r'\{\{IF:[^}]+\}\}(.*?)\{\{/IF\}\}', template_str, re.DOTALL)
        conditional_placeholders = set()
        
        for block in conditional_blocks:
            block_placeholders = re.findall(r'\{\{([^|}]+)(?:\|[^}]*)?\}\}', block)
            conditional_placeholders.update(block_placeholders)
        
        # Required are those not in conditional blocks
        required = [p for p in all_placeholders if p not in conditional_placeholders and not p.startswith('FUNC:')]
        
        return list(set(required))
    
    def _extract_optional_placeholders(self, template: Any) -> List[str]:
        """Extract optional placeholders (those in IF blocks)"""
        template_str = json.dumps(template)
        
        conditional_blocks = re.findall(r'\{\{IF:[^}]+\}\}(.*?)\{\{/IF\}\}', template_str, re.DOTALL)
        optional_placeholders = set()
        
        for block in conditional_blocks:
            block_placeholders = re.findall(r'\{\{([^|}]+)(?:\|[^}]*)?\}\}', block)
            optional_placeholders.update(block_placeholders)
        
        return list(optional_placeholders)
    
    def _has_content_for_placeholder(self, placeholder: str, content_data: Dict[str, Any]) -> bool:
        """Check if content data has value for placeholder"""
        keys = placeholder.split('.')
        current = content_data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False
        
        return current is not None and current != ""
    
    def _validate_data_types(self, content_data: Dict[str, Any]) -> List[str]:
        """Validate data types for known fields"""
        errors = []
        
        # Define expected types
        type_expectations = {
            'services': list,
            'team_members': list,
            'testimonials': list,
            'gallery': list,
            'social_links': list,
            'background': dict,
            'responsive': dict,
            'layout': dict
        }
        
        for field, expected_type in type_expectations.items():
            if field in content_data and not isinstance(content_data[field], expected_type):
                errors.append(f"Field '{field}' should be {expected_type.__name__}, got {type(content_data[field]).__name__}")
        
        return errors


class PlaceholderResolutionError(Exception):
    """Custom exception for placeholder resolution errors"""
    pass


# Usage example and testing
if __name__ == "__main__":
    # Initialize system
    resolver = PlaceholderResolver()
    template_library = TemplateLibrary()
    validator = ContentValidator(template_library)
    
    # Example content
    content_data = {
        "title": "Professional Services",
        "subtitle": "Quality Guaranteed",
        "text": "We provide top-notch professional services",
        "icon": "fas fa-star",
        "services": [
            {"title": "Service 1", "text": "Description 1", "icon": "fas fa-check"},
            {"title": "Service 2", "text": "Description 2", "icon": "fas fa-star"},
            {"title": "Service 3", "text": "Description 3", "icon": "fas fa-heart"}
        ],
        "layout": {"structure": "33", "columns": 3}
    }
    
    # Validate content
    errors = validator.validate_content('cholot-texticon', content_data)
    if errors:
        print("Validation errors:", errors)
    else:
        print("Content validation passed!")
    
    # Resolve template
    template = template_library.get_template('cholot-texticon')
    resolved_widget = resolver.resolve(template, content_data)
    
    print(f"Generated widget ID: {resolved_widget['id']}")
    print(f"Widget title: {resolved_widget['settings']['title']}")
    
    # Test section template
    section_template = template_library.get_template('cholot-services-section')
    resolved_section = resolver.resolve(section_template, content_data)
    
    print(f"Generated section with {len(resolved_section['elements'])} columns")