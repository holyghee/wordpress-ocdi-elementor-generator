#!/usr/bin/env python3
"""
Create XML with WebP images hosted on external server (port 8082).
This allows WordPress to properly import and download the images.
"""
import re
from pathlib import Path

def main():
    """Convert XML to use WebP images from external server."""
    
    input_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml")
    output_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/riman-webp-external.xml")
    
    print(f"Reading XML file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Converting to use external WebP images...")
    
    # Change base URL from localhost:8081 to localhost:8082 (external image server)
    xml_content = xml_content.replace(
        'http://localhost:8081/wp-content/uploads/2025/08/',
        'http://localhost:8082/'
    )
    
    # Convert .jpg to .webp
    xml_content = re.sub(r'\.jpg(?=["<\s])', '.webp', xml_content)
    
    # Update MIME types
    xml_content = xml_content.replace('image/jpeg', 'image/webp')
    
    # Fix attachment metadata
    xml_content = re.sub(
        r'(s:4:"file";s:\d+:")2025/08/([^"]+)\.jpg(")',
        r'\1\2.webp\3',
        xml_content
    )
    
    # Remove size variants since we only have full-size WebP
    # WordPress will generate thumbnails after import
    xml_content = re.sub(r'-\d+x\d+\.webp', '.webp', xml_content)
    
    # Update attachment URLs
    xml_content = re.sub(
        r'(<wp:attachment_url>.*?)\.jpg(</wp:attachment_url>)',
        r'\1.webp\2',
        xml_content
    )
    
    # Fix GUIDs
    xml_content = re.sub(
        r'(<guid.*?>.*?)\.jpg(</guid>)',
        r'\1.webp\2',
        xml_content
    )
    
    print(f"Writing external WebP XML to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ Created XML with external WebP images")
    print("🌐 Images will be served from: http://localhost:8082/")
    print("📦 WordPress will download and import them properly")
    print(f"📁 Import this file: {output_file}")

if __name__ == "__main__":
    main()