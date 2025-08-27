# Cholot Widgets Quick Reference Guide

## Widget List & Usage Count

| Widget | Count | Primary Use | Required Settings |
|--------|-------|-------------|-------------------|
| **cholot-texticon** | 37 | Icon + Text blocks | `title`, `selected_icon` |
| **cholot-title** | 47 | Section headings | `title` |
| **cholot-text-line** | 24 | Text with lines | `title` |
| **cholot-team** | 12 | Staff profiles | `title`, `text`, `image` |
| **cholot-button-text** | 10 | CTA buttons | `btn_text`, `link` |
| **cholot-contact** | 8 | Contact forms | `shortcode` |
| **cholot-testimonial-two** | 6 | Customer reviews | `testi_list` |
| **cholot-gallery** | 3 | Image grids | `gallery`, `port_column` |
| **cholot-post-four** | 2 | Blog 2-col | `blog_post`, `blog_column` |
| **cholot-logo** | 2 | Site logos | `logo_img` |
| **cholot-menu** | 2 | Navigation | `cholot_menu` |
| **cholot-sidebar** | 2 | Sidebar content | `width` |
| **cholot-post-three** | 1 | Blog 1-col | `blog_post`, `blog_column` |

## Color Palette

```css
--primary-accent: #b68c2f    /* Golden brown - used throughout */
--dark-primary: #1f1f1f      /* Dark backgrounds */
--light-bg: #f4f4f4          /* Light section backgrounds */
--white: #ffffff             /* Text and overlays */
--overlay-dark: rgba(0,0,0,0.61)  /* Image overlays */
```

## Typography Stack

```css
/* Headings */
font-family: 'Playfair Display', serif;
font-weight: 700;
font-size: 35px (desktop), 25px (mobile);

/* Body Text */
font-family: 'Source Sans Pro', sans-serif;
font-weight: 400;
font-size: 15px;

/* Subtitles/Meta */
font-family: 'Source Sans Pro', sans-serif;
font-weight: 700;
text-transform: uppercase;
font-size: 13px;
letter-spacing: 1px;
```

## Common Icon Types (FontAwesome)

| Icon | Usage | Widget |
|------|-------|--------|
| `fas fa-crown` | Premium services | texticon |
| `fas fa-procedures` | Healthcare | texticon |
| `fas fa-people-carry` | Community support | texticon |
| `fas fa-chair` | Amenities | button-text |
| `fas fa-feather-alt` | Decorative | team |

## Standard Spacing

```css
Section Padding: 60px (top/bottom)
Column Margin: 15px
Widget Margin: 30px (bottom)
Icon Size: 15px (small), 35px (medium), 72px (large)
Border Width: 1px, 2px, 3px
```

## Responsive Breakpoints

- **Desktop**: Default settings
- **Tablet**: `_tablet` suffix settings, often 50% width
- **Mobile**: `_mobile` suffix settings, typically 100% width

## Most Common Patterns

### 1. Feature Section (3-column)
```
Section (background: #b68c2f)
├── Column (33%) - cholot-texticon
├── Column (33%) - cholot-texticon  
└── Column (33%) - cholot-texticon
```

### 2. Content Section
```
Section
├── Column (50%)
│   ├── cholot-title
│   ├── divider
│   └── text-editor
└── Column (50%)
    └── image
```

### 3. Team Section
```
Section (shape divider)
├── Column (33%) - cholot-team
├── Column (33%) - cholot-team
└── Column (33%) - cholot-team
```

## Widget-Specific Quick Notes

### cholot-texticon
- **Most versatile** - used 37 times
- Supports left/right icon positioning
- Icon background can be transparent or colored
- Text content supports HTML

### cholot-title  
- **Most frequent** - used 47 times
- Use `<span>` tags for accent colors
- Supports h1-h6 heading levels
- Responsive font sizing

### cholot-team
- **Hover animation**: "shrink" is default
- **Social icons**: Facebook, Twitter, Instagram, LinkedIn
- **Background images** with overlay effects
- Profile images with custom borders

### cholot-gallery
- **Grid options**: `col-md-4` (3-col), `col-md-6` (2-col)
- **Image arrays** with ID and URL
- Responsive height adjustments

### cholot-button-text
- **Dual text**: Main button text + subtitle
- **Icon positioning**: Left or right
- **Hover effects** on colors and backgrounds

## File Structure

```
/demo-data-fixed.xml              # Source XML file
/cholot_widget_analyzer.py        # Analysis script  
/cholot_widgets_catalog.json      # Complete JSON catalog
/CHOLOT_WIDGETS_ANALYSIS.md       # Full documentation
/CHOLOT_COMPONENT_HIERARCHY.md    # Layout patterns
/QUICK_REFERENCE.md               # This file
```

## Key Insights

1. **Design System**: Consistent color palette and typography across all widgets
2. **Responsive First**: All widgets include mobile-specific settings
3. **FontAwesome Integration**: Heavy use of Font Awesome 5 icons
4. **Retirement Theme**: Optimized for senior living/retirement communities
5. **Professional Polish**: Hover effects, animations, and shadows throughout

## JSON Structure Template

```json
{
  "id": "unique_id",
  "elType": "widget",
  "widgetType": "cholot-[name]",
  "settings": {
    "setting_name": "value",
    "responsive_setting": {
      "unit": "px",
      "size": 15,
      "sizes": []
    },
    "spacing_setting": {
      "unit": "px", 
      "top": "0", "right": "0", "bottom": "0", "left": "0",
      "isLinked": false
    }
  },
  "elements": []
}
```

This analysis provides everything needed to understand, implement, and extend the Cholot theme's Elementor widget system.