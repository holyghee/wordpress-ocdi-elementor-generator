#!/bin/bash

# ============================================
# WORKING COMMANDS - WordPress XML Pipeline
# ============================================
# 
# These are the exact commands that work with your current setup.
# Copy and paste these commands to process YAML to WordPress XML.

echo "=== WORKING COMMANDS FOR WORDPRESS XML GENERATION ==="
echo ""

echo "# 1. AUTOMATED PIPELINE (RECOMMENDED)"
echo "./process_yaml_to_wordpress.sh beispiel_riman.yaml riman"
echo ""

echo "# 2. MANUAL STEP-BY-STEP COMMANDS"
echo ""

echo "# Step 1: Convert YAML to JSON"
echo "python3 yaml_to_json_processor.py beispiel_riman.yaml -o riman_elementor.json --debug"
echo ""

echo "# Step 2: Convert JSON to WordPress XML"  
echo "python3 json_to_xml_converter.py riman_elementor.json -o riman_wordpress.xml \\"
echo "    --site-title 'RIMAN GmbH' \\"
echo "    --site-url 'https://riman-gmbh.de' \\"
echo "    --elementor-version '3.15.3' \\"
echo "    --debug"
echo ""

echo "# 3. VALIDATION COMMANDS"
echo ""

echo "# Check generated files exist"
echo "ls -la *riman*"
echo ""

echo "# Validate XML structure"
echo "grep -c '_elementor_data' riman_wordpress.xml"
echo "grep -c 'wp:post_type.*page' riman_wordpress.xml"
echo ""

echo "# Compare with reference"
echo "echo 'Generated XML size:' && wc -c riman_wordpress.xml"
echo "echo 'Reference XML size:' && wc -c demo-data-fixed.xml"
echo ""

echo "=== EXPECTED RESULTS ==="
echo "✅ riman_elementor.json - ~4,630 bytes"
echo "✅ riman_wordpress.xml - ~8,194 bytes"  
echo "✅ 1 WordPress page with Elementor data"
echo "✅ All required meta fields present"
echo "✅ Compatible with WordPress importer"
echo ""

echo "=== WORDPRESS IMPORT ==="
echo "1. WordPress Admin > Tools > Import"
echo "2. Install 'WordPress' importer plugin"
echo "3. Upload: riman_wordpress.xml"
echo "4. Import content"
echo ""

# If running this script, execute the commands
if [ "$1" = "run" ]; then
    echo "🚀 EXECUTING PIPELINE..."
    echo ""
    
    # Run the automated pipeline
    ./process_yaml_to_wordpress.sh beispiel_riman.yaml riman
    
    echo ""
    echo "✅ PIPELINE COMPLETED!"
    echo "📁 Files generated:"
    ls -la riman_*
fi