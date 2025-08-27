# RIMAN WordPress Content Transformation Swarm Prompt

## Mission Critical
Transform the Cholot retirement theme WordPress XML to RIMAN GmbH environmental remediation content while **PRESERVING 100% of the structural integrity**. CEO Jürgen Fischer loves the Cholot theme design - only replace text content, NEVER change structural elements.

## Background Context
- **Current State**: WordPress site with Cholot theme (retirement community design)
- **Target State**: Same Cholot theme structure with RIMAN environmental remediation content
- **CEO Requirements**: Keep exact design, replace ALL text content with RIMAN services
- **Company**: RIMAN GmbH - Professional hazardous material remediation since 1998
- **Mission**: "sicher bauen und gesund leben" (safe building and healthy living)

## Available Resources

### 1. Live Reference Site
- **Original Cholot Theme**: http://localhost:8080/
- View the working theme structure and design that CEO loves
- Study the exact layout and content areas to preserve

### 2. Original XML Structure
- File: `demo-data-fixed.xml` (Cholot theme original)
- Structure: WordPress WXR format with Elementor page builder data
- Critical: ALL widget names must remain as "cholot-*" (NOT "riman-*")
- Preserve: All CDATA sections, JSON structures, widget configurations

### 2. RIMAN Content (from riman-content-structure.json)
**Company Info:**
- Name: RIMAN GmbH - Gesellschaft für Sicherheitsmanagement
- CEO: Jürgen Fischer
- Founded: 1998
- Address: Hochplattenstr. 6, 83109 Großkarolinenfeld
- Phone: 08031-408 43 44
- Email: j.fischer@riman.de
- Website: www.riman.de

**6 Main Services to Replace Retirement Content:**
1. **Rückbaumanagement** - Professional demolition management
2. **Altlastensanierung** - Contaminated site remediation  
3. **Schadstoff-Management** - Hazardous material management
4. **Sicherheitskoordination** - Safety coordination (EU law)
5. **Baubiologische Beratung** - Building biology consulting
6. **Mediation & Konfliktmanagement** - Project mediation

### 3. Image Resources (SEO-optimized German names)
Available at: http://localhost:8082/
- schadstoffsanierung-industrieanlage-riman-gmbh.jpg
- rueckbaumanagement-abriss-professionell.jpg
- altlastensanierung-bodenaushub-fachgerecht.jpg
- sicherheitskoordination-baustelle-riman.jpg
- gefahrstoff-management-asbest-sanierung.jpg
- baubiologische-beratung-gesundes-bauen.jpg
(24 total images with German SEO slugs)

## Transformation Rules

### MUST PRESERVE:
1. All XML tag structures
2. All Elementor widget names (keep "cholot-*")
3. All widget IDs and references
4. All JSON-encoded structures
5. Post IDs and relationships
6. CDATA section formatting

### MUST REPLACE:
1. **Hero Slider Content:**
   - "Discover the best retirement..." → RIMAN professional services
   - "for best and worst" → "Sicherheit seit 1998"
   - Retirement imagery → Industrial/safety imagery

2. **Service Boxes:**
   - "Healthly life" → "Schadstoffsanierung"
   - "Improving life" → "Rückbaumanagement"
   - "Relationship" → "Altlastensanierung"
   - "Exciting" → "Professionell"

3. **Testimonials:**
   - Senior resident stories → Project manager testimonials
   - "Irgan Rogan" → "Johann Müller, Projektleiter"
   - Retirement community reviews → Project success stories

4. **Contact Information:**
   - Address → Hochplattenstr. 6, 83109 Großkarolinenfeld
   - Phone → 08031-408 43 44
   - Email → j.fischer@riman.de

5. **About Section:**
   - Building relationships → Safety and environmental protection
   - Heart-focused care → Technical expertise since 1998

### Content Mapping Strategy:
- Map retirement "care" concepts → "safety" concepts
- Map "community" → "project management"
- Map "wellness" → "environmental protection"
- Map "lifestyle" → "professional services"
- Keep all emotional appeal but redirect to business trust

## Success Criteria:
1. ✅ XML imports without errors
2. ✅ Cholot theme design remains intact
3. ✅ All RIMAN services visible
4. ✅ Professional German content
5. ✅ Contact info updated
6. ✅ Images properly referenced
7. ✅ No broken Elementor widgets

## Command to Execute:
```bash
npx claude-flow@alpha swarm "Transform Cholot WordPress XML from retirement to RIMAN environmental remediation content while preserving 100% structural integrity. Read demo-data-fixed.xml and riman-content-structure.json. Replace ONLY text content, never structural elements. Keep all cholot widget names. Output: riman-transformed-final.xml" \
  --strategy content-transformation \
  --neural-patterns enabled \
  --memory-compression high \
  --agents 4
```

## Important Notes:
- CEO loves the Cholot design - DO NOT change structure
- Previous attempts failed because structure was modified
- Widget names must stay as "cholot-*" for theme compatibility
- All content must be professional German business language
- Focus on safety, expertise, and 25+ years experience