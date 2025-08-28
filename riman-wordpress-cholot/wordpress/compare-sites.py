#!/usr/bin/env python3
"""
Site Comparison Utility
Vergleicht localhost:8080 (original) vs localhost:8081 (test) 

Teil der CHOLOT TEST SUITE für visuelle Verifizierung
Author: Claude Code Assistant (OCDI TEST SUITE BUILDER)
Date: 2025-08-28
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import difflib
import re

class SiteComparator:
    """
    Vergleicht zwei WordPress Sites (Original vs Test)
    """
    
    def __init__(self, original_url: str = "http://localhost:8080", test_url: str = "http://localhost:8081"):
        self.original_url = original_url.rstrip('/')
        self.test_url = test_url.rstrip('/')
        self.results = {}
        self.timeout = 10
        
        print(f"🔍 SITE COMPARISON UTILITY")
        print(f"==========================")
        print(f"Original Site: {self.original_url}")
        print(f"Test Site: {self.test_url}")
        print(f"==========================\n")
    
    def compare_sites(self, pages: List[str] = None) -> Dict[str, Any]:
        """Hauptvergleichsfunktion"""
        if pages is None:
            pages = ['/', '/about', '/services', '/contact', '/blog']
        
        print(f"📋 Testing {len(pages)} pages...")
        
        overall_results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'original_url': self.original_url,
            'test_url': self.test_url,
            'pages_tested': len(pages),
            'pages_successful': 0,
            'pages_failed': 0,
            'page_results': {},
            'summary': {}
        }
        
        for page_path in pages:
            print(f"\n📄 Testing: {page_path}")
            print("-" * 20)
            
            page_result = self._compare_single_page(page_path)
            overall_results['page_results'][page_path] = page_result
            
            if page_result.get('accessible_both', False):
                overall_results['pages_successful'] += 1
            else:
                overall_results['pages_failed'] += 1
        
        # Generate summary
        overall_results['summary'] = self._generate_summary(overall_results)
        
        return overall_results
    
    def _compare_single_page(self, page_path: str) -> Dict[str, Any]:
        """Vergleiche eine einzelne Seite"""
        original_url = urljoin(self.original_url, page_path)
        test_url = urljoin(self.test_url, page_path)
        
        result = {
            'page_path': page_path,
            'original_url': original_url,
            'test_url': test_url,
            'accessible_both': False,
            'status_codes': {},
            'content_comparison': {},
            'performance': {},
            'errors': []
        }
        
        try:
            # Request original site
            print(f"  🔍 Checking original: {original_url}")
            start_time = time.time()
            original_response = requests.get(original_url, timeout=self.timeout)
            original_duration = time.time() - start_time
            
            result['status_codes']['original'] = original_response.status_code
            result['performance']['original'] = round(original_duration, 3)
            
            print(f"    Status: {original_response.status_code} ({original_duration:.3f}s)")
            
        except requests.RequestException as e:
            result['errors'].append(f"Original site error: {str(e)}")
            print(f"    ❌ Error: {e}")
            return result
        
        try:
            # Request test site
            print(f"  🔍 Checking test: {test_url}")
            start_time = time.time()
            test_response = requests.get(test_url, timeout=self.timeout)
            test_duration = time.time() - start_time
            
            result['status_codes']['test'] = test_response.status_code
            result['performance']['test'] = round(test_duration, 3)
            
            print(f"    Status: {test_response.status_code} ({test_duration:.3f}s)")
            
        except requests.RequestException as e:
            result['errors'].append(f"Test site error: {str(e)}")
            print(f"    ❌ Error: {e}")
            return result
        
        # Both sites accessible
        if original_response.status_code == 200 and test_response.status_code == 200:
            result['accessible_both'] = True
            
            # Compare content
            content_comparison = self._compare_content(
                original_response.text, 
                test_response.text,
                page_path
            )
            result['content_comparison'] = content_comparison
            
            # Performance comparison
            perf_diff = abs(original_duration - test_duration)
            result['performance']['difference'] = round(perf_diff, 3)
            
            if perf_diff < 0.5:
                print(f"    ⚡ Performance: Similar ({perf_diff:.3f}s diff)")
            else:
                print(f"    ⚠️ Performance: {perf_diff:.3f}s difference")
            
            # Content summary
            similarity = content_comparison.get('similarity_percent', 0)
            if similarity >= 90:
                print(f"    ✅ Content: {similarity:.1f}% similar")
            elif similarity >= 70:
                print(f"    ⚠️ Content: {similarity:.1f}% similar")
            else:
                print(f"    ❌ Content: {similarity:.1f}% similar")
        
        elif original_response.status_code != test_response.status_code:
            print(f"    ⚠️ Status mismatch: {original_response.status_code} vs {test_response.status_code}")
        
        return result
    
    def _compare_content(self, original_html: str, test_html: str, page_path: str) -> Dict[str, Any]:
        """Vergleiche HTML-Content von zwei Seiten"""
        comparison = {
            'original_length': len(original_html),
            'test_length': len(test_html),
            'length_difference': abs(len(original_html) - len(test_html)),
            'length_diff_percent': 0,
            'similarity_percent': 0,
            'elementor_comparison': {},
            'title_comparison': {},
            'meta_comparison': {},
            'differences': []
        }
        
        if len(original_html) > 0:
            comparison['length_diff_percent'] = round(
                (comparison['length_difference'] / len(original_html)) * 100, 2
            )
        
        # Text similarity (simplified)
        original_text = self._extract_text_content(original_html)
        test_text = self._extract_text_content(test_html)
        
        if original_text and test_text:
            similarity = difflib.SequenceMatcher(None, original_text, test_text).ratio()
            comparison['similarity_percent'] = round(similarity * 100, 1)
        
        # Title comparison
        original_title = self._extract_title(original_html)
        test_title = self._extract_title(test_html)
        
        comparison['title_comparison'] = {
            'original': original_title,
            'test': test_title,
            'matches': original_title == test_title
        }
        
        # Elementor-specific comparison
        elementor_comparison = self._compare_elementor_content(original_html, test_html)
        comparison['elementor_comparison'] = elementor_comparison
        
        # Find major differences
        if comparison['length_diff_percent'] > 20:
            comparison['differences'].append(f"Significant size difference: {comparison['length_diff_percent']:.1f}%")
        
        if not comparison['title_comparison']['matches']:
            comparison['differences'].append("Page titles don't match")
        
        if elementor_comparison.get('structure_different', False):
            comparison['differences'].append("Elementor structure differs")
        
        return comparison
    
    def _extract_text_content(self, html: str) -> str:
        """Extrahiere sichtbaren Text aus HTML"""
        # Simple text extraction (remove HTML tags)
        import re
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_title(self, html: str) -> str:
        """Extrahiere Seitentitel"""
        import re
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        return title_match.group(1).strip() if title_match else ""
    
    def _compare_elementor_content(self, original_html: str, test_html: str) -> Dict[str, Any]:
        """Vergleiche Elementor-spezifische Inhalte"""
        comparison = {
            'original_has_elementor': False,
            'test_has_elementor': False,
            'structure_different': False,
            'widget_counts': {},
            'section_counts': {}
        }
        
        # Check for Elementor indicators
        elementor_indicators = [
            'elementor-element',
            'elementor-section',
            'elementor-widget',
            'data-element_type'
        ]
        
        original_elementor = any(indicator in original_html for indicator in elementor_indicators)
        test_elementor = any(indicator in test_html for indicator in elementor_indicators)
        
        comparison['original_has_elementor'] = original_elementor
        comparison['test_has_elementor'] = test_elementor
        
        if original_elementor and test_elementor:
            # Count Elementor elements
            original_sections = len(re.findall(r'data-element_type="section"', original_html))
            test_sections = len(re.findall(r'data-element_type="section"', test_html))
            
            original_widgets = len(re.findall(r'elementor-widget-', original_html))
            test_widgets = len(re.findall(r'elementor-widget-', test_html))
            
            comparison['section_counts'] = {
                'original': original_sections,
                'test': test_sections,
                'difference': abs(original_sections - test_sections)
            }
            
            comparison['widget_counts'] = {
                'original': original_widgets,
                'test': test_widgets,
                'difference': abs(original_widgets - test_widgets)
            }
            
            # Determine if structure is significantly different
            section_diff_pct = (comparison['section_counts']['difference'] / max(original_sections, 1)) * 100
            widget_diff_pct = (comparison['widget_counts']['difference'] / max(original_widgets, 1)) * 100
            
            if section_diff_pct > 20 or widget_diff_pct > 30:
                comparison['structure_different'] = True
        
        return comparison
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generiere Zusammenfassung der Ergebnisse"""
        page_results = results['page_results']
        
        summary = {
            'overall_health': 'unknown',
            'accessibility_rate': 0,
            'average_similarity': 0,
            'performance_difference': 0,
            'elementor_consistency': 'unknown',
            'issues_found': [],
            'recommendations': []
        }
        
        if results['pages_tested'] > 0:
            summary['accessibility_rate'] = round(
                (results['pages_successful'] / results['pages_tested']) * 100, 1
            )
        
        # Calculate average similarity
        similarities = []
        performance_diffs = []
        elementor_issues = 0
        
        for page_path, page_result in page_results.items():
            if page_result.get('accessible_both', False):
                content_comp = page_result.get('content_comparison', {})
                similarities.append(content_comp.get('similarity_percent', 0))
                
                perf = page_result.get('performance', {})
                if 'difference' in perf:
                    performance_diffs.append(perf['difference'])
                
                # Check Elementor consistency
                elementor_comp = content_comp.get('elementor_comparison', {})
                if elementor_comp.get('structure_different', False):
                    elementor_issues += 1
        
        if similarities:
            summary['average_similarity'] = round(sum(similarities) / len(similarities), 1)
        
        if performance_diffs:
            summary['performance_difference'] = round(sum(performance_diffs) / len(performance_diffs), 3)
        
        # Overall health assessment
        if summary['accessibility_rate'] >= 90 and summary['average_similarity'] >= 80:
            summary['overall_health'] = 'excellent'
        elif summary['accessibility_rate'] >= 70 and summary['average_similarity'] >= 60:
            summary['overall_health'] = 'good'
        elif summary['accessibility_rate'] >= 50:
            summary['overall_health'] = 'fair'
        else:
            summary['overall_health'] = 'poor'
        
        # Elementor consistency
        if elementor_issues == 0:
            summary['elementor_consistency'] = 'consistent'
        elif elementor_issues <= len(page_results) / 2:
            summary['elementor_consistency'] = 'mostly_consistent'
        else:
            summary['elementor_consistency'] = 'inconsistent'
        
        # Issues and recommendations
        if summary['accessibility_rate'] < 100:
            summary['issues_found'].append(f"Some pages not accessible ({summary['accessibility_rate']:.1f}% success rate)")
            summary['recommendations'].append("Check WordPress configuration and fix broken pages")
        
        if summary['average_similarity'] < 70:
            summary['issues_found'].append(f"Low content similarity ({summary['average_similarity']:.1f}%)")
            summary['recommendations'].append("Review import process and check for missing content")
        
        if elementor_issues > 0:
            summary['issues_found'].append(f"Elementor structure differences on {elementor_issues} pages")
            summary['recommendations'].append("Verify Elementor data import and check widget availability")
        
        if summary['performance_difference'] > 1.0:
            summary['issues_found'].append(f"Significant performance difference ({summary['performance_difference']:.3f}s)")
            summary['recommendations'].append("Check server performance and optimize slow site")
        
        return summary
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Speichere Ergebnisse in JSON-Datei"""
        if filename is None:
            timestamp = time.strftime('%Y%m%d-%H%M%S')
            filename = f'site-comparison-{timestamp}.json'
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Results saved to: {filepath}")
        return str(filepath)
    
    def print_summary_report(self, results: Dict[str, Any]):
        """Drucke Zusammenfassungs-Report"""
        summary = results['summary']
        
        print(f"\n📊 COMPARISON SUMMARY")
        print(f"=====================")
        print(f"Overall Health: {summary['overall_health'].upper()}")
        print(f"Pages Accessible: {results['pages_successful']}/{results['pages_tested']} ({summary['accessibility_rate']:.1f}%)")
        print(f"Average Similarity: {summary['average_similarity']:.1f}%")
        print(f"Performance Diff: {summary['performance_difference']:.3f}s")
        print(f"Elementor Consistency: {summary['elementor_consistency']}")
        
        if summary['issues_found']:
            print(f"\n⚠️ ISSUES FOUND:")
            for issue in summary['issues_found']:
                print(f"  - {issue}")
        
        if summary['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in summary['recommendations']:
                print(f"  - {rec}")
        
        print(f"\n🎯 QUALITY SCORE:")
        # Calculate overall quality score
        quality_score = (
            (summary['accessibility_rate'] * 0.3) +
            (summary['average_similarity'] * 0.4) +
            (100 - min(summary['performance_difference'] * 10, 50)) * 0.2 +
            (100 if summary['elementor_consistency'] == 'consistent' else 50) * 0.1
        )
        
        print(f"   {quality_score:.1f}/100")
        
        if quality_score >= 90:
            print(f"   Status: 🏆 EXCELLENT")
        elif quality_score >= 75:
            print(f"   Status: ✅ GOOD") 
        elif quality_score >= 60:
            print(f"   Status: ⚠️ FAIR")
        else:
            print(f"   Status: ❌ POOR")

def main():
    """Main function"""
    # Parse command line arguments
    original_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    test_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8081"
    
    pages_to_test = [
        '/',
        '/about',
        '/services', 
        '/contact',
        '/blog'
    ]
    
    # Custom pages from command line
    if len(sys.argv) > 3:
        pages_to_test = sys.argv[3].split(',')
    
    comparator = SiteComparator(original_url, test_url)
    
    try:
        results = comparator.compare_sites(pages_to_test)
        
        # Save results
        results_file = comparator.save_results(results)
        
        # Print summary
        comparator.print_summary_report(results)
        
        print(f"\n✅ SITE COMPARISON COMPLETED!")
        print(f"📄 Detailed results: {results_file}")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Comparison interrupted by user")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())