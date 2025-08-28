#!/usr/bin/env python3
"""
CSS Enhanced Generator
Fügt CSS-Klassen, Custom Styles und Animationen hinzu
"""

import json
import yaml
from datetime import datetime

class CSSEnhancedGenerator:
    """
    Generiert Elementor JSON mit CSS-Klassen und Styles
    """
    
    def __init__(self):
        self.attachment_id = 200
        self.css_classes = {}
        self.custom_css = []
    
    def create_enhanced_config(self):
        """
        Config mit CSS-Klassen und Styles
        """
        return {
            "page_title": "RIMAN GmbH - Styled mit CSS",
            "hero_title": "Professionelle Schadstoffsanierung",
            "hero_subtitle": "Seit 1998 Ihr Partner in Berlin",
            
            # CSS Settings pro Section
            "css_settings": {
                "hero": {
                    "css_classes": "hero-section fade-in",
                    "custom_css": ".hero-section { min-height: 100vh; }",
                    "animation": "fadeInUp",
                    "animation_delay": "0.2s"
                },
                "services": {
                    "css_classes": "services-grid hover-effects",
                    "custom_css": ".services-grid .service-item:hover { transform: translateY(-10px); transition: all 0.3s ease; }",
                    "animation": "fadeInUp",
                    "stagger": True
                },
                "team": {
                    "css_classes": "team-section gradient-bg",
                    "custom_css": ".gradient-bg { background: linear-gradient(45deg, #f8f9fa 0%, #e9ecef 100%); }",
                    "animation": "slideInFromLeft"
                }
            },
            
            # Services mit individuellen CSS-Einstellungen
            "services": [
                {
                    "title": "Asbestsanierung",
                    "description": "Sichere Asbestentfernung nach TRGS 519",
                    "icon": "shield",
                    "color": "#e74c3c",
                    "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=300&fit=crop",
                    "css_classes": "service-item asbest-service pulse-on-hover",
                    "custom_style": {
                        "border": "2px solid #e74c3c",
                        "border-radius": "15px",
                        "box-shadow": "0 5px 15px rgba(231, 76, 60, 0.2)",
                        "padding": "30px"
                    }
                },
                {
                    "title": "PCB-Sanierung",
                    "description": "Umweltgerechte PCB-Behandlung",
                    "icon": "flask", 
                    "color": "#3498db",
                    "image": "https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=400&h=300&fit=crop",
                    "css_classes": "service-item pcb-service slide-in-effect",
                    "custom_style": {
                        "border": "2px solid #3498db",
                        "border-radius": "15px", 
                        "box-shadow": "0 5px 15px rgba(52, 152, 219, 0.2)",
                        "padding": "30px",
                        "background": "linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%)"
                    }
                },
                {
                    "title": "Schimmelsanierung",
                    "description": "Nachhaltige Schimmelbekämpfung",
                    "icon": "home",
                    "color": "#2ecc71",
                    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop",
                    "css_classes": "service-item schimmel-service bounce-in",
                    "custom_style": {
                        "border": "2px solid #2ecc71",
                        "border-radius": "15px",
                        "box-shadow": "0 5px 15px rgba(46, 204, 113, 0.2)",
                        "padding": "30px",
                        "position": "relative"
                    }
                }
            ],
            
            # Team mit CSS-Styling
            "team": [
                {
                    "name": "Thomas Schmidt",
                    "position": "Geschäftsführer",
                    "bio": "25 Jahre Erfahrung",
                    "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop",
                    "css_classes": "team-member ceo-style rotate-on-hover",
                    "custom_style": {
                        "border-radius": "50%",
                        "border": "5px solid #gold",
                        "box-shadow": "0 10px 30px rgba(0,0,0,0.2)"
                    }
                },
                {
                    "name": "Maria Weber",
                    "position": "Projektleiterin", 
                    "bio": "Expertin für Großprojekte",
                    "image": "https://images.unsplash.com/photo-1494790108755-2616b332c67c?w=300&h=300&fit=crop",
                    "css_classes": "team-member manager-style scale-on-hover",
                    "custom_style": {
                        "border-radius": "50%",
                        "border": "3px solid #3498db",
                        "transition": "all 0.3s ease"
                    }
                }
            ],
            
            # Global CSS
            "global_css": """
                /* RIMAN Custom Styles */
                .fade-in { 
                    animation: fadeIn 1s ease-in-out; 
                }
                
                .pulse-on-hover:hover {
                    animation: pulse 0.5s infinite;
                }
                
                .rotate-on-hover:hover {
                    transform: rotate(5deg);
                    transition: transform 0.3s ease;
                }
                
                .scale-on-hover:hover {
                    transform: scale(1.05);
                    transition: transform 0.3s ease;
                }
                
                .slide-in-effect {
                    transform: translateX(-20px);
                    opacity: 0;
                    animation: slideIn 0.6s ease forwards;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.02); }
                    100% { transform: scale(1); }
                }
                
                @keyframes slideIn {
                    to { 
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                
                /* Responsive Design */
                @media (max-width: 768px) {
                    .services-grid {
                        grid-template-columns: 1fr;
                    }
                    
                    .hero-section {
                        min-height: 70vh;
                    }
                }
                
                /* Dark Mode Support */
                @media (prefers-color-scheme: dark) {
                    .service-item {
                        background-color: #2c3e50;
                        color: white;
                    }
                }
            """,
            
            "contact": {
                "email": "info@riman-gmbh.de",
                "phone": "030-12345678",
                "address": "Musterstraße 123, 10115 Berlin"
            }
        }
    
    def apply_css_to_widget(self, widget, css_config):
        """
        Wendet CSS-Klassen und Styles auf Widget an
        """
        settings = widget.get('settings', {})
        
        # CSS Klassen
        if 'css_classes' in css_config:
            settings['_css_classes'] = css_config['css_classes']
        
        # Custom CSS/Inline Styles
        if 'custom_style' in css_config:
            # Konvertiere Python dict zu CSS string
            css_string = []
            for prop, value in css_config['custom_style'].items():
                css_string.append(f"{prop.replace('_', '-')}: {value}")
            settings['_custom_css'] = "; ".join(css_string)
        
        # Animation Settings
        if 'animation' in css_config:
            settings['_animation'] = css_config['animation']
            settings['_animation_delay'] = css_config.get('animation_delay', '0')
        
        # Responsive Settings
        if 'responsive' in css_config:
            for device, responsive_settings in css_config['responsive'].items():
                for prop, value in responsive_settings.items():
                    settings[f'{prop}_{device}'] = value
        
        widget['settings'] = settings
        return widget
    
    def apply_css_to_section(self, section, css_config):
        """
        Wendet CSS auf Section an
        """
        settings = section.get('settings', {})
        
        # CSS Klassen für Section
        if 'css_classes' in css_config:
            settings['css_classes'] = css_config['css_classes']
        
        # Custom CSS
        if 'custom_css' in css_config:
            settings['custom_css'] = css_config['custom_css']
        
        # Animation für ganze Section
        if 'animation' in css_config:
            settings['animation'] = css_config['animation']
            if css_config.get('stagger'):
                settings['animation_delay'] = '0.1s'
        
        section['settings'] = settings
        return section
    
    def create_styled_elementor_structure(self, config):
        """
        Erstellt Elementor-Struktur mit CSS-Styling
        """
        structure = []
        css_settings = config.get('css_settings', {})
        
        # 1. Hero Section mit CSS
        hero = {
            "id": "hero_section", 
            "elType": "section",
            "settings": {
                "layout": "full_width",
                "min_height": {"unit": "vh", "size": 100},
                "background_background": "classic",
                "background_image": {
                    "url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=1920&h=1080&fit=crop"
                },
                "background_overlay_background": "classic",
                "background_overlay_color": "rgba(0,0,0,0.6)",
                "padding": {"unit": "px", "top": "100", "bottom": "100"}
            },
            "elements": [{
                "id": "hero_column",
                "elType": "column",
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None
                },
                "elements": [
                    {
                        "id": "hero_title",
                        "elType": "widget", 
                        "widgetType": "cholot-title",
                        "settings": {
                            "title": config.get('hero_title', 'Willkommen'),
                            "align": "center",
                            "title_color": "#ffffff",
                            "desc_typography_font_size": {"unit": "px", "size": 54},
                            "_css_classes": "hero-title animated-title",
                            "_animation": "fadeInDown",
                            "_animation_delay": "0.3s"
                        }
                    },
                    {
                        "id": "hero_subtitle",
                        "elType": "widget",
                        "widgetType": "text-editor", 
                        "settings": {
                            "editor": f"<p class='hero-subtitle'>{config.get('hero_subtitle', '')}</p>",
                            "_css_classes": "hero-text fade-in-delayed",
                            "_animation": "fadeInUp",
                            "_animation_delay": "0.6s"
                        }
                    }
                ]
            }]
        }
        
        # CSS auf Hero anwenden
        if 'hero' in css_settings:
            hero = self.apply_css_to_section(hero, css_settings['hero'])
        
        structure.append(hero)
        
        # 2. Services mit individuellen CSS-Klassen
        services_section = {
            "id": "services_section",
            "elType": "section", 
            "settings": {
                "layout": "boxed",
                "padding": {"unit": "px", "top": "100", "bottom": "100"}
            },
            "elements": []
        }
        
        # CSS auf Services Section anwenden
        if 'services' in css_settings:
            services_section = self.apply_css_to_section(services_section, css_settings['services'])
        
        # Service Columns mit CSS
        for i, service in enumerate(config.get('services', [])):
            column = {
                "id": f"service_col_{i}",
                "elType": "column",
                "settings": {
                    "_column_size": 33,
                    "_inline_size": None
                },
                "elements": [{
                    "id": f"service_widget_{i}",
                    "elType": "widget",
                    "widgetType": "cholot-texticon", 
                    "settings": {
                        "title": service.get('title', 'Service'),
                        "text": f"<p>{service.get('description', '')}</p>",
                        "icon": f"fa fa-{service.get('icon', 'check')}",
                        "icon_color": service.get('color', '#ff6b6b'),
                        "title_color": "#232323",
                        "text_color": "#666666",
                        "icon_size": {"size": 60, "unit": "px"}
                    }
                }]
            }
            
            # Service Bild hinzufügen
            if 'image' in service:
                column['elements'][0]['settings']['image'] = {
                    'url': service['image']
                }
            
            # CSS auf Service Widget anwenden
            if 'css_classes' in service or 'custom_style' in service:
                column['elements'][0] = self.apply_css_to_widget(
                    column['elements'][0], 
                    service
                )
            
            # Animation Delay für Staggered Effect
            if css_settings.get('services', {}).get('stagger'):
                column['elements'][0]['settings']['_animation_delay'] = f"{i * 0.2}s"
            
            services_section['elements'].append(column)
        
        structure.append(services_section)
        
        # 3. Team mit CSS
        if config.get('team'):
            team_section = {
                "id": "team_section",
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "padding": {"unit": "px", "top": "100", "bottom": "100"}
                },
                "elements": []
            }
            
            # CSS auf Team Section
            if 'team' in css_settings:
                team_section = self.apply_css_to_section(team_section, css_settings['team'])
            
            # Team Title
            title_column = {
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
                        "title": "Unser Team",
                        "header_size": "h2", 
                        "align": "center",
                        "_css_classes": "section-title team-title",
                        "_animation": "fadeInDown"
                    }
                }]
            }
            team_section['elements'].append(title_column)
            
            # Team Members mit CSS
            for i, member in enumerate(config['team']):
                column = {
                    "id": f"team_col_{i}",
                    "elType": "column",
                    "settings": {
                        "_column_size": int(100 / len(config['team'])),
                        "_inline_size": None
                    },
                    "elements": [{
                        "id": f"team_widget_{i}",
                        "elType": "widget",
                        "widgetType": "cholot-team",
                        "settings": {
                            "title": member.get('name', 'Team Member'),
                            "text": member.get('position', 'Position'),
                            "description": member.get('bio', ''),
                            "image": {"url": member.get('image', '')}
                        }
                    }]
                }
                
                # CSS auf Team Member anwenden
                if 'css_classes' in member or 'custom_style' in member:
                    column['elements'][0] = self.apply_css_to_widget(
                        column['elements'][0],
                        member
                    )
                
                team_section['elements'].append(column)
            
            structure.append(team_section)
        
        # 4. Contact mit CSS
        contact_section = {
            "id": "contact_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "background_background": "classic",
                "background_color": "#232323",
                "padding": {"unit": "px", "top": "80", "bottom": "80"},
                "css_classes": "contact-section dark-section"
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
                            "title": "Kontakt",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": "#ffffff",
                            "_css_classes": "contact-title glow-effect",
                            "_animation": "fadeIn"
                        }
                    },
                    {
                        "id": "contact_info",
                        "elType": "widget", 
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"""<div class='contact-info styled-contact'>
                            <p>📧 {config.get('contact', {}).get('email', '')}</p>
                            <p>📞 {config.get('contact', {}).get('phone', '')}</p>
                            <p>📍 {config.get('contact', {}).get('address', '')}</p>
                            </div>""",
                            "_css_classes": "contact-details fade-in-up"
                        }
                    }
                ]
            }]
        }
        structure.append(contact_section)
        
        return structure
    
    def generate_custom_css_section(self, config):
        """
        Generiert Custom CSS Section für WordPress
        """
        css = config.get('global_css', '')
        
        # Füge automatische CSS hinzu basierend auf den verwendeten Klassen
        auto_css = """
/* Auto-generated CSS for RIMAN */
.animated-title {
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.hero-subtitle {
    font-size: 1.2em;
    color: rgba(255,255,255,0.9);
    text-align: center;
    margin-top: 20px;
}

.glow-effect:hover {
    text-shadow: 0 0 20px rgba(255,255,255,0.5);
    transition: text-shadow 0.3s ease;
}

.styled-contact p {
    color: white;
    text-align: center;
    font-size: 1.1em;
    margin: 10px 0;
}

.fade-in-delayed {
    animation-delay: 0.5s;
}

.fade-in-up {
    animation: fadeInUp 0.8s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
        """
        
        return css + auto_css
    
    def generate_complete_styled_xml(self):
        """
        Generiert komplette WordPress XML mit CSS-Styling
        """
        print("🎨 CSS ENHANCED GENERATOR")
        print("=" * 60)
        
        # Config mit CSS erstellen
        config = self.create_enhanced_config()
        print(f"✅ Config mit CSS-Klassen erstellt")
        
        # Styled Elementor Struktur
        structure = self.create_styled_elementor_structure(config)
        print(f"✅ {len(structure)} Sections mit CSS-Styling")
        
        # Custom CSS generieren
        custom_css = self.generate_custom_css_section(config)
        print(f"✅ {len(custom_css)} Zeichen Custom CSS")
        
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
    <title>RIMAN GmbH - CSS Enhanced</title>
    <link>https://riman-gmbh.de</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <!-- CUSTOM CSS -->
    <item>
        <title>RIMAN Custom CSS</title>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <content:encoded><![CDATA[{custom_css}]]></content:encoded>
        <wp:post_type><![CDATA[custom_css]]></wp:post_type>
        <wp:status><![CDATA[publish]]></wp:status>
    </item>
    
    <!-- MAIN PAGE WITH CSS -->
    <item>
        <title>RIMAN GmbH - CSS Enhanced</title>
        <link>https://riman-gmbh.de/</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://riman-gmbh.de/?page_id=100</guid>
        <description>{config.get('hero_subtitle', '')}</description>
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
            <wp:meta_key><![CDATA[_elementor_custom_css]]></wp:meta_key>
            <wp:meta_value><![CDATA[{custom_css}]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>"""
        
        # Speichere XML
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"riman-css-enhanced-{timestamp}.xml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print("\n" + "=" * 60)
        print("✅ CSS-ENHANCED XML GENERIERT!")
        print("=" * 60)
        
        print(f"\n📄 Datei: {filename}")
        print(f"📊 Größe: {len(xml_content):,} Zeichen")
        
        print(f"\n🎨 CSS Features:")
        print(f"   ✅ Custom CSS-Klassen pro Element")
        print(f"   ✅ Animationen (fadeIn, slideIn, pulse)")
        print(f"   ✅ Hover-Effekte (scale, rotate, glow)")
        print(f"   ✅ Responsive Design")
        print(f"   ✅ Dark Mode Support") 
        print(f"   ✅ Staggered Animations")
        
        print(f"\n🎯 Applied Styles:")
        print(f"   • Hero: Full-height mit Fade-in Animation")
        print(f"   • Services: Hover-Effekte + Borders")
        print(f"   • Team: Runde Bilder mit Hover-Rotation")
        print(f"   • Contact: Glow-Effekte")
        
        return filename


def main():
    generator = CSSEnhancedGenerator()
    xml_file = generator.generate_complete_styled_xml()
    
    print(f"\n🚀 FERTIG! CSS-Enhanced Website:")
    print(f"   Import: {xml_file}")
    print(f"   Ergebnis: Animierte, responsive RIMAN Website!")

if __name__ == "__main__":
    main()