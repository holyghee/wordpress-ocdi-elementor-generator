#!/usr/bin/env python3
"""
Complete Image Generator
Erzeugt WordPress XML mit Bildern aus YAML
"""

import json
import yaml
from datetime import datetime
from pathlib import Path

class CompleteImageGenerator:
    """
    Generiert komplette WordPress XML mit Bild-Support
    """
    
    def __init__(self):
        self.attachment_id = 200
        self.images = {}
    
    def create_riman_with_images(self):
        """
        Erstellt RIMAN Config mit echten Bildern
        """
        return {
            "page_title": "RIMAN GmbH - Schadstoffsanierung Berlin",
            "hero_title": "Professionelle Schadstoffsanierung in Berlin",
            "hero_subtitle": "Seit 1998 Ihr zuverlässiger Partner",
            
            # Hero mit Background
            "hero_background": {
                "image": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1920&q=80",
                "overlay": "rgba(0,0,0,0.6)"
            },
            
            "company": {
                "name": "RIMAN GmbH",
                "industry": "Schadstoffsanierung",
                "logo": "https://images.unsplash.com/photo-1599305445671-ac291c95aaa9?ixlib=rb-4.0.3&w=200&h=100&fit=crop&auto=format"
            },
            
            # Services mit Bildern
            "services": [
                {
                    "title": "Asbestsanierung",
                    "description": "Sichere und zertifizierte Asbestentfernung nach TRGS 519",
                    "icon": "shield",
                    "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?ixlib=rb-4.0.3&w=400&h=300&fit=crop&auto=format",
                    "color": "#e74c3c"
                },
                {
                    "title": "PCB-Sanierung",
                    "description": "Fachgerechte PCB-Sanierung nach aktuellen Umweltstandards",
                    "icon": "flask",
                    "image": "https://images.unsplash.com/photo-1530587191325-3db32d826c18?ixlib=rb-4.0.3&w=400&h=300&fit=crop&auto=format",
                    "color": "#3498db"
                },
                {
                    "title": "Schimmelsanierung",
                    "description": "Nachhaltige Schimmelbeseitigung und -prävention", 
                    "icon": "home",
                    "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&w=400&h=300&fit=crop&auto=format",
                    "color": "#2ecc71"
                }
            ],
            
            # Team mit Fotos
            "team": [
                {
                    "name": "Thomas Schmidt",
                    "position": "Geschäftsführer",
                    "bio": "25 Jahre Erfahrung in der Schadstoffsanierung",
                    "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&w=300&h=300&fit=crop&auto=format"
                },
                {
                    "name": "Maria Weber", 
                    "position": "Projektleiterin",
                    "bio": "Expertin für komplexe Sanierungsprojekte",
                    "image": "https://images.unsplash.com/photo-1494790108755-2616b332c67c?ixlib=rb-4.0.3&w=300&h=300&fit=crop&auto=format"
                },
                {
                    "name": "Stefan Mueller",
                    "position": "Technischer Leiter", 
                    "bio": "Spezialist für innovative Sanierungsverfahren",
                    "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&w=300&h=300&fit=crop&auto=format"
                }
            ],
            
            # Projekt-Galerie
            "gallery": {
                "title": "Unsere Projekte",
                "images": [
                    {
                        "image": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&w=600&h=400&fit=crop&auto=format",
                        "caption": "Asbestsanierung Bürogebäude Berlin-Mitte"
                    },
                    {
                        "image": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?ixlib=rb-4.0.3&w=600&h=400&fit=crop&auto=format", 
                        "caption": "PCB-Sanierung Industriehalle"
                    },
                    {
                        "image": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?ixlib=rb-4.0.3&w=600&h=400&fit=crop&auto=format",
                        "caption": "Schimmelsanierung Wohnkomplex"
                    }
                ]
            },
            
            "contact": {
                "email": "info@riman-gmbh.de",
                "phone": "030-12345678",
                "address": "Musterstraße 123, 10115 Berlin"
            }
        }
    
    def process_images(self, config):
        """
        Verarbeitet alle Bilder in der Config
        """
        images = {}
        
        # Hero Background
        if 'hero_background' in config and 'image' in config['hero_background']:
            images['hero_bg'] = self.create_image_attachment(
                config['hero_background']['image'], 
                'Hero Background RIMAN GmbH'
            )
        
        # Company Logo
        if 'company' in config and 'logo' in config['company']:
            images['logo'] = self.create_image_attachment(
                config['company']['logo'],
                f"{config['company']['name']} Logo"
            )
        
        # Service Images
        if 'services' in config:
            for i, service in enumerate(config['services']):
                if 'image' in service:
                    images[f'service_{i}'] = self.create_image_attachment(
                        service['image'],
                        f"RIMAN {service['title']} Service"
                    )
        
        # Team Images
        if 'team' in config:
            for i, member in enumerate(config['team']):
                if 'image' in member:
                    images[f'team_{i}'] = self.create_image_attachment(
                        member['image'],
                        f"RIMAN Team - {member['name']}"
                    )
        
        # Gallery Images
        if 'gallery' in config and 'images' in config['gallery']:
            for i, gallery_item in enumerate(config['gallery']['images']):
                if 'image' in gallery_item:
                    images[f'gallery_{i}'] = self.create_image_attachment(
                        gallery_item['image'],
                        gallery_item.get('caption', f'RIMAN Projekt {i+1}')
                    )
        
        self.images = images
        return images
    
    def create_image_attachment(self, url, title):
        """
        Erstellt ein WordPress Image Attachment
        """
        attachment_id = self.attachment_id
        self.attachment_id += 1
        
        # Filename aus URL extrahieren
        filename = url.split('/')[-1].split('?')[0]
        if not filename or '.' not in filename:
            filename = f"riman-image-{attachment_id}.jpg"
        
        return {
            'id': attachment_id,
            'url': url,
            'filename': filename,
            'title': title,
            'alt': title
        }
    
    def create_elementor_structure_with_images(self, config):
        """
        Erstellt Elementor-Struktur mit Bildern
        """
        structure = []
        
        # 1. Hero Section mit Background
        hero = {
            "id": "hero_section",
            "elType": "section",
            "settings": {
                "layout": "full_width",
                "min_height": {"unit": "px", "size": 600},
                "background_background": "classic",
                "background_color": "#232323",
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
                            "desc_typography_font_size": {"unit": "px", "size": 48}
                        }
                    },
                    {
                        "id": "hero_subtitle",
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"<p style='color: white; text-align: center; font-size: 20px;'>{config.get('hero_subtitle', '')}</p>"
                        }
                    }
                ]
            }]
        }
        
        # Hero Background hinzufügen wenn vorhanden
        if 'hero_bg' in self.images:
            hero['settings']['background_image'] = {
                'url': self.images['hero_bg']['url'],
                'id': self.images['hero_bg']['id']
            }
            hero['settings']['background_overlay_background'] = 'classic'
            hero['settings']['background_overlay_color'] = config.get('hero_background', {}).get('overlay', 'rgba(0,0,0,0.6)')
        
        structure.append(hero)
        
        # 2. Services Section
        services_section = {
            "id": "services_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "padding": {"unit": "px", "top": "80", "bottom": "80"}
            },
            "elements": []
        }
        
        # Services Columns
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
            
            # Service-Bild hinzufügen wenn vorhanden
            if f'service_{i}' in self.images:
                column['elements'][0]['settings']['image'] = {
                    'url': self.images[f'service_{i}']['url'],
                    'id': self.images[f'service_{i}']['id']
                }
            
            services_section['elements'].append(column)
        
        structure.append(services_section)
        
        # 3. Team Section
        if config.get('team'):
            team_section = {
                "id": "team_section",
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "background_color": "#f8f9fa",
                    "padding": {"unit": "px", "top": "80", "bottom": "80"}
                },
                "elements": []
            }
            
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
                        "align": "center"
                    }
                }]
            }
            team_section['elements'].append(title_column)
            
            # Team Members
            for i, member in enumerate(config['team']):
                column = {
                    "id": f"team_col_{i}",
                    "elType": "column",
                    "settings": {
                        "_column_size": 33,
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
                            "image": {
                                "url": self.images[f'team_{i}']['url'],
                                "id": self.images[f'team_{i}']['id']
                            } if f'team_{i}' in self.images else {"url": ""}
                        }
                    }]
                }
                team_section['elements'].append(column)
            
            structure.append(team_section)
        
        # 4. Gallery Section
        if config.get('gallery'):
            gallery_section = {
                "id": "gallery_section",
                "elType": "section",
                "settings": {
                    "layout": "boxed",
                    "padding": {"unit": "px", "top": "80", "bottom": "80"}
                },
                "elements": [{
                    "id": "gallery_column",
                    "elType": "column",
                    "settings": {
                        "_column_size": 100,
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "gallery_title",
                            "elType": "widget",
                            "widgetType": "heading",
                            "settings": {
                                "title": config['gallery'].get('title', 'Galerie'),
                                "header_size": "h2",
                                "align": "center"
                            }
                        }
                    ]
                }]
            }
            
            # Gallery Images als Grid
            if 'images' in config['gallery']:
                gallery_images = []
                for key, image in self.images.items():
                    if key.startswith('gallery_'):
                        gallery_images.append({
                            'id': image['id'],
                            'url': image['url']
                        })
                
                if gallery_images:
                    gallery_widget = {
                        "id": "gallery_widget",
                        "elType": "widget",
                        "widgetType": "gallery",
                        "settings": {
                            "gallery": gallery_images,
                            "columns": 3,
                            "columns_mobile": 1,
                            "columns_tablet": 2,
                            "image_size": "medium",
                            "gap": {"size": 20, "unit": "px"}
                        }
                    }
                    gallery_section['elements'][0]['elements'].append(gallery_widget)
            
            structure.append(gallery_section)
        
        # 5. Contact Section
        contact_section = {
            "id": "contact_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "background_color": "#232323",
                "padding": {"unit": "px", "top": "60", "bottom": "60"}
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
                            "title_color": "#ffffff"
                        }
                    },
                    {
                        "id": "contact_info",
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": f"""<p style='color: white; text-align: center;'>
                            📧 {config.get('contact', {}).get('email', '')}<br>
                            📞 {config.get('contact', {}).get('phone', '')}<br>
                            📍 {config.get('contact', {}).get('address', '')}
                            </p>"""
                        }
                    }
                ]
            }]
        }
        structure.append(contact_section)
        
        return structure
    
    def generate_attachments_xml(self):
        """
        Generiert XML für alle Image Attachments
        """
        attachments_xml = []
        
        for image in self.images.values():
            xml = f"""
    <item>
        <title><![CDATA[{image['title']}]]></title>
        <link>{image['url']}</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">?attachment_id={image['id']}</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <wp:post_id>{image['id']}</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_name><![CDATA[{image['filename']}]]></wp:post_name>
        <wp:status><![CDATA[inherit]]></wp:status>
        <wp:post_type><![CDATA[attachment]]></wp:post_type>
        <wp:post_mime_type>image/jpeg</wp:post_mime_type>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_attached_file]]></wp:meta_key>
            <wp:meta_value><![CDATA[2025/08/{image['filename']}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_attachment_image_alt]]></wp:meta_key>
            <wp:meta_value><![CDATA[{image['alt']}]]></wp:meta_value>
        </wp:postmeta>
    </item>"""
            attachments_xml.append(xml)
        
        return attachments_xml
    
    def generate_complete_xml(self):
        """
        Generiert komplette WordPress XML mit Bildern
        """
        print("🚀 COMPLETE IMAGE GENERATOR")
        print("=" * 60)
        
        # Config mit Bildern erstellen
        config = self.create_riman_with_images()
        print(f"✅ Config erstellt mit {len(config.get('services', []))} Services")
        
        # Bilder verarbeiten
        images = self.process_images(config)
        print(f"✅ {len(images)} Bilder verarbeitet")
        
        # Elementor Struktur mit Bildern
        structure = self.create_elementor_structure_with_images(config)
        print(f"✅ {len(structure)} Sections mit Bildern erstellt")
        
        # Attachment XMLs
        attachments = self.generate_attachments_xml()
        print(f"✅ {len(attachments)} Image Attachments generiert")
        
        # Komplette WordPress XML
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>RIMAN GmbH</title>
    <link>https://riman-gmbh.de</link>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    
    <!-- IMAGE ATTACHMENTS -->
    {"".join(attachments)}
    
    <!-- MAIN PAGE -->
    <item>
        <title>RIMAN GmbH - Schadstoffsanierung Berlin</title>
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
        <wp:is_sticky>0</wp:is_sticky>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_edit_mode]]></wp:meta_key>
            <wp:meta_value><![CDATA[builder]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_template_type]]></wp:meta_key>
            <wp:meta_value><![CDATA[wp-page]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_elementor_version]]></wp:meta_key>
            <wp:meta_value><![CDATA[3.17.0]]></wp:meta_value>
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
        
        # Speichere XML
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"riman-with-images-{timestamp}.xml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print("\n" + "=" * 60)
        print("✅ KOMPLETTE XML MIT BILDERN GENERIERT!")
        print("=" * 60)
        
        print(f"\n📄 Datei: {filename}")
        print(f"📊 Größe: {len(xml_content):,} Zeichen")
        print(f"🖼️  Bilder: {len(images)} Attachments")
        
        print(f"\n🎯 Features:")
        print(f"   ✅ Hero Background: Unsplash Industrial Image")
        print(f"   ✅ Service Bilder: 3 thematische Fotos")
        print(f"   ✅ Team Fotos: 3 Profilbilder")
        print(f"   ✅ Projekt Galerie: 3 Beispielprojekte")
        print(f"   ✅ Alle Bilder automatisch herunterladbar")
        
        print(f"\n📋 WordPress Import:")
        print(f"   1. {filename} in WordPress hochladen")
        print(f"   2. 'Download and import file attachments' aktivieren")
        print(f"   3. Import starten")
        print(f"   4. Alle Bilder werden automatisch heruntergeladen")
        
        return filename


def main():
    generator = CompleteImageGenerator()
    xml_file = generator.generate_complete_xml()
    
    print(f"\n🚀 FERTIG! Teste jetzt:")
    print(f"   WordPress Admin → Tools → Import → {xml_file}")

if __name__ == "__main__":
    main()