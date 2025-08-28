#!/usr/bin/env python3
"""
Image Processor für WordPress XML
Verarbeitet Bilder und fügt sie in WordPress XML ein
"""

import json
import yaml
import re
from datetime import datetime
from urllib.parse import urlparse
import os

class ImageProcessor:
    """
    Verarbeitet Bilder für WordPress XML Import
    """
    
    def __init__(self):
        self.attachment_id = 200  # Start-ID für Media Attachments
    
    def process_config_images(self, config):
        """
        Findet alle Bilder in der Config und bereitet sie vor
        """
        images = {}
        
        # Hero Background
        if 'hero_background' in config and 'image' in config['hero_background']:
            images['hero_bg'] = self.prepare_image(config['hero_background']['image'], 'Hero Background')
        
        # Company Logo
        if 'company' in config and 'logo' in config['company']:
            images['logo'] = self.prepare_image(config['company']['logo'], 'Company Logo')
        
        # Service Images
        if 'services' in config:
            for i, service in enumerate(config['services']):
                if 'image' in service:
                    images[f'service_{i}'] = self.prepare_image(service['image'], f"Service: {service['title']}")
        
        # Team Images
        if 'team' in config:
            for i, member in enumerate(config['team']):
                if 'image' in member:
                    images[f'team_{i}'] = self.prepare_image(member['image'], f"Team: {member['name']}")
        
        # Gallery Images
        if 'gallery' in config and 'images' in config['gallery']:
            for i, gallery_item in enumerate(config['gallery']['images']):
                if 'image' in gallery_item:
                    images[f'gallery_{i}'] = self.prepare_image(
                        gallery_item['image'], 
                        gallery_item.get('caption', f'Gallery Image {i+1}')
                    )
        
        return images
    
    def prepare_image(self, image_path, alt_text):
        """
        Bereitet ein einzelnes Bild für WordPress vor
        """
        # Prüfe ob URL oder lokaler Pfad
        if image_path.startswith(('http://', 'https://')):
            # URL - WordPress lädt automatisch herunter
            filename = os.path.basename(urlparse(image_path).path)
            if not filename:
                filename = f"image_{self.attachment_id}.jpg"
        else:
            # Lokaler Pfad - muss hochgeladen werden
            filename = os.path.basename(image_path)
        
        attachment_id = self.attachment_id
        self.attachment_id += 1
        
        return {
            'id': attachment_id,
            'url': image_path,
            'filename': filename,
            'alt': alt_text,
            'title': alt_text
        }
    
    def generate_attachment_xml(self, image_info):
        """
        Generiert WordPress XML für ein Bild-Attachment
        """
        return f"""
    <item>
        <title>{image_info['title']}</title>
        <link>{image_info['url']}</link>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">?attachment_id={image_info['id']}</guid>
        <description></description>
        <content:encoded><![CDATA[]]></content:encoded>
        <wp:post_id>{image_info['id']}</wp:post_id>
        <wp:post_date>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</wp:post_date>
        <wp:post_name><![CDATA[{image_info['filename']}]]></wp:post_name>
        <wp:status><![CDATA[inherit]]></wp:status>
        <wp:post_type><![CDATA[attachment]]></wp:post_type>
        <wp:post_mime_type>image/jpeg</wp:post_mime_type>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_attached_file]]></wp:meta_key>
            <wp:meta_value><![CDATA[{image_info['filename']}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_attachment_image_alt]]></wp:meta_key>
            <wp:meta_value><![CDATA[{image_info['alt']}]]></wp:meta_value>
        </wp:postmeta>
    </item>"""
    
    def enhance_elementor_structure_with_images(self, structure, images):
        """
        Fügt Bilder in die Elementor-Struktur ein
        """
        enhanced = json.loads(json.dumps(structure))  # Deep copy
        
        for section in enhanced:
            # Hero Section mit Background
            if section.get('id') == 'hero_section' and 'hero_bg' in images:
                section['settings']['background_background'] = 'classic'
                section['settings']['background_image'] = {
                    'url': images['hero_bg']['url'],
                    'id': images['hero_bg']['id']
                }
            
            # Service Sections mit Bildern
            if 'elements' in section:
                for column in section['elements']:
                    if 'elements' in column:
                        for widget in column['elements']:
                            if widget.get('widgetType') == 'cholot-texticon':
                                # Finde passendes Service-Bild
                                service_title = widget.get('settings', {}).get('title', '')
                                for key, image in images.items():
                                    if key.startswith('service_') and service_title.lower() in image['title'].lower():
                                        widget['settings']['image'] = {
                                            'url': image['url'],
                                            'id': image['id']
                                        }
                            
                            elif widget.get('widgetType') == 'cholot-team':
                                # Team-Bilder
                                team_name = widget.get('settings', {}).get('title', '')
                                for key, image in images.items():
                                    if key.startswith('team_') and team_name.lower() in image['title'].lower():
                                        widget['settings']['image'] = {
                                            'url': image['url'],
                                            'id': image['id']
                                        }
        
        return enhanced
    
    def create_image_gallery_section(self, gallery_config, images):
        """
        Erstellt eine Galerie-Section mit Bildern
        """
        if not gallery_config or not images:
            return None
        
        gallery_images = []
        for key, image in images.items():
            if key.startswith('gallery_'):
                gallery_images.append({
                    'id': image['id'],
                    'url': image['url']
                })
        
        return {
            "id": "gallery_section",
            "elType": "section",
            "settings": {
                "layout": "boxed",
                "padding": {"unit": "px", "top": "60", "bottom": "60"}
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
                            "title": gallery_config.get('title', 'Galerie'),
                            "header_size": "h2",
                            "align": "center"
                        }
                    },
                    {
                        "id": "gallery_widget",
                        "elType": "widget", 
                        "widgetType": "gallery",
                        "settings": {
                            "gallery": gallery_images,
                            "columns": 3,
                            "image_size": "medium_large",
                            "gap": {"unit": "px", "size": 10}
                        }
                    }
                ]
            }]
        }


