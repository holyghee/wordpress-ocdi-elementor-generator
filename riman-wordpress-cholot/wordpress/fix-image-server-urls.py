#!/usr/bin/env python3
"""
Fix XML to use external image server (port 8082) for images.
"""
import re
from pathlib import Path

def main():
    """Fix image URLs to point to external server."""
    
    input_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml")
    output_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/riman-import-final.xml")
    
    print(f"Reading XML file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Fixing image URLs to use external server...")
    
    # Change image URLs from localhost:8081 to localhost:8082
    # And remove the wp-content/uploads path since images are in root of image server
    
    # Fix attachment URLs - these should download from external server
    xml_content = xml_content.replace(
        'http://localhost:8081/wp-content/uploads/2025/08/',
        'http://localhost:8082/'
    )
    
    # Also remove size variants for main images (keep only for display)
    # WordPress will generate its own sizes after import
    
    print(f"Writing final import XML to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ Created final import XML with external server URLs")
    print("🌐 Images will be downloaded from: http://localhost:8082/")
    print(f"📁 Import this file: {output_file}")
    print("\nImportant: Make sure the image server is running on port 8082!")

if __name__ == "__main__":
    main()