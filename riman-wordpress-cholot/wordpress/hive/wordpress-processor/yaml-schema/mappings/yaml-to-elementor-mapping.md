# YAML to Elementor JSON Mapping Documentation

This document explains how to convert the Cholot theme YAML configuration into Elementor JSON format that WordPress can import.

## Overview

The YAML schema provides a human-readable way to configure the Cholot theme, while Elementor uses JSON for its internal structure. This mapping shows how each YAML section translates to Elementor JSON.

## Core Structure Mapping

### 1. Pages → Elementor Pages

**YAML Structure:**
```yaml
pages:
  - id: "home"
    title: "Home"
    slug: ""
    template: "default"
    sections: []
```

**Elementor JSON Structure:**
```json
{
  "post_title": "Home",
  "post_name": "",
  "post_type": "page",
  "meta_input": {
    "_elementor_data": "[...]",
    "_elementor_edit_mode": "builder",
    "_elementor_template_type": "wp-page"
  }
}
```

### 2. Sections → Elementor Sections

**YAML Structure:**
```yaml
sections:
  - type: "content"
    id: "main_content"
    settings:
      background:
        type: "classic"
        color: "#f4f4f4"
      padding: {top: "60px", right: "0", bottom: "60px", left: "0"}
      structure: "40"
    columns: []
```

**Elementor JSON Structure:**
```json
{
  "id": "main_content",
  "elType": "section",
  "settings": {
    "gap": "extended",
    "background_background": "classic",
    "background_color": "#f4f4f4",
    "padding": {
      "unit": "px",
      "top": "60",
      "right": "0",
      "bottom": "60",
      "left": "0",
      "isLinked": false
    },
    "structure": "40"
  },
  "elements": []
}
```

### 3. Columns → Elementor Columns

**YAML Structure:**
```yaml
columns:
  - size: 25
    responsive: {tablet: 50, mobile: 100}
    widgets: []
```

**Elementor JSON Structure:**
```json
{
  "id": "generated_id",
  "elType": "column",
  "settings": {
    "_column_size": 25,
    "_inline_size_tablet": 50,
    "_inline_size_mobile": 100
  },
  "elements": []
}
```

## Widget Mapping

### Cholot TextIcon Widget

**YAML Structure:**
```yaml
widgets:
  - type: "cholot-texticon"
    id: "service_card"
    settings:
      title: "Cholot"
      subtitle: ""
      text: "<p>Retirement Community</p>"
      icon: "fas fa-crown"
      title_color: "#ffffff"
      subtitle_color: "#b68c2f"
      text_color: "#b68c2f"
      icon_color: "#b68c2f"
      icon_size: 15
```

**Elementor JSON Structure:**
```json
{
  "id": "service_card",
  "elType": "widget",
  "settings": {
    "title": "Cholot",
    "subtitle": "",
    "text": "<p>Retirement Community</p>",
    "selected_icon": {"value": "fas fa-crown", "library": "fa-solid"},
    "title_color": "#ffffff",
    "subtitle_color": "#b68c2f",
    "text_color": "#b68c2f",
    "icon_size": {"unit": "px", "size": 15, "sizes": []},
    "title_typography_typography": "custom",
    "title_typography_font_size": {"unit": "px", "size": 24, "sizes": []},
    "__fa4_migrated": {"selected_icon": true}
  },
  "elements": [],
  "widgetType": "cholot-texticon"
}
```

### Cholot Menu Widget

**YAML Structure:**
```yaml
widgets:
  - type: "cholot-menu"
    id: "main_menu"
    settings:
      cholot_menu: "default-menu"
      align: "right"
      styling:
        menu_color: "#ffffff"
        menu_color_hover: "#b68c2f"
      typography:
        font_family: "Source Sans Pro"
        font_weight: 900
```

**Elementor JSON Structure:**
```json
{
  "id": "main_menu",
  "elType": "widget",
  "settings": {
    "cholot_menu": "default-menu",
    "align": "right",
    "menu_color": "#ffffff",
    "menu_color_hover": "#b68c2f",
    "menu_typo_typography": "custom",
    "menu_typo_font_family": "Source Sans Pro",
    "menu_typo_font_weight": "900"
  },
  "elements": [],
  "widgetType": "cholot-menu"
}
```

