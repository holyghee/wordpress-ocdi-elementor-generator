#!/usr/bin/env python3
"""
Cholot Structure Extractor - Key Information for Replication
Extracts critical structural data for exact Cholot replication
"""

import json

def extract_key_structure(analysis_file):
    """Extract key structural information for replication"""
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Extract key information for replication
    key_structure = {
        'meta': {
            'total_items': analysis['meta_info']['total_items'],
            'verification_count': 65  # Expected count for validation
        },
        
        'pages': {
            'count': len(analysis['pages']),
            'items': []
        },
        
        'posts': {
            'count': len(analysis['posts']), 
            'items': []
        },
        
        'media': {
            'count': len(analysis['media_attachments']),
            'items': []
        },
        
        'menu_items': {
            'count': len(analysis['menu_items']),
            'items': []
        },
        
        'elementor_templates': {
            'count': 0,
            'items': []
        },
        
        'cholot_widgets': {
            'count': len(analysis['cholot_widgets']),
            'widget_types': set(),
            'items': []
        },
        
        'custom_post_types': {
            'headers': [],
            'footers': [],
            'other': []
        }
    }
    
    # Extract page details
    for post_id, page_data in analysis['pages'].items():
        page_info = {
            'id': post_id,
            'title': page_data['title'],
            'slug': page_data['post_name'],
            'parent': page_data['post_parent'],
            'menu_order': page_data['menu_order'],
            'has_elementor': '_elementor_data' in page_data.get('postmeta', {}),
            'cholot_meta': {k: v for k, v in page_data.get('postmeta', {}).items() 
                           if 'cholot' in k.lower()}
        }
        key_structure['pages']['items'].append(page_info)
    
    # Extract post details
    for post_id, post_data in analysis['posts'].items():
        post_info = {
            'id': post_id,
            'title': post_data['title'],
            'slug': post_data['post_name'],
            'date': post_data['post_date'],
            'has_elementor': '_elementor_data' in post_data.get('postmeta', {}),
            'categories': [cat['term'] for cat in post_data.get('categories', [])],
            'tags': [tag['term'] for tag in post_data.get('tags', [])]
        }
        key_structure['posts']['items'].append(post_info)
    
    # Extract media details
    for post_id, media_data in analysis['media_attachments'].items():
        media_info = {
            'id': post_id,
            'title': media_data['title'],
            'filename': media_data['post_name'],
            'attachment_url': media_data.get('postmeta', {}).get('_wp_attachment_metadata', ''),
            'alt_text': media_data.get('postmeta', {}).get('_wp_attachment_image_alt', '')
        }
        key_structure['media']['items'].append(media_info)
    
    # Extract menu items
    for post_id, menu_data in analysis['menu_items'].items():
        menu_info = {
            'id': post_id,
            'title': menu_data['title'],
            'menu_order': menu_data['menu_order'],
            'parent': menu_data['post_parent'],
            'url': menu_data.get('postmeta', {}).get('_menu_item_url', ''),
            'object_id': menu_data.get('postmeta', {}).get('_menu_item_object_id', ''),
            'type': menu_data.get('postmeta', {}).get('_menu_item_type', '')
        }
        key_structure['menu_items']['items'].append(menu_info)
    
    # Extract Elementor templates from custom post types
    for post_id, cpt_data in analysis['custom_post_types'].items():
        if cpt_data['post_type'] == 'elementor_library':
            template_info = {
                'id': post_id,
                'title': cpt_data['title'],
                'type': cpt_data.get('postmeta', {}).get('_elementor_template_type', ''),
                'has_data': '_elementor_data' in cpt_data.get('postmeta', {})
            }
            key_structure['elementor_templates']['items'].append(template_info)
            key_structure['elementor_templates']['count'] += 1
        elif cpt_data['post_type'] == 'header':
            key_structure['custom_post_types']['headers'].append({
                'id': post_id,
                'title': cpt_data['title']
            })
        elif cpt_data['post_type'] == 'footer':
            key_structure['custom_post_types']['footers'].append({
                'id': post_id,
                'title': cpt_data['title']
            })
        else:
            key_structure['custom_post_types']['other'].append({
                'id': post_id,
                'title': cpt_data['title'],
                'type': cpt_data['post_type']
            })
    
    # Extract Cholot widget information
    for post_id, widget_data in analysis['cholot_widgets'].items():
        cholot_info = {
            'id': post_id,
            'title': widget_data['title'],
            'widget_data': widget_data['cholot_data']
        }
        key_structure['cholot_widgets']['items'].append(cholot_info)
        key_structure['cholot_widgets']['widget_types'].update(widget_data['cholot_data'].keys())
    
    # Convert set to list for JSON serialization
    key_structure['cholot_widgets']['widget_types'] = list(key_structure['cholot_widgets']['widget_types'])
    
    return key_structure

