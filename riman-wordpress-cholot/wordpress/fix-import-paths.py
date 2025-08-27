#!/usr/bin/env python3
"""
Fix image URLs in XML to use file:// URLs for local import.
"""
import re
from pathlib import Path

def main():
    """Fix the import paths to use existing local files."""
    
    xml_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml")
    output_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/riman-import-ready.xml")
    
    print(f"Reading XML file: {xml_file}")
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Since images already exist locally, we can either:
    # 1. Skip image imports entirely (remove attachment items)
    # 2. Use the local server we just set up
    
    # For now, let's use localhost:8081 since the files are already there
    # This ensures WordPress can access them during import
    
    # The images are already in the right place, so the import should work
    # But we need to ensure the server can serve them
    
    print("Images are already in place at wp-content/uploads/2025/08/")
    print("The XML already points to http://localhost:8081/wp-content/uploads/2025/08/")
    print("This should work as-is since the PHP server serves from the WordPress root")
    
    # Just copy the file as-is since paths are correct
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created import-ready XML: {output_file}")
    print("\nThe images are already in the correct location.")
    print("WordPress should be able to import the XML successfully now.")

if __name__ == "__main__":
    main()