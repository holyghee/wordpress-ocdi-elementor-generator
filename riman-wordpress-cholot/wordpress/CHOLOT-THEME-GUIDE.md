# Cholot Theme Widget Guide

Complete documentation for all 13 Cholot WordPress theme widgets. This guide provides detailed configuration options, examples, and best practices for each widget type.

## 🎨 Theme Overview

**Cholot** is a premium WordPress theme designed for retirement communities, healthcare facilities, and senior living organizations. It features:

- **Primary Color**: #b68c2f (Golden)
- **Typography**: Source Sans Pro, custom weight variations
- **Design Philosophy**: Clean, professional, accessible
- **Target Audience**: Senior communities, healthcare providers
- **Layout**: Responsive, mobile-first approach

## 📋 Complete Widget Catalog

### 1. cholot-texticon
**Purpose**: Display text content with decorative icons and structured typography.

#### Required Parameters
- `title` (string): Main heading text
- `icon` (string): FontAwesome icon class (e.g., "fas fa-home")

#### Optional Parameters
- `subtitle` (string): Subheading text
- `text` (string): Body content (HTML allowed)
- `custom_settings` (object): Override default styling

#### Example Configuration
```yaml
- type: "texticon"
  title: "Premium Healthcare"
  subtitle: "Excellence in Care"
  icon: "fas fa-heart-pulse"
  text: "<p>Professional medical services available 24/7 with qualified staff.</p>"
  custom_settings:
    title_color: "#ffffff"
    subtitle_color: "#b68c2f"
    text_color: "#b68c2f"
    icon_size: {"unit": "px", "size": 20, "sizes": []}
```