### Standard Elementor Widgets

#### Text Editor Widget

**YAML Structure:**
```yaml
widgets:
  - type: "text-editor"
    id: "about_content"
    settings:
      editor: "<p>Building with our residents...</p>"
      text_color: "#000000"
      align: "left"
      margins: {top: -15, right: 0, bottom: -30, left: 0}
```

**Elementor JSON Structure:**
```json
{
  "id": "about_content",
  "elType": "widget",
  "settings": {
    "editor": "<p>Building with our residents...</p>",
    "text_color": "#000000",
    "align": "left",
    "_margin": {
      "unit": "px",
      "top": "-15",
      "right": "0",
      "bottom": "-30",
      "left": "0",
      "isLinked": false
    }
  },
  "elements": [],
  "widgetType": "text-editor"
}
```

#### Divider Widget

**YAML Structure:**
```yaml
widgets:
  - type: "divider"
    id: "about_divider"
    settings:
      color: "#b68c2f"
      width: 25
      align: "left"
```

**Elementor JSON Structure:**
```json
{
  "id": "about_divider",
  "elType": "widget",
  "settings": {
    "color": "#b68c2f",
    "width": {"unit": "px", "size": 25, "sizes": []},
    "align": "left"
  },
  "elements": [],
  "widgetType": "divider"
}
```

## Design Token Mapping

### Colors
Design tokens in YAML are applied to individual widget settings in Elementor JSON.

**YAML Design Tokens:**
```yaml
design:
  colors:
    primary: "#b68c2f"
    secondary: "#ffffff"
    background: "#f4f4f4"
```

**Applied in Elementor JSON:**
- `primary` color → `title_color: "#b68c2f"`
- `background` color → `background_color: "#f4f4f4"`
- `secondary` color → `text_color: "#ffffff"`

### Typography
Font settings are converted to Elementor's typography system.

**YAML Typography:**
```yaml
design:
  fonts:
    primary:
      family: "Source Sans Pro"
      weights: [400, 600, 700, 900]
```

**Elementor Typography:**
```json
{
  "title_typography_typography": "custom",
  "title_typography_font_family": "Source Sans Pro",
  "title_typography_font_weight": "900"
}
```

### Spacing
Spacing tokens are converted to padding/margin settings.

**YAML Spacing:**
```yaml
design:
  spacing:
    lg: "30px"
    xl: "60px"
```

**Elementor Spacing:**
```json
{
  "padding": {
    "unit": "px",
    "top": "60",
    "right": "0",
    "bottom": "60",
    "left": "0",
    "isLinked": false
  }
}
```

## Content Management Mapping

### Navigation Menus

**YAML Structure:**
```yaml
navigation:
  menus:
    - id: "default-menu"
      name: "Default Menu"
      items:
        - label: "Home"
          url: "/"
        - label: "About"
          url: "/about/"
```

**WordPress Navigation:**
```php
// Create menu in WordPress
wp_create_nav_menu('Default Menu');

// Add menu items
wp_update_nav_menu_item($menu_id, 0, array(
    'menu-item-title' => 'Home',
    'menu-item-url' => '/',
    'menu-item-status' => 'publish'
));
```

### Media Library

**YAML Structure:**
```yaml
content:
  media:
    images:
      - id: "50"
        url: "https://example.com/image.jpg"
        alt: "Gallery Image 1"
        title: "Gallery Image 1"
```

**WordPress Media:**
```php
// Import image to WordPress Media Library
$attachment_id = wp_insert_attachment(array(
    'post_title' => 'Gallery Image 1',
    'post_content' => '',
    'post_excerpt' => 'Gallery Image 1',
    'post_status' => 'inherit'
), $file_path);
```

## Conversion Process

### 1. YAML Parsing
```javascript
const yaml = require('js-yaml');
const config = yaml.load(fs.readFileSync('site-config.yaml', 'utf8'));
```

### 2. Structure Conversion
```javascript
function convertYamlToElementor(yamlConfig) {
    const elementorData = [];
    
    yamlConfig.pages.forEach(page => {
        const elementorPage = {
            post_title: page.title,
            post_name: page.slug,
            post_type: 'page',
            meta_input: {
                '_elementor_data': JSON.stringify(convertSections(page.sections)),
                '_elementor_edit_mode': 'builder'
            }
        };
        elementorData.push(elementorPage);
    });
    
    return elementorData;
}
```

