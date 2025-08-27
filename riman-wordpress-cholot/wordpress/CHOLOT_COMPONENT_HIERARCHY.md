# Cholot Theme - Component Hierarchy & Reusable Structures

## Section Layout Patterns

### 1. Hero Section Pattern
```
Section (full-width, background image/video)
├── Column (100%)
    └── rdn-slider (not cholot widget, but commonly used)
        ├── Title with span styling
        ├── Subtitle
        ├── Content text
        └── Call-to-action button
```

### 2. Feature Section Pattern (Most Common)
```
Section (colored background, padding: 60px)
├── Column (25% each - 4 columns)
│   ├── Inner Section (with background image)
│   │   └── Column (100%)
│   │       └── image widget
│   └── Inner Section (content overlay)
│       └── Column (100%)
│           └── cholot-texticon
│               ├── Icon (FontAwesome)
│               ├── Subtitle (uppercase, #b68c2f)
│               ├── Title (main heading)
│               └── Description text
```

### 3. About/Content Section Pattern
```
Section (standard padding)
├── Column (50% - Content)
│   ├── cholot-title (with span accent)
│   ├── divider (25px width, #b68c2f)
│   ├── text-editor (main content)
│   └── Inner Section (2 columns)
│       ├── Column (50%) - cholot-texticon (feature 1)
│       └── Column (50%) - cholot-texticon (feature 2)
└── Column (50% - Image)
    └── image widget (with animation)
```

### 4. Team Section Pattern
```
Section (background with shape divider)
├── Column (33.33% each - 3 columns)
    └── cholot-team
        ├── Background image
        ├── Team member photo
        ├── Name and position
        ├── Social media icons
        └── Hover animation effects
```

### 5. Testimonial Section Pattern
```
Section (full-width, dark background)
├── Column (100%)
    └── cholot-testimonial-two
        ├── Multiple testimonial slides
        ├── Customer photos
        ├── Quote content
        └── Name and position
```

### 6. Blog/News Section Pattern
```
Section (standard layout)
├── Column (title column)
│   ├── cholot-title
│   └── divider
└── Column (content column)
    └── cholot-post-three OR cholot-post-four
        ├── Featured images
        ├── Post titles
        ├── Meta information
        └── Read more buttons
```

### 7. Contact Section Pattern
```
Section (background image with overlay)
├── Column (content description)
│   ├── cholot-title
│   ├── divider
│   └── text-editor
└── Column (contact form)
    └── cholot-contact
        └── Contact Form 7 shortcode
```

### 8. Header/Footer Pattern
```
Section (header/footer styling)
├── Column (logo - 25%)
│   └── cholot-logo
├── Column (menu - 50%)
│   └── cholot-menu
└── Column (button - 25%)
    └── cholot-button-text
```

---

## Reusable Component Structures

### Icon-Text Component (cholot-texticon)
**Most versatile component - used in 37 instances**

```json
{
  "widgetType": "cholot-texticon",
  "common_structure": {
    "icon_area": {
      "selected_icon": "FontAwesome icon",
      "icon_size": "15px | 20px | larger",
      "icon_color": "#ffffff",
      "icon_background": "#b68c2f | transparent",
      "icon_border": "optional styling"
    },
    "content_area": {
      "subtitle": "UPPERCASE CATEGORY",
      "title": "Main Heading Text",
      "text": "Descriptive content paragraph"
    },
    "layout_options": {
      "icon_position": "top | left | right",
      "alignment": "left | center | right",
      "spacing": "custom margins and padding"
    }
  }
}
```

### Title Component (cholot-title)
**Standard heading component with accent spans**

```json
{
  "widgetType": "cholot-title",
  "pattern": {
    "title": "Main text <span>accent text</span>",
    "header_size": "h1 | h2 | h3 | h4 | h5 | h6",
    "styling": {
      "main_color": "#000000 | #ffffff",
      "accent_color": "#b68c2f | theme accent",
      "typography": "Playfair Display | Source Sans Pro"
    }
  }
}
```

### Service Card Pattern
**Commonly used 3-card layout**

```json
{
  "section_structure": {
    "background": "#b68c2f | theme color",
    "columns": 3,
    "column_content": {
      "background_image": "service related image",
      "overlay": {
        "widget": "cholot-texticon",
        "icon": "service specific FontAwesome",
        "content": "service description",
        "styling": "card-like appearance"
      }
    }
  }
}
```

---

