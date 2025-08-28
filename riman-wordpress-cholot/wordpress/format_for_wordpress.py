#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def format_for_wordpress_xml(elementor_data, company_name="RIMAN GmbH"):
    """
    Formats the Elementor data for the WordPress XML generator
    """
    wordpress_format = {
        "site": {
            "title": company_name,
            "url": "https://example.com",
            "description": f"{company_name} Website"
        },
        "posts": [
            {
                "title": f"{company_name} - Home",
                "slug": "home",
                "type": "page",
                "status": "publish",
                "template": "elementor_canvas",
                "meta": {
                    "_elementor_edit_mode": "builder",
                    "_elementor_template_type": "wp-page",
                    "_elementor_version": "3.14.1",
                    "_elementor_data": json.dumps(elementor_data)
                }
            }
        ]
    }
    
    return wordpress_format

def main():
    if len(sys.argv) < 2:
        print("Usage: python format_for_wordpress.py <input_json> [output_json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '_formatted.json')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        elementor_data = json.load(f)
    
    # Extract company name from filename if possible
    company_name = Path(input_file).stem.replace('_page', '').replace('_', ' ').title()
    
    formatted_data = format_for_wordpress_xml(elementor_data, company_name)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Formatted for WordPress XML: {output_file}")
    
    return output_file

if __name__ == '__main__':
    main()