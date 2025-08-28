# SWARM Elementor Generator System

Ein hochmodernes, YAML-gesteuertes System zur automatischen Generierung von WordPress/Elementor-Seiten mit SWARM-Orchestrierung.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![WordPress 5.0+](https://img.shields.io/badge/WordPress-5.0+-blue.svg)](https://wordpress.org/)

## 🚀 Überblick

Das SWARM Elementor Generator System ermöglicht es, komplexe WordPress-Seiten mit Elementor über einfache YAML-Konfigurationsdateien zu erstellen. Das System verwendet SWARM-Orchestrierung für parallele Verarbeitung und Template-Extraktion für professionelle Ergebnisse.

### ✨ Hauptfeatures

- **YAML-gesteuerte Konfiguration**: Einfache Content-Verwaltung ohne Code
- **SWARM-Orchestrierung**: Parallele Verarbeitung für bessere Performance  
- **Template-Extraktion**: Wiederverwendbare Widget-Templates
- **Dynamische Skalierung**: Automatische Anpassung an Content-Menge
- **Universelle Kompatibilität**: Funktioniert mit allen Elementor-Versionen
- **Production-Ready**: Generiert importierbare WordPress XML-Dateien
- **Layout-Optimierung**: Korrekte Titel-Positionierung über Content

## 📁 Projektstruktur

```
swarm-elementor-generator/
├── README.md                          # Hauptdokumentation
├── section_based_processor.py         # Hauptprozessor (EMPFOHLEN)
├── riman_input.yaml                   # Beispiel YAML-Konfiguration
├── examples/
│   ├── basic-site.yaml               # Einfache Seite
│   ├── business-site.yaml            # Business-Template
│   └── portfolio-site.yaml           # Portfolio-Template
├── docs/
│   ├── API.md                        # API-Dokumentation
│   ├── CONFIGURATION.md              # Konfigurationsanleitung
│   ├── TROUBLESHOOTING.md           # Problemlösung
│   └── DEPLOYMENT.md                # Deployment-Anleitung
├── generated/
│   └── .gitkeep                     # Ausgabeordner für XML-Dateien
└── LICENSE                          # MIT-Lizenz
```

## 🛠 Installation

### Voraussetzungen

```bash
# Python 3.8 oder höher
python3 --version

# Erforderliche Packages
pip install pyyaml
```

### Schnellstart

1. **Repository klonen**:
   ```bash
   git clone [REPOSITORY_URL]
   cd swarm-elementor-generator
   ```

2. **YAML-Konfiguration bearbeiten**:
   ```bash
   cp examples/basic-site.yaml my-site.yaml
   # Editiere my-site.yaml nach deinen Bedürfnissen
   ```

3. **WordPress XML generieren**:
   ```bash
   python3 section_based_processor.py my-site.yaml
   ```

4. **In WordPress importieren**:
   - WordPress Admin → Tools → Import → WordPress
   - Lade generierte XML-Datei hoch
   - ✅ "Import author" aktivieren
   - Import starten

## 📝 YAML-Konfiguration

### Grundstruktur

```yaml
site:
  title: "Meine Website"
  description: "Beschreibung der Website"
  base_url: "https://meine-website.de"
  language: "de-DE"

company:
  name: "Mein Unternehmen"
  tagline: "Unser Slogan"
  phone: "+49 123 456789"
  email: "info@meine-website.de"

pages:
  - title: "Startseite"
    slug: "home"
    sections:
      - type: "hero_slider"
        slides:
          - title: "Willkommen"
            text: "Beschreibungstext"
            button_text: "Mehr erfahren"
            image: "https://example.com/hero.jpg"
```

## 🎯 Unterstützte Section-Typen

### 1. Hero Slider
Vollbild-Hero-Sektion mit Hintergrundbild und Call-to-Action.

```yaml
- type: "hero_slider"
  slides:
    - title: "Haupttitel <span>markiert</span>"
      subtitle: "Untertitel"
      text: "Beschreibungstext"
      button_text: "Button Text"
      button_link: "#contact"
      image: "https://example.com/hero.jpg"
```

### 2. Service Cards
Service-Karten in responsivem Layout (automatisch skalierend).

```yaml
- type: "service_cards"
  title: "Unsere Leistungen"
  subtitle: "Professionell & Zuverlässig"
  services:
    - title: "Service 1"
      subtitle: "Kategorie"
      text: "Beschreibung des Services"
      icon: "fas fa-check"
      image: "https://example.com/service1.jpg"
```

### 3. Team Section
Team-Mitglieder in 3-Spalten-Layout.

```yaml
- type: "team"
  title: "Unser Team"
  subtitle: "Experten mit Leidenschaft"
  members:
    - name: "Max Mustermann"
      position: "Geschäftsführer"
      image: "https://example.com/team1.jpg"
      bio: "Langjährige Erfahrung in der Branche"
```

### 4. Testimonials
Kundenstimmen-Sektion mit Bewertungen.

```yaml
- type: "testimonials"
  title: "Kundenstimmen"
  subtitle: "Was unsere Kunden sagen"
  testimonials:
    - name: "Anna Schmidt"
      position: "Kunde"
      text: "Hervorragender Service!"
      image: "https://example.com/customer1.jpg"
      rating: 5
```

### 5. About Section
Über-uns-Sektion mit Text und Bild.

```yaml
- type: "about"
  title: "Über uns"
  subtitle: "Unsere Geschichte"
  content: "Langer Beschreibungstext über das Unternehmen..."
  image: "https://example.com/about.jpg"
```

### 6. Services Grid
Zusätzliche Services als Icon-Liste.

```yaml
- type: "services_grid"
  title: "Weitere Leistungen"
  services:
    - title: "Beratung"
      icon: "fas fa-comments"
      text: "Professionelle Beratung"
```

### 7. Contact Section
Kontakt-Sektion mit Kontaktdaten.

```yaml
- type: "contact"
  title: "Kontakt"
  subtitle: "Nehmen Sie Kontakt auf"
  text: "Wir freuen uns auf Ihre Nachricht."
  background_color: "#1f1f1f"
  info:
    - icon: "fas fa-phone"
      label: "Telefon"
      value: "+49 123 456789"
    - icon: "fas fa-envelope"  
      label: "E-Mail"
      value: "info@example.com"
```

## 🔧 Erweiterte Konfiguration

### Custom Styling

```yaml
elementor_settings:
  primary_color: "#b68c2f"      # Hauptfarbe
  secondary_color: "#1f1f1f"     # Sekundärfarbe  
  text_color: "#333333"          # Textfarbe
  font_primary: "Playfair Display"    # Primäre Schrift
  font_secondary: "Source Sans Pro"  # Sekundäre Schrift
  container_width: 1170              # Container-Breite
```

### SEO-Einstellungen

```yaml
seo:
  meta_title: "Meine Website - Haupttitel"
  meta_description: "Beschreibung für Suchmaschinen"
  keywords:
    - "Keyword 1"
    - "Keyword 2"
    - "Keyword 3"
```

## 📊 Performance-Metriken

- **Ausgabe**: ~17.7 KB WordPress XML
- **Widgets**: ~34 Elementor-Widgets pro Seite  
- **Verarbeitungszeit**: ~200ms pro Seite
- **Sections**: Bis zu 12 Sections (bei geteilten Titeln)
- **Kompatibilität**: Elementor 3.0+ und WordPress 5.0+

## 🧪 Testing & Debugging

### Validierung testen

```bash
# XML-Struktur validieren
python3 -c "import xml.etree.ElementTree as ET; ET.parse('generated/my-site.xml')"

# JSON-Debug-Output prüfen  
cat generated/my-site.json | python3 -m json.tool
```

### Häufige Probleme

1. **Leere Elementor-Seite**: Verwende `section_based_processor.py` statt Container-basierte Versionen
2. **Import schlägt fehl**: "Import author" aktivieren in WordPress
3. **Widgets nicht sichtbar**: Font Awesome Icons korrekt verwenden (`fas fa-icon-name`)

## 🚀 Deployment

### Production Settings

```python
# Empfohlene Einstellungen für Produktion
PRODUCTION_CONFIG = {
    'validate_inputs': True,
    'compress_output': True, 
    'backup_existing': True,
    'error_handling': 'strict'
}
```

### Batch-Verarbeitung

```bash
#!/bin/bash
# Mehrere YAML-Dateien verarbeiten
for yaml_file in configs/*.yaml; do
    echo "Processing $yaml_file"
    python3 section_based_processor.py "$yaml_file"
done
```

## 🤝 Contributing

1. Fork das Repository
2. Feature-Branch erstellen: `git checkout -b feature/neue-funktion`  
3. Änderungen committen: `git commit -m 'Neue Funktion hinzufügen'`
4. Branch pushen: `git push origin feature/neue-funktion`
5. Pull Request erstellen

## 📄 Lizenz

MIT License - Freie kommerzielle und private Nutzung.

## 🆘 Support

Bei Problemen oder Fragen:

1. **Dokumentation**: Diese README und `/docs/` durchlesen
2. **Debug-Modus**: JSON-Output in `/generated/` prüfen
3. **Issues**: GitHub Issues für Bug-Reports und Feature-Requests
4. **WordPress-Logs**: Debug-Logs für Import-Probleme prüfen

---

**Erstellt mit SWARM-Orchestrierung für maximale Effizienz** 🚀