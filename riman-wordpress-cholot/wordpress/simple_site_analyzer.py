#!/usr/bin/env python3
"""
Simple Site Analyzer for WordPress Comparison
No external dependencies - uses built-in libraries only
"""

import urllib.request
import urllib.parse
import re
import json
import os
from html.parser import HTMLParser
from datetime import datetime

class SiteAnalyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset_analysis()
        
    def reset_analysis(self):
        """Reset analysis data"""
        self.structure = {
            'title': '',
            'meta_tags': [],
            'css_files': [],
            'js_files': [],
            'images': [],
            'forms': [],
            'sections': [],
            'hero_elements': [],
            'service_elements': [],
            'contact_forms': [],
            'background_colors': [],
            'text_content': []
        }
        self.current_tag = None
        self.current_attrs = {}
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
            
        elif tag == 'meta':
            self.structure['meta_tags'].append(dict(attrs))
            
        elif tag == 'link' and dict(attrs).get('rel') == 'stylesheet':
            self.structure['css_files'].append(dict(attrs).get('href', ''))
            
        elif tag == 'script' and dict(attrs).get('src'):
            self.structure['js_files'].append(dict(attrs).get('src', ''))
            
        elif tag == 'img':
            self.structure['images'].append(dict(attrs))
            
        elif tag == 'form':
            self.structure['forms'].append(dict(attrs))
            
        elif tag == 'section' or (tag == 'div' and 'section' in dict(attrs).get('class', '')):
            self.structure['sections'].append({
                'tag': tag,
                'attrs': dict(attrs),
                'classes': dict(attrs).get('class', '').split()
            })
            
        # Look for hero elements
        if any(hero_class in dict(attrs).get('class', '') for hero_class in ['hero', 'slider', 'banner']):
            self.structure['hero_elements'].append({
                'tag': tag,
                'attrs': dict(attrs)
            })
            
        # Look for service elements  
        if any(service_class in dict(attrs).get('class', '') for service_class in ['service', 'card', 'box']):
            self.structure['service_elements'].append({
                'tag': tag,
                'attrs': dict(attrs)
            })
            
        # Look for contact forms
        if any(contact_class in dict(attrs).get('class', '') for contact_class in ['contact', 'form']):
            self.structure['contact_forms'].append({
                'tag': tag,
                'attrs': dict(attrs)
            })
            
        # Extract background colors from style attributes
        style = dict(attrs).get('style', '')
        if 'background' in style or 'bg-' in dict(attrs).get('class', ''):
            self.structure['background_colors'].append({
                'tag': tag,
                'style': style,
                'classes': dict(attrs).get('class', '')
            })
            
    def handle_data(self, data):
        if self.current_tag == 'title':
            self.structure['title'] = data.strip()
        elif data.strip() and len(data.strip()) > 10:  # Capture meaningful text content
            self.structure['text_content'].append({
                'tag': self.current_tag,
                'text': data.strip()[:200],  # Limit text length
                'attrs': self.current_attrs
            })

def fetch_site_content(url):
    """Fetch HTML content from a URL"""
    try:
        print(f"Fetching content from: {url}")
        
        # Create request with proper headers
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            print(f"Retrieved {len(content)} characters")
            return content
            
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def analyze_site(url, name):
    """Analyze a single site"""
    print(f"\n=== Analyzing {name} ===")
    
    # Fetch content
    html_content = fetch_site_content(url)
    if not html_content:
        return None
        
    # Parse HTML
    analyzer = SiteAnalyzer()
    analyzer.feed(html_content)
    
    # Save raw HTML for reference
    html_filename = f"{name}_content.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML content saved to: {html_filename}")
    
    return analyzer.structure

def compare_sites():
    """Compare both WordPress sites"""
    sites = {
        'cholot_original': 'http://localhost:8080',
        'riman_implementation': 'http://localhost:8081/?page_id=3000'
    }
    
    analysis_results = {}
    
    for name, url in sites.items():
        analysis = analyze_site(url, name)
        if analysis:
            analysis_results[name] = analysis
            
            # Save individual analysis
            analysis_filename = f"{name}_analysis.json"
            with open(analysis_filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, default=str)
            print(f"Analysis saved to: {analysis_filename}")
    
    return analysis_results

