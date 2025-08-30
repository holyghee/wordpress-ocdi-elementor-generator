# YAML Processor Examples

This directory contains practical examples demonstrating the flexibility and power of our YAML-to-WordPress processor. Each example shows how the same system can create completely different types of websites by simply changing the YAML configuration.

## 📁 Available Examples

### 1. Simple Example (`simple_example.yaml`)
**Use Case:** Minimal single-page website  
**Demonstrates:** Basic YAML structure, essential sections  
**Perfect for:** Personal sites, landing pages, portfolios  

**Features:**
- Hero section with call-to-action buttons
- About section with text content
- Contact form with basic fields
- Clean, minimal design
- SEO optimization

**Sections:** Hero, Content, Contact  
**Complexity:** ⭐ (Beginner)

### 2. Service Company (`service_company.yaml`)
**Use Case:** Professional IT consulting company  
**Demonstrates:** Complex business website structure  
**Perfect for:** Service businesses, consultancies, agencies  

**Features:**
- Multiple service cards with detailed information
- Team member profiles with social links
- Client testimonials carousel
- Pricing tables with comparison
- Statistics/achievements section
- Multi-level navigation with dropdowns
- Advanced contact forms with service selection

**Sections:** Hero, Services, Stats, Team, Testimonials, Pricing, CTA, Contact  
**Complexity:** ⭐⭐⭐⭐ (Advanced)

### 3. Restaurant Example (`restaurant_example.yaml`)
**Use Case:** Full-service restaurant website  
**Demonstrates:** Industry-specific features and layouts  
**Perfect for:** Restaurants, cafes, food services  

**Features:**
- Categorized menu with prices and dietary info
- Image gallery with multiple categories
- Online reservation system
- Special events and offers
- Wine list integration
- Chef and restaurant story
- Location with map integration
- Social media feeds
- Loyalty program integration

**Sections:** Hero, Story, Menu, Gallery, Reviews, Events, Reservations, Contact  
**Complexity:** ⭐⭐⭐⭐⭐ (Expert)

## 🚀 How to Use These Examples

### Quick Start
```bash
# Process all examples at once
php run_examples.php

# Or process individual examples
./process_example.sh simple
./process_example.sh service
./process_example.sh restaurant
```

### Step-by-Step Processing
```bash
# 1. Navigate to the examples directory
cd examples/

# 2. Run the demonstration script
php run_examples.php

# 3. Check the generated output
ls -la output/

# 4. Process with actual YAML processor (if available)
php ../yaml_processor.php simple_example.yaml
```

## 📋 What Each Example Demonstrates

| Feature | Simple | Service | Restaurant |
|---------|---------|---------|------------|
| Basic sections | ✅ | ✅ | ✅ |
| Navigation menu | ✅ | ✅ | ✅ |
| Contact forms | ✅ | ✅ | ✅ |
| Service/product cards | ❌ | ✅ | ✅ (Menu items) |
| Team members | ❌ | ✅ | ✅ (Chef) |
| Testimonials | ❌ | ✅ | ✅ |
| Pricing tables | ❌ | ✅ | ❌ |
| Gallery | ❌ | ❌ | ✅ |
| Events/specials | ❌ | ❌ | ✅ |
| Reservations | ❌ | ❌ | ✅ |
| Social integration | ❌ | ✅ | ✅ |
| SEO optimization | ✅ | ✅ | ✅ |
| Analytics | ❌ | ✅ | ✅ |

## 🎨 Customization Examples

Each YAML file includes extensive comments explaining:

- **Configuration options**: What each setting does
- **Section types**: Available section types and their properties
- **Layout options**: Different ways to display content
- **Theme settings**: Colors, fonts, and styling options
- **Integration options**: Third-party services and APIs

## 🔧 Processing Commands

### Using the YAML Processor Directly
```bash
# Basic processing
php yaml_processor.php examples/simple_example.yaml

# With custom output directory
php yaml_processor.php examples/service_company.yaml output/my_service_site/

# Process restaurant example
php yaml_processor.php examples/restaurant_example.yaml themes/bella_vista/
```

### Using Convenience Scripts
```bash
# Process all examples
./examples/process_example.sh

# Process specific example
./examples/process_example.sh simple
./examples/process_example.sh service
./examples/process_example.sh restaurant
```

## 📂 Generated File Structure

Each processed example creates:

```
output/example_name/
├── index.php           # Main theme template
├── style.css          # Theme styles with YAML colors/fonts
├── functions.php      # WordPress theme functions
├── README.md          # Instructions for the generated theme
└── assets/           # Generated assets (if any)
    ├── js/
    └── css/
```

## 💡 Learning Path

**For Beginners:**
1. Start with `simple_example.yaml`
2. Understand the basic structure
3. Modify colors and content
4. Process and see the results

**For Intermediate Users:**
1. Study `service_company.yaml`
2. Learn about complex sections
3. Understand navigation structures
4. Experiment with different layouts

**For Advanced Users:**
1. Examine `restaurant_example.yaml`
2. Study industry-specific features
3. Learn about integrations
4. Create your own complex configurations

## 🔍 Key Concepts Demonstrated

### YAML Structure
- **Global settings**: Site name, description, theme
- **Navigation**: Menus, dropdowns, icons
- **Sections**: Different content types and layouts
- **SEO**: Meta tags, structured data
- **Integrations**: Third-party services

### Section Types
- `hero` - Landing/banner sections
- `content` - Text content blocks
- `services` - Service/product cards
- `team` - Staff/team member profiles
- `testimonials` - Customer reviews
- `pricing` - Pricing tables
- `gallery` - Image galleries
- `menu` - Restaurant menus (industry-specific)
- `contact` - Contact forms and information
- `cta` - Call-to-action sections

### Flexibility Examples
- Same `contact` section works for all website types
- `services` becomes `menu items` for restaurants
- `team` becomes `chef profile` for restaurants
- Theme colors adapt to industry (blue for tech, red for restaurants)

## 🚀 Next Steps

1. **Examine the YAML files** - Read through each example to understand the structure
2. **Run the demonstrations** - Process the examples to see the output
3. **Modify and experiment** - Change colors, content, and sections
4. **Create your own** - Use these as templates for your own projects

## 📞 Support

If you have questions about these examples or need help with your own YAML configurations:

1. Check the comments in each YAML file
2. Review the generated README files
3. Compare similar sections across different examples
4. Start with simple modifications before complex changes

---

*These examples showcase the power and flexibility of YAML-driven website generation. The same processor creates a simple landing page, a complex business site, and a feature-rich restaurant website - all from declarative YAML configuration.*