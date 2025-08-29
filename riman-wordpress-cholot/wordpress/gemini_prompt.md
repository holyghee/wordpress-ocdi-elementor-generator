# Aufgabe: Elementor Design-Block Analyse und Extraktion

## Kontext
Ich entwickle einen WordPress Elementor Generator, der aus einfachen YAML-Konfigurationen komplexe Websites erstellen kann. Dafür benötige ich eine detaillierte Analyse der Design-Blocks aus dem Cholot Theme.

## Deine Aufgabe
Analysiere die beigefügten Dateien und extrahiere wiederverwendbare Design-Block-Patterns, die als modulare Bausteine in unserem Generator verwendet werden können.

## Beigefügte Dateien
1. `demo-data-fixed.xml` - Cholot Theme Demo-Daten Export (WordPress XML Format)
2. JSON-Dateien aus `cholot_theme_library/`:
   - `hero_slider.json`
   - `service_card_with_shape.json`
   - `icon_box.json`
   - `three_column.json`
   - `single_column.json`
   - `contact_form.json`
   - `testimonials.json`
   - weitere Block-Typen...

## Analyse-Anforderungen

### 1. Block-Pattern Identifikation
Identifiziere für jeden gefundenen Block-Typ:
- **Struktureller Aufbau**: Wie sind die Elementor-Elemente verschachtelt (section → column → widget)?
- **Visuelle Merkmale**: Shape Dividers, Animationen, Hintergrundbilder, etc.
- **Widget-Typen**: Welche spezifischen Widgets werden verwendet (cholot-texticon, rdn-slider, etc.)?
- **Responsive Settings**: Wie verhalten sich die Blocks auf verschiedenen Bildschirmgrößen?

### 2. Erstelle Block-Templates
Für jeden identifizierten Block-Typ erstelle ein generisches Template im folgenden Format:

```json
{
  "block_name": "service_card_curved",
  "description": "Service Card mit Bild, curved shape divider und Text-Icon Widget",
  "category": "content",
  "dependencies": ["cholot-texticon", "shape-dividers"],
  "structure": {
    "type": "column",
    "settings": {
      "_column_size": 33,
      "animation": "fadeInUp"
    },
    "elements": [
      {
        "type": "section",
        "isInner": true,
        "purpose": "image_container",
        "settings": {
          "shape_divider_bottom": "curve",
          "shape_divider_bottom_negative": "yes"
        }
      },
      {
        "type": "section", 
        "isInner": true,
        "purpose": "content_container",
        "widgets": ["cholot-texticon"]
      }
    ]
  },
  "configurable_fields": [
    "image_url",
    "title",
    "subtitle",
    "description",
    "icon",
    "animation_delay"
  ]
}
```

### 3. Design-System Extraktion
Identifiziere das übergreifende Design-System:
- **Farben**: Primary (#b68c2f), Secondary, Text-Farben
- **Typografie**: Schriftarten, Größen, Gewichtungen
- **Spacing**: Padding/Margin-Patterns
- **Animationen**: Verwendete Animation-Types und Delays
- **Container-Breiten**: Standard-Breiten (1140px, etc.)

### 4. Widget-Mapping
Erstelle eine Mapping-Tabelle für Cholot-spezifische Widgets:

```json
{
  "cholot_widgets": {
    "cholot-texticon": {
      "standard_equivalent": "icon-box",
      "unique_features": ["subtitle field", "custom icon styling"],
      "required_settings": ["selected_icon", "title", "subtitle", "text"]
    },
    "rdn-slider": {
      "standard_equivalent": "slides",
      "unique_features": ["video background support", "multiple buttons"],
      "required_settings": ["slider_items"]
    }
  }
}
```

### 5. Generator-Regeln
Definiere Regeln für unseren Generator:
- Wann soll welcher Block-Typ verwendet werden?
- Wie können Blocks kombiniert werden?
- Welche Blocks sind für bestimmte Seitentypen essentiell?

### 6. YAML Config Schema
Schlage ein optimales YAML-Schema vor, das alle identifizierten Patterns abdeckt:

```yaml
pages:
  - name: "Homepage"
    sections:
      - type: "hero_slider"
        config:
          slides:
            - title: "..."
              background: "..."
      
      - type: "service_cards"
        config:
          layout: "3_columns_curved"
          cards:
            - title: "..."
              image: "..."
```

## Erwartete Ausgabe
1. **Block-Bibliothek**: JSON mit allen extrahierten Block-Templates
2. **Widget-Dokumentation**: Übersicht aller Cholot-spezifischen Widgets
3. **Design-System**: Extrahierte Design-Tokens (Farben, Fonts, etc.)
4. **Generator-Logik**: Pseudo-Code oder Flowchart für die Generierung
5. **YAML-Schema**: Optimales Schema für Endnutzer-Konfiguration

## Ziel
Das Endergebnis soll es ermöglichen, aus einer einfachen YAML-Datei eine komplette Website zu generieren, die das volle Design-Potential des Cholot Themes nutzt, aber mit individuellen Inhalten gefüllt werden kann.

## Beispiel Use-Case
Ein Nutzer soll in der Lage sein, eine YAML-Datei zu schreiben:
```yaml
company: "RIMAN GmbH"
services:
  - name: "Asbestsanierung"
    icon: "shield"
    image: "asbestos.jpg"
```

Und daraus soll automatisch eine vollständige Elementor-Seite mit allen Cholot Design-Elementen generiert werden.

## Technische Details
- Elementor Version: 3.18.3
- WordPress Version: 6.x
- Theme: Cholot
- Custom Widgets: cholot-texticon, rdn-slider, testimonial-carousel, cholot-contact-shortcode

Bitte analysiere die Dateien gründlich und erstelle eine strukturierte Dokumentation, die als Grundlage für unseren Generator dienen kann.