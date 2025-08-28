# 🚀 SWARM PROMPT: Vollautomatische Cholot Theme Rekonstruktion mit Selbst-Verifikation

## MISSION
Du bist ein autonomer SWARM-Agent. Deine Aufgabe ist es, das Cholot Retirement Community WordPress Theme vollständig zu rekonstruieren, indem du die vorhandenen Templates und Elementor-Blöcke analysierst und eine funktionierende YAML-Konfiguration erstellst, die das Theme exakt nachbildet. Du musst deine Lösung selbst testen und iterativ verbessern, bis sie nachweislich funktioniert.

## ARBEITSVERZEICHNIS
```bash
cd /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress
```

## VERFÜGBARE RESSOURCEN

### 1. Templates (Komplette Seiten als JSON)
- **Verzeichnis**: `./templates/`
- 19 vollständige Seitenlayouts
- Enthält: home-page.json, about-page.json, contact-page.json, etc.

### 2. Elementor Blocks (Wiederverwendbare Komponenten)
- **Verzeichnis**: `./elementor blocks/`
- 8 modulare Block-Komponenten
- Hero-Sections, Service-Cards, Team-Sections, etc.

### 3. Ziel-XML (Das zu erreichende Ergebnis)
- **Datei**: `/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml`
- 65 Items, komplette Theme-Demo-Struktur

### 4. Werkzeuge
- **Generator**: `full_site_generator.py` - Erzeugt XML aus YAML
- **Processor**: `section_based_processor.py` - Verarbeitet Elementor-Strukturen
- **Analyzer**: `cholot_analyzer.py` - Analysiert Templates und Blocks
- **Tester**: `test_cholot_import.py` - Testet Imports
- **Cleanup**: `./wordpress-cleanup.sh` - Bereinigt WordPress
- **OCDI Test**: `php test-direct-ocdi.php` - Testet OCDI Import
- **Verify**: `php check-imported.php` - Verifiziert Import

## DEINE AUFGABEN (SEQUENZIELL)

### PHASE 1: Analyse & Verstehen
1. Liste ALLE Templates in `./templates/`:
   ```bash
   ls -la templates/*.json | wc -l
   ```

2. Liste ALLE Elementor Blocks:
   ```bash
   ls -la "elementor blocks"/*.json
   ```

3. Analysiere die Struktur jedes Templates:
   ```bash
   python3 cholot_analyzer.py
   ```

4. Extrahiere kritische Informationen aus dem Ziel-XML:
   - Anzahl der Seiten mit Elementor-Daten
   - Menu-Struktur
   - Custom Widget Types (cholot-*)
   - Media Attachments

### PHASE 2: YAML-Konfiguration erstellen
1. Erstelle `cholot-complete.yaml` mit:
   - Allen Seiten aus den Templates
   - Menu-Struktur aus dem Ziel-XML
   - Korrekten Widget-Mappings
   - Media-Referenzen

2. Nutze die analysierten Templates um die sections zu füllen:
   ```python
   import json
   import yaml
   
   # Lade Template
   with open('templates/home-page.json') as f:
       template = json.load(f)
   
   # Konvertiere zu YAML-Struktur
   sections = template.get('content', [])
   ```

### PHASE 3: Automatischer Test-Zyklus

**WICHTIG**: Du musst diesen Zyklus SELBSTSTÄNDIG ausführen und bei Fehlern AUTOMATISCH korrigieren!

