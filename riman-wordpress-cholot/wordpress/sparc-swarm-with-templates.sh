#!/bin/bash

echo "🚀 SPARC SWARM: Orchestrated Elementor Generator with Real Templates"
echo "===================================================================="
echo ""

npx claude-flow sparc run sparc "Orchestrate SWARM for template-based Elementor generator.

WORKING DIR: /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress

AVAILABLE RESOURCES:
- cholot_widgets_catalog.json (42KB - widget property documentation)
- cholot-widget-properties-catalog.json (13KB - property descriptions)
- elementor-templates/*.json (7 REAL Cholot templates with actual values)
- enhanced_elementor_generator.py (existing generator to extend)

CRITICAL INSIGHT: The widget catalog tells us WHAT properties exist, but the templates show us HOW they should look!

SPAWN SPECIALIZED AGENTS:

1. TEMPLATE-ANALYST:
   - Load elementor-templates/home-page.json, service-page.json, about-page.json
   - Extract REAL widget instances (not just property names)
   - Create widget_templates.json with actual working examples
   - Note default values, units, nested structures

2. PATTERN-ARCHITECT:
   - Compare catalog properties with real template values
   - Design TemplateWidgetFactory that uses real JSON, not hardcoded
   - Define extraction strategy for each of 13 widgets
   - Create placeholder mapping system

3. EXTRACTOR-1 (Core Widgets):
   - Extract cholot-texticon from templates (find all instances)
   - Extract cholot-title instances
   - Extract cholot-button-text instances
   - Save complete JSON structures with all 400+ params

4. EXTRACTOR-2 (Content Widgets):
   - Extract cholot-post-three, cholot-post-four
   - Extract cholot-gallery instances
   - Extract cholot-team, cholot-testimonial-two

5. EXTRACTOR-3 (Layout Widgets):
   - Extract cholot-menu, cholot-logo
   - Extract cholot-text-line, cholot-contact
   - Extract cholot-sidebar instances

6. INTEGRATOR:
   - Merge extracted templates into widget library
   - Create generate_from_template() method
   - Add content injection with {{placeholders}}
   - Preserve all styling/structure from templates

7. VALIDATOR:
   - Compare generated JSON with original templates
   - Ensure structure matches exactly (except content)
   - Test with RIMAN GmbH example
   - Verify import compatibility

COORDINATION STRATEGY:
- Phase 1: PARALLEL extraction (Agents 3-5)
- Phase 2: SEQUENTIAL integration and validation
- Phase 3: Test with real WordPress import

DELIVERABLE: template_widget_factory.py that:
- Uses REAL templates as base (not guessed structures)
- Extracts actual widgets from elementor-templates/*.json
- Only modifies content fields
- Preserves all Cholot styling and structure
- 100% compatible with original theme

KEY DIFFERENCE from previous approach:
- DON'T build widgets from scratch
- DO extract and reuse real widget JSON
- DON'T guess parameter values
- DO preserve exact template structure"

echo ""
echo "⚡ This SWARM uses the REAL templates, not theoretical structures!"