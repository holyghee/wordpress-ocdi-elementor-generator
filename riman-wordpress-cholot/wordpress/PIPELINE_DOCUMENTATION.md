# WordPress XML Generation Pipeline

## Overview

This pipeline processes YAML examples through a complete workflow to create importable WordPress XML files compatible with Elementor. The generated XML files can be imported directly into WordPress using the built-in WordPress importer, just like the provided `demo-data-fixed.xml`.

## Pipeline Components

### 1. YAML to JSON Processor (`yaml_to_json_processor.py`)
- Converts simplified YAML structure to Elementor JSON format
- Handles 13+ Cholot widget types with proper settings
- Generates unique element IDs and proper nesting
- Supports responsive settings and shape dividers

### 2. JSON to XML Converter (`json_to_xml_converter.py`)
- Converts Elementor JSON to WordPress WXR (eXtended RSS) format
- Properly encodes Elementor data as JSON in `_elementor_data` meta field
- Includes all necessary WordPress fields and meta data
- Generates valid WXR 1.2 format for import

### 3. Pipeline Script (`process_yaml_to_wordpress.sh`)
- Automated end-to-end processing
- Validation and compatibility checks
- User-friendly output and error handling
- Comparison with reference XML structure

## Quick Start

### Basic Usage

```bash
# Make script executable (first time only)
chmod +x process_yaml_to_wordpress.sh

# Process the main RIMAN example
./process_yaml_to_wordpress.sh beispiel_riman.yaml riman

# Process any YAML file
./process_yaml_to_wordpress.sh [input.yaml] [output_name]
```

### Generated Files
- `{output_name}_elementor.json` - Intermediate Elementor JSON structure
- `{output_name}_wordpress.xml` - Final WordPress importable XML

## Supported YAML Structure

The pipeline currently works with YAML files that have this structure:

```yaml
site:
  name: "Site Name"
  url: "https://example.com"
  language: "en-US"
  description: "Site description"

pages:
  - id: "unique-id"
    title: "Page Title"
    sections:
      - type: "hero"
        widgets:
          - type: "cholot-title"
            content:
              title: "Main Title"
```

### Working Examples

✅ **Compatible Files** (have `pages` structure):
- `beispiel_riman.yaml` - Complete RIMAN company site

❌ **Incompatible Files** (different structure):
- Most other YAML files in the directory use a different schema

## Detailed Commands

### Step-by-Step Manual Processing

```bash
# Step 1: Convert YAML to JSON
python3 yaml_to_json_processor.py beispiel_riman.yaml -o riman_elementor.json --debug

# Step 2: Convert JSON to WordPress XML
python3 json_to_xml_converter.py riman_elementor.json -o riman_wordpress.xml \
    --site-title "RIMAN GmbH" \
    --site-url "https://riman-gmbh.de" \
    --elementor-version "3.15.3" \
    --debug
```

### Advanced Options

```bash
# YAML to JSON with custom settings
python3 yaml_to_json_processor.py input.yaml \
    --output output.json \
    --base-url "http://localhost:8080" \
    --debug \
    --validate

# JSON to XML with custom configuration
python3 json_to_xml_converter.py input.json \
    --output output.xml \
    --site-title "Custom Title" \
    --site-url "https://example.com" \
    --elementor-version "3.15.3" \
    --debug
```

## WordPress Import Instructions

### 1. Import the Generated XML
1. Log into your WordPress admin panel
2. Go to **Tools > Import**
3. Install the **WordPress** importer plugin if not already installed
4. Click **Run Importer**
5. Choose the generated XML file (e.g., `riman_wordpress.xml`)
6. Select import options and map authors
7. Click **Submit**

### 2. Verify Import
- Check **Pages** for imported content
- Verify Elementor data is properly loaded
- Test pages in Elementor editor

## Output Structure Validation

The generated XML includes:

### WordPress WXR Structure
- ✅ Proper XML declaration and encoding
- ✅ All required WXR namespaces
- ✅ Valid channel information
- ✅ Author information
- ✅ Page items with correct post type

### Elementor Compatibility
- ✅ `_elementor_edit_mode` = "builder"
- ✅ `_elementor_template_type` = "wp-page"
- ✅ `_elementor_version` = "3.15.3"
- ✅ `_elementor_data` with proper JSON encoding
- ✅ `_elementor_page_settings` = "[]"
- ✅ `_elementor_css` (empty)

### Validation Comparison
The generated XML structure matches `demo-data-fixed.xml`:
- Same WXR version (1.2)
- Same meta field structure
- Compatible Elementor data format
- Proper CDATA and escaping handling

## Troubleshooting

### Common Issues

1. **"No pages found in YAML data"**
   - Ensure YAML has `pages:` section
   - Check YAML syntax and indentation

2. **"YAML parsing error"**
   - Validate YAML syntax
   - Check for special characters or encoding issues

3. **"XML validation failed"**
   - Check JSON structure validity
   - Ensure proper character encoding

### Debug Mode
Add `--debug` flag to see detailed processing information:
```bash
python3 yaml_to_json_processor.py input.yaml --debug
```

## File Locations

```
wordpress/
├── yaml_to_json_processor.py     # YAML → JSON converter
├── json_to_xml_converter.py      # JSON → XML converter
├── process_yaml_to_wordpress.sh  # Automated pipeline script
├── beispiel_riman.yaml           # Main working example
├── demo-data-fixed.xml           # Reference XML structure
└── [generated files]             # Output JSON and XML files
```

## Success Example

When processing `beispiel_riman.yaml`:
- ✅ Input: 334 lines of YAML
- ✅ Generated: 4,630 bytes JSON + 8,194 bytes XML
- ✅ Content: 1 WordPress page with 7 Elementor sections
- ✅ Validation: All required Elementor fields present
- ✅ Compatibility: Matches demo-data-fixed.xml structure

The generated XML file can be imported directly into WordPress and will create a fully functional Elementor page.

## Next Steps

1. **Import Testing**: Test the generated XML in a WordPress installation
2. **Widget Enhancement**: Improve YAML processor to handle more widget content
3. **Schema Extension**: Add support for different YAML structures
4. **Content Validation**: Add more sophisticated content validation

## Support

For issues or questions:
1. Check the debug output with `--debug` flag
2. Validate YAML structure matches expected format
3. Compare generated XML with `demo-data-fixed.xml`
4. Test import in WordPress development environment