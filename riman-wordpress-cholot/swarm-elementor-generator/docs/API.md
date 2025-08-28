# API-Dokumentation

## SectionBasedProcessor Klasse

Die `SectionBasedProcessor` Klasse ist das Herzstück des SWARM Elementor Generator Systems.

### Hauptmethoden

#### `process_yaml_to_elementor(yaml_path: str) -> tuple[Dict, List]`

Konvertiert eine YAML-Konfigurationsdatei zu Elementor-JSON-Struktur.

**Parameter:**
- `yaml_path` (str): Pfad zur YAML-Konfigurationsdatei

**Rückgabe:**
- `tuple[Dict, List]`: (config, elementor_data)
  - `config`: Geparste YAML-Konfiguration
  - `elementor_data`: Liste von Elementor-Sections

**Beispiel:**
```python
processor = SectionBasedProcessor()
config, elementor_data = processor.process_yaml_to_elementor('my-site.yaml')
```

#### `generate_wordpress_xml(config: Dict, elementor_data: List, output_path: str) -> str`

Generiert eine WordPress XML-Datei aus der Elementor-Struktur.

**Parameter:**
- `config` (Dict): Geparste YAML-Konfiguration
- `elementor_data` (List): Liste von Elementor-Sections
- `output_path` (str): Pfad für die Ausgabedatei

**Rückgabe:**
- `str`: Pfad zur generierten XML-Datei

**Beispiel:**
```python
output_path = processor.generate_wordpress_xml(
    config, 
    elementor_data, 
    'generated/my-site.xml'
)
```

#### `generate_unique_id() -> str`

Generiert eine eindeutige ID für Elementor-Elemente.

**Rückgabe:**
- `str`: 7-stellige hexadezimale ID

### Section-Ersteller-Methoden

#### `_create_hero_section(config: Dict) -> Dict`

Erstellt eine Hero-Section mit Vollbild-Hintergrund.

**Parameter:**
- `config['slides']`: Liste von Slides mit title, text, button_text, button_link, image

**Struktur:**
```python
{
    "type": "hero_slider",
    "slides": [{
        "title": "Haupttitel",
        "subtitle": "Untertitel", 
        "text": "Beschreibungstext",
        "button_text": "Button Text",
        "button_link": "#anchor",
        "image": "https://example.com/hero.jpg"
    }]
}
```

#### `_create_services_section(config: Dict) -> List[Dict]`

Erstellt Service-Karten-Section (2 Sections: Titel + Content).

**Parameter:**
- `config['title']`: Section-Titel
- `config['subtitle']`: Section-Untertitel  
- `config['services']`: Liste von Services

**Struktur:**
```python
{
    "type": "service_cards",
    "title": "Unsere Leistungen",
    "subtitle": "Professionell",
    "services": [{
        "title": "Service Name",
        "subtitle": "Kategorie",
        "text": "Beschreibung",
        "icon": "fas fa-check",
        "image": "https://example.com/service.jpg"
    }]
}
```

#### `_create_team_section(config: Dict) -> List[Dict]`

Erstellt Team-Section (2 Sections: Titel + Mitglieder).

**Parameter:**
- `config['title']`: Section-Titel
- `config['members']`: Liste von Team-Mitgliedern (max. 3)

**Struktur:**
```python
{
    "type": "team",
    "title": "Unser Team", 
    "members": [{
        "name": "Max Mustermann",
        "position": "Position",
        "image": "https://example.com/team.jpg",
        "bio": "Kurzbeschreibung"
    }]
}
```

#### `_create_testimonials_section(config: Dict) -> List[Dict]`

Erstellt Testimonials-Section (2 Sections: Titel + Testimonials).

**Parameter:**
- `config['title']`: Section-Titel
- `config['testimonials']`: Liste von Kundenstimmen (max. 3)

**Struktur:**
```python
{
    "type": "testimonials",
    "title": "Kundenstimmen",
    "testimonials": [{
        "name": "Kundenname",
        "position": "Position/Firma",
        "text": "Testimonial-Text",
        "image": "https://example.com/customer.jpg",
        "rating": 5
    }]
}
```

#### `_create_about_section(config: Dict) -> Dict`

Erstellt About-Section mit Text und Bild.

**Parameter:**
- `config['title']`: Section-Titel
- `config['content']`: Textinhalt
- `config['image']`: Bild-URL

#### `_create_services_grid_section(config: Dict) -> List[Dict]`

