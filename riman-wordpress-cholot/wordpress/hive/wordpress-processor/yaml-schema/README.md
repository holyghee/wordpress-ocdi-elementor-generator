# Cholot WordPress Theme YAML Configuration System

A comprehensive, human-readable configuration system for the Cholot WordPress theme that allows complete control over all theme aspects through simple YAML files.

## 🎯 Overview

This YAML schema system transforms the complex Cholot theme customization process into an intuitive, declarative configuration approach. Instead of manually configuring Elementor widgets and WordPress settings, you define your entire site structure in clean, readable YAML files.

## 🚀 Key Features

- **Complete Theme Control**: Configure every aspect of the Cholot theme from a single YAML file
- **Design Token System**: Centralized color, typography, and spacing management
- **Responsive Configuration**: Define responsive behavior for all screen sizes
- **Widget Library**: Support for all Cholot custom widgets and standard Elementor widgets
- **Template System**: Reusable components and layouts
- **Content Management**: Structured content definition with media library integration
- **Performance Optimization**: Built-in performance and SEO settings
- **Migration Tools**: Seamless import/export between YAML and WordPress

## 📁 Directory Structure

```
yaml-schema/
├── schemas/
│   └── cholot-schema.yaml          # Main schema definition
├── examples/
│   ├── demo-site-replica.yaml     # Exact demo data replication
│   ├── riman-gmbh-site.yaml      # Business site example
│   └── advanced-customization.yaml # Complex features showcase
├── templates/
│   ├── template-structure.md      # Template system documentation
│   ├── components/                # Reusable component templates
│   ├── layouts/                   # Layout templates
│   └── pages/                     # Page templates
├── mappings/
│   └── yaml-to-elementor-mapping.md # Conversion documentation
└── README.md                       # This file
```

## 🛠️ Quick Start

### 1. Basic Site Configuration

Create a simple site configuration:

```yaml
# my-site.yaml
site:
  title: "My Business"
  description: "Professional services"
  url: "https://mybusiness.com"

design:
  colors:
    primary: "#2c3e50"
    secondary: "#3498db"
    background: "#ffffff"

pages:
  - id: "home"
    title: "Home"
    sections:
      - type: "hero"
        columns:
          - size: 100
            widgets:
              - type: "cholot-title"
                settings:
                  title: "Welcome to My Business"
                  header_size: "h1"
```

### 2. Using Pre-built Examples

Start with one of our example configurations:

```bash
# Copy an example
cp examples/riman-gmbh-site.yaml my-site.yaml

# Customize for your needs
vim my-site.yaml
```

### 3. Template-based Configuration

Use templates for rapid development:

```yaml
# my-business.yaml
pages:
  - template: "pages/landing-page.yaml"
    variables:
      page_title: "My Business"
      hero_title: "Professional Services"
      service_1_title: "Consulting"
      service_1_icon: "fas fa-chart-line"
```

## 📋 Schema Structure

### Core Sections

1. **Site Configuration**
   - Basic site metadata
   - Language and timezone settings

2. **Design System**
   - Color palette management
   - Typography definitions
   - Spacing and layout tokens

3. **Navigation**
   - Menu structure and items
   - Responsive navigation behavior

4. **Content Management**
   - Posts and categories
   - Media library assets
   - Gallery management

5. **Page Structure**
   - Section definitions
   - Column layouts
   - Widget configurations

6. **Global Settings**
   - Header and footer configuration
   - Performance optimizations
   - SEO settings

## 🎨 Design System

### Colors
```yaml
design:
  colors:
    primary: "#b68c2f"      # Brand primary color
    secondary: "#ffffff"    # Secondary/accent color
    background: "#f4f4f4"   # Page background
    text: "#000000"         # Primary text color
    accent: "#232323"       # Highlight color
```

### Typography
```yaml
design:
  fonts:
    primary: 
      family: "Source Sans Pro"
      weights: [400, 600, 700, 900]
    headings:
      family: "Montserrat"
      weights: [600, 700]
```

