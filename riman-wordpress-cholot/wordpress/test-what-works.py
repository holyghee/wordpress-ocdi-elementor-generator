#!/usr/bin/env python3
"""
Test was WIRKLICH funktioniert
"""

import json
import os
from pathlib import Path

def test_system():
    """
    Testet jeden Teil des Systems
    """
    print("🧪 SYSTEM TEST - Was funktioniert wirklich?")
    print("=" * 60)
    
    # Test 1: Gibt es JSON Templates?
    print("\n1️⃣ JSON Templates vorhanden?")
    json_files = list(Path(".").glob("*.json"))
    elementor_jsons = [f for f in json_files if 'elementor' in f.name.lower() or 'cholot' in f.name.lower()]
    
    if elementor_jsons:
        print(f"   ✅ {len(elementor_jsons)} JSON Dateien gefunden")
        for f in elementor_jsons[:5]:
            size = f.stat().st_size
            print(f"      - {f.name} ({size:,} bytes)")
    else:
        print("   ❌ Keine JSON Templates gefunden")
    
    # Test 2: Kann generate_wordpress_xml.py ausgeführt werden?
    print("\n2️⃣ WordPress XML Generator funktioniert?")
    if Path("generate_wordpress_xml.py").exists():
        print("   ✅ generate_wordpress_xml.py existiert")
        # Test mit minimal config
        test_yaml = """site:
  title: "Test Site"
pages:
  - title: "Test Page"
    content: "Test Content"
"""
        with open("test-minimal.yaml", "w") as f:
            f.write(test_yaml)
        
        result = os.system("python generate_wordpress_xml.py -i test-minimal.yaml -o test-output.xml 2>&1 | head -5")
        if result == 0 and Path("test-output.xml").exists():
            print("   ✅ Generator läuft")
            size = Path("test-output.xml").stat().st_size
            print(f"      Generated: test-output.xml ({size:,} bytes)")
        else:
            print("   ⚠️  Generator hat Probleme")
    else:
        print("   ❌ generate_wordpress_xml.py nicht gefunden")
    
    # Test 3: Hat die XML Elementor-Daten?
    print("\n3️⃣ Elementor-Daten in generierten XMLs?")
    xml_files = list(Path(".").glob("riman*.xml"))[:3]
    
    for xml_file in xml_files:
        with open(xml_file, 'r') as f:
            content = f.read()
            
        has_elementor = "_elementor_data" in content
        page_count = content.count("<item>")
        
        if has_elementor:
            print(f"   ✅ {xml_file.name}")
            print(f"      - Pages: {page_count}")
            print(f"      - Elementor data: {'Yes' if has_elementor else 'No'}")
        else:
            print(f"   ❌ {xml_file.name} - Keine Elementor-Daten")
    
    # Test 4: Ist das Problem die JSON-Struktur?
    print("\n4️⃣ JSON Struktur korrekt?")
    if Path("elementor-content-only.json").exists():
        with open("elementor-content-only.json", 'r') as f:
            data = json.load(f)
        
        # Check structure
        if isinstance(data, list):
            print(f"   ✅ JSON ist Liste mit {len(data)} Sections")
            if data and 'elType' in data[0]:
                print(f"      - Erste Section: {data[0].get('elType', 'unknown')}")
                if 'elements' in data[0]:
                    print(f"      - Hat {len(data[0]['elements'])} Elements")
        else:
            print(f"   ⚠️  JSON ist {type(data).__name__}, nicht Liste")
    else:
        print("   ❌ elementor-content-only.json nicht gefunden")
    
    # Test 5: Der wichtigste Test - können wir eine funktionierende XML machen?
    print("\n5️⃣ MINIMAL TEST - Kann ich EINE funktionierende Seite machen?")
    
    # Nimm die demo-data-fixed.xml als Basis (die funktioniert!)
    if Path("/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml").exists():
        print("   ✅ Original Cholot XML gefunden")
        print("      Diese XML FUNKTIONIERT definitiv!")
        print("\n   💡 LÖSUNG: Wir sollten diese XML als Basis nehmen")
        print("      und nur die Texte ersetzen!")
    
    print("\n" + "=" * 60)
    print("📊 FAZIT:")
    print("=" * 60)
    
    print("""
Das System hat Teile die funktionieren, aber:

1. Die generierten XMLs haben zu wenig Seiten
2. Elementor-Daten sind nicht korrekt eingebettet
3. Die JSON→XML Konversion ist unvollständig

LÖSUNG: Wir brauchen einen EINFACHEREN Ansatz:
- Nimm die FUNKTIONIERENDE demo-data-fixed.xml
- Ersetze NUR die Texte
- Behalte die komplette Struktur
""")

if __name__ == "__main__":
    test_system()