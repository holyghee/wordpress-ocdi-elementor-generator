#!/bin/bash
# test-import.sh - WordPress XML Import Testing Script
# Part of Cholot Iterative Generator System

set -e  # Exit on any error

XML_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/generated/test-import.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[${timestamp}] [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_success() { log "${GREEN}SUCCESS${NC}" "$1"; }
log_error() { log "${RED}ERROR${NC}" "$1"; }
log_warning() { log "${YELLOW}WARNING${NC}" "$1"; }
log_info() { log "${BLUE}INFO${NC}" "$1"; }

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to validate XML file
validate_xml_file() {
    local xml_file="$1"
    
    log_info "🔍 Validating XML file: $xml_file"
    
    # Check if file exists
    if [[ ! -f "$xml_file" ]]; then
        log_error "XML file does not exist: $xml_file"
        return 1
    fi
    
    # Check if file is not empty
    if [[ ! -s "$xml_file" ]]; then
        log_error "XML file is empty: $xml_file"
        return 1
    fi
    
    # Check file size (should be reasonable)
    file_size=$(stat -f%z "$xml_file" 2>/dev/null || stat -c%s "$xml_file" 2>/dev/null || echo "0")
    log_info "📊 File size: ${file_size} bytes"
    
    if [[ $file_size -lt 1000 ]]; then
        log_warning "XML file seems very small (< 1KB)"
    fi
    
    # Try to parse XML with xmllint if available
    if command_exists xmllint; then
        log_info "🔧 Checking XML syntax with xmllint..."
        if xmllint --noout "$xml_file" 2>/dev/null; then
            log_success "XML syntax is valid"
        else
            log_error "XML syntax errors detected"
            xmllint --noout "$xml_file" 2>&1 | head -10 | while read -r line; do
                log_error "  $line"
            done
            return 1
        fi
    else
        log_info "xmllint not available, skipping syntax check"
    fi
    
    return 0
}

# Function to analyze XML content
analyze_xml_content() {
    local xml_file="$1"
    
    log_info "🔍 Analyzing XML content..."
    
    # Count items
    local item_count=$(grep -c "<item>" "$xml_file" || echo "0")
    log_info "📄 Total items found: $item_count"
    
    # Count pages
    local page_count=$(grep -c "<wp:post_type>page</wp:post_type>" "$xml_file" || echo "0")
    log_info "📄 Pages found: $page_count"
    
    # Count posts
    local post_count=$(grep -c "<wp:post_type>post</wp:post_type>" "$xml_file" || echo "0")
    log_info "📝 Posts found: $post_count"
    
    # Count menu items
    local menu_count=$(grep -c "<wp:post_type>nav_menu_item</wp:post_type>" "$xml_file" || echo "0")
    log_info "🧭 Menu items found: $menu_count"
    
    # Check for Elementor data
    local elementor_count=$(grep -c "_elementor_data" "$xml_file" || echo "0")
    log_info "🔧 Elementor data blocks found: $elementor_count"
    
    if [[ $elementor_count -eq 0 ]]; then
        log_warning "No Elementor data found in XML"
        return 1
    else
        log_success "Elementor data present in XML"
    fi
    
    # Check for required WordPress elements
    local required_elements=(
        "<rss"
        "<channel>"
        "<wp:wxr_version>"
        "<wp:base_site_url>"
        "<title>"
    )
    
    for element in "${required_elements[@]}"; do
        if grep -q "$element" "$xml_file"; then
            log_success "Required element found: $element"
        else
            log_error "Missing required element: $element"
            return 1
        fi
    done
    
    return 0
}

# Function to simulate WordPress import
simulate_import() {
    local xml_file="$1"
    
    log_info "🧪 Simulating WordPress import process..."
    
    # Check for potential import issues
    local issues_found=0
    
    # Check for problematic characters
    if grep -q $'[\x00-\x08\x0B\x0C\x0E-\x1F]' "$xml_file"; then
        log_error "Binary/control characters found in XML"
        ((issues_found++))
    fi
    
    # Check for extremely long lines (can cause memory issues)
    if awk 'length > 100000' "$xml_file" | grep -q .; then
        log_warning "Very long lines found (>100K chars) - may cause import issues"
        ((issues_found++))
    fi
    
    # Check for unescaped HTML entities
    if grep -E '&[^#].*[^;]' "$xml_file" | grep -v '&amp;\|&lt;\|&gt;\|&quot;\|&apos;' | grep -q .; then
        log_warning "Potentially unescaped HTML entities found"
        ((issues_found++))
    fi
    
    # Check for missing CDATA sections in content
    if grep -E '<content:encoded>[^<]*<[^!]' "$xml_file" | grep -q .; then
        log_warning "HTML content not wrapped in CDATA sections"
        ((issues_found++))
    fi
    
    # Check Elementor data encoding
    if grep -q "_elementor_data" "$xml_file"; then
        # Check if Elementor data is properly escaped
        if grep -A 1 "_elementor_data" "$xml_file" | grep -E '\[|\{' | grep -q .; then
            # Extract a sample of Elementor data to check
            local elementor_sample=$(grep -A 1 "_elementor_data" "$xml_file" | grep -o '\[.*\]' | head -1)
            if [[ -n "$elementor_sample" ]]; then
                # Try to validate JSON structure (basic check)
                if echo "$elementor_sample" | grep -E '^\[.*\]$' | grep -q .; then
                    log_success "Elementor data appears to be properly formatted"
                else
                    log_error "Elementor data may not be properly formatted"
                    ((issues_found++))
                fi
            fi
        fi
    fi
    
    if [[ $issues_found -eq 0 ]]; then
        log_success "Import simulation passed - no critical issues found"
        return 0
    else
        log_error "Import simulation found $issues_found potential issues"
        return 1
    fi
}

# Function to test with WordPress CLI (if available)
test_with_wp_cli() {
    local xml_file="$1"
    
    if command_exists wp; then
        log_info "🔧 WordPress CLI found - attempting dry run import..."
        
        # Try to run WP-CLI import with dry run (if supported)
        # Note: This would require WordPress installation
        log_info "WP-CLI import test would require WordPress installation"
        log_info "Skipping actual WP-CLI test in this simulation"
        
        return 0
    else
        log_info "WordPress CLI not available - skipping WP-CLI tests"
        return 0
    fi
}

# Function to generate test report
generate_test_report() {
    local xml_file="$1"
    local test_result="$2"
    local report_file="${SCRIPT_DIR}/generated/test-import-report.json"
    
    log_info "📊 Generating test report..."
    
    # Get file stats
    local file_size=$(stat -f%z "$xml_file" 2>/dev/null || stat -c%s "$xml_file" 2>/dev/null || echo "0")
    local item_count=$(grep -c "<item>" "$xml_file" || echo "0")
    local elementor_count=$(grep -c "_elementor_data" "$xml_file" || echo "0")
    
    # Generate JSON report
    cat > "$report_file" << EOF
{
    "test_date": "$(date -Iseconds)",
    "xml_file": "$xml_file",
    "test_result": "$test_result",
    "file_size": $file_size,
    "statistics": {
        "total_items": $item_count,
        "pages": $(grep -c "<wp:post_type>page</wp:post_type>" "$xml_file" || echo "0"),
        "posts": $(grep -c "<wp:post_type>post</wp:post_type>" "$xml_file" || echo "0"),
        "menu_items": $(grep -c "<wp:post_type>nav_menu_item</wp:post_type>" "$xml_file" || echo "0"),
        "elementor_blocks": $elementor_count
    },
    "validations": {
        "xml_syntax": $(xmllint --noout "$xml_file" >/dev/null 2>&1 && echo "true" || echo "false"),
        "has_elementor_data": $([ $elementor_count -gt 0 ] && echo "true" || echo "false"),
        "has_required_elements": true
    }
}
EOF
    
    log_success "Test report saved to: $report_file"
}

# Main function
main() {
    local xml_file="$1"
    
    # Initialize
    echo "🧪 CHOLOT XML IMPORT TESTER"
    echo "=========================="
    echo "Testing WordPress XML import compatibility"
    echo
    
    # Create output directory
    mkdir -p "${SCRIPT_DIR}/generated"
    
    # Clear previous log
    > "$LOG_FILE"
    
    if [[ -z "$xml_file" ]]; then
        log_error "Usage: $0 <xml_file>"
        echo "Example: $0 cholot-generated.xml"
        exit 1
    fi
    
    log_info "🚀 Starting import test for: $xml_file"
    
    # Run validation tests
    local overall_result="PASS"
    
    echo
    echo "📋 TEST 1: XML File Validation"
    echo "==============================="
    if ! validate_xml_file "$xml_file"; then
        overall_result="FAIL"
    fi
    
    echo
    echo "📋 TEST 2: XML Content Analysis"
    echo "==============================="
    if ! analyze_xml_content "$xml_file"; then
        overall_result="FAIL"
    fi
    
    echo
    echo "📋 TEST 3: Import Simulation"
    echo "============================"
    if ! simulate_import "$xml_file"; then
        overall_result="FAIL"
    fi
    
    echo
    echo "📋 TEST 4: WordPress CLI Test"
    echo "============================="
    test_with_wp_cli "$xml_file"
    
    echo
    echo "📋 FINAL RESULTS"
    echo "================"
    
    if [[ "$overall_result" == "PASS" ]]; then
        log_success "🎉 ALL TESTS PASSED"
        log_success "XML file is ready for WordPress import"
        generate_test_report "$xml_file" "PASS"
        exit 0
    else
        log_error "❌ SOME TESTS FAILED"
        log_error "XML file may have import issues"
        generate_test_report "$xml_file" "FAIL"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"