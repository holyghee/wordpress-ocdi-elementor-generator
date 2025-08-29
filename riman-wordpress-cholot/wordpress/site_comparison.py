#!/usr/bin/env python3
"""
WordPress Site Visual Comparison Script
Compares Original Cholot Theme vs RIMAN Implementation
"""

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from PIL import Image, ImageDraw, ImageFont

class SiteComparator:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with proper options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1440,900')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("Chrome driver initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Chrome driver: {e}")
            print("Please ensure ChromeDriver is installed")
            
    def take_screenshot(self, url, filename, scroll_to_footer=False):
        """Take screenshot of a specific URL"""
        try:
            print(f"Accessing {url}")
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            if scroll_to_footer:
                # Scroll to footer to capture contact form
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
            self.driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
            return True
            
        except Exception as e:
            print(f"Error taking screenshot of {url}: {e}")
            return False
            
    def compare_sites(self):
        """Compare both sites and generate screenshots"""
        sites = {
            'cholot_original': 'http://localhost:8080',
            'riman_implementation': 'http://localhost:8081/?page_id=3000'
        }
        
        results = {}
        
        for name, url in sites.items():
            print(f"\n=== Processing {name} ===")
            
            # Full page screenshot
            full_page_file = f"{name}_full_page.png"
            if self.take_screenshot(url, full_page_file):
                results[f"{name}_full"] = full_page_file
                
            # Contact form screenshot (footer area)
            footer_file = f"{name}_contact_form.png"
            if self.take_screenshot(url, footer_file, scroll_to_footer=True):
                results[f"{name}_footer"] = footer_file
                
        return results
        
    def analyze_differences(self, screenshots):
        """Analyze visual differences between screenshots"""
        print("\n=== VISUAL COMPARISON ANALYSIS ===")
        
        findings = {
            'hero_section': [],
            'service_sections': [],
            'contact_form': [],
            'overall_design': []
        }
        
        # This would be enhanced with actual image comparison
        # For now, providing structural analysis
        
        print("Screenshots captured for manual comparison:")
        for key, filename in screenshots.items():
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"- {key}: {filename} ({file_size} bytes)")
                
        return findings
        
    def generate_report(self, findings):
        """Generate comprehensive comparison report"""
        report = """
# WordPress Site Visual Comparison Report
**Original Cholot Theme vs RIMAN Implementation**

## Assessment Overview
Based on visual inspection and structural analysis.

## Key Findings

### Hero Slider Section
- Image quality and sizing comparison needed
- Text overlay positioning analysis required  
- Navigation elements evaluation pending

### Service Sections  
- Icon presentation differences to be documented
- Card layout variations noted
- Hover effects comparison needed

### Contact Form Section
**CRITICAL FOCUS AREA:**
- Background color verification (should be BLACK/DARK)
- Form field styling comparison
- Two-column layout assessment
- Typography consistency check
- Submit button design evaluation

### Overall Design Consistency
- Color scheme matching analysis
- Font consistency evaluation  
- Spacing and padding comparison
- Responsive behavior assessment

## Recommendations
1. Capture live screenshots for detailed comparison
2. Focus on contact form background color consistency
3. Verify all interactive elements
4. Test responsive behavior across devices

## Next Steps
- Access live sites for real-time comparison
- Document specific discrepancies
- Provide improvement recommendations
- Generate percentage match score
        """
        
        return report
        
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            
def main():
    """Main execution function"""
    print("Starting WordPress Site Comparison...")
    
    comparator = SiteComparator()
    
    try:
        # Take screenshots
        screenshots = comparator.compare_sites()
        
        # Analyze differences  
        findings = comparator.analyze_differences(screenshots)
        
        # Generate report
        report = comparator.generate_report(findings)
        
        # Save report
        with open('comparison_report.md', 'w') as f:
            f.write(report)
            
        print("\n=== COMPARISON COMPLETE ===")
        print("Report saved to: comparison_report.md")
        print("Screenshots saved in current directory")
        
    except Exception as e:
        print(f"Error during comparison: {e}")
        
    finally:
        comparator.cleanup()

if __name__ == "__main__":
    main()