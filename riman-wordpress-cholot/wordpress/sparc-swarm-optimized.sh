#!/bin/bash

echo "🚀 OPTIMIZED SPARC SWARM: Template-Based Elementor Generator"
echo "============================================================"
echo ""

npx claude-flow sparc run sparc "Orchestrate SWARM for Elementor generator using template extraction.

WORKING DIR: /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress

## 🎯 PHASE 0: MEMORY CHECK (WICHTIG!)
First, check what we already know:
- npx claude-flow memory query 'elementor'
- npx claude-flow memory query 'cholot'
- npx claude-flow memory query 'widget_patterns'
Use existing knowledge to accelerate!

## 📊 PHASE 1: SINGLE-PASS ANALYSIS (Effizienter!)
Create ONE smart analyzer instead of 3:

SPAWN UNIFIED-ANALYZER:
- Load elementor-content-only.json (52KB)
- Parse ALL widgets in ONE pass
- Create widget_instance_map = {
    'cholot-texticon': [instance1, instance2, ...],
    'cholot-title': [instance1, instance2, ...],
    // ... für alle 13 widget types
  }
- Extract ACTUAL JSON, not descriptions
- OUTPUT: widget_library.json with real examples

## 🏗️ PHASE 2: PATTERN EXTRACTION (Fokussiert!)
SPAWN PATTERN-EXTRACTOR for each widget type:

For EACH widget type in parallel:
1. Take all instances from widget_library.json
2. Find common structure (what's always there)
3. Find variations (what changes)
4. Identify content fields vs styling fields
5. Create template with {{placeholders}} ONLY for content
6. Keep ALL styling exactly as-is

OUTPUT: templates/cholot-{widget}.template.json for each

## 🔧 PHASE 3: FACTORY BUILDER (Simpel!)
SPAWN FACTORY-CREATOR:

class TemplateBasedFactory:
    def __init__(self):
        self.templates = load_all_templates()
    
    def create_widget(self, widget_type, content_data):
        template = self.templates[widget_type]
        return inject_content(template, content_data)

Keep it SIMPLE - just template + content injection!

## ⚡ PHASE 4: TEST WITH REAL DATA
SPAWN TESTER:

Test case: RIMAN GmbH
- Company: 'RIMAN GmbH'
- Services: ['Asbestsanierung', 'PCB-Sanierung', 'Schimmelsanierung']
- Generate complete page JSON
- Wrap with generate_wordpress_xml.py
- Validate structure matches original

## 🎯 KEY OPTIMIZATIONS:

1. MEMORY FIRST: Check existing knowledge
2. SINGLE PASS: One analyzer, not three
3. REAL JSON: Extract actual widget JSON, not properties
4. MINIMAL CHANGES: Only replace content, keep ALL styling
5. TEMPLATE FILES: Save each widget as reusable template
6. SIMPLE FACTORY: Just template loading + content injection

## 📁 DELIVERABLES:

/templates/
  ├── cholot-texticon.template.json (real example with {{title}}, {{text}})
  ├── cholot-title.template.json
  ├── cholot-gallery.template.json
  └── ... (all 13 widgets)

template_based_generator.py:
  - load_template(widget_type)
  - inject_content(template, data)
  - generate_page(widgets_list)

## ⏱️ TIME ESTIMATE: 45 minutes
- 10 min: Analysis & extraction
- 15 min: Template creation
- 10 min: Factory implementation
- 10 min: Testing & validation

## 🚫 AVOID:
- Don't rebuild widgets from scratch
- Don't guess parameter values
- Don't modify styling parameters
- Don't create complex abstractions

## ✅ SUCCESS CRITERIA:
Generated JSON must be IDENTICAL to original except for content text/images"

echo ""
echo "🎯 Optimized for speed and accuracy - using real templates!"