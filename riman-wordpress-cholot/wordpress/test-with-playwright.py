#!/usr/bin/env python3
"""
WordPress Import Test with Direct Playwright Control
"""

import subprocess
import time
import os

def cleanup_wordpress():
    """Run WordPress cleanup"""
    print("🧹 Cleaning WordPress...")
    subprocess.run(["./wordpress-cleanup.sh"], check=True)
    print("✅ WordPress cleaned\n")

def start_server():
    """Start WordPress server"""
    print("🔄 Starting WordPress server...")
    subprocess.run(["pkill", "-f", "php -S localhost:8081"], capture_output=True)
    time.sleep(1)
    proc = subprocess.Popen(
        ["php", "-S", "localhost:8081", "server.php"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    print("✅ Server running on port 8081\n")
    return proc

def import_xml_manual(xml_file):
    """Guide user through manual import"""
    print(f"📤 MANUAL IMPORT REQUIRED:")
    print("=" * 40)
    print(f"1. Open: http://localhost:8081/wp-admin")
    print(f"2. Login: admin / admin")
    print(f"3. Navigate: Tools → Import → WordPress")
    print(f"4. Upload: {xml_file}")
    print(f"5. Click: Run Importer")
    print(f"6. Check: 'Download and import file attachments'")
    print(f"7. Click: Submit")
    print()
    input("Press ENTER when import is complete...")
    print()

def run_playwright_review():
    """Use Playwright MCP to review the site"""
    print("🎨 Running Playwright Design Review...")
    print("=" * 40)
    
    # This would use the actual MCP Playwright commands
    # For now, we'll use a subprocess call to Task agent
    
    review_script = """
    # Navigate to site
    mcp__playwright__browser_navigate http://localhost:8081
    
    # Take screenshot
    mcp__playwright__browser_take_screenshot
    
    # Check for errors
    mcp__playwright__browser_console_messages
    
    # Test responsive
    mcp__playwright__browser_resize 375 667  # Mobile
    mcp__playwright__browser_take_screenshot mobile.png
    
    mcp__playwright__browser_resize 768 1024  # Tablet
    mcp__playwright__browser_take_screenshot tablet.png
    
    mcp__playwright__browser_resize 1920 1080  # Desktop
    mcp__playwright__browser_take_screenshot desktop.png
    """
    
    print("Would run Playwright commands:")
    print(review_script)
    print()
    
    # Fallback to manual review
    print("📋 MANUAL REVIEW CHECKLIST:")
    print("=" * 40)
    print("[ ] Homepage loads correctly")
    print("[ ] Images load from http://localhost:8082")
    print("[ ] Color scheme uses #b68c2f (gold)")
    print("[ ] All Cholot widgets render")
    print("[ ] Responsive design works")
    print("[ ] No console errors")
    print()

def main():
    print("🚀 WordPress Import Test System")
    print("=" * 40)
    print()
    
    # Step 1: Cleanup
    cleanup_wordpress()
    
    # Step 2: Start server
    server_proc = start_server()
    
    try:
        # Step 3: Select XML
        print("📄 Available test files:")
        print("1. demo_yaml_format.xml")
        print("2. demo_widget_showcase.xml")
        print("3. demo_customization.xml")
        print()
        
        choice = input("Select file (1-3): ") or "1"
        files = {
            "1": "demo_yaml_format.xml",
            "2": "demo_widget_showcase.xml",
            "3": "demo_customization.xml"
        }
        xml_file = files.get(choice, "demo_yaml_format.xml")
        print(f"✅ Selected: {xml_file}\n")
        
        # Step 4: Import
        import_xml_manual(xml_file)
        
        # Step 5: Review
        run_playwright_review()
        
        # Step 6: Results
        print("📊 TEST COMPLETE")
        print("=" * 40)
        print("View site: http://localhost:8081")
        print()
        
    finally:
        # Cleanup
        print("\n🧹 Shutting down server...")
        server_proc.terminate()

if __name__ == "__main__":
    main()