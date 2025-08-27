#!/usr/bin/env python3
"""
Widget Factory Interfaces Design
===============================

Defines the interfaces and factory pattern for all 13 Cholot widgets
Based on the hybrid architecture analysis and existing CholotComponentFactory
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json


class WidgetType(Enum):
    """Enumeration of all Cholot widget types"""
    TEXTICON = "cholot-texticon"
    TITLE = "cholot-title" 
    POST_THREE = "cholot-post-three"
    POST_FOUR = "cholot-post-four"
    GALLERY = "cholot-gallery"
    LOGO = "cholot-logo"
    MENU = "cholot-menu"
    BUTTON_TEXT = "cholot-button-text"
    TEAM = "cholot-team"
    TESTIMONIAL = "cholot-testimonial-two"
    TEXT_LINE = "cholot-text-line"
    CONTACT = "cholot-contact"
    SIDEBAR = "cholot-sidebar"
    SLIDER = "rdn-slider"  # Hero slider


@dataclass
class WidgetContentRequirements:
    """Defines content requirements for each widget type"""
    required_fields: List[str]
    optional_fields: List[str]
    content_types: Dict[str, type]
    default_values: Dict[str, Any]


@dataclass
class LayoutConfig:
    """Configuration for adaptive layouts"""
    structure: str  # "100", "50", "33", "25", "20"
    columns: int
    rows: int = 1
    responsive_tablet: Optional[str] = None
    responsive_mobile: str = "100"
    name: str = "auto"


class IWidgetGenerator(ABC):
    """Interface for widget generators"""
    
    @abstractmethod
    def get_widget_type(self) -> WidgetType:
        """Return the widget type this generator handles"""
        pass
    
    @abstractmethod
    def get_content_requirements(self) -> WidgetContentRequirements:
        """Return content requirements for this widget"""
        pass
    
    @abstractmethod
    def generate_widget(self, content_data: Dict[str, Any], widget_id: str = None) -> Dict[str, Any]:
        """Generate widget JSON from content data"""
        pass
    
    @abstractmethod
    def validate_content(self, content_data: Dict[str, Any]) -> List[str]:
        """Validate content data, return list of errors"""
        pass
    
    @abstractmethod
    def get_template(self) -> Dict[str, Any]:
        """Return base template with placeholders"""
        pass


class BaseWidgetGenerator(IWidgetGenerator):
    """Base implementation with common functionality"""
    
    def __init__(self, theme_config, id_generator):
        self.theme_config = theme_config
        self.id_generator = id_generator
    
    def generate_widget_id(self) -> str:
        """Generate unique widget ID"""
        return self.id_generator.generate_id()
    
    def validate_content(self, content_data: Dict[str, Any]) -> List[str]:
        """Default content validation"""
        errors = []
        requirements = self.get_content_requirements()
        
        for field in requirements.required_fields:
            if field not in content_data or not content_data[field]:
                errors.append(f"Required field '{field}' is missing or empty")
        
        return errors
    
    def apply_theme_defaults(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Apply theme-specific defaults"""
        # Apply Cholot theme colors and spacing
        if 'subtitle_color' not in settings:
            settings['subtitle_color'] = self.theme_config.PRIMARY_COLOR
        
        # Apply default spacing objects where needed
        spacing_fields = ['title_margin', 'sb_margin', 'sb_padding', 'text_margin', 'icon_margin']
        for field in spacing_fields:
            if field not in settings:
                settings[field] = self.theme_config.SPACING_OBJECT.copy()
        
        return settings


# Widget Generator Implementations