#### Default Styling
- Title: 24px, white color, custom typography
- Subtitle: 13px, bold, uppercase, golden color (#b68c2f)
- Icon: 15px size, 35px background
- Text: 13px, uppercase, golden color

#### Common Use Cases
- Service descriptions
- Feature highlights
- Benefits lists
- Introduction sections

---

### 2. cholot-title
**Purpose**: Styled headings with optional span elements for accent colors.

#### Required Parameters
- `title` (string): Heading text (can include `<span>` tags)

#### Optional Parameters
- `header_size` (string): HTML tag ("h1", "h2", "h3", etc.)
- `align` (string): Text alignment ("left", "center", "right")
- `responsive` (object): Tablet/mobile specific alignment

#### Example Configuration
```yaml
- type: "title"
  title: "About Our <span>Community</span>"
  header_size: "h2"
  align: "center"
  responsive:
    tablet: "left"
  custom_settings:
    span_title_color: "#b68c2f"
    desc_typography_font_size: {"unit": "px", "size": 28, "sizes": []}
```

#### Styling Features
- Supports span elements for accent colors
- Responsive alignment options
- Custom typography controls
- Header size flexibility (h1-h6)

#### Common Use Cases
- Section headings
- Page titles
- Content dividers
- Accent text

---

### 3. cholot-button-text
**Purpose**: Call-to-action buttons with subtitle support and icon integration.

#### Required Parameters
- `text` (string): Button text
- `url` (string): Link destination

#### Optional Parameters
- `subtitle` (string): Secondary text below button
- `icon` (string): FontAwesome icon class
- `icon_align` (string): Icon position ("left", "right")
- `external` (boolean): Open in new tab

#### Example Configuration
```yaml
- type: "button-text"
  text: "Schedule Tour"
  subtitle: "Call us today"
  url: "https://example.com/contact"
  icon: "fas fa-calendar-alt"
  icon_align: "right"
  external: true
  custom_settings:
    btn_bg: "#b68c2f"
    btn_bg_hover: "#000000"
    btn_color: "#ffffff"
    btn_typography_font_size: {"unit": "px", "size": 18, "sizes": []}
```

#### Styling Options
- Background colors (normal and hover states)
- Text colors (normal and hover states)
- Typography controls
- Icon styling and positioning
- Padding and margin controls

#### Common Use Cases
- Contact buttons
- Appointment scheduling
- Information requests
- Navigation links

---

### 4. cholot-team
**Purpose**: Team member profiles with photos, social links, and background effects.

#### Required Parameters
- `name` (string): Team member name
- `position` (string): Job title or role
- `image_url` (string): Profile photo URL

#### Optional Parameters
- `image_id` (integer): WordPress media ID
- `height` (string): Container height (default: "420px")
- `align` (string): Content alignment ("left", "center", "right")
- `animation` (string): Hover effect ("shrink", "grow", etc.)
- `social_links` (array): Social media profiles

#### Example Configuration
```yaml
- type: "team"
  name: "Dr. Sarah Johnson"
  position: "Medical Director"
  image_url: "https://demo.ridianur.com/wp-content/uploads/team1.jpg"
  height: "450px"
  align: "center"
  animation: "shrink"
  social_links:
    - icon: "fab fa-facebook"
      url: "https://facebook.com/drsarahjohnson"
    - icon: "fab fa-linkedin"
      url: "https://linkedin.com/in/sarahjohnson"
    - icon: "fab fa-twitter"
      url: "https://twitter.com/drsarahjohnson"
```

#### Advanced Features
- Mask overlay effects
- Background image support
- Social icon styling
- Hover animations
- Responsive image positioning

#### Common Use Cases
- Staff directories
- Leadership teams
- Medical professionals
- Department heads

---

### 5. cholot-testimonial-two
**Purpose**: Customer testimonial slider with photos and ratings.

#### Required Parameters
- `testimonials` (array): List of testimonial objects

#### Optional Parameters
- `columns` (integer): Desktop display columns (default: 3)
- `align` (string): Content alignment
- `responsive` (object): Mobile/tablet settings

#### Example Configuration
```yaml
- type: "testimonial"
  columns: 2
  align: "center"
  testimonials:
    - name: "Margaret Smith"
      position: "Resident since 2019"
      image_url: "https://demo.ridianur.com/testimonial1.jpg"
      content: "The care here is exceptional. Staff is always available and friendly."
    - name: "Robert Chen"
      position: "Family Member"
      image_url: "https://demo.ridianur.com/testimonial2.jpg"
      content: "My mother loves living here. The activities and community are wonderful."
  responsive:
    mobile:
      title_size: 15
      name_size: 16
```

#### Testimonial Object Structure
Each testimonial should include:
- `name`: Person's name
- `position`: Title or relationship
- `content`: Testimonial text
- `image_url`: Photo URL
- `rating` (optional): Star rating

#### Common Use Cases
- Customer reviews
- Family feedback
- Resident testimonials
- Service endorsements

---

### 6. cholot-gallery
**Purpose**: Image galleries with grid layouts and lightbox functionality.

#### Required Parameters
- `images` (array): List of image URLs or objects
- `columns` (string): Bootstrap column class ("col-md-4", "col-md-6")

#### Optional Parameters
- `height` (integer): Image height in pixels
- `margin` (number): Spacing between images
- `show_title` (boolean): Display image titles
- `show_caption` (boolean): Display image captions
- `responsive` (object): Mobile/tablet specific settings

#### Example Configuration
```yaml
- type: "gallery"
  columns: "col-md-4"
  height: 300
  margin: 10
  show_title: false
  show_caption: false
  images:
    - url: "https://demo.ridianur.com/gallery/image1.jpg"
      id: 101
      title: "Community Garden"
    - url: "https://demo.ridianur.com/gallery/image2.jpg"
      id: 102
      title: "Dining Hall"
    - url: "https://demo.ridianur.com/gallery/image3.jpg"
      id: 103
      title: "Recreation Room"
  responsive:
    tablet:
      height: 200
      margin: 5
```

#### Layout Options
- `col-md-12`: Single column (1 per row)
- `col-md-6`: Two columns (2 per row)
- `col-md-4`: Three columns (3 per row)
- `col-md-3`: Four columns (4 per row)

#### Common Use Cases
- Facility photos
- Activity galleries
- Before/after showcases
- Portfolio displays

---

### 7. cholot-post-three
**Purpose**: Blog post display in single-column layout with meta information.

#### Required Parameters
- `post_count` (integer): Number of posts to display
- `column` (string): Layout type ("one" for single column)

#### Optional Parameters
- `categories` (array): Filter by category IDs
- `show_excerpt` (boolean): Display post excerpts
- `excerpt_after` (string): Text after excerpt (default: "...")
- `button_text` (string): Read more button text

#### Example Configuration
```yaml
- type: "post-three"
  post_count: 3
  column: "one"
  categories: [1, 5, 8]
  show_excerpt: true
  excerpt_after: "Read more..."
  button_text: "Continue Reading"
  custom_settings:
    title_typo_font_size: {"unit": "px", "size": 16, "sizes": []}
    meta_color: "#b68c2f"
```

#### Meta Information Displayed
- Publication date
- Author name
- Category tags
- Comment count (if enabled)

#### Common Use Cases
- Latest news
- Blog highlights
- Announcements
- Activity updates

---

### 8. cholot-post-four
**Purpose**: Blog post display in two-column grid layout.

#### Required Parameters
- `post_count` (integer): Number of posts to display
- `column` (string): Layout type ("two" for grid)

#### Optional Parameters
- `excerpt_length` (integer): Number of excerpt words
- `show_pagination` (boolean): Display pagination controls
- `categories` (array): Filter by category IDs

#### Example Configuration
```yaml
- type: "post-four"
  post_count: 6
  column: "two"
  excerpt_length: 120
  show_pagination: true
  categories: [2, 4]
  custom_settings:
    content_bg: "#f8f8f8"
    title_typo_font_size: {"unit": "px", "size": 18, "sizes": []}
```

#### Grid Features
- Responsive grid layout
- Featured image support
- Excerpt text with custom length
- Pagination controls
- Category filtering

#### Common Use Cases
- News archives
- Blog listings
- Event summaries
- Resource libraries

---

### 9. cholot-contact
**Purpose**: Contact forms with custom styling and integration support.

#### Required Parameters
- `shortcode` (string): Contact Form 7 shortcode

#### Optional Parameters
- `button_width` (string): Submit button width (default: "100%")
- `custom_settings` (object): Style overrides

#### Example Configuration
```yaml
- type: "contact"
  shortcode: '[contact-form-7 id="1" title="Contact Form"]'
  button_width: "200px"
  custom_settings:
    btn_bg: "#b68c2f"
    btn_color: "#ffffff"
    form_bg: "rgba(0,0,0,0)"
    form_border_color: "#ffffff"
    form_text: "#ffffff"
```

#### Styling Options
- Button colors (background, text, border)
- Form field appearance
- Placeholder text styling
- Border and background colors
- Responsive width controls

#### Integration Notes
- Requires Contact Form 7 plugin
- Supports custom form styling
- Works with form validation
- Email integration ready

#### Common Use Cases
- Contact pages
- Inquiry forms
- Appointment requests
- Information gathering

---

### 10. cholot-text-line
**Purpose**: Text content with decorative line elements and background images.

#### Required Parameters
- `title` (string): Main heading text

#### Optional Parameters
- `subtitle` (string): Subheading text
- `line_width` (integer): Decorative line width in pixels
- `line_height` (integer): Line thickness in pixels
- `background_color` (string): Background color
- `background_image` (string): Background image URL

#### Example Configuration
```yaml
- type: "text-line"
  title: "Excellence in Senior Care"
  subtitle: "Our Promise"
  line_width: 80
  line_height: 3
  background_color: "#f5f5f5"
  background_image: "https://demo.ridianur.com/patterns/bg-pattern.png"
  custom_settings:
    title_typography_font_size: {"unit": "px", "size": 32, "sizes": []}
    subtitle_color: "#b68c2f"
    line_color_hover: "#b68c2f"
```

#### Visual Features
- Decorative line elements
- Background image support
- Color transitions on hover
- Typography controls
- Spacing customization

#### Common Use Cases
- Section dividers
- Feature highlights
- Mission statements
- Value propositions

---

### 11. cholot-logo
**Purpose**: Site logo display with alignment and sizing options.

#### Required Parameters
- `url` (string): Logo image URL

#### Optional Parameters
- `id` (integer): WordPress media ID
- `align` (string): Logo alignment ("left", "center", "right")
- `height` (string): Logo height (default: "70px")

#### Example Configuration
```yaml
- type: "logo"
  url: "https://demo.ridianur.com/logo-white.png"
  id: 659
  align: "center"
  height: "80px"
```

#### Features
- Responsive sizing
- Flexible alignment
- Retina display support
- Link functionality (to homepage)

#### Common Use Cases
- Header logos
- Footer branding
- Partner logos
- Certification badges

---

### 12. cholot-menu
**Purpose**: WordPress navigation menus with mobile responsive design.

#### Required Parameters
- `menu_name` (string): WordPress menu slug

#### Optional Parameters
- `align` (string): Menu alignment
- `mobile_menu` (string): Mobile display style
- `desktop_tablet` (string): Tablet display behavior

#### Example Configuration
```yaml
- type: "menu"
  menu_name: "main-menu"
  align: "right"
  mobile_menu: "hamburger"
  desktop_tablet: "none"
  custom_settings:
    menu_color: "#ffffff"
    menu_color_hover: "#b68c2f"
    menu_typo_font_weight: "700"
```

#### Menu Features
- Dropdown support
- Mobile hamburger menu
- Hover effects
- Typography controls
- Color customization

#### Common Use Cases
- Primary navigation
- Footer menus
- Mobile navigation
- Secondary menus

---

### 13. cholot-sidebar
**Purpose**: Sidebar content areas with custom width control.

#### Required Parameters
- `width` (string): Sidebar width (e.g., "33px", "300px")

#### Optional Parameters
- `custom_settings` (object): Additional styling

#### Example Configuration
```yaml
- type: "sidebar"
  width: "350px"
  custom_settings:
    title_typography_font_size: {"unit": "px", "size": 18, "sizes": []}
```

#### Features
- Flexible width control
- Typography customization
- Content area support
- Widget integration

#### Common Use Cases
- Blog sidebars
- Information panels
- Navigation areas
- Advertisement spaces

## 🎯 Template Usage Examples

### Complete Page Template
```yaml
site:
  title: "Sunset Senior Living"
  description: "Premium retirement community"
  base_url: "https://sunsetseniorliving.com"

pages:
  - title: "Home"
    slug: "home"
    template: "elementor_canvas"
    
    sections:
      # Header Section
      - structure: "50,50"
        columns:
          - width: 50
            widgets:
              - type: "logo"
                url: "https://demo.ridianur.com/logo.png"
                align: "left"
          - width: 50
            widgets:
              - type: "menu"
                menu_name: "primary-menu"
                align: "right"
      
      # Hero Section
      - structure: "100"
        settings:
          background:
            _background_background: "classic"
            _background_image:
              url: "https://demo.ridianur.com/hero-bg.jpg"
        columns:
          - width: 100
            widgets:
              - type: "texticon"
                title: "Welcome to Sunset Senior Living"
                subtitle: "Your New Home"
                icon: "fas fa-home"
                text: "Experience luxury living in our beautiful community"
      
      # Services Section
      - structure: "33,33,33"
        columns:
          - width: 33
            widgets:
              - type: "texticon"
                title: "Medical Care"
                icon: "fas fa-heart-pulse"
                text: "24/7 professional medical support"
          - width: 33
            widgets:
              - type: "texticon"
                title: "Activities"
                icon: "fas fa-users"
                text: "Engaging social and recreational programs"
          - width: 33
            widgets:
              - type: "texticon"
                title: "Dining"
                icon: "fas fa-utensils"
                text: "Gourmet meals prepared by our chefs"
```

### Team Page Template
```yaml
pages:
  - title: "Our Team"
    slug: "team"
    
    sections:
      # Page Title
      - structure: "100"
        columns:
          - width: 100
            widgets:
              - type: "title"
                title: "Meet Our <span>Professional Team</span>"
                header_size: "h1"
                align: "center"
      
      # Team Members Grid
      - structure: "25,25,25,25"
        columns:
          - width: 25
            widgets:
              - type: "team"
                name: "Dr. Sarah Johnson"
                position: "Medical Director"
                image_url: "https://demo.ridianur.com/team1.jpg"
                social_links:
                  - icon: "fab fa-linkedin"
                    url: "https://linkedin.com/in/sarahjohnson"
          - width: 25
            widgets:
              - type: "team"
                name: "Michael Chen"
                position: "Activities Coordinator"
                image_url: "https://demo.ridianur.com/team2.jpg"
          - width: 25
            widgets:
              - type: "team"
                name: "Lisa Rodriguez"
                position: "Nursing Supervisor"
                image_url: "https://demo.ridianur.com/team3.jpg"
          - width: 25
            widgets:
              - type: "team"
                name: "David Wilson"
                position: "Facility Manager"
                image_url: "https://demo.ridianur.com/team4.jpg"
```

## 🔧 Advanced Configuration

### Color Scheme Customization
```yaml
# Override theme colors
custom_settings:
  primary_color: "#b68c2f"      # Cholot gold
  secondary_color: "#232323"    # Dark gray
  accent_color: "#ffffff"       # White
  text_color: "#878787"         # Light gray
  background_color: "#f4f4f4"   # Light background
```

### Typography System
```yaml
# Typography overrides
typography_settings:
  font_family: "Source Sans Pro"
  headings:
    h1: {"size": 48, "weight": "700"}
    h2: {"size": 36, "weight": "600"}
    h3: {"size": 24, "weight": "600"}
  body: {"size": 16, "weight": "400"}
  small: {"size": 13, "weight": "400"}
```

### Responsive Breakpoints
```yaml
# Responsive settings structure
responsive:
  desktop: 1200    # Large screens
  tablet: 768      # Tablets
  mobile: 480      # Mobile devices
```

### Spacing System
```yaml
# Standard spacing object
spacing_object:
  unit: "px"
  top: "20"
  right: "20"
  bottom: "20"
  left: "20"
  isLinked: true
```

## 🚀 Best Practices

### Content Strategy
1. **Hierarchy**: Use title widgets for clear content structure
2. **Consistency**: Maintain color scheme throughout
3. **Accessibility**: Provide alt text for images
4. **Mobile First**: Test on mobile devices first
5. **Performance**: Optimize images before use

### Design Guidelines
1. **White Space**: Use adequate spacing between elements
2. **Typography**: Limit to 2-3 font weights
3. **Colors**: Stick to the Cholot color palette
4. **Images**: Use high-quality, consistent imagery
5. **Navigation**: Keep menu structure simple

### Technical Considerations
1. **Image URLs**: Use accessible demo servers
2. **Widget Limits**: Don't exceed reasonable widget counts per page
3. **Template Types**: Use "elementor_canvas" for full-width layouts
4. **Meta Fields**: Include proper Elementor meta data
5. **Validation**: Always validate generated XML

## 🔍 Troubleshooting

### Common Widget Issues

**Problem**: Widget not displaying correctly
```yaml
# Solution: Check widget type name
- type: "texticon"  # ✅ Correct
- type: "text-icon" # ❌ Incorrect
```

**Problem**: Colors not applying
```yaml
# Solution: Use proper color format
custom_settings:
  title_color: "#ffffff"           # ✅ Hex format
  subtitle_color: "rgb(255,255,255)" # ❌ RGB not supported
```

**Problem**: Images not loading
```yaml
# Solution: Use accessible URLs
image_url: "https://demo.ridianur.com/image.jpg"  # ✅ Accessible
image_url: "https://localhost/image.jpg"          # ❌ Not accessible
```

### Widget-Specific Issues

**texticon**: Icon not showing
- Check FontAwesome class name
- Verify icon library is loaded
- Use "fas", "fab", or "far" prefixes

**team**: Social links not working
- Ensure proper URL format (include https://)
- Check icon names match social platforms
- Verify array structure

**gallery**: Images not in grid
- Check column class format ("col-md-4")
- Verify responsive settings
- Test with different image sizes

**contact**: Form not submitting
- Verify Contact Form 7 is installed
- Check shortcode ID matches created form
- Test form functionality separately

## 📚 Resources

### FontAwesome Icons
- **Website**: https://fontawesome.com/icons
- **Format**: "fas fa-icon-name" (solid), "fab fa-brand-name" (brands)
- **Usage**: Copy icon class directly into icon fields

### Bootstrap Grid System
- **Columns**: "col-md-12" (full), "col-md-6" (half), "col-md-4" (third)
- **Documentation**: Bootstrap grid system reference
- **Responsive**: Automatic mobile adaptation

### WordPress Integration
- **Menus**: Create in WordPress Admin → Appearance → Menus
- **Categories**: Manage in WordPress Admin → Posts → Categories
- **Contact Forms**: Requires Contact Form 7 plugin

## 📖 Examples Repository

All working examples are available in the `/templates/` directory:

1. `home-page.yaml` - Complete homepage with 8 sections
2. `about-page.yaml` - About page with team and testimonials
3. `contact-page.yaml` - Contact form with location info
4. `service-page.yaml` - Services overview with features
5. `blog-page.yaml` - Blog listing with sidebar
6. `single-service-1.yaml` - Individual service page
7. `single-service-2.yaml` - Alternative service layout

Each template demonstrates different widget combinations and best practices for the Cholot theme.

---

**Cholot Theme Widget Guide - Complete reference for building beautiful senior living websites! 🏡**