# SWARM Cholot WordPress Test Orchestrator

## Mission
Erstelle einen vollständig automatisierten Test-Prozess für die Cholot WordPress/Elementor XML-Generierung mit visueller Verifizierung.

## Context
- **Original-Site**: localhost:8080 - Korrekte Cholot-Implementation mit allen Widgets
- **Test-Site**: localhost:8081 - Für Import der generierten XML
- **Working Directory**: `/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress`
- **OCDI Plugin**: Bereits installiert unter `/wp-content/plugins/one-click-demo-import/`

## Phase 1: Test-Script Erstellung
Erstelle `cholot-test-suite.py` mit folgenden Komponenten:

### 1.1 Import-Modul
```python
class CholotImporter:
    def __init__(self, site_url="http://localhost:8081"):
        self.site_url = site_url
        
    def prepare_wordpress(self):
        """Reset WordPress für sauberen Test"""
        # - Lösche alle Seiten außer Privacy Policy
        # - Lösche alle Posts
        # - Setze Theme auf cholot-child
        # - Aktiviere erforderliche Plugins
        
    def import_xml_via_ocdi(self, xml_path):
        """Import XML über One Click Demo Import"""
        # - Kopiere XML nach wp-content/uploads/[year]/[month]/demo-import-files/
        # - Erstelle OCDI-kompatible Import-Konfiguration
        # - Triggere Import über OCDI Admin-Ajax
        # - Warte auf Import-Abschluss
        
    def fix_homepage_settings(self):
        """Korrigiere WordPress Homepage-Einstellungen nach Import"""
        # - Finde die Home-Seite mit Elementor-Daten
        # - Setze show_on_front = 'page'
        # - Setze page_on_front auf Home-ID
```

### 1.2 Vergleichs-Modul mit Playwright
```python
class CholotVisualTester:
    def __init__(self):
        self.original_url = "http://localhost:8080"
        self.test_url = "http://localhost:8081"
        
    async def capture_screenshots(self):
        """Erfasse Screenshots beider Sites"""
        # - Navigiere zu beiden URLs
        # - Warte auf vollständiges Laden (Elementor-Widgets)
        # - Erstelle Screenshots: Full-Page und Viewport
        # - Speichere mit Zeitstempel
        
    async def compare_elements(self):
        """Vergleiche DOM-Struktur und Inhalte"""
        # Prüfe auf Original-Site vorhandene Elemente:
        # - Hero Slider mit Cholot-Texten
        # - Service Cards (cholot-texticon widgets)
        # - Team Members Section
        # - Testimonials Carousel
        # - Contact Form
        
    def generate_report(self):
        """Erstelle visuellen Vergleichsbericht"""
        # - Screenshot-Vergleich
        # - Element-Differenzen
        # - Fehlende Widgets/Sections
        # - Erfolgsrate in Prozent
```

### 1.3 Haupt-Test-Runner
```python
class CholotTestRunner:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.importer = CholotImporter()
        self.tester = CholotVisualTester()
        
    async def run_full_test(self):
        """Führe kompletten Test-Zyklus durch"""
        print("🧹 Phase 1: WordPress vorbereiten...")
        self.importer.prepare_wordpress()
        
        print("📥 Phase 2: XML importieren...")
        self.importer.import_xml_via_ocdi(self.xml_path)
        
        print("🔧 Phase 3: Homepage-Einstellungen korrigieren...")
        self.importer.fix_homepage_settings()
        
        print("📸 Phase 4: Screenshots erstellen...")
        await self.tester.capture_screenshots()
        
        print("🔍 Phase 5: Elemente vergleichen...")
        results = await self.tester.compare_elements()
        
        print("📊 Phase 6: Report generieren...")
        report = self.tester.generate_report()
        
        return {
            "success": results['match_rate'] > 90,
            "match_rate": results['match_rate'],
            "report": report,
            "screenshots": results['screenshots']
        }
```

## Phase 2: Design-Review Agent Integration

### 2.1 Automatische visuelle Prüfung
Nach dem Import und Screenshot-Erstellung:

1. **Starte design-review Agent** mit:
   - URL Original: http://localhost:8080
   - URL Test: http://localhost:8081
   - Prüfkriterien:
     - Visuelle Konsistenz der Cholot-Elemente
     - Korrekte Widget-Darstellung
     - Responsive Design auf Mobile/Tablet
     - Farbschema und Typography
     - Interactive Elements (Slider, Hover-Effects)

2. **Agent soll prüfen**:
   - Sind alle Service-Cards sichtbar?
   - Funktioniert der Hero-Slider?
   - Werden Team-Members korrekt angezeigt?
   - Ist das Testimonial-Carousel aktiv?
   - Stimmt das Layout überein?

### 2.2 Fehler-Feedback Loop
Bei Fehler: Agent soll konkrete Korrektur-Vorschläge machen:
- Fehlende Elementor-Data in XML
- Falsche Widget-Types
- Missing Assets/Images
- CSS/JS Dependencies

## Phase 3: Iterative Korrektur

### 3.1 XML-Generator Anpassung
Basierend auf Test-Ergebnissen:
```python
class XMLCorrector:
    def analyze_failures(self, test_report):
        """Analysiere was in der XML fehlt"""
        
    def patch_xml(self, original_xml, corrections):
        """Korrigiere die XML basierend auf Fehler-Analyse"""
        
    def validate_xml(self, xml_path):
        """Validiere XML-Struktur vor erneutem Import"""
```

### 3.2 Automatischer Re-Test
```python
max_iterations = 3
for iteration in range(max_iterations):
    results = await runner.run_full_test()
    if results['success']:
        print(f"✅ Test erfolgreich nach {iteration+1} Iterationen!")
        break
    else:
        print(f"❌ Iteration {iteration+1} fehlgeschlagen. Korrigiere XML...")
        corrected_xml = corrector.patch_xml(xml_path, results['failures'])
        xml_path = corrected_xml
```

## Execution Command
```bash
# Führe den kompletten Test-Zyklus aus
python cholot-test-suite.py --xml generated-cholot.xml --iterations 3 --visual-review
```

## Success Criteria
- ✅ Alle Cholot-Widgets werden korrekt angezeigt
- ✅ Homepage zeigt Elementor-Content (nicht Blog-Posts)
- ✅ Service-Cards mit Icons und Texten sichtbar
- ✅ Hero-Slider funktioniert
- ✅ Team-Section vorhanden
- ✅ Testimonials-Carousel aktiv
- ✅ Responsive Design funktioniert
- ✅ Visuelle Übereinstimmung > 90%

## Output
Der Test soll generieren:
1. `test-report-[timestamp].html` - Visueller Bericht
2. `screenshots/` - Vergleichs-Screenshots
3. `corrections.json` - Liste der nötigen XML-Korrekturen
4. `success.log` - Bei erfolgreichem Import

## WICHTIG
- Verwende Playwright MCP für Browser-Automation
- Nutze design-review Agent für visuelle Prüfung
- One Click Demo Import Plugin für XML-Import
- Teste IMMER auf localhost:8081 (Test-Site)
- Vergleiche IMMER mit localhost:8080 (Original)