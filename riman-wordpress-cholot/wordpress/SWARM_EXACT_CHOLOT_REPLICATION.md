# 🎯 SWARM MISSION: EXAKTE CHOLOT XML REPLIKATION

## KRITISCHES ZIEL
**Du musst eine YAML-Datei erstellen, die mit `full_site_generator.py` eine XML erzeugt, die IDENTISCH zu `/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml` ist.**

## ERFOLGS-DEFINITION
```bash
# Diese beiden Befehle müssen das GLEICHE Ergebnis zeigen:
diff cholot-generated.xml /Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml

# Oder minimal diese Kriterien erfüllen:
- Gleiche Anzahl <item> Elemente (65)
- Gleiche Page-Titel und Slugs
- Gleiche Menu-Struktur
- Gleiche Elementor-Datenstruktur
- Gleiche Custom Widget Types (cholot-*)
```

## ARBEITSWEISE

### SCHRITT 1: ZIEL-XML VOLLSTÄNDIG VERSTEHEN
```python
import xml.etree.ElementTree as ET
import json

# Parse die Ziel-XML
tree = ET.parse('/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml')
root = tree.getroot()

# Extrahiere ALLES was du replizieren musst:
target_structure = {
    'pages': [],
    'menus': [],
    'posts': [],
    'media': [],
    'custom_widgets': set(),
    'elementor_structures': []
}

# Für jedes Item mit Elementor-Daten
for item in root.findall('.//item'):
    title = item.find('.//title').text
    
    # Finde Elementor-Daten
    for meta in item.findall('.//wp:postmeta', {'wp': 'http://wordpress.org/export/1.2/'}):
        key = meta.find('.//wp:meta_key', {'wp': 'http://wordpress.org/export/1.2/'})
        if key.text == '_elementor_data':
            value = meta.find('.//wp:meta_value', {'wp': 'http://wordpress.org/export/1.2/'}).text
            elementor_data = json.loads(value)
            
            # DIES ist was du nachbauen musst!
            print(f"Seite: {title}")
            print(f"Elementor-Struktur: {json.dumps(elementor_data, indent=2)}")
            
            # Sammle alle Widget-Types
            extract_widget_types(elementor_data, target_structure['custom_widgets'])
```

### SCHRITT 2: TEMPLATES ALS BAUSTEINE VERWENDEN
```python
# Die Templates enthalten die EXAKTEN Elementor-Strukturen
templates_dir = './templates/'
blocks_dir = './elementor blocks/'

# Mappe Ziel-Seiten zu verfügbaren Templates
page_to_template_mapping = {}

for target_page in target_structure['pages']:
    # Finde das passende Template
    best_match = find_matching_template(target_page, templates_dir)
    if best_match:
        page_to_template_mapping[target_page['slug']] = best_match
    else:
        # Baue aus Blocks zusammen
        page_to_template_mapping[target_page['slug']] = build_from_blocks(target_page, blocks_dir)
```

### SCHRITT 3: YAML GENERIERUNG MIT EXAKTER STRUKTUR
```yaml
# cholot-exact.yaml
site:
  title: "Cholot – Retirement Community WordPress Theme"
  url: "http://ridianur.com/wp/cholot"
  description: "Just another Ridianur WordPress Theme Sites site"

# WICHTIG: Die IDs müssen mit der Ziel-XML übereinstimmen!
pages:
  - id: 1674  # EXAKT wie in demo-data-fixed.xml
    title: "Home 1"
    slug: "home-1"
    template: "elementor_canvas"
    elementor_data: # Direkt aus templates/home-page.json
      - id: "5a8c92f"
        elType: "section"
        settings:
          structure: "20"
        elements:
          # EXAKTE Struktur aus dem Template
          
  - id: 1656
    title: "Home"
    slug: "home"
    # ... etc für ALLE 65 Items
    
menus:
  - id: 178  # Menu ID aus Ziel-XML
    name: "Main Menu"
    slug: "main-menu"
    items:
      - id: 1710
        title: "Home"
        object_id: 1656  # Verweist auf Page ID
        parent: 0
      # ALLE Menu-Items genau wie im Original
```