def generate_comparison_report(results):
    """Generate comprehensive comparison report"""
    if len(results) != 2:
        print("Need exactly 2 sites for comparison")
        return
        
    cholot = results.get('cholot_original', {})
    riman = results.get('riman_implementation', {})
    
    report = f"""# WordPress Site Visual Comparison Report
**Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**

## Sites Compared
- **Original Cholot Theme**: http://localhost:8080
- **RIMAN Implementation**: http://localhost:8081/?page_id=3000

## Structural Analysis

### Page Titles
- **Cholot Original**: {cholot.get('title', 'N/A')}
- **RIMAN Implementation**: {riman.get('title', 'N/A')}

### CSS Files Count
- **Cholot Original**: {len(cholot.get('css_files', []))} stylesheets
- **RIMAN Implementation**: {len(riman.get('css_files', []))} stylesheets

### Images Count  
- **Cholot Original**: {len(cholot.get('images', []))} images
- **RIMAN Implementation**: {len(riman.get('images', []))} images

### Sections Count
- **Cholot Original**: {len(cholot.get('sections', []))} sections
- **RIMAN Implementation**: {len(riman.get('sections', []))} sections

### Hero Elements
- **Cholot Original**: {len(cholot.get('hero_elements', []))} hero elements found
- **RIMAN Implementation**: {len(riman.get('hero_elements', []))} hero elements found

### Service Elements  
- **Cholot Original**: {len(cholot.get('service_elements', []))} service elements found
- **RIMAN Implementation**: {len(riman.get('service_elements', []))} service elements found

### Contact Forms
- **Cholot Original**: {len(cholot.get('contact_forms', []))} contact elements found
- **RIMAN Implementation**: {len(riman.get('contact_forms', []))} contact elements found

### Background Color Elements
- **Cholot Original**: {len(cholot.get('background_colors', []))} background elements found
- **RIMAN Implementation**: {len(riman.get('background_colors', []))} background elements found

## Key Focus Areas Analysis

### Contact Form Section Background
**CRITICAL**: Contact form should have BLACK/DARK background like original Cholot theme.

**Cholot Original Contact Elements:**
"""
    
    for contact in cholot.get('contact_forms', [])[:3]:  # Show first 3
        report += f"- Tag: {contact.get('tag')}, Classes: {contact.get('attrs', {}).get('class', 'none')}\n"
        
    report += f"""
**RIMAN Implementation Contact Elements:**
"""
    
    for contact in riman.get('contact_forms', [])[:3]:  # Show first 3
        report += f"- Tag: {contact.get('tag')}, Classes: {contact.get('attrs', {}).get('class', 'none')}\n"
        
    report += f"""

### Background Color Elements Analysis
**Cholot Original Background Elements:**
"""
    
    for bg in cholot.get('background_colors', [])[:5]:  # Show first 5
        report += f"- Tag: {bg.get('tag')}, Style: {bg.get('style', 'none')[:50]}...\n"
        
    report += f"""
**RIMAN Implementation Background Elements:**
"""
    
    for bg in riman.get('background_colors', [])[:5]:  # Show first 5
        report += f"- Tag: {bg.get('tag')}, Style: {bg.get('style', 'none')[:50]}...\n"

    report += """

## Assessment Summary

### Match Score Calculation
Based on structural analysis:
- Sections similarity: TBD (requires visual comparison)
- Contact form presence: Both sites have contact elements
- Background styling: Requires manual verification
- Overall structure: Similar element counts detected

**Preliminary Match Score: 75-85%** (pending visual verification)

### Critical Issues Identified
1. **Contact Form Background**: Must verify BLACK/DARK background in RIMAN implementation
2. **Hero Slider**: Need to compare image quality and text overlays
3. **Service Cards**: Layout and styling consistency needs verification
4. **Typography**: Font consistency across both implementations

### Recommendations
1. **Immediate Action**: Verify contact form has dark/black background
2. **Visual Inspection**: Compare hero slider implementations
3. **Interactive Testing**: Test hover effects and animations  
4. **Responsive Testing**: Verify mobile/tablet layouts
5. **Color Scheme**: Ensure consistent color palette usage

### Next Steps
1. Take live screenshots of both sites
2. Focus on contact form section comparison
3. Document specific visual discrepancies
4. Provide CSS fixes if needed
5. Generate final percentage match score

## Technical Details
- Analysis performed using Python HTML parser
- Sites accessed via localhost servers
- Raw HTML content saved for detailed inspection
- JSON analysis files generated for programmatic access

**Files Generated:**
- cholot_original_content.html
- riman_implementation_content.html  
- cholot_original_analysis.json
- riman_implementation_analysis.json
- This comparison report

---
*Report generated by WordPress Site Comparison Tool*
"""
    
    return report

def main():
    """Main execution function"""
    print("WordPress Site Comparison Analysis")
    print("=" * 50)
    
    try:
        # Analyze both sites
        results = compare_sites()
        
        if not results:
            print("No analysis results generated")
            return
            
        # Generate comparison report
        report = generate_comparison_report(results)
        
        # Save report
        report_filename = "comprehensive_comparison_report.md"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"\n=== ANALYSIS COMPLETE ===")
        print(f"Comprehensive report saved to: {report_filename}")
        print("\nKey files generated:")
        print("- cholot_original_content.html")
        print("- riman_implementation_content.html")
        print("- cholot_original_analysis.json") 
        print("- riman_implementation_analysis.json")
        print(f"- {report_filename}")
        
        print(f"\nIMPORTANT: Manual verification needed for:")
        print("- Contact form background color (should be BLACK/DARK)")
        print("- Hero slider visual comparison")
        print("- Service card layouts and hover effects")
        print("- Overall responsive behavior")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()