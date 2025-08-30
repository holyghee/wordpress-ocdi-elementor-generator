# TechSolutions Pro - Example Demonstration

Professional IT consulting and digital transformation services

## Configuration Overview

This example demonstrates a **TechSolutions Pro** website with the following features:

- **Sections:** 8 different content sections
- **Navigation:** 22 menu items
- **Theme:** Primary color is #2c5aa0

### Section Types

- `hero` - Landing section with title, subtitle, and call-to-action buttons
- `services` - Grid of service cards with icons and descriptions
- `stats` - Statistics and achievements display
- `team` - Team member profiles with photos and social links
- `testimonials` - Customer reviews and testimonials
- `pricing` - Pricing tables with feature comparisons
- `cta` - Call-to-action section
- `contact` - Contact form and business information

### Special Features

- ✅ Service Cards
- ✅ Team Profiles
- ✅ Testimonials
- ✅ Pricing Tables

## How This Example Works

1. **YAML Configuration**: The `service_company.yaml` file contains all the website configuration
2. **Processing**: The YAML processor reads this file and generates WordPress files
3. **Output**: Complete WordPress theme with all sections and features

## Processing Commands

```bash
# Process this example
php yaml_processor.php examples/service_company.yaml

# Or use the convenience script
./examples/process_example.sh service_company
```

## What Gets Generated

When processed, this YAML configuration will create:

- **index.php** - Main theme template with all 8 sections
- **style.css** - Theme styles with #2c5aa0 color scheme
- **functions.php** - WordPress theme functions and features
- **Elementor templates** - Pre-configured page builder templates
- **Custom post types** - If needed for specific features

---
*This is a demonstration file showing how the YAML processor analyzes configurations.*
*Generated at: 2025-08-30 12:48:56*
