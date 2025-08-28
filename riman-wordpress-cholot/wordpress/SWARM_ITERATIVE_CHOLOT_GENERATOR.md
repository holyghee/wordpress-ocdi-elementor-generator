# 🎯 SWARM MISSION: ITERATIVE CHOLOT XML GENERATOR

## KRITISCHES ZIEL
**Erstelle einen Generator, der aus einer einfachen YAML-Config die EXAKTE Cholot Demo XML (`/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data.xml`) reproduziert.**

## ⚠️ WICHTIGSTE ANFORDERUNG
**Du MUSST so lange iterieren, bis die generierte XML beim Import in WordPress TATSÄCHLICH Seiten mit Elementor-Inhalten erzeugt!**

## SCHRITT 1: VERSTEHE DIE ZIEL-XML STRUKTUR

```python
import xml.etree.ElementTree as ET
import json

# ANALYSIERE die Original XML
target_xml = '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data.xml'
tree = ET.parse(target_xml)
root = tree.getroot()

# ZÄHLE und VERSTEHE was drin ist
stats = {
    'total_items': len(root.findall('.//item')),
    'pages': 0,
    'posts': 0,
    'menus': 0,
    'attachments': 0,
    'elementor_pages': 0
}

for item in root.findall('.//item'):
    post_type = item.find('.//{http://wordpress.org/export/1.2/}post_type')
    if post_type is not None:
        post_type_text = post_type.text
        if post_type_text == 'page':
            stats['pages'] += 1
            # Check for Elementor data
            for meta in item.findall('.//{http://wordpress.org/export/1.2/}postmeta'):
                key = meta.find('.//{http://wordpress.org/export/1.2/}meta_key')
                if key is not None and key.text == '_elementor_data':
                    stats['elementor_pages'] += 1
                    break
        elif post_type_text == 'post':
            stats['posts'] += 1
        elif post_type_text == 'nav_menu_item':
            stats['menus'] += 1
        elif post_type_text == 'attachment':
            stats['attachments'] += 1

print(f"""
ORIGINAL CHOLOT XML STRUKTUR:
==============================
Total Items: {stats['total_items']}
Pages: {stats['pages']} (davon {stats['elementor_pages']} mit Elementor)
Posts: {stats['posts']}
Menu Items: {stats['menus']}
Attachments: {stats['attachments']}
""")
```

## SCHRITT 2: EXTRAHIERE DIE ECHTEN ELEMENTOR DATEN

```python
# KRITISCH: Hole die EXAKTEN Elementor-Strukturen
elementor_pages = {}

for item in root.findall('.//item'):
    title_elem = item.find('.//title')
    if title_elem is None:
        continue
    
    title = title_elem.text
    
    # Finde Elementor data
    for meta in item.findall('.//{http://wordpress.org/export/1.2/}postmeta'):
        key = meta.find('.//{http://wordpress.org/export/1.2/}meta_key')
        if key is not None and key.text == '_elementor_data':
            value = meta.find('.//{http://wordpress.org/export/1.2/}meta_value')
            if value is not None and value.text:
                try:
                    elementor_data = json.loads(value.text)
                    elementor_pages[title] = elementor_data
                    
                    # ANALYSIERE die Widget-Typen
                    widget_types = set()
                    def extract_widgets(elements):
                        for el in elements:
                            if el.get('widgetType'):
                                widget_types.add(el['widgetType'])
                            if 'elements' in el:
                                extract_widgets(el['elements'])
                    
                    extract_widgets(elementor_data)
                    print(f"\nSeite: {title}")
                    print(f"Widgets: {', '.join(widget_types)}")
                except:
                    pass

# SPEICHERE die Elementor-Strukturen
with open('cholot_elementor_structures.json', 'w') as f:
    json.dump(elementor_pages, f, indent=2)
```

## SCHRITT 3: ERSTELLE MINIMAL YAML CONFIG

