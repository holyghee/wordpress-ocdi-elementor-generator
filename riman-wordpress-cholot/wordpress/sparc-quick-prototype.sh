#!/bin/bash

echo "⚡ SPARC Quick Prototype - Elementor JSON Generator"
echo "==================================================="
echo ""
echo "🎯 Goal: Build working prototype in 1 hour"
echo ""

# Single comprehensive SPARC command for rapid prototyping
npx claude-flow sparc run code "Build minimal viable Elementor JSON generator prototype. 

WORKING DIRECTORY: /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress

CRITICAL FILES TO ANALYZE:
- /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor-templates/home-page.json (52KB, real Cholot template)
- /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor-templates/service-page.json (real service widgets)
- /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/generate_wordpress_xml.py (line 74-400: CholotComponentFactory with 13 widgets)
- /Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml (reference XML structure)

EXISTING PROTOTYPES TO LEVERAGE:
- adaptive-layout-engine.py (line 57-89: calculate_layout function for responsive grids)
- content-design-separator.py (line 40-52: shows placeholder concept)
- block-library-system.py (line 48-79: extract_section_block method)

KNOWN WIDGET STRUCTURE (from templates):
{
  'id': '7-char-id',
  'elType': 'widget',
  'widgetType': 'cholot-texticon',
  'settings': {
    'title': 'TEXT_HERE',
    'selected_icon': {'value': 'fas fa-crown'},
    'title_typography_font_size': {'unit': 'px', 'size': 24},
    // 40+ more parameters with specific structure
  }
}

IMMEDIATE TASKS:
1. Load and parse /wordpress/elementor-templates/home-page.json
2. Extract cholot-hero, cholot-texticon, cholot-services widget patterns
3. Create ElementorGenerator class that generates valid JSON matching the structure
4. Test with: company='RIMAN GmbH', services=['Asbestsanierung', 'PCB-Sanierung', 'Schimmelsanierung']
5. Output must match exact structure from templates (all nested objects, units, etc.)

DELIVERABLE: elementor_json_generator.py that:
- Generates JSON identical to template structure
- Integrates with generate_wordpress_xml.py workflow
- Handles the 400+ parameters correctly

VALIDATION: Generated JSON must import successfully when wrapped in XML by generate_wordpress_xml.py"

echo ""
echo "🏁 Quick prototype will be ready at: elementor_json_generator.py"