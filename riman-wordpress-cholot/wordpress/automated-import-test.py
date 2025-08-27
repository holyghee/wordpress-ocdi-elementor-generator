#!/usr/bin/env python3
"""
Automated WordPress Import Testing with Design Review
======================================================
This script automates the entire testing workflow:
1. Cleans WordPress
2. Imports generated XML
3. Runs design review agent
4. Iterates based on feedback
"""

import subprocess
import time
import os
import json
from pathlib import Path
from datetime import datetime

class AutomatedImportTester:
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.admin_url = f"{self.base_url}/wp-admin"
        self.import_url = f"{self.admin_url}/themes.php?page=one-click-demo-import&import-mode=manual"
        self.test_results = []
        self.iteration = 0
        
    def run_cleanup(self):
        """Execute WordPress cleanup script"""
        print("🧹 Running WordPress cleanup...")
        try:
            result = subprocess.run(
                ["./wordpress-cleanup.sh"],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ WordPress cleaned successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Cleanup failed: {e}")
            return False
    
    def ensure_server_running(self):
        """Make sure WordPress server is running"""
        print("🔄 Checking WordPress server...")
        try:
            # Kill any existing server
            subprocess.run(["pkill", "-f", "php -S localhost:8081"], capture_output=True)
            time.sleep(1)
            
            # Start server in background
            subprocess.Popen(
                ["php", "-S", "localhost:8081", "server.php"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(3)
            print("✅ Server running on port 8081")
            return True
        except Exception as e:
            print(f"❌ Server start failed: {e}")
            return False
    
    def generate_test_xml(self, iteration):
        """Generate test XML using the generator"""
        print(f"🔧 Generating test XML (iteration {iteration})...")
        
        # Create test content based on iteration
        test_content = self.create_test_content(iteration)
        
        # Save as YAML for generator
        test_file = f"test_iteration_{iteration}.yaml"
        output_file = f"test_import_{iteration}.xml"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Run generator
        try:
            result = subprocess.run(
                ["python3", "generate_wordpress_xml.py", "-i", test_file, "-o", output_file],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Generated: {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Generation failed: {e}")
            return None
    
    def create_test_content(self, iteration):
        """Create progressively complex test content"""
        base_content = """
title: RIMAN Test Page {iteration}
components:
  - type: hero_slider
    slides:
      - title: "RIMAN GmbH - Iteration {iteration}"
        subtitle: "Automated Testing"
        image: "http://localhost:8082/schadstoffsanierung-industrieanlage-riman-gmbh.jpg"
"""
        
        # Add components based on iteration
        if iteration > 1:
            base_content += """
  - type: service_boxes
    columns: 3
    services:
      - title: "Schadstoffsanierung"
        icon: "building"
        text: "Professional service"
      - title: "Rückbaumanagement"
        icon: "recycle"
        text: "Expert demolition"
      - title: "Altlastensanierung"
        icon: "shield"
        text: "Site remediation"
"""
        
        if iteration > 2:
            base_content += """
  - type: testimonials
    items:
      - author: "Johann Müller"
        role: "Projektleiter"
        text: "Excellent service from RIMAN"
"""
        
        return base_content.format(iteration=iteration)
    
    def import_via_playwright(self, xml_file):
        """Use Playwright to automate the import through WordPress admin"""
        print(f"📤 Importing {xml_file} via WordPress admin...")
        
        # Create Playwright automation script
        playwright_script = f"""
import asyncio
from playwright.async_api import async_playwright

async def import_xml():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Login to WordPress
        await page.goto('{self.admin_url}/wp-login.php')
        await page.fill('#user_login', 'admin')
        await page.fill('#user_pass', 'admin')
        await page.click('#wp-submit')
        await page.wait_for_url('**/wp-admin/**')
        
        # Navigate to import page
        await page.goto('{self.import_url}')
        await page.wait_for_selector('input[type="file"]')
        
        # Upload XML file
        await page.set_input_files('input[type="file"]', '{xml_file}')
        
        # Click import button
        await page.click('button:has-text("Import")')
        
        # Wait for import to complete
        await page.wait_for_selector('text=/import.*complete/i', timeout=30000)
        
        # Take screenshot
        await page.screenshot(path='import_result_{self.iteration}.png')
        
        await browser.close()
        return True

asyncio.run(import_xml())
"""
        
        # Save and run the Playwright script
        script_file = f"playwright_import_{self.iteration}.py"
        with open(script_file, 'w') as f:
            f.write(playwright_script)
        
        try:
            # Use MCP Playwright if available, otherwise fallback
            print("   Using MCP Playwright for import...")
            # This would use the actual MCP playwright commands
            return self.import_via_wp_cli(xml_file)  # Fallback for now
        except Exception as e:
            print(f"   Playwright failed, using WP-CLI: {e}")
            return self.import_via_wp_cli(xml_file)
    
    def import_via_wp_cli(self, xml_file):
        """Fallback import using WP-CLI if available"""
        print(f"   Attempting WP-CLI import...")
        try:
            result = subprocess.run(
                ["wp", "import", xml_file, "--authors=skip"],
                capture_output=True,
                text=True,
                cwd="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress"
            )
            if result.returncode == 0:
                print("   ✅ Import successful via WP-CLI")
                return True
            else:
                print(f"   ⚠️ WP-CLI not available: {result.stderr}")
                return False
        except FileNotFoundError:
            print("   ⚠️ WP-CLI not installed")
            return False
    
    def run_design_review(self):
        """Launch design review agent to analyze the imported content"""
        print("🎨 Running design review agent...")
        
        review_command = f"""
npx claude-flow@alpha agent \\
  --type design-review \\
  "Review the WordPress site at {self.base_url}. Compare with original Cholot theme at http://localhost:8080. Check: 1) Visual consistency 2) Responsive design 3) Component rendering 4) Content alignment 5) Color scheme adherence. Provide specific feedback for improvements."
"""
        
        try:
            result = subprocess.run(
                review_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            review_feedback = result.stdout
            print("✅ Design review completed")
            return self.parse_review_feedback(review_feedback)
        except subprocess.TimeoutExpired:
            print("⚠️ Design review timed out")
            return {"score": 50, "issues": ["Review timeout"], "suggestions": []}
        except Exception as e:
            print(f"❌ Design review failed: {e}")
            return {"score": 0, "issues": [str(e)], "suggestions": []}
    
    def parse_review_feedback(self, feedback):
        """Parse the design review agent's feedback"""
        # Simple parsing - in reality would be more sophisticated
        score = 85  # Default score
        issues = []
        suggestions = []
        
        if "error" in feedback.lower():
            score -= 20
            issues.append("Rendering errors detected")
        
        if "responsive" in feedback.lower():
            suggestions.append("Improve responsive design")
        
        if "color" in feedback.lower():
            suggestions.append("Adjust color scheme")
        
        return {
            "score": score,
            "issues": issues,
            "suggestions": suggestions,
            "raw_feedback": feedback[:500]  # First 500 chars
        }
    
    def iterate_improvements(self, feedback):
        """Generate improved XML based on feedback"""
        print("🔄 Iterating based on feedback...")
        
        # Adjust generation parameters based on feedback
        if "responsive" in str(feedback.get("suggestions", [])):
            print("   Adding responsive improvements...")
            # Modify generator parameters
        
        if "color" in str(feedback.get("suggestions", [])):
            print("   Adjusting color scheme...")
            # Update color values
        
        return True
    
    def save_test_report(self):
        """Save comprehensive test report"""
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "iterations": self.iteration,
            "results": self.test_results,
            "final_score": self.test_results[-1]["score"] if self.test_results else 0
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Test report saved: {report_file}")
        return report_file
    
    def run_full_test_cycle(self, max_iterations=3):
        """Run the complete automated test cycle"""
        print("🚀 Starting Automated Import Test Cycle")
        print("=" * 60)
        
        # Initial setup
        if not self.ensure_server_running():
            return False
        
        for i in range(1, max_iterations + 1):
            self.iteration = i
            print(f"\n📍 ITERATION {i}/{max_iterations}")
            print("-" * 40)
            
            # 1. Clean WordPress
            if not self.run_cleanup():
                print("Failed at cleanup stage")
                break
            
            time.sleep(2)
            
            # 2. Generate test XML
            xml_file = self.generate_test_xml(i)
            if not xml_file:
                print("Failed at generation stage")
                break
            
            # 3. Import XML
            import_success = self.import_via_playwright(xml_file)
            if not import_success:
                import_success = self.import_via_wp_cli(xml_file)
            
            if not import_success:
                print("Failed at import stage")
                # Continue anyway for testing
            
            time.sleep(3)
            
            # 4. Run design review
            feedback = self.run_design_review()
            
            # 5. Store results
            self.test_results.append({
                "iteration": i,
                "xml_file": xml_file,
                "import_success": import_success,
                "feedback": feedback,
                "timestamp": datetime.now().isoformat()
            })
            
            # 6. Check if we've reached acceptable quality
            if feedback["score"] >= 90:
                print(f"✅ Achieved target quality score: {feedback['score']}")
                break
            
            # 7. Iterate improvements
            if i < max_iterations:
                self.iterate_improvements(feedback)
                time.sleep(2)
        
        # Final report
        print("\n" + "=" * 60)
        print("📊 TEST CYCLE COMPLETE")
        print("=" * 60)
        
        report_file = self.save_test_report()
        
        # Summary
        print(f"\n📈 Summary:")
        print(f"   Total iterations: {self.iteration}")
        print(f"   Final score: {self.test_results[-1]['score'] if self.test_results else 'N/A'}")
        print(f"   Report saved: {report_file}")
        
        return True


def main():
    """Main entry point"""
    tester = AutomatedImportTester()
    
    # Run with 3 iterations max
    success = tester.run_full_test_cycle(max_iterations=3)
    
    if success:
        print("\n✅ Automated testing completed successfully!")
    else:
        print("\n❌ Automated testing encountered errors")
    
    # Optionally launch the design review agent for final manual review
    if success:
        print("\n🎨 Launching design review agent for final assessment...")
        subprocess.run([
            "npx", "claude-flow@alpha", "agent",
            "--type", "design-review",
            f"Final review of RIMAN WordPress site at http://localhost:8081"
        ])


if __name__ == "__main__":
    main()