class TextIconWidgetGenerator(BaseWidgetGenerator):
    """Generator for cholot-texticon widgets"""
    
    def get_widget_type(self) -> WidgetType:
        return WidgetType.TEXTICON
    
    def get_content_requirements(self) -> WidgetContentRequirements:
        return WidgetContentRequirements(
            required_fields=['title'],
            optional_fields=['subtitle', 'text', 'icon', 'icon_align'],
            content_types={
                'title': str,
                'subtitle': str,
                'text': str,
                'icon': str,
                'icon_align': str
            },
            default_values={
                'icon': 'fas fa-crown',
                'icon_align': 'top'
            }
        )
    
    def get_template(self) -> Dict[str, Any]:
        """Return texticon template with placeholders"""
        return {
            "id": "{{widget_id}}",
            "elType": "widget", 
            "settings": {
                "title": "{{title}}",
                "{{IF:subtitle}}subtitle": "{{subtitle}}",{{/IF}}
                "{{IF:text}}text": "<p>{{text}}</p>",{{/IF}}
                "selected_icon": {
                    "value": "{{icon|fas fa-crown}}",
                    "library": "fa-solid"
                },
                "__fa4_migrated": {"selected_icon": True},
                
                # Fixed design parameters
                "title_typography_typography": "custom",
                "title_typography_font_size": {"unit": "px", "size": 24, "sizes": []},
                "title_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
                "title_color": "{{title_color|#ffffff}}",
                "subtitle_typography_typography": "custom", 
                "subtitle_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
                "subtitle_typography_font_weight": "700",
                "subtitle_typography_text_transform": "uppercase",
                "subtitle_typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
                "subtitle_color": "{{subtitle_color|#b68c2f}}",
                "icon_size": {"unit": "px", "size": 15, "sizes": []},
                "icon_bg_size": {"unit": "px", "size": 35, "sizes": []},
                
                # Margins and spacing (will be resolved to proper objects)
                "title_margin": "{{title_margin|SPACING_OBJECT}}",
                "sb_margin": "{{sb_margin|SPACING_OBJECT}}",
                "sb_padding": "{{sb_padding|SPACING_OBJECT}}",
                "text_margin": "{{text_margin|SPACING_OBJECT}}",
                "icon_margin": "{{icon_margin|SPACING_OBJECT}}"
            },
            "elements": [],
            "widgetType": "cholot-texticon"
        }
    
    def generate_widget(self, content_data: Dict[str, Any], widget_id: str = None) -> Dict[str, Any]:
        """Generate texticon widget from content data"""
        if not widget_id:
            widget_id = self.generate_widget_id()
        
        # Start with template
        template = self.get_template()
        
        # Apply content data
        settings = template["settings"].copy()
        
        # Required fields
        settings["title"] = content_data["title"]
        
        # Optional fields
        if "subtitle" in content_data:
            settings["subtitle"] = content_data["subtitle"]
        
        if "text" in content_data:
            settings["text"] = f"<p>{content_data['text']}</p>"
            # Add text typography settings
            settings.update({
                "text_typography_typography": "custom",
                "text_typography_font_size": {"unit": "px", "size": 13, "sizes": []},
                "text_typography_font_weight": "normal",
                "text_typography_text_transform": "uppercase",
                "text_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
                "text_color": self.theme_config.PRIMARY_COLOR
            })
        
        if "icon" in content_data:
            settings["selected_icon"]["value"] = content_data["icon"]
        
        # Apply theme defaults
        settings = self.apply_theme_defaults(settings)
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-texticon"
        }


