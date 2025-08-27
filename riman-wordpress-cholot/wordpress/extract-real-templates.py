#!/usr/bin/env python3
"""
Extract REAL Cholot widget templates from actual Elementor JSON files
This solves the problem: We need complete widget structures, not just settings lists!
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import copy

class RealTemplateExtractor:
    """
    Extracts complete widget structures from real Elementor exports
    """
    
    def __init__(self):
        self.widget_templates = {}
        self.cholot_widgets = [
            'cholot-texticon', 'cholot-title', 'cholot-post-three', 
            'cholot-post-four', 'cholot-gallery', 'cholot-logo', 
            'cholot-menu', 'cholot-button-text', 'cholot-team', 
            'cholot-testimonial-two', 'cholot-text-line', 
            'cholot-contact', 'cholot-sidebar'
        ]
    
    def extract_from_json(self, json_file: str) -> Dict[str, List[Dict]]:
        """
        Extract all Cholot widgets from an Elementor JSON file
        """
        print(f"📂 Analyzing: {json_file}")
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        widgets_found = {}
        
        def find_widgets(element, depth=0):
            """Recursively find all Cholot widgets"""
            
            # Check if this is a widget
            if isinstance(element, dict):
                widget_type = element.get('widgetType', '')
                
                # Is it a Cholot widget?
                if widget_type in self.cholot_widgets:
                    if widget_type not in widgets_found:
                        widgets_found[widget_type] = []
                    
                    # Store COMPLETE widget structure
                    widget_copy = copy.deepcopy(element)
                    widgets_found[widget_type].append(widget_copy)
                    
                    print(f"  {'  ' * depth}✅ Found {widget_type}")
                    print(f"  {'  ' * depth}   ID: {element.get('id', 'unknown')}")
                    print(f"  {'  ' * depth}   Settings: {len(element.get('settings', {}))} properties")
                
                # Check nested elements
                if 'elements' in element:
                    for child in element['elements']:
                        find_widgets(child, depth + 1)
            
            # Handle lists
            elif isinstance(element, list):
                for item in element:
                    find_widgets(item, depth)
        
        # Start extraction
        find_widgets(data)
        
        return widgets_found
    
    def extract_from_all_templates(self):
        """
        Extract widgets from all template files
        """
        template_files = [
            'elementor-templates/home-page.json',
            'elementor-templates/service-page.json',
            'elementor-templates/about-page.json',
            'elementor-templates/gallery-page.json',
            'elementor-templates/contact-page.json',
            'elementor-templates/post-page.json',
            'elementor-templates/portfolio-page.json',
            'elementor-content-only.json'
        ]
        
        all_widgets = {}
        
        for template_file in template_files:
            if Path(template_file).exists():
                widgets = self.extract_from_json(template_file)
                
                # Merge into main collection
                for widget_type, instances in widgets.items():
                    if widget_type not in all_widgets:
                        all_widgets[widget_type] = []
                    all_widgets[widget_type].extend(instances)
        
        return all_widgets
    
    def create_widget_library(self):
        """
        Create a library of widget templates with complete structures
        """
        print("\n🔍 EXTRACTING REAL WIDGET TEMPLATES")
        print("=" * 50)
        
        all_widgets = self.extract_from_all_templates()
        
        # Create template library
        template_library = {
            "metadata": {
                "description": "Real Cholot widget templates extracted from actual Elementor exports",
                "source": "elementor-templates/*.json",
                "complete_structure": True
            },
            "widgets": {}
        }
        
        print("\n📚 WIDGET LIBRARY SUMMARY")
        print("=" * 50)
        
        for widget_type in self.cholot_widgets:
            if widget_type in all_widgets and all_widgets[widget_type]:
                # Take the first instance as template
                template = all_widgets[widget_type][0]
                
                # Identify content fields (that should be replaced)
                content_fields = self.identify_content_fields(template)
                
                template_library["widgets"][widget_type] = {
                    "template": template,
                    "instances_found": len(all_widgets[widget_type]),
                    "content_fields": content_fields,
                    "structure": {
                        "has_id": "id" in template,
                        "has_elements": "elements" in template,
                        "settings_count": len(template.get("settings", {})),
                        "is_inner": template.get("isInner", False)
                    }
                }
                
                print(f"✅ {widget_type}:")
                print(f"   - {len(all_widgets[widget_type])} instances found")
                print(f"   - {len(template.get('settings', {}))} settings")
                print(f"   - Content fields: {', '.join(content_fields[:5])}")
            else:
                print(f"❌ {widget_type}: Not found in templates")
        
        # Save the library
        output_file = "cholot-widget-templates-complete.json"
        with open(output_file, 'w') as f:
            json.dump(template_library, f, indent=2)
        
        print(f"\n💾 Saved to: {output_file}")
        print(f"📊 Total size: {Path(output_file).stat().st_size:,} bytes")
        
        return template_library
    
    def identify_content_fields(self, widget: Dict) -> List[str]:
        """
        Identify which fields contain content (vs styling)
        """
        content_keywords = [
            'title', 'text', 'subtitle', 'description', 'content',
            'heading', 'label', 'caption', 'btn_text', 'button_text',
            'name', 'position', 'testimonial', 'quote'
        ]
        
        content_fields = []
        settings = widget.get('settings', {})
        
        for key, value in settings.items():
            # Check if this is likely a content field
            if any(keyword in key.lower() for keyword in content_keywords):
                # Skip typography and style settings
                if not any(skip in key for skip in ['_typography', '_color', '_size', '_align']):
                    content_fields.append(key)
        
        return content_fields
    
    def demonstrate_template_usage(self):
        """
        Show how to use the extracted templates
        """
        print("\n🎯 HOW TO USE THE TEMPLATES")
        print("=" * 50)
        
        print("""
# Load the template library
with open('cholot-widget-templates-complete.json', 'r') as f:
    library = json.load(f)

# Get a widget template
texticon_template = library['widgets']['cholot-texticon']['template']

# Deep copy to preserve original
my_widget = copy.deepcopy(texticon_template)

# Only modify content fields
my_widget['settings']['title'] = 'RIMAN GmbH'
my_widget['settings']['text'] = 'Professionelle Sanierung'

# Keep all 400+ other parameters exactly as they are!
# This ensures 100% Cholot compatibility
        """)


def main():
    extractor = RealTemplateExtractor()
    
    # Extract and create library
    library = extractor.create_widget_library()
    
    # Show usage
    extractor.demonstrate_template_usage()
    
    print("\n✨ SUCCESS!")
    print("Now you have REAL widget templates with complete structures!")
    print("Use these instead of guessing the widget format!")


if __name__ == "__main__":
    main()