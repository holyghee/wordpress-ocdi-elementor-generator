#!/usr/bin/env python3
"""
Script to update WordPress XML with SEO-optimized German image filenames.
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
    
    # Base URL mappings
    old_base = "https://www.riman.de/wp-content/uploads/sites/9/"
    new_base = "http://localhost:8081/wp-content/uploads/2025/08/"
    
    for image in image_mapping['images']:
        original = image['original']
        seo_name = image['seo_name']
        alt_text = image['alt_text']
        file_format = image['format']
        
        # Main image filename
        old_filename = f"{original}.jpg"  # Default to jpg for most
        if original in ['logo', 'logo-white', 'sign', '5', '6']:
            old_filename = f"{original}.png"
        
        new_filename = f"{seo_name}.{file_format}"
        
        # Create mappings for different contexts
        # 1. Basic filename replacements
        replacements[old_filename] = new_filename
        replacements[original] = seo_name
        
        # 2. Full URL replacements
        replacements[f"{old_base}2019/06/{old_filename}"] = f"{new_base}{new_filename}"
        replacements[f"{old_base}2019/07/{old_filename}"] = f"{new_base}{new_filename}"
        
        # 3. GUID replacements
        replacements[f"https://www.riman.de/wp-content/uploads/sites/9/2019/06/{old_filename}"] = f"{new_base}{new_filename}"
        replacements[f"https://www.riman.de/wp-content/uploads/sites/9/2019/07/{old_filename}"] = f"{new_base}{new_filename}"
        
        # 4. Attachment URL replacements
        replacements[f"2019/06/{old_filename}"] = f"2025/08/{new_filename}"
        replacements[f"2019/07/{old_filename}"] = f"2025/08/{new_filename}"
        
        # 5. Different sized versions
        size_suffixes = ['-150x150', '-300x200', '-300x199', '-300x225', '-768x510', '-768x511', '-768x512', '-768x576', '-1024x680', '-1024x681', '-1024x683', '-1024x768', '-500x300']
        
        for suffix in size_suffixes:
            old_sized = f"{original}{suffix}.jpg"
            new_sized = f"{seo_name}{suffix}.jpg"
            replacements[old_sized] = new_sized
            
            # Full URLs for sized versions
            replacements[f"{old_base}2019/06/{old_sized}"] = f"{new_base}{new_sized}"
            replacements[f"{old_base}2019/07/{old_sized}"] = f"{new_base}{new_sized}"
        
        # 6. Standard WordPress sizes
        # Thumbnail (300x300)
        replacements[f"{original}-300x300.{file_format}"] = f"{seo_name}-300x300.{file_format}"
        # Medium (768x768) 
        replacements[f"{original}-768x768.{file_format}"] = f"{seo_name}-768x768.{file_format}"
        
    # Special cases for cropped images
    replacements["cropped-matteo-vistocco-537858-unsplash"] = "schadstoffsanierung-detailaufnahme-ausruestung"
    replacements["cropped-matteo-vistocco-537858-unsplash-32x32.jpg"] = "schadstoffsanierung-detailaufnahme-ausruestung-32x32.jpg"
    
    # Logo variations
    replacements["logo-white-1.png"] = "riman-gmbh-logo-weiss.png"
    
    return replacements

def update_xml_content(xml_content, replacements, image_mapping):
    """Update XML content with new SEO filenames and structure."""
    
    # First, handle URL replacements
    for old_pattern, new_pattern in replacements.items():
        xml_content = xml_content.replace(old_pattern, new_pattern)
    
    # Add alt text attributes where missing
    # This is a complex task that would require careful HTML parsing
    # For now, we'll focus on the main replacements
    
    # Update base site URLs
    xml_content = xml_content.replace(
        'https://www.riman.de/wp-content/uploads/sites/9/',
        'http://localhost:8081/wp-content/uploads/2025/08/'
    )
    
    # Update any remaining date-based paths
    xml_content = xml_content.replace('2019/06/', '2025/08/')
    xml_content = xml_content.replace('2019/07/', '2025/08/')
    
    # Update post names and slugs to use SEO names
    for image in image_mapping['images']:
        original = image['original']
        seo_name = image['seo_name']
        
        # Update post names in CDATA sections
        xml_content = xml_content.replace(
            f'<wp:post_name><![CDATA[{original}]]></wp:post_name>',
            f'<wp:post_name><![CDATA[{seo_name}]]></wp:post_name>'
        )
        
        # Update titles
        xml_content = xml_content.replace(
            f'<title>{original}</title>',
            f'<title>{seo_name}</title>'
        )
        
        # Update links
        xml_content = xml_content.replace(
            f'https://www.riman.de/Projekt/{original}/',
            f'http://localhost:8081/projekt/{seo_name}/'
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