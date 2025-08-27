#!/usr/bin/env python3
"""
Final path fix script for WordPress XML.
"""
import re
from pathlib import Path

def main():
    """Main function to fix all remaining path issues."""
    # File paths
    script_dir = Path(__file__).parent
    input_file = script_dir.parent / "wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml"
    
    print(f"Reading XML file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Fixing all remaining path issues...")
    
    # Fix meta_value CDATA paths that still have old dates
    xml_content = re.sub(r'2019/0[67]/', '2025/08/', xml_content)
    
    # Fix any remaining uploadz typos
    xml_content = xml_content.replace('/uploadz/', '/uploads/')
    xml_content = xml_content.replace('uploadz/', 'uploads/')
    
    print(f"Writing final fixed XML to: {input_file}")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ All path issues fixed!")
    print("📁 The riman-content-transformed-seo.xml file is ready for WordPress import")

if __name__ == "__main__":
    main()