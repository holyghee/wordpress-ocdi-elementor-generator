# Template Library System - Die praktische Lösung

## Das Problem
- Elementor JSON ist zu komplex (400+ Style-Parameter)
- KI kann das nicht sinnvoll generieren
- Nutzer wollen nur Inhalte ändern, nicht Design

## Die Lösung: Template Library + Content Injection

### 1. Template Library aufbauen
```
templates/
  ├── hero-sections/
  │   ├── hero-slider.json         # Vom Cholot Home
  │   ├── hero-simple.json         # Vom About Page
  │   └── hero-video.json          # Custom
  │
  ├── service-sections/
  │   ├── service-3-boxes.json     # Cholot Style
  │   ├── service-grid.json        # Modern
  │   └── service-list.json        # Minimal
  │
  ├── complete-pages/
  │   ├── business-landing.json    # Fertige Business-Page
  │   ├── service-company.json     # Für Dienstleister
  │   └── portfolio.json           # Für Kreative
```

### 2. Einfaches Content-Format
```yaml
# Das schreibt der Nutzer
page: "RIMAN Startseite"
template: "business-landing"

content:
  company: "RIMAN GmbH"
  tagline: "Professionelle Schadstoffsanierung seit 1998"
  
  services:
    - "Asbestsanierung"
    - "PCB-Entsorgung" 
    - "Schimmelsanierung"
    
  contact:
    email: "info@riman.de"
    phone: "+49 123 456789"
```

### 3. Smart Mapping
```python
# System mapped automatisch
"Asbestsanierung" → {
    "icon": "fa-shield",  # Intelligent guess
    "color": "#e74c3c",   # Danger color for hazmat
    "description": auto_generate("Asbestsanierung")  # AI generiert Text
}
```

## Implementierungs-Schritte

### Phase 1: Template Extraction (1 Tag)
- [ ] Cholot Templates in Komponenten zerlegen
- [ ] Jede Section als wiederverwendbares Template speichern
- [ ] Variablen-Platzhalter definieren

### Phase 2: Content Mapper (2 Tage)
- [ ] Simple YAML → Template Variable Mapping
- [ ] Intelligente Defaults (Icons, Farben)
- [ ] Content-Validierung

### Phase 3: Builder Interface (3 Tage)
```python
builder = PageBuilder()
builder.add_section("hero", template="cholot-slider", content={...})
builder.add_section("services", template="3-columns", content={...})
builder.generate()  # → WordPress XML
```

### Phase 4: AI Integration (Optional)
```python
# Natural Language → Simple YAML
ai_prompt = "Sanierungsfirma Website mit Hero und 3 Services"
yaml_content = ai.generate_yaml(ai_prompt)
xml = builder.from_yaml(yaml_content).generate()
```

## Vorteile

✅ **Für Nutzer:**
- Nur Content schreiben, kein Design-Stress
- Professionelle Ergebnisse garantiert
- 10x schneller als Elementor

✅ **Für Entwickler:**
- Wiederverwendbare Komponenten
- Versionierbar in Git
- Testbar und wartbar

✅ **Für Business:**
- Skalierbar für viele Kunden
- Template-Marktplatz möglich
- SaaS-Potential

## Beispiel-Workflow

```bash
# 1. User schreibt simple Datei
nano riman-content.yaml

# 2. Generator macht Magic
python generate.py --template="business" --content="riman-content.yaml"

# 3. Fertige Website!
→ Output: riman-website.xml (import-ready)
```

## Nächste Schritte

1. **Proof of Concept**: Eine Section (z.B. Hero) voll durchimplementieren
2. **Template Library**: 5-10 Standard-Sections extrahieren
3. **CLI Tool**: Einfaches Command-Line Interface
4. **Web Interface**: Simple Upload-Form
5. **AI Integration**: OpenAI API für Content-Generation