### Spacing
```yaml
design:
  spacing:
    xs: "5px"    # Extra small spacing
    sm: "10px"   # Small spacing
    md: "15px"   # Medium spacing
    lg: "30px"   # Large spacing
    xl: "60px"   # Extra large spacing
```

## 🧩 Widget System

### Cholot Custom Widgets

#### Text Icon Widget
```yaml
widgets:
  - type: "cholot-texticon"
    settings:
      title: "Service Title"
      subtitle: "Optional subtitle"
      text: "<p>Service description</p>"
      icon: "fas fa-star"
      title_color: "#2c3e50"
      icon_color: "#3498db"
```

#### Menu Widget
```yaml
widgets:
  - type: "cholot-menu"
    settings:
      cholot_menu: "main-menu"
      align: "center"
      styling:
        menu_color: "#ffffff"
        menu_color_hover: "#3498db"
```

#### Post Widget
```yaml
widgets:
  - type: "cholot-post-three"
    settings:
      blog_post: 3
      blog_column: "three"
      show_excerpt: true
      button: "Read More"
```

### Standard Elementor Widgets

#### Text Editor
```yaml
widgets:
  - type: "text-editor"
    settings:
      editor: "<p>Your content here</p>"
      text_color: "#000000"
      align: "left"
```

#### Button
```yaml
widgets:
  - type: "cholot-button"
    settings:
      btn_text: "Get Started"
      link:
        url: "/contact/"
        is_external: false
      styling:
        background_color: "#3498db"
        text_color: "#ffffff"
```

## 📱 Responsive Configuration

All widgets support responsive settings:

```yaml
columns:
  - size: 50              # Desktop: 50%
    responsive:
      tablet: 100          # Tablet: 100%
      mobile: 100          # Mobile: 100%
    widgets: []
```

## 🎛️ Advanced Features

### Animations
```yaml
advanced_features:
  animations:
    enabled: true
    library: "AOS"
    duration: 800
    offset: 100
```

### Performance
```yaml
global:
  performance:
    lazy_load_images: true
    minify_css: true
    minify_js: true
    enable_caching: true
```

### SEO
```yaml
advanced_features:
  seo:
    schema_markup: true
    open_graph: true
    twitter_cards: true
```

## 🔄 Conversion Process

The YAML configuration is converted to WordPress/Elementor format through:

1. **YAML Parsing**: Configuration is parsed and validated
2. **Design Token Application**: Colors, fonts, and spacing are applied
3. **Widget Mapping**: YAML widgets are converted to Elementor JSON
4. **Content Creation**: Posts, pages, and media are generated
5. **WordPress Import**: Standard WordPress XML import process

## 📚 Examples

### Simple Business Site
```yaml
site:
  title: "ACME Consulting"
  
design:
  colors:
    primary: "#2c3e50"
    secondary: "#3498db"

pages:
  - id: "home"
    sections:
      - type: "hero"
        columns:
          - size: 100
            widgets:
              - type: "cholot-title"
                settings:
                  title: "Professional <span style='color: #3498db;'>Consulting</span>"
              - type: "cholot-button"
                settings:
                  btn_text: "Contact Us"
                  link: {url: "/contact/"}
```

### E-commerce Site
```yaml
site:
  title: "Fashion Store"

design:
  colors:
    primary: "#e91e63"
    secondary: "#000000"
    
pages:
  - id: "home"
    sections:
      - type: "hero"
        settings:
          background:
            type: "image"
            image: "/wp-content/uploads/fashion-hero.jpg"
        columns:
          - widgets:
              - type: "cholot-title"
                settings:
                  title: "Latest Fashion Trends"
              - type: "cholot-gallery"
                settings:
                  gallery: 
                    - {id: "1", url: "/uploads/product1.jpg"}
                    - {id: "2", url: "/uploads/product2.jpg"}
```

