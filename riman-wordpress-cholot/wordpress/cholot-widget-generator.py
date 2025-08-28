#!/usr/bin/env python3
"""
Cholot Widget Generator
Verwendet die echte Cholot Theme Widget Library
"""

import json
from datetime import datetime

class CholotWidgetGenerator:
    """
    Generiert Elementor JSON mit echten Cholot Widgets
    """
    
    def __init__(self):
        self.load_cholot_library()
    
    def load_cholot_library(self):
        """
        Lädt die Cholot Widget Templates
        """
        self.cholot_widgets = {
            "cholot-service-card": {
                "template": {
                    "id": "service_card",
                    "elType": "widget",
                    "widgetType": "cholot-service-card",
                    "settings": {
                        "service_icon": {"value": "fa fa-shield", "library": "fa-solid"},
                        "service_title": "Service Title",
                        "service_description": "Service description text here...",
                        "service_image": {"url": "", "id": ""},
                        "card_style": "style-1",
                        "icon_color": "#e74c3c",
                        "title_color": "#232323",
                        "description_color": "#666666",
                        "card_background": "#ffffff",
                        "card_border_radius": {"unit": "px", "size": 10},
                        "card_padding": {"unit": "px", "top": 30, "right": 25, "bottom": 30, "left": 25},
                        "card_shadow": {
                            "horizontal": 0,
                            "vertical": 5,
                            "blur": 15,
                            "spread": 0,
                            "color": "rgba(0,0,0,0.1)"
                        },
                        "hover_animation": "float",
                        "button_text": "Learn More",
                        "button_link": {"url": "#", "is_external": "", "nofollow": ""},
                        "button_style": "primary"
                    }
                }
            },
            
            "cholot-hero-banner": {
                "template": {
                    "id": "hero_banner",
                    "elType": "widget", 
                    "widgetType": "cholot-hero-banner",
                    "settings": {
                        "hero_style": "style-1",
                        "hero_title": "Hero Title Here",
                        "hero_subtitle": "Hero subtitle text",
                        "hero_description": "Detailed hero description...",
                        "title_color": "#ffffff",
                        "subtitle_color": "rgba(255,255,255,0.9)",
                        "description_color": "rgba(255,255,255,0.8)",
                        "hero_background_type": "image",
                        "hero_background_image": {"url": "", "id": ""},
                        "hero_overlay": "yes",
                        "hero_overlay_color": "rgba(0,0,0,0.6)",
                        "content_alignment": "center",
                        "content_vertical_align": "middle",
                        "title_typography": {
                            "typography": "custom",
                            "font_family": "Playfair Display",
                            "font_size": {"unit": "px", "size": 54},
                            "font_weight": "700",
                            "line_height": {"unit": "em", "size": 1.2}
                        },
                        "cta_button_text": "Get Started",
                        "cta_button_link": {"url": "#contact"},
                        "cta_button_style": "primary",
                        "animation_type": "fadeInUp",
                        "animation_delay": "0.3s"
                    }
                }
            },
            
            "cholot-team-member": {
                "template": {
                    "id": "team_member",
                    "elType": "widget",
                    "widgetType": "cholot-team-member", 
                    "settings": {
                        "member_style": "style-1",
                        "member_image": {"url": "", "id": ""},
                        "member_name": "Team Member Name",
                        "member_position": "Position Title",
                        "member_bio": "Brief bio about the team member...",
                        "image_border_radius": {"unit": "%", "size": 50},
                        "name_color": "#232323",
                        "position_color": "#666666",
                        "bio_color": "#666666",
                        "card_background": "#ffffff",
                        "card_padding": {"unit": "px", "top": 30, "right": 20, "bottom": 30, "left": 20},
                        "social_links": [
                            {"platform": "linkedin", "url": "", "icon": "fab fa-linkedin"},
                            {"platform": "twitter", "url": "", "icon": "fab fa-twitter"},
                            {"platform": "email", "url": "", "icon": "fas fa-envelope"}
                        ],
                        "hover_animation": "zoom-in",
                        "image_hover_effect": "scale"
                    }
                }
            },
            
            "cholot-testimonial": {
                "template": {
                    "id": "testimonial",
                    "elType": "widget",
                    "widgetType": "cholot-testimonial",
                    "settings": {
                        "testimonial_style": "style-1", 
                        "testimonial_content": "Great service and professional team!",
                        "client_name": "Client Name",
                        "client_position": "Client Position",
                        "client_company": "Company Name",
                        "client_image": {"url": "", "id": ""},
                        "rating": 5,
                        "show_rating": "yes",
                        "content_color": "#666666",
                        "name_color": "#232323",
                        "position_color": "#666666",
                        "quote_icon": {"value": "fas fa-quote-left", "library": "fa-solid"},
                        "quote_color": "#e74c3c"
                    }
                }
            },
            
            "cholot-contact-info": {
                "template": {
                    "id": "contact_info",
                    "elType": "widget",
                    "widgetType": "cholot-contact-info",
                    "settings": {
                        "contact_style": "style-1",
                        "contact_items": [
                            {
                                "type": "address",
                                "icon": {"value": "fas fa-map-marker-alt", "library": "fa-solid"},
                                "label": "Address",
                                "value": "123 Business St, City, State 12345"
                            },
                            {
                                "type": "phone", 
                                "icon": {"value": "fas fa-phone", "library": "fa-solid"},
                                "label": "Phone",
                                "value": "+1 (555) 123-4567"
                            },
                            {
                                "type": "email",
                                "icon": {"value": "fas fa-envelope", "library": "fa-solid"},
                                "label": "Email", 
                                "value": "contact@company.com"
                            }
                        ],
                        "icon_color": "#e74c3c",
                        "label_color": "#232323",
                        "value_color": "#666666",
                        "item_spacing": {"unit": "px", "size": 20}
                    }
                }
            },
            
            "cholot-pricing-table": {
                "template": {
                    "id": "pricing_table",
                    "elType": "widget",
                    "widgetType": "cholot-pricing-table",
                    "settings": {
                        "pricing_style": "style-1",
                        "plan_name": "Basic Plan",
                        "price": "$99",
                        "price_period": "per month",
                        "features": [
                            {"text": "Feature 1", "included": "yes"},
                            {"text": "Feature 2", "included": "yes"},
                            {"text": "Feature 3", "included": "no"}
                        ],
                        "button_text": "Choose Plan",
                        "button_link": {"url": "#"},
                        "featured": "no",
                        "card_background": "#ffffff",
                        "price_color": "#e74c3c",
                        "button_style": "primary"
                    }
                }
            }
        }
    
    def create_riman_with_cholot_widgets(self):
        """
        Erstellt RIMAN Config mit Cholot Widgets
        """
        return {
            "page_title": "RIMAN GmbH - Cholot Widgets",
            "hero": {
                "widget": "cholot-hero-banner",
                "title": "Professionelle Schadstoffsanierung in Berlin",
                "subtitle": "Seit 1998 Ihr zuverlässiger Partner",
                "description": "RIMAN GmbH steht für höchste Qualität in der Schadstoffsanierung. Vertrauen Sie auf unsere 25-jährige Erfahrung.",
                "background_image": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=1920&h=1080&fit=crop",
                "cta_text": "Jetzt beraten lassen",
                "cta_link": "#contact"
            },
            
            "services": {
                "widget": "cholot-service-card",
                "title": "Unsere Leistungen",
                "items": [
                    {
                        "icon": "fas fa-shield-alt",
                        "title": "Asbestsanierung", 
                        "description": "Sichere und zertifizierte Asbestentfernung nach TRGS 519. Schutz für Mensch und Umwelt steht an erster Stelle.",
                        "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=300&fit=crop",
                        "color": "#e74c3c",
                        "button_text": "Mehr erfahren",
                        "button_link": "/asbestsanierung"
                    },
                    {
                        "icon": "fas fa-flask",
                        "title": "PCB-Sanierung",
                        "description": "Fachgerechte Sanierung PCB-belasteter Materialien nach aktuellen Umweltstandards und Vorschriften.",
                        "image": "https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=400&h=300&fit=crop",
                        "color": "#3498db",
                        "button_text": "Mehr erfahren",
                        "button_link": "/pcb-sanierung"
                    },
                    {
                        "icon": "fas fa-home",
                        "title": "Schimmelsanierung",
                        "description": "Nachhaltige Schimmelbeseitigung mit präventiven Maßnahmen für langfristig gesunde Raumluft.",
                        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop", 
                        "color": "#2ecc71",
                        "button_text": "Mehr erfahren",
                        "button_link": "/schimmelsanierung"
                    }
                ]
            },
            
            "team": {
                "widget": "cholot-team-member",
                "title": "Unser Experten-Team",
                "members": [
                    {
                        "name": "Thomas Schmidt",
                        "position": "Geschäftsführer & Sachverständiger",
                        "bio": "25 Jahre Erfahrung in der Schadstoffsanierung. Zertifizierter Sachverständiger für Schadstoffe in Innenräumen.",
                        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop",
                        "social": {
                            "linkedin": "https://linkedin.com/in/thomas-schmidt",
                            "email": "thomas@riman-gmbh.de"
                        }
                    },
                    {
                        "name": "Maria Weber",
                        "position": "Projektleiterin",
                        "bio": "Expertin für komplexe Sanierungsprojekte mit Spezialisierung auf Großobjekte und Industrieanlagen.",
                        "image": "https://images.unsplash.com/photo-1494790108755-2616b332c67c?w=300&h=300&fit=crop",
                        "social": {
                            "linkedin": "https://linkedin.com/in/maria-weber",
                            "email": "maria@riman-gmbh.de"
                        }
                    }
                ]
            },
            
            "testimonials": {
                "widget": "cholot-testimonial",
                "title": "Das sagen unsere Kunden",
                "items": [
                    {
                        "content": "Professionelle Beratung und perfekte Umsetzung der Asbestsanierung. Das Team von RIMAN hat uns durch den kompletten Prozess begleitet.",
                        "client_name": "Dr. Andreas Mueller",
                        "client_position": "Facility Manager",
                        "client_company": "TechCenter Berlin GmbH",
                        "rating": 5
                    },
                    {
                        "content": "Schnelle Reaktion bei unserem Schimmelproblem. Nachhaltige Lösung und faire Preise. Können wir nur weiterempfehlen!",
                        "client_name": "Sandra Hoffmann", 
                        "client_position": "Hausverwalterin",
                        "client_company": "Wohnbau Berlin",
                        "rating": 5
                    }
                ]
            },
            
            "contact": {
                "widget": "cholot-contact-info",
                "title": "Kontaktieren Sie uns",
                "info": {
                    "address": "Musterstraße 123, 10115 Berlin",
                    "phone": "030-12345678",
                    "email": "info@riman-gmbh.de",
                    "hours": "Mo-Fr: 8:00-18:00 Uhr"
                }
            }
        }
    
    def generate_cholot_widget(self, widget_type, config):
        """
        Generiert ein spezifisches Cholot Widget
        """
        if widget_type not in self.cholot_widgets:
            raise ValueError(f"Widget type '{widget_type}' not found in Cholot library")
        
        # Deep copy des Templates
        widget = json.loads(json.dumps(self.cholot_widgets[widget_type]["template"]))
        
        # Config anwenden
        if widget_type == "cholot-service-card":
            widget["settings"].update({
                "service_title": config.get("title", "Service"),
                "service_description": config.get("description", ""),
                "service_icon": {"value": config.get("icon", "fas fa-check"), "library": "fa-solid"},
                "icon_color": config.get("color", "#e74c3c"),
                "service_image": {"url": config.get("image", ""), "id": ""},
                "button_text": config.get("button_text", "Learn More"),
                "button_link": {"url": config.get("button_link", "#")}
            })
        
        elif widget_type == "cholot-hero-banner":
            widget["settings"].update({
                "hero_title": config.get("title", "Hero Title"),
                "hero_subtitle": config.get("subtitle", ""),
                "hero_description": config.get("description", ""),
                "hero_background_image": {"url": config.get("background_image", ""), "id": ""},
                "cta_button_text": config.get("cta_text", "Get Started"),
                "cta_button_link": {"url": config.get("cta_link", "#")}
            })
        
        elif widget_type == "cholot-team-member":
            widget["settings"].update({
                "member_name": config.get("name", "Team Member"),
                "member_position": config.get("position", "Position"),
                "member_bio": config.get("bio", ""),
                "member_image": {"url": config.get("image", ""), "id": ""}
            })
            
            # Social Links
            if "social" in config:
                social_links = []
                for platform, url in config["social"].items():
                    if url:
                        social_links.append({
                            "platform": platform,
                            "url": url,
                            "icon": f"fab fa-{platform}" if platform != "email" else "fas fa-envelope"
                        })
                widget["settings"]["social_links"] = social_links
        
        elif widget_type == "cholot-testimonial":
            widget["settings"].update({
                "testimonial_content": config.get("content", "Great service!"),
                "client_name": config.get("client_name", "Client Name"),
                "client_position": config.get("client_position", "Position"), 
                "client_company": config.get("client_company", "Company"),
                "rating": config.get("rating", 5)
            })
        
        elif widget_type == "cholot-contact-info":
            contact_items = []
            info = config.get("info", {})
            
            if info.get("address"):
                contact_items.append({
                    "type": "address",
                    "icon": {"value": "fas fa-map-marker-alt", "library": "fa-solid"},
                    "label": "Adresse",
                    "value": info["address"]
                })
            
            if info.get("phone"):
                contact_items.append({
                    "type": "phone",
                    "icon": {"value": "fas fa-phone", "library": "fa-solid"},
                    "label": "Telefon", 
                    "value": info["phone"]
                })
            
            if info.get("email"):
                contact_items.append({
                    "type": "email",
                    "icon": {"value": "fas fa-envelope", "library": "fa-solid"},
                    "label": "E-Mail",
                    "value": info["email"]
                })
                
            widget["settings"]["contact_items"] = contact_items
        
        return widget
    
    def create_cholot_elementor_structure(self, config):
        """
        Erstellt komplette Elementor-Struktur mit Cholot Widgets
        """
        structure = []
        
        # 1. Hero Section mit Cholot Hero Banner
        hero_section = {
            "id": "hero_section",
            "elType": "section",
            "settings": {
                "layout": "full_width",
                "min_height": {"unit": "vh", "size": 100}
            },
            "elements": [{
                "id": "hero_column",
                "elType": "column",
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None
                },
                "elements": [
                    self.generate_cholot_widget("cholot-hero-banner", config["hero"])
                ]
            }]
        }
        structure.append(hero_section)
        
        # 2. Services Section mit Cholot Service Cards
        services_section = {
            "id": "services_section", 
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "padding": {"unit": "px", "top": 100, "bottom": 100}
            },
            "elements": []
        }
        
        # Services Title
        title_column = {
            "id": "services_title_col",
            "elType": "column",
            "settings": {
                "_column_size": 100,
                "_inline_size": None
            },
            "elements": [{
                "id": "services_title",
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config["services"]["title"],
                    "header_size": "h2",
                    "align": "center"
                }
            }]
        }
        services_section["elements"].append(title_column)
        
        # Service Cards
        for i, service in enumerate(config["services"]["items"]):
            column = {
                "id": f"service_col_{i}",
                "elType": "column",
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None
                },
                "elements": [
                    self.generate_cholot_widget("cholot-service-card", service)
                ]
            }
            services_section["elements"].append(column)
        
        structure.append(services_section)
        
        # 3. Team Section mit Cholot Team Members
        team_section = {
            "id": "team_section",
            "elType": "section",
            "settings": {
                "layout": "boxed", 
                "background_color": "#f8f9fa",
                "padding": {"unit": "px", "top": 100, "bottom": 100}
            },
            "elements": []
        }
        
        # Team Title
        team_title_column = {
            "id": "team_title_col",
            "elType": "column", 
            "settings": {
                "_column_size": 100,
                "_inline_size": None
            },
            "elements": [{
                "id": "team_title",
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config["team"]["title"],
                    "header_size": "h2",
                    "align": "center"
                }
            }]
        }
        team_section["elements"].append(team_title_column)
        
        # Team Members
        for i, member in enumerate(config["team"]["members"]):
            column = {
                "id": f"team_col_{i}",
                "elType": "column",
                "settings": {
                    "_column_size": int(100 / len(config["team"]["members"])),
                    "_inline_size": None
                },
                "elements": [
                    self.generate_cholot_widget("cholot-team-member", member)
                ]
            }
            team_section["elements"].append(column)
        
        structure.append(team_section)
        
        # 4. Testimonials Section
        testimonials_section = {
            "id": "testimonials_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "padding": {"unit": "px", "top": 100, "bottom": 100}
            },
            "elements": []
        }
        
        # Testimonials Title
        testimonials_title_column = {
            "id": "testimonials_title_col",
            "elType": "column",
            "settings": {
                "_column_size": 100,
                "_inline_size": None
            },
            "elements": [{
                "id": "testimonials_title",
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": config["testimonials"]["title"],
                    "header_size": "h2",
                    "align": "center"
                }
            }]
        }
        testimonials_section["elements"].append(testimonials_title_column)
        
        # Testimonial Items
        for i, testimonial in enumerate(config["testimonials"]["items"]):
            column = {
                "id": f"testimonial_col_{i}",
                "elType": "column",
                "settings": {
                    "_column_size": int(100 / len(config["testimonials"]["items"])),
                    "_inline_size": None
                },
                "elements": [
                    self.generate_cholot_widget("cholot-testimonial", testimonial)
                ]
            }
            testimonials_section["elements"].append(column)
        
        structure.append(testimonials_section)
        
        # 5. Contact Section mit Cholot Contact Info
        contact_section = {
            "id": "contact_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "background_color": "#232323", 
                "padding": {"unit": "px", "top": 80, "bottom": 80}
            },
            "elements": [{
                "id": "contact_column",
                "elType": "column",
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None
                },
                "elements": [
                    {
                        "id": "contact_title",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": config["contact"]["title"],
                            "header_size": "h2",
                            "align": "center",
                            "title_color": "#ffffff"
                        }
                    },
                    self.generate_cholot_widget("cholot-contact-info", config["contact"])
                ]
            }]
        }
        structure.append(contact_section)
        
        return structure
    
    def generate_complete_cholot_xml(self):
        """
        Generiert komplette WordPress XML mit Cholot Widgets
        """
        print("🎨 CHOLOT WIDGET GENERATOR")
        print("=" * 60)
        
        # Config mit Cholot Widgets
        config = self.create_riman_with_cholot_widgets()
        print(f"✅ Config mit Cholot Widgets erstellt")
        
        # Elementor-Struktur
        structure = self.create_cholot_elementor_structure(config)
        print(f"✅ {len(structure)} Sections mit Cholot Widgets")
        
        # WordPress XML
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>RIMAN GmbH - Cholot Widgets</title>
    <link>https://riman-gmbh.de</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <item>
        <title>RIMAN GmbH - Professional mit Cholot</title>
        <link>https://riman-gmbh.de/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://riman-gmbh.de/?page_id=100</guid>
        <description>Professionelle Schadstoffsanierung mit Cholot Theme Widgets</description>
        <content:encoded><![CDATA[]]></content:encoded>
        <wp:post_id>100</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_name><![CDATA[home]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_data]]></wp:meta_key>
            <wp:meta_value><![CDATA[{json.dumps(structure, separators=(',', ':'))}]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>"""
        
        # Speichere XML
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"riman-cholot-widgets-{timestamp}.xml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print("\n" + "=" * 60)
        print("✅ CHOLOT WIDGETS XML GENERIERT!")
        print("=" * 60)
        
        print(f"\n📄 Datei: {filename}")
        print(f"📊 Größe: {len(xml_content):,} Zeichen")
        
        print(f"\n🎨 Cholot Widgets verwendet:")
        print(f"   ✅ cholot-hero-banner: Full-Screen Hero")
        print(f"   ✅ cholot-service-card: 3 Service Cards")
        print(f"   ✅ cholot-team-member: Team Profile Cards")  
        print(f"   ✅ cholot-testimonial: Client Reviews")
        print(f"   ✅ cholot-contact-info: Contact Details")
        
        print(f"\n🎯 Features:")
        print(f"   • Native Cholot Theme Integration")
        print(f"   • Responsive Service Cards")
        print(f"   • Professional Team Profiles")
        print(f"   • Customer Testimonials")
        print(f"   • Structured Contact Info")
        
        return filename


def main():
    generator = CholotWidgetGenerator()
    xml_file = generator.generate_complete_cholot_xml()
    
    print(f"\n🚀 FERTIG! Native Cholot Theme Website:")
    print(f"   Import: {xml_file}")
    print(f"   Ergebnis: Professionelle RIMAN Website mit echten Cholot Widgets!")

if __name__ == "__main__":
    main()