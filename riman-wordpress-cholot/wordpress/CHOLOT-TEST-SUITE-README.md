# CHOLOT TEST SUITE - OCDI Import & Visual Verification

**Automatisierte Test-Pipeline für Cholot WordPress Import**

Erstellt von **SWARM CHOLOT TESTER** für vollständige OCDI Import-Verifizierung.

## 🎯 Überblick

Diese Test-Suite bietet:
- **OCDI Import Management** - Direkter WordPress XML Import via One Click Demo Import Plugin
- **Visuelle Verifizierung** - Playwright-basierte Screenshot-Vergleiche
- **Automatische Korrektur** - Iterative XML-Korrektur bei Import-Fehlern
- **Umfassende Reports** - Detaillierte Test-Berichte und Quality Scores

## 🏗️ Architektur

### Hauptkomponenten

1. **`cholot-test-suite.py`** - Zentrale Test-Suite mit allen Klassen
2. **`test-ocdi-import.php`** - PHP-Script für direkten OCDI Import
3. **`set-homepage.php`** - Homepage-Konfiguration nach Import
4. **`verify-elementor.php`** - Elementor Daten-Verifizierung
5. **`compare-sites.py`** - Site-Vergleich zwischen localhost:8080 & 8081

### Klassen-Struktur

```python
CholotImporter        # OCDI Import Management
CholotVisualTester    # Playwright Visual Testing  
CholotTestRunner      # Automatischer Test-Zyklus
XMLCorrector          # Iterative XML-Korrektur
```

## 🚀 Quick Start

### 1. Einzelne Komponenten testen

```bash
# XML Import ausführen
php test-ocdi-import.php cholot-final.xml

# Homepage konfigurieren
php set-homepage.php "Home"

# Elementor Daten prüfen
php verify-elementor.php --detailed

# Sites vergleichen
python3 compare-sites.py
```

### 2. Vollständige Test-Suite ausführen

```bash
python3 cholot-test-suite.py
```

## 📋 Voraussetzungen

### WordPress Setup
- WordPress Installation auf `localhost:8080` (Original)
- WordPress Installation auf `localhost:8081` (Test)
- **One Click Demo Import Plugin** installiert und aktiviert
- **Elementor Plugin** installiert und aktiviert
- **Cholot Theme** aktiviert

### Python Dependencies
```bash
pip install requests pyyaml
pip install playwright  # Für visuelle Tests
playwright install chromium  # Browser für Screenshots
```

### XML Files
- `cholot-final.xml` - Hauptimport-Datei
- `riman-complete.xml` - Alternative Import-Datei
- `cholot-complete-content.xml` - Vollständige Content-Version

## 🔧 Konfiguration

### Test-Einstellungen
```python
config = {
    'xml_files_to_test': [
        'cholot-final.xml',
        'riman-complete.xml'
    ],
    'pages_to_test': ['/', '/about', '/services', '/contact'],
    'max_correction_iterations': 3,
    'screenshot_comparison': True
}
```

### URLs anpassen
```python
original_url = "http://localhost:8080"  # Original Site
test_url = "http://localhost:8081"      # Test Site
```

## 📊 Test-Pipeline

### Phase 1: XML Import Testing
1. **XML Analyse** - Struktur und Inhalte analysieren
2. **OCDI Import** - Import via One Click Demo Import
3. **Error Handling** - Automatische Korrektur bei Fehlern
4. **Iteration** - Bis zu 3 Korrektur-Iterationen
5. **Verification** - Import-Ergebnisse validieren

### Phase 2: Visual Testing
1. **Screenshot Capture** - Beide Sites screenshotten
2. **Elementor Analysis** - Widget & Section-Vergleich
3. **Content Comparison** - HTML-Inhalt vergleichen
4. **Performance Check** - Ladezeiten messen

### Phase 3: Report Generation
1. **Quality Score** - 0-100 Punkte Bewertung
2. **Detailed Analysis** - Pro-Seite Ergebnisse
3. **Recommendations** - Verbesserungsvorschläge
4. **JSON Export** - Maschinenlesbare Ergebnisse

## 📈 Quality Scoring

