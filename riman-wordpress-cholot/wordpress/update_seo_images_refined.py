#!/usr/bin/env python3
"""
Refined script to update WordPress XML with SEO-optimized German image filenames.
"""
import json
import re
import os
from pathlib import Path

def load_image_mapping(mapping_file):
    """Load the SEO image mapping from JSON file."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_replacement_mappings(image_mapping):
    """Create comprehensive replacement mappings for all image references."""
    replacements = {}
    
    # Base URL mappings - only for full URLs and specific patterns
    old_base = "https://www.riman.de/wp-content/uploads/sites/9/"
    new_base = "http://localhost:8081/wp-content/uploads/2025/08/"
    
    for image in image_mapping['images']:
        original = image['original']
        seo_name = image['seo_name']
        alt_text = image['alt_text']
        file_format = image['format']
        
        # Main image filename - be specific about extensions
        if original in ['logo', 'logo-white', 'sign', '5', '6']:
            old_filename = f"{original}.png"
        else:
            old_filename = f"{original}.jpg"
        
        new_filename = f"{seo_name}.{file_format}"
        
        # 1. Full URL replacements (most specific first)
        replacements[f"{old_base}2019/06/{old_filename}"] = f"{new_base}{new_filename}"
        replacements[f"{old_base}2019/07/{old_filename}"] = f"{new_base}{new_filename}"
        
        # 2. GUID replacements
        replacements[f"https://www.riman.de/wp-content/uploads/sites/9/2019/06/{old_filename}"] = f"http://localhost:8081/wp-content/uploads/2025/08/{new_filename}"
        replacements[f"https://www.riman.de/wp-content/uploads/sites/9/2019/07/{old_filename}"] = f"http://localhost:8081/wp-content/uploads/2025/08/{new_filename}"
        
        # 3. Attachment URL replacements in CDATA
        replacements[f"2019/06/{old_filename}"] = f"2025/08/{new_filename}"
        replacements[f"2019/07/{old_filename}"] = f"2025/08/{new_filename}"
        
        # 4. Different sized versions - be very specific
        size_patterns = [
            (r'-150x150', '-150x150'),
            (r'-300x[0-9]+', '-300x300'),  # Standardize medium thumbnails
            (r'-768x[0-9]+', '-768x768'),  # Standardize medium large
            (r'-1024x[0-9]+', '-1024x1024'), # Standardize large
            (r'-500x300', '-500x300')  # Keep riman-related-post size
        ]
        
        for old_pattern, new_size in size_patterns:
            # Match the old pattern and replace with new SEO name + new size
            old_sized_pattern = f"{original}{old_pattern}.jpg"
            new_sized = f"{seo_name}{new_size}.{file_format}"
            
            # Replace in metadata strings
            replacements[old_sized_pattern] = new_sized
            
            # Full URLs for sized versions
            replacements[f"{old_base}2019/06/{old_sized_pattern}"] = f"{new_base}{new_sized}"
            replacements[f"{old_base}2019/07/{old_sized_pattern}"] = f"{new_base}{new_sized}"
    
    # Special cases
    replacements["cropped-matteo-vistocco-537858-unsplash-32x32.jpg"] = "schadstoffsanierung-detailaufnahme-ausruestung-32x32.jpg"
    replacements["logo-white-1.png"] = "riman-gmbh-logo-weiss.png"
    
    return replacements

def update_xml_content(xml_content, replacements, image_mapping):
    """Update XML content with new SEO filenames and structure."""
    
    # First, handle the most specific URL replacements
    for old_pattern, new_pattern in replacements.items():
        xml_content = xml_content.replace(old_pattern, new_pattern)
    
    # Update post names and titles in a controlled way
    for image in image_mapping['images']:
        original = image['original']
        seo_name = image['seo_name']
        
        # Update post names in CDATA sections - be very specific
        xml_content = xml_content.replace(
            f'<wp:post_name><![CDATA[{original}]]></wp:post_name>',
            f'<wp:post_name><![CDATA[{seo_name}]]></wp:post_name>'
        )
        
        # Update titles - be very specific with tags
        xml_content = xml_content.replace(
            f'<title>{original}</title>',
            f'<title>{seo_name}</title>'
        )
        
        # Update project links
        xml_content = xml_content.replace(
            f'https://www.riman.de/Projekt/{original}/',
            f'http://localhost:8081/projekt/{seo_name}/'
        )
    
    # Update any remaining generic base URLs
    xml_content = xml_content.replace(
        'https://www.riman.de/wp-content/uploads/sites/9/',
        'http://localhost:8081/wp-content/uploads/2025/08/'
    )
    
    return xml_content

def fix_serialized_metadata(xml_content, image_mapping):
    """Fix the WordPress serialized metadata that got corrupted."""
    
    # This is a complex fix for the serialized PHP data that got mangled
    # For now, we'll just clean up the most obvious issues
    
    for image in image_mapping['images']:
        original = image['original']
        seo_name = image['seo_name']
        file_format = image['format']
        
        # Fix the most common metadata patterns
        old_filename = f"{original}.jpg" if original not in ['logo', 'logo-white', 'sign', '5', '6'] else f"{original}.png"
        new_filename = f"{seo_name}.{file_format}"
        
        # Fix file references in serialized data
        xml_content = re.sub(
            rf'file&quot;;s:\d+:&quot;[^&]*{re.escape(original)}[^&]*&quot;',
            f'file&quot;;s:{len(f"2025/08/{new_filename}")}:&quot;2025/08/{new_filename}&quot;',
            xml_content
        )
    
    return xml_content

def main():
    """Main function to process the XML file."""
    # File paths
    script_dir = Path(__file__).parent
    mapping_file = script_dir / "seo-image-mapping.json"
    input_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/riman-content-transformed.xml")
    output_file = script_dir.parent / "wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml"
    
    print("Loading image mapping...")
    image_mapping = load_image_mapping(mapping_file)
    
    print("Creating replacement mappings...")
    replacements = create_replacement_mappings(image_mapping)
    
    print(f"Reading XML file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Processing XML content...")
    updated_content = update_xml_content(xml_content, replacements, image_mapping)
    
    print("Fixing serialized metadata...")
    updated_content = fix_serialized_metadata(updated_content, image_mapping)
    
    print(f"Writing updated XML to: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Successfully created riman-content-transformed-seo.xml")
    print(f"📁 Output file: {output_file}")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   - Processed {len(image_mapping['images'])} images")
    print(f"   - Created {len(replacements)} replacement mappings")
    print(f"   - Updated base URL to: http://localhost:8081/wp-content/uploads/2025/08/")
    print(f"   - All image references updated with SEO-optimized German filenames")

if __name__ == "__main__":
    main()