def print_replication_summary(structure):
    """Print summary for replication team"""
    
    print("\n" + "="*60)
    print("CHOLOT EXACT REPLICATION STRUCTURE")
    print("="*60)
    
    print(f"\nTOTAL ITEMS: {structure['meta']['total_items']} (Expected: {structure['meta']['verification_count']})")
    
    if structure['meta']['total_items'] == structure['meta']['verification_count']:
        print("✓ Item count matches expected value")
    else:
        print("⚠ Item count discrepancy - verify XML")
    
    print(f"\n📄 PAGES ({structure['pages']['count']} items):")
    for page in sorted(structure['pages']['items'], key=lambda x: int(x['id'])):
        elementor = "📱" if page['has_elementor'] else "  "
        cholot = "🎨" if page['cholot_meta'] else "  "
        print(f"  ID {page['id']}: {elementor}{cholot} {page['title']} (/{page['slug']})")
    
    print(f"\n📝 POSTS ({structure['posts']['count']} items):")
    for post in sorted(structure['posts']['items'], key=lambda x: int(x['id'])):
        elementor = "📱" if post['has_elementor'] else "  "
        print(f"  ID {post['id']}: {elementor} {post['title']} (/{post['slug']})")
    
    print(f"\n🖼️ MEDIA ATTACHMENTS ({structure['media']['count']} items):")
    for i, media in enumerate(sorted(structure['media']['items'], key=lambda x: int(x['id']))[:5]):
        print(f"  ID {media['id']}: {media['title']} ({media['filename']})")
    if structure['media']['count'] > 5:
        print(f"  ... and {structure['media']['count'] - 5} more media files")
    
    print(f"\n🔗 MENU ITEMS ({structure['menu_items']['count']} items):")
    for menu in sorted(structure['menu_items']['items'], key=lambda x: int(x['menu_order'])):
        print(f"  Order {menu['menu_order']}: {menu['title']} (ID: {menu['id']})")
    
    print(f"\n📋 ELEMENTOR TEMPLATES ({structure['elementor_templates']['count']} items):")
    for template in structure['elementor_templates']['items']:
        print(f"  ID {template['id']}: {template['title']} ({template['type']})")
    
    print(f"\n🎨 CHOLOT WIDGETS ({structure['cholot_widgets']['count']} items with custom data):")
    print("  Widget Types Found:")
    for widget_type in sorted(structure['cholot_widgets']['widget_types']):
        print(f"    - {widget_type}")
    
    print(f"\n🏗️ CUSTOM POST TYPES:")
    print(f"  Headers: {len(structure['custom_post_types']['headers'])}")
    for header in structure['custom_post_types']['headers']:
        print(f"    ID {header['id']}: {header['title']}")
    
    print(f"  Footers: {len(structure['custom_post_types']['footers'])}")
    for footer in structure['custom_post_types']['footers']:
        print(f"    ID {footer['id']}: {footer['title']}")
    
    if structure['custom_post_types']['other']:
        print(f"  Other: {len(structure['custom_post_types']['other'])}")
        for other in structure['custom_post_types']['other']:
            print(f"    ID {other['id']}: {other['title']} ({other['type']})")

if __name__ == "__main__":
    analysis_file = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot_target_structure.json"
    output_file = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot_replication_structure.json"
    
    print("Extracting key structure for Cholot replication...")
    
    structure = extract_key_structure(analysis_file)
    
    # Save key structure
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    print_replication_summary(structure)
    
    print(f"\n✓ Replication structure saved to: {output_file}")