### 3. Widget Settings Mapping
```javascript
function mapWidgetSettings(yamlWidget) {
    const elementorSettings = {};
    
    switch (yamlWidget.type) {
        case 'cholot-texticon':
            elementorSettings.title = yamlWidget.settings.title;
            elementorSettings.selected_icon = {
                value: yamlWidget.settings.icon,
                library: 'fa-solid'
            };
            elementorSettings.title_color = yamlWidget.settings.title_color;
            break;
        
        case 'text-editor':
            elementorSettings.editor = yamlWidget.settings.editor;
            elementorSettings.text_color = yamlWidget.settings.text_color;
            break;
    }
    
    return elementorSettings;
}
```

## WordPress Import Integration

### 1. Create WordPress XML Export
```javascript
function generateWordPressXML(elementorData) {
    let xml = `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>Cholot Site</title>
    <wp:wxr_version>1.2</wp:wxr_version>
`;

    elementorData.forEach(page => {
        xml += `
    <item>
        <title>${page.post_title}</title>
        <wp:post_type>${page.post_type}</wp:post_type>
        <wp:post_name>${page.post_name}</wp:post_name>
        <wp:postmeta>
            <wp:meta_key>_elementor_data</wp:meta_key>
            <wp:meta_value><![CDATA[${page.meta_input._elementor_data}]]></wp:meta_value>
        </wp:postmeta>
    </item>
`;
    });
    
    xml += `
</channel>
</rss>`;
    
    return xml;
}
```

### 2. PHP Processing Script
```php
<?php
function process_yaml_import($yaml_file) {
    // Parse YAML
    $yaml_data = yaml_parse_file($yaml_file);
    
    // Process design tokens
    update_theme_mods_from_yaml($yaml_data['design']);
    
    // Create navigation menus
    create_menus_from_yaml($yaml_data['navigation']);
    
    // Import media
    import_media_from_yaml($yaml_data['content']['media']);
    
    // Create pages
    create_pages_from_yaml($yaml_data['pages']);
}

function update_theme_mods_from_yaml($design) {
    set_theme_mod('primary_color', $design['colors']['primary']);
    set_theme_mod('secondary_color', $design['colors']['secondary']);
    // ... more theme customizations
}
?>
```

## Advanced Features Mapping

### Animations
**YAML:**
```yaml
advanced_features:
  animations:
    enabled: true
    library: "AOS"
    duration: 800
```

**Elementor:**
```json
{
  "_animation": "fadeInUp",
  "_animation_delay": 800
}
```

### Responsive Settings
**YAML:**
```yaml
responsive: {tablet: 50, mobile: 100}
```

**Elementor:**
```json
{
  "_inline_size_tablet": 50,
  "_inline_size_mobile": 100
}
```

## Validation and Error Handling

### YAML Schema Validation
```javascript
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = {
    type: 'object',
    properties: {
        site: { type: 'object' },
        design: { type: 'object' },
        pages: { type: 'array' }
    },
    required: ['site', 'pages']
};

const validate = ajv.compile(schema);
const valid = validate(yamlData);

if (!valid) {
    console.log(validate.errors);
}
```

### Error Recovery
```javascript
function safeConvert(yamlData) {
    try {
        return convertYamlToElementor(yamlData);
    } catch (error) {
        console.error('Conversion error:', error);
        return generateFallbackStructure();
    }
}
```

## Usage Examples

### Complete Conversion Workflow
```bash
# 1. Validate YAML
node validate-yaml.js site-config.yaml

# 2. Convert to Elementor JSON
node convert-yaml.js site-config.yaml output.json

# 3. Generate WordPress XML
node generate-xml.js output.json export.xml

# 4. Import to WordPress
wp import export.xml
```

### Partial Updates
```javascript
// Update only design tokens
updateDesignTokens(yamlConfig.design);

// Update specific page
updatePage(yamlConfig.pages.find(p => p.id === 'home'));

// Update navigation
updateNavigation(yamlConfig.navigation);
```

This mapping system provides a complete bridge between the human-readable YAML configuration and the WordPress/Elementor ecosystem, enabling powerful theme customization through simple configuration files.