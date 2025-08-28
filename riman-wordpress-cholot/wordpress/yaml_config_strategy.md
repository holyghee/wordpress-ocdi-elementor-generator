# YAML Configuration Strategy for Cholot Generator

## Overview

This document outlines the configuration strategy for the iterative Cholot WordPress generator, defining two YAML configurations that utilize the extracted Elementor structures to create progressive WordPress import scenarios.

## Configuration Files Created

### 1. cholot-minimal.yaml
**Purpose**: Essential MVP configuration for rapid testing and development
- **Items**: 3 core pages (Home, About, Contact) 
- **Strategy**: Minimal viable product approach
- **Use Case**: Quick development iterations, basic functionality testing

### 2. cholot-complete.yaml  
**Purpose**: Comprehensive configuration with all 65 extracted items
- **Items**: All extracted content (8 pages, 8 posts, 27 media, 11 nav items, 7 Elementor templates, 4 custom post types)
- **Strategy**: Full feature demonstration and production readiness
- **Use Case**: Complete theme showcase, client presentations, production deployment

## Configuration Architecture

### Site Structure
```yaml
site:
  title: "Cholot – Retirement Community WordPress Theme"
  url: "http://localhost:8082"
```

### WordPress Integration
- **Theme**: cholot
- **Required Plugins**: elementor, cholot-core
- **Admin Setup**: Automated user creation

### Elementor Integration Strategy

#### 1. Template Mapping
All pages reference extracted Elementor JSON structures:
```yaml
elementor_file: "elementor_structures/Home.json"
```

#### 2. Widget Configuration  
Complete widget inventory from extracted data:
- 24 custom Cholot widgets
- Standard Elementor widgets
- Theme-specific components

#### 3. Global Settings
- **Brand Color**: #b68c2f (extracted from theme)
- **Typography**: Playfair Display + Open Sans
- **Version**: 2.6.2 (matches extracted data)

### Content Hierarchy

#### Minimal Configuration (3 pages)
1. **Home** (ID: 6) - Front page with hero slider
2. **About** (ID: 179) - Company information  
3. **Contact** (ID: 289) - Contact form and details

#### Complete Configuration (All 65 items)
1. **Pages (8)**: Home, About, Service, Contact, Independent Living, Assisted Living, Blog
2. **Posts (8)**: Sample blog content with Elementor layouts
3. **Media (27)**: Images, videos, documents - all referenced media
4. **Navigation (11)**: Complete menu structure with hierarchical organization
5. **Elementor Library (7)**: Reusable templates and sections
6. **Custom Post Types (4)**: testimonial, team_member, service, gallery

### Import Processing Strategy

#### Minimal Strategy
- Core functionality first
- Essential pages only  
- Basic navigation
- Elementor validation
- Quick setup for development

#### Complete Strategy
- Full content import
- Media optimization
- Menu reconstruction  
- Custom post type setup
- Elementor library integration
- Quality assurance testing
- Production-ready configuration

### Navigation Structure

```yaml
menus:
  primary:
    name: "Default Menu"
    items:
      - Home (/)
      - About (/about)
      - Services (dropdown)
        - Service Overview (/service)
        - Independent Living (/independent-living)
        - Assisted Living (/assisted-living)  
      - Blog (/blog)
      - Contact (/contact)
```

### Quality Assurance Framework

Both configurations include validation steps:
- **Structure Validation**: Verify page hierarchy
- **Elementor Verification**: Confirm widget compatibility  
- **Link Validation**: Check internal/external links
- **Media Processing**: Optimize and validate images
- **Performance Testing**: Basic speed checks

## Implementation Benefits

### Iterative Development
1. **Rapid Prototyping**: Minimal config for quick MVP
2. **Feature Expansion**: Complete config for full deployment
3. **Progressive Testing**: Validate core before adding complexity

### Risk Mitigation
- **Minimal First**: Test core functionality before full import
- **Modular Approach**: Each section can be imported independently
- **Rollback Capability**: Clear configuration boundaries

### Developer Experience
- **Clear Documentation**: Self-documenting YAML structure
- **Predictable Imports**: Consistent file naming and organization
- **Easy Customization**: YAML allows simple modifications

## File Organization

```
/elementor_structures/
├── Home.json
├── About.json  
├── Contact.json
├── Service.json
├── Independent_living.json
├── Assisted_living.json
├── Post_*.json (8 files)
├── Header_Template.json
├── Footer_Template.json  
└── [Additional templates]
```

## Next Steps

1. **Test Minimal Configuration**: Validate core import process
2. **Iterate on Structure**: Refine based on import results  
3. **Complete Testing**: Full 65-item import validation
4. **Production Deployment**: Use complete config for final site

This strategy provides a clear path from development to production while maintaining the flexibility to test and validate at each step.