## Common CDATA and JSON Encoding Patterns

### Elementor Data Structure
```xml
<wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
<wp:meta_value><![CDATA[
[
  {
    "id": "unique_id",
    "elType": "section",
    "settings": { section_settings },
    "elements": [
      {
        "id": "column_id", 
        "elType": "column",
        "settings": { column_settings },
        "elements": [
          {
            "id": "widget_id",
            "elType": "widget",
            "widgetType": "cholot-[widget-name]",
            "settings": { widget_settings },
            "elements": []
          }
        ]
      }
    ]
  }
]
]]></wp:meta_value>
```

### Widget Settings Pattern
```json
{
  "responsive_settings": {
    "setting_name": {"unit": "px", "size": 15, "sizes": []},
    "setting_name_tablet": {"unit": "px", "size": 12, "sizes": []},
    "setting_name_mobile": {"unit": "px", "size": 10, "sizes": []}
  },
  "spacing_settings": {
    "margin": {
      "unit": "px",
      "top": "0", "right": "0", "bottom": "0", "left": "0",
      "isLinked": false
    }
  },
  "typography_settings": {
    "typography_typography": "custom",
    "typography_font_size": {"unit": "px", "size": 16, "sizes": []},
    "typography_font_weight": "400 | 700 | 900",
    "typography_text_transform": "none | uppercase | lowercase"
  }
}
```

---

## Widget Parameter Requirements

### Required vs Optional Parameters

#### cholot-texticon
**Required:**
- `title` - Main heading text
- `selected_icon` - FontAwesome icon object

**Optional but Common:**
- `subtitle` - Category/subheading
- `text` - Description content
- `icon_size` - Icon dimensions
- `title_color` - Text color
- `subtitle_color` - Accent color

#### cholot-team
**Required:**
- `title` - Team member name
- `text` - Job title/position
- `image` - Profile photo object

**Optional but Common:**
- `social_icon_list` - Social media links
- `hover_animation` - Animation effect
- `background_image` - Card background

#### cholot-gallery
**Required:**
- `gallery` - Array of image objects
- `port_column` - Grid layout class

**Optional:**
- `gallery_height` - Image height
- `gallery_margin` - Spacing between images
- `title_show` - Show image titles
- `caption_show` - Show image captions

---

## Default Values and Settings

### Color Defaults
```css
:root {
  --cholot-primary: #b68c2f;
  --cholot-dark: #1f1f1f;
  --cholot-light: #fafafa;
  --cholot-white: #ffffff;
  --cholot-overlay: rgba(0,0,0,0.61);
}
```

### Typography Defaults
```css
.cholot-title {
  font-family: 'Playfair Display', serif;
  font-size: 35px;
  line-height: 1.1em;
  font-weight: 700;
}

.cholot-subtitle {
  font-family: 'Source Sans Pro', sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #b68c2f;
}

.cholot-body {
  font-family: 'Source Sans Pro', sans-serif;
  font-size: 15px;
  font-weight: 400;
  line-height: 1.6em;
}
```

### Spacing Defaults
```css
.cholot-section {
  padding: 60px 0;
}

.cholot-column {
  padding: 15px;
}

.cholot-widget {
  margin-bottom: 30px;
}

.cholot-icon {
  width: 35px;
  height: 35px;
  font-size: 15px;
}
```

---

## Advanced Layout Patterns

### Multi-Column Service Grid
```
Section
├── Column (25%) - Service 1
│   ├── Background Image
│   └── cholot-texticon overlay
├── Column (25%) - Service 2  
│   ├── Video background
│   └── cholot-texticon overlay
├── Column (25%) - Service 3
│   ├── Background Image  
│   └── cholot-texticon overlay
└── Column (25%) - Service 4
    ├── Background Image
    └── cholot-texticon overlay
```

### Content + Sidebar Layout
```
Section
├── Column (66%) - Main Content
│   ├── cholot-title
│   ├── cholot-text-line (multiple)
│   └── cholot-contact
└── Column (33%) - Sidebar
    ├── cholot-sidebar
    ├── cholot-post-three
    └── cholot-gallery
```

### Alternating Content Layout
```
Section 1 (Image Left, Content Right)
├── Column (50%) - Image
└── Column (50%) - Content

Section 2 (Content Left, Image Right)  
├── Column (50%) - Content
└── Column (50%) - Image
```

This hierarchical structure shows how Cholot widgets work together to create cohesive, professional-looking pages for retirement community websites.