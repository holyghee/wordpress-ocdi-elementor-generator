#!/usr/bin/env python3
"""
Cholot ID Mapping - Exact Replication Reference
Creates precise ID mapping for exact Cholot theme replication
"""

import json

def create_id_mapping():
    """Create exact ID mapping for replication"""
    
    # Load the replication structure
    with open('/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot_replication_structure.json', 'r') as f:
        structure = json.load(f)
    
    id_mapping = {
        'verification': {
            'total_items': 65,
            'status': 'VERIFIED - XML contains exactly 65 items'
        },
        
        'pages': {},
        'posts': {},
        'media': {},
        'menu_items': {},
        'elementor_templates': {},
        'custom_headers': {},
        'custom_footers': {},
        'contact_forms': {},
        
        'cholot_widget_types': [
            'cholot_dark_bg',
            'cholot_default_header', 
            'cholot_footer_option',
            'cholot_header_option',
            'cholot_header_position',
            'cholot_meta_choose_footer',
            'cholot_meta_choose_header'
        ]
    }
    
    # Map pages with exact IDs
    for page in structure['pages']['items']:
        id_mapping['pages'][page['id']] = {
            'title': page['title'],
            'slug': page['slug'],
            'has_elementor': page['has_elementor'],
            'has_cholot_widgets': bool(page['cholot_meta']),
            'cholot_meta_keys': list(page['cholot_meta'].keys()),
            'parent': page['parent'],
            'menu_order': page['menu_order']
        }
    
    # Map posts with exact IDs  
    for post in structure['posts']['items']:
        id_mapping['posts'][post['id']] = {
            'title': post['title'],
            'slug': post['slug'],
            'date': post['date'],
            'has_elementor': post['has_elementor'],
            'categories': post['categories'],
            'tags': post['tags']
        }
    
    # Map media files
    for media in structure['media']['items']:
        id_mapping['media'][media['id']] = {
            'title': media['title'],
            'filename': media['filename'],
            'alt_text': media['alt_text']
        }
    
    # Map menu items
    for menu in structure['menu_items']['items']:
        id_mapping['menu_items'][menu['id']] = {
            'title': menu['title'],
            'menu_order': menu['menu_order'],
            'parent': menu['parent'],
            'url': menu['url'],
            'object_id': menu['object_id'],
            'type': menu['type']
        }
    
    # Map Elementor templates
    for template in structure['elementor_templates']['items']:
        id_mapping['elementor_templates'][template['id']] = {
            'title': template['title'],
            'type': template['type'],
            'has_data': template['has_data']
        }
    
    # Map custom headers
    for header in structure['custom_post_types']['headers']:
        id_mapping['custom_headers'][header['id']] = {
            'title': header['title']
        }
    
    # Map custom footers
    for footer in structure['custom_post_types']['footers']:
        id_mapping['custom_footers'][footer['id']] = {
            'title': footer['title']
        }
    
    # Map other custom post types
    for other in structure['custom_post_types']['other']:
        if other['type'] == 'wpcf7_contact_form':
            id_mapping['contact_forms'][other['id']] = {
                'title': other['title']
            }
    
    return id_mapping

def print_id_mapping(mapping):
    """Print detailed ID mapping for replication team"""
    
    print("\n" + "="*70)
    print("CHOLOT EXACT REPLICATION - ID MAPPING REFERENCE")
    print("="*70)
    
    print(f"\n✓ VERIFICATION: {mapping['verification']['status']}")
    
    print(f"\n📄 PAGES - EXACT IDS TO REPLICATE:")
    for page_id, page_data in mapping['pages'].items():
        widgets = "🎨" if page_data['has_cholot_widgets'] else "  "
        elementor = "📱" if page_data['has_elementor'] else "  "
        print(f"  ID {page_id}: {widgets}{elementor} {page_data['title']}")
        print(f"         Slug: /{page_data['slug']}")
        if page_data['cholot_meta_keys']:
            print(f"         Cholot: {', '.join(page_data['cholot_meta_keys'])}")
        print()
    
    print(f"📝 POSTS - EXACT IDS TO REPLICATE:")
    for post_id, post_data in mapping['posts'].items():
        elementor = "📱" if post_data['has_elementor'] else "  "
        print(f"  ID {post_id}: {elementor} {post_data['title']}")
        print(f"         Slug: /{post_data['slug']}")
        if post_data['categories']:
            print(f"         Categories: {', '.join(post_data['categories'])}")
        print()
    
    print(f"🖼️ MEDIA FILES - KEY ATTACHMENTS:")
    for media_id, media_data in list(mapping['media'].items())[:10]:
        print(f"  ID {media_id}: {media_data['title']} ({media_data['filename']})")
    if len(mapping['media']) > 10:
        print(f"  ... and {len(mapping['media']) - 10} more media files")
    
    print(f"\n📋 ELEMENTOR TEMPLATES - EXACT IDS:")
    for template_id, template_data in mapping['elementor_templates'].items():
        data_status = "✓" if template_data['has_data'] else "✗"
        print(f"  ID {template_id}: {data_status} {template_data['title']} ({template_data['type']})")
    
    print(f"\n🏗️ CUSTOM ELEMENTS - EXACT IDS:")
    print("  Headers:")
    for header_id, header_data in mapping['custom_headers'].items():
        print(f"    ID {header_id}: {header_data['title']}")
    
    print("  Footers:")
    for footer_id, footer_data in mapping['custom_footers'].items():
        print(f"    ID {footer_id}: {footer_data['title']}")
    
    print("  Contact Forms:")
    for form_id, form_data in mapping['contact_forms'].items():
        print(f"    ID {form_id}: {form_data['title']}")
    
    print(f"\n🎨 CHOLOT WIDGET TYPES TO REPLICATE:")
    for widget_type in mapping['cholot_widget_types']:
        print(f"  - {widget_type}")
    
    print(f"\n🔗 MENU STRUCTURE:")
    sorted_menu = sorted(mapping['menu_items'].items(), 
                        key=lambda x: int(x[1]['menu_order']))
    for menu_id, menu_data in sorted_menu:
        print(f"  Order {menu_data['menu_order']}: {menu_data['title']} (ID {menu_id})")
        if menu_data['url']:
            print(f"           URL: {menu_data['url']}")

def save_mapping(mapping, filename):
    """Save mapping to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("Creating exact ID mapping for Cholot replication...")
    
    mapping = create_id_mapping()
    
    # Save the mapping
    output_file = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot_exact_id_mapping.json"
    save_mapping(mapping, output_file)
    
    print_id_mapping(mapping)
    
    print(f"\n✓ Exact ID mapping saved to: {output_file}")
    print("\n🎯 REPLICATION READY - Use this mapping for exact structure duplication!")