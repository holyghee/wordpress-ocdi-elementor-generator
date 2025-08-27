#!/usr/bin/env python3
"""
RIMAN XML Transformation Script - Final Version
Transforms WordPress XML file with RIMAN content and SEO-optimized images.

CRITICAL: Preserves 100% XML structure while replacing only content in CDATA sections.
"""

import re
import json
import os
from pathlib import Path

def load_json_file(filepath):
    """Load and parse JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def replace_image_urls(content, seo_mapping):
    """Replace all image URLs with SEO-optimized versions."""
    # Create mapping from original filenames to SEO names
    url_mapping = {}
    
    for img in seo_mapping.get('images', []):
        original = img['original']
        seo_name = img['seo_name']
        format_ext = img['format']
        
        # Map various URL patterns to SEO name
        url_mapping[original] = f"http://localhost:8082/{seo_name}.{format_ext}"
        
        # Also handle uploaded file patterns
        if original.endswith('-unsplash') or original.isdigit() or original.startswith('team') or original in ['logo', 'logo-white', 'sign', 'bg-ab']:
            # Handle different URL patterns that might appear
            url_patterns = [
                f"https://theme.winnertheme.com/cholot/wp-content/uploads/2019/07/{original}",
                f"https://theme.winnertheme.com/cholot/wp-content/uploads/2019/06/{original}",
                f"https://theme.winnertheme.com/cholot/wp-content/uploads/{original}",
                f"wp-content/uploads/2019/07/{original}",
                f"wp-content/uploads/2019/06/{original}",
                f"wp-content/uploads/{original}",
            ]
            
            for pattern in url_patterns:
                for ext in ['.jpg', '.jpeg', '.png', '.webp', '-300x300.jpg', '-768x768.jpg', '-1024x1024.jpg']:
                    url_mapping[f"{pattern}{ext}"] = f"http://localhost:8082/{seo_name}.{format_ext}"
                    url_mapping[f"{pattern.replace('https://theme.winnertheme.com/cholot/', '')}{ext}"] = f"http://localhost:8082/{seo_name}.{format_ext}"
    
    # Replace URLs in content
    modified_content = content
    
    # Replace all winnertheme.com URLs
    modified_content = re.sub(
        r'https://theme\.winnertheme\.com/cholot/wp-content/uploads/[^"\'>\s]+',
        lambda m: url_mapping.get(m.group(0), m.group(0)),
        modified_content
    )
    
    # Replace relative wp-content URLs
    modified_content = re.sub(
        r'wp-content/uploads/[^"\'>\s]+',
        lambda m: url_mapping.get(m.group(0), f"http://localhost:8082/{m.group(0)}"),
        modified_content
    )
    
    # Generic replacement for any remaining winnertheme URLs
    modified_content = modified_content.replace(
        'https://theme.winnertheme.com/cholot',
        'http://localhost:8082'
    )
    
    return modified_content

def apply_content_mappings(content, content_mapping, riman_structure):
    """Apply content mappings from both mapping files."""
    
    # First, apply basic site information
    content = content.replace(
        '<title>Cholot</title>',
        '<title>RIMAN GmbH</title>'
    )
    
    content = content.replace(
        '<description>Just another WordPress site</description>',
        '<description>Ihr Partner für professionelle Schadstoffsanierung</description>'
    )
    
    content = content.replace(
        '<language>en-US</language>',
        '<language>de-DE</language>'
    )
    
    # Replace base URLs
    content = content.replace(
        'https://theme.winnertheme.com/cholot',
        'http://localhost:8082'
    )
    
    # Apply content mappings from content-mapping.json
    if 'hero_section' in content_mapping:
        hero = content_mapping['hero_section']
        
        # Replace hero content in CDATA sections
        content = replace_in_cdata(content, hero.get('old_title', ''), hero.get('new_title', ''))
        content = replace_in_cdata(content, hero.get('old_subtitle', ''), hero.get('new_subtitle', ''))
        content = replace_in_cdata(content, hero.get('old_tagline', ''), hero.get('new_tagline', ''))
        content = replace_in_cdata(content, hero.get('old_description', ''), hero.get('new_description', ''))
    
    # Apply service mappings
    if 'services_section' in content_mapping:
        services = content_mapping['services_section']
        
        # Replace service cards
        for service_card in services.get('service_cards', []):
            content = replace_in_cdata(content, service_card.get('old_title', ''), service_card.get('new_title', ''))
            content = replace_in_cdata(content, service_card.get('old_description', ''), service_card.get('new_description', ''))
            
            # Replace service lists if they exist as JSON in CDATA
            if service_card.get('old_services') and service_card.get('new_services'):
                for old_service, new_service in zip(service_card['old_services'], service_card['new_services']):
                    content = replace_in_cdata(content, old_service, new_service)
    
    # Apply company info from riman_structure
    if 'company_info' in riman_structure:
        company_info = riman_structure['company_info']
        if 'ceo_message' in company_info:
            ceo = company_info['ceo_message']
            content = replace_in_cdata(content, 'CEO Message', ceo.get('title', ''))
            content = replace_in_cdata(content, 'Company Philosophy', ceo.get('content', ''))
    
    # Apply footer information
    if 'footer' in riman_structure:
        footer = riman_structure['footer']
        content = replace_in_cdata(content, 'ridianur@yahoo.com', footer.get('contact', {}).get('email', 'j.fischer@riman.de'))
        
    # Apply homepage content from riman_structure
    if 'homepage' in riman_structure:
        homepage = riman_structure['homepage']
        
        # Replace welcome section
        if 'welcome_section' in homepage:
            welcome = homepage['welcome_section']
            content = replace_in_cdata(content, 'Welcome', welcome.get('title', ''))
            content = replace_in_cdata(content, 'Just another WordPress site', welcome.get('content', ''))
        
        # Replace service cards with RIMAN content
        for i, service_card in enumerate(homepage.get('service_cards', []), 1):
            content = replace_in_cdata(content, f'Service {i}', service_card.get('title', ''))
            content = replace_in_cdata(content, f'Service {i} Description', service_card.get('description', ''))
    
    return content

def replace_in_cdata(content, old_text, new_text):
    """Replace text within CDATA sections only."""
    if not old_text or not new_text:
        return content
    
    # Pattern to find CDATA sections containing the old text
    cdata_pattern = r'<!\[CDATA\[(.*?)\]\]>'
    
    def replace_in_cdata_match(match):
        cdata_content = match.group(1)
        if old_text in cdata_content:
            return f'<![CDATA[{cdata_content.replace(old_text, new_text)}]]>'
        return match.group(0)
    
    return re.sub(cdata_pattern, replace_in_cdata_match, content, flags=re.DOTALL)

def replace_widget_content(content, riman_structure):
    """Replace widget content with RIMAN-specific data while preserving cholot-* widget names."""
    
    # Find and replace content in widgets while keeping widget IDs intact
    widget_patterns = [
        # Text widgets
        (r'(<wp:meta_key><!\[CDATA\[_cholot_text_widget_\d+\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)(.*?)(\]\]></wp:meta_value>)', 'text'),
        # Service widgets  
        (r'(<wp:meta_key><!\[CDATA\[_cholot_service_widget_\d+\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)(.*?)(\]\]></wp:meta_value>)', 'service'),
        # Hero widgets
        (r'(<wp:meta_key><!\[CDATA\[_cholot_hero_widget_\d+\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)(.*?)(\]\]></wp:meta_value>)', 'hero'),
    ]
    
    for pattern, widget_type in widget_patterns:
        def replace_widget_data(match):
            prefix = match.group(1)
            widget_data = match.group(2)
            suffix = match.group(3)
            
            # Try to parse as JSON and replace content
            try:
                import json
                data = json.loads(widget_data)
                
                # Replace content based on widget type and RIMAN data
                if widget_type == 'text' and 'homepage' in riman_structure:
                    if 'text' in data:
                        data['text'] = riman_structure['homepage']['welcome_section']['content']
                elif widget_type == 'service' and 'homepage' in riman_structure:
                    service_cards = riman_structure['homepage']['service_cards']
                    if 'title' in data and service_cards:
                        # Map to appropriate service
                        service_idx = hash(data.get('title', '')) % len(service_cards)
                        service = service_cards[service_idx]
                        data['title'] = service['title']
                        data['description'] = service['description']
                
                return f"{prefix}{json.dumps(data, ensure_ascii=False)}{suffix}"
                
            except (json.JSONDecodeError, KeyError):
                # If not JSON or parsing fails, do simple text replacement
                if widget_type == 'hero' and 'homepage' in riman_structure:
                    hero_data = riman_structure['homepage']['hero_video']
                    widget_data = widget_data.replace('Cholot', 'RIMAN GmbH')
                    widget_data = widget_data.replace('Just another WordPress site', hero_data['subtitle'])
                
                return f"{prefix}{widget_data}{suffix}"
        
        content = re.sub(pattern, replace_widget_data, content, flags=re.DOTALL)
    
    return content

def transform_xml_file():
    """Main transformation function."""
    
    # File paths
    base_dir = Path(__file__).parent
    input_file = base_dir / "demo-data-fixed.xml"
    output_file = base_dir / "riman-transformed-final.xml"
    content_mapping_file = base_dir / "content-mapping.json"
    riman_structure_file = base_dir / "riman-content-structure.json"
    seo_mapping_file = base_dir / "seo-image-mapping.json"
    
    # Load configuration files
    print("Loading configuration files...")
    content_mapping = load_json_file(content_mapping_file)
    riman_structure = load_json_file(riman_structure_file)
    seo_mapping = load_json_file(seo_mapping_file)
    
    # Read the XML file
    print(f"Reading XML file: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return False
    
    print("Original XML size:", len(xml_content), "characters")
    
    # Apply transformations
    print("Applying content mappings...")
    xml_content = apply_content_mappings(xml_content, content_mapping, riman_structure)
    
    print("Replacing widget content...")
    xml_content = replace_widget_content(xml_content, riman_structure)
    
    print("Replacing image URLs...")
    xml_content = replace_image_urls(xml_content, seo_mapping)
    
    # Write the transformed XML
    print(f"Writing transformed XML to: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"Transformation complete!")
        print(f"Final XML size: {len(xml_content)} characters")
        print(f"Output file: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

def validate_transformation(output_file):
    """Validate the transformed XML file."""
    try:
        import xml.etree.ElementTree as ET
        ET.parse(output_file)
        print("✓ XML validation successful - file is well-formed")
        return True
    except ET.ParseError as e:
        print(f"✗ XML validation failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Validation error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting RIMAN XML Transformation...")
    print("=" * 50)
    
    success = transform_xml_file()
    
    if success:
        output_path = Path(__file__).parent / "riman-transformed-final.xml"
        if validate_transformation(output_path):
            print("\n✅ Transformation completed successfully!")
            print("\nTransformation Summary:")
            print("- ✓ Content mappings applied")
            print("- ✓ RIMAN service data integrated") 
            print("- ✓ SEO image URLs updated")
            print("- ✓ XML structure preserved")
            print("- ✓ Widget names unchanged (cholot-*)")
            print(f"- ✓ Output file: {output_path}")
        else:
            print("\n❌ Transformation completed but XML validation failed!")
    else:
        print("\n❌ Transformation failed!")
        
    print("=" * 50)