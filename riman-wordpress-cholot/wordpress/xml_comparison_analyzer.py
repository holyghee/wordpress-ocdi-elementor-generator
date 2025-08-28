#!/usr/bin/env python3
"""
XML Comparison Analyzer - Analyze differences between target and generated XML
"""

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict

class XMLComparisonAnalyzer:
    def __init__(self, target_path: str, generated_path: str):
        self.target_path = target_path
        self.generated_path = generated_path
        self.differences = []
        self.target_items = {}
        self.generated_items = {}
        
    def analyze(self) -> Dict:
        """Analyze differences between target and generated XML"""
        print("🔍 XML Comparison Analyzer")
        print("=" * 60)
        
        # Load and extract items from both files
        self.extract_target_items()
        self.extract_generated_items()
        
        # Compare basic stats
        target_count = len(self.target_items)
        generated_count = len(self.generated_items)
        
        print(f"📊 Target XML items: {target_count}")
        print(f"📊 Generated XML items: {generated_count}")
        
        if target_count == generated_count:
            print("✅ Item counts match!")
        else:
            print(f"❌ Item count mismatch! Difference: {generated_count - target_count}")
            
        # Compare individual items
        self.compare_items()
        
        # Generate comparison report
        return self.generate_report()
    
    def extract_target_items(self):
        """Extract items from target XML"""
        print("📖 Reading target XML...")
        
        with open(self.target_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract items using regex since the XML might have formatting issues
        item_pattern = r'<item>.*?</item>'
        items = re.findall(item_pattern, content, re.DOTALL)
        
        for item in items:
            # Extract post_id
            id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            if id_match:
                post_id = int(id_match.group(1))
                
                # Extract post_type
                type_match = re.search(r'<wp:post_type>([^<]+)</wp:post_type>', item)
                post_type = type_match.group(1) if type_match else 'unknown'
                
                # Extract title
                title_match = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
                title = title_match.group(1) if title_match else 'No title'
                
                self.target_items[post_id] = {
                    'type': post_type,
                    'title': title,
                    'xml': item
                }
        
        print(f"✅ Extracted {len(self.target_items)} items from target")
    
    def extract_generated_items(self):
        """Extract items from generated XML"""
        print("📖 Reading generated XML...")
        
        with open(self.generated_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract items using regex
        item_pattern = r'<item>.*?</item>'
        items = re.findall(item_pattern, content, re.DOTALL)
        
        for item in items:
            # Extract post_id (with namespace prefix)
            id_match = re.search(r'<(?:ns0:)?post_id>(\d+)</(?:ns0:)?post_id>', item)
            if id_match:
                post_id = int(id_match.group(1))
                
                # Extract post_type
                type_match = re.search(r'<(?:ns0:)?post_type>([^<]+)</(?:ns0:)?post_type>', item)
                post_type = type_match.group(1) if type_match else 'unknown'
                
                # Extract title
                title_match = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
                title = title_match.group(1) if title_match else 'No title'
                
                self.generated_items[post_id] = {
                    'type': post_type,
                    'title': title,
                    'xml': item
                }
        
        print(f"✅ Extracted {len(self.generated_items)} items from generated")
    
    def compare_items(self):
        """Compare items between target and generated"""
        print("🔍 Comparing items...")
        
        # Check for missing items in generated
        missing_in_generated = set(self.target_items.keys()) - set(self.generated_items.keys())
        if missing_in_generated:
            print(f"❌ Missing in generated: {sorted(missing_in_generated)}")
            for item_id in missing_in_generated:
                self.differences.append({
                    'type': 'missing_in_generated',
                    'id': item_id,
                    'target_title': self.target_items[item_id]['title'],
                    'target_type': self.target_items[item_id]['type']
                })
        
        # Check for extra items in generated
        extra_in_generated = set(self.generated_items.keys()) - set(self.target_items.keys())
        if extra_in_generated:
            print(f"❌ Extra in generated: {sorted(extra_in_generated)}")
            for item_id in extra_in_generated:
                self.differences.append({
                    'type': 'extra_in_generated',
                    'id': item_id,
                    'generated_title': self.generated_items[item_id]['title'],
                    'generated_type': self.generated_items[item_id]['type']
                })
        
        # Compare common items
        common_items = set(self.target_items.keys()) & set(self.generated_items.keys())
        print(f"✅ Common items: {len(common_items)}")
        
        type_mismatches = []
        title_mismatches = []
        
        for item_id in common_items:
            target = self.target_items[item_id]
            generated = self.generated_items[item_id]
            
            # Compare types
            if target['type'] != generated['type']:
                type_mismatches.append((item_id, target['type'], generated['type']))
                
            # Compare titles
            if target['title'] != generated['title']:
                title_mismatches.append((item_id, target['title'], generated['title']))
        
        if type_mismatches:
            print(f"❌ Type mismatches: {len(type_mismatches)}")
            for item_id, target_type, generated_type in type_mismatches:
                print(f"   ID {item_id}: '{target_type}' -> '{generated_type}'")
                
        if title_mismatches:
            print(f"❌ Title mismatches: {len(title_mismatches)}")
            for item_id, target_title, generated_title in title_mismatches:
                print(f"   ID {item_id}: '{target_title}' -> '{generated_title}'")
                
    def generate_report(self) -> Dict:
        """Generate detailed comparison report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'target_file': self.target_path,
            'generated_file': self.generated_path,
            'summary': {
                'target_items': len(self.target_items),
                'generated_items': len(self.generated_items),
                'items_match': len(self.target_items) == len(self.generated_items),
                'differences_count': len(self.differences)
            },
            'target_by_type': {},
            'generated_by_type': {},
            'differences': self.differences
        }
        
        # Count by type
        for item in self.target_items.values():
            item_type = item['type']
            report['target_by_type'][item_type] = report['target_by_type'].get(item_type, 0) + 1
            
        for item in self.generated_items.values():
            item_type = item['type']
            report['generated_by_type'][item_type] = report['generated_by_type'].get(item_type, 0) + 1
        
        # Print summary
        print("\n📋 SUMMARY:")
        print(f"Target Items: {report['summary']['target_items']}")
        print(f"Generated Items: {report['summary']['generated_items']}")
        print(f"Items Match: {report['summary']['items_match']}")
        print(f"Differences: {report['summary']['differences_count']}")
        
        print("\n📊 BREAKDOWN BY TYPE:")
        print("Target:")
        for item_type, count in sorted(report['target_by_type'].items()):
            print(f"  {item_type}: {count}")
            
        print("Generated:")
        for item_type, count in sorted(report['generated_by_type'].items()):
            print(f"  {item_type}: {count}")
        
        return report

def main():
    """Main function"""
    import sys
    import json
    
    if len(sys.argv) != 3:
        print("Usage: python xml_comparison_analyzer.py target.xml generated.xml")
        sys.exit(1)
    
    analyzer = XMLComparisonAnalyzer(sys.argv[1], sys.argv[2])
    report = analyzer.analyze()
    
    # Save report
    with open('comparison-report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Detailed report saved to: comparison-report.json")

if __name__ == "__main__":
    main()