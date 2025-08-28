#!/usr/bin/env python3
"""
XML Formatter - Pretty format XML files for comparison
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def format_xml(input_file, output_file):
    """Format XML file with proper indentation"""
    print(f"Formatting {input_file} -> {output_file}")
    
    # Read the XML string
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_string = f.read()
    
    # Parse and pretty print
    try:
        # Parse the XML
        dom = minidom.parseString(xml_string)
        
        # Pretty print with tabs like the target
        pretty_xml = dom.toprettyxml(indent='\t', encoding='UTF-8')
        
        # Clean up empty lines
        lines = pretty_xml.decode('utf-8').split('\n')
        clean_lines = [line for line in lines if line.strip()]
        
        # Save formatted version
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(clean_lines))
        
        print(f"✅ Formatted XML saved to {output_file}")
        
    except Exception as e:
        print(f"Error formatting XML: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python xml_formatter.py input.xml output.xml")
        sys.exit(1)
    
    format_xml(sys.argv[1], sys.argv[2])