### SCHRITT 4: AUTOMATISIERTER TEST-ZYKLUS MIT VERGLEICH

```python
#!/usr/bin/env python3
import subprocess
import xml.etree.ElementTree as ET
import difflib
import json

class CholtExactReplicator:
    def __init__(self):
        self.target_xml = '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml'
        self.max_iterations = 20
        self.current_yaml = 'cholot-exact.yaml'
        
    def run(self):
        for iteration in range(self.max_iterations):
            print(f"\n{'='*60}")
            print(f"ITERATION {iteration + 1}")
            print('='*60)
            
            # 1. Generate XML from YAML
            result = subprocess.run([
                'python3', 'full_site_generator.py',
                self.current_yaml,
                'cholot-generated.xml'
            ], capture_output=True)
            
            # 2. Compare with target
            comparison = self.compare_xmls('cholot-generated.xml', self.target_xml)
            
            if comparison['identical']:
                print("🎉 PERFEKT! XML ist IDENTISCH zum Original!")
                return True
            
            # 3. Analyze differences
            print(f"\n❌ Unterschiede gefunden:")
            print(f"  - Fehlende Items: {comparison['missing_items']}")
            print(f"  - Extra Items: {comparison['extra_items']}")
            print(f"  - Falsche Widgets: {comparison['wrong_widgets']}")
            
            # 4. Fix YAML based on differences
            self.fix_yaml_based_on_diff(comparison)
            
        return False
    
    def compare_xmls(self, generated, target):
        """Detaillierter XML-Vergleich"""
        gen_tree = ET.parse(generated)
        target_tree = ET.parse(target)
        
        comparison = {
            'identical': False,
            'missing_items': [],
            'extra_items': [],
            'wrong_widgets': []
        }
        
        # Vergleiche Item-Anzahl
        gen_items = gen_tree.findall('.//item')
        target_items = target_tree.findall('.//item')
        
        if len(gen_items) != len(target_items):
            comparison['item_count_mismatch'] = f"{len(gen_items)} vs {len(target_items)}"
        
        # Vergleiche Titles
        gen_titles = {item.find('.//title').text for item in gen_items}
        target_titles = {item.find('.//title').text for item in target_items}
        
        comparison['missing_items'] = list(target_titles - gen_titles)
        comparison['extra_items'] = list(gen_titles - target_titles)
        
        # Vergleiche Elementor-Strukturen
        for target_item in target_items:
            title = target_item.find('.//title').text
            gen_item = self.find_item_by_title(gen_tree, title)
            
            if gen_item:
                # Vergleiche Elementor-Daten
                target_elementor = self.get_elementor_data(target_item)
                gen_elementor = self.get_elementor_data(gen_item)
                
                if target_elementor and gen_elementor:
                    if not self.compare_elementor_structures(target_elementor, gen_elementor):
                        comparison['wrong_widgets'].append(title)
        
        comparison['identical'] = (
            len(comparison['missing_items']) == 0 and
            len(comparison['extra_items']) == 0 and
            len(comparison['wrong_widgets']) == 0
        )
        
        return comparison
    
    def fix_yaml_based_on_diff(self, comparison):
        """Korrigiere YAML basierend auf Unterschieden"""
        import yaml
        
        with open(self.current_yaml, 'r') as f:
            config = yaml.safe_load(f)
        
        # Füge fehlende Items hinzu
        for missing_title in comparison['missing_items']:
            print(f"  ➕ Füge hinzu: {missing_title}")
            # Extrahiere aus Ziel-XML und füge zu YAML hinzu
            self.add_item_from_target(config, missing_title)
        
        # Entferne extra Items
        for extra_title in comparison['extra_items']:
            print(f"  ➖ Entferne: {extra_title}")
            config['pages'] = [p for p in config.get('pages', []) if p['title'] != extra_title]
        
        # Korrigiere Widget-Strukturen
        for wrong_page in comparison['wrong_widgets']:
            print(f"  🔧 Korrigiere Widgets in: {wrong_page}")
            self.fix_widget_structure(config, wrong_page)
        
        # Speichere korrigierte YAML
        with open(self.current_yaml, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def add_item_from_target(self, config, title):
        """Füge Item aus Ziel-XML zu Config hinzu"""
        target_tree = ET.parse(self.target_xml)
        item = self.find_item_by_title(target_tree, title)
        
        if item:
            # Extrahiere alle Daten
            page_data = self.extract_page_data(item)
            
            # Suche passendes Template
            template_file = self.find_matching_template(page_data)
            if template_file:
                with open(template_file) as f:
                    template_data = json.load(f)
                    page_data['sections'] = template_data.get('content', [])
            
            config['pages'].append(page_data)
    
    def find_matching_template(self, page_data):
        """Finde das beste Template für eine Seite"""
        import os
        
        # Suche nach Slug-Match
        slug = page_data.get('slug', '')
        
        # Versuche exakten Match
        template_candidates = [
            f'templates/{slug}.json',
            f'templates/{slug}-page.json',
            f'templates/{slug.replace("-", "_")}.json'
        ]
        
        for candidate in template_candidates:
            if os.path.exists(candidate):
                return candidate
        
        # Fallback auf home-page.json für Homepage-ähnliche
        if 'home' in slug.lower():
            return 'templates/home-page.json'
        
        return None

# AUSFÜHRUNG
if __name__ == "__main__":
    replicator = CholtExactReplicator()
    success = replicator.run()
    
    if success:
        print("\n" + "="*60)
        print("✅ ERFOLG! Exakte Cholot XML wurde repliziert!")
        print("="*60)
        print("\nDie finale YAML ist: cholot-exact.yaml")
        print("Die generierte XML ist: cholot-generated.xml")
        print("\nÜberprüfung:")
        print("  diff cholot-generated.xml", replicator.target_xml)
    else:
        print("\n⚠️ Konnte keine exakte Replikation erreichen")
        print("Prüfe die Logs für Details")
```

