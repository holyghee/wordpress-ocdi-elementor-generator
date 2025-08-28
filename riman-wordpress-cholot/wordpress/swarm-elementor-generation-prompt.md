# SWARM Prompt: Elementor JSON Generation Pipeline

## Problem Statement
We need to generate complex Elementor page builder JSON (400+ parameters per widget) from simple YAML input (5-10 fields) to automate WordPress content creation.

## Current Situation
- **Pain Point**: Creating pages in Elementor UI is extremely tedious ("heute ist mir jedes mal die Hero Section in den Service Block gerutsch")
- **Business Need**: RIMAN GmbH needs to generate multiple SEO-optimized landing pages for different Berlin districts
- **Technical Challenge**: Elementor JSON has 400+ parameters per widget that must be preserved exactly

## Input (What we have)
Simple YAML with business information:
```yaml
company:
  name: "RIMAN GmbH"
  industry: "Schadstoffsanierung"
services:
  - title: "Asbestsanierung"
    description: "Sichere Asbestentfernung"
```

## Output (What we need)
Valid Elementor JSON matching the structure of `/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json`:
- 78,000+ characters of nested JSON
- Preserves all widget settings, animations, responsive settings
- Only changes actual text content
- Compatible with Cholot theme's 13 custom widgets

## The Core Challenge
1. **Complexity Gap**: Input has ~10 fields, output needs ~1000+ fields
2. **Structure Preservation**: Must maintain exact JSON structure or pages appear blank
3. **Widget Compatibility**: Must work with custom Cholot theme widgets (cholot-title, cholot-texticon, etc.)
4. **Batch Processing**: Need to generate 10-50 pages at once for SEO campaigns

## What We've Tried
1. **HTML to Elementor Conversion**: Too complex, requires understanding all CSS-to-JSON mappings
2. **AI/LLM Generation**: Unreliable for complex nested structures
3. **Template Extraction**: Partially successful but incomplete
4. **Fixed Code Generation**: Too rigid for varying content

## The Solution We Need
A hybrid approach that:
1. Loads the working template JSON (`elementor-1482-2025-08-27.json`)
2. Maps simple YAML fields to specific locations in the JSON
3. Preserves all non-content settings
4. Outputs valid JSON that can be embedded in WordPress XML
5. Supports batch generation of multiple pages

## Success Criteria
- Generated pages must display correctly (not blank/white)
- All Cholot widgets must render properly
- Content must be editable in Elementor after import
- Process must handle 10+ pages in one run
- No manual Elementor clicking required

## SWARM Architecture Needed

### Agent 1: Template Analyzer
- Parse and understand the template JSON structure
- Identify content insertion points
- Map widget types to content types

### Agent 2: Content Mapper
- Take simple YAML input
- Map fields to JSON locations
- Handle dynamic content counts (3 services vs 6 services)

### Agent 3: JSON Builder
- Preserve all structural/style parameters
- Insert content at correct locations
- Validate output structure

### Agent 4: Batch Processor
- Handle multiple page configurations
- Generate unique IDs for elements
- Ensure no conflicts between pages

### Agent 5: XML Wrapper
- Embed JSON in WordPress XML format
- Handle proper escaping
- Generate valid WXR format

## The Ask
Create a robust pipeline that transforms simple business information into production-ready Elementor pages, eliminating the need for manual page building while maintaining full design fidelity.

## Files to Reference
- Template: `/Users/holgerbrandt/Downloads/elementor-1482-2025-08-27.json`
- Current Generator: `elementor-json-generator-final.py`
- XML Generator: `generate_wordpress_xml.py`
- Example Config: `seo-content-config.yaml`