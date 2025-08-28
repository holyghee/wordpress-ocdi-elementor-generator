# Troubleshooting Guide

## Häufige Probleme und Lösungen

### 1. Import-Probleme

#### Problem: "Elementor zeigt leere Seite"
**Symptome:**
- WordPress-Import erfolgreich
- Seite wird angelegt, aber Elementor-Editor zeigt keine Inhalte

**Lösungen:**
✅ **Verwende `section_based_processor.py`**
- Container-basierte Versionen können inkompatibel sein
- Classic Section/Column-Struktur ist universell kompatibel

✅ **Elementor Cache leeren**
```bash
# WordPress Admin → Elementor → Tools → Regenerate Files & Data
```

✅ **WordPress Cache leeren**
- Plugins: WP Super Cache, W3 Total Cache deaktivieren
- Server-Cache (Cloudflare, etc.) leeren

#### Problem: "Import schlägt fehl"
**Fehlermeldung:** `Fatal error during import`

**Lösungen:**
✅ **"Import author" aktivieren**
- WordPress Admin → Tools → Import
- ☑️ "Download and import file attachments" aktivieren
- ☑️ "Import author" aktivieren

✅ **WordPress Speicherlimit erhöhen**
```php
// wp-config.php
ini_set('memory_limit', '256M');
ini_set('max_execution_time', 300);
```

✅ **XML-Datei validieren**
```bash
# XML-Syntax prüfen
python3 -c "import xml.etree.ElementTree as ET; ET.parse('generated/output.xml')"
```

### 2. Widget-Probleme

#### Problem: "Widgets werden nicht angezeigt"
**Symptome:**
- Elementor-Editor zeigt Widgets
- Frontend zeigt leere Bereiche

**Lösungen:**
✅ **Font Awesome Icons prüfen**
```yaml
# Korrekte Syntax
icon: "fas fa-shield-alt"

# Falsche Syntax  
icon: "fa-shield-alt"        # ❌ Fehlt "fas"
icon: "fas shield-alt"       # ❌ Fehlt "fa-"
```

✅ **Bild-URLs validieren**
- Vollständige URLs verwenden: `https://example.com/image.jpg`
- HTTPS verwenden (nicht HTTP)
- Bildgrößen unter 5MB halten

✅ **Widget-Kompatibilität prüfen**
- Nur Standard-Elementor-Widgets verwenden
- Pro-Widgets vermeiden, wenn Elementor Free verwendet wird

#### Problem: "Icons werden nicht angezeigt"
**Lösungen:**
✅ **Font Awesome aktivieren**
```bash
# WordPress Admin → Elementor → Settings → Advanced
# Font Awesome: Enable
```

✅ **Icon-Bibliothek prüfen**
```python
"selected_icon": {
    "value": "fas fa-shield-alt",    # Font Awesome Solid
    "library": "fa-solid"            # Bibliothek angeben
}
```

### 3. Layout-Probleme

#### Problem: "Titel erscheinen neben Content statt darüber"
**Lösung:**
✅ **Section-basierte Struktur verwenden**
- `section_based_processor.py` verwendet automatisch getrennte Sections
- Titel und Content werden in separate Sections aufgeteilt

#### Problem: "Responsive Layout funktioniert nicht"
**Lösungen:**
✅ **Column-Größen prüfen**
```python
"settings": {
    "_column_size": 33.33,    # Für 3 Spalten
    "_column_size": 25        # Für 4 Spalten
}
```

✅ **Container-Breite anpassen**
```yaml
elementor_settings:
  container_width: 1170      # Standard-Breite
```

### 4. Performance-Probleme

#### Problem: "XML-Generation zu langsam"
**Lösungen:**
✅ **Anzahl Services/Team-Mitglieder begrenzen**
```yaml
services: [...] # Max. 4 Services empfohlen
members: [...]  # Max. 3 Team-Mitglieder
```

✅ **Bild-Optimierung**
- WebP-Format verwenden
- Bildgrößen optimieren (max. 1920x1080 für Hero-Images)
- CDN für Bilder verwenden

#### Problem: "Zu große XML-Dateien"
**Lösungen:**
✅ **JSON komprimieren**
```python
clean_json = json.dumps(elementor_data, separators=(',', ':'))
```

✅ **Unnötige Sections entfernen**
- Nur benötigte Section-Typen verwenden
- Leere Sections automatisch ausschließen

### 5. YAML-Konfigurationsfehler

#### Problem: "YAML-Parsing-Fehler"
**Fehlermeldungen:**
- `yaml.scanner.ScannerError`
- `yaml.parser.ParserError`