class TitleWidgetGenerator(BaseWidgetGenerator):
    """Generator for cholot-title widgets"""
    
    def get_widget_type(self) -> WidgetType:
        return WidgetType.TITLE
    
    def get_content_requirements(self) -> WidgetContentRequirements:
        return WidgetContentRequirements(
            required_fields=['title'],
            optional_fields=['header_size', 'align', 'responsive'],
            content_types={
                'title': str,
                'header_size': str,
                'align': str,
                'responsive': dict
            },
            default_values={
                'header_size': 'h2',
                'align': 'left'
            }
        )
    
    def get_template(self) -> Dict[str, Any]:
        return {
            "id": "{{widget_id}}",
            "elType": "widget",
            "settings": {
                "title": "{{title}}",
                "header_size": "{{header_size|h2}}",
                "{{IF:align}}align": "{{align}}",{{/IF}}
                "desc_typography_typography": "custom",
                "desc_typography_font_size": {"unit": "px", "size": 20, "sizes": []},
                "title_margin": "{{title_margin|SPACING_OBJECT}}",
                "_margin": "{{_margin|SPACING_OBJECT}}"
            },
            "elements": [],
            "widgetType": "cholot-title"
        }
    
    def generate_widget(self, content_data: Dict[str, Any], widget_id: str = None) -> Dict[str, Any]:
        if not widget_id:
            widget_id = self.generate_widget_id()
        
        settings = {
            "title": content_data["title"],
            "header_size": content_data.get("header_size", "h2"),
            "desc_typography_typography": "custom",
            "desc_typography_font_size": {"unit": "px", "size": 20, "sizes": []},
            "title_margin": self.theme_config.SPACING_OBJECT.copy(),
            "_margin": self.theme_config.SPACING_OBJECT.copy()
        }
        
        # Add alignment if specified
        if 'align' in content_data:
            settings['align'] = content_data['align']
            
            # Add responsive alignment
            if 'responsive' in content_data:
                responsive = content_data['responsive']
                if 'tablet' in responsive:
                    settings['align_tablet'] = responsive['tablet']
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-title"
        }


class TeamWidgetGenerator(BaseWidgetGenerator):
    """Generator for cholot-team widgets"""
    
    def get_widget_type(self) -> WidgetType:
        return WidgetType.TEAM
    
    def get_content_requirements(self) -> WidgetContentRequirements:
        return WidgetContentRequirements(
            required_fields=['name', 'position', 'image_url'],
            optional_fields=['social_links', 'height', 'align', 'animation'],
            content_types={
                'name': str,
                'position': str,
                'image_url': str,
                'social_links': list,
                'height': str,
                'align': str,
                'animation': str
            },
            default_values={
                'height': '420px',
                'align': 'left',
                'animation': 'shrink'
            }
        )
    
    def get_template(self) -> Dict[str, Any]:
        return {
            "id": "{{widget_id}}",
            "elType": "widget",
            "settings": {
                "title": "{{name}}",
                "text": "{{position}}",
                "image": {
                    "url": "{{image_url}}",
                    "id": "{{image_id|359}}"
                },
                "team_height": "{{height|420px}}",
                "content_align": "{{align|left}}",
                "hover_animation": "{{animation|shrink}}",
                
                # Colors
                "title_cl": "#000000",
                "txt_cl": "#b68c2f",
                "bg_content": "#1f1f1f",
                "mask_color": "#000000",
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
                "titlep_margin": "{{titlep_margin|SPACING_OBJECT}}",
                "titlep_padding": "{{titlep_padding|SPACING_OBJECT}}",
                "tx_margin": "{{tx_margin|SPACING_OBJECT}}",
                "tx_padding": "{{tx_padding|SPACING_OBJECT}}",
                "port_padding": "{{port_padding|SPACING_OBJECT}}",
                "_margin": "{{_margin|SPACING_OBJECT}}",
                
                # Social links (handled specially)
                "{{IF:social_links}}social_icon_list": [
                    "{{LOOP:social_links}}{\"_id\": \"{{_id}}\", \"social_icon\": \"{{icon}}\", \"social_link\": \"{{url}}\"}{{/LOOP}}"
                ]{{/IF}}
            },
            "elements": [],
            "widgetType": "cholot-team"
        }
    
    def generate_widget(self, content_data: Dict[str, Any], widget_id: str = None) -> Dict[str, Any]:
        if not widget_id:
            widget_id = self.generate_widget_id()
        
        settings = {
            "title": content_data["name"],
            "text": content_data["position"],
            "image": {
                "url": content_data["image_url"],
                "id": content_data.get("image_id", 359)
            },
            "team_height": content_data.get("height", "420px"),
            "content_align": content_data.get("align", "left"),
            "hover_animation": content_data.get("animation", "shrink"),
            
            # Fixed colors
            "title_cl": self.theme_config.BLACK,
            "txt_cl": self.theme_config.PRIMARY_COLOR,
            "bg_content": "#1f1f1f",
            "mask_color": self.theme_config.BLACK,
            "mask_color_opacity": {"unit": "px", "size": 0.8, "sizes": []},
            
            # Fixed typography
            "cport_typography_typography": "custom",
            "cport_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "cport_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
            "cport_typography_text_transform": "capitalize",
            "ctext_typography_typography": "custom",
            "ctext_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
            "ctext_typography_font_weight": "normal",
            "ctext_typography_line_height": {"unit": "em", "size": 1, "sizes": []},
        }
        
        # Apply theme defaults for spacing
        settings = self.apply_theme_defaults(settings)
        
        # Add social icons if provided
        if 'social_links' in content_data:
            social_list = []
            for social in content_data['social_links']:
                social_item = {
                    "_id": self.id_generator.generate_id(),
                    "social_icon": social['icon'],
                    "social_link": social['url']
                }
                social_list.append(social_item)
            settings['social_icon_list'] = social_list
        
        return {
            "id": widget_id,
            "elType": "widget",
            "settings": settings,
            "elements": [],
            "widgetType": "cholot-team"
        }


