#!/usr/bin/env python3
"""
compare-xml.py - XML Comparison and Analysis Script
Part of Cholot Iterative Generator System

This script compares generated XML with original/reference XML files to:
1. Identify structural differences
2. Compare content completeness
3. Validate data transformation accuracy
4. Report missing or incorrect elements
"""

import sys
import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Tuple, Set
from datetime import datetime
import difflib
import re

class XMLComparator:
    def __init__(self, reference_xml: str, generated_xml: str):
        self.reference_xml = reference_xml
        self.generated_xml = generated_xml
        self.comparison_results = {
            "reference_stats": {},
            "generated_stats": {},
            "differences": [],
            "missing_elements": [],
            "extra_elements": [],
            "content_matches": [],
            "content_differences": [],
            "overall_score": 0.0
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def parse_xml_stats(self, xml_file: str) -> Dict[str, Any]:
        """Extract statistics from XML file"""
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stats = {
                "file_size": len(content),
                "total_items": len(re.findall(r'<item>', content)),
                "pages": len(re.findall(r'<wp:post_type>page</wp:post_type>', content)),
                "posts": len(re.findall(r'<wp:post_type>post</wp:post_type>', content)),
                "menu_items": len(re.findall(r'<wp:post_type>nav_menu_item</wp:post_type>', content)),
                "elementor_blocks": len(re.findall(r'_elementor_data', content)),
                "custom_posts": len(re.findall(r'<wp:post_type>(?!page|post|nav_menu_item)', content)),
                "media_attachments": len(re.findall(r'<wp:post_type>attachment</wp:post_type>', content))
            }
            
            # Extract titles
            titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)
            stats["titles"] = titles
            
            # Extract post IDs
            post_ids = re.findall(r'<wp:post_id>(\d+)</wp:post_id>', content)
            stats["post_ids"] = [int(pid) for pid in post_ids]
            
            # Extract widget types from Elementor data
            widget_types = set()
            elementor_matches = re.findall(r'"widgetType":"([^"]+)"', content)
            widget_types.update(elementor_matches)
            stats["widget_types"] = list(widget_types)
            
            return stats
        
        except Exception as e:
            self.log(f"Error parsing XML stats: {str(e)}", "ERROR")
            return {}
    
    def compare_basic_stats(self):
        """Compare basic statistics between reference and generated XML"""
        self.log("📊 Comparing basic statistics...")
        
        ref_stats = self.parse_xml_stats(self.reference_xml)
        gen_stats = self.parse_xml_stats(self.generated_xml)
        
        self.comparison_results["reference_stats"] = ref_stats
        self.comparison_results["generated_stats"] = gen_stats
        
        # Compare numeric stats
        numeric_fields = ["total_items", "pages", "posts", "menu_items", "elementor_blocks", "media_attachments"]
        
        for field in numeric_fields:
            ref_val = ref_stats.get(field, 0)
            gen_val = gen_stats.get(field, 0)
            
            if ref_val != gen_val:
                diff = {
                    "type": "count_difference",
                    "field": field,
                    "reference": ref_val,
                    "generated": gen_val,
                    "difference": gen_val - ref_val
                }
                self.comparison_results["differences"].append(diff)
                
                if gen_val < ref_val:
                    self.log(f"⚠️ {field}: Generated has {gen_val}, reference has {ref_val} (missing {ref_val - gen_val})", "WARNING")
                else:
                    self.log(f"ℹ️ {field}: Generated has {gen_val}, reference has {ref_val} (extra {gen_val - ref_val})", "INFO")
            else:
                self.log(f"✅ {field}: Match ({gen_val})")
    
    def compare_content_titles(self):
        """Compare content titles between files"""
        self.log("📝 Comparing content titles...")
        
        ref_titles = set(self.comparison_results["reference_stats"].get("titles", []))
        gen_titles = set(self.comparison_results["generated_stats"].get("titles", []))
        
        missing_titles = ref_titles - gen_titles
        extra_titles = gen_titles - ref_titles
        matching_titles = ref_titles & gen_titles
        
        if missing_titles:
            self.log(f"❌ Missing titles: {len(missing_titles)}", "ERROR")
            for title in missing_titles:
                self.log(f"  - '{title}'", "ERROR")
                self.comparison_results["missing_elements"].append({
                    "type": "title",
                    "content": title
                })
        
        if extra_titles:
            self.log(f"➕ Extra titles: {len(extra_titles)}", "INFO")
            for title in extra_titles:
                self.log(f"  + '{title}'", "INFO")
                self.comparison_results["extra_elements"].append({
                    "type": "title",
                    "content": title
                })
        
        self.log(f"✅ Matching titles: {len(matching_titles)}")
        for title in matching_titles:
            self.comparison_results["content_matches"].append({
                "type": "title",
                "content": title
            })
    
    def compare_post_ids(self):
        """Compare post IDs between files"""
        self.log("🆔 Comparing post IDs...")
        
        ref_ids = set(self.comparison_results["reference_stats"].get("post_ids", []))
        gen_ids = set(self.comparison_results["generated_stats"].get("post_ids", []))
        
        missing_ids = ref_ids - gen_ids
        extra_ids = gen_ids - ref_ids
        matching_ids = ref_ids & gen_ids
        
        if missing_ids:
            self.log(f"❌ Missing post IDs: {sorted(missing_ids)}", "ERROR")
            for post_id in missing_ids:
                self.comparison_results["missing_elements"].append({
                    "type": "post_id",
                    "content": post_id
                })
        
        if extra_ids:
            self.log(f"➕ Extra post IDs: {sorted(extra_ids)}", "INFO")
            for post_id in extra_ids:
                self.comparison_results["extra_elements"].append({
                    "type": "post_id",
                    "content": post_id
                })
        
        self.log(f"✅ Matching post IDs: {len(matching_ids)}")
    
    def compare_widget_types(self):
        """Compare widget types used in Elementor data"""
        self.log("🧩 Comparing Elementor widget types...")
        
        ref_widgets = set(self.comparison_results["reference_stats"].get("widget_types", []))
        gen_widgets = set(self.comparison_results["generated_stats"].get("widget_types", []))
        
        missing_widgets = ref_widgets - gen_widgets
        extra_widgets = gen_widgets - ref_widgets
        matching_widgets = ref_widgets & gen_widgets
        
        if missing_widgets:
            self.log(f"❌ Missing widget types: {sorted(missing_widgets)}", "ERROR")
            for widget in missing_widgets:
                self.comparison_results["missing_elements"].append({
                    "type": "widget_type",
                    "content": widget
                })
        
        if extra_widgets:
            self.log(f"➕ Extra widget types: {sorted(extra_widgets)}", "INFO")
            for widget in extra_widgets:
                self.comparison_results["extra_elements"].append({
                    "type": "widget_type",
                    "content": widget
                })
        
        self.log(f"✅ Matching widget types: {len(matching_widgets)}")
        
        # Special focus on Cholot widgets
        cholot_ref = {w for w in ref_widgets if w.startswith('cholot-')}
        cholot_gen = {w for w in gen_widgets if w.startswith('cholot-')}
        
        if cholot_ref or cholot_gen:
            self.log(f"🏠 Cholot widgets - Reference: {len(cholot_ref)}, Generated: {len(cholot_gen)}")
            
            missing_cholot = cholot_ref - cholot_gen
            if missing_cholot:
                self.log(f"❌ Missing Cholot widgets: {sorted(missing_cholot)}", "ERROR")
    
    def compare_xml_structure(self):
        """Compare XML structure using element trees"""
        try:
            self.log("🌳 Comparing XML structure...")
            
            # Parse both XML files
            with open(self.reference_xml, 'r', encoding='utf-8') as f:
                ref_content = f.read()
            
            with open(self.generated_xml, 'r', encoding='utf-8') as f:
                gen_content = f.read()
            
            # Extract the basic structure (remove variable content)
            ref_structure = self._extract_structure(ref_content)
            gen_structure = self._extract_structure(gen_content)
            
            # Compare structures
            if ref_structure == gen_structure:
                self.log("✅ XML structures match")
            else:
                self.log("❌ XML structure differences found", "ERROR")
                
                # Find differences using difflib
                diff = difflib.unified_diff(
                    ref_structure.splitlines(keepends=True),
                    gen_structure.splitlines(keepends=True),
                    fromfile='reference_structure',
                    tofile='generated_structure',
                    n=3
                )
                
                diff_lines = list(diff)
                if len(diff_lines) > 100:  # Limit output
                    diff_lines = diff_lines[:100] + ['... (truncated)\n']
                
                for line in diff_lines:
                    if line.startswith('+'):
                        self.log(f"  + {line.rstrip()}", "INFO")
                    elif line.startswith('-'):
                        self.log(f"  - {line.rstrip()}", "ERROR")
        
        except Exception as e:
            self.log(f"Error comparing XML structure: {str(e)}", "ERROR")
    
    def _extract_structure(self, xml_content: str) -> str:
        """Extract XML structure by removing variable content"""
        # Remove CDATA content
        structure = re.sub(r'<!\[CDATA\[.*?\]\]>', '<![CDATA[...]]>', xml_content, flags=re.DOTALL)
        
        # Remove dates
        structure = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', 'YYYY-MM-DD HH:MM:SS', structure)
        
        # Remove URLs
        structure = re.sub(r'https?://[^\s<>"]+', 'http://example.com', structure)
        
        # Remove post IDs (keep structure)
        structure = re.sub(r'<wp:post_id>\d+</wp:post_id>', '<wp:post_id>###</wp:post_id>', structure)
        
        return structure
    
    def calculate_similarity_score(self) -> float:
        """Calculate overall similarity score between files"""
        self.log("📈 Calculating similarity score...")
        
        ref_stats = self.comparison_results["reference_stats"]
        gen_stats = self.comparison_results["generated_stats"]
        
        # Calculate scores for different aspects
        scores = []
        
        # 1. Content count similarity (40% weight)
        content_fields = ["total_items", "pages", "posts", "elementor_blocks"]
        content_score = 0
        for field in content_fields:
            ref_val = ref_stats.get(field, 0)
            gen_val = gen_stats.get(field, 0)
            if ref_val == 0 and gen_val == 0:
                scores.append(1.0)
            elif ref_val == 0:
                scores.append(0.0)
            else:
                similarity = min(gen_val, ref_val) / max(gen_val, ref_val)
                scores.append(similarity)
        
        # 2. Title matching (30% weight)
        ref_titles = set(ref_stats.get("titles", []))
        gen_titles = set(gen_stats.get("titles", []))
        if ref_titles:
            title_score = len(ref_titles & gen_titles) / len(ref_titles)
        else:
            title_score = 1.0 if not gen_titles else 0.5
        scores.append(title_score)
        
        # 3. Widget type matching (20% weight)
        ref_widgets = set(ref_stats.get("widget_types", []))
        gen_widgets = set(gen_stats.get("widget_types", []))
        if ref_widgets:
            widget_score = len(ref_widgets & gen_widgets) / len(ref_widgets)
        else:
            widget_score = 1.0 if not gen_widgets else 0.5
        scores.append(widget_score)
        
        # 4. Post ID matching (10% weight)
        ref_ids = set(ref_stats.get("post_ids", []))
        gen_ids = set(gen_stats.get("post_ids", []))
        if ref_ids:
            id_score = len(ref_ids & gen_ids) / len(ref_ids)
        else:
            id_score = 1.0 if not gen_ids else 0.5
        scores.append(id_score)
        
        # Calculate weighted average
        weights = [0.4, 0.3, 0.2, 0.1]  # Adjust as needed
        if len(scores) > len(weights):
            # If we have more scores than weights, use equal weighting
            weighted_score = sum(scores) / len(scores)
        else:
            weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        
        self.comparison_results["overall_score"] = weighted_score * 100
        
        self.log(f"📊 Individual scores: {[f'{s:.2f}' for s in scores]}")
        self.log(f"🎯 Overall similarity score: {weighted_score * 100:.1f}%")
        
        return weighted_score
    
    def run_comparison(self) -> Dict[str, Any]:
        """Run complete comparison"""
        self.log("🔍 Starting XML comparison...")
        
        # Check if files exist
        if not os.path.exists(self.reference_xml):
            self.log(f"Reference XML not found: {self.reference_xml}", "ERROR")
            return self.comparison_results
        
        if not os.path.exists(self.generated_xml):
            self.log(f"Generated XML not found: {self.generated_xml}", "ERROR")
            return self.comparison_results
        
        # Run all comparison tests
        self.compare_basic_stats()
        self.compare_content_titles()
        self.compare_post_ids()
        self.compare_widget_types()
        self.compare_xml_structure()
        
        # Calculate overall score
        self.calculate_similarity_score()
        
        return self.comparison_results
    
    def generate_report(self) -> bool:
        """Generate comparison report"""
        try:
            output_dir = os.path.join(os.path.dirname(self.generated_xml), 'generated')
            os.makedirs(output_dir, exist_ok=True)
            
            report_file = os.path.join(output_dir, 'xml-comparison-report.json')
            
            report = {
                'comparison_date': datetime.now().isoformat(),
                'reference_file': self.reference_xml,
                'generated_file': self.generated_xml,
                'results': self.comparison_results
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.log(f"Comparison report saved to: {report_file}")
            
            # Also generate a human-readable summary
            summary_file = os.path.join(output_dir, 'xml-comparison-summary.txt')
            self._generate_summary_file(summary_file)
            
            return True
        
        except Exception as e:
            self.log(f"Error generating report: {str(e)}", "ERROR")
            return False
    
    def _generate_summary_file(self, summary_file: str):
        """Generate human-readable summary file"""
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("XML COMPARISON SUMMARY\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Reference: {self.reference_xml}\n")
                f.write(f"Generated: {self.generated_xml}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write(f"OVERALL SIMILARITY: {self.comparison_results['overall_score']:.1f}%\n\n")
                
                # Statistics comparison
                f.write("STATISTICS COMPARISON\n")
                f.write("-" * 30 + "\n")
                ref_stats = self.comparison_results["reference_stats"]
                gen_stats = self.comparison_results["generated_stats"]
                
                stats_fields = ["total_items", "pages", "posts", "menu_items", "elementor_blocks"]
                for field in stats_fields:
                    ref_val = ref_stats.get(field, 0)
                    gen_val = gen_stats.get(field, 0)
                    status = "✓" if ref_val == gen_val else "✗"
                    f.write(f"{field:15} {status} Ref: {ref_val:3}, Gen: {gen_val:3}\n")
                
                f.write(f"\nMISSING ELEMENTS: {len(self.comparison_results['missing_elements'])}\n")
                f.write(f"EXTRA ELEMENTS: {len(self.comparison_results['extra_elements'])}\n")
                f.write(f"CONTENT MATCHES: {len(self.comparison_results['content_matches'])}\n")
        
        except Exception as e:
            self.log(f"Error generating summary: {str(e)}", "ERROR")
    
    def print_summary(self) -> bool:
        """Print comparison summary"""
        print("\n" + "="*60)
        print("XML COMPARISON SUMMARY")
        print("="*60)
        
        score = self.comparison_results["overall_score"]
        ref_stats = self.comparison_results["reference_stats"]
        gen_stats = self.comparison_results["generated_stats"]
        
        print(f"📊 Overall Similarity Score: {score:.1f}%")
        print()
        
        print("📈 Content Statistics:")
        stats_fields = ["total_items", "pages", "posts", "menu_items", "elementor_blocks"]
        for field in stats_fields:
            ref_val = ref_stats.get(field, 0)
            gen_val = gen_stats.get(field, 0)
            status = "✅" if ref_val == gen_val else "❌"
            print(f"  {status} {field:15}: Reference {ref_val:3}, Generated {gen_val:3}")
        
        print()
        missing_count = len(self.comparison_results["missing_elements"])
        extra_count = len(self.comparison_results["extra_elements"])
        
        if missing_count > 0:
            print(f"❌ Missing Elements: {missing_count}")
        
        if extra_count > 0:
            print(f"➕ Extra Elements: {extra_count}")
        
        matches_count = len(self.comparison_results["content_matches"])
        print(f"✅ Content Matches: {matches_count}")
        
        # Determine overall result
        if score >= 80 and missing_count == 0:
            print("\n🎉 COMPARISON PASSED")
            return True
        elif score >= 60:
            print("\n⚠️ COMPARISON PARTIALLY PASSED")
            return True
        else:
            print("\n❌ COMPARISON FAILED")
            return False


def main():
    """Main execution function"""
    if len(sys.argv) not in [2, 3]:
        print("Usage: python compare-xml.py <generated_xml> [reference_xml]")
        print("Example: python compare-xml.py cholot-generated.xml cholot-original.xml")
        sys.exit(1)
    
    generated_xml = sys.argv[1]
    
    # Try to find a reference file if not provided
    if len(sys.argv) == 3:
        reference_xml = sys.argv[2]
    else:
        # Look for common reference file names
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_refs = [
            "cholot-original.xml",
            "cholot-reference.xml",
            "cholot-export.xml",
            "reference.xml"
        ]
        
        reference_xml = None
        for ref_name in possible_refs:
            ref_path = os.path.join(script_dir, ref_name)
            if os.path.exists(ref_path):
                reference_xml = ref_path
                break
        
        if not reference_xml:
            print("❌ No reference XML file found. Please specify one:")
            print(f"Available files in {script_dir}:")
            for file in os.listdir(script_dir):
                if file.endswith('.xml'):
                    print(f"  - {file}")
            sys.exit(1)
    
    print("🔍 CHOLOT XML COMPARATOR")
    print("=" * 60)
    print("Comparing generated XML with reference XML")
    print()
    
    comparator = XMLComparator(reference_xml, generated_xml)
    comparison_results = comparator.run_comparison()
    
    # Generate detailed report
    comparator.generate_report()
    
    # Print summary and determine exit code
    success = comparator.print_summary()
    
    if success:
        sys.exit(0)  # Success or partial success
    else:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()