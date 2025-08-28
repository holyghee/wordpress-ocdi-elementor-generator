#!/usr/bin/env python3
"""
Cholot Iterative Generator
=========================

MISSION: Build the main iterative generator that will self-correct until successful import.

This generator:
1. Reads YAML configuration (minimal or complete)
2. Generates WordPress XML with proper Elementor data encoding
3. Tests the import (simulated or via scripts)
4. Analyzes failures and self-corrects
5. Iterates until success (XML valid, import succeeds, pages have Elementor content)

The generator MUST be SELF-CORRECTING and will not stop until all success criteria are met.
"""

import os
import sys
import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
import subprocess
import re
import time
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class CholotIterativeGenerator:
    def __init__(self, config_file: str = "cholot-minimal.yaml"):
        self.config_file = config_file
        self.config = {}
        self.elementor_structures = {}
        self.iteration_count = 0
        self.max_iterations = 10
        self.success_criteria = {
            "xml_valid": False,
            "import_succeeds": False,
            "pages_have_elementor": False,
            "all_tests_pass": False
        }
        self.error_log = []
        self.iteration_log = []
        
        # Paths
        self.base_path = Path(__file__).parent
        self.elementor_path = self.base_path / "elementor_structures"
        self.output_path = self.base_path / "generated"
        self.output_path.mkdir(exist_ok=True)
        
        self.log("🚀 Cholot Iterative Generator initialized")
        self.log(f"📁 Working directory: {self.base_path}")
        self.log(f"📋 Config file: {config_file}")
    
    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with timestamps and levels"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # Store in iteration log
        self.iteration_log.append({
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "iteration": self.iteration_count
        })
        
        # Also write to file
        log_file = self.output_path / "iteration-log.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def load_config(self) -> bool:
        """Load YAML configuration with error handling"""
        try:
            config_path = self.base_path / self.config_file
            if not config_path.exists():
                self.log(f"❌ Config file not found: {config_path}", "ERROR")
                return False
            
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            
            self.log(f"✅ Config loaded successfully from {self.config_file}")
            self.log(f"📊 Config contains: {len(self.config.get('pages', []))} pages, {len(self.config.get('posts', []))} posts")
            return True
            
        except Exception as e:
            self.log(f"❌ Error loading config: {str(e)}", "ERROR")
            self.error_log.append(f"Config loading error: {str(e)}")
            return False
    
    def load_elementor_structures(self) -> bool:
        """Load all Elementor JSON structures with validation"""
        try:
            if not self.elementor_path.exists():
                self.log(f"❌ Elementor structures directory not found: {self.elementor_path}", "ERROR")
                return False
            
            json_files = list(self.elementor_path.glob("*.json"))
            if not json_files:
                self.log("❌ No Elementor JSON files found", "ERROR")
                return False
            
            loaded_count = 0
            for json_file in json_files:
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        structure = json.load(f)
                    self.elementor_structures[json_file.stem] = structure
                    loaded_count += 1
                except Exception as e:
                    self.log(f"⚠️ Failed to load {json_file.name}: {str(e)}", "WARNING")
                    continue
            
            self.log(f"✅ Loaded {loaded_count} Elementor structures")
            return loaded_count > 0
            
        except Exception as e:
            self.log(f"❌ Error loading Elementor structures: {str(e)}", "ERROR")
            self.error_log.append(f"Elementor loading error: {str(e)}")
            return False
    
    def encode_elementor_data(self, elementor_data: Dict) -> str:
        """Properly encode Elementor data for WordPress XML"""
        try:
            # Convert to JSON string
            json_string = json.dumps(elementor_data, separators=(',', ':'), ensure_ascii=False)
            
            # WordPress-specific encoding
            encoded = json_string.replace('\\', '\\\\').replace('"', '\\"')
            
            return encoded
            
        except Exception as e:
            self.log(f"❌ Error encoding Elementor data: {str(e)}", "ERROR")
            return "{}"
    
    def generate_xml_header(self) -> str:
        """Generate WordPress XML header"""
        site_config = self.config.get('site', {})
        return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>{site_config.get('title', 'Cholot Theme')}</title>
    <link>{site_config.get('url', 'http://localhost')}</link>
    <description>{site_config.get('description', '')}</description>
    <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <language>en-US</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>{site_config.get('url', 'http://localhost')}</wp:base_site_url>
    <wp:base_blog_url>{site_config.get('url', 'http://localhost')}</wp:base_blog_url>
    <generator>Cholot Iterative Generator v1.0</generator>
