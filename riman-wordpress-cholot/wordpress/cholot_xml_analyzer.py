#!/usr/bin/env python3
"""
Cholot XML Structure Analyzer
Extracts complete structure from target XML for exact replication
"""

import xml.etree.ElementTree as ET
import json
import re
from collections import defaultdict

def analyze_xml_structure(xml_path):
    """Analyze the Cholot XML file and extract complete structure"""
    
    print(f"Analyzing XML file: {xml_path}")
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        print(f"Root tag: {root.tag}")
        
        # Initialize analysis structure
        analysis = {
            'meta_info': {
                'total_items': 0,
                'xml_namespaces': dict(root.attrib) if root.attrib else {},
                'xml_root_tag': root.tag
            },
            'pages': {},
            'posts': {},
            'media_attachments': {},
            'menu_items': {},
            'custom_post_types': {},
            'elementor_data': {},
            'cholot_widgets': {},
            'taxonomies': {},
            'custom_fields': {},
            'item_types_count': defaultdict(int)
        }
        
        # Find channel element (WordPress export structure)
        channel = root.find('.//channel')
        if channel is None:
            # Try to find items directly
            items = root.findall('.//item')
        else:
            items = channel.findall('item')
        
        analysis['meta_info']['total_items'] = len(items)
        print(f"Found {len(items)} items to analyze")
        
        # Analyze each item
        for i, item in enumerate(items):
            if i % 10 == 0:
                print(f"Processing item {i+1}/{len(items)}")
                
            item_data = analyze_item(item)
            item_type = item_data.get('post_type', 'unknown')
            analysis['item_types_count'][item_type] += 1
            
            # Categorize items
            if item_type == 'page':
                analysis['pages'][item_data['post_id']] = item_data
            elif item_type == 'post':
                analysis['posts'][item_data['post_id']] = item_data
            elif item_type == 'attachment':
                analysis['media_attachments'][item_data['post_id']] = item_data
            elif item_type == 'nav_menu_item':
                analysis['menu_items'][item_data['post_id']] = item_data
            else:
                analysis['custom_post_types'][item_data['post_id']] = item_data
            
            # Extract Elementor data
            if '_elementor_data' in item_data.get('postmeta', {}):
                analysis['elementor_data'][item_data['post_id']] = {
                    'title': item_data.get('title', ''),
                    'elementor_data': item_data['postmeta']['_elementor_data']
                }
            
            # Extract Cholot widgets
            cholot_meta = {k: v for k, v in item_data.get('postmeta', {}).items() 
                          if 'cholot' in k.lower()}
            if cholot_meta:
                analysis['cholot_widgets'][item_data['post_id']] = {
                    'title': item_data.get('title', ''),
                    'cholot_data': cholot_meta
                }
        
        # Extract taxonomy information
        if channel:
            for category in channel.findall('wp:category', {'wp': 'http://wordpress.org/export/1.2/'}):
                cat_data = extract_category_data(category)
                if cat_data:
                    analysis['taxonomies'][cat_data['term_id']] = cat_data
        
        print(f"Analysis complete!")
        print(f"Item type counts: {dict(analysis['item_types_count'])}")
        
        return analysis
        
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return None
    except Exception as e:
        print(f"Error analyzing XML: {e}")
        return None

def analyze_item(item):
    """Analyze a single WordPress item"""
    
    # WordPress export namespace
    wp_ns = {'wp': 'http://wordpress.org/export/1.2/'}
    content_ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
    excerpt_ns = {'excerpt': 'http://wordpress.org/export/1.2/excerpt/'}
    
    item_data = {
        'title': get_text(item.find('title')),
        'link': get_text(item.find('link')),
        'pub_date': get_text(item.find('pubDate')),
        'creator': get_text(item.find('dc:creator', {'dc': 'http://purl.org/dc/elements/1.1/'})),
        'guid': get_text(item.find('guid')),
        'description': get_text(item.find('description')),
        'content': get_text(item.find('content:encoded', content_ns)),
        'excerpt': get_text(item.find('excerpt:encoded', excerpt_ns)),
        
        # WordPress specific fields
        'post_id': get_text(item.find('wp:post_id', wp_ns)),
        'post_date': get_text(item.find('wp:post_date', wp_ns)),
        'post_date_gmt': get_text(item.find('wp:post_date_gmt', wp_ns)),
        'comment_status': get_text(item.find('wp:comment_status', wp_ns)),
        'ping_status': get_text(item.find('wp:ping_status', wp_ns)),
        'post_name': get_text(item.find('wp:post_name', wp_ns)),
        'status': get_text(item.find('wp:status', wp_ns)),
        'post_parent': get_text(item.find('wp:post_parent', wp_ns)),
        'menu_order': get_text(item.find('wp:menu_order', wp_ns)),
        'post_type': get_text(item.find('wp:post_type', wp_ns)),
        'post_password': get_text(item.find('wp:post_password', wp_ns)),
        'is_sticky': get_text(item.find('wp:is_sticky', wp_ns)),
        
        # Categories and tags
        'categories': [],
        'tags': [],
        
        # Post meta
        'postmeta': {},
        
        # Comments
        'comments': []
    }
    
    # Extract categories
    for category in item.findall('category'):
        cat_data = {
            'domain': category.get('domain'),
            'nicename': category.get('nicename'),
            'term': category.text
        }
        if cat_data['domain'] == 'category':
            item_data['categories'].append(cat_data)
        elif cat_data['domain'] == 'post_tag':
            item_data['tags'].append(cat_data)
    
    # Extract post meta
    for postmeta in item.findall('wp:postmeta', wp_ns):
        key = get_text(postmeta.find('wp:meta_key', wp_ns))
        value = get_text(postmeta.find('wp:meta_value', wp_ns))
        if key:
            item_data['postmeta'][key] = value
    
    # Extract comments
    for comment in item.findall('wp:comment', wp_ns):
        comment_data = extract_comment_data(comment, wp_ns)
        item_data['comments'].append(comment_data)
    
    return item_data

