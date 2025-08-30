#!/usr/bin/env python3
"""
Compare Current Implementation vs Original Cholot Theme
"""

import asyncio
from playwright.async_api import async_playwright
import time

async def compare_sites():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        
        # Create two pages for side-by-side comparison
        current_page = await context.new_page()
        original_page = await context.new_page()
        
        try:
            print("📸 Capturing current implementation (localhost:8081)...")
            await current_page.goto('http://localhost:8081/?page_id=3000', wait_until='networkidle')
            await current_page.wait_for_timeout(2000)  # Allow time for dynamic content
            await current_page.screenshot(path='current_implementation.png', full_page=True)
            
            # Get page content for analysis
            current_html = await current_page.content()
            current_title = await current_page.title()
            
            # Check for cholot-texticon widgets
            texticon_widgets = await current_page.query_selector_all('.cholot-texticon')
            service_cards = await current_page.query_selector_all('.service-card, .services-section, [class*="service"]')
            
            print(f"Current page title: {current_title}")
            print(f"Found {len(texticon_widgets)} cholot-texticon widgets")
            print(f"Found {len(service_cards)} potential service card elements")
            
            print("\n📸 Capturing original theme (localhost:8080)...")
            await original_page.goto('http://localhost:8080', wait_until='networkidle')
            await original_page.wait_for_timeout(2000)
            await original_page.screenshot(path='original_theme.png', full_page=True)
            
            original_html = await original_page.content()
            original_title = await original_page.title()
            
            # Check for cholot-texticon widgets in original
            orig_texticon_widgets = await original_page.query_selector_all('.cholot-texticon')
            orig_service_cards = await original_page.query_selector_all('.service-card, .services-section, [class*="service"]')
            
            print(f"Original page title: {original_title}")
            print(f"Found {len(orig_texticon_widgets)} cholot-texticon widgets in original")
            print(f"Found {len(orig_service_cards)} potential service card elements in original")
            
            # Capture specific sections for detailed comparison
            print("\n📸 Capturing Hero sections...")
            
            # Hero section screenshots
            hero_current = await current_page.query_selector('header, .hero, .banner, .jumbotron, [class*="hero"]')
            if hero_current:
                await hero_current.screenshot(path='hero_current.png')
                print("✅ Hero section captured from current implementation")
            else:
                print("❌ No hero section found in current implementation")
            
            hero_original = await original_page.query_selector('header, .hero, .banner, .jumbotron, [class*="hero"]')
            if hero_original:
                await hero_original.screenshot(path='hero_original.png')
                print("✅ Hero section captured from original theme")
            else:
                print("❌ No hero section found in original theme")
            
            # Check console errors
            print("\n🔍 Checking console messages...")
            current_logs = []
            original_logs = []
            
            current_page.on("console", lambda msg: current_logs.append(f"[CURRENT] {msg.type}: {msg.text}"))
            original_page.on("console", lambda msg: original_logs.append(f"[ORIGINAL] {msg.type}: {msg.text}"))
            
            # Reload to capture console messages
            await current_page.reload(wait_until='networkidle')
            await original_page.reload(wait_until='networkidle')
            await asyncio.sleep(2)
            
            # Check for specific CSS and JS files
            print("\n🎨 Checking CSS/JS resources...")
            
            current_styles = await current_page.query_selector_all('link[rel="stylesheet"], style')
            current_scripts = await current_page.query_selector_all('script[src]')
            
            original_styles = await original_page.query_selector_all('link[rel="stylesheet"], style')
            original_scripts = await original_page.query_selector_all('script[src]')
            
            print(f"Current implementation: {len(current_styles)} stylesheets, {len(current_scripts)} scripts")
            print(f"Original theme: {len(original_styles)} stylesheets, {len(original_scripts)} scripts")
            
            # Save detailed analysis
            with open('site_comparison_analysis.txt', 'w') as f:
                f.write("SITE COMPARISON ANALYSIS\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("CURRENT IMPLEMENTATION (localhost:8081)\n")
                f.write("-" * 40 + "\n")
                f.write(f"Title: {current_title}\n")
                f.write(f"Cholot-texticon widgets: {len(texticon_widgets)}\n")
                f.write(f"Service cards: {len(service_cards)}\n")
                f.write(f"Stylesheets: {len(current_styles)}\n")
                f.write(f"Scripts: {len(current_scripts)}\n")
                
                f.write("\nORIGINAL THEME (localhost:8080)\n")
                f.write("-" * 40 + "\n")
                f.write(f"Title: {original_title}\n")
                f.write(f"Cholot-texticon widgets: {len(orig_texticon_widgets)}\n")
                f.write(f"Service cards: {len(orig_service_cards)}\n")
                f.write(f"Stylesheets: {len(original_styles)}\n")
                f.write(f"Scripts: {len(orig_scripts)}\n")
                
                if current_logs:
                    f.write("\nCURRENT CONSOLE MESSAGES:\n")
                    for log in current_logs:
                        f.write(f"{log}\n")
                
                if original_logs:
                    f.write("\nORIGINAL CONSOLE MESSAGES:\n")
                    for log in original_logs:
                        f.write(f"{log}\n")
            
            print("\n✅ Screenshots and analysis saved!")
            print("Files created:")
            print("- current_implementation.png")
            print("- original_theme.png")
            print("- hero_current.png (if found)")
            print("- hero_original.png (if found)")
            print("- site_comparison_analysis.txt")
            
        except Exception as e:
            print(f"❌ Error during comparison: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(compare_sites())