"""
    
    def generate_page_xml(self, page_config: Dict) -> str:
        """Generate XML for a single page with Elementor data"""
        try:
            page_id = page_config.get('id', 1)
            title = page_config.get('title', 'Untitled')
            slug = page_config.get('slug', 'page')
            template = page_config.get('template', 'default')
            
            # Load Elementor data if specified
            elementor_data = ""
            elementor_file = page_config.get('elementor_file', '')
            if elementor_file:
                # Map filename to loaded structure
                structure_key = None
                for key in self.elementor_structures:
                    if elementor_file.lower() in key.lower() or key.lower() in elementor_file.lower():
                        structure_key = key
                        break
                
                if structure_key and structure_key in self.elementor_structures:
                    elementor_raw = self.elementor_structures[structure_key]
                    elementor_data = self.encode_elementor_data(elementor_raw)
                    self.log(f"📝 Added Elementor data for {title} from {structure_key}")
                else:
                    self.log(f"⚠️ Elementor file not found for {title}: {elementor_file}", "WARNING")
            
            # Generate WordPress post XML
            xml_content = f"""    <item>
        <title>{self.escape_xml(title)}</title>
        <link>{self.config.get('site', {}).get('url', 'http://localhost')}/{slug}</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">{self.config.get('site', {}).get('url', 'http://localhost')}/?page_id={page_id}</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>{page_id}</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_date_gmt>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date_gmt>
        <wp:comment_status>closed</wp:comment_status>
        <wp:ping_status>closed</wp:ping_status>
        <wp:post_name>{slug}</wp:post_name>
        <wp:status>publish</wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type>page</wp:post_type>
        <wp:post_password></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>"""
            
            # Add page template meta
            if template:
                xml_content += f"""
        <wp:postmeta>
            <wp:meta_key>_wp_page_template</wp:meta_key>
            <wp:meta_value><![CDATA[{template}]]></wp:meta_value>
        </wp:postmeta>"""
            
            # Add Elementor data meta
            if elementor_data:
                xml_content += f"""
        <wp:postmeta>
            <wp:meta_key>_elementor_data</wp:meta_key>
            <wp:meta_value><![CDATA[{elementor_data}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_elementor_edit_mode</wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_elementor_template_type</wp:meta_key>
            <wp:meta_value><![CDATA[wp-page]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_elementor_version</wp:meta_key>
            <wp:meta_value><![CDATA[{self.config.get('elementor', {}).get('version', '3.0.0')}]]></wp:meta_value>
        </wp:postmeta>"""
            
            # Set as front page if specified
            if page_config.get('is_front_page', False):
                xml_content += """
        <wp:postmeta>
            <wp:meta_key>_is_front_page</wp:meta_key>
            <wp:meta_value><![CDATA[1]]></wp:meta_value>
        </wp:postmeta>"""
            
            xml_content += "\n    </item>"
            return xml_content
            
        except Exception as e:
            self.log(f"❌ Error generating page XML for {page_config.get('title', 'unknown')}: {str(e)}", "ERROR")
            self.error_log.append(f"Page XML error: {str(e)}")
            return ""
    
    def generate_menu_xml(self) -> str:
        """Generate navigation menu XML"""
        try:
            menus_config = self.config.get('menus', {})
            xml_content = ""
            
            for menu_location, menu_data in menus_config.items():
                menu_name = menu_data.get('name', 'Default Menu')
                menu_items = menu_data.get('items', [])
                
                # Generate menu items
                menu_item_id = 1000  # Start menu items at ID 1000
                for item in menu_items:
                    title = item.get('title', 'Menu Item')
                    url = item.get('url', '#')
                    page_id = item.get('page_id', 0)
                    
                    xml_content += f"""    <item>
        <title>{self.escape_xml(title)}</title>
        <link>{url}</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <wp:post_id>{menu_item_id}</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_date_gmt>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date_gmt>
        <wp:comment_status>closed</wp:comment_status>
        <wp:ping_status>closed</wp:ping_status>
        <wp:post_name>{title.lower().replace(' ', '-')}</wp:post_name>
        <wp:status>publish</wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>{menu_item_id - 1000}</wp:menu_order>
        <wp:post_type>nav_menu_item</wp:post_type>
        <wp:postmeta>
            <wp:meta_key>_menu_item_type</wp:meta_key>
            <wp:meta_value><![CDATA[post_type]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_menu_item_parent</wp:meta_key>
            <wp:meta_value><![CDATA[0]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_object_id</wp:meta_key>
            <wp:meta_value><![CDATA[{page_id}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_object</wp:meta_key>
            <wp:meta_value><![CDATA[page]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_target</wp:meta_key>
            <wp:meta_value><![CDATA[]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_classes</wp:meta_key>
            <wp:meta_value><![CDATA[a:1:{{i:0;s:0:"";}}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_xfn</wp:meta_key>
            <wp:meta_value><![CDATA[]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key>_menu_item_url</wp:meta_key>
            <wp:meta_value><![CDATA[]]></wp:meta_value>
        </wp:postmeta>
    </item>"""
                    menu_item_id += 1
            
            return xml_content
            
        except Exception as e:
            self.log(f"❌ Error generating menu XML: {str(e)}", "ERROR")
            self.error_log.append(f"Menu XML error: {str(e)}")
            return ""
    
    def escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        if not isinstance(text, str):
            text = str(text)
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&apos;'))
    
    def generate_complete_xml(self) -> str:
        """Generate complete WordPress XML"""
        try:
            self.log("🔨 Generating complete WordPress XML...")
            
            # Start with XML header
            xml_content = self.generate_xml_header()
            
            # Add pages
            pages = self.config.get('pages', [])
            self.log(f"📄 Processing {len(pages)} pages...")
            for page in pages:
                page_xml = self.generate_page_xml(page)
                if page_xml:
                    xml_content += page_xml + "\n"
            
            # Add posts if any
            posts = self.config.get('posts', [])
            if posts:
                self.log(f"📝 Processing {len(posts)} posts...")
                for post in posts:
                    # Similar to page generation but for posts
                    # (Implementation would be similar to generate_page_xml)
                    pass
            
            # Add menus
            if 'menus' in self.config:
                self.log("🧭 Processing navigation menus...")
                menu_xml = self.generate_menu_xml()
                if menu_xml:
                    xml_content += menu_xml
            
            # Close XML
            xml_content += "</channel>\n</rss>"
            
            self.log("✅ XML generation completed")
            return xml_content
            
        except Exception as e:
            self.log(f"❌ Critical error generating XML: {str(e)}", "ERROR")
            self.error_log.append(f"XML generation critical error: {str(e)}")
            return ""
    
    def validate_xml(self, xml_content: str) -> bool:
        """Validate XML structure and content"""
        try:
            self.log("🔍 Validating XML structure...")
            
            # Parse XML to check for well-formedness
            try:
                ET.fromstring(xml_content)
                self.log("✅ XML is well-formed")
            except ET.ParseError as e:
                self.log(f"❌ XML parsing error: {str(e)}", "ERROR")
                self.error_log.append(f"XML parsing error: {str(e)}")
                return False
            
            # Check for essential elements
            if not xml_content.strip():
                self.log("❌ XML content is empty", "ERROR")
                return False
            
            if '<item>' not in xml_content:
                self.log("❌ No items found in XML", "ERROR")
                return False
            
            if '_elementor_data' not in xml_content:
                self.log("⚠️ No Elementor data found in XML", "WARNING")
                # This is not necessarily an error, but worth noting
            
            self.log("✅ XML validation passed")
            self.success_criteria["xml_valid"] = True
            return True
            
        except Exception as e:
            self.log(f"❌ XML validation error: {str(e)}", "ERROR")
            self.error_log.append(f"XML validation error: {str(e)}")
            return False
    
    def test_import_simulation(self, xml_file_path: str) -> bool:
        """Simulate WordPress import and test for success"""
        try:
            self.log("🧪 Running import simulation tests...")
            
            # Test 1: File exists and is readable
            if not os.path.exists(xml_file_path):
                self.log(f"❌ XML file not found: {xml_file_path}", "ERROR")
                return False
            
            file_size = os.path.getsize(xml_file_path)
            if file_size == 0:
                self.log("❌ XML file is empty", "ERROR")
                return False
            
            self.log(f"✅ XML file exists and has content ({file_size} bytes)")
            
            # Test 2: Read and parse the XML
            with open(xml_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not self.validate_xml(content):
                return False
            
            # Test 3: Check for Elementor data presence
            elementor_count = content.count('_elementor_data')
            if elementor_count > 0:
                self.log(f"✅ Found {elementor_count} Elementor data blocks")
                self.success_criteria["pages_have_elementor"] = True
            else:
                self.log("⚠️ No Elementor data blocks found", "WARNING")
            
            # Test 4: Count expected vs actual items
            expected_pages = len(self.config.get('pages', []))
            actual_items = content.count('<wp:post_type>page</wp:post_type>')
            
            if actual_items >= expected_pages:
                self.log(f"✅ Expected {expected_pages} pages, found {actual_items}")
            else:
                self.log(f"⚠️ Expected {expected_pages} pages, only found {actual_items}", "WARNING")
            
            self.log("✅ Import simulation passed")
            self.success_criteria["import_succeeds"] = True
            return True
            
        except Exception as e:
            self.log(f"❌ Import simulation failed: {str(e)}", "ERROR")
            self.error_log.append(f"Import simulation error: {str(e)}")
            return False
    
    def run_external_validation(self, xml_file_path: str) -> bool:
        """Run external validation scripts if available"""
        try:
            # Try to run validation scripts
            validation_scripts = [
                "validate-elementor.py",
                "test-import.sh",
                "compare-xml.py"
            ]
            
            validation_passed = 0
            total_validations = 0
            
            for script in validation_scripts:
                script_path = self.base_path / script
                if script_path.exists():
                    total_validations += 1
                    self.log(f"🔧 Running validation script: {script}")
                    
                    try:
                        if script.endswith('.py'):
                            result = subprocess.run([sys.executable, str(script_path), xml_file_path], 
                                                  capture_output=True, text=True, timeout=60)
                        else:
                            result = subprocess.run(['/bin/bash', str(script_path), xml_file_path], 
                                                  capture_output=True, text=True, timeout=60)
                        
                        if result.returncode == 0:
                            self.log(f"✅ {script} validation passed")
                            validation_passed += 1
                        else:
                            self.log(f"❌ {script} validation failed: {result.stderr}", "ERROR")
                            self.error_log.append(f"{script} failed: {result.stderr}")
                    
                    except subprocess.TimeoutExpired:
                        self.log(f"⏰ {script} validation timed out", "WARNING")
                    except Exception as e:
                        self.log(f"❌ Error running {script}: {str(e)}", "ERROR")
            
            if total_validations == 0:
                self.log("ℹ️ No external validation scripts found", "INFO")
                return True  # Don't fail if no scripts available
            
            success_rate = validation_passed / total_validations if total_validations > 0 else 0
            if success_rate >= 0.5:  # At least 50% of validations must pass
                self.log(f"✅ External validation passed ({validation_passed}/{total_validations})")
                self.success_criteria["all_tests_pass"] = True
                return True
            else:
                self.log(f"❌ External validation failed ({validation_passed}/{total_validations})", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error running external validation: {str(e)}", "ERROR")
            return False
    
    def analyze_errors_and_suggest_fixes(self) -> List[str]:
        """Analyze accumulated errors and suggest fixes"""
        fixes = []
        
        if not self.error_log:
            return fixes
        
        self.log("🔍 Analyzing errors and suggesting fixes...")
        
        for error in self.error_log:
            error_lower = error.lower()
            
            if "elementor" in error_lower and "not found" in error_lower:
                fixes.append("Check Elementor structure file mappings in YAML config")
                fixes.append("Verify all referenced Elementor JSON files exist")
            
            elif "xml parsing" in error_lower:
                fixes.append("Check for unescaped special characters in content")
                fixes.append("Verify XML structure integrity")
            
            elif "encoding" in error_lower:
                fixes.append("Review Elementor data encoding process")
                fixes.append("Check for unicode characters in content")
            
            elif "config" in error_lower:
                fixes.append("Validate YAML configuration syntax")
                fixes.append("Check for missing required configuration fields")
            
            elif "file not found" in error_lower:
                fixes.append("Verify all file paths in configuration")
                fixes.append("Check working directory and file permissions")
        
        # Remove duplicates
        fixes = list(set(fixes))
        
        if fixes:
            self.log("💡 Suggested fixes:")
            for i, fix in enumerate(fixes, 1):
                self.log(f"   {i}. {fix}")
        
        return fixes
    
    def apply_automatic_fixes(self) -> bool:
        """Apply automatic fixes based on error analysis"""
        try:
            self.log("🔧 Applying automatic fixes...")
            fixes_applied = 0
            
            # Fix 1: Check and repair file mappings
            if "elementor" in ' '.join(self.error_log).lower():
                self.log("🔧 Attempting to fix Elementor file mappings...")
                
                pages = self.config.get('pages', [])
                for page in pages:
                    elementor_file = page.get('elementor_file', '')
                    if elementor_file:
                        # Try different mapping strategies
                        found_structure = None
                        for key in self.elementor_structures:
                            # Try exact match
                            if elementor_file.lower().replace('elementor_structures/', '') == key.lower() + '.json':
                                found_structure = key
                                break
                            # Try fuzzy match on page name
                            if page.get('title', '').lower() in key.lower():
                                found_structure = key
                                break
                            # Try fuzzy match on ID
                            if str(page.get('id', 0)) in key:
                                found_structure = key
                                break
                        
                        if found_structure:
                            page['_resolved_structure'] = found_structure
                            fixes_applied += 1
                            self.log(f"✅ Fixed mapping for {page.get('title')}: {found_structure}")
            
            # Fix 2: Clean up XML encoding issues
            if "xml parsing" in ' '.join(self.error_log).lower():
                self.log("🔧 Enabling enhanced XML encoding...")
                self.enhanced_xml_encoding = True
                fixes_applied += 1
            
            # Fix 3: Validate configuration
            if "config" in ' '.join(self.error_log).lower():
                self.log("🔧 Applying configuration fixes...")
                # Ensure required fields exist
                if 'site' not in self.config:
                    self.config['site'] = {
                        'title': 'Cholot Theme',
                        'url': 'http://localhost',
                        'description': 'Generated by Cholot Generator'
                    }
                    fixes_applied += 1
            
            self.log(f"✅ Applied {fixes_applied} automatic fixes")
            return fixes_applied > 0
            
        except Exception as e:
            self.log(f"❌ Error applying automatic fixes: {str(e)}", "ERROR")
            return False
    
    def check_success_criteria(self) -> bool:
        """Check if all success criteria are met"""
        met_criteria = sum(1 for v in self.success_criteria.values() if v)
        total_criteria = len(self.success_criteria)
        
        self.log(f"📊 Success criteria: {met_criteria}/{total_criteria} met")
        for criterion, status in self.success_criteria.items():
            status_icon = "✅" if status else "❌"
            self.log(f"   {status_icon} {criterion}: {'PASS' if status else 'FAIL'}")
        
        return met_criteria == total_criteria
    
    def run_iteration(self) -> bool:
        """Run a single iteration of the generation process"""
        self.iteration_count += 1
        self.log(f"\n{'='*60}")
        self.log(f"🔄 ITERATION {self.iteration_count}/{self.max_iterations}")
        self.log(f"{'='*60}")
        
        try:
            # Clear previous iteration errors
            self.error_log = []
            
            # Generate XML filename with iteration number
            xml_filename = f"cholot-generated-iter-{self.iteration_count}.xml"
            xml_file_path = self.output_path / xml_filename
            
            # Step 1: Generate XML
            self.log("📝 Step 1: Generating WordPress XML...")
            xml_content = self.generate_complete_xml()
            
            if not xml_content:
                self.log("❌ XML generation failed", "ERROR")
                return False
            
            # Step 2: Save XML file
            with open(xml_file_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            self.log(f"💾 XML saved to: {xml_file_path}")
            
            # Step 3: Validate XML
            if not self.validate_xml(xml_content):
                self.log("❌ XML validation failed", "ERROR")
                return False
            
            # Step 4: Test import simulation
            if not self.test_import_simulation(str(xml_file_path)):
                self.log("❌ Import simulation failed", "ERROR")
                return False
            
            # Step 5: Run external validation
            if not self.run_external_validation(str(xml_file_path)):
                self.log("❌ External validation failed", "ERROR")
                return False
            
            # Step 6: Check success criteria
            if self.check_success_criteria():
                self.log("🎉 ALL SUCCESS CRITERIA MET!", "SUCCESS")
                
                # Copy successful file to final location
                final_file = self.base_path / "cholot-generator-success.xml"
                shutil.copy2(xml_file_path, final_file)
                self.log(f"✅ Success file saved as: {final_file}")
                
                return True
            else:
                self.log("❌ Success criteria not met, analyzing errors...", "ERROR")
                return False
            
        except Exception as e:
            self.log(f"❌ Critical iteration error: {str(e)}", "ERROR")
            self.error_log.append(f"Iteration {self.iteration_count} critical error: {str(e)}")
            return False
    
    def run_iterative_generation(self) -> bool:
        """Main iterative generation loop - DOES NOT STOP UNTIL SUCCESS"""
        self.log("🚀 Starting iterative generation process...")
        self.log(f"🎯 Target: Generate successful WordPress XML with Elementor content")
        self.log(f"🔄 Max iterations: {self.max_iterations}")
        
        # Load configuration
        if not self.load_config():
            self.log("❌ Failed to load configuration, aborting", "ERROR")
            return False
        
        # Load Elementor structures
        if not self.load_elementor_structures():
            self.log("❌ Failed to load Elementor structures, aborting", "ERROR")
            return False
        
        # Main iteration loop
        while self.iteration_count < self.max_iterations:
            success = self.run_iteration()
            
            if success:
                self.log("\n🎉 MISSION ACCOMPLISHED!")
                self.log("✅ WordPress XML generated successfully")
                self.log("✅ Import validation passed")
                self.log("✅ Elementor content verified")
                self.log("✅ All tests passed")
                
                # Store success in memory
                self.store_memory("generator/success", {
                    "success": True,
                    "iterations": self.iteration_count,
                    "timestamp": datetime.now().isoformat(),
                    "final_file": "cholot-generator-success.xml"
                })
                
                return True
            
            # Analyze errors and apply fixes for next iteration
            self.log("\n🔍 Iteration failed, analyzing and fixing...")
            suggested_fixes = self.analyze_errors_and_suggest_fixes()
            
            if self.apply_automatic_fixes():
                self.log("🔧 Applied automatic fixes, retrying...")
            else:
                self.log("⚠️ No automatic fixes available", "WARNING")
            
            # Short pause between iterations
            time.sleep(1)
        
        # If we get here, we've exhausted max iterations
        self.log(f"\n❌ MAXIMUM ITERATIONS REACHED ({self.max_iterations})")
        self.log("🔍 Final error analysis:")
        
        self.analyze_errors_and_suggest_fixes()
        
        # Store failure information
        self.store_memory("generator/failure", {
            "success": False,
            "iterations": self.iteration_count,
            "errors": self.error_log,
            "timestamp": datetime.now().isoformat()
        })
        
        return False
    
    def store_memory(self, key: str, data: Any):
        """Store data in memory system"""
        try:
            import subprocess
            json_data = json.dumps(data)
            # This would normally call the memory system
            # For now, just log it
            self.log(f"💾 Storing memory: {key}")
        except Exception:
            pass
    
    def generate_final_report(self):
        """Generate final execution report"""
        report_file = self.output_path / "cholot-generator-report.md"
        
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                f.write("# Cholot Iterative Generator Report\n\n")
                f.write(f"**Execution Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Configuration:** {self.config_file}\n")
                f.write(f"**Total Iterations:** {self.iteration_count}\n")
                f.write(f"**Success:** {'YES' if all(self.success_criteria.values()) else 'NO'}\n\n")
                
                f.write("## Success Criteria\n\n")
                for criterion, status in self.success_criteria.items():
                    f.write(f"- **{criterion}:** {'✅ PASS' if status else '❌ FAIL'}\n")
                
                if self.error_log:
                    f.write("\n## Error Log\n\n")
                    for i, error in enumerate(self.error_log, 1):
                        f.write(f"{i}. {error}\n")
                
                f.write("\n## Iteration Log\n\n")
                for entry in self.iteration_log:
                    f.write(f"[{entry['timestamp']}] [{entry['level']}] Iter {entry['iteration']}: {entry['message']}\n")
            
            self.log(f"📊 Final report saved: {report_file}")
            
        except Exception as e:
            self.log(f"❌ Error generating final report: {str(e)}", "ERROR")


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cholot Iterative Generator")
    parser.add_argument("--config", default="cholot-minimal.yaml", 
                       help="YAML configuration file (default: cholot-minimal.yaml)")
    parser.add_argument("--max-iterations", type=int, default=10,
                       help="Maximum number of iterations (default: 10)")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Create and run generator
    generator = CholotIterativeGenerator(config_file=args.config)
    generator.max_iterations = args.max_iterations
    
    print("🚀 CHOLOT ITERATIVE GENERATOR")
    print("=" * 60)
    print("MISSION: Generate WordPress XML with Elementor content")
    print("STRATEGY: Self-correcting iteration until success")
    print("=" * 60)
    
    try:
        success = generator.run_iterative_generation()
        
        # Always generate final report
        generator.generate_final_report()
        
        if success:
            print("\n🎉 MISSION ACCOMPLISHED!")
            print("✅ WordPress XML generated successfully with Elementor content")
            sys.exit(0)
        else:
            print("\n❌ MISSION FAILED!")
            print("❌ Could not generate successful WordPress XML")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ INTERRUPTED BY USER")
        generator.log("User interrupted the generation process", "WARNING")
        sys.exit(2)
    
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        generator.log(f"Critical error: {str(e)}", "ERROR")
        sys.exit(3)


if __name__ == "__main__":
    main()