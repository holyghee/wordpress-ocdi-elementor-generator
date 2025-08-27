# Cholot WordPress XML Generator - Complete Guide

A production-ready generator that creates valid WordPress/Elementor XML files from simple input formats, supporting all 13 Cholot widget types with smart defaults and proper XML structure.

## 🚀 Quick Start

```python
from generate_wordpress_xml import WordPressXMLGenerator

# Create generator instance
generator = WordPressXMLGenerator()

# Simple YAML input
yaml_content = """
site:
  title: "My Website"
  description: "A beautiful website"
  base_url: "http://localhost:8082"

pages:
  - title: "Home"
    slug: "home"
    sections:
      - structure: "100"
        columns:
          - width: 100
            widgets:
              - type: "texticon"
                title: "Welcome"
                icon: "fas fa-home"
                text: "Welcome to our website"
"""

# Generate XML
xml_output = generator.generate_xml(yaml_content)

# Save to file
with open('my_site.xml', 'w', encoding='utf-8') as f:
    f.write(xml_output)
```

## 📋 Features

### ✅ **Complete Cholot Theme Support**
- All 13 widget types: texticon, title, post-three, post-four, gallery, logo, menu, button-text, team, testimonial-two, text-line, contact, sidebar
- Exact widget structure preservation
- Theme color scheme integration (#b68c2f)
- Responsive settings support

### ✅ **Multiple Input Formats**
- **YAML**: User-friendly, great for configuration
- **JSON**: Programmatic generation, API integration  
- **Markdown**: Content creators, documentation-style

### ✅ **Smart Defaults**
- Auto-generated unique IDs (Elementor-compatible)
- Theme color scheme applied automatically
- Responsive breakpoint handling
- Typography and spacing defaults

### ✅ **WordPress Compliance**
- Valid WordPress WXR format
- Proper CDATA handling
- Elementor data structure compatibility
- XML validation built-in

## 🏗️ Architecture Overview

```
WordPressXMLGenerator
├── InputFormatParser          # Handles YAML/JSON/Markdown parsing
├── CholotComponentFactory     # Creates all 13 widget types
├── ElementorIDGenerator       # Generates unique IDs
├── CholotThemeConfig         # Theme defaults and colors
└── XML Structure Builder      # Assembles final XML
```

## 🎨 Widget Types Reference

### 1. TextIcon Widget (`cholot-texticon`)

**Purpose**: Display title, subtitle, and text with customizable icon

```yaml
- type: "texticon"
  title: "Our Service"                    # Required
  subtitle: "Professional"               # Optional
  icon: "fas fa-star"                    # Required (FontAwesome)
  text: "Description of our service"     # Optional
  custom_settings:                       # Optional overrides
    title_color: "#ffffff"
    icon_size: { unit: "px", size: 20 }
```

**Common Use Cases**: Service cards, feature highlights, informational sections

### 2. Title Widget (`cholot-title`)

**Purpose**: Display headings with custom styling and span support

```yaml
- type: "title"
  title: "About Us<span>.</span>"        # Required (HTML allowed)
  header_size: "h2"                     # h1, h2, h3, h4, h5, h6
  align: "center"                       # left, center, right
  responsive:                           # Optional
    tablet: "left"
```

**Common Use Cases**: Page headers, section titles, content dividers

### 3. Post Widgets (`cholot-post-three`, `cholot-post-four`)

**Purpose**: Display blog posts in grid layouts

```yaml
- type: "post-three"                    # or "post-four"
  post_count: 4                         # Number of posts
  column: "two"                         # Layout: one, two, three
  categories: ["news", "updates"]       # Filter by categories
  show_excerpt: "yes"                   # Show post excerpts
  button_text: "Read More"              # CTA button text
```

**Common Use Cases**: Blog listings, news sections, article archives

### 4. Gallery Widget (`cholot-gallery`)

**Purpose**: Display image galleries with grid layout

```yaml
- type: "gallery"
  columns: "col-md-4"                   # col-md-3, col-md-4, col-md-6
  height: 250                           # Image height in pixels
  margin: 10                            # Space between images
  images:                               # Array of images
    - "http://localhost:8082/img1.jpg"  # Simple URL string
    - id: 101                           # Or object with ID
      url: "http://localhost:8082/img2.jpg"
  responsive:                           # Optional responsive settings
    tablet:
      height: 200
      margin: 5
```

**Common Use Cases**: Portfolio galleries, photo collections, project showcases

### 5. Logo Widget (`cholot-logo`)

**Purpose**: Display site logo with alignment options

```yaml
- type: "logo"
  url: "http://localhost:8082/logo.png" # Required
  id: 123                               # Optional image ID
  height: "80px"                        # Logo height
  align: "center"                       # left, center, right
```

**Common Use Cases**: Site headers, brand sections, partner logos

### 6. Menu Widget (`cholot-menu`)

**Purpose**: Display WordPress navigation menus

```yaml
- type: "menu"
  menu_name: "main-menu"                # Required WordPress menu slug
  align: "right"                        # left, center, right
  desktop_tablet: "none"                # Desktop display on tablet
  mobile: "none"                        # Mobile menu display
  mobile_tablet: "inline-block"         # Mobile on tablet
```

**Common Use Cases**: Site navigation, header menus, footer menus

### 7. Button Text Widget (`cholot-button-text`)

**Purpose**: Display buttons with text, subtitle, and icon support

```yaml
- type: "button-text"
  text: "Contact Us"                    # Required button text
  url: "http://example.com/contact"     # Required link URL
  external: ""                          # External link flag
  subtitle: "Get in touch today"        # Optional subtitle
  icon: "fas fa-phone"                  # Optional icon
  icon_align: "right"                   # left, right
  custom_settings:                      # Optional styling
    btn_bg: "#b68c2f"
    btn_padding: { unit: "px", top: "15", right: "30" }
```

**Common Use Cases**: Call-to-action buttons, contact links, download buttons

### 8. Team Widget (`cholot-team`)

**Purpose**: Display team member profiles with social links

```yaml
- type: "team"
  name: "John Smith"                    # Required
  position: "CEO"                       # Required
  image_url: "http://localhost:8082/john.jpg" # Required
  image_id: 456                         # Optional
  height: "400px"                       # Card height
  align: "center"                       # left, center, right
  animation: "shrink"                   # Hover animation
  social_links:                         # Optional social media
    - icon: "fab fa-linkedin-in"
      url: "https://linkedin.com/in/johnsmith"
    - icon: "fab fa-twitter" 
      url: "https://twitter.com/johnsmith"
```

**Common Use Cases**: About pages, team sections, staff directories

### 9. Testimonial Widget (`cholot-testimonial-two`)

**Purpose**: Display customer testimonials in slider format

```yaml
- type: "testimonial"
  columns: 3                            # Number of columns
  align: "center"                       # left, center, right
  testimonials:                         # Array of testimonials
    - _id: "test1"                      # Unique identifier
      name: "Jane Doe"
      position: "CEO, Company"
      image:
        url: "http://localhost:8082/jane.jpg"
        id: 789
      testimonial: "Excellent service and support!"
      rating: 5
```

**Common Use Cases**: Customer reviews, client feedback, success stories

### 10. Text Line Widget (`cholot-text-line`)

**Purpose**: Display text with decorative line elements

```yaml
- type: "text-line"
  title: "Our Mission"                  # Required
  subtitle: "What We Do"               # Optional
  line_width: 50                       # Line width in pixels
  line_height: 2                       # Line thickness
  background_color: "#f4f4f4"          # Section background
  background_image: "http://localhost:8082/bg.png" # Optional
  title_size: 28                       # Title font size
  subtitle_size: 14                    # Subtitle font size
```

**Common Use Cases**: Section dividers, content blocks, decorative text

### 11. Contact Widget (`cholot-contact`)

**Purpose**: Display contact forms with custom styling

```yaml
- type: "contact"
  shortcode: '[contact-form-7 id="1" title="Contact form"]' # Required
  button_width: "100%"                  # Button width
  custom_settings:                      # Optional form styling
    btn_bg: "#b68c2f"
    btn_color: "#ffffff"
    form_bg: "rgba(0,0,0,0.1)"
    form_border_color: "#ffffff"
```

**Common Use Cases**: Contact pages, inquiry forms, feedback forms

### 12. Sidebar Widget (`cholot-sidebar`)

**Purpose**: Display sidebar content with custom width

```yaml
- type: "sidebar"
  width: "300px"                        # Required sidebar width
  title_size: 18                        # Title font size
```

**Common Use Cases**: Page sidebars, widget areas, secondary content

## 📐 Layout Structure

### Page Structure
```yaml
pages:
  - title: "Page Title"
    slug: "page-slug"                   # URL slug
    status: "publish"                   # publish, draft, private
    sections: []                        # Array of sections
```

### Section Structure
```yaml
sections:
  - structure: "50"                     # Layout: 100, 50, 33, 25
    settings:                           # Optional section settings
      background:
        background_background: "classic"
        background_color: "#f4f4f4"
        background_image:
          url: "http://localhost:8082/bg.jpg"
          id: 123
    columns: []                         # Array of columns
```

### Column Structure
```yaml
columns:
  - width: 50                           # Column width percentage
    widgets: []                         # Array of widgets
```

## 🎨 Styling & Customization

### Theme Colors
- **Primary**: `#b68c2f` (Cholot golden)
- **White**: `#ffffff`
- **Black**: `#000000`
- **Dark Background**: `#232323`
- **Light Background**: `#f4f4f4`

### Custom Settings Override
Any widget can include `custom_settings` to override defaults:

```yaml
- type: "texticon"
  title: "Custom Styled"
  custom_settings:
    title_typography_font_size:
      unit: "px"
      size: 32
      sizes: []
    title_color: "#ff0000"
    icon_bg_size:
      unit: "px"
      size: 50
      sizes: []
```

### Responsive Settings
Use responsive objects for device-specific styling:

```yaml
responsive:
  tablet:
    height: 200
    margin: 5
  mobile:
    height: 150
    margin: 2
```

## 📁 File Examples

### Simple Business Site (YAML)
```yaml
site:
  title: "Acme Corporation"
  description: "Professional services company"
  base_url: "http://localhost:8082"

pages:
  - title: "Home"
    slug: "home"
    sections:
      # Hero section
      - structure: "100"
        settings:
          background:
            background_color: "#232323"
        columns:
          - width: 100
            widgets:
              - type: "texticon"
                title: "Welcome to Acme Corporation"
                subtitle: "Excellence in Service"
                icon: "fas fa-building"
                text: "Your trusted business partner"

      # Services section  
      - structure: "33"
        columns:
          - width: 33
            widgets:
              - type: "texticon"
                title: "Consulting"
                icon: "fas fa-lightbulb"
                text: "Strategic business consulting"
          - width: 33
            widgets:
              - type: "texticon"
                title: "Implementation"
                icon: "fas fa-cogs"
                text: "Solution implementation"
          - width: 33
            widgets:
              - type: "texticon"
                title: "Support"
                icon: "fas fa-headset"
                text: "24/7 customer support"
```

### Portfolio Site (JSON)
```json
{
  "site": {
    "title": "Creative Studio",
    "description": "Design and development agency"
  },
  "pages": [
    {
      "title": "Portfolio",
      "sections": [
        {
          "structure": "100",
          "columns": [
            {
              "width": 100,
              "widgets": [
                {
                  "type": "gallery",
                  "columns": "col-md-4",
                  "height": 300,
                  "images": [
                    "http://localhost:8082/project1.jpg",
                    "http://localhost:8082/project2.jpg",
                    "http://localhost:8082/project3.jpg"
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## 🧪 Testing & Validation

### Run Test Suite
```bash
python test_generator.py
```

### Manual Testing
```python
from generate_wordpress_xml import WordPressXMLGenerator

generator = WordPressXMLGenerator()

# Test specific widget
test_data = {
    'pages': [{
        'title': 'Test',
        'sections': [{
            'columns': [{
                'widgets': [{
                    'type': 'texticon',
                    'title': 'Test Widget',
                    'icon': 'fas fa-test'
                }]
            }]
        }]
    }]
}

xml_output = generator.generate_xml(test_data)

# Validate XML
import xml.etree.ElementTree as ET
try:
    ET.fromstring(xml_output)
    print("✅ Valid XML generated")
except ET.ParseError as e:
    print(f"❌ XML validation failed: {e}")
```

## 🚀 Production Usage

### Command Line Usage
```bash
# Generate from YAML file
python -c "
from generate_wordpress_xml import WordPressXMLGenerator
import yaml

generator = WordPressXMLGenerator()

with open('my_site.yaml', 'r') as f:
    content = f.read()
    data = yaml.safe_load(content)
    site_config = data.get('site', {})

xml_output = generator.generate_xml(content, site_config)

with open('output.xml', 'w', encoding='utf-8') as f:
    f.write(xml_output)
"
```

### Integration Example
```python
class SiteGenerator:
    def __init__(self):
        self.generator = WordPressXMLGenerator()
    
    def build_from_template(self, template_name, data):
        # Load template
        with open(f'templates/{template_name}.yaml', 'r') as f:
            template = f.read()
        
        # Replace placeholders
        for key, value in data.items():
            template = template.replace(f'{{{key}}}', str(value))
        
        # Generate XML
        return self.generator.generate_xml(template)
    
    def deploy_to_wordpress(self, xml_content):
        # Deploy via WordPress XML import
        pass
```

## 🔧 Troubleshooting

### Common Issues

1. **XML Validation Errors**
   - Check for unescaped HTML in content
   - Ensure all required fields are provided
   - Validate JSON/YAML syntax

2. **Missing Widgets**
   - Verify widget type names are correct
   - Check required fields are provided
   - Review widget configuration structure

3. **Import Issues**
   - Ensure WordPress has Elementor plugin installed
   - Check file encoding (should be UTF-8)
   - Verify image URLs are accessible

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

generator = WordPressXMLGenerator()
xml_output = generator.generate_xml(data)
```

## 📚 Advanced Features

### Custom Widget Factory
```python
from generate_wordpress_xml import CholotComponentFactory

class CustomFactory(CholotComponentFactory):
    def create_custom_widget(self, config):
        # Implement custom widget logic
        return {
            "id": self.id_generator.generate_id(),
            "elType": "widget",
            "widgetType": "custom-widget",
            "settings": config
        }
```

### Batch Processing
```python
def generate_multiple_sites(site_configs):
    generator = WordPressXMLGenerator()
    
    for site_name, config in site_configs.items():
        xml_output = generator.generate_xml(config['data'], config['site'])
        
        with open(f'{site_name}.xml', 'w', encoding='utf-8') as f:
            f.write(xml_output)
```

## 🤝 Contributing

### Adding New Widget Types
1. Add widget method to `CholotComponentFactory`
2. Update `_create_widget_from_data()` in `WordPressXMLGenerator`
3. Add test case to `test_generator.py`
4. Update documentation

### Extending Input Formats
1. Add parser method to `InputFormatParser`
2. Update `auto_detect_and_parse()` method
3. Add format test to test suite

## 📄 License

This generator is designed for use with the Cholot WordPress theme. Ensure you have appropriate licenses for the theme and any dependencies.

---

**Generated by Generator Design Agent** | Production-ready WordPress XML generation for Cholot theme