# Factory Registry Pattern

class WidgetGeneratorFactory:
    """Factory for creating widget generators"""
    
    def __init__(self, theme_config, id_generator):
        self.theme_config = theme_config
        self.id_generator = id_generator
        self._generators = {}
        self._register_default_generators()
    
    def _register_default_generators(self):
        """Register all default widget generators"""
        generators = [
            TextIconWidgetGenerator(self.theme_config, self.id_generator),
            TitleWidgetGenerator(self.theme_config, self.id_generator),
            TeamWidgetGenerator(self.theme_config, self.id_generator),
            # TODO: Add remaining 10 widget generators
        ]
        
        for generator in generators:
            self.register_generator(generator)
    
    def register_generator(self, generator: IWidgetGenerator):
        """Register a widget generator"""
        widget_type = generator.get_widget_type()
        self._generators[widget_type.value] = generator
    
    def get_generator(self, widget_type: str) -> IWidgetGenerator:
        """Get generator for widget type"""
        if widget_type not in self._generators:
            raise ValueError(f"No generator registered for widget type: {widget_type}")
        return self._generators[widget_type]
    
    def get_supported_widgets(self) -> List[str]:
        """Get list of supported widget types"""
        return list(self._generators.keys())
    
    def generate_widget(self, widget_type: str, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate widget using appropriate generator"""
        generator = self.get_generator(widget_type)
        
        # Validate content first
        errors = generator.validate_content(content_data)
        if errors:
            raise ValueError(f"Content validation failed: {', '.join(errors)}")
        
        return generator.generate_widget(content_data)


# Section Generator Interface

class ISectionGenerator(ABC):
    """Interface for section generators"""
    
    @abstractmethod
    def generate_section(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate section from configuration"""
        pass
    
    @abstractmethod
    def calculate_layout(self, items: List, layout_hint: str = None) -> LayoutConfig:
        """Calculate optimal layout for items"""
        pass


class AdaptiveSectionGenerator(ISectionGenerator):
    """Generator for adaptive sections with automatic layout"""
    
    def __init__(self, widget_factory: WidgetGeneratorFactory, theme_config, id_generator):
        self.widget_factory = widget_factory
        self.theme_config = theme_config
        self.id_generator = id_generator
    
    def calculate_layout(self, items: List, layout_hint: str = None) -> LayoutConfig:
        """Calculate optimal layout for items"""
        count = len(items)
        
        # Layout patterns from existing analysis
        if count == 1:
            return LayoutConfig("100", 1, name="single")
        elif count == 2:
            return LayoutConfig("50", 2, name="two-column")
        elif count == 3:
            return LayoutConfig("33", 3, name="three-column")
        elif count == 4:
            return LayoutConfig("25", 4, name="four-column")
        elif count <= 6:
            return LayoutConfig("33", 3, rows=2, name="three-by-two-grid")
        elif count <= 8:
            return LayoutConfig("25", 4, rows=2, name="four-by-two-grid")
        else:
            return LayoutConfig("33", 3, rows=(count + 2) // 3, name="three-column-multi-row")
    
    def generate_section(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate adaptive section"""
        section_type = config.get('type', 'services')
        content = config.get('content', {})
        layout_hint = config.get('layout', 'auto')
        
        if section_type == 'services':
            return self._generate_services_section(content, layout_hint)
        elif section_type == 'team':
            return self._generate_team_section(content, layout_hint)
        else:
            raise ValueError(f"Unsupported section type: {section_type}")
    
    def _generate_services_section(self, content: Dict, layout_hint: str) -> Dict[str, Any]:
        """Generate services section with adaptive layout"""
        services = content.get('services', [])
        
        if not services:
            raise ValueError("Services section requires 'services' content")
        
        # Calculate layout
        layout = self.calculate_layout(services, layout_hint)
        
        # Create section
        section = {
            "id": self.id_generator.generate_id(),
            "elType": "section",
            "settings": {
                "structure": layout.structure,
                "gap": "extended",
                "padding": {"unit": "px", "top": 60, "right": 0, "bottom": 60, "left": 0}
            },
            "elements": []
        }
        
        # Add background if specified
        if 'background' in content:
            section['settings'].update(content['background'])
        
        # Generate columns with widgets
        column_width = 100 / layout.columns
        columns = []
        
        for i, service in enumerate(services):
            # Generate service widget
            widget = self.widget_factory.generate_widget('cholot-texticon', service)
            
            # Create column
            column = {
                "id": self.id_generator.generate_id(),
                "elType": "column",
                "settings": {
                    "_column_size": column_width,
                    "_inline_size": None
                },
                "elements": [widget],
                "isInner": False
            }
            
            columns.append(column)
        
        section['elements'] = columns
        return section


# Usage Example Interface

class CholotWidgetSystem:
    """Main interface for the widget generation system"""
    
    def __init__(self, theme_config=None, enable_llm=False):
        self.theme_config = theme_config or self._get_default_theme_config()
        self.id_generator = self._get_id_generator()
        self.widget_factory = WidgetGeneratorFactory(self.theme_config, self.id_generator)
        self.section_generator = AdaptiveSectionGenerator(self.widget_factory, self.theme_config, self.id_generator)
    
    def generate_widget(self, widget_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate single widget"""
        return self.widget_factory.generate_widget(widget_type, content)
    
    def generate_section(self, section_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate adaptive section"""
        return self.section_generator.generate_section(section_config)
    
    def get_widget_requirements(self, widget_type: str) -> WidgetContentRequirements:
        """Get content requirements for widget type"""
        generator = self.widget_factory.get_generator(widget_type)
        return generator.get_content_requirements()
    
    def validate_content(self, widget_type: str, content: Dict[str, Any]) -> List[str]:
        """Validate content for widget type"""
        generator = self.widget_factory.get_generator(widget_type)
        return generator.validate_content(content)
    
    def _get_default_theme_config(self):
        """Get default Cholot theme configuration"""
        from generate_wordpress_xml import CholotThemeConfig
        return CholotThemeConfig()
    
    def _get_id_generator(self):
        """Get Elementor ID generator"""
        from generate_wordpress_xml import ElementorIDGenerator
        return ElementorIDGenerator()


if __name__ == "__main__":
    # Example usage
    system = CholotWidgetSystem()
    
    # Generate a texticon widget
    texticon_content = {
        "title": "Professional Service",
        "subtitle": "Quality Assured",
        "text": "We provide top-quality services with professional expertise.",
        "icon": "fas fa-star"
    }
    
    widget = system.generate_widget('cholot-texticon', texticon_content)
    print(f"Generated texticon widget: {widget['id']}")
    
    # Generate a services section
    services_config = {
        "type": "services",
        "layout": "auto",
        "content": {
            "services": [
                {"title": "Service 1", "text": "Description 1", "icon": "fas fa-check"},
                {"title": "Service 2", "text": "Description 2", "icon": "fas fa-star"},
                {"title": "Service 3", "text": "Description 3", "icon": "fas fa-heart"}
            ]
        }
    }
    
    section = system.generate_section(services_config)
    print(f"Generated services section with {len(section['elements'])} columns")