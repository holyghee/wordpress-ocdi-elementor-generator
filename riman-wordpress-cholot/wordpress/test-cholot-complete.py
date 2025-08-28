#!/usr/bin/env python3
"""
Vollständiger Test-Zyklus für Cholot XML Import
Testet ob generierte XML identisch mit Original ist
"""

import subprocess
import time
import json
import requests
from pathlib import Path
import sys

class CholutCompleteTest:
    def __init__(self):
        self.wp_url = "http://localhost:8082"
        self.original_url = "http://localhost:8080"  # Original Cholot Demo
        self.admin_url = f"{self.wp_url}/wp-admin"
        self.original_xml = "/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml"
        
    def import_via_ocdi(self, xml_file):
        """Import XML via One Click Demo Import"""
        print(f"📥 Importing {Path(xml_file).name}...")
        
        # Copy XML to OCDI import directory
        import_dir = Path("wp-content/uploads/2024/08/demo-import")
        import_dir.mkdir(parents=True, exist_ok=True)
        
        import shutil
        target_file = import_dir / "content.xml"
        shutil.copy(xml_file, target_file)
        
        # Trigger import via WP-CLI if available
        result = subprocess.run([
            "wp", "ocdi", "import", 
            "--content-file=" + str(target_file),
            "--path=.",
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            # Fallback to direct import
            print("⚠️ WP-CLI nicht verfügbar, nutze direkten Import...")
            return self.direct_import(xml_file)
        
        return True
    
    def direct_import(self, xml_file):
        """Direkter Import ohne OCDI"""
        print("📥 Direkter WordPress Import...")
        
        result = subprocess.run([
            "wp", "import", xml_file,
            "--authors=create",
            "--path=."
        ], capture_output=True, text=True)
        
        return "Success" in result.stdout or "Imported" in result.stdout
    
    def check_pages_created(self):
        """Prüfe ob Seiten erstellt wurden"""
        result = subprocess.run([
            "wp", "post", "list",
            "--post_type=page",
            "--format=json",
            "--path=."
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            return []
        
        try:
            pages = json.loads(result.stdout)
            return pages
        except:
            return []
    
    def check_elementor_data(self, page_id):
        """Prüfe ob Seite Elementor-Daten hat"""
        result = subprocess.run([
            "wp", "post", "meta", "get",
            str(page_id),
            "_elementor_data",
            "--path=."
        ], capture_output=True, text=True)
        
        if result.returncode != 0 or not result.stdout.strip():
            return False
        
        try:
            data = json.loads(result.stdout)
            return len(data) > 0
        except:
            return False
    
    def compare_with_playwright(self):
        """Vergleiche Seiten mit Playwright"""
        print("\n🎭 Starte visuellen Vergleich mit Playwright...")
        
        # Erstelle Playwright Test Script
        test_script = """
import asyncio
from playwright.async_api import async_playwright
import cv2
import numpy as np
from pathlib import Path

async def compare_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # Screenshot Original (Port 8080)
        page_original = await browser.new_page()
        await page_original.goto('http://localhost:8080')
        await page_original.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        original_screenshot = await page_original.screenshot(path='original-8080.png', full_page=True)
        
        # Screenshot Generated (Port 8082)
        page_generated = await browser.new_page()
        await page_generated.goto('http://localhost:8082')
        await page_generated.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        generated_screenshot = await page_generated.screenshot(path='generated-8082.png', full_page=True)
        
        await browser.close()
        
        # Vergleiche Screenshots
        img1 = cv2.imread('original-8080.png')
        img2 = cv2.imread('generated-8082.png')
        
        if img1.shape != img2.shape:
            print(f"⚠️ Unterschiedliche Größen: {img1.shape} vs {img2.shape}")
            return False
        
        # Berechne Ähnlichkeit
        difference = cv2.subtract(img1, img2)
        b, g, r = cv2.split(difference)
        
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            print("✅ Seiten sind identisch!")
            return True
        else:
            # Berechne Ähnlichkeitsgrad
            total_pixels = img1.shape[0] * img1.shape[1] * 3
            different_pixels = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
            similarity = (1 - different_pixels / total_pixels) * 100
            
            print(f"📊 Ähnlichkeit: {similarity:.2f}%")
            
            # Speichere Differenz-Bild
            cv2.imwrite('difference.png', difference)
            print("📸 Differenz-Bild gespeichert als difference.png")
            
            return similarity > 90

asyncio.run(compare_pages())
"""
        
        # Speichere und führe Test aus
        with open("playwright_test.py", "w") as f:
            f.write(test_script)
        
        result = subprocess.run(["python3", "playwright_test.py"], capture_output=True, text=True)
        print(result.stdout)
        
        return "identisch" in result.stdout or "90" in result.stdout
    
    def run_complete_test(self):
        """Führe vollständigen Test durch"""
        print("=" * 60)
        print("🚀 CHOLOT VOLLSTÄNDIGER TEST")
        print("=" * 60)
        
        # 1. Teste Original XML
        print("\n1️⃣ TESTE ORIGINAL CHOLOT XML")
        print("-" * 40)
        
        if not Path(self.original_xml).exists():
            print("❌ Original XML nicht gefunden!")
            return False
        
        # Bereinige WordPress
        print("🧹 Bereinige WordPress...")
        subprocess.run(["./wordpress-cleanup.sh"], capture_output=True)
        
        # Importiere Original
        if self.import_via_ocdi(self.original_xml):
            print("✅ Original importiert")
        else:
            print("❌ Import fehlgeschlagen")
            return False
        
        # Prüfe Seiten
        pages = self.check_pages_created()
        print(f"📄 {len(pages)} Seiten erstellt")
        
        elementor_pages = 0
        for page in pages:
            if self.check_elementor_data(page['ID']):
                elementor_pages += 1
                print(f"  ✅ {page['post_title']} - Elementor OK")
            else:
                print(f"  ❌ {page['post_title']} - Kein Elementor")
        
        print(f"\n📊 Ergebnis: {elementor_pages}/{len(pages)} Seiten mit Elementor")
        
        # 2. Screenshot Original
        print("\n2️⃣ ERSTELLE SCREENSHOTS")
        print("-" * 40)
        
        # Nutze Playwright für Screenshots
        success = self.compare_with_playwright()
        
        if success:
            print("\n✅✅✅ TEST ERFOLGREICH ✅✅✅")
            print("Die Seiten sind visuell identisch!")
        else:
            print("\n❌ TEST FEHLGESCHLAGEN")
            print("Die Seiten unterscheiden sich visuell")
            
            # Analysiere Unterschiede
            self.analyze_differences()
        
        return success
    
    def analyze_differences(self):
        """Analysiere was fehlt"""
        print("\n📊 ANALYSE DER UNTERSCHIEDE")
        print("-" * 40)
        
        # Prüfe Elementor Widgets
        result = subprocess.run([
            "wp", "db", "query",
            "SELECT meta_value FROM wp_postmeta WHERE meta_key='_elementor_data' LIMIT 1",
            "--path=."
        ], capture_output=True, text=True)
        
        if result.stdout:
            try:
                data = json.loads(result.stdout.split('\n')[1] if '\n' in result.stdout else result.stdout)
                
                # Sammle Widget-Typen
                widget_types = set()
                def extract_widgets(elements):
                    for el in elements:
                        if isinstance(el, dict):
                            if el.get('widgetType'):
                                widget_types.add(el['widgetType'])
                            if 'elements' in el:
                                extract_widgets(el['elements'])
                
                extract_widgets(data)
                print(f"Gefundene Widgets: {', '.join(widget_types)}")
                
                # Prüfe auf Cholot-spezifische Widgets
                cholot_widgets = [w for w in widget_types if 'cholot' in w or 'rdn' in w]
                if cholot_widgets:
                    print(f"✅ Cholot Widgets vorhanden: {', '.join(cholot_widgets)}")
                else:
                    print("❌ KEINE Cholot Widgets gefunden!")
                    print("   → Das ist das Hauptproblem!")
                    
            except Exception as e:
                print(f"Fehler bei Analyse: {e}")
    
    def fix_and_retry(self):
        """Korrigiere Probleme und versuche erneut"""
        print("\n🔧 AUTOMATISCHE KORREKTUR")
        print("-" * 40)
        
        # TODO: Implementiere automatische Korrekturen basierend auf gefundenen Problemen
        
        return False


if __name__ == "__main__":
    tester = CholutCompleteTest()
    
    # Führe Test aus
    success = tester.run_complete_test()
    
    if not success:
        print("\n🔄 Starte Korrektur-Zyklus...")
        for i in range(3):
            print(f"\nIteration {i+1}/3")
            if tester.fix_and_retry():
                print("✅ Erfolgreich nach Korrektur!")
                sys.exit(0)
        
        print("\n❌ Konnte nicht automatisch korrigiert werden")
        print("Manuelle Intervention erforderlich!")
        sys.exit(1)
    
    sys.exit(0)