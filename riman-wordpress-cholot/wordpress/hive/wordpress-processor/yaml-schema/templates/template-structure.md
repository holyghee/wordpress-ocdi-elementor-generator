# Cholot Theme YAML Template Structure

This document outlines the template system for the Cholot YAML configuration, providing reusable patterns and components.

## Template Hierarchy

### 1. Base Templates

#### Minimal Site Template
```yaml
# templates/minimal-site.yaml
site:
  title: "{{ site_title }}"
  description: "{{ site_description }}"
  url: "{{ site_url }}"
  language: "{{ language | default: 'en-US' }}"

design:
  colors:
    primary: "{{ primary_color | default: '#b68c2f' }}"
    secondary: "{{ secondary_color | default: '#ffffff' }}"
    background: "{{ background_color | default: '#ffffff' }}"
    text: "{{ text_color | default: '#000000' }}"

navigation:
  menus:
    - id: "main-menu"
      name: "Main Menu"
      items: "{{ menu_items }}"

pages:
  - id: "home"
    title: "Home"
    slug: ""
    template: "default"
    sections: "{{ home_sections }}"

global:
  performance:
    lazy_load_images: true
    minify_css: true
    minify_js: true
    enable_caching: true
```

#### Business Site Template
```yaml
# templates/business-site.yaml
extends: "minimal-site.yaml"

design:
  colors:
    primary: "{{ brand_primary }}"
    secondary: "{{ brand_secondary }}"
    accent: "{{ brand_accent }}"
  
  fonts:
    primary:
      family: "{{ primary_font | default: 'Open Sans' }}"
      weights: [300, 400, 600, 700]
    headings:
      family: "{{ heading_font | default: 'Montserrat' }}"
      weights: [400, 600, 700]

sections:
  hero_business:
    type: "hero"
    settings:
      background:
        type: "classic"
        color: "{{ hero_bg_color }}"
        image: "{{ hero_bg_image }}"
        overlay:
          color: "{{ hero_overlay_color }}"
          opacity: "{{ hero_overlay_opacity | default: 0.7 }}"
      padding: {top: "120px", right: "0", bottom: "120px", left: "0"}
    columns:
      - size: 60
        widgets:
          - type: "cholot-title"
            settings:
              title: "{{ hero_title }}"
              header_size: "h1"
              typography:
                font_size: "{{ hero_font_size | default: 48 }}"
                color: "{{ hero_text_color | default: '#ffffff' }}"
          - type: "text-editor"
            settings:
              editor: "{{ hero_description }}"
              text_color: "{{ hero_text_color | default: '#ffffff' }}"
          - type: "cholot-button"
            settings:
              btn_text: "{{ cta_text | default: 'Get Started' }}"
              link:
                url: "{{ cta_url | default: '/contact/' }}"
```

### 2. Component Templates

#### Service Card Component
```yaml
# templates/components/service-card.yaml
type: "cholot-texticon"
settings:
  title: "{{ service_title }}"
  subtitle: "{{ service_number | default: '' }}"
  text: "{{ service_description }}"
  icon: "{{ service_icon }}"
  title_color: "{{ colors.primary }}"
  subtitle_color: "{{ colors.secondary }}"
  text_color: "{{ colors.text }}"
  icon_color: "{{ colors.primary }}"
  icon_size: "{{ icon_size | default: 32 }}"
  typography:
    title:
      font_size: "{{ title_font_size | default: 24 }}"
      font_weight: "{{ title_font_weight | default: 600 }}"
    text:
      font_size: "{{ text_font_size | default: 16 }}"
      line_height: "{{ text_line_height | default: 1.6 }}"
```

#### Hero Section Component
```yaml
# templates/components/hero-section.yaml
type: "hero"
id: "{{ section_id | default: 'hero_section' }}"
settings:
  background:
    type: "{{ bg_type | default: 'classic' }}"
    color: "{{ bg_color }}"
    image: "{{ bg_image }}"
    overlay:
      color: "{{ overlay_color }}"
      opacity: "{{ overlay_opacity | default: 0.5 }}"
  padding: "{{ section_padding | default: {top: '120px', right: '0', bottom: '120px', left: '0'} }}"
  structure: "{{ column_structure | default: '60' }}"
columns:
  - size: "{{ content_width | default: 60 }}"
    widgets:
      - type: "cholot-title"
        settings:
          title: "{{ hero_title }}"
          header_size: "{{ title_size | default: 'h1' }}"
          typography:
            font_size: "{{ title_font_size | default: 48 }}"
            color: "{{ title_color }}"
      - type: "text-editor"
        settings:
          editor: "{{ hero_content }}"
          text_color: "{{ content_color }}"
      - type: "cholot-button"
        settings:
          btn_text: "{{ button_text }}"
          link:
            url: "{{ button_url }}"
```

