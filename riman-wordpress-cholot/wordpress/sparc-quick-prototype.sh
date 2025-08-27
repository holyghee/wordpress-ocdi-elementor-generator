#!/bin/bash

echo "⚡ SPARC Quick Prototype - Elementor JSON Generator"
echo "==================================================="
echo ""
echo "🎯 Goal: Build working prototype in 1 hour"
echo ""

# Single comprehensive SPARC command for rapid prototyping
npx claude-flow sparc run code "Build minimal viable Elementor JSON generator prototype. 

CONTEXT: We have 7 working Elementor templates in elementor-templates/*.json and a working XML generator (generate_wordpress_xml.py). We need to generate valid Elementor JSON from simple input.

IMMEDIATE TASKS:
1. Extract and analyze patterns from elementor-templates/home-page.json
2. Create ElementorGenerator class with 3 core widgets: cholot-hero, cholot-texticon, cholot-services
3. Implement simple content injection: replace {{TITLE}}, {{TEXT}} placeholders
4. Build test function that generates JSON for 'RIMAN GmbH with 3 services'
5. Validate output matches structure from templates

DELIVERABLE: Single Python file 'elementor_json_generator.py' that:
- Takes input: company_name, services_list
- Returns: Valid Elementor JSON
- Works with existing generate_wordpress_xml.py

Skip complex features - just make it work for basic use case.
Time limit: 60 minutes."

echo ""
echo "🏁 Quick prototype will be ready at: elementor_json_generator.py"