#!/usr/bin/env python3
"""
WordPress Gutenberg Block Editor Prozessor mit Cholot-Design
Erstellt native WordPress Blocks mit Cholot-Theme-Styling
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from datetime import datetime
import re

class GutenbergCholotProcessor:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = None
        self.generated_pages = []
        self.cholot_colors = {
            'primary': '#b68c2f',  # Cholot Gold
            'secondary': '#333399',  # RIMAN Blau
            'accent': '#FF0000',     # RIMAN Rot
            'dark': '#1a1a1a',
            'light': '#fafafa'
        }
        self.cholot_fonts = {
            'heading': 'Playfair Display',
            'body': 'Source Sans Pro'
        }
    
    def load_config(self) -> bool:
        """Lade YAML-Konfiguration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            print(f"✅ Config geladen: {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Fehler: {e}")
            return False
    
    def create_gutenberg_blocks(self, page_config: Dict) -> str:
        """Erstelle Gutenberg Blocks für eine Seite"""
        blocks = []
        
        for block_config in page_config.get('blocks', []):
            block_type = block_config.get('type')
            
            if block_type == 'hero-slider':
                blocks.append(self._create_hero_section(block_config))
            elif block_type == 'service-cards':
                blocks.append(self._create_service_cards(block_config))
            elif block_type == 'title-section':
                blocks.append(self._create_title_section(block_config))
            elif block_type == 'text-content':
                blocks.append(self._create_text_content(block_config))
            elif block_type == 'team-section':
                blocks.append(self._create_team_section(block_config))
            elif block_type == 'testimonials':
                blocks.append(self._create_testimonials(block_config))
            elif block_type == 'contact-form':
                blocks.append(self._create_contact_form(block_config))
            elif block_type == 'gallery-section':
                blocks.append(self._create_gallery(block_config))
            else:
                print(f"  ⚠️  Block-Typ nicht unterstützt: {block_type}")
        
        return '\n\n'.join(blocks)
    
    def _create_hero_section(self, config: Dict) -> str:
        """Erstelle Hero-Section mit Cholot-Design"""
        slides = config.get('slides', [])
        if not slides:
            return ""
        
        # Verwende Cover-Block für Hero
        slide = slides[0]  # Erste Slide für statischen Hero
        
        hero_block = f"""<!-- wp:cover {{"url":"{slide.get('image', '')}","dimRatio":60,"overlayColor":"dark","minHeight":600,"minHeightUnit":"px","contentPosition":"center center","align":"full","style":{{"spacing":{{"padding":{{"top":"100px","bottom":"100px"}}}}}}}} -->
<div class="wp-block-cover alignfull" style="padding-top:100px;padding-bottom:100px;min-height:600px">
    <span aria-hidden="true" class="wp-block-cover__background has-dark-background-color has-background-dim-60 has-background-dim"></span>
    <img class="wp-block-cover__image-background" alt="" src="{slide.get('image', '')}" data-object-fit="cover"/>
    <div class="wp-block-cover__inner-container">
        <!-- wp:group {{"layout":{{"type":"constrained","contentSize":"1170px"}}}} -->
        <div class="wp-block-group">
            <!-- wp:heading {{"level":1,"style":{{"typography":{{"fontFamily":"Playfair Display","fontSize":"45px","fontWeight":"700"}},"color":{{"text":"#ffffff"}},"spacing":{{"margin":{{"bottom":"20px"}}}}}}}} -->
            <h1 class="wp-block-heading" style="color:#ffffff;margin-bottom:20px;font-family:Playfair Display;font-size:45px;font-weight:700">{slide.get('title', '')}</h1>
            <!-- /wp:heading -->
            
            <!-- wp:paragraph {{"style":{{"typography":{{"fontSize":"15px","fontWeight":"700","textTransform":"uppercase","letterSpacing":"2px"}},"color":{{"text":"#b68c2f"}},"spacing":{{"margin":{{"bottom":"30px"}}}}}}}} -->
            <p style="color:#b68c2f;margin-bottom:30px;font-size:15px;font-weight:700;letter-spacing:2px;text-transform:uppercase">{slide.get('subtitle', '')}</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:paragraph {{"style":{{"typography":{{"fontSize":"18px"}},"color":{{"text":"rgba(255,255,255,0.89)"}},"spacing":{{"margin":{{"bottom":"40px"}}}}}}}} -->
            <p style="color:rgba(255,255,255,0.89);margin-bottom:40px;font-size:18px">{slide.get('text', '')}</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {{"style":{{"border":{{"radius":"0px","width":"1px"}},"color":{{"background":"transparent","text":"#ffffff"}},"spacing":{{"padding":{{"top":"12px","bottom":"12px","left":"30px","right":"30px"}}}},"className":"is-style-outline"}} -->
                <div class="wp-block-button is-style-outline">
                    <a class="wp-block-button__link wp-element-button" href="{slide.get('button_link', '#')}" style="border-width:1px;border-radius:0px;color:#ffffff;background-color:transparent;padding-top:12px;padding-right:30px;padding-bottom:12px;padding-left:30px">{slide.get('button_text', 'Mehr erfahren')}</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:group -->
    </div>
</div>
<!-- /wp:cover -->"""
        
        return hero_block
    
    def _create_service_cards(self, config: Dict) -> str:
        """Erstelle Service Cards mit Cholot-Styling"""
        services = config.get('services', [])
        columns = config.get('columns', 3)
        
        cards_html = []
        for service in services:
            card = f"""<!-- wp:column {{"style":{{"spacing":{{"padding":{{"top":"30px","right":"30px","bottom":"30px","left":"30px"}}}},"border":{{"width":"1px","style":"dashed","color":"#b68c2f"}}}}}} -->
<div class="wp-block-column" style="border-style:dashed;border-color:#b68c2f;border-width:1px;padding-top:30px;padding-right:30px;padding-bottom:30px;padding-left:30px">
    <!-- wp:group {{"layout":{{"type":"flex","flexWrap":"nowrap"}}}} -->
    <div class="wp-block-group">
        <!-- wp:html -->
        <div style="width:32px;height:32px;background-color:#b68c2f;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-right:15px">
            <i class="{service.get('icon', 'fa fa-check')}" style="color:#ffffff;font-size:14px"></i>
        </div>
        <!-- /wp:html -->
        
        <!-- wp:group -->
        <div class="wp-block-group">
            <!-- wp:paragraph {{"style":{{"typography":{{"fontSize":"13px","fontWeight":"700","textTransform":"uppercase","letterSpacing":"1px"}},"color":{{"text":"#b68c2f"}},"spacing":{{"margin":{{"bottom":"10px"}}}}}}}} -->
            <p style="color:#b68c2f;margin-bottom:10px;font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase">{service.get('subtitle', '')}</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:heading {{"level":3,"style":{{"typography":{{"fontSize":"20px"}},"spacing":{{"margin":{{"bottom":"15px"}}}}}}}} -->
            <h3 class="wp-block-heading" style="margin-bottom:15px;font-size:20px">{service.get('title', '')}</h3>
            <!-- /wp:heading -->
            
            <!-- wp:paragraph {{"style":{{"typography":{{"fontSize":"15px","fontStyle":"italic"}}}}}} -->
            <p style="font-size:15px;font-style:italic">{service.get('text', '')}</p>
            <!-- /wp:paragraph -->
        </div>
        <!-- /wp:group -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:column -->"""
            cards_html.append(card)
        
        # Wrap in columns block
        service_cards_block = f"""<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"60px","bottom":"60px"}}}},"color":{{"background":"#ffffff"}}}}}} -->
<div class="wp-block-group alignfull" style="background-color:#ffffff;padding-top:60px;padding-bottom:60px">
    <!-- wp:group {{"layout":{{"type":"constrained","contentSize":"1170px"}}}} -->
    <div class="wp-block-group">
        {self._create_section_header(config)}
        
        <!-- wp:columns {{"columns":{columns}}} -->
        <div class="wp-block-columns">
            {''.join(cards_html)}
        </div>
        <!-- /wp:columns -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->"""
        
        return service_cards_block
    
    def _create_title_section(self, config: Dict) -> str:
        """Erstelle Title Section"""
        return f"""<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"60px","bottom":"60px"}}}}}}}} -->
<div class="wp-block-group alignfull" style="padding-top:60px;padding-bottom:60px">
    <!-- wp:group {{"layout":{{"type":"constrained","contentSize":"800px"}}}} -->
    <div class="wp-block-group">
        <!-- wp:paragraph {{"align":"center","style":{{"typography":{{"fontSize":"15px","fontWeight":"700","textTransform":"uppercase"}},"color":{{"text":"#b68c2f"}},"spacing":{{"margin":{{"bottom":"10px"}}}}}}}} -->
        <p class="has-text-align-center" style="color:#b68c2f;margin-bottom:10px;font-size:15px;font-weight:700;text-transform:uppercase">{config.get('subtitle', '')}</p>
        <!-- /wp:paragraph -->
        
        <!-- wp:heading {{"textAlign":"center","style":{{"typography":{{"fontFamily":"Playfair Display","fontSize":"35px","fontWeight":"700"}},"spacing":{{"margin":{{"bottom":"20px"}}}}}}}} -->
        <h2 class="wp-block-heading has-text-align-center" style="margin-bottom:20px;font-family:Playfair Display;font-size:35px;font-weight:700">{config.get('title', '')}</h2>
        <!-- /wp:heading -->
        
        <!-- wp:separator {{"style":{{"color":{{"background":"#b68c2f"}},"spacing":{{"margin":{{"top":"20px","bottom":"20px"}}}},"className":"is-style-default"}} -->
        <hr class="wp-block-separator has-alpha-channel-opacity has-background is-style-default" style="background-color:#b68c2f;margin-top:20px;margin-bottom:20px"/>
        <!-- /wp:separator -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->"""
    
    def _create_text_content(self, config: Dict) -> str:
        """Erstelle Text-Content Block"""
        content = config.get('content', '')
        
        return f"""<!-- wp:group {{"align":"wide","style":{{"spacing":{{"padding":{{"top":"40px","bottom":"40px"}}}}}}}} -->
<div class="wp-block-group alignwide" style="padding-top:40px;padding-bottom:40px">
    <!-- wp:html -->
    {content}
    <!-- /wp:html -->
</div>
<!-- /wp:group -->"""
    
    def _create_team_section(self, config: Dict) -> str:
        """Erstelle Team Section"""
        members = config.get('members', [])
        
        team_cards = []
        for member in members:
            card = f"""<!-- wp:column -->
<div class="wp-block-column">
    <!-- wp:image {{"sizeSlug":"large","linkDestination":"none","style":{{"border":{{"radius":"5px"}}}}}} -->
    <figure class="wp-block-image size-large" style="border-radius:5px">
        <img src="{member.get('image', '')}" alt="{member.get('name', '')}"/>
    </figure>
    <!-- /wp:image -->
    
    <!-- wp:heading {{"level":3,"style":{{"typography":{{"fontSize":"24px"}},"spacing":{{"margin":{{"top":"20px","bottom":"10px"}}}}}}}} -->
    <h3 class="wp-block-heading" style="margin-top:20px;margin-bottom:10px;font-size:24px">{member.get('name', '')}</h3>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph {{"style":{{"color":{{"text":"#b68c2f"}},"typography":{{"fontSize":"14px","fontWeight":"600"}},"spacing":{{"margin":{{"bottom":"15px"}}}}}}}} -->
    <p style="color:#b68c2f;margin-bottom:15px;font-size:14px;font-weight:600">{member.get('position', '')}</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:paragraph {{"style":{{"typography":{{"fontSize":"15px"}}}}}} -->
    <p style="font-size:15px">{member.get('bio', '')}</p>
    <!-- /wp:paragraph -->
</div>
<!-- /wp:column -->"""
            team_cards.append(card)
        
        return f"""<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"80px","bottom":"80px"}}}},"color":{{"background":"#fafafa"}}}}}} -->
<div class="wp-block-group alignfull" style="background-color:#fafafa;padding-top:80px;padding-bottom:80px">
    <!-- wp:group {{"layout":{{"type":"constrained","contentSize":"1170px"}}}} -->
    <div class="wp-block-group">
        {self._create_section_header(config)}
        
        <!-- wp:columns {{"columns":3}} -->
        <div class="wp-block-columns">
            {''.join(team_cards)}
        </div>
        <!-- /wp:columns -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->"""
    
    def _create_testimonials(self, config: Dict) -> str:
        """Erstelle Testimonials Section"""
        testimonials = config.get('testimonials', [])
        
        testimonial_blocks = []
        for testimonial in testimonials:
            block = f"""<!-- wp:column {{"style":{{"spacing":{{"padding":{{"top":"30px","right":"30px","bottom":"30px","left":"30px"}}}},"color":{{"background":"#ffffff"}},"border":{{"radius":"5px"}}}}}} -->
<div class="wp-block-column" style="border-radius:5px;background-color:#ffffff;padding-top:30px;padding-right:30px;padding-bottom:30px;padding-left:30px">
    <!-- wp:quote {{"style":{{"typography":{{"fontSize":"16px","fontStyle":"italic"}},"spacing":{{"margin":{{"bottom":"20px"}}}}}}}} -->
    <blockquote class="wp-block-quote" style="margin-bottom:20px;font-size:16px;font-style:italic">
        <p>{testimonial.get('text', '')}</p>
        <cite>
            <strong>{testimonial.get('author', '')}</strong><br>
            {testimonial.get('position', '')}
        </cite>
    </blockquote>
    <!-- /wp:quote -->
    
    <!-- wp:html -->
    <div style="color:#b68c2f">
        {'⭐' * testimonial.get('rating', 5)}
    </div>
    <!-- /wp:html -->
</div>
<!-- /wp:column -->"""
            testimonial_blocks.append(block)
        
        return f"""<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"80px","bottom":"80px"}}}},"color":{{"background":"#f5f5f5"}}}}}} -->
<div class="wp-block-group alignfull" style="background-color:#f5f5f5;padding-top:80px;padding-bottom:80px">
    <!-- wp:group {{"layout":{{"type":"constrained","contentSize":"1170px"}}}} -->
    <div class="wp-block-group">
        {self._create_section_header(config)}
        
        <!-- wp:columns {{"columns":3}} -->
        <div class="wp-block-columns">
            {''.join(testimonial_blocks)}
        </div>
        <!-- /wp:columns -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->"""
    
    def _create_contact_form(self, config: Dict) -> str:
        """Erstelle Contact Form"""
        return f"""<!-- wp:group {{"align":"full","style":{{"spacing":{{"padding":{{"top":"80px","bottom":"80px"}}}},"color":{{"background":"#ffffff"}}}}}} -->
<div class="wp-block-group alignfull" style="background-color:#ffffff;padding-top:80px;padding-bottom:80px">
    <!-- wp:group {{"layout":{{"type":"constrained","contentSize":"800px"}}}} -->
    <div class="wp-block-group">
        {self._create_section_header(config)}
        
        <!-- wp:contact-form-7/contact-form-selector {{"title":"Kontaktformular"}} -->
        <div class="wp-block-contact-form-7-contact-form-selector">
            [contact-form-7 title="Kontaktformular"]
        </div>
        <!-- /wp:contact-form-7/contact-form-selector -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->"""
    
    def _create_gallery(self, config: Dict) -> str:
        """Erstelle Gallery Section"""
        images = config.get('images', [])
        
        gallery_items = []
        for img in images:
            gallery_items.append(f'{{"url":"{img}"}}')
        
        return f"""<!-- wp:gallery {{"columns":3,"imageCrop":true,"linkTo":"none","sizeSlug":"large","align":"wide"}} -->
<figure class="wp-block-gallery alignwide has-nested-images columns-3 is-cropped">
    {' '.join([f'<!-- wp:image {{"sizeSlug":"large","linkDestination":"none"}} --><figure class="wp-block-image size-large"><img src="{img}" alt=""/></figure><!-- /wp:image -->' for img in images])}
</figure>
<!-- /wp:gallery -->"""
    
    def _create_section_header(self, config: Dict) -> str:
        """Erstelle Section Header für wiederverwendbare Titel"""
        title = config.get('title', '')
        subtitle = config.get('subtitle', '')
        
        if not title:
            return ""
        
        return f"""<!-- wp:group {{"layout":{{"type":"constrained"}},"style":{{"spacing":{{"margin":{{"bottom":"50px"}}}}}}}} -->
<div class="wp-block-group" style="margin-bottom:50px">
    {f'<!-- wp:paragraph {{"align":"center","style":{{"typography":{{"fontSize":"15px","fontWeight":"700","textTransform":"uppercase","letterSpacing":"1px"}},"color":{{"text":"#b68c2f"}}}}}} --><p class="has-text-align-center" style="color:#b68c2f;font-size:15px;font-weight:700;letter-spacing:1px;text-transform:uppercase">{subtitle}</p><!-- /wp:paragraph -->' if subtitle else ''}
    
    <!-- wp:heading {{"textAlign":"center","style":{{"typography":{{"fontFamily":"Playfair Display","fontSize":"35px","fontWeight":"700"}},"spacing":{{"margin":{{"top":"10px","bottom":"20px"}}}}}}}} -->
    <h2 class="wp-block-heading has-text-align-center" style="margin-top:10px;margin-bottom:20px;font-family:Playfair Display;font-size:35px;font-weight:700">{title}</h2>
    <!-- /wp:heading -->
    
    <!-- wp:separator {{"style":{{"width":{{"value":"50px"}},"color":{{"background":"#b68c2f"}}}},"className":"is-style-default aligncenter"}} -->
    <hr class="wp-block-separator has-alpha-channel-opacity has-background is-style-default aligncenter" style="background-color:#b68c2f;width:50px"/>
    <!-- /wp:separator -->
</div>
<!-- /wp:group -->"""
    
    def generate_wordpress_xml(self, output_file: str):
        """Generiere WordPress XML mit Gutenberg Blocks"""
        # XML-Struktur
        root = ET.Element('rss', {
            'version': '2.0',
            'xmlns:excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:wfw': 'http://wellformedweb.org/CommentAPI/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:wp': 'http://wordpress.org/export/1.2/'
        })
        
        channel = ET.SubElement(root, 'channel')
        
        # Site-Info
        site_config = self.config.get('site', {})
        ET.SubElement(channel, 'title').text = site_config.get('title', 'RIMAN GmbH')
        ET.SubElement(channel, 'link').text = site_config.get('url', 'http://localhost:8081')
        ET.SubElement(channel, 'description').text = site_config.get('description', '')
        ET.SubElement(channel, 'language').text = 'de-DE'
        ET.SubElement(channel, 'wp:wxr_version').text = '1.2'
        
        # Autor
        author = ET.SubElement(channel, 'wp:author')
        ET.SubElement(author, 'wp:author_id').text = '1'
        ET.SubElement(author, 'wp:author_login').text = 'admin'
        ET.SubElement(author, 'wp:author_email').text = 'admin@example.com'
        ET.SubElement(author, 'wp:author_display_name').text = 'Administrator'
        
        # Custom CSS für Cholot-Styling
        self._add_custom_css_to_xml(channel)
        
        # Generiere Seiten
        page_id = 2000
        for page_config in self.config.get('pages', []):
            self._add_gutenberg_page_to_xml(channel, page_config, page_id)
            page_id += 1
            self.generated_pages.append(page_config)
        
        # XML formatieren und speichern
        tree = ET.ElementTree(root)
        ET.indent(tree, '  ')
        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        
        # Dateigröße
        file_size = Path(output_file).stat().st_size
        print(f"✅ XML generiert: {output_file} ({file_size} bytes)")
        print(f"📊 {len(self.generated_pages)} Gutenberg-Seiten erstellt")
    
    def _add_custom_css_to_xml(self, channel):
        """Füge Custom CSS für Cholot-Styling hinzu"""
        css_content = """
/* Cholot-Theme Styling für Gutenberg Blocks */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600;700&display=swap');

body {
    font-family: 'Source Sans Pro', sans-serif;
    color: #333333;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    line-height: 1.2;
}

.wp-block-button__link {
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

.wp-block-button__link:hover {
    background-color: #b68c2f !important;
    border-color: #b68c2f !important;
}

.wp-block-cover__inner-container {
    max-width: 1170px;
    margin: 0 auto;
}

.wp-block-separator {
    height: 2px;
    border: none;
}

/* Font Awesome Integration */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
"""
        
        # Als WordPress Option speichern
        item = ET.SubElement(channel, 'wp:option')
        ET.SubElement(item, 'wp:option_key').text = 'custom_css_cholot_gutenberg'
        ET.SubElement(item, 'wp:option_value').text = css_content
    
    def _add_gutenberg_page_to_xml(self, channel, page_config: Dict, page_id: int):
        """Füge Gutenberg-Seite zur XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = page_config.get('title', 'Untitled')
        ET.SubElement(item, 'link').text = f"http://localhost:8081/{page_config.get('slug', '')}"
        ET.SubElement(item, 'dc:creator').text = 'admin'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"http://localhost:8081/?page_id={page_id}"
        ET.SubElement(item, 'description').text = ''
        
        # Gutenberg Block Content
        blocks_content = self.create_gutenberg_blocks(page_config)
        ET.SubElement(item, 'content:encoded').text = blocks_content
        
        ET.SubElement(item, 'wp:post_id').text = str(page_id)
        ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, 'wp:post_name').text = page_config.get('slug', '')
        ET.SubElement(item, 'wp:status').text = 'publish'
        ET.SubElement(item, 'wp:post_type').text = 'page'
        
        # Page Template
        postmeta = ET.SubElement(item, 'wp:postmeta')
        ET.SubElement(postmeta, 'wp:meta_key').text = '_wp_page_template'
        ET.SubElement(postmeta, 'wp:meta_value').text = 'default'
        
        print(f"  ✅ Gutenberg-Seite erstellt: {page_config.get('title', 'Untitled')}")
    
    def run(self):
        """Hauptausführung"""
        print("\n🚀 WordPress Gutenberg Block Editor Prozessor")
        print("    mit Cholot-Theme-Design")
        print("="*60)
        
        # Lade Config
        if not self.load_config():
            return False
        
        # Generiere XML
        print("\n📝 Generiere WordPress XML mit Gutenberg Blocks...")
        output_file = 'gutenberg-cholot-output.xml'
        self.generate_wordpress_xml(output_file)
        
        print(f"\n✅ Fertig! Gutenberg-Seiten mit Cholot-Design erstellt.")
        print(f"   Output: {output_file}")
        print(f"\n💡 Diese Version benötigt kein Elementor!")
        print(f"   Alle Blocks sind native WordPress Gutenberg Blocks.")
        
        return True

def main():
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'riman-cholot-intelligent.yaml'
    processor = GutenbergCholotProcessor(config_file)
    processor.run()

if __name__ == "__main__":
    main()