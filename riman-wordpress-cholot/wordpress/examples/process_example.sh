#!/bin/bash

# YAML Processor Examples - Processing Script
# This script demonstrates how to process each example YAML file

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== YAML Processor Examples ==="
echo ""

# Function to process a single example
process_example() {
    local example_name="$1"
    local description="$2"
    
    echo "--- Processing: $description ---"
    echo "📁 File: $example_name.yaml"
    
    if [ ! -f "$SCRIPT_DIR/$example_name.yaml" ]; then
        echo "❌ ERROR: $example_name.yaml not found!"
        return 1
    fi
    
    # Create output directory
    output_dir="$SCRIPT_DIR/output/$example_name"
    mkdir -p "$output_dir"
    
    echo "🔄 Processing YAML configuration..."
    
    # Check if YAML processor exists
    if [ -f "$PROJECT_DIR/yaml_processor.php" ]; then
        # Process using the actual YAML processor
        php "$PROJECT_DIR/yaml_processor.php" "$SCRIPT_DIR/$example_name.yaml" "$output_dir"
        echo "✅ Generated WordPress files in: $output_dir"
    else
        echo "⚠️  YAML processor not found, running demo instead..."
        php "$SCRIPT_DIR/run_examples.php"
    fi
    
    echo "📋 Files created:"
    if [ -d "$output_dir" ]; then
        ls -la "$output_dir"
    fi
    
    echo ""
}

# Check if specific example was requested
if [ $# -eq 1 ]; then
    case "$1" in
        "simple")
            process_example "simple_example" "Simple Single-Page Website"
            ;;
        "service")
            process_example "service_company" "Professional Service Company"
            ;;
        "restaurant")
            process_example "restaurant_example" "Restaurant Website"
            ;;
        *)
            echo "Unknown example: $1"
            echo "Available examples: simple, service, restaurant"
            echo "Or run without arguments to process all examples"
            exit 1
            ;;
    esac
else
    # Process all examples
    echo "Processing all examples..."
    echo ""
    
    process_example "simple_example" "Simple Single-Page Website"
    process_example "service_company" "Professional Service Company" 
    process_example "restaurant_example" "Restaurant Website"
    
    echo "=== All Examples Processed ==="
    echo ""
    echo "🎉 Demonstration complete!"
    echo ""
    echo "📖 What was demonstrated:"
    echo "   1. Simple example - Minimal configuration with basic sections"
    echo "   2. Service company - Complex business site with services, team, pricing"
    echo "   3. Restaurant - Completely different use case with menu, reservations"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Examine the generated files in examples/output/"
    echo "   2. Compare the YAML files to see configuration differences"
    echo "   3. Try creating your own YAML configuration"
    echo ""
    echo "💡 Commands to remember:"
    echo "   php yaml_processor.php your_file.yaml"
    echo "   ./process_example.sh simple"
    echo "   ./process_example.sh service"  
    echo "   ./process_example.sh restaurant"
fi