#!/bin/bash

# ============================================
# YAML to WordPress XML Pipeline
# ============================================
# 
# This script processes YAML examples through the complete pipeline 
# to create importable WordPress XML files compatible with Elementor.
#
# Usage: ./process_yaml_to_wordpress.sh [yaml_file] [output_name]
#
# Examples:
#   ./process_yaml_to_wordpress.sh beispiel_riman.yaml riman
#   ./process_yaml_to_wordpress.sh restaurant_example.yaml restaurant
#   ./process_yaml_to_wordpress.sh service_company.yaml service
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default files
YAML_FILE="${1:-beispiel_riman.yaml}"
OUTPUT_NAME="${2:-riman}"
JSON_FILE="${OUTPUT_NAME}_elementor.json"
XML_FILE="${OUTPUT_NAME}_wordpress.xml"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE} YAML to WordPress XML Pipeline${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check if files exist
if [ ! -f "$YAML_FILE" ]; then
    echo -e "${RED}❌ Error: YAML file '$YAML_FILE' not found!${NC}"
    echo ""
    echo "Available YAML files:"
    ls -1 *.yaml 2>/dev/null || echo "  No YAML files found"
    exit 1
fi

if [ ! -f "yaml_to_json_processor.py" ]; then
    echo -e "${RED}❌ Error: yaml_to_json_processor.py not found!${NC}"
    exit 1
fi

if [ ! -f "json_to_xml_converter.py" ]; then
    echo -e "${RED}❌ Error: json_to_xml_converter.py not found!${NC}"
    exit 1
fi

echo -e "${YELLOW}📁 Input YAML: $YAML_FILE${NC}"
echo -e "${YELLOW}📄 Output JSON: $JSON_FILE${NC}"
echo -e "${YELLOW}📋 Output XML: $XML_FILE${NC}"
echo ""

# Step 1: Convert YAML to JSON
echo -e "${BLUE}🔄 Step 1: Converting YAML to Elementor JSON...${NC}"
if python3 yaml_to_json_processor.py "$YAML_FILE" -o "$JSON_FILE" --debug; then
    echo -e "${GREEN}✅ YAML to JSON conversion completed${NC}"
else
    echo -e "${RED}❌ YAML to JSON conversion failed${NC}"
    exit 1
fi

# Check if JSON was created
if [ ! -f "$JSON_FILE" ]; then
    echo -e "${RED}❌ Error: JSON file was not created${NC}"
    exit 1
fi

echo ""

# Step 2: Convert JSON to WordPress XML
echo -e "${BLUE}🔄 Step 2: Converting JSON to WordPress XML...${NC}"
if python3 json_to_xml_converter.py "$JSON_FILE" -o "$XML_FILE" --debug; then
    echo -e "${GREEN}✅ JSON to XML conversion completed${NC}"
else
    echo -e "${RED}❌ JSON to XML conversion failed${NC}"
    exit 1
fi

# Check if XML was created
if [ ! -f "$XML_FILE" ]; then
    echo -e "${RED}❌ Error: XML file was not created${NC}"
    exit 1
fi

echo ""

# Step 3: Validate and report
echo -e "${BLUE}🔍 Step 3: Validating output...${NC}"

# Check file sizes
JSON_SIZE=$(wc -c < "$JSON_FILE")
XML_SIZE=$(wc -c < "$XML_FILE")

echo -e "${GREEN}📊 File sizes:${NC}"
echo -e "  JSON: ${JSON_SIZE} bytes"
echo -e "  XML:  ${XML_SIZE} bytes"

# Count sections/pages
JSON_SECTIONS=$(grep -o '"elType":"section"' "$JSON_FILE" | wc -l || echo "0")
XML_PAGES=$(grep -c '<wp:post_type>page</wp:post_type>' "$XML_FILE" || echo "0")

echo -e "${GREEN}📈 Content stats:${NC}"
echo -e "  Elementor sections: ${JSON_SECTIONS}"
echo -e "  WordPress pages: ${XML_PAGES}"

echo ""

# Step 4: Compare with reference
echo -e "${BLUE}🔍 Step 4: Comparing with reference XML...${NC}"

if [ -f "demo-data-fixed.xml" ]; then
    echo -e "${GREEN}✅ Reference file found${NC}"
    
    # Check for required Elementor fields
    ELEMENTOR_FIELDS="_elementor_data _elementor_version _elementor_edit_mode _elementor_template_type"
    MISSING_FIELDS=""
    
    for field in $ELEMENTOR_FIELDS; do
        if grep -q "$field" "$XML_FILE"; then
            echo -e "  ✅ $field: Found"
        else
            echo -e "  ❌ $field: Missing"
            MISSING_FIELDS="$MISSING_FIELDS $field"
        fi
    done
    
    if [ -z "$MISSING_FIELDS" ]; then
        echo -e "${GREEN}✅ All required Elementor fields present${NC}"
    else
        echo -e "${YELLOW}⚠️  Missing fields:$MISSING_FIELDS${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Reference file demo-data-fixed.xml not found${NC}"
fi

echo ""

# Final success message
echo -e "${GREEN}🎉 Pipeline completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Generated files:${NC}"
echo -e "  📄 ${JSON_FILE} - Elementor JSON structure"
echo -e "  📋 ${XML_FILE} - WordPress importable XML"
echo ""
echo -e "${BLUE}🚀 Import Instructions:${NC}"
echo -e "  1. Log into your WordPress admin panel"
echo -e "  2. Go to Tools > Import"
echo -e "  3. Install the 'WordPress' importer plugin"
echo -e "  4. Choose file: ${XML_FILE}"
echo -e "  5. Import the content"
echo ""
echo -e "${BLUE}📚 Additional files to process:${NC}"
ls -1 *.yaml 2>/dev/null | grep -v "$YAML_FILE" || echo "  No other YAML files found"
echo ""