```yaml
# cholot-minimal.yaml
site:
  title: "Cholot – Retirement Community WordPress Theme"
  url: "http://localhost:8082"

pages:
  - title: "Home"
    slug: "home"
    template: "elementor_canvas"
    elementor_file: "elementor_structures/home.json"
    
  - title: "About"
    slug: "about"
    template: "elementor_canvas"
    elementor_file: "elementor_structures/about.json"
    
  - title: "Services"
    slug: "services"
    template: "elementor_canvas"
    elementor_file: "elementor_structures/services.json"

menus:
  - name: "Main Menu"
    slug: "main-menu"
    items:
      - title: "Home"
        page: "home"
      - title: "About"
        page: "about"
      - title: "Services"
        page: "services"
```

## SCHRITT 4: GENERATOR MIT IMPORT-TEST-ZYKLUS

```python
#!/usr/bin/env python3
"""
Cholot XML Generator mit automatischem Test-Zyklus
"""

import subprocess
import requests
import time
from pathlib import Path

class CholutIterativeGenerator:
    def __init__(self):
        self.wordpress_url = "http://localhost:8082"
        self.iterations = 0
        self.max_iterations = 10
        
    def generate_xml(self, yaml_config, output_xml):
        """Generiere XML aus YAML"""
        # Generator-Code hier
        pass
    
    def test_import(self, xml_file):
        """Teste Import via WP-CLI oder REST API"""
        # Option 1: WP-CLI
        result = subprocess.run([
            'wp', 'import', xml_file,
            '--authors=create',
            '--path=/path/to/wordpress'
        ], capture_output=True, text=True)
        
        if 'Success' not in result.stdout:
            return False
        
        # Prüfe ob Seiten erstellt wurden
        pages = subprocess.run([
            'wp', 'post', 'list',
            '--post_type=page',
            '--format=json',
            '--path=/path/to/wordpress'
        ], capture_output=True, text=True)
        
        pages_data = json.loads(pages.stdout)
        
        # Prüfe ob Elementor-Daten vorhanden sind
        for page in pages_data:
            elementor_check = subprocess.run([
                'wp', 'post', 'meta', 'get',
                str(page['ID']),
                '_elementor_data',
                '--path=/path/to/wordpress'
            ], capture_output=True, text=True)
            
            if elementor_check.stdout.strip():
                try:
                    data = json.loads(elementor_check.stdout)
                    if len(data) > 0:
                        print(f"✅ Seite {page['post_title']} hat Elementor-Inhalt")
                        return True
                except:
                    pass
        
        print("❌ Keine Seiten mit Elementor-Inhalt gefunden")
        return False
    
    def iterate_until_success(self):
        """Iteriere bis erfolgreicher Import"""
        while self.iterations < self.max_iterations:
            self.iterations += 1
            print(f"\n{'='*60}")
            print(f"ITERATION {self.iterations}")
            print('='*60)
            
            # 1. Generiere XML
            self.generate_xml('cholot-minimal.yaml', f'cholot-test-{self.iterations}.xml')
            
            # 2. Teste Import
            if self.test_import(f'cholot-test-{self.iterations}.xml'):
                print(f"🎉 ERFOLG nach {self.iterations} Iterationen!")
                return True
            
            # 3. Analysiere Fehler und passe an
            self.analyze_and_fix()
        
        print(f"❌ Fehlgeschlagen nach {self.max_iterations} Iterationen")
        return False
    
    def analyze_and_fix(self):
        """Analysiere Fehler und korrigiere Generator"""
        # Vergleiche mit Original
        # Finde fehlende Elemente
        # Korrigiere Format-Probleme
        pass
```

## SCHRITT 5: KRITISCHE ERFOLGSPRÜFUNGEN

