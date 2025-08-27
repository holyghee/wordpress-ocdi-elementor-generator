#!/usr/bin/env python3
"""
Final cleanup script to fix remaining path issues in the SEO XML.
"""
import re
from pathlib import Path

def main():
    """Main function to clean up the XML file."""
    # File paths
    script_dir = Path(__file__).parent
    input_file = script_dir.parent / "wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml"
    
    print(f"Reading XML file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Cleaning up path issues...")
    
    # Fix double path issues like /2025/08/2019/06/
    xml_content = xml_content.replace('/2025/08/2019/06/', '/2025/08/')
    xml_content = xml_content.replace('/2025/08/2019/07/', '/2025/08/')
    
    # Fix any remaining 2019 date references in paths
    xml_content = re.sub(r'2025/08/2019/0[67]/', '2025/08/', xml_content)
    
    # Fix any remaining https references to use http localhost
    xml_content = xml_content.replace('https://www.riman.de/', 'http://localhost:8081/')
    
    print(f"Writing cleaned XML back to: {input_file}")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ Final cleanup completed!")
    print("📁 The riman-content-transformed-seo.xml file is ready for import")

if __name__ == "__main__":
    main()