def extract_comment_data(comment, wp_ns):
    """Extract comment data"""
    return {
        'comment_id': get_text(comment.find('wp:comment_id', wp_ns)),
        'comment_author': get_text(comment.find('wp:comment_author', wp_ns)),
        'comment_author_email': get_text(comment.find('wp:comment_author_email', wp_ns)),
        'comment_author_url': get_text(comment.find('wp:comment_author_url', wp_ns)),
        'comment_author_IP': get_text(comment.find('wp:comment_author_IP', wp_ns)),
        'comment_date': get_text(comment.find('wp:comment_date', wp_ns)),
        'comment_date_gmt': get_text(comment.find('wp:comment_date_gmt', wp_ns)),
        'comment_content': get_text(comment.find('wp:comment_content', wp_ns)),
        'comment_approved': get_text(comment.find('wp:comment_approved', wp_ns)),
        'comment_type': get_text(comment.find('wp:comment_type', wp_ns)),
        'comment_parent': get_text(comment.find('wp:comment_parent', wp_ns)),
        'comment_user_id': get_text(comment.find('wp:comment_user_id', wp_ns))
    }

def extract_category_data(category):
    """Extract taxonomy data"""
    wp_ns = {'wp': 'http://wordpress.org/export/1.2/'}
    
    return {
        'term_id': get_text(category.find('wp:term_id', wp_ns)),
        'category_nicename': get_text(category.find('wp:category_nicename', wp_ns)),
        'category_parent': get_text(category.find('wp:category_parent', wp_ns)),
        'cat_name': get_text(category.find('wp:cat_name', wp_ns)),
        'category_description': get_text(category.find('wp:category_description', wp_ns))
    }

def get_text(element):
    """Safely get text from XML element"""
    if element is not None:
        return element.text or ''
    return ''

def save_analysis(analysis, output_path):
    """Save analysis to JSON file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"Analysis saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return False

def print_summary(analysis):
    """Print analysis summary"""
    print("\n" + "="*60)
    print("CHOLOT XML STRUCTURE ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"Total Items: {analysis['meta_info']['total_items']}")
    print(f"XML Root: {analysis['meta_info']['xml_root_tag']}")
    
    print(f"\nItem Type Breakdown:")
    for item_type, count in analysis['item_types_count'].items():
        print(f"  {item_type}: {count}")
    
    print(f"\nPages: {len(analysis['pages'])}")
    print(f"Posts: {len(analysis['posts'])}")
    print(f"Media Attachments: {len(analysis['media_attachments'])}")
    print(f"Menu Items: {len(analysis['menu_items'])}")
    print(f"Custom Post Types: {len(analysis['custom_post_types'])}")
    print(f"Items with Elementor Data: {len(analysis['elementor_data'])}")
    print(f"Items with Cholot Widgets: {len(analysis['cholot_widgets'])}")
    print(f"Taxonomies: {len(analysis['taxonomies'])}")
    
    print(f"\nTop Pages by ID:")
    for i, (post_id, page_data) in enumerate(list(analysis['pages'].items())[:5]):
        print(f"  ID {post_id}: {page_data.get('title', 'No title')[:50]}")
    
    print(f"\nCholot Widget Types Found:")
    cholot_keys = set()
    for item_data in analysis['cholot_widgets'].values():
        cholot_keys.update(item_data['cholot_data'].keys())
    
    for key in sorted(cholot_keys):
        print(f"  {key}")

if __name__ == "__main__":
    xml_path = "/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml"
    output_path = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot_target_structure.json"
    
    print("Starting Cholot XML Structure Analysis...")
    
    analysis = analyze_xml_structure(xml_path)
    
    if analysis:
        print_summary(analysis)
        
        if save_analysis(analysis, output_path):
            print(f"\n✓ Complete analysis saved to: {output_path}")
        else:
            print(f"\n✗ Failed to save analysis")
    else:
        print("Failed to analyze XML structure")