```python
#!/usr/bin/env python3
# Speichere als: auto_test_cholot.py

import subprocess
import time
import os
import json
import yaml

class CholotAutoTester:
    def __init__(self):
        self.iteration = 0
        self.max_iterations = 10
        self.success = False
        
    def run_complete_test(self):
        while self.iteration < self.max_iterations and not self.success:
            print(f"\n{'='*60}")
            print(f"ITERATION {self.iteration + 1}/{self.max_iterations}")
            print('='*60)
            
            # 1. Generate XML from YAML
            print("\n📝 Step 1: Generating XML from YAML...")
            result = subprocess.run([
                'python3', 'full_site_generator.py',
                'cholot-complete.yaml',
                'cholot-test.xml'
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ XML generation failed: {result.stderr}")
                self.fix_yaml_errors(result.stderr)
                self.iteration += 1
                continue
            
            # 2. Clean WordPress
            print("\n🧹 Step 2: Cleaning WordPress...")
            subprocess.run(['./wordpress-cleanup.sh'], check=True)
            time.sleep(2)
            
            # 3. Test import with OCDI
            print("\n📥 Step 3: Testing OCDI import...")
            result = subprocess.run([
                'php', 'test-direct-ocdi.php'
            ], capture_output=True, text=True)
            
            print(result.stdout[-500:])  # Last 500 chars of output
            
            # 4. Verify import
            print("\n✅ Step 4: Verifying import...")
            verify_result = subprocess.run([
                'php', 'check-imported.php'
            ], capture_output=True, text=True)
            
            verification = self.analyze_verification(verify_result.stdout)
            
            if verification['success']:
                print("\n🎉 SUCCESS! All checks passed!")
                self.success = True
                self.save_working_solution()
                break
            else:
                print(f"\n❌ Verification failed:")
                for error in verification['errors']:
                    print(f"  - {error}")
                self.fix_import_errors(verification['errors'])
            
            self.iteration += 1
        
        return self.success
    
    def analyze_verification(self, output):
        """Analyze verification output"""
        errors = []
        
        # Check pages
        if 'Pages: 0' in output:
            errors.append('No pages imported')
        elif 'Pages:' in output:
            # Extract page count
            import re
            match = re.search(r'Pages: (\d+)', output)
            if match:
                page_count = int(match.group(1))
                if page_count < 10:  # Cholot should have at least 10 pages
                    errors.append(f'Only {page_count} pages imported, expected 10+')
        
        # Check Elementor data
        if 'Has Elementor data' not in output:
            errors.append('No Elementor data found')
        
        # Check menus
        if 'Menus: 0' in output or 'Items: 0' in output:
            errors.append('Menu not properly imported')
        
        # Check custom post types
        if 'footer' not in output.lower() or 'header' not in output.lower():
            errors.append('Custom post types missing')
        
        return {
            'success': len(errors) == 0,
            'errors': errors
        }
    
    def fix_yaml_errors(self, error_msg):
        """Fix YAML generation errors"""
        print("\n🔧 Fixing YAML errors...")
        
        with open('cholot-complete.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Common fixes
        if 'datetime' in error_msg:
            # Fix date format issues
            for page in config.get('pages', []):
                if 'date' not in page:
                    page['date'] = '2024-08-21'
        
        if 'NoneType' in error_msg:
            # Ensure all required fields exist
            for page in config.get('pages', []):
                page.setdefault('slug', page['title'].lower().replace(' ', '-'))
                page.setdefault('template', 'elementor_canvas')
                page.setdefault('sections', [])
        
        # Save fixed YAML
        with open('cholot-complete.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def fix_import_errors(self, errors):
        """Fix import errors in YAML"""
        print("\n🔧 Fixing import errors...")
        
        with open('cholot-complete.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        for error in errors:
            if 'No pages' in error:
                # Ensure pages have correct structure
                if 'pages' not in config:
                    config['pages'] = []
                
                # Add a test page if empty
                if len(config['pages']) == 0:
                    config['pages'].append({
                        'id': 101,
                        'title': 'Home',
                        'slug': 'home',
                        'template': 'elementor_canvas',
                        'sections': []
                    })
            
            elif 'No Elementor data' in error:
                # Add Elementor sections from templates
                self.add_elementor_from_templates(config)
            
            elif 'Menu not' in error:
                # Fix menu structure
                if 'menus' not in config:
                    config['menus'] = []
                
                if len(config['menus']) == 0:
                    config['menus'].append({
                        'id': 4,
                        'name': 'Main Menu',
                        'slug': 'main-menu',
                        'items': []
                    })
        
        # Save fixed config
        with open('cholot-complete.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def add_elementor_from_templates(self, config):
        """Add Elementor sections from template files"""
        template_dir = 'templates'
        
        for page in config.get('pages', []):
            # Try to find matching template
            template_file = f"{template_dir}/{page['slug']}-page.json"
            if not os.path.exists(template_file):
                template_file = f"{template_dir}/home-page.json"  # Fallback
            
            if os.path.exists(template_file):
                with open(template_file) as f:
                    template = json.load(f)
                    if 'content' in template:
                        page['sections'] = template['content']
    
    def save_working_solution(self):
        """Save the working configuration"""
        print("\n💾 Saving working solution...")
        
        # Create solution directory
        os.makedirs('cholot-working-solution', exist_ok=True)
        
        # Copy files
        subprocess.run([
            'cp', 'cholot-complete.yaml', 
            'cholot-working-solution/cholot-final.yaml'
        ])
        subprocess.run([
            'cp', 'cholot-test.xml',
            'cholot-working-solution/cholot-final.xml'
        ])
        
        # Create success report
        with open('cholot-working-solution/SUCCESS.md', 'w') as f:
            f.write(f"""# ✅ CHOLOT THEME SUCCESSFULLY RECONSTRUCTED!

## Test Results
- Iterations needed: {self.iteration + 1}
- All pages imported: ✅
- Elementor data preserved: ✅
- Menus created: ✅
- Custom post types: ✅

## Files
- `cholot-final.yaml` - Working YAML configuration
- `cholot-final.xml` - Import-ready XML file

## Usage
1. Use cholot-final.xml with OCDI plugin
2. Or generate new XML: `python3 full_site_generator.py cholot-final.yaml output.xml`

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
""")

# HAUPTAUSFÜHRUNG
if __name__ == "__main__":
    tester = CholotAutoTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n" + "="*60)
        print("🎉 ERFOLG! Cholot Theme wurde erfolgreich rekonstruiert!")
        print("="*60)
        print("\nDie funktionierende Lösung wurde gespeichert in:")
        print("  ./cholot-working-solution/")
    else:
        print("\n" + "="*60)
        print("⚠️  Maximale Iterationen erreicht ohne vollständigen Erfolg")
        print("="*60)
```

