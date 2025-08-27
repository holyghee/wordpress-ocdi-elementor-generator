#!/usr/bin/env python3
"""
Fix image URLs in Elementor JSON data to match local WordPress installation
"""

import json
import re
import sys
from pathlib import Path

def fix_image_urls(json_file, output_file, new_base_url="http://localhost:8082"):
    """Fix all image URLs in Elementor JSON data."""
    
    # Read the JSON file
    with open(json_file, 'r') as f:
        content = f.read()
    
    # URL patterns to replace
    replacements = [
        # Replace localhost:8080 with new base URL
        (r'http://localhost:8080', new_base_url),
        (r'http:\\/\\/localhost:8080', new_base_url.replace('/', '\\/')),
        
        # Replace theme.winnertheme.com URLs
        (r'https://theme\.winnertheme\.com/cholot', new_base_url),
        (r'https:\\/\\/theme\\.winnertheme\\.com\\/cholot', new_base_url.replace('/', '\\/')),
        
        # Fix uploadz to uploads
        (r'/uploadz/', '/uploads/'),
        (r'\\/uploadz\\/', '\\/uploads\\/')
    ]
    
    # Apply replacements
    fixed_content = content
    for pattern, replacement in replacements:
        fixed_content = re.sub(pattern, replacement, fixed_content)
    
    # Parse to verify JSON is still valid
    try:
        json_data = json.loads(fixed_content)
        print(f"✅ JSON is valid after URL fixes")
        
        # Count URLs
        url_count = len(re.findall(r'"url":', fixed_content))
        local_count = len(re.findall(f'{new_base_url}', fixed_content))
        
        print(f"📊 Total URLs found: {url_count}")
        print(f"📊 URLs pointing to {new_base_url}: {local_count}")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalid after fixes: {e}")
        return False
    
    # Save the fixed JSON
    with open(output_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"✅ Saved fixed JSON to: {output_file}")
    return True

def create_yaml_with_fixed_urls(yaml_file, json_file):
    """Create YAML that uses the fixed JSON file."""
    
    yaml_content = f"""# Cholot Homepage with Fixed Image URLs
site:
  title: "Cholot Theme Test"
  description: "Testing with fixed image URLs"
  base_url: "http://localhost:8082"
  language: "en-US"

pages:
  - title: "Cholot Home (Fixed URLs)"
    slug: "home"
    status: "publish"
    post_id: 1482
    template: "elementor_canvas"
    
    # Use the fixed elementor data
    elementor_data_file: "{json_file}"
    
    # Meta fields
    meta_fields:
      _elementor_template_type: "page"
      _elementor_version: "3.15.0"
      _wp_page_template: "elementor_canvas"
"""
    
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    
    print(f"✅ Created YAML file: {yaml_file}")

if __name__ == "__main__":
    # Fix the Elementor JSON
    input_json = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor-content-only.json"
    output_json = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor-content-fixed-urls.json"
    
    if fix_image_urls(input_json, output_json):
        # Create YAML that uses the fixed JSON
        yaml_file = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot-fixed-urls.yaml"
        create_yaml_with_fixed_urls(yaml_file, output_json)
        
        print("\n🎯 Next steps:")
        print("1. Upload the demo images to: wp-content/uploads/2019/06/ and wp-content/uploads/2019/07/")
        print("2. Generate the XML: python generate_wordpress_xml.py -i cholot-fixed-urls.yaml -o cholot-fixed-urls.xml")
        print("3. Import the XML into WordPress")