#!/bin/bash

# Iterative WordPress Import Testing with Design Review
# ======================================================
# This script orchestrates the full testing workflow with design review

echo "🚀 Starting Iterative WordPress Import Testing"
echo "=============================================="
echo ""

# Configuration
WORDPRESS_DIR="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress"
ORIGINAL_SITE="http://localhost:8080"
TEST_SITE="http://localhost:8081"
MAX_ITERATIONS=3
CURRENT_ITERATION=0

# Function to run cleanup
cleanup_wordpress() {
    echo "🧹 Cleaning WordPress..."
    cd "$WORDPRESS_DIR"
    ./wordpress-cleanup.sh
    echo "✅ WordPress cleaned"
    echo ""
}

# Function to ensure servers are running
ensure_servers() {
    echo "🔄 Checking servers..."
    
    # Check if image server is running on 8082
    if ! curl -s http://localhost:8082 > /dev/null; then
        echo "Starting image server on port 8082..."
        cd "$WORDPRESS_DIR/seo-images"
        python3 -m http.server 8082 &
        sleep 2
    fi
    
    # Check if original Cholot is on 8080
    if ! curl -s http://localhost:8080 > /dev/null; then
        echo "⚠️  Original Cholot site not running on port 8080"
        echo "   Please start it in another terminal"
    fi
    
    # Ensure test WordPress on 8081
    pkill -f "php -S localhost:8081" 2>/dev/null
    sleep 1
    cd "$WORDPRESS_DIR"
    php -S localhost:8081 server.php &
    PHP_PID=$!
    sleep 3
    
    echo "✅ Servers ready"
    echo ""
}

# Function to generate test XML
generate_xml() {
    local iteration=$1
    echo "🔧 Generating XML for iteration $iteration..."
    
    # Use the demo generator for now
    cd "$WORDPRESS_DIR"
    python3 demo_generator.py > /dev/null 2>&1
    
    # Select appropriate XML based on iteration
    case $iteration in
        1)
            XML_FILE="demo_yaml_format.xml"
            ;;
        2)
            XML_FILE="demo_widget_showcase.xml"
            ;;
        3)
            XML_FILE="demo_performance_test.xml"
            ;;
        *)
            XML_FILE="demo_customization.xml"
            ;;
    esac
    
    echo "✅ Using: $XML_FILE"
    echo ""
}

# Function to import XML using Playwright MCP
import_with_playwright() {
    local xml_file=$1
    echo "📤 Importing $xml_file using Playwright..."
    
    # Use Task agent with design-review type for import and analysis
    npx claude-flow@alpha agent \
        --type task-orchestrator \
        "Import the WordPress XML file $xml_file to $TEST_SITE. Steps: 1) Navigate to $TEST_SITE/wp-admin 2) Login with admin/admin 3) Go to Tools > Import 4) Upload $xml_file 5) Complete import wizard. Use Playwright MCP tools." \
        2>&1 | tee import_log_$CURRENT_ITERATION.txt
    
    echo ""
}

# Function to run design review
run_design_review() {
    local iteration=$1
    echo "🎨 Running Design Review Agent (Iteration $iteration)..."
    echo "================================================"
    
    # Launch the design review agent with specific checks
    npx claude-flow@alpha agent \
        --type design-review \
        "Comprehensive design review of RIMAN WordPress site at $TEST_SITE. 
        
        CRITICAL CHECKS:
        1. Compare with original Cholot at $ORIGINAL_SITE
        2. Verify all RIMAN content is properly displayed
        3. Check responsive design at mobile/tablet/desktop sizes
        4. Test Elementor widget rendering
        5. Validate color scheme (#b68c2f primary)
        6. Check image loading from http://localhost:8082
        7. Test navigation and internal links
        8. Verify animations and transitions
        9. Check for console errors
        10. Measure page load performance
        
        PROVIDE:
        - Quality score (0-100)
        - List of specific issues found
        - Actionable improvements for next iteration
        - Screenshots of problematic areas
        
        OUTPUT FORMAT:
        SCORE: [number]
        ISSUES: [bullet list]
        IMPROVEMENTS: [numbered list]
        " \
        2>&1 | tee review_log_$iteration.txt
    
    echo ""
    echo "✅ Design review completed for iteration $iteration"
    echo ""
}

# Function to parse review and decide on improvements
analyze_and_improve() {
    local review_file="review_log_$1.txt"
    echo "🔍 Analyzing review feedback..."
    
    # Extract score from review (simple grep, could be more sophisticated)
    SCORE=$(grep -i "SCORE:" "$review_file" | head -1 | grep -o '[0-9]\+' | head -1)
    
    if [ -z "$SCORE" ]; then
        SCORE=70  # Default if parsing fails
    fi
    
    echo "   Current quality score: $SCORE/100"
    
    if [ "$SCORE" -ge 90 ]; then
        echo "✅ Target quality achieved!"
        return 0
    else
        echo "📈 Score below target, preparing improvements..."
        
        # Extract improvements and prepare for next iteration
        grep -A10 "IMPROVEMENTS:" "$review_file" > improvements_$1.txt
        
        echo "   Improvements identified for next iteration"
        return 1
    fi
}

# Main test cycle
main() {
    echo "🏁 Initializing test environment..."
    echo ""
    
    # Setup
    ensure_servers
    
    # Run iterations
    for i in $(seq 1 $MAX_ITERATIONS); do
        CURRENT_ITERATION=$i
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📍 ITERATION $i of $MAX_ITERATIONS"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Step 1: Clean WordPress
        cleanup_wordpress
        
        # Step 2: Generate XML
        generate_xml $i
        
        # Step 3: Import XML
        import_with_playwright "$XML_FILE"
        
        # Wait for import to settle
        echo "⏳ Waiting for import to complete..."
        sleep 5
        
        # Step 4: Run design review
        run_design_review $i
        
        # Step 5: Analyze and decide
        if analyze_and_improve $i; then
            echo "🎉 Testing complete - quality target achieved!"
            break
        fi
        
        if [ $i -lt $MAX_ITERATIONS ]; then
            echo ""
            echo "🔄 Preparing for next iteration..."
            echo ""
            sleep 3
        fi
    done
    
    # Final summary
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 TESTING COMPLETE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Total iterations: $CURRENT_ITERATION"
    echo "Final score: $SCORE/100"
    echo ""
    echo "📁 Review logs saved:"
    ls -la review_log_*.txt 2>/dev/null
    echo ""
    echo "🔗 View results at: $TEST_SITE"
    echo ""
    
    # Option to run final manual review
    read -p "Run final design review? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npx claude-flow@alpha agent \
            --type design-review \
            "Final comprehensive review of RIMAN site at $TEST_SITE. Compare with $ORIGINAL_SITE and provide final assessment."
    fi
}

# Cleanup on exit
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    pkill -f "php -S localhost:8081" 2>/dev/null
    pkill -f "python3 -m http.server 8082" 2>/dev/null
}

trap cleanup EXIT

# Run the main function
main