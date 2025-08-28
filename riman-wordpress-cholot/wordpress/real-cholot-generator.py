#!/usr/bin/env python3
"""
Real Cholot Generator
Verwendet die tatsächlichen Cholot Theme Widgets
"""

import json
from datetime import datetime

class RealCholotGenerator:
    """
    Generiert mit den echten Cholot Widgets aus dem Template
    """
    
    def __init__(self):
        # Echte Cholot Widgets aus dem Original-Template
        self.real_cholot_widgets = [
            "cholot-contact",      # Contact widget
            "cholot-team",         # Team member widget  
            "cholot-testimonial-two", # Testimonial widget
            "cholot-text-line",    # Text with line widget
            "cholot-texticon",     # Text with icon widget
            "cholot-title"         # Title widget
        ]
    
    def create_cholot_texticon(self, service):
        """
        Erstellt cholot-texticon Widget (exakt wie Original-Template)
        """
        return {
            "id": f"texticon_{service['title'].lower().replace(' ', '_')}",
            "elType": "widget",
            "widgetType": "cholot-texticon",
            "settings": {
                "title": service.get('title', 'Service Title'),
                "text": f"<p>{service.get('description', 'Service description')}</p>",
                "icon": f"fa {service.get('icon', 'fa-check')}",
                "icon_style": "left",
                "subtitle": service.get('subtitle', ''),
                "icon_color": "#ffffff",
                "iconbg_color": service.get('color', '#b68c2f'),
                "title_color": "#232323",
                "text_color": "#666666",
                "icon_size": {"unit": "px", "size": 50},
                "icon_bg_size": {"unit": "px", "size": 72, "sizes": []},
                "title_typography_typography": "custom",
                "title_typography_font_size": {"unit": "px", "size": 24},
                "title_typography_font_weight": "600",
                "text_typography_typography": "custom", 
                "text_typography_font_size": {"unit": "px", "size": 16},
                "text_typography_line_height": {"unit": "em", "size": 1.6},
                "content_alignment": "center",
                "icon_position": "top",
                "icon_bordering_border": "solid",
                "icon_bordering_color": "#fafafa",
                "icon_bordering_width": {"unit": "px", "top": 7, "right": 7, "bottom": 7, "left": 7, "isLinked": True},
                "icon_margin": {"unit": "px", "top": -27, "right": 0, "bottom": 0, "left": 0, "isLinked": False},
                "icon_lheight": {"unit": "px", "size": 58, "sizes": []},
                "title_margin": {"unit": "px", "top": 0, "right": 0, "bottom": 15, "left": 0, "isLinked": False},
                "text_margin": {"unit": "px", "top": 15, "right": 0, "bottom": -30, "left": 0, "isLinked": False},
                "_padding": {"unit": "px", "top": 30, "right": 30, "bottom": 30, "left": 30, "isLinked": True},
                "_border_width": {"unit": "px", "top": 0, "right": 1, "bottom": 1, "left": 1, "isLinked": False},
                "_border_color": service.get('color', '#b68c2f'),
                "_border_border": "dashed"
            }
        }
    
    def create_cholot_title(self, title_text, subtitle=""):
        """
        Erstellt cholot-title Widget (aus Original-Template)
        """
        return {
            "id": f"title_{title_text.lower().replace(' ', '_')}",
            "elType": "widget", 
            "widgetType": "cholot-title",
            "settings": {
                "title": title_text,
                "subtitle": subtitle,
                "title_color": "#232323",
                "subtitle_color": "#666666",
                "title_typography_typography": "custom",
                "title_typography_font_family": "Playfair Display",
                "title_typography_font_size": {"unit": "px", "size": 48},
                "title_typography_font_weight": "700",
                "title_typography_line_height": {"unit": "em", "size": 1.2},
                "subtitle_typography_typography": "custom", 
                "subtitle_typography_font_size": {"unit": "px", "size": 18},
                "subtitle_typography_line_height": {"unit": "em", "size": 1.5},
                "alignment": "center",
                "title_margin": {"unit": "px", "top": 0, "right": 0, "bottom": 20, "left": 0}
            }
        }
    
    def create_cholot_team(self, member):
        """
        Erstellt cholot-team Widget (aus Original-Template)
        """
        return {
            "id": f"team_{member['name'].lower().replace(' ', '_')}",
            "elType": "widget",
            "widgetType": "cholot-team",
            "settings": {
                "name": member.get('name', 'Team Member'),
                "position": member.get('position', 'Position'),
                "description": member.get('bio', ''),
                "image": {"url": member.get('image', ''), "id": ""},
                "name_color": "#232323",
                "position_color": "#666666", 
                "description_color": "#666666",
                "name_typography_typography": "custom",
                "name_typography_font_size": {"unit": "px", "size": 24},
                "name_typography_font_weight": "700",
                "position_typography_typography": "custom",
                "position_typography_font_size": {"unit": "px", "size": 16},
                "position_typography_font_style": "italic",
                "description_typography_typography": "custom",
                "description_typography_font_size": {"unit": "px", "size": 14},
                "description_typography_line_height": {"unit": "em", "size": 1.6},
                "content_alignment": "center",
                "image_border_radius": {"unit": "%", "size": 50},
                "social_links": [
                    {"platform": "linkedin", "url": member.get('social', {}).get('linkedin', ''), "icon": "fab fa-linkedin"},
                    {"platform": "email", "url": f"mailto:{member.get('social', {}).get('email', '')}", "icon": "fas fa-envelope"}
                ]
            }
        }
    
    def create_cholot_testimonial_two(self, testimonial):
        """
        Erstellt cholot-testimonial-two Widget (aus Original-Template)  
        """
        return {
            "id": f"testimonial_{testimonial['client_name'].lower().replace(' ', '_')}",
            "elType": "widget",
            "widgetType": "cholot-testimonial-two",
            "settings": {
                "testimonial_content": testimonial.get('content', 'Great service!'),
                "client_name": testimonial.get('client_name', 'Client Name'),
                "client_position": testimonial.get('client_position', 'Position'),
                "client_company": testimonial.get('client_company', 'Company'),
                "client_image": {"url": testimonial.get('client_image', ''), "id": ""},
                "rating": testimonial.get('rating', 5),
                "show_rating": "yes",
                "content_color": "#666666",
                "name_color": "#232323", 
                "position_color": "#666666",
                "rating_color": "#f39c12",
                "content_typography_typography": "custom",
                "content_typography_font_size": {"unit": "px", "size": 16},
                "content_typography_line_height": {"unit": "em", "size": 1.6},
                "content_typography_font_style": "italic",
                "name_typography_typography": "custom",
                "name_typography_font_size": {"unit": "px", "size": 18},
                "name_typography_font_weight": "600",
                "quote_icon": "fas fa-quote-left",
                "quote_icon_color": "#e74c3c",
                "quote_icon_size": {"unit": "px", "size": 30},
                "background_color": "#f8f9fa",
                "border_radius": {"unit": "px", "size": 10},
                "padding": {"unit": "px", "top": 30, "right": 25, "bottom": 30, "left": 25}
            }
        }
    
    def create_cholot_contact(self, contact_info):
        """
        Erstellt cholot-contact Widget (aus Original-Template)
        """
        return {
            "id": "contact_widget", 
            "elType": "widget",
            "widgetType": "cholot-contact",
            "settings": {
                "contact_form_title": "Kontaktieren Sie uns",
                "show_contact_info": "yes",
                "contact_address": contact_info.get('address', ''),
                "contact_phone": contact_info.get('phone', ''),
                "contact_email": contact_info.get('email', ''),
                "contact_hours": contact_info.get('hours', 'Mo-Fr: 8:00-18:00'),
                "form_fields": [
                    {"field_type": "text", "field_label": "Name", "field_required": "yes"},
                    {"field_type": "email", "field_label": "E-Mail", "field_required": "yes"},
                    {"field_type": "text", "field_label": "Telefon", "field_required": "no"},
                    {"field_type": "textarea", "field_label": "Nachricht", "field_required": "yes"}
                ],
                "submit_button_text": "Nachricht senden",
                "success_message": "Vielen Dank für Ihre Nachricht. Wir melden uns schnellstmöglich bei Ihnen.",
                "form_style": "style-1",
                "input_background_color": "#ffffff",
                "input_border_color": "#dddddd",
                "button_background_color": "#e74c3c",
                "button_text_color": "#ffffff",
                "info_icon_color": "#e74c3c",
                "info_text_color": "#666666",
                "title_color": "#232323"
            }
        }
    
    def create_cholot_text_line(self, text, line_position="bottom"):
        """
        Erstellt cholot-text-line Widget (aus Original-Template)
        """
        return {
            "id": f"textline_{text.lower().replace(' ', '_')[:10]}",
            "elType": "widget",
            "widgetType": "cholot-text-line", 
            "settings": {
                "text": text,
                "line_position": line_position,  # top, bottom, both
                "text_color": "#232323",
                "line_color": "#e74c3c",
                "line_width": {"unit": "px", "size": 50},
                "line_height": {"unit": "px", "size": 3},
                "text_typography_typography": "custom",
                "text_typography_font_size": {"unit": "px", "size": 16},
                "text_typography_font_weight": "500",
                "text_typography_text_transform": "uppercase",
                "text_typography_letter_spacing": {"unit": "px", "size": 1},
                "alignment": "center",
                "spacing": {"unit": "px", "size": 15}
            }
        }
    
    def create_riman_config(self):
        """
        RIMAN Config für echte Cholot Widgets
        """
        return {
            "page_title": "RIMAN GmbH - Echte Cholot Widgets",
            
            "hero": {
                "title": "Professionelle Schadstoffsanierung in Berlin",
                "subtitle": "Seit 1998 Ihr zuverlässiger Partner für Asbest, PCB und Schimmelsanierung",
                "background": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=1920&h=1080&fit=crop"
            },
            
            "services": [
                {
                    "title": "Asbestsanierung",
                    "description": "Sichere und zertifizierte Asbestentfernung nach TRGS 519. Schutz für Mensch und Umwelt.",
                    "icon": "fa-shield",
                    "color": "#e74c3c"
                },
                {
                    "title": "PCB-Sanierung", 
                    "description": "Fachgerechte Sanierung PCB-belasteter Materialien nach Umweltstandards.",
                    "icon": "fa-flask",
                    "color": "#3498db"
                },
                {
                    "title": "Schimmelsanierung",
                    "description": "Nachhaltige Schimmelbeseitigung mit präventiven Maßnahmen.",
                    "icon": "fa-home",
                    "color": "#2ecc71"
                }
            ],
            
            "team": [
                {
                    "name": "Thomas Schmidt",
                    "position": "Geschäftsführer & Sachverständiger",
                    "bio": "25 Jahre Erfahrung in der Schadstoffsanierung. Zertifizierter Sachverständiger für Schadstoffe in Innenräumen.",
                    "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop",
                    "social": {
                        "linkedin": "https://linkedin.com/in/thomas-schmidt-riman",
                        "email": "thomas@riman-gmbh.de"
                    }
                },
                {
                    "name": "Maria Weber",
                    "position": "Projektleiterin",
                    "bio": "Expertin für komplexe Sanierungsprojekte mit Spezialisierung auf Großobjekte.",
                    "image": "https://images.unsplash.com/photo-1494790108755-2616b332c67c?w=300&h=300&fit=crop",
                    "social": {
                        "linkedin": "https://linkedin.com/in/maria-weber-riman",
                        "email": "maria@riman-gmbh.de"
                    }
                }
            ],
            
            "testimonials": [
                {
                    "content": "Professionelle Beratung und perfekte Umsetzung der Asbestsanierung. Das Team von RIMAN hat uns durch den kompletten Prozess begleitet.",
                    "client_name": "Dr. Andreas Mueller",
                    "client_position": "Facility Manager",
                    "client_company": "TechCenter Berlin GmbH", 
                    "rating": 5,
                    "client_image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop"
                },
                {
                    "content": "Schnelle Reaktion bei unserem Schimmelproblem. Nachhaltige Lösung und faire Preise. Können wir nur weiterempfehlen!",
                    "client_name": "Sandra Hoffmann",
                    "client_position": "Hausverwalterin", 
                    "client_company": "Wohnbau Berlin",
                    "rating": 5,
                    "client_image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop"
                }
            ],
            
            "contact": {
                "address": "Musterstraße 123, 10115 Berlin",
                "phone": "030-12345678", 
                "email": "info@riman-gmbh.de",
                "hours": "Mo-Fr: 8:00-18:00 Uhr"
            }
        }
    
    def create_real_cholot_structure(self, config):
        """
        Erstellt Elementor-Struktur mit echten Cholot Widgets
        """
        structure = []
        
        # 1. Hero Section mit cholot-title
        hero_section = {
            "id": "hero_section",
            "elType": "section", 
            "settings": {
                "layout": "full_width",
                "min_height": {"unit": "vh", "size": 100},
                "background_background": "classic",
                "background_image": {"url": config["hero"]["background"]},
                "background_overlay_background": "classic",
                "background_overlay_color": "rgba(0,0,0,0.6)",
                "content_position": "middle"
            },
            "elements": [{
                "id": "hero_column",
                "elType": "column",
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None
                },
                "elements": [
                    self.create_cholot_text_line("Schadstoffsanierung seit 1998"),
                    self.create_cholot_title(config["hero"]["title"], config["hero"]["subtitle"])
                ]
            }]
        }
        structure.append(hero_section)
        
        # 2. Services mit cholot-texticon
        services_section = {
            "id": "services_section",
            "elType": "section",
            "settings": {
                "layout": "boxed", 
                "padding": {"unit": "px", "top": 100, "bottom": 100}
            },
            "elements": []
        }
        
        # Services Title mit cholot-title
        title_column = {
            "id": "services_title_col",
            "elType": "column",
            "settings": {
                "_column_size": 100,
                "_inline_size": None
            },
            "elements": [
                self.create_cholot_title("Unsere Leistungen", "Professionelle Schadstoffsanierung für Berlin und Brandenburg")
            ]
        }
        services_section["elements"].append(title_column)
        
        # Service Columns mit cholot-texticon
        for service in config["services"]:
            column = {
                "id": f"service_col_{service['title'].lower().replace(' ', '_')}",
                "elType": "column",
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None
                },
                "elements": [
                    self.create_cholot_texticon(service)
                ]
            }
            services_section["elements"].append(column)
        
        structure.append(services_section)
        
        # 3. Team Section mit cholot-team
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
            "elements": [
                self.create_cholot_text_line("Unser Team"),
                self.create_cholot_title("Experten mit Erfahrung", "Qualifizierte Fachkräfte für Ihre Sicherheit")
            ]
        }
        team_section["elements"].append(team_title_column)
        
        # Team Members mit cholot-team
        for member in config["team"]:
            column = {
                "id": f"team_col_{member['name'].lower().replace(' ', '_')}",
                "elType": "column",
                "settings": {
                    "_column_size": int(100 / len(config["team"])),
                    "_inline_size": None
                },
                "elements": [
                    self.create_cholot_team(member)
                ]
            }
            team_section["elements"].append(column)
        
        structure.append(team_section)
        
        # 4. Testimonials mit cholot-testimonial-two
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
            "elements": [
                self.create_cholot_text_line("Kundenstimmen"),
                self.create_cholot_title("Das sagen unsere Kunden", "Vertrauen Sie auf unsere Referenzen")
            ]
        }
        testimonials_section["elements"].append(testimonials_title_column)
        
        # Testimonial Columns mit cholot-testimonial-two
        for testimonial in config["testimonials"]:
            column = {
                "id": f"testimonial_col_{testimonial['client_name'].lower().replace(' ', '_')}",
                "elType": "column",
                "settings": {
                    "_column_size": int(100 / len(config["testimonials"])),
                    "_inline_size": None
                },
                "elements": [
                    self.create_cholot_testimonial_two(testimonial)
                ]
            }
            testimonials_section["elements"].append(column)
        
        structure.append(testimonials_section)
        
        # 5. Contact Section mit cholot-contact
        contact_section = {
            "id": "contact_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "background_color": "#232323",
                "padding": {"unit": "px", "top": 100, "bottom": 100}
            },
            "elements": [{
                "id": "contact_column",
                "elType": "column",
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None
                },
                "elements": [
                    self.create_cholot_contact(config["contact"])
                ]
            }]
        }
        structure.append(contact_section)
        
        return structure
    
    def generate_real_cholot_xml(self):
        """
        Generiert WordPress XML mit echten Cholot Widgets
        """
        print("🎯 REAL CHOLOT GENERATOR")
        print("=" * 60)
        print("Verwendet die tatsächlichen Cholot Theme Widgets:")
        for widget in self.real_cholot_widgets:
            print(f"   ✅ {widget}")
        
        # Config erstellen
        config = self.create_riman_config()
        print(f"\n✅ RIMAN Config für echte Cholot Widgets erstellt")
        
        # Struktur mit echten Widgets
        structure = self.create_real_cholot_structure(config)
        print(f"✅ {len(structure)} Sections mit echten Cholot Widgets")
        
        # Widget-Zählung
        widget_count = {}
        for section in structure:
            for column in section.get('elements', []):
                for widget in column.get('elements', []):
                    widget_type = widget.get('widgetType', 'unknown')
                    widget_count[widget_type] = widget_count.get(widget_type, 0) + 1
        
        print(f"\n📊 Verwendete Widgets:")
        for widget_type, count in widget_count.items():
            print(f"   • {widget_type}: {count}x")
        
        # WordPress XML generieren
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>RIMAN GmbH - Echte Cholot Widgets</title>
    <link>https://riman-gmbh.de</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <item>
        <title>RIMAN GmbH - Original Cholot Theme</title>
        <link>https://riman-gmbh.de/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://riman-gmbh.de/?page_id=100</guid>
        <description>Professionelle Schadstoffsanierung mit echten Cholot Theme Widgets</description>
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
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[elementor_header_footer]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>"""
        
        # Speichern
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"riman-real-cholot-{timestamp}.xml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"\n" + "=" * 60)
        print("✅ REAL CHOLOT XML GENERIERT!")
        print("=" * 60)
        
        print(f"\n📄 Datei: {filename}")
        print(f"📊 Größe: {len(xml_content):,} Zeichen")
        
        print(f"\n🎯 Echte Cholot Widgets verwendet:")
        for widget_type, count in widget_count.items():
            if widget_type.startswith('cholot-'):
                print(f"   ✅ {widget_type}: {count}x")
        
        return filename


def main():
    generator = RealCholotGenerator()
    xml_file = generator.generate_real_cholot_xml()
    
    print(f"\n🚀 FERTIG! Echte Cholot Theme Website:")
    print(f"   Import: {xml_file}")
    print(f"   Jetzt mit den tatsächlichen Cholot Widgets!")

if __name__ == "__main__":
    main()