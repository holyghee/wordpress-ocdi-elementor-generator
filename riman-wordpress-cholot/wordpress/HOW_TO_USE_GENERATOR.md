# WordPress XML Generator - Benutzerhandbuch

## So fütterst du den Generator mit Content

Der Generator unterstützt 3 Eingabeformate: **YAML**, **JSON** und **Markdown**

### 1. YAML Format (riman-homepage.yaml)
```yaml
title: RIMAN GmbH - Startseite
slug: home
components:
  - type: cholot_slider
    slides:
      - title: "Willkommen bei RIMAN"
        image: "http://localhost:8082/bild.jpg"
```

### 2. JSON Format (riman-services.json)
```json
{
  "title": "RIMAN Services",
  "slug": "dienstleistungen",
  "components": [
    {
      "type": "cholot_title_text",
      "title": "Unsere Services"
    }
  ]
}
```

### 3. Markdown Format (riman-about.md)
```markdown
---
title: Über RIMAN
slug: ueber-uns
---

# Über uns

::cholot_counter_row[columns=4]
:::cholot_counter
count: 25
title: Jahre Erfahrung
:::
::
```

## Generator ausführen

```bash
# YAML zu XML konvertieren
python3 generate_wordpress_xml.py -i riman-homepage.yaml -o output.xml

# JSON zu XML konvertieren  
python3 generate_wordpress_xml.py -i riman-services.json -o output.xml

# Markdown zu XML konvertieren
python3 generate_wordpress_xml.py -i riman-about.md -o output.xml
```

## Verfügbare Cholot Widgets

Der Generator unterstützt alle 13 Cholot Theme Widgets:

1. **cholot_slider** - Hero Slider mit Bildern
2. **cholot_title_text** - Titel mit Text
3. **cholot_texticon_row** - Icon-Boxen in Spalten
4. **cholot_servicepostitem_row** - Service-Karten
5. **cholot_teampostitem_row** - Team-Mitglieder
6. **cholot_counter_row** - Zähler/Statistiken
7. **cholot_testimonial** - Kundenstimmen
8. **cholot_processbox_row** - Prozess-Schritte
9. **cholot_cta** - Call-to-Action Button
10. **cholot_button_text** - Button mit Text
11. **cholot_contact_form** - Kontaktformular
12. **cholot_portfolio** - Portfolio-Galerie
13. **cholot_blog_posts** - Blog-Beiträge

## Beispiel: Komplette Seite erstellen

1. Erstelle eine Datei `meine-seite.yaml`:
```yaml
title: RIMAN Komplettservice
slug: komplettservice
components:
  # Hero Section
  - type: cholot_slider
    slides:
      - title: "Professionelle Sanierung"
        text: "Seit 1998 Ihr Partner"
        image: "http://localhost:8082/hero.jpg"
        button_text: "Kontakt"
        button_link: "/kontakt"
  
  # 3 Service Boxen
  - type: cholot_texticon_row
    columns: 3
    items:
      - title: "Asbestsanierung"
        icon: "fas fa-shield-alt"
        text: "Fachgerecht und sicher"
      - title: "PCB-Sanierung"  
        icon: "fas fa-building"
        text: "Nach aktuellen Standards"
      - title: "Schimmelpilz"
        icon: "fas fa-recycle"
        text: "Nachhaltige Beseitigung"
```

2. Konvertiere zu XML:
```bash
python3 generate_wordpress_xml.py -i meine-seite.yaml -o meine-seite.xml
```

3. Importiere in WordPress:
   - WordPress Admin → Werkzeuge → Importieren
   - WordPress auswählen → XML-Datei hochladen
   - Importieren klicken

## Bilder verwenden

Alle Bilder müssen auf dem lokalen Server (Port 8082) verfügbar sein:
```yaml
image: "http://localhost:8082/mein-bild.jpg"
```

Die generierten Bilder liegen im Ordner:
`/projects/riman-wordpress/riman-wordpress-cholot/wordpress/generated_images/`

## Tipps

- **YAML** ist am einfachsten für strukturierte Inhalte
- **JSON** eignet sich für programmgesteuerte Generierung
- **Markdown** ist ideal für textlastige Inhalte mit eingebetteten Widgets
- Nutze `cholot_widgets_catalog.json` als Referenz für alle Widget-Parameter