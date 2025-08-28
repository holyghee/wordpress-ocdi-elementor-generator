#!/usr/bin/env python3
"""
Analyze the actual CONTENT in Cholot demo XML, not just structure
"""

import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path

def clean_html(text):
    """Remove HTML tags and decode entities"""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Basic HTML entity decode
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#8217;', "'")
    text = text.replace('&#8220;', '"')
    text = text.replace('&#8221;', '"')
    return text.strip()

def extract_widget_content(widget_data):
    """Extract actual content from Elementor widget"""
    if not isinstance(widget_data, dict):
        return None
    
    widget_type = widget_data.get('widgetType', '')
    settings = widget_data.get('settings', {})
    
    content = {
        'type': widget_type,
        'content': {}
    }
    
    # Extract content based on widget type
    if widget_type == 'cholot-texticon':
        icon_data = settings.get('icon', {})
        icon_value = icon_data.get('value', '') if isinstance(icon_data, dict) else str(icon_data) if icon_data else ''
        link_data = settings.get('link', {})
        link_url = link_data.get('url', '') if isinstance(link_data, dict) else str(link_data) if link_data else ''
        
        content['content'] = {
            'icon': icon_value,
            'title': settings.get('title', ''),
            'text': clean_html(settings.get('text', '')),
            'link': link_url
        }
    elif widget_type == 'cholot-title':
        content['content'] = {
            'title': settings.get('title', ''),
            'subtitle': settings.get('subtitle', ''),
            'text': clean_html(settings.get('text', ''))
        }
    elif widget_type == 'rdn-slider':
        slides = settings.get('slides', [])
        content['content']['slides'] = []
        for slide in slides if isinstance(slides, list) else []:
            if isinstance(slide, dict):
                button_link = slide.get('button_link', {})
                button_url = button_link.get('url', '') if isinstance(button_link, dict) else str(button_link) if button_link else ''
                content['content']['slides'].append({
                    'title': slide.get('title', ''),
                    'text': clean_html(slide.get('text', '')),
                    'button_text': slide.get('button_text', ''),
                    'button_link': button_url
                })
    elif widget_type == 'cholot-team':
        content['content'] = {
            'team_members': settings.get('team_members', [])
        }
    elif widget_type == 'cholot-testimonial-two':
        testimonials = settings.get('testimonials', [])
        content['content']['testimonials'] = testimonials
    elif widget_type == 'text-editor':
        content['content'] = {
            'text': clean_html(settings.get('editor', ''))
        }
    elif widget_type == 'cholot-contact':
        content['content'] = {
            'title': settings.get('title', ''),
            'address': settings.get('address', ''),
            'phone': settings.get('phone', ''),
            'email': settings.get('email', '')
        }
    
    return content if content['content'] else None

def analyze_elementor_content(elementor_data, level=0):
    """Recursively extract content from Elementor structure"""
    if not isinstance(elementor_data, list):
        return []
    
    contents = []
    for element in elementor_data:
        if not isinstance(element, dict):
            continue
            
        el_type = element.get('elType', '')
        
        if el_type == 'widget':
            widget_content = extract_widget_content(element)
            if widget_content and widget_content['content']:
                contents.append(widget_content)
        
        # Recurse into elements
        if 'elements' in element:
            contents.extend(analyze_elementor_content(element['elements'], level + 1))
    
    return contents

def main():
    xml_path = '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml'
    
    # Parse XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Namespaces
    namespaces = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
    }
    
    extracted_content = {
        'pages': {},
        'service_cards': [],
        'hero_sliders': [],
        'team_members': [],
        'testimonials': [],
        'contact_info': []
    }
    
    print("=" * 80)
    print("ANALYZING CHOLOT DEMO CONTENT")
    print("=" * 80)
    
    # Find all items
    for item in root.findall('.//item'):
        title_elem = item.find('title')
        if title_elem is None:
            continue
            
        title = title_elem.text or ''
        
        # Get post type
        post_type = None
        for meta in item.findall('.//wp:postmeta', namespaces):
            key_elem = meta.find('wp:meta_key', namespaces)
            if key_elem is not None and key_elem.text == '_wp_page_template':
                post_type = 'page'
                break
        
        # Get Elementor data
        elementor_data = None
        for meta in item.findall('.//wp:postmeta', namespaces):
            key_elem = meta.find('wp:meta_key', namespaces)
            if key_elem is not None and key_elem.text == '_elementor_data':
                value_elem = meta.find('wp:meta_value', namespaces)
                if value_elem is not None and value_elem.text:
                    try:
                        elementor_data = json.loads(value_elem.text)
                    except:
                        pass
        
        if elementor_data:
            contents = analyze_elementor_content(elementor_data)
            
            if contents:
                print(f"\n{'='*60}")
                print(f"PAGE: {title}")
                print('='*60)
                
                for content in contents:
                    widget_type = content['type']
                    widget_content = content['content']
                    
                    if widget_type == 'cholot-texticon' and widget_content.get('title'):
                        print(f"\n📦 SERVICE CARD:")
                        print(f"  Icon: {widget_content.get('icon', '')}")
                        print(f"  Title: {widget_content.get('title', '')}")
                        print(f"  Text: {widget_content.get('text', '')[:100]}...")
                        extracted_content['service_cards'].append(widget_content)
                    
                    elif widget_type == 'rdn-slider' and widget_content.get('slides'):
                        print(f"\n🎬 HERO SLIDER:")
                        for slide in widget_content['slides']:
                            print(f"  Slide:")
                            print(f"    Title: {slide.get('title', '')}")
                            print(f"    Text: {slide.get('text', '')[:100]}...")
                            print(f"    Button: {slide.get('button_text', '')}")
                        extracted_content['hero_sliders'].append(widget_content)
                    
                    elif widget_type == 'cholot-team' and widget_content.get('team_members'):
                        print(f"\n👥 TEAM MEMBERS:")
                        for member in widget_content['team_members']:
                            if isinstance(member, dict):
                                print(f"  - {member.get('name', 'Unknown')}: {member.get('position', '')}")
                        extracted_content['team_members'].extend(widget_content['team_members'])
                    
                    elif widget_type == 'cholot-testimonial-two' and widget_content.get('testimonials'):
                        print(f"\n💬 TESTIMONIALS:")
                        for testimonial in widget_content['testimonials']:
                            if isinstance(testimonial, dict):
                                print(f"  - {testimonial.get('name', 'Unknown')}: {testimonial.get('text', '')[:50]}...")
                        extracted_content['testimonials'].extend(widget_content['testimonials'])
                    
                    elif widget_type == 'cholot-contact':
                        print(f"\n📞 CONTACT INFO:")
                        print(f"  Address: {widget_content.get('address', '')}")
                        print(f"  Phone: {widget_content.get('phone', '')}")
                        print(f"  Email: {widget_content.get('email', '')}")
                        extracted_content['contact_info'].append(widget_content)
    
    # Save extracted content
    with open('cholot_extracted_content.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_content, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("CONTENT SUMMARY:")
    print("="*80)
    print(f"Service Cards found: {len(extracted_content['service_cards'])}")
    print(f"Hero Sliders found: {len(extracted_content['hero_sliders'])}")
    print(f"Team Members found: {len(extracted_content['team_members'])}")
    print(f"Testimonials found: {len(extracted_content['testimonials'])}")
    print(f"Contact Info found: {len(extracted_content['contact_info'])}")
    
    if len(extracted_content['service_cards']) == 0:
        print("\n⚠️ WARNING: No service cards with content found!")
        print("The demo might be using a different structure or widget type.")

if __name__ == "__main__":
    main()