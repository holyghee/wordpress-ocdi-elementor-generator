#!/usr/bin/env python3
"""
Intelligenter Prozessor Verifikations-Test
Verifiziert dass alle Ziele erreicht wurden
"""

import json
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
import time
from typing import Dict, List, Tuple

class IntelligentProcessorVerification:
    def __init__(self):
        self.tests = []
        self.passed = []
        self.failed = []
        
    def run_all_tests(self) -> bool:
        """Führe alle Verifikations-Tests durch"""
        print("\n" + "="*60)
        print("🧪 INTELLIGENTER PROZESSOR VERIFIKATION")
        print("="*60)
        
        # Test 1: Strukturelle Flexibilität
        self.test_structural_flexibility()
        
        # Test 2: Komponenten-Wiederverwendung
        self.test_component_reusability()
        
        # Test 3: Design-Anpassung
        self.test_design_adaptation()
        
        # Test 4: Inhaltliche Kontrolle
        self.test_content_control()
        
        # Test 5: Block-Library Erweiterbarkeit
        self.test_library_extensibility()
        
        # Test 6: XML-Generation
        self.test_xml_generation()
        
        # Test 7: Elementor-Kompatibilität
        self.test_elementor_compatibility()
        
        # Report
        self.generate_report()
        
        return len(self.failed) == 0
    
    def test_structural_flexibility(self):
        """Test 1: Kann die Reihenfolge der Blocks geändert werden?"""
        print("\n📋 Test 1: Strukturelle Flexibilität")
        
        # Erstelle zwei YAMLs mit unterschiedlicher Block-Reihenfolge
        yaml1 = {
            'site': {'title': 'Test', 'url': 'http://test'},
            'pages': [{
                'title': 'Test Page 1',
                'blocks': [
                    {'type': 'hero-slider'},
                    {'type': 'service-cards'},
                    {'type': 'testimonials'}
                ]
            }]
        }
        
        yaml2 = {
            'site': {'title': 'Test', 'url': 'http://test'},
            'pages': [{
                'title': 'Test Page 2',
                'blocks': [
                    {'type': 'testimonials'},
                    {'type': 'hero-slider'},
                    {'type': 'service-cards'}
                ]
            }]
        }
        
        # Speichere temporär
        with open('test_order1.yaml', 'w') as f:
            yaml.dump(yaml1, f)
        with open('test_order2.yaml', 'w') as f:
            yaml.dump(yaml2, f)
        
        # Führe Prozessor aus
        result1 = subprocess.run(['python3', 'intelligent_block_processor.py', 'test_order1.yaml'],
                                capture_output=True, text=True)
        result2 = subprocess.run(['python3', 'intelligent_block_processor.py', 'test_order2.yaml'],
                                capture_output=True, text=True)
        
        # Prüfe ob beide erfolgreich waren
        if 'assembliert' in result1.stdout and 'assembliert' in result2.stdout:
            print("  ✅ Blocks können in beliebiger Reihenfolge angeordnet werden")
            self.passed.append("Strukturelle Flexibilität")
        else:
            print("  ❌ Block-Reihenfolge kann nicht geändert werden")
            self.failed.append("Strukturelle Flexibilität")
    
    def test_component_reusability(self):
        """Test 2: Können Komponenten wiederverwendet werden?"""
        print("\n📋 Test 2: Komponenten-Wiederverwendung")
        
        # Prüfe ob Block-Library existiert
        block_library = Path('block_library')
        if block_library.exists():
            blocks = list(block_library.glob('*.json'))
            if len(blocks) > 10:
                print(f"  ✅ {len(blocks)} wiederverwendbare Blocks in Library")
                self.passed.append("Komponenten-Wiederverwendung")
            else:
                print(f"  ⚠️  Nur {len(blocks)} Blocks in Library")
                self.failed.append("Komponenten-Wiederverwendung")
        else:
            print("  ❌ Block-Library nicht gefunden")
            self.failed.append("Komponenten-Wiederverwendung")
    
    def test_design_adaptation(self):
        """Test 3: Werden globale Design-Settings angewendet?"""
        print("\n📋 Test 3: Design-Anpassung")
        
        # Prüfe ob Design-Settings in der generierten XML angewendet wurden
        if Path('intelligent-assembled.xml').exists():
            with open('intelligent-assembled.xml', 'r') as f:
                xml_content = f.read()
            
            # Prüfe ob die neue Farbe angewendet wurde
            if '#FF6B35' in xml_content:  # Orange aus der Test-Config
                print("  ✅ Globale Design-Settings wurden angewendet")
                self.passed.append("Design-Anpassung")
            else:
                print("  ❌ Design-Settings wurden nicht angewendet")
                self.failed.append("Design-Anpassung")
        else:
            print("  ⚠️  Generierte XML nicht gefunden")
            self.failed.append("Design-Anpassung")
    
    def test_content_control(self):
        """Test 4: Werden Inhalte aus der YAML übernommen?"""
        print("\n📋 Test 4: Inhaltliche Kontrolle")
        
        if Path('intelligent-assembled.xml').exists():
            with open('intelligent-assembled.xml', 'r') as f:
                xml_content = f.read()
            
            # Prüfe ob spezifische Inhalte aus der YAML in der XML sind
            test_strings = [
                'Willkommen zur intelligenten Seite',
                'Dynamisch assembliert',
                'Schnelle Entwicklung',
                'Modularer Aufbau'
            ]
            
            found = sum(1 for s in test_strings if s in xml_content)
            
            if found >= 3:
                print(f"  ✅ {found}/4 Test-Inhalte in generierter XML gefunden")
                self.passed.append("Inhaltliche Kontrolle")
            else:
                print(f"  ❌ Nur {found}/4 Test-Inhalte gefunden")
                self.failed.append("Inhaltliche Kontrolle")
        else:
            print("  ⚠️  Generierte XML nicht gefunden")
            self.failed.append("Inhaltliche Kontrolle")
    
    def test_library_extensibility(self):
        """Test 5: Kann die Block-Library erweitert werden?"""
        print("\n📋 Test 5: Block-Library Erweiterbarkeit")
        
        # Prüfe ob neue Blocks hinzugefügt werden können
        block_library = Path('block_library')
        if block_library.exists() and (block_library / 'index.json').exists():
            print("  ✅ Block-Library ist erweiterbar (Index vorhanden)")
            self.passed.append("Library-Erweiterbarkeit")
        else:
            print("  ❌ Block-Library nicht erweiterbar")
            self.failed.append("Library-Erweiterbarkeit")
    
    def test_xml_generation(self):
        """Test 6: Wird valide WordPress XML generiert?"""
        print("\n📋 Test 6: XML-Generation")
        
        xml_file = Path('intelligent-assembled.xml')
        if xml_file.exists():
            try:
                tree = ET.parse(str(xml_file))
                root = tree.getroot()
                
                # Prüfe WordPress-Struktur
                items = root.findall('.//item')
                if len(items) > 0:
                    print(f"  ✅ Valide WordPress XML mit {len(items)} Items")
                    self.passed.append("XML-Generation")
                else:
                    print("  ❌ Keine Items in XML")
                    self.failed.append("XML-Generation")
            except ET.ParseError as e:
                print(f"  ❌ XML Parse-Fehler: {e}")
                self.failed.append("XML-Generation")
        else:
            print("  ❌ XML-Datei nicht gefunden")
            self.failed.append("XML-Generation")
    
    def test_elementor_compatibility(self):
        """Test 7: Ist die generierte Struktur Elementor-kompatibel?"""
        print("\n📋 Test 7: Elementor-Kompatibilität")
        
        xml_file = Path('intelligent-assembled.xml')
        if xml_file.exists():
            tree = ET.parse(str(xml_file))
            
            # Prüfe auf Elementor-Metadaten
            elementor_found = False
            for meta in tree.findall('.//{http://wordpress.org/export/1.2/}postmeta'):
                key = meta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                if key is not None and key.text == '_elementor_data':
                    value = meta.find('.//{http://wordpress.org/export/1.2/}meta_value')
                    if value is not None and value.text:
                        try:
                            elementor_data = json.loads(value.text)
                            if isinstance(elementor_data, list) and len(elementor_data) > 0:
                                elementor_found = True
                                break
                        except:
                            pass
            
            if elementor_found:
                print("  ✅ Elementor-kompatible Datenstruktur")
                self.passed.append("Elementor-Kompatibilität")
            else:
                print("  ❌ Keine gültigen Elementor-Daten gefunden")
                self.failed.append("Elementor-Kompatibilität")
        else:
            print("  ❌ XML-Datei nicht gefunden")
            self.failed.append("Elementor-Kompatibilität")
    
    def generate_report(self):
        """Generiere finalen Test-Report"""
        print("\n" + "="*60)
        print("📊 TEST-ERGEBNISSE")
        print("="*60)
        
        total = len(self.passed) + len(self.failed)
        success_rate = (len(self.passed) / total * 100) if total > 0 else 0
        
        print(f"\n✅ Bestandene Tests ({len(self.passed)}):")
        for test in self.passed:
            print(f"  • {test}")
        
        if self.failed:
            print(f"\n❌ Fehlgeschlagene Tests ({len(self.failed)}):")
            for test in self.failed:
                print(f"  • {test}")
        
        print(f"\n📈 Erfolgsrate: {success_rate:.1f}%")
        
        if success_rate >= 85:
            print("\n🎉 ZIEL ERREICHT!")
            print("Der intelligente Prozessor funktioniert wie geplant.")
            print("Seiten können dynamisch aus Block-Library assembliert werden.")
        elif success_rate >= 60:
            print("\n⚠️  TEILWEISE ERREICHT")
            print("Grundfunktionalität vorhanden, weitere Arbeit nötig.")
        else:
            print("\n❌ ZIEL NICHT ERREICHT")
            print("Weitere Entwicklung erforderlich.")
        
        # Speichere Report
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'passed': self.passed,
            'failed': self.failed,
            'success_rate': success_rate
        }
        
        with open('verification_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report gespeichert: verification_report.json")
        
        return success_rate >= 85

def main():
    """Hauptausführung"""
    verifier = IntelligentProcessorVerification()
    success = verifier.run_all_tests()
    
    if success:
        print("\n✅ VERIFIKATION ERFOLGREICH")
        print("Das System erfüllt alle Anforderungen!")
    else:
        print("\n⚠️  VERIFIKATION UNVOLLSTÄNDIG")
        print("Weitere Iteration erforderlich.")
    
    return success

if __name__ == "__main__":
    main()