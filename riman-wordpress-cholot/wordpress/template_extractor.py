#!/usr/bin/env python3
import json
import re
from pathlib import Path
from copy import deepcopy

CONTENT_FIELDS = {
    'cholot-texticon': ['title', 'subtitle', 'text', 'btn_text', 'selected_icon'],
    'cholot-title': ['title', 'editor'],
    'cholot-team': ['title', 'text', 'image', 'social_icon_list'],
    'cholot-testimonial-two': ['testi_list'],
    'cholot-text-line': ['title', 'subtitle'],
    'text-editor': ['editor'],
    'divider': ['text'],
    'image': ['image'],
    'video': ['youtube_url', 'vimeo_url', 'dailymotion_url', 'videopress_url', 'image_overlay'],
    'icon': ['selected_icon'],
    'rdn-slider': ['slider_list'],
    'cholot-contact': ['shortcode']
}

def replace_content_with_placeholders(value, field_name):
    if isinstance(value, str):
        if field_name == 'title':
            return '{{title}}'
        elif field_name == 'subtitle':
            return '{{subtitle}}'
        elif field_name == 'text' or field_name == 'editor':
            return '{{content}}'
        elif field_name == 'btn_text':
            return '{{button_text}}'
        elif field_name == 'shortcode':
            return '{{shortcode}}'
        else:
            return f'{{{{{field_name}}}}}'
    elif isinstance(value, dict):
        if 'url' in value:
            return {'url': '{{image_url}}', 'id': '{{image_id}}'}
        elif 'value' in value:
            return {'value': '{{icon_value}}', 'library': value.get('library', 'fa-solid')}
        return value
    elif isinstance(value, list):
        if field_name == 'slider_list':
            return [create_slider_template(value[0]) if value else {}]
        elif field_name == 'testi_list':
            return [create_testimonial_template(value[0]) if value else {}]
        elif field_name == 'social_icon_list':
            return [create_social_template(value[0]) if value else {}]
        return value
    return value

def create_slider_template(item):
    template = deepcopy(item)
    template['title'] = '{{slide_title}}'
    template['subtitle'] = '{{slide_subtitle}}'
    template['text'] = '{{slide_text}}'
    template['btn_text'] = '{{button_text}}'
    if 'btn_link' in template:
        template['btn_link'] = {'url': '{{button_link}}'}
    if 'image' in template:
        template['image'] = {'url': '{{slide_image_url}}', 'id': '{{slide_image_id}}'}
    return template

def create_testimonial_template(item):
    template = deepcopy(item)
    template['title'] = '{{testimonial_name}}'
    template['position'] = '{{testimonial_position}}'
    template['text'] = '{{testimonial_text}}'
    if 'image' in template:
        template['image'] = {'url': '{{testimonial_image_url}}', 'id': '{{testimonial_image_id}}'}
    return template

def create_social_template(item):
    template = deepcopy(item)
    if 'social_icon' in template:
        template['social_icon'] = {'value': '{{social_icon}}', 'library': 'fa-brands'}
    if 'link' in template:
        template['link'] = {'url': '{{social_link}}'}
    return template

def create_widget_template(widget):
    template = deepcopy(widget)
    widget_type = widget.get('widgetType', 'unknown')
    
    if 'settings' in template:
        content_fields = CONTENT_FIELDS.get(widget_type, [])
        for field in content_fields:
            if field in template['settings']:
                template['settings'][field] = replace_content_with_placeholders(
                    template['settings'][field], field
                )
    
    return template

def extract_templates():
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    with open('widget_library.json', 'r', encoding='utf-8') as f:
        widget_library = json.load(f)
    
    template_summary = {}
    
    for widget_type, widget_data in widget_library.items():
        if widget_data['count'] > 0:
            first_instance = widget_data['instances'][0]
            template = create_widget_template(first_instance)
            
            template_file = templates_dir / f'{widget_type}.template.json'
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            
            template_summary[widget_type] = {
                'template_file': str(template_file),
                'instance_count': widget_data['count']
            }
            
            print(f"Created template: {template_file}")
    
    with open('template_summary.json', 'w', encoding='utf-8') as f:
        json.dump(template_summary, f, indent=2)
    
    print(f"\n✅ Created {len(template_summary)} widget templates")
    return template_summary

if __name__ == '__main__':
    extract_templates()