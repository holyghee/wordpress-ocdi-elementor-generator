#!/usr/bin/env python3
"""
Convert XML to use WebP images instead of JPEG/PNG.
"""
import re
from pathlib import Path

def main():
    """Convert all image references to WebP format."""
    
    input_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml")
    output_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/riman-webp-import.xml")
    
    print(f"Reading XML file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Converting image references to WebP...")
    
    # Replace .jpg extensions with .webp in URLs and file references
    xml_content = re.sub(r'\.jpg(?=["<\s])', '.webp', xml_content)
    
    # Keep PNG files as PNG (logos need transparency)
    # But we can check if WebP versions exist for PNGs too
    png_files = [
        'riman-gmbh-logo',
        'riman-gmbh-logo-weiss',
        'riman-gmbh-firmenschild-gebaeude'
    ]
    
    # For PNG files, check if WebP exists, otherwise keep PNG
    for png_file in png_files:
        # Keep PNGs as is for now since they need transparency
        pass
    
    # Update MIME types for WebP
    xml_content = xml_content.replace('image/jpeg', 'image/webp')
    
    # Fix any attachment metadata that might reference JPEG
    xml_content = re.sub(
        r'(a:5:\{s:5:"width";i:\d+;s:6:"height";i:\d+;s:4:"file";s:\d+:")([^"]+)\.jpg(")',
        r'\1\2.webp\3',
        xml_content
    )
    
    # Remove thumbnail sizes since we don't have WebP versions of thumbnails
    # Or we could generate them
    xml_content = re.sub(r'-\d+x\d+\.webp', '.webp', xml_content)
    
    print(f"Writing WebP-optimized XML to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    # Count conversions
    webp_count = xml_content.count('.webp')
    print(f"✅ Converted to use WebP images")
    print(f"📊 Total WebP references: {webp_count}")
    print(f"📁 Output file: {output_file}")
    print("\n⚡ WebP images are 25-35% smaller than JPEG")
    print("🎯 Ready for import with modern image format!")

if __name__ == "__main__":
    main()