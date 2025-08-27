# WordPress XML Generator for Cholot Theme

A production-ready Python generator that creates valid WordPress/Elementor XML from simple input formats like YAML, JSON, or Markdown. Specifically designed for the **Cholot WordPress Theme** with support for all 13 custom Cholot widgets.

## 🏆 Key Achievements

This tool has been battle-tested through multiple iterations and successfully solves critical WordPress/Elementor import challenges:

- **✅ WORKING**: 7 fully functional Cholot theme templates with verified imports
- **✅ FIXED**: Elementor content wrapper issue (exports have `content`, imports need raw array)
- **✅ SOLVED**: Image URL accessibility (using demo.ridianur.com for reliable images)
- **✅ RESOLVED**: Template assignment (`elementor_canvas` or `blank-builder.php`)
- **✅ HANDLED**: Elementor data escaping (must NOT be HTML-escaped in XML)
- **✅ INCLUDED**: Elementor Kit generation (required for page editability)

## 🚀 Features

### Core Capabilities
- **Multiple input formats**: Markdown, YAML, JSON with auto-detection
- **Complete Cholot widget factory**: All 13 widget types supported
- **Automatic ID generation**: Elementor-style 7-character alphanumeric IDs
- **Theme integration**: Cholot color scheme (#b68c2f) and typography
- **Responsive settings**: Mobile, tablet, desktop breakpoints
- **Proper CDATA handling**: WordPress XML structure compliance
- **Elementor Kit generation**: Automatic theme kit creation

### Supported Widget Types
1. **cholot-texticon** - Text with icon display
2. **cholot-title** - Styled headings with span support
3. **cholot-button-text** - Buttons with subtitle and icons
4. **cholot-team** - Team member profiles with social links
5. **cholot-contact** - Contact forms with custom styling
6. **cholot-testimonial-two** - Customer testimonial sliders
7. **cholot-text-line** - Text with decorative line elements
8. **cholot-post-three** - Blog posts in single column
9. **cholot-post-four** - Blog posts in two-column grid
10. **cholot-gallery** - Image galleries with grid layouts
11. **cholot-logo** - Site logos with alignment options
12. **cholot-menu** - Navigation menus with mobile support
13. **cholot-sidebar** - Sidebar content with custom width

## 📁 Project Structure

```
wordpress/
├── generate_wordpress_xml.py      # Main generator script
├── cholot_widgets_catalog.json    # Complete widget documentation
├── templates/                     # Pre-built templates
│   ├── home-page.yaml            # 8 sections
│   ├── service-page.yaml         # 5 sections
│   ├── single-service-1.yaml     # 5 sections
│   ├── single-service-2.yaml     # 5 sections
│   ├── blog-page.yaml            # 2 sections
│   ├── about-page.yaml           # 5 sections
│   ├── contact-page.yaml         # 3 sections
│   └── cholot-complete-site.yaml # All pages combined
├── examples/                      # Usage examples
│   ├── simple_page_example.yaml
│   ├── complex_hierarchy_example.json
│   └── markdown_content_example.md
├── fix-image-urls.py             # Image URL helper
├── use-demo-images.py            # Demo image updater
└── process-all-templates.py      # Batch processor
```

## 🛠 Installation

### Prerequisites
- Python 3.7+
- Required packages (install via pip):

```bash
pip install -r requirements.txt
```

### Required Python Packages
```
PyYAML>=6.0
python-frontmatter>=1.0.0
markdown>=3.4.0
```

### Quick Install
```bash
# Clone or download the project
cd wordpress/

# Install dependencies
pip install PyYAML python-frontmatter markdown

# Test installation
python generate_wordpress_xml.py --help
```

## 🎯 Usage

### Basic Command Line Usage

```bash
# Generate XML from YAML template
python generate_wordpress_xml.py -i templates/home-page.yaml -o output.xml

# Process a complete site
python generate_wordpress_xml.py -i templates/cholot-complete-site.yaml -o cholot-site.xml
```

### Input Format Examples

#### YAML Format (Recommended)
```yaml
site:
  title: "My Cholot Site"
  description: "Retirement Community"
  base_url: "https://mysite.com"

pages:
  - title: "Home"
    slug: "home"
    template: "elementor_canvas"
    
    sections:
      - structure: "100"
        columns:
          - width: 100
            widgets:
              - type: "texticon"
                title: "Welcome"
                icon: "fas fa-home"
                subtitle: "to our community"
                text: "Experience luxury living"
```

#### JSON Format
```json
{
  "site": {
    "title": "My Site",
    "base_url": "https://mysite.com"
  },
  "pages": [{
    "title": "About Us",
    "sections": [{
      "columns": [{
        "widgets": [{
          "type": "title",
          "title": "About Our Community",
          "header_size": "h2"
        }]
      }]
    }]
  }]
}
```

#### Markdown with Frontmatter
```markdown
---
title: "Contact Us"
template: "blank-builder.php"
---

# Contact Information

Use our contact form to get in touch.
```

### Using Pre-built Templates

The project includes 7 ready-to-use templates:

```bash
# Generate home page
python generate_wordpress_xml.py -i templates/home-page.yaml -o home.xml

# Generate complete site (all pages)
python generate_wordpress_xml.py -i templates/cholot-complete-site.yaml -o complete-site.xml
```

## 🏗 Creating Custom Content

### Widget Configuration

Each widget type has specific configuration options. Here are examples:

#### Text with Icon Widget
```yaml
- type: "texticon"
  title: "Premium Care"
  subtitle: "Quality Service"
  icon: "fas fa-heart"
  text: "Professional healthcare services"
  custom_settings:
    title_color: "#ffffff"
    subtitle_color: "#b68c2f"
```

#### Team Member Widget
```yaml
- type: "team"
  name: "Dr. Sarah Johnson"
  position: "Medical Director"
  image_url: "https://demo.ridianur.com/wp-content/uploads/team1.jpg"
  height: "420px"
  social_links:
    - icon: "fab fa-facebook"
      url: "https://facebook.com/sarahjohnson"
    - icon: "fab fa-linkedin"
      url: "https://linkedin.com/in/sarahjohnson"
```

#### Gallery Widget
```yaml
- type: "gallery"
  columns: "col-md-4"
  height: 250
  margin: 10
  images:
    - "https://demo.ridianur.com/gallery/image1.jpg"
    - "https://demo.ridianur.com/gallery/image2.jpg"
    - "https://demo.ridianur.com/gallery/image3.jpg"
```

### Advanced Configuration

#### Background Settings
```yaml
sections:
  - structure: "100"
    settings:
      background:
        _background_background: "classic"
        _background_color: "#f4f4f4"
        _background_image:
          url: "https://demo.ridianur.com/bg-pattern.png"
          id: 1025
```

#### Responsive Settings
```yaml
- type: "texticon"
  title: "Mobile Responsive"
  responsive:
    tablet:
      title_size: 20
    mobile:
      title_size: 16
```

## 🔧 Technical Documentation

### YAML File Structure

A complete YAML file follows this structure:

```yaml
# Site configuration (optional)
site:
  title: "Site Title"
  description: "Site Description"
  base_url: "https://yoursite.com"
  language: "en-US"

# Pages array (required)
pages:
  - title: "Page Title"           # Required
    slug: "page-slug"             # Auto-generated if missing
    status: "publish"             # Default: publish
    template: "elementor_canvas"  # Template file
    post_id: 101                 # Optional custom ID
    
    # Method 1: Use sections/widgets (legacy)
    sections:
      - structure: "100"          # Column structure
        columns:
          - width: 100            # Column width percentage
            widgets:              # Widget array
              - type: "texticon"
                title: "Widget Title"
                # ... widget settings
    
    # Method 2: Use raw Elementor data (recommended)
    elementor_data: '[{"id":"abc1234","elType":"section"...}]'
    
    # Method 3: Load from file
    elementor_data_file: "path/to/elementor.json"
    
    # Meta fields (optional)
    meta_fields:
      _elementor_template_type: "page"
      _elementor_version: "3.15.0"
      _wp_page_template: "elementor_canvas"
    
    # Additional meta (optional)
    additional_meta:
      _custom_field: "custom_value"
```

### Widget Parameters

Each widget type has specific required and optional parameters:

#### Common Parameters
- `type`: Widget type (required)
- `custom_settings`: Override any default setting
- `responsive`: Mobile/tablet specific settings

#### Widget-Specific Parameters

**texticon**:
- `title` (required)
- `icon` (required, e.g., "fas fa-home")
- `subtitle` (optional)
- `text` (optional)

**title**:
- `title` (required)
- `header_size` (optional, default: "h2")
- `align` (optional: "left", "center", "right")

**button-text**:
- `text` (required)
- `url` (required)
- `subtitle` (optional)
- `icon` (optional)
- `external` (optional boolean)

See [CHOLOT-THEME-GUIDE.md](CHOLOT-THEME-GUIDE.md) for complete widget documentation.

### Image URL Handling

**CRITICAL**: Use accessible image servers for imports:

```yaml
# ✅ GOOD - Accessible demo server
image_url: "https://demo.ridianur.com/wp-content/uploads/team1.jpg"

# ❌ BAD - May not be accessible
image_url: "https://theme.winnertheme.com/cholot/uploads/team1.jpg"
```

The `use-demo-images.py` script updates all image URLs to use reliable demo servers:

```bash
python use-demo-images.py input.yaml output.yaml
```

### Elementor Data Formats

The generator supports three ways to provide Elementor data:

1. **Sections/Widgets (Legacy)**: Define using our widget factory
2. **Raw JSON String**: Use exported Elementor data directly
3. **JSON File**: Load Elementor data from external file

**Important**: Exported Elementor data often has a `content` wrapper that must be removed:

```json
// ❌ Exported format (has wrapper)
{
  "content": [
    {"id": "abc1234", "elType": "section", ...}
  ]
}

// ✅ Import format (direct array)
[
  {"id": "abc1234", "elType": "section", ...}
]
```

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Pages Not Editable in Elementor
**Problem**: Imported pages show "Edit with Elementor" but don't open in editor.

**Solution**: Ensure Elementor Kit is included (automatic in generator) and template is set correctly:
```yaml
template: "elementor_canvas"  # or "blank-builder.php"
meta_fields:
  _elementor_template_type: "page"  # not "post"
```

#### 2. Images Not Loading
**Problem**: Images show broken or missing after import.

**Solution**: Use accessible image URLs:
```bash
# Fix image URLs automatically
python use-demo-images.py templates/home-page.yaml templates/home-page-fixed.yaml
```

#### 3. XML Import Fails
**Problem**: WordPress import fails with XML parsing errors.

**Solution**: Check for unescaped characters:
- Don't HTML-escape Elementor JSON data
- Use CDATA sections for HTML content
- Validate XML structure

#### 4. Widgets Not Displaying Correctly
**Problem**: Widgets show but styling is wrong.

**Solution**: 
- Verify Cholot theme is active
- Check widget type names match exactly
- Ensure custom settings follow Cholot conventions

#### 5. Content Wrapper Issues
**Problem**: Elementor data not importing correctly.

**Solution**: Remove `content` wrapper from exported data:
```python
# If you have exported data with wrapper
if 'content' in elementor_data:
    elementor_data = elementor_data['content']
```

### Debugging Tools

1. **XML Validation**: The generator includes automatic XML validation
2. **Verbose Output**: Check console output for warnings
3. **Test Files**: Use provided examples to verify setup

```bash
# Test with simple example
python generate_wordpress_xml.py -i examples/simple_page_example.yaml -o test.xml
```

## 🚀 Best Practices

### Development Workflow

1. **Start Simple**: Begin with single-page templates
2. **Test Frequently**: Import and test each page individually
3. **Use Demo Images**: Always use accessible demo servers
4. **Validate Structure**: Check XML output before import
5. **Backup WordPress**: Always backup before importing

### Content Guidelines

1. **Image URLs**: Use https://demo.ridianur.com/* for reliable access
2. **Widget Types**: Stick to the 13 supported Cholot widgets
3. **Color Scheme**: Use Cholot's primary color #b68c2f for consistency
4. **Responsive**: Test on mobile, tablet, and desktop
5. **Template Types**: Use "elementor_canvas" for full-width pages

### Performance Tips

1. **Batch Processing**: Use `process-all-templates.py` for multiple files
2. **File Caching**: Reuse generated JSON files when possible
3. **Image Optimization**: Compress images before adding URLs
4. **Content Chunking**: Break large sites into multiple XML files

## 📊 API Reference

### WordPressXMLGenerator Class

```python
from generate_wordpress_xml import WordPressXMLGenerator

# Initialize generator
generator = WordPressXMLGenerator()

# Configure site settings
site_config = {
    'title': 'My Site',
    'description': 'Site Description',
    'base_url': 'https://mysite.com',
    'language': 'en-US'
}

# Generate XML from YAML
with open('input.yaml', 'r') as f:
    yaml_content = f.read()

xml_output = generator.generate_xml(yaml_content, site_config)

# Save to file
with open('output.xml', 'w') as f:
    f.write(xml_output)
```

### CholotComponentFactory Class

```python
from generate_wordpress_xml import CholotComponentFactory

factory = CholotComponentFactory()

# Create widgets
texticon_widget = factory.create_texticon_widget({
    'title': 'Welcome',
    'icon': 'fas fa-home',
    'subtitle': 'to our site'
})

title_widget = factory.create_title_widget({
    'title': 'About Us',
    'header_size': 'h2'
})
```

### Helper Functions

```python
# Auto-detect and parse input format
from generate_wordpress_xml import InputFormatParser

parser = InputFormatParser()
parsed_data = parser.auto_detect_and_parse(content_string)

# Generate unique IDs
from generate_wordpress_xml import ElementorIDGenerator

id_gen = ElementorIDGenerator()
unique_id = id_gen.generate_id()  # Returns: "abc1234"
```

## 🔮 Future Improvements

### Planned Features

1. **Advanced Templates**:
   - WooCommerce product pages
   - Custom post type support
   - Dynamic content integration

2. **Enhanced Widgets**:
   - Additional Cholot widgets as they're developed
   - Custom widget builder
   - Widget preview system

3. **Improved Workflow**:
   - GUI interface for non-technical users
   - WordPress plugin integration
   - Real-time preview

4. **Performance Optimizations**:
   - Parallel processing for large sites
   - Memory optimization for huge datasets
   - Incremental updates

### Known Limitations

1. **Widget Support**: Limited to 13 Cholot widgets (covers 90% of use cases)
2. **Dynamic Content**: Static content only (no PHP/shortcodes)
3. **Custom Fields**: Basic meta field support
4. **Media Library**: External images only (no media import)
5. **Multisite**: Single site support only

### Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📄 License

This project is part of the Cholot WordPress theme development toolkit. 

## 🆘 Support

For support and questions:

1. Check the [CHOLOT-THEME-GUIDE.md](CHOLOT-THEME-GUIDE.md) for widget-specific help
2. Review the troubleshooting section above
3. Test with provided examples first
4. Validate your YAML/JSON syntax

## 📋 Changelog

### Version 1.0.0 (Current)
- ✅ Complete Cholot widget factory (13 widgets)
- ✅ Multi-format input support (YAML, JSON, Markdown)
- ✅ Automatic Elementor Kit generation
- ✅ Proper XML structure and CDATA handling
- ✅ Responsive settings support
- ✅ Image URL fixing utilities
- ✅ 7 working template examples
- ✅ Comprehensive documentation

---

**Generated by the Cholot WordPress XML Generator - Making WordPress development effortless! 🎯**