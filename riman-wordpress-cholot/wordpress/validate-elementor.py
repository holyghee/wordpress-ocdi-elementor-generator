#!/usr/bin/env python3
"""
validate-elementor.py - Elementor Data Validation Script
Part of Cholot Iterative Generator System

This script validates Elementor data in WordPress XML files to ensure:
1. Elementor data is properly encoded
2. JSON structure is valid
3. Required Elementor meta keys are present
4. Widget data is complete and valid
"""

import sys
import os
import json
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import html

class ElementorValidator:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.validation_results = {
            "total_pages": 0,
            "pages_with_elementor": 0,
            "valid_elementor_data": 0,
            "invalid_elementor_data": 0,
            "missing_meta_keys": 0,
            "errors": [],
            "warnings": [],
            "details": []
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
        if level == "ERROR":
            self.validation_results["errors"].append(message)
        elif level == "WARNING":
            self.validation_results["warnings"].append(message)
    
    def extract_elementor_data_from_xml(self) -> List[Dict]:
        """Extract all Elementor data from XML file"""
        try:
            with open(self.xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all _elementor_data meta values
            elementor_pattern = r'<wp:meta_key>_elementor_data</wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>'
            matches = re.findall(elementor_pattern, content, re.DOTALL)
            
            elementor_data_blocks = []
            for i, match in enumerate(matches):
                elementor_data_blocks.append({
                    'index': i,
                    'raw_data': match,
                    'post_id': self._get_post_id_for_elementor_data(content, match)
                })
            
            self.log(f"Found {len(elementor_data_blocks)} Elementor data blocks")
            return elementor_data_blocks
        
        except Exception as e:
            self.log(f"Error extracting Elementor data: {str(e)}", "ERROR")
            return []
    
    def _get_post_id_for_elementor_data(self, content: str, elementor_data: str) -> Optional[int]:
        """Try to find the post ID associated with Elementor data"""
        try:
            # Find the position of this Elementor data in the content
            data_pos = content.find(elementor_data)
            if data_pos == -1:
                return None
            
            # Look backwards for the nearest <wp:post_id>
            before_content = content[:data_pos]
            post_id_matches = re.findall(r'<wp:post_id>(\d+)</wp:post_id>', before_content)
            
            if post_id_matches:
                return int(post_id_matches[-1])  # Get the last (closest) post ID
            
            return None
        
        except Exception:
            return None
    
    def validate_json_structure(self, raw_data: str) -> Tuple[bool, Optional[List], str]:
        """Validate that Elementor data is valid JSON"""
        try:
            # Clean up the data - remove extra escaping that might be present
            cleaned_data = raw_data.strip()
            
            # Handle WordPress-style escaping
            cleaned_data = cleaned_data.replace('\\"', '"').replace('\\\\', '\\')
            
            # Try to parse as JSON
            parsed_data = json.loads(cleaned_data)
            
            if not isinstance(parsed_data, list):
                return False, None, "Elementor data should be a JSON array"
            
            return True, parsed_data, "Valid JSON structure"
        
        except json.JSONDecodeError as e:
            return False, None, f"JSON parsing error: {str(e)}"
        except Exception as e:
            return False, None, f"Validation error: {str(e)}"
    
    def validate_elementor_structure(self, data: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate Elementor section/column/widget structure"""
        issues = []
        
        try:
            for i, section in enumerate(data):
                if not isinstance(section, dict):
                    issues.append(f"Section {i}: Not a dictionary object")
                    continue
                
                # Check required section fields
                required_section_fields = ['id', 'elType']
                for field in required_section_fields:
                    if field not in section:
                        issues.append(f"Section {i}: Missing required field '{field}'")
                
                # Validate elType
                if section.get('elType') not in ['section', 'column', 'widget']:
                    issues.append(f"Section {i}: Invalid elType '{section.get('elType')}'")
                
                # If it's a section, check for elements (columns)
                if section.get('elType') == 'section':
                    elements = section.get('elements', [])
                    if not isinstance(elements, list):
                        issues.append(f"Section {i}: 'elements' should be a list")
                    else:
                        for j, column in enumerate(elements):
                            self._validate_column(column, f"Section {i}, Column {j}", issues)
        
        except Exception as e:
            issues.append(f"Structure validation error: {str(e)}")
        
        return len(issues) == 0, issues
    
    def _validate_column(self, column: Dict, context: str, issues: List[str]):
        """Validate a column structure"""
        if not isinstance(column, dict):
            issues.append(f"{context}: Not a dictionary object")
            return
        
        # Check required column fields
        required_fields = ['id', 'elType']
        for field in required_fields:
            if field not in column:
                issues.append(f"{context}: Missing required field '{field}'")
        
        # Validate elType for column
        if column.get('elType') != 'column':
            issues.append(f"{context}: Expected elType 'column', got '{column.get('elType')}'")
        
        # Check column elements (widgets)
        elements = column.get('elements', [])
        if isinstance(elements, list):
            for k, widget in enumerate(elements):
                self._validate_widget(widget, f"{context}, Widget {k}", issues)
    
    def _validate_widget(self, widget: Dict, context: str, issues: List[str]):
        """Validate a widget structure"""
        if not isinstance(widget, dict):
            issues.append(f"{context}: Not a dictionary object")
            return
        
        # Check required widget fields
        required_fields = ['id', 'elType', 'widgetType']
        for field in required_fields:
            if field not in widget:
                issues.append(f"{context}: Missing required field '{field}'")
        
        # Validate elType for widget
        if widget.get('elType') != 'widget':
            issues.append(f"{context}: Expected elType 'widget', got '{widget.get('elType')}'")
        
        # Check if widgetType is specified
        widget_type = widget.get('widgetType')
        if not widget_type:
            issues.append(f"{context}: Missing widgetType")
        
        # Check for settings
        settings = widget.get('settings', {})
        if not isinstance(settings, dict):
            issues.append(f"{context}: Settings should be a dictionary")
    
    def validate_cholot_widgets(self, data: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate Cholot-specific widgets"""
        issues = []
        cholot_widgets = []
        
        def find_widgets(elements):
            widgets = []
            for element in elements:
                if element.get('elType') == 'widget':
                    widgets.append(element)
                elif element.get('elType') in ['section', 'column'] and 'elements' in element:
                    widgets.extend(find_widgets(element['elements']))
            return widgets
        
        all_widgets = find_widgets(data)
        
        for widget in all_widgets:
            widget_type = widget.get('widgetType', '')
            if widget_type.startswith('cholot-'):
                cholot_widgets.append(widget)
        
        self.log(f"Found {len(cholot_widgets)} Cholot-specific widgets")
        
        # Validate Cholot widgets
        for i, widget in enumerate(cholot_widgets):
            widget_type = widget.get('widgetType')
            settings = widget.get('settings', {})
            
            # Basic validation for common Cholot widgets
            if widget_type == 'cholot-texticon':
                if not settings.get('title'):
                    issues.append(f"Cholot TextIcon widget {i}: Missing title")
            
            elif widget_type == 'cholot-team':
                if not settings.get('name'):
                    issues.append(f"Cholot Team widget {i}: Missing name")
            
            elif widget_type == 'cholot-testimonial-two':
                if not settings.get('content'):
                    issues.append(f"Cholot Testimonial widget {i}: Missing content")
            
            elif widget_type == 'cholot-contact':
                # Validate contact form fields
                required_fields = ['email', 'phone']
                for field in required_fields:
                    if not settings.get(field):
                        issues.append(f"Cholot Contact widget {i}: Missing {field}")
        
        return len(issues) == 0, issues
    
    def validate_required_meta_keys(self) -> bool:
        """Check for required Elementor meta keys"""
        try:
            with open(self.xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_meta_keys = [
                '_elementor_data',
                '_elementor_edit_mode',
                '_elementor_template_type',
                '_elementor_version'
            ]
            
            missing_keys = []
            for key in required_meta_keys:
                if f'<wp:meta_key>{key}</wp:meta_key>' not in content:
                    missing_keys.append(key)
            
            if missing_keys:
                self.log(f"Missing required meta keys: {', '.join(missing_keys)}", "WARNING")
                self.validation_results["missing_meta_keys"] = len(missing_keys)
                return False
            
            self.log("All required Elementor meta keys are present")
            return True
        
        except Exception as e:
            self.log(f"Error checking meta keys: {str(e)}", "ERROR")
            return False
    
    def run_validation(self) -> Dict:
        """Run complete validation"""
        self.log("🔍 Starting Elementor validation...")
        
        if not os.path.exists(self.xml_file):
            self.log(f"XML file not found: {self.xml_file}", "ERROR")
            return self.validation_results
        
        # Extract Elementor data
        elementor_blocks = self.extract_elementor_data_from_xml()
        self.validation_results["pages_with_elementor"] = len(elementor_blocks)
        
        if not elementor_blocks:
            self.log("No Elementor data found in XML", "ERROR")
            return self.validation_results
        
        # Validate each Elementor data block
        for block in elementor_blocks:
            index = block['index']
            post_id = block.get('post_id', 'unknown')
            raw_data = block['raw_data']
            
            self.log(f"Validating Elementor block {index} (Post ID: {post_id})")
            
            # Validate JSON structure
            is_valid_json, parsed_data, json_message = self.validate_json_structure(raw_data)
            
            detail = {
                'block_index': index,
                'post_id': post_id,
                'json_valid': is_valid_json,
                'json_message': json_message,
                'structure_valid': False,
                'cholot_widgets_valid': False
            }
            
            if is_valid_json:
                self.validation_results["valid_elementor_data"] += 1
                
                # Validate Elementor structure
                is_valid_structure, structure_issues = self.validate_elementor_structure(parsed_data)
                detail['structure_valid'] = is_valid_structure
                detail['structure_issues'] = structure_issues
                
                if not is_valid_structure:
                    self.log(f"Block {index}: Structure validation failed", "ERROR")
                    for issue in structure_issues:
                        self.log(f"  - {issue}", "ERROR")
                else:
                    self.log(f"Block {index}: Structure validation passed")
                
                # Validate Cholot widgets
                is_valid_cholot, cholot_issues = self.validate_cholot_widgets(parsed_data)
                detail['cholot_widgets_valid'] = is_valid_cholot
                detail['cholot_issues'] = cholot_issues
                
                if not is_valid_cholot:
                    self.log(f"Block {index}: Cholot widget validation issues found", "WARNING")
                    for issue in cholot_issues:
                        self.log(f"  - {issue}", "WARNING")
                else:
                    self.log(f"Block {index}: Cholot widget validation passed")
            
            else:
                self.validation_results["invalid_elementor_data"] += 1
                self.log(f"Block {index}: {json_message}", "ERROR")
            
            self.validation_results["details"].append(detail)
        
        # Check for required meta keys
        self.validate_required_meta_keys()
        
        return self.validation_results
    
    def generate_report(self) -> bool:
        """Generate validation report"""
        try:
            report_file = os.path.join(os.path.dirname(self.xml_file), 'generated', 'elementor-validation-report.json')
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            
            report = {
                'validation_date': datetime.now().isoformat(),
                'xml_file': self.xml_file,
                'summary': {
                    'total_blocks': self.validation_results["pages_with_elementor"],
                    'valid_blocks': self.validation_results["valid_elementor_data"],
                    'invalid_blocks': self.validation_results["invalid_elementor_data"],
                    'success_rate': (self.validation_results["valid_elementor_data"] / 
                                   max(1, self.validation_results["pages_with_elementor"])) * 100
                },
                'results': self.validation_results
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.log(f"Validation report saved to: {report_file}")
            return True
        
        except Exception as e:
            self.log(f"Error generating report: {str(e)}", "ERROR")
            return False
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*60)
        print("ELEMENTOR VALIDATION SUMMARY")
        print("="*60)
        
        total_blocks = self.validation_results["pages_with_elementor"]
        valid_blocks = self.validation_results["valid_elementor_data"]
        
        if total_blocks == 0:
            print("❌ No Elementor data found in XML")
            return False
        
        success_rate = (valid_blocks / total_blocks) * 100
        
        print(f"📊 Total Elementor blocks: {total_blocks}")
        print(f"✅ Valid blocks: {valid_blocks}")
        print(f"❌ Invalid blocks: {self.validation_results['invalid_elementor_data']}")
        print(f"📈 Success rate: {success_rate:.1f}%")
        
        if self.validation_results["errors"]:
            print(f"\n❌ Errors found: {len(self.validation_results['errors'])}")
            for error in self.validation_results["errors"]:
                print(f"  - {error}")
        
        if self.validation_results["warnings"]:
            print(f"\n⚠️ Warnings: {len(self.validation_results['warnings'])}")
            for warning in self.validation_results["warnings"]:
                print(f"  - {warning}")
        
        # Overall result
        if success_rate >= 80 and len(self.validation_results["errors"]) == 0:
            print("\n🎉 VALIDATION PASSED")
            return True
        else:
            print("\n❌ VALIDATION FAILED")
            return False


def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python validate-elementor.py <xml_file>")
        print("Example: python validate-elementor.py cholot-generated.xml")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    
    print("🔍 CHOLOT ELEMENTOR VALIDATOR")
    print("=" * 60)
    print("Validating Elementor data in WordPress XML")
    print()
    
    validator = ElementorValidator(xml_file)
    validation_results = validator.run_validation()
    
    # Generate detailed report
    validator.generate_report()
    
    # Print summary and determine exit code
    success = validator.print_summary()
    
    if success:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()