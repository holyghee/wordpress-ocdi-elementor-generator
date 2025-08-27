#!/bin/bash

# WordPress Import Test with Task Agent
# ======================================

echo "🚀 WordPress Import Test with Design Review"
echo "==========================================="
echo ""

# Configuration
WORDPRESS_DIR="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress"
TEST_SITE="http://localhost:8081"
ORIGINAL_SITE="http://localhost:8080"

# Step 1: Clean WordPress
echo "🧹 Cleaning WordPress..."
cd "$WORDPRESS_DIR"
./wordpress-cleanup.sh
echo ""

# Step 2: Ensure server is running
echo "🔄 Starting WordPress server..."
pkill -f "php -S localhost:8081" 2>/dev/null
sleep 1
php -S localhost:8081 server.php > /dev/null 2>&1 &
PHP_PID=$!
sleep 3
echo "✅ Server running on port 8081"
echo ""

# Step 3: Select test file
echo "📄 Available XML files for import:"
echo "1) demo_yaml_format.xml (Simple)"
echo "2) demo_widget_showcase.xml (All widgets)"  
echo "3) demo_customization.xml (Custom styles)"
echo "4) demo_performance_test.xml (Large)"
echo ""
read -p "Select file to test (1-4): " choice

case $choice in
    1) XML_FILE="demo_yaml_format.xml";;
    2) XML_FILE="demo_widget_showcase.xml";;
    3) XML_FILE="demo_customization.xml";;
    4) XML_FILE="demo_performance_test.xml";;
    *) XML_FILE="demo_yaml_format.xml";;
esac

echo "✅ Selected: $XML_FILE"
echo ""

# Step 4: Manual import instruction
echo "📤 MANUAL IMPORT REQUIRED:"
echo "================================"
echo "1. Open browser: $TEST_SITE/wp-admin"
echo "2. Login: admin / admin"
echo "3. Go to: Tools → Import → WordPress"
echo "4. Upload: $WORDPRESS_DIR/$XML_FILE"
echo "5. Click: Import"
echo ""
read -p "Press ENTER when import is complete..."
echo ""

# Step 5: Run design review with Task agent
echo "🎨 Running Design Review with Task Agent..."
echo "==========================================="

npx claude-flow@alpha task \
  --description "Design review of WordPress" \
  --subagent_type design-review \
  --prompt "Comprehensive design review of RIMAN WordPress site at $TEST_SITE.

Navigate to $TEST_SITE and analyze:

VISUAL INSPECTION:
1. Homepage loads correctly
2. All text is visible and readable
3. Images load from http://localhost:8082
4. Color scheme uses #b68c2f (gold) as primary
5. Navigation menu works
6. Responsive design (test mobile/tablet views)

COMPARE WITH ORIGINAL:
- Original Cholot theme: $ORIGINAL_SITE
- Does the structure match?
- Are widgets rendering correctly?

ELEMENTOR WIDGETS CHECK:
- cholot-title widgets
- cholot-texticon widgets  
- cholot-button widgets
- Gallery widgets
- Testimonial widgets

TECHNICAL ANALYSIS:
- Open browser console for errors
- Check network tab for failed resources
- Verify all URLs use localhost:8082 for images

PROVIDE SCORE (0-100) based on:
- 30 points: Visual correctness
- 30 points: Widget functionality
- 20 points: Responsive design
- 20 points: Technical (no errors)

OUTPUT FORMAT:
==================
SCORE: [number]/100
VISUAL: [Pass/Fail with details]
WIDGETS: [List of working/broken widgets]
RESPONSIVE: [Mobile/Tablet/Desktop status]
ERRORS: [List any console errors]
IMPROVEMENTS: [Specific actionable items]
SCREENSHOTS: [Take screenshots of issues]
==================" \
  2>&1 | tee design_review_result.txt

echo ""
echo "✅ Design review complete!"
echo ""

# Step 6: Parse and display results
echo "📊 RESULTS SUMMARY"
echo "=================="
if grep -q "SCORE:" design_review_result.txt 2>/dev/null; then
    grep "SCORE:" design_review_result.txt | head -1
    echo ""
    echo "Details saved in: design_review_result.txt"
else
    echo "Score parsing failed - check design_review_result.txt for full output"
fi

echo ""
echo "🔗 View site: $TEST_SITE"
echo ""

# Cleanup
cleanup() {
    echo "🧹 Shutting down server..."
    kill $PHP_PID 2>/dev/null
}

trap cleanup EXIT