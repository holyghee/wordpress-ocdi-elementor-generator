---
title: "Modern Architecture Firm"
description: "Award-winning architectural design and construction services"
base_url: "http://localhost:8082"
language: "en-US"
theme: "cholot"

# Page Configuration
pages:
  - title: "Home" 
    slug: "home"
    template: "home-page"
    sections:
      # Hero Section
      - type: "hero"
        background_image: "http://localhost:8082/architecture-hero.jpg"
        background_color: "#232323"
        widgets:
          - type: "texticon"
            title: "Modern Architecture Studio"
            subtitle: "Design • Build • Inspire"
            icon: "fas fa-compass-drafting"
            text: "Creating exceptional spaces that inspire and endure"
            settings:
              title_size: 48
              subtitle_transform: "uppercase"
              
      # Services Overview
      - type: "services"
        background_color: "#f8f8f8"
        structure: "33"
        widgets:
          - type: "text-line"
            title: "Residential Design"
            subtitle: "Custom Homes"
            line_width: 70
          - type: "text-line"  
            title: "Commercial Projects"
            subtitle: "Office & Retail"
            line_width: 70
          - type: "text-line"
            title: "Interior Design"
            subtitle: "Complete Solutions"
            line_width: 70
            
      # Featured Projects
      - type: "portfolio"
        widgets:
          - type: "gallery"
            columns: "col-md-6"
            height: 300
            images:
              - "http://localhost:8082/projects/modern-house-1.jpg"
              - "http://localhost:8082/projects/office-building-1.jpg"  
              - "http://localhost:8082/projects/interior-design-1.jpg"
              - "http://localhost:8082/projects/residential-complex-1.jpg"
              
  - title: "About"
    slug: "about"
    sections:
      - type: "intro"
        widgets:
          - type: "title"
            title: "About Our Studio<span>.</span>"
            header_size: "h1"
            align: "center"
            
      - type: "content"
        structure: "50"
        widgets:
          - type: "text-line"
            title: "Our Philosophy"
            subtitle: "Design Excellence"
            content: |
              We believe that great architecture emerges from the careful balance 
              of functionality, sustainability, and aesthetic beauty. Our designs 
              reflect the unique needs of each client while respecting the 
              environment and community context.
              
          - type: "team"
            name: "Maria Rodriguez"
            position: "Principal Architect"
            image_url: "http://localhost:8082/team/maria-rodriguez.jpg"
            bio: |
              With over 15 years of experience in modern architecture, 
              Maria leads our design team with passion and expertise.
            social_links:
              - platform: "linkedin"
                url: "https://linkedin.com/in/mariarodriguez"
              - platform: "instagram" 
                url: "https://instagram.com/maria_architect"
                
# Navigation Menu
navigation:
  - title: "Home"
    url: "/"
  - title: "Projects"
    url: "/projects/"
  - title: "Services"
    url: "/services/"
  - title: "About"
    url: "/about/"
  - title: "Contact"
    url: "/contact/"

# Site Settings
settings:
  logo_url: "http://localhost:8082/logo-architecture.png"
  primary_color: "#b68c2f"
  secondary_color: "#232323"
  font_family: "Source Sans Pro"
---

# Modern Architecture Studio

We are a contemporary architecture firm specializing in innovative design solutions that blend functionality with aesthetic excellence. Our portfolio spans residential, commercial, and public projects, each crafted with meticulous attention to detail and environmental consciousness.

## Our Services

### Architectural Design
From initial concept to final construction drawings, we provide comprehensive architectural design services tailored to your vision and budget.

### Interior Design  
Complete interior design solutions that seamlessly integrate with architectural elements, creating cohesive and inspiring spaces.

### Project Management
Full project oversight ensuring quality execution, timeline adherence, and budget management throughout the construction process.

### Sustainable Design
Environmentally conscious design approaches that minimize environmental impact while maximizing energy efficiency and occupant comfort.

## Why Choose Us

- **Award-Winning Designs**: Recognized for excellence in modern architecture
- **Sustainable Approach**: Committed to environmentally responsible design
- **Client-Focused**: Collaborative process ensuring your vision becomes reality
- **Expert Team**: Licensed professionals with decades of combined experience

## Recent Projects

Our recent work includes a variety of project types, from luxury residential homes to innovative commercial spaces. Each project reflects our commitment to design excellence and client satisfaction.

Contact us today to discuss your next architectural project and discover how we can bring your vision to life.