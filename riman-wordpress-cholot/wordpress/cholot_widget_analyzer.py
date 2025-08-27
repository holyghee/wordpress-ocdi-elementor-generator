#!/usr/bin/env python3

import json
import re
from datetime import datetime

def get_widget_description(widget_type):
    descriptions = {
        'cholot-texticon': 'Text with icon widget - displays title, subtitle, text content with customizable icon and styling',
        'cholot-title': 'Title widget - displays headings with custom styling and span support',
        'cholot-post-three': 'Blog post widget - displays posts in single column layout with customizable meta',
        'cholot-gallery': 'Gallery widget - displays image galleries with grid layout options',
        'cholot-logo': 'Logo widget - displays site logo with alignment and sizing options',
        'cholot-menu': 'Navigation menu widget - displays WordPress menus with mobile responsive options',
        'cholot-button-text': 'Button with text widget - displays buttons with subtitle and icon support',
        'cholot-team': 'Team member widget - displays team member profiles with social icons and background images',
        'cholot-testimonial-two': 'Testimonial widget - displays customer testimonials in slider format',
        'cholot-text-line': 'Text with line widget - displays text content with decorative line elements',
        'cholot-contact': 'Contact form widget - displays contact forms with custom styling',
        'cholot-post-four': 'Blog post widget - displays posts in two-column grid layout',
        'cholot-sidebar': 'Sidebar widget - displays sidebar content with custom width'
    }
    return descriptions.get(widget_type, 'Custom Cholot widget')

def format_example_settings(settings):
    formatted = {}
    for key, value in settings.items():
        if isinstance(value, dict):
            if 'unit' in value and 'size' in value:
                formatted[key] = f"{value.get('size', 0)}{value.get('unit', 'px')}"
            elif 'top' in value or 'left' in value:
                formatted[key] = 'spacing_object'
            else:
                formatted[key] = dict(list(value.items())[:2]) if value else {}
        elif isinstance(value, list):
            formatted[key] = f'array[{len(value)}]'
        else:
            formatted[key] = str(value)[:50] + ('...' if len(str(value)) > 50 else '')
    return formatted

def analyze_patterns(instances, widget_type):
    patterns = {}
    if widget_type == 'cholot-texticon':
        patterns['icon_types'] = list(set(inst.get('settings', {}).get('selected_icon', {}).get('value', 'N/A') for inst in instances))
        patterns['layout_styles'] = list(set(inst.get('settings', {}).get('icon_style', 'default') for inst in instances))
    elif widget_type == 'cholot-team':
        patterns['social_networks'] = ['facebook', 'twitter', 'instagram', 'linkedin']
        patterns['image_positions'] = list(set(inst.get('settings', {}).get('image_position_tablet', 'center center') for inst in instances))
    elif widget_type == 'cholot-gallery':
        patterns['column_options'] = list(set(inst.get('settings', {}).get('port_column', 'col-md-4') for inst in instances))
    return patterns

def main():
    # Read the XML file and extract Elementor data sections
    with open('/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/demo-data-fixed.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all _elementor_data sections
    pattern = r'<wp:meta_key><!\[CDATA\[_elementor_data\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>'
    matches = re.findall(pattern, content, re.DOTALL)

    cholot_widgets = {}

    for match in matches:
        try:
            # Parse the JSON data
            data = json.loads(match)
            
            # Recursively find cholot widgets
            def find_cholot_widgets(elements):
                for element in elements:
                    if element.get('elType') == 'widget':
                        widget_type = element.get('widgetType', '')
                        if widget_type.startswith('cholot-'):
                            if widget_type not in cholot_widgets:
                                cholot_widgets[widget_type] = []
                            cholot_widgets[widget_type].append(element)
                    
                    # Recursively check nested elements
                    if 'elements' in element:
                        find_cholot_widgets(element['elements'])
            
            find_cholot_widgets(data)
        except json.JSONDecodeError:
            continue

    # Generate comprehensive JSON catalog
    catalog = {
        'cholot_theme_analysis': {
            'meta': {
                'analysis_date': datetime.now().strftime('%Y-%m-%d'),
                'total_widget_types': len(cholot_widgets),
                'total_instances': sum(len(instances) for instances in cholot_widgets.values()),
                'elementor_version': '2.6.2',
                'theme_name': 'Cholot WordPress Theme',
                'analysis_scope': 'demo-data-fixed.xml'
            },
            'widgets': {}
        }
    }

    # Analyze each widget type
    for widget_type, instances in cholot_widgets.items():
        widget_name = widget_type.replace('cholot-', '').replace('-', '_')
        
        # Get common settings across all instances
        all_settings = set()
        for instance in instances:
            all_settings.update(instance.get('settings', {}).keys())
        
        # Get example settings from first instance
        example_settings = instances[0].get('settings', {}) if instances else {}
        
        # Categorize settings
        typography_settings = [k for k in all_settings if 'typography' in k or 'font' in k]
        color_settings = [k for k in all_settings if 'color' in k or 'bg' in k]
        spacing_settings = [k for k in all_settings if any(x in k for x in ['margin', 'padding', 'width', 'height', 'size', 'gap'])]
        animation_settings = [k for k in all_settings if any(x in k for x in ['animation', 'hover', 'transition'])]
        
        catalog['cholot_theme_analysis']['widgets'][widget_name] = {
            'widget_type': widget_type,
            'instances_found': len(instances),
            'description': get_widget_description(widget_type),
            'settings_structure': {
                'total_settings': len(all_settings),
                'typography': sorted(typography_settings),
                'colors': sorted(color_settings),
                'spacing': sorted(spacing_settings),
                'animations': sorted(animation_settings),
                'other': sorted(list(all_settings - set(typography_settings + color_settings + spacing_settings + animation_settings)))
            },
            'example_configuration': format_example_settings(example_settings),
            'common_patterns': analyze_patterns(instances, widget_type),
            'required_settings': get_required_settings(widget_type),
            'default_values': get_default_values(instances, widget_type)
        }

    return catalog

def get_required_settings(widget_type):
    """Define required settings for each widget type"""
    required = {
        'cholot-texticon': ['title', 'selected_icon'],
        'cholot-title': ['title'],
        'cholot-post-three': ['blog_post', 'blog_column'],
        'cholot-gallery': ['gallery', 'port_column'],
        'cholot-logo': ['logo_img'],
        'cholot-menu': ['cholot_menu'],
        'cholot-button-text': ['btn_text', 'link'],
        'cholot-team': ['title', 'text', 'image'],
        'cholot-testimonial-two': ['testi_list'],
        'cholot-text-line': ['title'],
        'cholot-contact': ['shortcode'],
        'cholot-post-four': ['blog_post', 'blog_column'],
        'cholot-sidebar': ['width']
    }
    return required.get(widget_type, [])

def get_default_values(instances, widget_type):
    """Extract common default values"""
    defaults = {}
    if instances:
        settings = instances[0].get('settings', {})
        if widget_type == 'cholot-texticon':
            defaults = {
                'icon_size': '15px',
                'title_color': '#ffffff',
                'subtitle_color': '#b68c2f'
            }
        elif widget_type == 'cholot-team':
            defaults = {
                'hover_animation': 'shrink',
                'content_align': 'left'
            }
    return defaults

if __name__ == '__main__':
    catalog = main()
    print(json.dumps(catalog, indent=2))