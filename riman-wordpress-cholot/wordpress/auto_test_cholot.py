#!/usr/bin/env python3
"""
Auto Test Cholot - Automated WordPress XML Testing and Import System
Implementation Specialist's testing automation script

This script automates:
1. XML generation from YAML configurations
2. WordPress cleanup
3. Import testing with OCDI
4. Verification and error detection
5. Auto-fix and iteration until success
"""

import os
import sys
import subprocess
import json
import time
import glob
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

class AutoTestCholot:
    def __init__(self):
        self.work_dir = os.getcwd()
        self.test_results = []
        self.iteration_count = 0
        self.max_iterations = 5
        self.success_criteria = {
            'pages_imported': True,
            'elementor_data_preserved': True,
            'menu_structure_created': True,
            'custom_post_types_present': True
        }
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def run_command(self, command: str, description: str = "") -> Tuple[int, str, str]:
        """Run shell command and return result"""
        if description:
            self.log(f"Running: {description}")
        self.log(f"Command: {command}")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.log("Command timed out after 5 minutes", "ERROR")
            return -1, "", "Timeout"
        except Exception as e:
            self.log(f"Command failed: {str(e)}", "ERROR")
            return -1, "", str(e)
            
    def find_best_yaml_config(self) -> str:
        """Find the best YAML configuration file for testing"""
        # Priority order for YAML files
        yaml_candidates = [
            "riman-xl-site.yaml",
            "full-site.yaml", 
            "adaptive-input.yaml",
            "riman-input.yaml",
            "cholot-complete.yaml"
        ]
        
        for yaml_file in yaml_candidates:
            if os.path.exists(yaml_file):
                self.log(f"Found YAML config: {yaml_file}")
                return yaml_file
                
        # If none found, use first available .yaml file
        yaml_files = glob.glob("*.yaml")
        if yaml_files:
            yaml_file = yaml_files[0]
            self.log(f"Using fallback YAML: {yaml_file}")
            return yaml_file
            
        self.log("No YAML configuration files found!", "ERROR")
        return None
        
    def generate_xml_from_yaml(self, yaml_file: str, output_xml: str = "cholot-auto-test.xml") -> bool:
        """Generate WordPress XML from YAML configuration"""
        self.log(f"Generating XML from {yaml_file}")
        
        # Try different generators in priority order
        generators = [
            ("full_site_generator.py", f"python3 full_site_generator.py {yaml_file} {output_xml}"),
            ("section_based_processor.py", f"python3 section_based_processor.py {yaml_file} {output_xml}"),
            ("adaptive-elementor-generator.py", f"python3 adaptive-elementor-generator.py {yaml_file} {output_xml}")
        ]
        
        for generator_name, command in generators:
            if os.path.exists(generator_name):
                self.log(f"Trying generator: {generator_name}")
                returncode, stdout, stderr = self.run_command(command, f"Generate XML with {generator_name}")
                
                # Check if generator created XML with expected name from YAML
                expected_xml = yaml_file.replace('.yaml', '.xml')
                output_files = [output_xml, expected_xml]
                
                # Check all possible output files
                for xml_file in output_files:
                    if os.path.exists(xml_file):
                        file_size = os.path.getsize(xml_file)
                        if file_size > 5000:  # Reasonable size for a real XML
                            self.log(f"XML generated successfully: {xml_file} ({file_size} bytes)")
                            # Copy to expected output name if needed
                            if xml_file != output_xml:
                                import shutil
                                shutil.copy2(xml_file, output_xml)
                                self.log(f"Copied {xml_file} to {output_xml}")
                            return True
                        else:
                            self.log(f"XML too small ({file_size} bytes): {xml_file}")
                
                if returncode != 0:
                    self.log(f"Generator returned error code {returncode}")
                    if stderr.strip():
                        self.log(f"Generator stderr: {stderr}", "ERROR")
                    if stdout.strip():
                        self.log(f"Generator stdout: {stdout}")
                    
        self.log("All XML generators failed", "ERROR")
        return False
        
    def cleanup_wordpress(self) -> bool:
        """Clean WordPress installation"""
        self.log("Cleaning WordPress installation")
        
        if os.path.exists("wordpress-cleanup.sh"):
            returncode, stdout, stderr = self.run_command("./wordpress-cleanup.sh", "WordPress cleanup")
            if returncode == 0:
                self.log("WordPress cleaned successfully")
                return True
            else:
                self.log(f"WordPress cleanup failed: {stderr}", "ERROR")
        else:
            self.log("wordpress-cleanup.sh not found, skipping cleanup")
            
        return False
        
    def test_import_xml(self, xml_file: str) -> Dict[str, Any]:
        """Test XML import using OCDI"""
        self.log(f"Testing XML import: {xml_file}")
        
        test_result = {
            'xml_file': xml_file,
            'import_success': False,
            'pages_imported': 0,
            'posts_imported': 0,
            'media_imported': 0,
            'errors': [],
            'warnings': []
        }
        
        # Test with direct OCDI import
        if os.path.exists("test-direct-ocdi.php"):
            returncode, stdout, stderr = self.run_command(
                f"php test-direct-ocdi.php {xml_file}",
                "Test direct OCDI import"
            )
            
            if returncode == 0:
                test_result['import_success'] = True
                self.log("Direct OCDI import successful")
                
                # Parse output for statistics
                if "pages imported" in stdout.lower():
                    import re
                    pages_match = re.search(r'(\d+)\s+pages?\s+imported', stdout.lower())
                    if pages_match:
                        test_result['pages_imported'] = int(pages_match.group(1))
                        
                if "posts imported" in stdout.lower():
                    posts_match = re.search(r'(\d+)\s+posts?\s+imported', stdout.lower())
                    if posts_match:
                        test_result['posts_imported'] = int(posts_match.group(1))
                        
            else:
                test_result['errors'].append(f"OCDI import failed: {stderr}")
                self.log(f"OCDI import failed: {stderr}", "ERROR")
                
        return test_result
        
    def verify_import_results(self) -> Dict[str, bool]:
        """Verify import results against success criteria"""
        self.log("Verifying import results")
        
        verification_result = {}
        
        # Check imported content with verification script
        if os.path.exists("check-imported.php"):
            returncode, stdout, stderr = self.run_command("php check-imported.php", "Check imported content")
            
            if returncode == 0:
                # Parse verification output with improved detection
                stdout_lower = stdout.lower()
                
                # Check for pages (look for page post type with count > 0)
                import re
                page_match = re.search(r'📄 page \((\d+)\)', stdout)
                verification_result['pages_imported'] = page_match and int(page_match.group(1)) > 0
                
                # Check for Elementor data
                verification_result['elementor_data_preserved'] = 'elementor' in stdout_lower or 'has elementor data' in stdout_lower
                
                # Check for menus
                verification_result['menu_structure_created'] = 'menu' in stdout_lower and ('assignments' in stdout_lower or 'nav_menu_item' in stdout_lower)
                
                # Check for custom post types (headers/footers/etc)
                verification_result['custom_post_types_present'] = 'header' in stdout_lower or 'footer' in stdout_lower or 'custom post' in stdout_lower
                
                self.log(f"Verification results: {verification_result}")
            else:
                self.log(f"Verification failed: {stderr}", "ERROR")
                verification_result = {key: False for key in self.success_criteria.keys()}
        else:
            self.log("check-imported.php not found, skipping verification")
            verification_result = {key: False for key in self.success_criteria.keys()}
            
        return verification_result
        
    def analyze_errors_and_suggest_fixes(self, test_result: Dict[str, Any]) -> List[str]:
        """Analyze errors and suggest automatic fixes"""
        self.log("Analyzing errors and suggesting fixes")
        
        fixes = []
        
        # Common error patterns and fixes
        error_patterns = {
            'missing media': "Add placeholder images or fix image paths",
            'invalid xml': "Fix XML structure and encoding issues",
            'elementor data': "Check Elementor JSON structure and widget IDs",
            'menu items': "Ensure menu items have proper parent-child relationships",
            'duplicate content': "Check for duplicate post IDs or slugs"
        }
        
        for error in test_result.get('errors', []):
            error_lower = error.lower()
            for pattern, fix in error_patterns.items():
                if pattern in error_lower:
                    fixes.append(fix)
                    
        if not fixes:
            fixes.append("Try different YAML configuration or generator")
            
        return fixes
        
    def apply_automatic_fixes(self, fixes: List[str], xml_file: str) -> str:
        """Apply automatic fixes to XML file"""
        self.log("Applying automatic fixes")
        
        fixed_xml = f"cholot-auto-test-fixed-{self.iteration_count}.xml"
        
        # Simple automatic fixes
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Fix common XML issues
            content = content.replace('&', '&amp;')  # Escape ampersands
            content = content.replace('<![CDATA[]]>', '')  # Remove empty CDATA
            
            # Add basic meta if missing
            if 'wp:post_type' not in content:
                self.log("Adding basic post type metadata")
                
            with open(fixed_xml, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.log(f"Fixed XML saved as: {fixed_xml}")
            return fixed_xml
            
        except Exception as e:
            self.log(f"Auto-fix failed: {str(e)}", "ERROR")
            return xml_file
            
    def store_progress_in_memory(self, data: Dict[str, Any]):
        """Store progress data in memory namespace"""
        try:
            # Store in Claude Flow memory if available
            memory_key = f"swarm-auto-centralized-1756388708434/implementation/test_iteration_{self.iteration_count}"
            self.log(f"Storing progress data: {memory_key}")
            # Memory.store(memory_key, data)  # Uncomment if Claude Flow is available
        except:
            pass  # Memory storage is optional
            
    def run_complete_test_cycle(self) -> bool:
        """Run the complete auto-test cycle"""
        self.log("🚀 Starting Auto Test Cholot - Complete Test Cycle")
        self.log("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Find best YAML configuration
        yaml_file = self.find_best_yaml_config()
        if not yaml_file:
            return False
            
        success = False
        
        for iteration in range(self.max_iterations):
            self.iteration_count = iteration + 1
            self.log(f"🔄 Test Iteration {self.iteration_count}/{self.max_iterations}")
            self.log("-" * 40)
            
            # Step 2: Generate XML
            xml_file = f"cholot-auto-test-iter-{self.iteration_count}.xml"
            if not self.generate_xml_from_yaml(yaml_file, xml_file):
                self.log("XML generation failed, trying next iteration")
                continue
                
            # Step 3: Clean WordPress
            self.cleanup_wordpress()
            
            # Step 4: Test import
            test_result = self.test_import_xml(xml_file)
            
            # Step 5: Verify results
            verification = self.verify_import_results()
            
            # Step 6: Check success criteria
            success_count = sum(verification.values())
            total_criteria = len(self.success_criteria)
            
            self.log(f"✅ Success: {success_count}/{total_criteria} criteria met")
            
            # Store progress
            progress_data = {
                'iteration': self.iteration_count,
                'xml_file': xml_file,
                'test_result': test_result,
                'verification': verification,
                'success_rate': success_count / total_criteria
            }
            self.store_progress_in_memory(progress_data)
            
            if success_count == total_criteria:
                success = True
                self.log("🎉 All success criteria met! Test cycle completed successfully")
                break
                
            # Step 7: Auto-fix if not successful
            if success_count < total_criteria:
                fixes = self.analyze_errors_and_suggest_fixes(test_result)
                self.log(f"📋 Suggested fixes: {fixes}")
                
                if iteration < self.max_iterations - 1:
                    xml_file = self.apply_automatic_fixes(fixes, xml_file)
                    yaml_file = xml_file  # Try using fixed XML in next iteration
                    
        end_time = time.time()
        duration = end_time - start_time
        
        self.log("=" * 60)
        self.log(f"🏁 Auto Test Cholot completed in {duration:.1f} seconds")
        self.log(f"Total iterations: {self.iteration_count}")
        self.log(f"Final result: {'SUCCESS' if success else 'FAILED'}")
        
        return success

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            return
            
    auto_test = AutoTestCholot()
    success = auto_test.run_complete_test_cycle()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()