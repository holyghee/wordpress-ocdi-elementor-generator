# RIMAN WordPress Import - Funktionierende Basis

## ✅ Aktuelle funktionierende Version
- **Page ID**: 3046 
- **URL**: http://localhost:8081/?page_id=3046
- **Status**: Hero Slider funktioniert, Service Cards teilweise (Platzhalter-Problem)

## 🚀 Ausführung

### Empfohlene Methode: PHP Direct Import
```bash
php robust_import.php
```
Erstellt neue Seite direkt in WordPress-Datenbank.

### Alternative: Python XML-Generator
```bash
# 1. XML generieren
python3 elementor_fixed_processor.py riman-cholot-intelligent.yaml

# 2. XML importieren  
php test-direct-ocdi.php elementor-fixed-output.xml

# 3. CSS regenerieren
php regenerate_elementor_css.php
```

## 📁 Wichtige Dateien

### Core-Dateien
- `block_library/` - 16 JSON-Templates aus Cholot extrahiert
- `riman-cholot-intelligent.yaml` - YAML-Config mit RIMAN-Inhalten
- `robust_import.php` - Funktionierender PHP Direct Import
- `elementor_fixed_processor.py` - Python XML-Generator mit Image-Fix

### Block Templates (in block_library/)
- `hero-slider_9.json` - ✅ Funktioniert
- `service-cards_2.json` - ⚠️ Teilweise (Platzhalter-Problem)
- `title-section_1.json` - ✅ Funktioniert
- `team-section_12.json` - 📦 Vorhanden
- `testimonials_5.json` - 📦 Vorhanden
- `contact-form_7.json` - 📦 Vorhanden

## 🔧 Bekannte Probleme

1. **Service Cards Platzhalter**: Zeigen noch `{{SERVICE_TITLE}}` und `{{SERVICE_TEXT}}`
2. **JSON-Encoding**: Beim XML-Import wird JSON oft beschädigt
3. **Custom Widgets**: `rdn-slider` und `cholot-texticon` brauchen Cholot-Theme

## 💡 Lösungsansätze

### Für Service Cards Problem:
```php
// In robust_import.php alle Platzhalter ersetzen:
$replacements = [
    'SERVICE_0_TITLE' => 'Asbestsanierung',
    'SERVICE_TITLE' => 'Asbestsanierung', // Fallback
    // etc.
];
```

### Für JSON-Problem:
- PHP Direct Import verwenden (umgeht XML)
- Oder: JSON vor Speichern validieren

## 📊 Workflow-Übersicht

```
1. YAML-Config → 2. Load Templates → 3. Replace Placeholders → 4. Save to DB
                      ↑
                 block_library/
```

## 🎯 Nächste Schritte

1. Service Cards Platzhalter komplett fixen
2. Alle 6 Sections implementieren (Team, Testimonials, Contact)
3. Bilder lokal sicherstellen
4. Elementor CSS automatisch regenerieren

## 🔗 Zusammenhänge

- **Original Cholot Import**: Page ID 103-106 (funktioniert perfekt)
- **RIMAN Tests**: Page ID 2000-2003, 3046-3048
- **Working XML**: `CHOLOT-WORKING-FINAL.xml` (30KB)

---
Stand: 30.08.2025