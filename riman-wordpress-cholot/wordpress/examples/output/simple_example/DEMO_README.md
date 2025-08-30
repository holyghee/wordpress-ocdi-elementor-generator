# My Simple Site - Example Demonstration

A minimal example of our YAML processor

## Configuration Overview

This example demonstrates a **My Simple Site** website with the following features:

- **Sections:** 3 different content sections
- **Navigation:** 6 menu items
- **Theme:** Primary color is #3498db

### Section Types

- `hero` - Landing section with title, subtitle, and call-to-action buttons
- `content` - Text content block with optional images
- `contact` - Contact form and business information

## How This Example Works

1. **YAML Configuration**: The `simple_example.yaml` file contains all the website configuration
2. **Processing**: The YAML processor reads this file and generates WordPress files
3. **Output**: Complete WordPress theme with all sections and features

## Processing Commands

```bash
# Process this example
php yaml_processor.php examples/simple_example.yaml

# Or use the convenience script
./examples/process_example.sh simple
```

## What Gets Generated

When processed, this YAML configuration will create:

- **index.php** - Main theme template with all 3 sections
- **style.css** - Theme styles with #3498db color scheme
- **functions.php** - WordPress theme functions and features
- **Elementor templates** - Pre-configured page builder templates
- **Custom post types** - If needed for specific features

---
*This is a demonstration file showing how the YAML processor analyzes configurations.*
*Generated at: 2025-08-30 12:48:56*