### Bewertungskriterien
- **XML Import Success** (40 Punkte)
  - Pages imported: 20 Punkte
  - Posts imported: 10 Punkte
  - Media imported: 10 Punkte

- **Elementor Import** (40 Punkte) 
  - Elementor pages found: 20 Punkte
  - Elements functioning: 15 Punkte
  - No errors: 5 Punkte

- **Homepage Setup** (20 Punkte)
  - Home page exists: 10 Punkte
  - Correctly configured: 10 Punkte

### Score Interpretation
- **90-100**: 🏆 EXCELLENT - Production ready
- **75-89**: ✅ GOOD - Minor issues
- **60-74**: ⚠️ FAIR - Review required
- **0-59**: ❌ POOR - Major issues

## 🛠️ Fehlerbehebung

### OCDI Plugin Fehler
```bash
# Plugin-Status prüfen
ls -la wp-content/plugins/one-click-demo-import/

# WordPress-Berechtigung prüfen
chmod 755 wp-content/
chmod -R 644 wp-content/plugins/
```

### Elementor Import Probleme
```bash
# Elementor Daten detailliert prüfen
php verify-elementor.php --detailed --page-id=123

# Alle Seiten analysieren
php verify-elementor.php --detailed
```

### Visual Testing Issues
```bash
# Playwright Setup prüfen
playwright --version

# Browser installieren
playwright install chromium

# Manual Screenshot Test
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:8080')
    page.screenshot(path='test.png')
    browser.close()
"
```

## 📁 Output Files

### Generierte Reports
- `cholot-test-report-[timestamp].md` - Markdown Report
- `cholot-test-summary-[timestamp].json` - JSON Summary
- `cholot-import-report-[timestamp].json` - Import Details
- `site-comparison-[timestamp].json` - Visual Comparison

### Screenshots (bei Visual Testing)
- `test-screenshots/original-[page]-[timestamp].png`
- `test-screenshots/test-[page]-[timestamp].png`

### Memory Storage
- `memory-[key].json` - Test-Daten im Memory Namespace

## 🔄 Workflow Integration

### Typischer Ablauf
```bash
# 1. Fresh WordPress Setup (localhost:8081)
# 2. OCDI Plugin installieren
# 3. Import testen
php test-ocdi-import.php cholot-final.xml

# 4. Homepage konfigurieren
php set-homepage.php

# 5. Elementor verifizieren  
php verify-elementor.php

# 6. Visueller Vergleich
python3 compare-sites.py

# 7. Vollständige Test-Suite (optional)
python3 cholot-test-suite.py
```

### CI/CD Integration
```bash
#!/bin/bash
# Automated test script
cd /path/to/wordpress

# Run OCDI import
php test-ocdi-import.php cholot-final.xml
if [ $? -ne 0 ]; then
    echo "Import failed"
    exit 1
fi

# Verify results
php verify-elementor.php
python3 compare-sites.py

echo "Tests completed successfully"
```

## 💾 Memory Namespace

Alle Test-Daten werden im Memory Namespace gespeichert:
**`swarm-cholot-tester-1756407314892`**

### Gespeicherte Daten
- `suite/implementation` - Test-Suite Ergebnisse
- `import/results` - Import-Details
- `visual/comparison` - Visuelle Vergleiche
- `corrections/history` - XML-Korrektur Historie

## 📞 Support & Debugging

### Logging
Alle Aktivitäten werden geloggt in:
- `cholot-test-[session-id].log`
- WordPress error logs
- PHP error logs

### Debug-Modus
```python
# In cholot-test-suite.py
logging.basicConfig(level=logging.DEBUG)

# Für detaillierte Ausgabe
detailed = True
```

### Häufige Probleme
1. **OCDI Plugin nicht gefunden** → Plugin installieren/aktivieren
2. **Elementor Daten fehlen** → XML-Datei auf Elementor Meta prüfen
3. **Screenshots fehlgeschlagen** → Playwright Setup prüfen
4. **Sites nicht erreichbar** → WordPress-Server Status prüfen

---

**Memory Namespace**: `swarm-cholot-tester-1756407314892`
**Erstellt**: 2025-08-28
**Author**: Claude Code Assistant (OCDI TEST SUITE BUILDER)