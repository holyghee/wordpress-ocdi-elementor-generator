# Bella Vista Ristorante - Example Demonstration

Authentic Italian cuisine in the heart of downtown

## Configuration Overview

This example demonstrates a **Bella Vista Ristorante** website with the following features:

- **Sections:** 8 different content sections
- **Navigation:** 33 menu items
- **Theme:** Primary color is #8b0000

### Section Types

- `hero` - Landing section with title, subtitle, and call-to-action buttons
- `story` - About/story section with rich content
- `menu` - Restaurant menu with categories and pricing
- `gallery` - Image gallery with categories and lightbox
- `reviews` - Customer reviews and ratings
- `events` - Special events and offers
- `reservations` - Online reservation system
- `contact` - Contact form and business information

### Special Features

- ✅ Restaurant Menu
- ✅ Reservations
- ✅ Wine List
- ✅ Social Media

## How This Example Works

1. **YAML Configuration**: The `restaurant_example.yaml` file contains all the website configuration
2. **Processing**: The YAML processor reads this file and generates WordPress files
3. **Output**: Complete WordPress theme with all sections and features

## Processing Commands

```bash
# Process this example
php yaml_processor.php examples/restaurant_example.yaml

# Or use the convenience script
./examples/process_example.sh restaurant
```

## What Gets Generated

When processed, this YAML configuration will create:

- **index.php** - Main theme template with all 8 sections
- **style.css** - Theme styles with #8b0000 color scheme
- **functions.php** - WordPress theme functions and features
- **Elementor templates** - Pre-configured page builder templates
- **Custom post types** - If needed for specific features

---
*This is a demonstration file showing how the YAML processor analyzes configurations.*
*Generated at: 2025-08-30 12:48:56*