#### Team Member Card
```yaml
# templates/components/team-member.yaml
type: "cholot-texticon"
settings:
  title: "{{ member_name }}"
  subtitle: "{{ member_position }}"
  text: "{{ member_bio }}"
  image: "{{ member_photo }}"
  social_links: "{{ member_social }}"
  card_style: true
  card_background: "{{ card_bg_color }}"
  card_border_radius: "{{ card_radius | default: 16 }}"
  card_padding: "{{ card_padding | default: {top: 32, right: 24, bottom: 32, left: 24} }}"
```

### 3. Layout Templates

#### Three Column Services Layout
```yaml
# templates/layouts/three-column-services.yaml
type: "content"
id: "services_section"
settings:
  background:
    type: "classic"
    color: "{{ section_bg_color | default: '#ffffff' }}"
  padding: {top: "100px", right: "0", bottom: "100px", left: "0"}
  structure: "33"
columns:
  - size: 33
    widgets:
      - template: "components/service-card.yaml"
        variables:
          service_title: "{{ service_1_title }}"
          service_description: "{{ service_1_description }}"
          service_icon: "{{ service_1_icon }}"
          service_number: "01"
  - size: 33
    widgets:
      - template: "components/service-card.yaml"
        variables:
          service_title: "{{ service_2_title }}"
          service_description: "{{ service_2_description }}"
          service_icon: "{{ service_2_icon }}"
          service_number: "02"
  - size: 33
    widgets:
      - template: "components/service-card.yaml"
        variables:
          service_title: "{{ service_3_title }}"
          service_description: "{{ service_3_description }}"
          service_icon: "{{ service_3_icon }}"
          service_number: "03"
```

#### About Section Layout
```yaml
# templates/layouts/about-section.yaml
type: "content"
id: "about_section"
settings:
  background:
    type: "classic"
    color: "{{ about_bg_color | default: '#f8f9fa' }}"
  padding: {top: "100px", right: "0", bottom: "100px", left: "0"}
  structure: "50"
columns:
  - size: 50
    widgets:
      - type: "cholot-title"
        settings:
          title: "{{ about_title }}"
          header_size: "h2"
          typography:
            font_size: 36
            color: "{{ colors.primary }}"
      - type: "text-editor"
        settings:
          editor: "{{ about_content }}"
          text_color: "{{ colors.text }}"
      - type: "cholot-button"
        settings:
          btn_text: "{{ about_cta_text | default: 'Learn More' }}"
          link:
            url: "{{ about_cta_url | default: '/about/' }}"
  - size: 50
    widgets:
      - type: "image"
        settings:
          image: "{{ about_image }}"
```

### 4. Page Templates

#### Landing Page Template
```yaml
# templates/pages/landing-page.yaml
id: "{{ page_id | default: 'landing' }}"
title: "{{ page_title }}"
slug: "{{ page_slug }}"
template: "{{ page_template | default: 'default' }}"
sections:
  - template: "components/hero-section.yaml"
    variables:
      hero_title: "{{ landing_hero_title }}"
      hero_content: "{{ landing_hero_content }}"
      bg_color: "{{ hero_background }}"
      title_color: "{{ hero_text_color }}"
  
  - template: "layouts/three-column-services.yaml"
    variables:
      service_1_title: "{{ service_1_title }}"
      service_1_description: "{{ service_1_description }}"
      service_1_icon: "{{ service_1_icon }}"
      service_2_title: "{{ service_2_title }}"
      service_2_description: "{{ service_2_description }}"
      service_2_icon: "{{ service_2_icon }}"
      service_3_title: "{{ service_3_title }}"
      service_3_description: "{{ service_3_description }}"
      service_3_icon: "{{ service_3_icon }}"
  
  - template: "layouts/about-section.yaml"
    variables:
      about_title: "{{ about_section_title }}"
      about_content: "{{ about_section_content }}"
      about_image: "{{ about_section_image }}"
```

#### Service Page Template
```yaml
# templates/pages/service-page.yaml
id: "{{ service_id }}"
title: "{{ service_title }}"
slug: "{{ service_slug }}"
template: "default"
sections:
  - type: "hero"
    settings:
      background:
        type: "classic"
        color: "{{ service_color }}"
      padding: {top: "80px", right: "0", bottom: "80px", left: "0"}
    columns:
      - size: 100
        widgets:
          - type: "cholot-title"
            settings:
              title: "{{ service_title }}"
              header_size: "h1"
              align: "center"
              typography:
                font_size: 42
                color: "#ffffff"
  
  - type: "content"
    settings:
      padding: {top: "100px", right: "0", bottom: "100px", left: "0"}
      structure: "60"
    columns:
      - size: 60
        widgets:
          - type: "text-editor"
            settings:
              editor: "{{ service_description }}"
          - type: "cholot-gallery"
            settings:
              gallery: "{{ service_images }}"
      - size: 40
        widgets:
          - type: "cholot-texticon"
            settings:
              title: "Key Features"
              text: "{{ service_features }}"
```

## Template Usage

### 1. Using Templates in Configuration
```yaml
# site-config.yaml
pages:
  - template: "pages/landing-page.yaml"
    variables:
      page_title: "Welcome to RIMAN GmbH"
      landing_hero_title: "Professional Consulting Services"
      service_1_title: "Strategy Consulting"
      service_1_description: "Strategic planning and execution"
      service_1_icon: "fas fa-chart-line"
```

