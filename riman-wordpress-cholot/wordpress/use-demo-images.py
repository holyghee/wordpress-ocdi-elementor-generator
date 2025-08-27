#!/usr/bin/env python3
"""
Update Elementor JSON to use working demo image URLs from demo.ridianur.com
"""

import json
import re

def use_demo_images(json_file, output_file):
    """Replace broken image URLs with working ones from demo.ridianur.com."""
    
    # Read the JSON file
    with open(json_file, 'r') as f:
        content = f.read()
    
    # URL patterns to replace - use the working demo URLs
    replacements = [
        # Replace theme.winnertheme.com with demo.ridianur.com
        (r'https://theme\.winnertheme\.com/cholot/wp-content/uploadz/', 
         'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/'),
        (r'https:\\/\\/theme\\.winnertheme\\.com\\/cholot\\/wp-content\\/uploadz\\/', 
         'https:\\/\\/demo.ridianur.com\\/cholot\\/wp-content\\/uploads\\/sites\\/9\\/'),
         
        # Replace localhost:8080 with demo.ridianur.com
        (r'http://localhost:8080/wp-content/uploads/', 
         'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/'),
        (r'http:\\/\\/localhost:8080\\/wp-content\\/uploads\\/', 
         'https:\\/\\/demo.ridianur.com\\/cholot\\/wp-content\\/uploads\\/sites\\/9\\/'),
         
        # Replace localhost:8082 (our previous fix) back to demo URLs
        (r'http://localhost:8082/wp-content/uploads/', 
         'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/'),
        (r'http:\\/\\/localhost:8082\\/wp-content\\/uploads\\/', 
         'https:\\/\\/demo.ridianur.com\\/cholot\\/wp-content\\/uploads\\/sites\\/9\\/'),
    ]
    
    # Apply replacements
    fixed_content = content
    for pattern, replacement in replacements:
        fixed_content = re.sub(pattern, replacement, fixed_content)
    
    # Parse to verify JSON is still valid
    try:
        json_data = json.loads(fixed_content)
        print(f"✅ JSON is valid after URL fixes")
        
        # Count demo.ridianur.com URLs
        demo_count = len(re.findall(r'demo\.ridianur\.com', fixed_content))
        print(f"📊 URLs pointing to demo.ridianur.com: {demo_count}")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalid after fixes: {e}")
        return False
    
    # Save the fixed JSON
    with open(output_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"✅ Saved fixed JSON to: {output_file}")
    return True

def create_yaml_with_demo_urls(yaml_file, json_file):
    """Create YAML that uses the demo image URLs."""
    
    yaml_content = f"""# Cholot Homepage with Working Demo Image URLs
site:
  title: "Cholot Theme Demo"
  description: "Using working demo.ridianur.com image URLs"
  base_url: "http://localhost:8082"
  language: "en-US"

pages:
  - title: "Cholot Home (Demo Images)"
    slug: "home"
    status: "publish"
    post_id: 1482
    template: "elementor_canvas"
    
    # Use the elementor data with demo URLs
    elementor_data_file: "{json_file}"
    
    # Meta fields
    meta_fields:
      _elementor_template_type: "page"
      _elementor_version: "3.15.0"
      _wp_page_template: "elementor_canvas"
    
    # Optional content
    content: |
      <!-- wp:paragraph -->
      <p>This page uses Cholot theme demo images from demo.ridianur.com</p>
      <!-- /wp:paragraph -->
"""
    
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    
    print(f"✅ Created YAML file: {yaml_file}")

if __name__ == "__main__":
    # Fix the Elementor JSON to use demo URLs
    input_json = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor-content-only.json"
    output_json = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor-content-demo-urls.json"
    
    if use_demo_images(input_json, output_json):
        # Create YAML that uses the demo URLs JSON
        yaml_file = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/cholot-demo-urls.yaml"
        create_yaml_with_demo_urls(yaml_file, output_json)
        
        print("\n🎯 Next steps:")
        print("1. Generate XML: python generate_wordpress_xml.py -i cholot-demo-urls.yaml -o cholot-demo-urls.xml")
        print("2. Import the XML - images will load from demo.ridianur.com")
        print("3. The demo images should work without downloading!")