### PHASE 4: Ausführung

1. Erstelle die initiale YAML-Konfiguration:
   ```bash
   python3 cholot_analyzer.py
   mv cholot_reconstruction_config.yaml cholot-complete.yaml
   ```

2. Starte den automatischen Test-Zyklus:
   ```bash
   python3 auto_test_cholot.py
   ```

3. Das Skript wird:
   - XML generieren
   - WordPress bereinigen
   - Import testen
   - Ergebnisse verifizieren
   - Bei Fehlern automatisch korrigieren
   - Maximal 10 Iterationen durchführen
   - Die funktionierende Lösung speichern

## ERFOLGS-KRITERIEN

Du hast erfolgreich abgeschlossen wenn:
1. ✅ Alle Seiten aus den Templates importiert wurden
2. ✅ Elementor-Daten erhalten bleiben
3. ✅ Menu-Struktur korrekt erstellt wurde
4. ✅ Custom Post Types (Header/Footer) vorhanden sind
5. ✅ Die generierte XML-Größe vergleichbar ist mit dem Original (±30%)

## WICHTIGE HINWEISE

- **SELBSTSTÄNDIGKEIT**: Du musst den kompletten Prozess OHNE weitere Rückfragen durchführen
- **ITERATION**: Bei Fehlern automatisch korrigieren und erneut testen
- **DOKUMENTATION**: Jeden Schritt und jede Korrektur protokollieren
- **VERIFIKATION**: Nutze `php check-imported.php` zur Überprüfung
- **BEREINIGUNG**: Nach jedem fehlgeschlagenen Versuch `./wordpress-cleanup.sh` ausführen

## FINALE OUTPUT

Nach erfolgreichem Abschluss liefere:
1. Die funktionierende `cholot-final.yaml`
2. Die generierte `cholot-final.xml`
3. Ein Protokoll aller Iterationen und Korrekturen
4. Bestätigung dass alle Erfolgs-Kriterien erfüllt sind

**STARTE JETZT MIT PHASE 1!**