## WICHTIGE REGELN

1. **EXAKTHEIT**: Die generierte XML muss IDENTISCH zur Ziel-XML sein (oder minimal alle wichtigen Elemente enthalten)

2. **VERWENDUNG DER TEMPLATES**: Die JSON-Dateien in `./templates/` enthalten die EXAKTEN Elementor-Strukturen - nutze sie!

3. **ITERATIVE VERBESSERUNG**: Nach jeder Generation:
   - Vergleiche mit Ziel-XML
   - Identifiziere Unterschiede
   - Korrigiere YAML
   - Generiere erneut
   - Wiederhole bis identisch

4. **KEINE IMPROVISATION**: Erfinde keine Inhalte - extrahiere ALLES aus:
   - Der Ziel-XML
   - Den vorhandenen Templates
   - Den Elementor Blocks

5. **TEST-BEWEISE**: Du musst BEWEISEN dass deine Lösung funktioniert:
   ```bash
   # Diese Befehle müssen erfolgreich sein:
   python3 full_site_generator.py cholot-exact.yaml cholot-generated.xml
   
   # Und dieser Vergleich muss minimal differences zeigen:
   diff -u cholot-generated.xml /Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml
   ```

## LIEFERUNG

Nach erfolgreichem Abschluss liefere:

1. **cholot-exact.yaml** - Die YAML die die exakte XML erzeugt
2. **cholot-generated.xml** - Die generierte XML (sollte identisch zum Original sein)
3. **comparison-report.txt** - Diff-Output der zeigt dass beide XMLs identisch/sehr ähnlich sind
4. **generation.log** - Log aller Iterationen und Korrekturen

**STARTE JETZT und höre NICHT AUF bis die XMLs übereinstimmen!**