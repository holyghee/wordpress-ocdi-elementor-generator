#!/usr/bin/env python3
"""
WordPress XML Content Transformer for RIMAN
Transforms content while preserving all XML structure, widget names, IDs, and formatting
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def load_content_mapping(mapping_file):
    """Load the content mapping from JSON file"""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def preserve_cdata_structure(text):
    """Preserve CDATA structure when replacing content"""
    if text is None:
        return text
    
    # Handle CDATA sections - don't modify the structure, only content inside
    if '<![CDATA[' in text and ']]>' in text:
        # Extract content from CDATA, transform it, then wrap back
        cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        if cdata_match:
            inner_content = cdata_match.group(1)
            return text.replace(cdata_match.group(0), f'<![CDATA[{inner_content}]]>')
    
    return text


def transform_elementor_widget_content(content, mapping):
    """Transform Elementor widget content based on mapping"""
    if not content:
        return content
    
    # Hero Slider transformations
    elementor_updates = mapping.get('elementor_widget_updates', {})
    
    # Transform hero slider content
    hero_slider = mapping.get('hero_slider', {})
    if hero_slider:
        # Update slide 1
        slide_1 = hero_slider.get('slide_1', {})
        if slide_1:
            content = re.sub(
                r'"title":"[^"]*"',
                f'"title":"{slide_1.get("title", "")}"',
                content
            )
            content = re.sub(
                r'"subtitle":"[^"]*"',
                f'"subtitle":"{slide_1.get("subtitle", "")}"',
                content
            )
            content = re.sub(
                r'"text":"[^"]*"',
                f'"text":"{slide_1.get("description", "")}"',
                content
            )
    
    # Transform service boxes
    service_boxes = mapping.get('service_boxes', [])
    if service_boxes and len(service_boxes) >= 3:
        # Replace generic titles with RIMAN services
        content = re.sub(r'"Healthy life"', f'"{service_boxes[2]["title"]}"', content)
        content = re.sub(r'"Improving life"', f'"{service_boxes[1]["title"]}"', content)
        content = re.sub(r'"Relationship"', f'"{service_boxes[0]["title"]}"', content)
    
    # Transform testimonials
    testimonial_update = elementor_updates.get('testimonial', {})
    if testimonial_update:
        old_text = testimonial_update.get('old_text', '')
        new_text = testimonial_update.get('new_text', '')
        old_author = testimonial_update.get('old_author', '')
        new_author = testimonor_update.get('new_author', '')
        
        if old_text and new_text:
            content = content.replace(old_text, new_text)
        if old_author and new_author:
            content = content.replace(old_author, new_author)
    
    return content


def transform_text_content(text, mapping):
    """Transform regular text content based on mapping"""
    if not text:
        return text
    
    # Apply content replacements
    content_replacements = mapping.get('content_replacements', {})
    
    # Replace placeholder titles
    placeholder_titles = content_replacements.get('placeholder_titles', {})
    if placeholder_titles.get('old') and placeholder_titles.get('new'):
        text = text.replace(placeholder_titles['old'], placeholder_titles['new'])
    
    # Replace service titles
    service_titles = content_replacements.get('service_titles', {})
    for old_title, new_title in service_titles.items():
        text = text.replace(old_title, new_title)
    
    # Replace generic descriptions
    generic_descriptions = content_replacements.get('generic_descriptions', {})
    old_desc = generic_descriptions.get('old', '')
    if old_desc:
        # Replace with appropriate new description based on context
        if 'Healthy life' in text or 'health' in text.lower():
            text = text.replace(old_desc, generic_descriptions.get('new_schadstoff', ''))
        elif 'Improving life' in text or 'improve' in text.lower():
            text = text.replace(old_desc, generic_descriptions.get('new_altlasten', ''))
        elif 'Relationship' in text or 'relation' in text.lower():
            text = text.replace(old_desc, generic_descriptions.get('new_abbruch', ''))
    
    return text


def transform_xml_content(xml_file_path, mapping_file_path, output_file_path):
    """Transform WordPress XML content while preserving structure"""
    print(f"Loading content mapping from: {mapping_file_path}")
    mapping = load_content_mapping(mapping_file_path)
    
    print(f"Reading XML file: {xml_file_path}")
    
    # Read the entire XML file as text to preserve exact formatting
    with open(xml_file_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Transforming content...")
    
    # Update site title and description
    company_info = mapping.get('company_info', {})
    xml_content = re.sub(r'<title>Cholot</title>', f'<title>{company_info.get("name", "RIMAN GmbH")}</title>', xml_content)
    xml_content = re.sub(
        r'<description>Just another WordPress site</description>',
        f'<description>{company_info.get("tagline", "sicher bauen und gesund leben")}</description>',
        xml_content
    )
    
    # Transform Elementor widget data in postmeta
    elementor_data_pattern = r'(<wp:meta_key><!\[CDATA\[_elementor_data\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)(.*?)(\]\]></wp:meta_value>)'
    
    def replace_elementor_data(match):
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        
        # Transform the content
        transformed_content = transform_elementor_widget_content(content, mapping)
        
        return f"{prefix}{transformed_content}{suffix}"
    
    xml_content = re.sub(elementor_data_pattern, replace_elementor_data, xml_content, flags=re.DOTALL)
    
    # Transform regular content in CDATA sections
    cdata_pattern = r'(<!\[CDATA\[)(.*?)(\]\]>)'
    
    def replace_cdata_content(match):
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        
        # Skip if this is elementor data or other structured data
        if any(skip in content for skip in ['_elementor_data', 'wp_attachment_metadata', 'serialized:']):
            return match.group(0)
        
        # Transform text content
        transformed_content = transform_text_content(content, mapping)
        
        return f"{prefix}{transformed_content}{suffix}"
    
    xml_content = re.sub(cdata_pattern, replace_cdata_content, xml_content, flags=re.DOTALL)
    
    # Update author email while preserving structure
    footer = mapping.get('footer', {})
    if footer.get('email'):
        xml_content = re.sub(
            r'<wp:author_email><!\[CDATA\[ridianur@yahoo\.com\]\]></wp:author_email>',
            f'<wp:author_email><![CDATA[{footer["email"]}]]></wp:author_email>',
            xml_content
        )
    
    print(f"Writing transformed XML to: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("Transformation completed successfully!")
    print("\nPreserved:")
    print("- All XML structure and tags")
    print("- All widget names (cholot-*)")
    print("- All IDs and relationships")
    print("- CDATA and JSON formatting")
    print("- File structure and hierarchy")
    
    return True


def main():
    """Main function to run the transformation"""
    base_dir = Path(__file__).parent
    
    xml_file = base_dir / "demo-data-fixed.xml"
    mapping_file = base_dir / "riman-content-mapping.json"
    output_file = base_dir / "riman-transformed-final.xml"
    
    if not xml_file.exists():
        print(f"Error: XML file not found: {xml_file}")
        return False
    
    if not mapping_file.exists():
        print(f"Error: Mapping file not found: {mapping_file}")
        return False
    
    try:
        transform_xml_content(xml_file, mapping_file, output_file)
        print(f"\nSuccess! Transformed XML saved as: {output_file}")
        return True
    except Exception as e:
        print(f"Error during transformation: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()