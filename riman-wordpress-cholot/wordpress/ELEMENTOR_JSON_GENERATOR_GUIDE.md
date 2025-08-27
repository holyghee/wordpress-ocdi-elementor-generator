# Elementor JSON Generator - Complete Implementation Guide

## Overview

This is the working prototype of the Elementor JSON generator using the hybrid approach. It combines rule-based generation with smart defaults to create valid Elementor JSON data structures that match the demo-data-fixed.xml format.

## Key Features

- **Complete Widget Support**: All 13 Cholot widget types implemented
- **Advanced Placeholder System**: Dynamic content injection with context resolution  
- **Smart Layout Optimization**: Automatic section/column structure generation
- **Comprehensive Validation**: JSON structure validation and error handling
- **Flexible Input Formats**: Supports YAML and JSON configuration files
- **Production Ready**: Clean, maintainable code with proper documentation

## Supported Cholot Widgets

1. **cholot-texticon** - Text with icon widgets
2. **cholot-title** - Title/heading widgets with span support
3. **cholot-team** - Team member profiles with social icons
4. **cholot-gallery** - Image galleries with grid layouts
5. **cholot-testimonial-two** - Customer testimonial sliders
6. **cholot-text-line** - Text content with decorative lines
7. **cholot-contact** - Contact form widgets
8. **cholot-button-text** - Buttons with subtitle and icon support
9. **cholot-post-three** - Blog posts in single column
10. **cholot-post-four** - Blog posts in two-column grid
11. **cholot-logo** - Logo/image widgets
12. **cholot-menu** - Navigation menu widgets
13. **cholot-sidebar** - Sidebar content widgets

## File Structure

```
elementor_json_generator.py        # Original implementation
enhanced_elementor_generator.py    # Complete production version  
test_elementor_config.yaml        # Comprehensive test configuration
test_output.json                  # Basic generator output
enhanced_output.json              # Enhanced generator output
```

## Usage

### Command Line Interface

```bash
# Basic usage
python3 enhanced_elementor_generator.py -i config.yaml -o output.json

# Minified output
python3 enhanced_elementor_generator.py -i config.yaml -o output.json --minify
```

### Python API

```python
from enhanced_elementor_generator import CompleteElementorGenerator

generator = CompleteElementorGenerator()
output = generator.generate_from_config('config.yaml', 'output.json')
```

## Configuration Format

### Basic Structure

```yaml
site:
  title: "Site Title"
  description: "Site Description"
  base_url: "http://localhost:8080"

context:
  site_name: "My Site"
  phone: "+1-555-123-4567"
  email: "info@example.com"

sections:
  - gap: "extended"
    background:
      color: "#ffffff"
      image:
        url: "https://example.com/image.jpg"
        position: "center center"
        size: "cover"
    padding:
      top: "80"
      bottom: "80"
    columns:
      - width: 50
        widgets:
          - type: texticon
            title: "Widget Title"
            subtitle: "Subtitle"
            text: "Widget description"
            icon: "fas fa-heart"
```

### Widget Configuration Examples

#### TextIcon Widget
```yaml
- type: texticon
  title: "Health & Wellness"
  subtitle: "Premium Care"
  text: "Professional healthcare services available 24/7"
  icon: "fas fa-medical-kit"
  icon_size: 25
  icon_color: "#ffffff"
  icon_bg_color: "#b68c2f"
  title_color: "#ffffff"
  text_color: "#ffffff"
  padding:
    all: "30"
  custom_settings:
    _border_radius:
      unit: "px"
      top: "10"
      right: "10"
      bottom: "10"
      left: "10"
      isLinked: true
```

#### Team Widget
```yaml
- type: team
  name: "Dr. Sarah Johnson"
  position: "Medical Director" 
  image:
    url: "https://example.com/doctor.jpg"
    alt: "Dr. Sarah Johnson"
  height: "420px"
  social_links:
    - icon: "fab fa-linkedin-in"
      url: "https://linkedin.com/in/dr-sarah-johnson"
      color: "#0077b5"
    - icon: "fab fa-twitter"
      url: "https://twitter.com/drsarah"
      color: "#1da1f2"
  background_icon: "fas fa-stethoscope"
```

#### Gallery Widget
```yaml
- type: gallery
  images:
    - url: "https://example.com/gallery1.jpg"
      alt: "Gallery image 1"
    - url: "https://example.com/gallery2.jpg"
      alt: "Gallery image 2"
  columns: "col-md-4"
  height: 200
  margin: 10
  overlay_color: "#000000"
  overlay_opacity: 0.6
  responsive:
    tablet:
      height: 150
      margin: 8
    mobile:
      height: 120
```

#### Testimonial Widget
```yaml
- type: testimonial
  columns: 3
  testimonials:
    - title: "John Smith"
      position: "Satisfied Customer"
      text: "Excellent service and professional staff!"
      image:
        url: "https://example.com/customer1.jpg"
        alt: "John Smith"
    - title: "Mary Johnson"
      position: "Long-time Resident"
      text: "This community feels like home."
      image:
        url: "https://example.com/customer2.jpg"
        alt: "Mary Johnson"
  align: "center"
  responsive:
    mobile:
      title_size: 15
      name_size: 16
      image_size: 40
```