```bash
#!/bin/bash

# Test 1: XML ist valide
xmllint --noout cholot-generated.xml && echo "✅ XML valide" || echo "❌ XML ungültig"

# Test 2: Enthält Elementor-Daten
grep -q "_elementor_data" cholot-generated.xml && echo "✅ Elementor-Daten vorhanden" || echo "❌ Keine Elementor-Daten"

# Test 3: Import funktioniert
wp import cholot-generated.xml --authors=create

# Test 4: Seiten wurden erstellt
wp post list --post_type=page --format=count

# Test 5: Elementor kann Seiten bearbeiten
for page_id in $(wp post list --post_type=page --format=ids); do
    elementor_data=$(wp post meta get $page_id _elementor_data)
    if [ ! -z "$elementor_data" ]; then
        echo "✅ Seite $page_id hat Elementor-Inhalt"
    else
        echo "❌ Seite $page_id hat KEINEN Elementor-Inhalt"
    fi
done
```

## SCHRITT 6: VERGLEICH MIT ORIGINAL

```python
def compare_with_original(generated_xml, original_xml):
    """Detaillierter Vergleich"""
    gen_tree = ET.parse(generated_xml)
    orig_tree = ET.parse(original_xml)
    
    issues = []
    
    # 1. Vergleiche Item-Anzahl
    gen_items = len(gen_tree.findall('.//item'))
    orig_items = len(orig_tree.findall('.//item'))
    
    if gen_items != orig_items:
        issues.append(f"Item-Anzahl: {gen_items} vs {orig_items}")
    
    # 2. Vergleiche Elementor-Daten
    for item in orig_tree.findall('.//item'):
        title = item.find('.//title').text
        
        # Finde entsprechendes Item in generated
        gen_item = None
        for gi in gen_tree.findall('.//item'):
            if gi.find('.//title').text == title:
                gen_item = gi
                break
        
        if not gen_item:
            issues.append(f"Fehlende Seite: {title}")
            continue
        
        # Vergleiche Elementor-Daten
        orig_elementor = get_elementor_data(item)
        gen_elementor = get_elementor_data(gen_item)
        
        if orig_elementor and not gen_elementor:
            issues.append(f"Fehlende Elementor-Daten: {title}")
        elif orig_elementor and gen_elementor:
            # Vergleiche Struktur
            if json.dumps(orig_elementor) != json.dumps(gen_elementor):
                issues.append(f"Unterschiedliche Elementor-Struktur: {title}")
    
    return issues
```

## LIEFERUNG ANFORDERUNGEN

1. **cholot-generator.py** - Generator der iteriert bis es funktioniert
2. **cholot-minimal.yaml** - Minimale Config-Datei
3. **test-import.sh** - Bash-Script zum Testen des Imports
4. **success-log.txt** - Beweis dass Import funktioniert hat

## ERFOLGS-KRITERIEN

Die Mission ist NUR erfolgreich wenn:

```bash
# 1. Import ohne Fehler
wp import cholot-generated.xml --authors=create
# Output: Success: Finished importing

# 2. Seiten existieren
wp post list --post_type=page --format=count
# Output: 8 (oder mehr)

# 3. Elementor kann die Seiten öffnen
wp post meta get [PAGE_ID] _elementor_data | jq length
# Output: > 0

# 4. Widget-Typen sind korrekt
grep -o "cholot-texticon\|cholot-team\|rdn-slider" cholot-generated.xml | sort -u
# Output: Alle Cholot-Widgets vorhanden
```

## WICHTIGE HINWEISE

1. **TESTE JEDEN SCHRITT** - Generiere nicht blind, teste ob es funktioniert
2. **ITERIERE BIS ZUM ERFOLG** - Gib nicht auf bis der Import funktioniert
3. **VERWENDE DIE TEMPLATES** - Die JSON-Dateien in `templates/` enthalten funktionierende Strukturen
4. **PRÜFE MIT WP-CLI** - Nutze `wp import` und `wp post meta get` zum Verifizieren
5. **DOKUMENTIERE FEHLER** - Schreibe auf was nicht funktioniert und wie du es gelöst hast

## START-BEFEHL

```bash
# Starte den iterativen Generator
python3 cholot-generator.py --yaml cholot-minimal.yaml --max-iterations 10 --test-import
```

**WICHTIG: Der Generator muss SO LANGE laufen und sich selbst korrigieren, bis die generierte XML beim Import TATSÄCHLICH Seiten mit Elementor-Inhalt erzeugt!**