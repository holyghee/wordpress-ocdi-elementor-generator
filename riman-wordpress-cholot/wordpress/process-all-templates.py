#!/usr/bin/env python3
"""
Process all Elementor template JSON files:
1. Extract content array from export format
2. Fix image URLs to use demo.ridianur.com
3. Create YAML files for each template
"""

import json
import re
import os
from pathlib import Path

def process_elementor_template(input_file, output_name):
    """Process a single Elementor template file."""
    
    print(f"\n📋 Processing: {output_name}")
    
    # Read the export JSON
    with open(input_file, 'r') as f:
        export_data = json.load(f)
    
    # Extract content array
    content = export_data.get('content', [])
    title = export_data.get('title', output_name)
    page_type = export_data.get('type', 'page')
    
    print(f"  ✓ Found {len(content)} sections")
    print(f"  ✓ Title: {title}")
    print(f"  ✓ Type: {page_type}")
    
    # Convert to string for URL replacement
    content_str = json.dumps(content, separators=(',', ':'))
    
    # Fix URLs
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
    ]
    
    for pattern, replacement in replacements:
        content_str = re.sub(pattern, replacement, content_str)
    
    # Parse back to verify
    content_fixed = json.loads(content_str)
    
    # Save fixed JSON
    json_output = f"/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/templates/{output_name}.json"
    os.makedirs(os.path.dirname(json_output), exist_ok=True)
    
    with open(json_output, 'w') as f:
        json.dump(content_fixed, f, separators=(',', ':'))
    
    print(f"  ✓ Saved JSON: {json_output}")
    
    # Create YAML
    yaml_output = f"/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/templates/{output_name}.yaml"
    
    slug = output_name.lower().replace(' ', '-').replace('_', '-')
    
    yaml_content = f"""# {title} - Cholot Theme Template
site:
  title: "Cholot Theme"
  description: "Retirement Community WordPress Theme"
  base_url: "http://localhost:8082"
  language: "en-US"

pages:
  - title: "{title}"
    slug: "{slug}"
    status: "publish"
    template: "elementor_canvas"
    
    # Elementor data from template
    elementor_data_file: "{json_output}"
    
    # Meta fields
    meta_fields:
      _elementor_template_type: "{page_type}"
      _elementor_version: "3.15.0"
      _wp_page_template: "elementor_canvas"
"""
    
    with open(yaml_output, 'w') as f:
        f.write(yaml_content)
    
    print(f"  ✓ Created YAML: {yaml_output}")
    
    return {
        'name': output_name,
        'title': title,
        'sections': len(content),
        'json_file': json_output,
        'yaml_file': yaml_output
    }

def main():
    """Process all template files."""
    
    templates = [
        ("/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json", "home-page"),
        ("/Users/holgerbrandt/Downloads/elementor-1488-2025-08-27.json", "service-page"),
        ("/Users/holgerbrandt/Downloads/elementor-1491-2025-08-27.json", "single-service-1"),
        ("/Users/holgerbrandt/Downloads/elementor-1494-2025-08-27.json", "single-service-2"),
        ("/Users/holgerbrandt/Downloads/elementor-1500-2025-08-27.json", "blog-page"),
        ("/Users/holgerbrandt/Downloads/elementor-1485-2025-08-27.json", "about-page"),
        ("/Users/holgerbrandt/Downloads/elementor-1497-2025-08-27.json", "contact-page"),
    ]
    
    print("🚀 Processing all Cholot theme templates...")
    print("=" * 50)
    
    results = []
    
    for input_file, output_name in templates:
        if os.path.exists(input_file):
            result = process_elementor_template(input_file, output_name)
            results.append(result)
        else:
            print(f"\n❌ File not found: {input_file}")
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    for result in results:
        print(f"\n✅ {result['title']}")
        print(f"   - Sections: {result['sections']}")
        print(f"   - JSON: {os.path.basename(result['json_file'])}")
        print(f"   - YAML: {os.path.basename(result['yaml_file'])}")
    
    print(f"\n🎉 Processed {len(results)} templates successfully!")
    
    # Create master YAML with all pages
    create_master_yaml(results)

def create_master_yaml(results):
    """Create a master YAML file with all pages."""
    
    master_yaml = """# Cholot Theme - Complete Site Import
# All pages with fixed image URLs

site:
  title: "Cholot Retirement Community"
  description: "Complete Cholot Theme Import"
  base_url: "http://localhost:8082"
  language: "en-US"

pages:"""
    
    for i, result in enumerate(results):
        master_yaml += f"""
  - title: "{result['title']}"
    slug: "{result['name'].lower().replace('_', '-')}"
    status: "publish"
    post_id: {1482 + i}
    template: "elementor_canvas"
    elementor_data_file: "{result['json_file']}"
    meta_fields:
      _elementor_template_type: "page"
      _elementor_version: "3.15.0"
      _wp_page_template: "elementor_canvas"
"""
    
    master_file = "/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/templates/cholot-complete-site.yaml"
    
    with open(master_file, 'w') as f:
        f.write(master_yaml)
    
    print(f"\n📦 Created master YAML: {master_file}")
    print("   Use this to import ALL pages at once!")

if __name__ == "__main__":
    main()