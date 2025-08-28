#!/usr/bin/env python3
"""
Cholot XML Data Extractor and Analyzer
Comprehensive analysis of the original Cholot XML focusing on Elementor data structures
"""

import xml.etree.ElementTree as ET
import json
import os
import re
from collections import defaultdict
from datetime import datetime

class CholotXMLAnalyzer:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.tree = None
        self.root = None
        self.analysis = {
            'total_counts': {},
            'elementor_data': {},
            'custom_widgets': set(),
            'pages_with_elementor': [],
            'posts_with_elementor': [],
            'elementor_structures': {},
            'meta_data': {},
            'custom_post_types': set(),
            'taxonomies': {},
            'extraction_timestamp': datetime.now().isoformat()
        }
        
    def load_xml(self):
        """Load and parse the XML file"""
        try:
            self.tree = ET.parse(self.xml_path)
            self.root = self.tree.getroot()
            print(f"✅ Successfully loaded XML with root: {self.root.tag}")
            return True
        except Exception as e:
            print(f"❌ Error loading XML: {e}")
            return False
    
    def count_items(self):
        """Count all types of items in the XML"""
        print("\n🔍 Counting items...")
        
        # Find all items
        items = self.root.findall('.//item')
        
        counts = {
            'total_items': len(items),
            'pages': 0,
            'posts': 0,
            'attachments': 0,
            'nav_menu_items': 0,
            'elementor_library': 0,
            'custom_post_types': 0,
            'other': 0
        }
        
        post_types = defaultdict(int)
        
        for item in items:
            post_type = item.find('.//{http://wordpress.org/export/1.2/}post_type')
            if post_type is not None:
                pt = post_type.text
                post_types[pt] += 1
                
                if pt == 'page':
                    counts['pages'] += 1
                elif pt == 'post':
                    counts['posts'] += 1
                elif pt == 'attachment':
                    counts['attachments'] += 1
                elif pt == 'nav_menu_item':
                    counts['nav_menu_items'] += 1
                elif pt == 'elementor_library':
                    counts['elementor_library'] += 1
                elif pt in ['page', 'post', 'attachment', 'nav_menu_item', 'elementor_library']:
                    pass  # Already counted
                else:
                    counts['custom_post_types'] += 1
                    self.analysis['custom_post_types'].add(pt)
            else:
                counts['other'] += 1
        
        self.analysis['total_counts'] = counts
        self.analysis['post_type_breakdown'] = dict(post_types)
        
        print(f"📊 Total items: {counts['total_items']}")
        for key, value in counts.items():
            if key != 'total_items' and value > 0:
                print(f"   {key}: {value}")
    
    def extract_elementor_data(self):
        """Extract all Elementor-related data"""
        print("\n🎨 Extracting Elementor data...")
        
        items = self.root.findall('.//item')
        elementor_pages = []
        elementor_posts = []
        
        for item in items:
            # Get basic item info
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else 'Untitled'
            
            post_type_elem = item.find('.//{http://wordpress.org/export/1.2/}post_type')
            post_type = post_type_elem.text if post_type_elem is not None else 'unknown'
            
            post_id_elem = item.find('.//{http://wordpress.org/export/1.2/}post_id')
            post_id = post_id_elem.text if post_id_elem is not None else 'unknown'
            
            # Look for Elementor meta data
            meta_items = item.findall('.//{http://wordpress.org/export/1.2/}postmeta')
            elementor_data = {}
            has_elementor = False
            
            for meta in meta_items:
                meta_key_elem = meta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                meta_value_elem = meta.find('.//{http://wordpress.org/export/1.2/}meta_value')
                
                if meta_key_elem is not None and meta_value_elem is not None:
                    key = meta_key_elem.text
                    value = meta_value_elem.text
                    
                    # Capture all Elementor-related meta
                    if key and ('elementor' in key.lower() or key.startswith('_elementor')):
                        elementor_data[key] = value
                        has_elementor = True
                        
                        # Special handling for Elementor data
                        if key == '_elementor_data' and value:
                            try:
                                # Try to parse as JSON
                                parsed_data = json.loads(value)
                                elementor_data[f'{key}_parsed'] = parsed_data
                                
                                # Extract widget types
                                self.extract_widget_types(parsed_data)
                                
                            except json.JSONDecodeError:
                                # If not JSON, store as string
                                elementor_data[f'{key}_raw'] = value
            
            if has_elementor:
                item_info = {
                    'id': post_id,
                    'title': title,
                    'post_type': post_type,
                    'elementor_data': elementor_data
                }
                
                if post_type == 'page':
                    elementor_pages.append(item_info)
                    self.analysis['pages_with_elementor'].append(item_info)
                elif post_type == 'post':
                    elementor_posts.append(item_info)
                    self.analysis['posts_with_elementor'].append(item_info)
                
                # Store in elementor_structures for easy access
                self.analysis['elementor_structures'][f"{post_type}_{post_id}_{title}"] = elementor_data
        
        print(f"🎨 Found {len(elementor_pages)} pages with Elementor data")
        print(f"🎨 Found {len(elementor_posts)} posts with Elementor data")
        print(f"🧩 Found {len(self.analysis['custom_widgets'])} unique widget types")
    
    def extract_widget_types(self, data, path=""):
        """Recursively extract widget types from Elementor data"""
        if isinstance(data, dict):
            if 'widgetType' in data:
                widget_type = data['widgetType']
                self.analysis['custom_widgets'].add(widget_type)
                
                # Special attention to cholot-specific widgets
                if 'cholot' in widget_type.lower():
                    print(f"🎯 Found Cholot widget: {widget_type} at {path}")
            
            for key, value in data.items():
                self.extract_widget_types(value, f"{path}.{key}" if path else key)
                
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self.extract_widget_types(item, f"{path}[{i}]" if path else f"[{i}]")
    
    def extract_taxonomies(self):
        """Extract taxonomy information"""
        print("\n🏷️  Extracting taxonomies...")
        
        # Categories
        categories = self.root.findall('.//{http://wordpress.org/export/1.2/}category')
        self.analysis['taxonomies']['categories'] = []
        for cat in categories:
            cat_data = {}
            for child in cat:
                tag_name = child.tag.replace('{http://wordpress.org/export/1.2/}', 'wp:')
                cat_data[tag_name] = child.text
            self.analysis['taxonomies']['categories'].append(cat_data)
        
        # Tags
        tags = self.root.findall('.//{http://wordpress.org/export/1.2/}tag')
        self.analysis['taxonomies']['tags'] = []
        for tag in tags:
            tag_data = {}
            for child in tag:
                tag_name = child.tag.replace('{http://wordpress.org/export/1.2/}', 'wp:')
                tag_data[tag_name] = child.text
            self.analysis['taxonomies']['tags'].append(tag_data)
        
        # Terms (custom taxonomies)
        terms = self.root.findall('.//{http://wordpress.org/export/1.2/}term')
        self.analysis['taxonomies']['terms'] = []
        for term in terms:
            term_data = {}
            for child in term:
                tag_name = child.tag.replace('{http://wordpress.org/export/1.2/}', 'wp:')
                term_data[tag_name] = child.text
            self.analysis['taxonomies']['terms'].append(term_data)
        
        print(f"📂 Categories: {len(self.analysis['taxonomies']['categories'])}")
        print(f"🏷️  Tags: {len(self.analysis['taxonomies']['tags'])}")
        print(f"🔗 Terms: {len(self.analysis['taxonomies']['terms'])}")
    
    def save_elementor_structures(self):
        """Save individual Elementor structures to separate files"""
        print("\n💾 Saving Elementor structures...")
        
        # Create directory
        structures_dir = "elementor_structures"
        os.makedirs(structures_dir, exist_ok=True)
        
        for key, data in self.analysis['elementor_structures'].items():
            # Save each structure as a separate JSON file
            filename = f"{structures_dir}/{key.replace(' ', '_').replace('/', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📁 Saved {len(self.analysis['elementor_structures'])} Elementor structures to {structures_dir}/")
    
    def save_complete_analysis(self):
        """Save complete analysis to JSON file"""
        print("\n💾 Saving complete analysis...")
        
        # Convert sets to lists for JSON serialization
        analysis_copy = self.analysis.copy()
        analysis_copy['custom_widgets'] = list(self.analysis['custom_widgets'])
        analysis_copy['custom_post_types'] = list(self.analysis['custom_post_types'])
        
        with open('cholot_elementor_structures.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_copy, f, indent=2, ensure_ascii=False, default=str)
        
        print("✅ Saved complete analysis to cholot_elementor_structures.json")
    
    def generate_report(self):
        """Generate a detailed analysis report"""
        print("\n📝 Generating analysis report...")
        
        report = []
        report.append("CHOLOT XML ANALYSIS REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {self.analysis['extraction_timestamp']}")
        report.append(f"Source XML: {self.xml_path}")
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 20)
        counts = self.analysis['total_counts']
        for key, value in counts.items():
            report.append(f"{key:20}: {value}")
        report.append("")
        
        # Post Types
        report.append("POST TYPE BREAKDOWN")
        report.append("-" * 20)
        for pt, count in self.analysis['post_type_breakdown'].items():
            report.append(f"{pt:20}: {count}")
        report.append("")
        
        # Elementor Data
        report.append("ELEMENTOR DATA ANALYSIS")
        report.append("-" * 20)
        report.append(f"Pages with Elementor: {len(self.analysis['pages_with_elementor'])}")
        report.append(f"Posts with Elementor: {len(self.analysis['posts_with_elementor'])}")
        report.append(f"Total Elementor structures: {len(self.analysis['elementor_structures'])}")
        report.append("")
        
        # Widget Types
        report.append("ELEMENTOR WIDGET TYPES FOUND")
        report.append("-" * 20)
        for widget in sorted(self.analysis['custom_widgets']):
            report.append(f"  • {widget}")
        report.append("")
        
        # Cholot-specific widgets
        cholot_widgets = [w for w in self.analysis['custom_widgets'] if 'cholot' in w.lower()]
        if cholot_widgets:
            report.append("CHOLOT-SPECIFIC WIDGETS")
            report.append("-" * 20)
            for widget in sorted(cholot_widgets):
                report.append(f"  🎯 {widget}")
            report.append("")
        
        # Pages with Elementor
        if self.analysis['pages_with_elementor']:
            report.append("PAGES WITH ELEMENTOR DATA")
            report.append("-" * 20)
            for page in self.analysis['pages_with_elementor']:
                report.append(f"  • {page['title']} (ID: {page['id']})")
        
        # Taxonomies
        report.append("\nTAXONOMIES")
        report.append("-" * 20)
        tax = self.analysis['taxonomies']
        report.append(f"Categories: {len(tax.get('categories', []))}")
        report.append(f"Tags: {len(tax.get('tags', []))}")
        report.append(f"Custom Terms: {len(tax.get('terms', []))}")
        
        # Custom Post Types
        if self.analysis['custom_post_types']:
            report.append("\nCUSTOM POST TYPES")
            report.append("-" * 20)
            for cpt in sorted(self.analysis['custom_post_types']):
                report.append(f"  • {cpt}")
        
        report_text = "\n".join(report)
        
        with open('cholot_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print("✅ Saved analysis report to cholot_analysis_report.txt")
        return report_text
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 Starting Cholot XML Analysis...")
        
        if not self.load_xml():
            return False
        
        self.count_items()
        self.extract_elementor_data()
        self.extract_taxonomies()
        self.save_elementor_structures()
        self.save_complete_analysis()
        report = self.generate_report()
        
        print("\n🎉 Analysis Complete!")
        print("\nFiles created:")
        print("  📄 cholot_elementor_structures.json - Complete analysis data")
        print("  📁 elementor_structures/ - Individual Elementor data files")
        print("  📝 cholot_analysis_report.txt - Detailed analysis report")
        
        return True

def main():
    xml_path = "/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data.xml"
    
    if not os.path.exists(xml_path):
        print(f"❌ XML file not found: {xml_path}")
        return
    
    analyzer = CholotXMLAnalyzer(xml_path)
    success = analyzer.run_complete_analysis()
    
    if success:
        print("\n✨ Analysis data ready for the iterative generator!")
        
        # Display summary of findings
        print(f"\n🔍 KEY FINDINGS:")
        print(f"   Total items: {analyzer.analysis['total_counts']['total_items']}")
        print(f"   Pages: {analyzer.analysis['total_counts']['pages']}")
        print(f"   Posts: {analyzer.analysis['total_counts']['posts']}")
        print(f"   Elementor pages: {len(analyzer.analysis['pages_with_elementor'])}")
        print(f"   Widget types: {len(analyzer.analysis['custom_widgets'])}")
        
        # Show cholot-specific widgets
        cholot_widgets = [w for w in analyzer.analysis['custom_widgets'] if 'cholot' in w.lower()]
        if cholot_widgets:
            print(f"   🎯 Cholot widgets: {', '.join(cholot_widgets)}")

if __name__ == "__main__":
    main()