Erstellt Services-Grid-Section (2 Sections: Titel + Grid).

**Parameter:**
- `config['title']`: Section-Titel
- `config['services']`: Liste von Services mit icon und title

#### `_create_contact_section(config: Dict) -> List[Dict]`

Erstellt Contact-Section (2 Sections: Titel + Kontaktdaten).

**Parameter:**
- `config['title']`: Section-Titel
- `config['text']`: Einleitungstext
- `config['info']`: Liste von Kontaktdaten
- `config['background_color']`: Hintergrundfarbe (optional)

## Elementor-Struktur

### Section-Objekt

```python
{
    "id": "abc1234",           # Eindeutige ID
    "elType": "section",       # Elementor-Typ
    "settings": {              # Section-Einstellungen
        "layout": "boxed",
        "content_width": {"unit": "px", "size": 1140},
        "margin": {"unit": "px", "top": 80, "bottom": 80}
    },
    "elements": [...]          # Liste von Columns
}
```

### Column-Objekt

```python
{
    "id": "def5678",           # Eindeutige ID
    "elType": "column",        # Elementor-Typ
    "settings": {              # Column-Einstellungen
        "_column_size": 50     # Breite in Prozent
    },
    "elements": [...]          # Liste von Widgets
}
```

### Widget-Objekt

```python
{
    "id": "ghi9012",           # Eindeutige ID
    "elType": "widget",        # Elementor-Typ
    "widgetType": "heading",   # Widget-Typ
    "settings": {              # Widget-Einstellungen
        "title": "Titel",
        "size": "xl",
        "align": "center"
    }
}
```

## Häufige Widget-Typen

### Heading Widget
```python
"settings": {
    "title": "Titel-Text",
    "size": "xl",                    # xxl, xl, large, medium, small
    "align": "center",               # left, center, right
    "title_color": "#232323",
    "typography_typography": "custom",
    "typography_font_size": {"unit": "px", "size": 42}
}
```

### Text Editor Widget
```python
"settings": {
    "editor": "<p>HTML-Inhalt</p>",
    "text_color": "#666666"
}
```

### Icon Box Widget
```python
"settings": {
    "selected_icon": {
        "value": "fas fa-shield-alt",
        "library": "fa-solid"
    },
    "title_text": "Titel",
    "description_text": "Beschreibung",
    "icon_primary_color": "#b68c2f"
}
```

### Image Widget
```python
"settings": {
    "image": {"url": "https://example.com/image.jpg"},
    "image_size": "large",
    "border_radius": {"unit": "px", "size": 8}
}
```

### Button Widget
```python
"settings": {
    "text": "Button Text",
    "link": {"url": "https://example.com"},
    "align": "center",
    "size": "lg",
    "button_background_color": "#b68c2f"
}
```

## WordPress XML-Struktur

### Namespace-Registrierung
```python
ET.register_namespace('wp', 'http://wordpress.org/export/1.2/')
ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
```

### Wichtige Metafelder
- `_elementor_data`: JSON-String mit Elementor-Struktur
- `_elementor_edit_mode`: "builder"
- `_elementor_template_type`: "wp-page"
- `_wp_page_template`: Template-Name (z.B. "elementor_canvas")

## Error Handling

### Häufige Fehler

1. **Ungültige YAML-Syntax**
   ```python
   try:
       config = yaml.safe_load(f)
   except yaml.YAMLError as e:
       print(f"YAML-Fehler: {e}")
   ```

2. **Fehlende Required-Felder**
   ```python
   if not config.get('pages'):
       raise ValueError("Keine Seiten in Konfiguration gefunden")
   ```

3. **XML-Generierung-Fehler**
   ```python
   try:
       xml_string = ET.tostring(rss, encoding='unicode')
   except Exception as e:
       print(f"XML-Fehler: {e}")
   ```

## Debugging

### JSON-Debug-Output
```python
with open('debug.json', 'w') as f:
    json.dump({'content': elementor_data}, f, indent=2)
```

### Widget-Zählung
```python
def count_widgets(data, count=0):
    if isinstance(data, dict):
        if 'widgetType' in data:
            count += 1
        for v in data.values():
            count = count_widgets(v, count)
    return count

widget_count = count_widgets(elementor_data)
```

## Performance-Optimierung

### Efficient ID-Generierung
```python
import uuid
def generate_unique_id():
    return uuid.uuid4().hex[:7]
```

### JSON-Komprimierung
```python
clean_json = json.dumps(elementor_data, separators=(',', ':'))
```