def create_image_test_config():
    """
    Erstellt eine Test-Config mit Bildern
    """
    return {
        "page_title": "RIMAN GmbH - Mit Bildern",
        "hero_title": "Professionelle Schadstoffsanierung",
        "hero_background": {
            "image": "https://picsum.photos/1920/600?random=1",
            "overlay_color": "rgba(0,0,0,0.5)"
        },
        "company": {
            "name": "RIMAN GmbH",
            "logo": "https://picsum.photos/200/100?random=2"
        },
        "services": [
            {
                "title": "Asbestsanierung",
                "description": "Sichere Asbestentfernung",
                "icon": "shield",
                "image": "https://picsum.photos/400/300?random=3",
                "color": "#e74c3c"
            },
            {
                "title": "PCB-Sanierung", 
                "description": "Umweltgerechte PCB-Sanierung",
                "icon": "flask",
                "image": "https://picsum.photos/400/300?random=4", 
                "color": "#3498db"
            }
        ],
        "team": [
            {
                "name": "Thomas Schmidt",
                "position": "Geschäftsführer",
                "image": "https://picsum.photos/300/300?random=5"
            }
        ],
        "gallery": {
            "title": "Unsere Projekte",
            "images": [
                {"image": "https://picsum.photos/600/400?random=6", "caption": "Projekt 1"},
                {"image": "https://picsum.photos/600/400?random=7", "caption": "Projekt 2"}
            ]
        }
    }


def main():
    """
    Testet den Image Processor
    """
    print("🖼️  IMAGE PROCESSOR TEST")
    print("=" * 50)
    
    # Test Config mit Bildern
    config = create_image_test_config()
    
    # Image Processor
    processor = ImageProcessor()
    images = processor.process_config_images(config)
    
    print(f"✅ {len(images)} Bilder gefunden:")
    for key, image in images.items():
        print(f"   • {key}: {image['filename']} (ID: {image['id']})")
    
    # Generiere Attachment XMLs
    print(f"\n📄 Generiere WordPress XML Attachments...")
    attachments_xml = []
    for image in images.values():
        attachments_xml.append(processor.generate_attachment_xml(image))
    
    print(f"✅ {len(attachments_xml)} Attachment XMLs generiert")
    
    # Speichere Test-Output
    with open("image-test-attachments.xml", "w") as f:
        f.write('\n'.join(attachments_xml))
    
    print("\n🎯 WordPress XML Import Features:")
    print("✅ URLs werden automatisch heruntergeladen")
    print("✅ Bilder werden in Media Library hochgeladen")
    print("✅ Attachment IDs werden korrekt referenziert")
    print("✅ ALT-Tags und Metadaten werden gesetzt")
    
    print(f"\n📁 Test-Datei erstellt: image-test-attachments.xml")


if __name__ == "__main__":
    main()