## Placeholder System

The generator includes an advanced placeholder system for dynamic content:

### Built-in Placeholders

- `{{site_title}}` - Site title from config
- `{{site_name}}` - Site name from context
- `{{primary_color}}` - Theme primary color (#b68c2f)
- `{{phone}}` - Phone number from context
- `{{email}}` - Email from context
- `{{current_year}}` - Current year
- `{{demo_image_1}}`, `{{demo_image_2}}` - Demo images
- `{{demo_logo}}` - Demo logo placeholder

### Usage in Configuration

```yaml
context:
  site_name: "Cholot Community"
  phone: "+1-555-CHOLOT"
  
sections:
  - columns:
    - widgets:
      - type: texticon
        title: "Welcome to {{site_name}}"
        text: "Call us at {{phone}} for more information"
```

### Default Values

```yaml
title: "{{site_name:Default Site Name}}"  # Uses "Default Site Name" if site_name not set
```

## Advanced Features

### Background Settings

```yaml
sections:
  - background:
      color: "#b68c2f"
      image:
        url: "https://example.com/bg.jpg"
        position: "center center"
        size: "cover"
```

### Responsive Settings

```yaml
- type: gallery
  responsive:
    tablet:
      height: 200
      margin: 8
    mobile:
      height: 150
      margin: 5
```

### Custom Settings Override

```yaml
- type: texticon
  title: "Custom Widget"
  custom_settings:
    _animation: "fadeInUp"
    _animation_duration: "fast"
    custom_property: "custom_value"
```

## Output Structure

The generator produces valid Elementor JSON with the following structure:

```json
[
  {
    "id": "section0001",
    "elType": "section", 
    "settings": {
      "gap": "extended",
      "structure": "100",
      "background_background": "classic",
      "background_color": "#ffffff"
    },
    "elements": [
      {
        "id": "column0001",
        "elType": "column",
        "settings": {
          "_column_size": 100,
          "_inline_size": null
        },
        "elements": [
          {
            "id": "txticon0001",
            "elType": "widget",
            "settings": { /* widget settings */ },
            "elements": [],
            "widgetType": "cholot-texticon"
          }
        ],
        "isInner": false
      }
    ],
    "isInner": false
  }
]
```

## Validation

The generator includes comprehensive validation:

- JSON structure validation
- Required setting verification
- Widget type validation
- Image URL validation
- Color format validation

## Error Handling

- Missing widget types are skipped with warnings
- Invalid configurations fall back to defaults
- Malformed JSON/YAML files show clear error messages
- Missing placeholder values use default values

## Performance

- Predictable ID generation for consistent output
- Optimized spacing object creation
- Efficient placeholder resolution
- Minimal memory footprint

## Testing

The included `test_elementor_config.yaml` demonstrates all widget types and features:

```bash
# Test the generator
python3 enhanced_elementor_generator.py -i test_elementor_config.yaml -o test_results.json
```

This generates a comprehensive 80KB+ JSON file with:
- Hero section with background image
- Feature grid with 3 texticon widgets  
- About section with title and gallery
- Team section with 3 member profiles
- Services showcase with text-line widgets
- Testimonials section with customer reviews
- Blog posts section
- Contact form section
- Footer with logo and menu

## Integration

### With WordPress XML Generator

```python
from enhanced_elementor_generator import CompleteElementorGenerator
from generate_wordpress_xml import WordPressXMLGenerator

# Generate Elementor JSON
elementor_generator = CompleteElementorGenerator()
elementor_json = elementor_generator.generate_from_config('config.yaml', 'temp.json')

# Use in WordPress XML
xml_generator = WordPressXMLGenerator() 
xml_output = xml_generator.generate_xml({
    'pages': [{
        'title': 'Generated Page',
        'elementor_data': elementor_json
    }]
})
```

### Standalone Usage

The generator can be used independently to create Elementor JSON for:
- Page builder imports
- Template libraries
- Theme development
- Content migration
- Automated page generation

## Technical Implementation

### Architecture

- **PlaceholderSystem**: Advanced context-aware placeholder resolution
- **PredictableIDGenerator**: Consistent ID generation for testing  
- **ComprehensiveCholotFactory**: Complete widget factory with all 13 types
- **CompleteElementorGenerator**: Main orchestration class

### Key Algorithms

- **Context Resolution**: Hierarchical lookup (local > global > defaults)
- **Structure Calculation**: Automatic column layout based on content
- **Widget Routing**: Type-based factory method selection  
- **Validation Pipeline**: Multi-stage validation and error recovery

### Code Quality

- Full type hints for IDE support
- Comprehensive docstrings
- Error handling and recovery
- Clean separation of concerns
- Extensible architecture

## Conclusion

This Elementor JSON Generator provides a complete, production-ready solution for generating valid Elementor page structures. It successfully combines the hybrid approach with comprehensive widget support, making it suitable for both development and production use cases.

The generator can create complex, multi-section pages with all 13 Cholot widget types while maintaining the exact JSON structure expected by Elementor and WordPress.