## 🔧 Development Tools

### Validation
```bash
# Validate YAML syntax
node scripts/validate-yaml.js my-site.yaml

# Check schema compliance
node scripts/check-schema.js my-site.yaml
```

### Conversion
```bash
# Convert YAML to Elementor JSON
node scripts/convert-yaml.js my-site.yaml output.json

# Generate WordPress XML export
node scripts/generate-xml.js output.json site-export.xml
```

### Testing
```bash
# Test configuration locally
node scripts/test-config.js my-site.yaml

# Preview in browser
node scripts/preview.js my-site.yaml
```

## 🎯 Use Cases

### 1. Rapid Prototyping
Quickly create and iterate on site designs without manual WordPress configuration.

### 2. Client Presentations
Present multiple design variations using different YAML configurations.

### 3. Development Workflow
- Developers work with YAML files in version control
- Designers can easily modify colors, fonts, and layouts
- Content teams can update copy and media references
- DevOps can deploy configurations automatically

### 4. Site Migration
Move sites between environments using portable YAML configurations.

### 5. Multi-site Management
Manage multiple WordPress sites with shared design systems and templates.

## 🚀 Integration Examples

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy Site
on:
  push:
    paths: ['site-config.yaml']
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Convert YAML to WordPress
        run: |
          node scripts/convert-yaml.js site-config.yaml
          wp import generated-export.xml
```

### Docker Integration
```dockerfile
# Dockerfile
FROM wordpress:latest
COPY site-config.yaml /var/www/html/
COPY scripts/ /var/www/html/scripts/
RUN node scripts/setup-from-yaml.js site-config.yaml
```

## 📊 Benefits

### For Developers
- **Version Control**: YAML files work perfectly with Git
- **Collaboration**: Multiple developers can work on different sections
- **Testing**: Easy to create test configurations and variations
- **Documentation**: Self-documenting configuration structure

### For Designers
- **Design Tokens**: Centralized control over colors, fonts, spacing
- **Consistency**: Enforced design system across all pages
- **Flexibility**: Easy to experiment with different layouts
- **Responsive**: Built-in responsive configuration

### For Content Teams
- **Structured Content**: Clear content structure and requirements
- **Media Management**: Organized media library with proper metadata
- **SEO Optimization**: Built-in SEO best practices
- **Performance**: Optimized output with lazy loading and minification

### For Clients
- **Transparency**: Clear understanding of site structure
- **Customization**: Easy to request specific changes
- **Maintenance**: Simplified ongoing updates and modifications
- **Portability**: Configuration can be used across different environments

## 🛣️ Roadmap

### Phase 1 (Current)
- [x] Core schema definition
- [x] Basic widget support
- [x] Example configurations
- [x] Documentation

### Phase 2 (Planned)
- [ ] Visual YAML editor
- [ ] Live preview system
- [ ] Advanced animation support
- [ ] Custom widget builder

### Phase 3 (Future)
- [ ] Multi-site management dashboard
- [ ] AI-powered configuration suggestions
- [ ] Integration with popular page builders
- [ ] Marketplace for templates

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/your-org/cholot-yaml-schema.git
cd cholot-yaml-schema
npm install
npm run validate
```

### Adding New Widgets
1. Add widget definition to `schemas/cholot-schema.yaml`
2. Create mapping in `mappings/yaml-to-elementor-mapping.md`
3. Add example usage to `examples/`
4. Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Full documentation available in the `/docs` folder
- **Issues**: Report bugs and request features on GitHub Issues
- **Community**: Join our Discord server for community support
- **Commercial**: Professional support available through our partners

## 🙏 Acknowledgments

- Cholot theme developers for the excellent foundation
- Elementor team for the powerful page builder
- YAML specification contributors
- Open source community for tools and libraries

---

**Ready to transform your WordPress development workflow?** Start with our [Quick Start Guide](#-quick-start) and build your first YAML-configured site in minutes!