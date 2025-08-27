#!/bin/bash

echo "🎯 SPARC: Template-Based Elementor Generator (Using REAL Cholot Templates)"
echo "=========================================================================="
echo ""

npx claude-flow sparc run code "Build template-based Elementor JSON generator using REAL Cholot templates.

WORKING DIR: /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress

CRITICAL INSIGHT: The existing generators (generate_wordpress_xml.py, enhanced_elementor_generator.py) are building widgets from scratch instead of using the real templates! We need to USE the actual JSON templates as base.

KEY FILES TO ANALYZE:
1. elementor-templates/home-page.json (52KB - REAL Cholot hero, services, etc.)
2. elementor-templates/service-page.json (REAL service layouts) 
3. elementor-templates/about-page.json (REAL about sections)
4. elementor-content-only.json (has all 13 widget examples in actual use)
5. generate_wordpress_xml.py lines 74-700 (shows what params the factory THINKS it needs)

THE 13 CHOLOT WIDGETS (from real templates):
cholot-texticon, cholot-title, cholot-post-three, cholot-post-four, cholot-gallery, cholot-logo, cholot-menu, cholot-button-text, cholot-team, cholot-testimonial-two, cholot-text-line, cholot-contact, cholot-sidebar

NEW APPROACH - Template Extraction & Reuse:
1. EXTRACT real widget instances from elementor-templates/*.json
   - Find each cholot-* widget type
   - Save complete JSON structure (all 400+ params)
   - Note which params are content vs styling

2. CREATE TemplateBasedGenerator class:
   ```python
   class TemplateBasedGenerator:
       def __init__(self):
           # Load REAL templates, not hardcoded structures
           self.templates = self.extract_from_real_json()
       
       def extract_from_real_json(self):
           # Parse elementor-templates/*.json
           # Extract each widget WITH its full structure
           # Keep ALL parameters (not just what we think we need)
       
       def generate_from_template(self, widget_type, content):
           # Get REAL widget template
           template = self.templates[widget_type]
           # Deep copy to preserve structure
           widget = copy.deepcopy(template)
           # ONLY replace content fields
           widget['settings']['title'] = content.get('title', widget['settings']['title'])
           # Keep all other 399+ params unchanged
           return widget
   ```

3. CONTENT INJECTION System:
   - Identify content fields: title, text, subtitle, btn_text, image urls
   - Keep ALL styling/layout params from template
   - Use placeholders: {{company_name}}, {{service_1}}, etc.

4. PRESERVE Template Integrity:
   - DO NOT modify structure params
   - DO NOT guess parameter values
   - DO NOT create params from scratch
   - USE exact JSON from templates

TEST CASE:
Input: {company: 'RIMAN GmbH', services: ['Asbestsanierung', 'PCB-Sanierung', 'Schimmelsanierung']}
Process:
1. Load home-page.json as base template
2. Find cholot-title widget, replace ONLY title text
3. Find cholot-texticon widgets, replace ONLY service names
4. Keep ALL other params exactly as in template

DELIVERABLE: template_based_generator.py that:
- Loads and parses REAL templates
- Extracts widget library from actual JSON
- Generates new pages using template structures
- Only modifies content, preserves all styling
- 100% compatible with Cholot theme

VALIDATION: Compare generated JSON with original templates - structure must be IDENTICAL except for content strings."

echo ""
echo "🚀 This approach uses the REAL templates instead of guessing the structure!"