### 2. Template Inheritance
```yaml
# custom-business.yaml
extends: "templates/business-site.yaml"

# Override specific values
design:
  colors:
    primary: "#2c3e50"
    secondary: "#3498db"

# Add custom sections
sections:
  custom_testimonials:
    type: "content"
    # ... custom section configuration
```

### 3. Conditional Templates
```yaml
# Conditional content based on site type
pages:
  - id: "home"
    sections:
      - template: "{% if site_type == 'business' %}components/hero-business.yaml{% else %}components/hero-personal.yaml{% endif %}"
        variables:
          hero_title: "{{ hero_title }}"
```

### 4. Dynamic Content Templates
```yaml
# templates/dynamic/blog-section.yaml
type: "content"
settings:
  background:
    type: "classic"
    color: "#ffffff"
columns:
  {% for post in recent_posts %}
  - size: "{{ 100 / recent_posts.length }}"
    widgets:
      - type: "cholot-post-three"
        settings:
          blog_post: 1
          specific_post: "{{ post.id }}"
          title: "{{ post.title }}"
          excerpt: "{{ post.excerpt }}"
  {% endfor %}
```

## Template Processing Engine

### 1. Template Loader
```javascript
class TemplateEngine {
    constructor(templateDir) {
        this.templateDir = templateDir;
        this.cache = new Map();
    }
    
    loadTemplate(templatePath) {
        if (this.cache.has(templatePath)) {
            return this.cache.get(templatePath);
        }
        
        const template = fs.readFileSync(
            path.join(this.templateDir, templatePath), 
            'utf8'
        );
        const parsed = yaml.load(template);
        this.cache.set(templatePath, parsed);
        return parsed;
    }
}
```

### 2. Variable Substitution
```javascript
function processTemplate(template, variables) {
    let processed = JSON.stringify(template);
    
    // Replace template variables
    for (const [key, value] of Object.entries(variables)) {
        const regex = new RegExp(`"\\{\\{\\s*${key}\\s*\\}\\}"`, 'g');
        processed = processed.replace(regex, JSON.stringify(value));
    }
    
    return JSON.parse(processed);
}
```

### 3. Template Compilation
```javascript
function compileTemplate(templatePath, variables = {}) {
    const template = templateEngine.loadTemplate(templatePath);
    
    // Handle template inheritance
    if (template.extends) {
        const baseTemplate = compileTemplate(template.extends, variables);
        template = deepMerge(baseTemplate, template);
    }
    
    // Process variables
    return processTemplate(template, variables);
}
```

## Pre-built Template Library

### Industry Templates
- `healthcare/clinic-site.yaml` - Medical practice template
- `restaurant/restaurant-site.yaml` - Restaurant/food service template
- `real-estate/agency-site.yaml` - Real estate agency template
- `consulting/professional-services.yaml` - Professional services template
- `nonprofit/charity-site.yaml` - Non-profit organization template

### Style Templates
- `modern/clean-minimal.yaml` - Clean, minimal design
- `corporate/professional-blue.yaml` - Corporate blue theme
- `creative/colorful-artistic.yaml` - Artistic, colorful design
- `luxury/elegant-gold.yaml` - Luxury, premium styling
- `tech/futuristic-dark.yaml` - Tech-focused dark theme

### Layout Templates
- `single-page/one-page-site.yaml` - Single page website
- `multi-page/standard-site.yaml` - Standard multi-page site
- `portfolio/creative-portfolio.yaml` - Portfolio/gallery focused
- `blog/content-focused.yaml` - Blog/content heavy site
- `ecommerce/online-store.yaml` - E-commerce template

## Template Customization Guide

### 1. Creating Custom Components
```yaml
# templates/custom/my-component.yaml
type: "cholot-texticon"
settings:
  # Define customizable properties
  title: "{{ component_title | default: 'Default Title' }}"
  subtitle: "{{ component_subtitle }}"
  # Set fixed styling
  typography:
    title:
      font_weight: 600
      text_transform: "uppercase"
```

### 2. Building Custom Layouts
```yaml
# templates/custom/my-layout.yaml
type: "content"
settings:
  structure: "{{ layout_structure | default: '50' }}"
columns:
  {% for column in layout_columns %}
  - size: "{{ column.size }}"
    widgets:
      {% for widget in column.widgets %}
      - template: "{{ widget.template }}"
        variables: "{{ widget.variables }}"
      {% endfor %}
  {% endfor %}
```

### 3. Template Validation
```yaml
# template-schema.yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: "object"
properties:
  type:
    type: "string"
    enum: ["content", "hero", "header", "footer"]
  settings:
    type: "object"
  columns:
    type: "array"
    items:
      type: "object"
      properties:
        size:
          type: "number"
          minimum: 1
          maximum: 100
required: ["type", "columns"]
```

This template system provides maximum flexibility while maintaining consistency and reusability across different site configurations.