**Lösungen:**
✅ **Einrückung prüfen**
```yaml
# Korrekt (2 Spaces)
pages:
  - title: "Test"
    sections:
      - type: "hero"

# Falsch (Tab/gemischte Einrückung)
pages:
	- title: "Test"
    sections:
		- type: "hero"
```

✅ **Sonderzeichen escapen**
```yaml
# Korrekt
title: "Test: \"Zitat\" mit Sonderzeichen"

# Falsch
title: Test: "Zitat" mit Sonderzeichen
```

✅ **YAML-Validator verwenden**
```bash
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### 6. WordPress-spezifische Probleme

#### Problem: "Seite wird nicht als Elementor-Seite erkannt"
**Lösungen:**
✅ **Template korrekt setzen**
```yaml
pages:
  - template: "elementor_canvas"    # Elementor Full Width
    # oder
    template: "elementor_header_footer"  # Mit Header/Footer
```

✅ **Meta-Felder prüfen**
- `_elementor_edit_mode`: "builder"
- `_elementor_template_type`: "wp-page"

#### Problem: "Elementor-Daten werden nicht gespeichert"
**Lösungen:**
✅ **JSON-Escaping prüfen**
```python
# Korrekte Escaping-Methode
clean_json = json.dumps(elementor_data, separators=(',', ':'))
```

✅ **WordPress-Berechtigungen prüfen**
- Benutzer muss "edit_posts"-Berechtigung haben
- Elementor-Plugin muss aktiv sein

### 7. Debug-Methoden

#### Debug-Modus aktivieren
```python
# In section_based_processor.py
DEBUG = True

if DEBUG:
    print(f"Generated sections: {len(elementor_data)}")
    for i, section in enumerate(elementor_data):
        print(f"Section {i}: {section.get('elType')} - {len(section.get('elements', []))} columns")
```

#### JSON-Debug-Output
```python
# JSON für Analyse speichern
with open('debug_output.json', 'w') as f:
    json.dump({
        'config': config,
        'elementor_data': elementor_data,
        'widget_count': count_widgets(elementor_data)
    }, f, indent=2)
```

#### XML-Struktur validieren
```bash
# XML-Struktur überprüfen
xmllint --format --noout generated/output.xml

# Falls xmllint nicht verfügbar:
python3 -c "
import xml.etree.ElementTree as ET
try:
    ET.parse('generated/output.xml')
    print('✅ XML ist valide')
except ET.ParseError as e:
    print(f'❌ XML-Fehler: {e}')
"
```

### 8. WordPress-Logs analysieren

#### Debug-Log aktivieren
```php
// wp-config.php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

#### Log-Dateien prüfen
```bash
# WordPress Debug-Log
tail -f wp-content/debug.log

# Server Error-Log
tail -f /var/log/apache2/error.log
# oder
tail -f /var/log/nginx/error.log
```

### 9. Notfall-Lösungen

#### Minimale Test-Konfiguration
```yaml
# test-minimal.yaml
site:
  title: "Test"
  base_url: "http://localhost"

pages:
  - title: "Test Page"
    sections:
      - type: "hero_slider"
        slides:
          - title: "Test"
            text: "Test"
            image: "https://picsum.photos/1920/1080"
```

#### Reset Elementor-Daten
```sql
-- WordPress-Datenbank
DELETE FROM wp_postmeta WHERE meta_key LIKE '_elementor%';
```

#### Cache komplett leeren
```bash
# Alle WordPress-Caches
wp cache flush
wp transient delete --all

# Elementor-spezifisch
wp elementor flush-css
```

### 10. Support-Informationen sammeln

#### System-Information
```bash
# PHP-Version
php --version

# WordPress-Version  
wp core version

# Elementor-Version
wp plugin get elementor --field=version

# Aktive Plugins
wp plugin list --status=active
```

#### Fehler-Report erstellen
```python
def create_error_report():
    return {
        'yaml_file': 'config.yaml',
        'elementor_version': '3.15.0',
        'wordpress_version': '6.3',
        'php_version': '8.1',
        'sections_generated': len(elementor_data),
        'widgets_total': count_widgets(elementor_data),
        'file_size_kb': os.path.getsize('output.xml') / 1024,
        'errors': []
    }
```

## Kontakt für weitere Hilfe

Bei persistenten Problemen:

1. **GitHub Issues**: Detaillierte Bug-Reports mit:
   - YAML-Konfiguration
   - Error-Logs  
   - System-Information
   - Screenshots

2. **Debug-Informationen bereitstellen**:
   - JSON-Debug-Output
   - WordPress-Logs
   - Elementor-Version

3. **Minimales Beispiel erstellen**:
   - Problem mit kleinstmöglicher Konfiguration reproduzieren
   - Test mit `examples/basic-site.yaml`