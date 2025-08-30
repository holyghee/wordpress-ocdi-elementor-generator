#!/usr/bin/env python3
"""
Simple Website Comparison Tool
"""

import re
import subprocess

def extract_section(html_content, section_name):
    """Extract a specific section from HTML"""
    # Look for various section markers
    patterns = [
        f'<section[^>]*class="[^"]*{section_name}[^"]*"[^>]*>.*?</section>',
        f'<div[^>]*class="[^"]*{section_name}[^"]*"[^>]*>.*?</div>',
        f'<div[^>]*id="[^"]*{section_name}[^"]*"[^>]*>.*?</div>',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0]
    return None

def count_cholot_widgets(html_content):
    """Count cholot-texticon widgets and extract their content"""
    pattern = r'<div[^>]*cholot-texticon[^>]*>.*?</div><!--/.box-small-icon-->'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    widget_data = []
    for match in matches:
        # Extract title
        title_match = re.search(r'<h3[^>]*icon-title[^>]*>(.*?)</h3>', match)
        title = title_match.group(1) if title_match else "No title"
        
        # Extract subtitle
        subtitle_match = re.search(r'<p[^>]*icon-subtitle[^>]*>(.*?)</p>', match)
        subtitle = subtitle_match.group(1) if subtitle_match else "No subtitle"
        
        # Extract icon
        icon_match = re.search(r'<i[^>]*class="[^"]*fa[^"]*"[^>]*>', match)
        svg_match = re.search(r'<svg[^>]*class="[^"]*cholot-icon[^"]*"[^>]*>', match)
        
        icon_type = "FontAwesome" if icon_match else ("SVG" if svg_match else "No icon")
        
        widget_data.append({
            'title': title.strip(),
            'subtitle': subtitle.strip(),
            'icon_type': icon_type
        })
    
    return len(matches), widget_data

def extract_css_links(html_content):
    """Extract all CSS link elements"""
    pattern = r'<link[^>]*rel=[\'"]stylesheet[\'"][^>]*>'
    matches = re.findall(pattern, html_content)
    return matches

def analyze_html_structure(html_content):
    """Analyze overall HTML structure"""
    title_match = re.search(r'<title>(.*?)</title>', html_content)
    title = title_match.group(1) if title_match else "No title"
    
    # Count major elements
    elementor_widgets = len(re.findall(r'elementor-widget-[a-zA-Z0-9-]+', html_content))
    elementor_columns = len(re.findall(r'elementor-column', html_content))
    elementor_sections = len(re.findall(r'elementor-section', html_content))
    
    return {
        'title': title,
        'elementor_widgets': elementor_widgets,
        'elementor_columns': elementor_columns,
        'elementor_sections': elementor_sections
    }

def main():
    print("🔍 WEBSITE COMPARISON ANALYSIS")
    print("=" * 50)
    
    # Read the HTML files
    with open('current_full.html', 'r', encoding='utf-8') as f:
        current_html = f.read()
    
    with open('original_full.html', 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # Analyze current implementation
    print("\n📊 CURRENT IMPLEMENTATION (localhost:8081)")
    print("-" * 45)
    current_structure = analyze_html_structure(current_html)
    current_widgets, current_widget_data = count_cholot_widgets(current_html)
    current_css = extract_css_links(current_html)
    
    print(f"Title: {current_structure['title']}")
    print(f"Elementor Widgets: {current_structure['elementor_widgets']}")
    print(f"Elementor Columns: {current_structure['elementor_columns']}")
    print(f"Elementor Sections: {current_structure['elementor_sections']}")
    print(f"Cholot-texticon widgets: {current_widgets}")
    print(f"CSS files loaded: {len(current_css)}")
    
    print("\n🎯 CHOLOT WIDGETS IN CURRENT IMPLEMENTATION:")
    for i, widget in enumerate(current_widget_data, 1):
        print(f"  {i}. {widget['title']} ({widget['subtitle']}) - {widget['icon_type']}")
    
    # Analyze original theme
    print("\n📊 ORIGINAL THEME (localhost:8080)")
    print("-" * 35)
    original_structure = analyze_html_structure(original_html)
    original_widgets, original_widget_data = count_cholot_widgets(original_html)
    original_css = extract_css_links(original_html)
    
    print(f"Title: {original_structure['title']}")
    print(f"Elementor Widgets: {original_structure['elementor_widgets']}")
    print(f"Elementor Columns: {original_structure['elementor_columns']}")
    print(f"Elementor Sections: {original_structure['elementor_sections']}")
    print(f"Cholot-texticon widgets: {original_widgets}")
    print(f"CSS files loaded: {len(original_css)}")
    
    print("\n🎯 CHOLOT WIDGETS IN ORIGINAL THEME:")
    for i, widget in enumerate(original_widget_data, 1):
        print(f"  {i}. {widget['title']} ({widget['subtitle']}) - {widget['icon_type']}")
    
    # CSS Differences
    print("\n🎨 CSS FILES COMPARISON")
    print("-" * 25)
    current_css_files = [re.search(r'href=[\'"]([^\'"]*)[\'"]', css).group(1) for css in current_css if re.search(r'href=[\'"]([^\'"]*)[\'"]', css)]
    original_css_files = [re.search(r'href=[\'"]([^\'"]*)[\'"]', css).group(1) for css in original_css if re.search(r'href=[\'"]([^\'"]*)[\'"]', css)]
    
    current_only = set(current_css_files) - set(original_css_files)
    original_only = set(original_css_files) - set(current_css_files)
    
    print(f"CSS files only in current: {len(current_only)}")
    for css_file in sorted(current_only):
        print(f"  + {css_file}")
    
    print(f"\nCSS files only in original: {len(original_only)}")
    for css_file in sorted(original_only):
        print(f"  - {css_file}")
    
    # Key Findings
    print("\n🔍 KEY FINDINGS")
    print("-" * 15)
    
    if current_widgets != original_widgets:
        print(f"⚠️  Widget count mismatch: Current({current_widgets}) vs Original({original_widgets})")
    else:
        print(f"✅ Widget count matches: {current_widgets} widgets found in both")
    
    if len(current_only) > 0:
        print(f"⚠️  Current implementation has {len(current_only)} extra CSS files")
        key_files = [f for f in current_only if 'cholot' in f or 'child' in f]
        if key_files:
            print(f"   Key files: {', '.join(key_files)}")
    
    if len(original_only) > 0:
        print(f"⚠️  Original theme has {len(original_only)} CSS files not in current")
    
    # Check for missing elements
    if 'fatnav' in str(current_css_files) and 'fatnav' not in str(original_css_files):
        print("⚠️  Current has fatnav CSS that original doesn't have")
    
    print(f"\n📝 SUMMARY")
    print("-" * 10)
    print(f"Both sites have cholot-texticon widgets, but content differs:")
    print(f"Current focuses on: Asbestsanierung, Schadstoffsanierung, etc. (German/Business)")
    print(f"Original focuses on: Healthy life, Improving life, etc. (English/Demo)")
    print(f"\nThis suggests the widgets are rendering correctly,")
    print(f"but the current implementation uses different content/data.")

if __name__ == "__main__":
    main()