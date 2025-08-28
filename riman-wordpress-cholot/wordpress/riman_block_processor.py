#!/usr/bin/env python3
"""
RIMAN Website Block Processor
Erweiterte Version des intelligenten Block-Processors für RIMAN Relaunch
"""

import json
import yaml
import copy
from pathlib import Path
from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from datetime import datetime
import re

class RIMANBlockProcessor:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = None
        self.blocks = {}
        self.block_library_path = Path("block_library")
        self.generated_pages = []
        self.generated_posts = []
        self.generated_menus = []
        
    def load_config(self) -> bool:
        """Lade YAML-Konfiguration"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            print(f"✅ Config geladen: {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Laden der Config: {e}")
            return False
    
    def load_block_library(self):
        """Lade Block-Library mit erweiterten Block-Typen"""
        if not self.block_library_path.exists():
            print("⚠️  Block-Library nicht gefunden, erstelle Standard-Blocks...")
            self.create_default_blocks()
            return
            
        # Lade existierende Blocks
        for block_file in self.block_library_path.glob("*.json"):
            with open(block_file, 'r', encoding='utf-8') as f:
                block_data = json.load(f)
                block_type = block_data.get('type', 'unknown')
                
                if block_type not in self.blocks:
                    self.blocks[block_type] = []
                    
                self.blocks[block_type].append(block_data)
        
        # Erstelle zusätzliche RIMAN-spezifische Blocks
        self.create_riman_blocks()
        
        print(f"✅ {len(self.blocks)} Block-Typen geladen")
    
    def create_riman_blocks(self):
        """Erstelle RIMAN-spezifische Block-Templates"""
        
        # Alert Box Block
        self.blocks['alert-box'] = [{
            'type': 'alert-box',
            'structure': self.create_alert_box_template()
        }]
        
        # Statistics Block
        self.blocks['statistics'] = [{
            'type': 'statistics',
            'structure': self.create_statistics_template()
        }]
        
        # Process Steps Block
        self.blocks['process-steps'] = [{
            'type': 'process-steps',
            'structure': self.create_process_steps_template()
        }]
        
        # CTA Section
        self.blocks['cta-section'] = [{
            'type': 'cta-section',
            'structure': self.create_cta_template()
        }]
        
        # Info Boxes
        self.blocks['info-boxes'] = [{
            'type': 'info-boxes',
            'structure': self.create_info_boxes_template()
        }]
        
        # Timeline
        self.blocks['timeline'] = [{
            'type': 'timeline',
            'structure': self.create_timeline_template()
        }]
        
        # Tabbed Content
        self.blocks['tabbed-content'] = [{
            'type': 'tabbed-content',
            'structure': self.create_tabbed_content_template()
        }]
        
        # Portfolio Grid
        self.blocks['portfolio-grid'] = [{
            'type': 'portfolio-grid',
            'structure': self.create_portfolio_grid_template()
        }]
        
        # Blog Grid
        self.blocks['blog-grid'] = [{
            'type': 'blog-grid',
            'structure': self.create_blog_grid_template()
        }]
        
        # Contact Info
        self.blocks['contact-info'] = [{
            'type': 'contact-info',
            'structure': self.create_contact_info_template()
        }]
        
        # Contact Form
        self.blocks['contact-form'] = [{
            'type': 'contact-form',
            'structure': self.create_contact_form_template()
        }]
        
        # Map
        self.blocks['map'] = [{
            'type': 'map',
            'structure': self.create_map_template()
        }]
        
        # Download Section
        self.blocks['download-section'] = [{
            'type': 'download-section',
            'structure': self.create_download_section_template()
        }]
        
        # Breadcrumb
        self.blocks['breadcrumb'] = [{
            'type': 'breadcrumb',
            'structure': self.create_breadcrumb_template()
        }]
        
        # Text Image Block
        self.blocks['text-image'] = [{
            'type': 'text-image',
            'structure': self.create_text_image_template()
        }]
        
        # Image Text Block (reverse)
        self.blocks['image-text'] = [{
            'type': 'image-text',
            'structure': self.create_image_text_template()
        }]
        
        # Certifications Block
        self.blocks['certifications'] = [{
            'type': 'certifications',
            'structure': self.create_certifications_template()
        }]
        
        # Process Timeline
        self.blocks['process-timeline'] = [{
            'type': 'process-timeline',
            'structure': self.create_process_timeline_template()
        }]
        
        print(f"✅ RIMAN-spezifische Blocks erstellt")
    
    def create_alert_box_template(self) -> Dict:
        """Template für Alert/Warning Boxes"""
        return {
            "elType": "section",
            "settings": {
                "background_background": "classic",
                "background_color": "{{ALERT_COLOR}}"
            },
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "cholot-title",
                    "settings": {
                        "title": "{{ALERT_TITLE}}",
                        "subtitle": "{{ALERT_TEXT}}",
                        "icon": "{{ALERT_ICON}}"
                    }
                }]
            }]
        }
    
    def create_statistics_template(self) -> Dict:
        """Template für Statistik-Blöcke"""
        return {
            "elType": "section",
            "settings": {
                "background_background": "classic",
                "background_overlay_background": "classic"
            },
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "counter",
                    "settings": {
                        "ending_number": "{{STAT_NUMBER}}",
                        "prefix": "{{STAT_PREFIX}}",
                        "suffix": "{{STAT_SUFFIX}}",
                        "title": "{{STAT_LABEL}}"
                    }
                }]
            }]
        }
    
    def create_process_steps_template(self) -> Dict:
        """Template für Prozess-Schritte"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "icon-box",
                    "settings": {
                        "title_text": "{{STEP_TITLE}}",
                        "description_text": "{{STEP_TEXT}}",
                        "selected_icon": {"value": "{{STEP_ICON}}"}
                    }
                }]
            }]
        }
    
    def create_cta_template(self) -> Dict:
        """Template für Call-to-Action Sections"""
        return {
            "elType": "section",
            "settings": {
                "background_background": "classic",
                "background_color": "{{CTA_BG_COLOR}}"
            },
            "elements": [{
                "elType": "column",
                "elements": [
                    {
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "{{CTA_TITLE}}",
                            "header_size": "h2"
                        }
                    },
                    {
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "{{CTA_SUBTITLE}}"
                        }
                    },
                    {
                        "elType": "widget",
                        "widgetType": "button",
                        "settings": {
                            "text": "{{CTA_BUTTON_TEXT}}",
                            "link": {"url": "{{CTA_BUTTON_LINK}}"}
                        }
                    }
                ]
            }]
        }
    
    def create_info_boxes_template(self) -> Dict:
        """Template für Info-Boxen"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "icon-box",
                    "settings": {
                        "title_text": "{{INFO_TITLE}}",
                        "description_text": "{{INFO_TEXT}}",
                        "selected_icon": {"value": "{{INFO_ICON}}"},
                        "primary_color": "{{INFO_COLOR}}"
                    }
                }]
            }]
        }
    
    def create_timeline_template(self) -> Dict:
        """Template für Timeline/Geschichte"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": "<div class='timeline-item'><h3>{{TIMELINE_YEAR}}</h3><h4>{{TIMELINE_TITLE}}</h4><p>{{TIMELINE_TEXT}}</p></div>"
                    }
                }]
            }]
        }
    
    def create_tabbed_content_template(self) -> Dict:
        """Template für Tabs"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "tabs",
                    "settings": {
                        "tabs": [
                            {
                                "tab_title": "{{TAB_TITLE}}",
                                "tab_content": "{{TAB_CONTENT}}"
                            }
                        ]
                    }
                }]
            }]
        }
    
    def create_portfolio_grid_template(self) -> Dict:
        """Template für Portfolio/Referenz-Grid"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "portfolio",
                    "settings": {
                        "posts_per_page": 6,
                        "show_title": "yes",
                        "show_excerpt": "yes"
                    }
                }]
            }]
        }
    
    def create_blog_grid_template(self) -> Dict:
        """Template für Blog-Grid"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "posts",
                    "settings": {
                        "posts_per_page": 3,
                        "show_title": "yes",
                        "show_excerpt": "yes",
                        "show_read_more": "yes"
                    }
                }]
            }]
        }
    
    def create_contact_info_template(self) -> Dict:
        """Template für Kontakt-Informationen"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "icon-list",
                    "settings": {
                        "icon_list": [
                            {
                                "text": "{{CONTACT_ADDRESS}}",
                                "selected_icon": {"value": "fa fa-map-marker-alt"}
                            },
                            {
                                "text": "{{CONTACT_PHONE}}",
                                "selected_icon": {"value": "fa fa-phone"}
                            },
                            {
                                "text": "{{CONTACT_EMAIL}}",
                                "selected_icon": {"value": "fa fa-envelope"}
                            }
                        ]
                    }
                }]
            }]
        }
    
    def create_contact_form_template(self) -> Dict:
        """Template für Kontaktformular"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "form",
                    "settings": {
                        "form_name": "Kontaktformular",
                        "form_fields": [
                            {
                                "field_type": "text",
                                "field_label": "{{FIELD_LABEL}}",
                                "placeholder": "{{FIELD_PLACEHOLDER}}",
                                "required": "{{FIELD_REQUIRED}}"
                            }
                        ],
                        "button_text": "{{FORM_SUBMIT_TEXT}}"
                    }
                }]
            }]
        }
    
    def create_map_template(self) -> Dict:
        """Template für Google Maps"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "google_maps",
                    "settings": {
                        "address": "{{MAP_ADDRESS}}",
                        "zoom": {"size": "{{MAP_ZOOM}}"},
                        "height": {"size": 400}
                    }
                }]
            }]
        }
    
    def create_download_section_template(self) -> Dict:
        """Template für Download-Bereich"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "icon-list",
                    "settings": {
                        "icon_list": [
                            {
                                "text": "{{DOWNLOAD_TITLE}}",
                                "selected_icon": {"value": "{{DOWNLOAD_ICON}}"},
                                "link": {"url": "{{DOWNLOAD_LINK}}"}
                            }
                        ]
                    }
                }]
            }]
        }
    
    def create_breadcrumb_template(self) -> Dict:
        """Template für Breadcrumb-Navigation"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "breadcrumbs",
                    "settings": {
                        "separator": ">",
                        "show_home": "yes"
                    }
                }]
            }]
        }
    
    def create_text_image_template(self) -> Dict:
        """Template für Text-Bild Kombination"""
        return {
            "elType": "section",
            "elements": [
                {
                    "elType": "column",
                    "settings": {"_column_size": 50},
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "{{TEXT_CONTENT}}"
                        }
                    }]
                },
                {
                    "elType": "column",
                    "settings": {"_column_size": 50},
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "{{IMAGE_URL}}"}
                        }
                    }]
                }
            ]
        }
    
    def create_image_text_template(self) -> Dict:
        """Template für Bild-Text Kombination (umgekehrt)"""
        return {
            "elType": "section",
            "elements": [
                {
                    "elType": "column",
                    "settings": {"_column_size": 50},
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "{{IMAGE_URL}}"}
                        }
                    }]
                },
                {
                    "elType": "column",
                    "settings": {"_column_size": 50},
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "{{TEXT_CONTENT}}"
                        }
                    }]
                }
            ]
        }
    
    def create_certifications_template(self) -> Dict:
        """Template für Zertifizierungen"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "icon-box",
                    "settings": {
                        "title_text": "{{CERT_TITLE}}",
                        "description_text": "{{CERT_TEXT}}",
                        "selected_icon": {"value": "{{CERT_ICON}}"}
                    }
                }]
            }]
        }
    
    def create_process_timeline_template(self) -> Dict:
        """Template für Prozess-Timeline"""
        return {
            "elType": "section",
            "elements": [{
                "elType": "column",
                "elements": [{
                    "elType": "widget",
                    "widgetType": "progress",
                    "settings": {
                        "title": "{{PROCESS_TITLE}}",
                        "type": "info",
                        "percentage": {"size": "{{PROCESS_PERCENTAGE}}"}
                    }
                }]
            }]
        }
    
    def create_default_blocks(self):
        """Erstelle minimale Standard-Blocks falls keine Library existiert"""
        # Verwende Blocks aus der existierenden Library oder erstelle Basis-Blocks
        self.blocks['hero-slider'] = [{
            'type': 'hero-slider',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "slides",
                        "settings": {
                            "slides": []
                        }
                    }]
                }]
            }
        }]
        
        self.blocks['title-section'] = [{
            'type': 'title-section',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "{{TITLE}}",
                            "header_size": "h1"
                        }
                    }]
                }]
            }
        }]
        
        self.blocks['text-content'] = [{
            'type': 'text-content',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "{{CONTENT}}"
                        }
                    }]
                }]
            }
        }]
        
        self.blocks['service-cards'] = [{
            'type': 'service-cards',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "icon-box",
                        "settings": {
                            "title_text": "{{SERVICE_TITLE}}",
                            "description_text": "{{SERVICE_TEXT}}",
                            "selected_icon": {"value": "{{SERVICE_ICON}}"}
                        }
                    }]
                }]
            }
        }]
        
        self.blocks['testimonials'] = [{
            'type': 'testimonials',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "testimonial",
                        "settings": {
                            "testimonial_content": "{{TESTIMONIAL_TEXT}}",
                            "testimonial_name": "{{TESTIMONIAL_AUTHOR}}",
                            "testimonial_job": "{{TESTIMONIAL_POSITION}}"
                        }
                    }]
                }]
            }
        }]
        
        self.blocks['team-section'] = [{
            'type': 'team-section',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "image-box",
                        "settings": {
                            "image": {"url": "{{MEMBER_IMAGE}}"},
                            "title_text": "{{MEMBER_NAME}}",
                            "description_text": "{{MEMBER_BIO}}"
                        }
                    }]
                }]
            }
        }]
        
        self.blocks['video-section'] = [{
            'type': 'video-section',
            'structure': {
                "elType": "section",
                "elements": [{
                    "elType": "column",
                    "elements": [{
                        "elType": "widget",
                        "widgetType": "video",
                        "settings": {
                            "youtube_url": "{{VIDEO_URL}}",
                            "video_type": "youtube"
                        }
                    }]
                }]
            }
        }]
    
    def assemble_page(self, page_config: Dict) -> Dict:
        """Assembliere eine Seite aus Blocks"""
        page_data = {
            'title': page_config.get('title', 'Untitled'),
            'slug': page_config.get('slug', ''),
            'template': page_config.get('template', 'elementor_canvas'),
            'elementor_data': []
        }
        
        # Assembliere Blocks
        for block_config in page_config.get('blocks', []):
            block_type = block_config.get('type')
            
            if block_type not in self.blocks:
                print(f"  ⚠️  Block-Typ nicht gefunden: {block_type}")
                continue
                
            # Wähle Block-Template
            block_template = self.blocks[block_type][0]['structure']
            
            # Fülle Template mit Daten
            filled_block = self._fill_block_template(block_template, block_config)
            
            # Füge Block zur Seite hinzu
            page_data['elementor_data'].append(filled_block)
            
            print(f"  ✅ Block assembliert: {block_type}")
        
        return page_data
    
    def _fill_block_template(self, template: Dict, config: Dict) -> Dict:
        """Fülle Block-Template mit Inhalten aus Config"""
        filled = copy.deepcopy(template)
        
        # Erstelle Content-Map basierend auf Block-Typ
        content_map = self._create_content_map(config)
        
        # Rekursive Ersetzung
        def replace_placeholders(element: Any, content: Dict) -> Any:
            if isinstance(element, str):
                for key, value in content.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in element:
                        element = element.replace(placeholder, str(value))
                return element
            elif isinstance(element, dict):
                result = {}
                for k, v in element.items():
                    result[k] = replace_placeholders(v, content)
                return result
            elif isinstance(element, list):
                return [replace_placeholders(item, content) for item in element]
            else:
                return element
        
        return replace_placeholders(filled, content_map)
    
    def _create_content_map(self, config: Dict) -> Dict:
        """Erstelle Content-Map für verschiedene Block-Typen"""
        content_map = {}
        block_type = config.get('type')
        
        # Standard-Felder
        if 'title' in config:
            content_map['TITLE'] = config['title']
        if 'subtitle' in config:
            content_map['SUBTITLE'] = config['subtitle']
        if 'content' in config:
            content_map['CONTENT'] = config['content']
            content_map['TEXT_CONTENT'] = config['content']
        
        # Block-spezifische Mappings
        if block_type == 'hero-slider' and 'slides' in config:
            for i, slide in enumerate(config['slides'][:3]):
                content_map[f'SLIDE_{i}_TITLE'] = slide.get('title', '')
                content_map[f'SLIDE_{i}_SUBTITLE'] = slide.get('subtitle', '')
                content_map[f'SLIDE_{i}_TEXT'] = slide.get('text', '')
                content_map[f'SLIDE_{i}_BUTTON'] = slide.get('button_text', '')
                content_map[f'SLIDE_{i}_LINK'] = slide.get('button_link', '#')
                content_map[f'SLIDE_{i}_IMAGE'] = slide.get('image', '')
        
        elif block_type == 'service-cards' and 'services' in config:
            # Für mehrere Services
            for i, service in enumerate(config['services'][:6]):
                content_map[f'SERVICE_{i}_TITLE'] = service.get('title', '')
                content_map[f'SERVICE_{i}_TEXT'] = service.get('text', '')
                content_map[f'SERVICE_{i}_ICON'] = service.get('icon', 'fa fa-check')
                content_map[f'SERVICE_{i}_LINK'] = service.get('link', '#')
            
            # Generische Platzhalter für ersten Service
            if config['services']:
                content_map['SERVICE_TITLE'] = config['services'][0].get('title', '')
                content_map['SERVICE_TEXT'] = config['services'][0].get('text', '')
                content_map['SERVICE_ICON'] = config['services'][0].get('icon', 'fa fa-check')
        
        elif block_type == 'statistics' and 'stats' in config:
            for i, stat in enumerate(config['stats'][:4]):
                content_map[f'STAT_{i}_NUMBER'] = stat.get('number', '0')
                content_map[f'STAT_{i}_LABEL'] = stat.get('label', '')
                content_map[f'STAT_{i}_PREFIX'] = stat.get('prefix', '')
                content_map[f'STAT_{i}_SUFFIX'] = stat.get('suffix', '')
                content_map[f'STAT_{i}_ICON'] = stat.get('icon', 'fa fa-chart-line')
            
            # Generisch für ersten Stat
            if config['stats']:
                content_map['STAT_NUMBER'] = config['stats'][0].get('number', '0')
                content_map['STAT_LABEL'] = config['stats'][0].get('label', '')
                content_map['STAT_PREFIX'] = config['stats'][0].get('prefix', '')
                content_map['STAT_SUFFIX'] = config['stats'][0].get('suffix', '')
        
        elif block_type == 'alert-box':
            content_map['ALERT_TITLE'] = config.get('title', 'Hinweis')
            content_map['ALERT_TEXT'] = config.get('text', '')
            content_map['ALERT_ICON'] = config.get('icon', 'fa fa-exclamation-triangle')
            content_map['ALERT_COLOR'] = '#FFF3CD' if config.get('type') == 'warning' else '#D1ECF1'
        
        elif block_type == 'cta-section':
            content_map['CTA_TITLE'] = config.get('title', '')
            content_map['CTA_SUBTITLE'] = config.get('subtitle', '')
            content_map['CTA_BUTTON_TEXT'] = config.get('button_text', 'Kontakt')
            content_map['CTA_BUTTON_LINK'] = config.get('button_link', '/kontakt')
            content_map['CTA_BG_COLOR'] = config.get('background', '#333399')
        
        elif block_type == 'timeline' and 'events' in config:
            for i, event in enumerate(config['events'][:10]):
                content_map[f'TIMELINE_{i}_YEAR'] = event.get('year', '')
                content_map[f'TIMELINE_{i}_TITLE'] = event.get('title', '')
                content_map[f'TIMELINE_{i}_TEXT'] = event.get('text', '')
            
            if config['events']:
                content_map['TIMELINE_YEAR'] = config['events'][0].get('year', '')
                content_map['TIMELINE_TITLE'] = config['events'][0].get('title', '')
                content_map['TIMELINE_TEXT'] = config['events'][0].get('text', '')
        
        elif block_type == 'team-section' and 'members' in config:
            for i, member in enumerate(config['members'][:4]):
                content_map[f'MEMBER_{i}_NAME'] = member.get('name', '')
                content_map[f'MEMBER_{i}_POSITION'] = member.get('position', '')
                content_map[f'MEMBER_{i}_BIO'] = member.get('bio', '')
                content_map[f'MEMBER_{i}_IMAGE'] = member.get('image', '')
            
            if config['members']:
                content_map['MEMBER_NAME'] = config['members'][0].get('name', '')
                content_map['MEMBER_POSITION'] = config['members'][0].get('position', '')
                content_map['MEMBER_BIO'] = config['members'][0].get('bio', '')
                content_map['MEMBER_IMAGE'] = config['members'][0].get('image', '')
        
        elif block_type == 'testimonials' and 'testimonials' in config:
            for i, testimonial in enumerate(config['testimonials'][:4]):
                content_map[f'TESTIMONIAL_{i}_TEXT'] = testimonial.get('text', '')
                content_map[f'TESTIMONIAL_{i}_AUTHOR'] = testimonial.get('author', '')
                content_map[f'TESTIMONIAL_{i}_POSITION'] = testimonial.get('position', '')
                content_map[f'TESTIMONIAL_{i}_RATING'] = testimonial.get('rating', 5)
            
            if config['testimonials']:
                content_map['TESTIMONIAL_TEXT'] = config['testimonials'][0].get('text', '')
                content_map['TESTIMONIAL_AUTHOR'] = config['testimonials'][0].get('author', '')
                content_map['TESTIMONIAL_POSITION'] = config['testimonials'][0].get('position', '')
        
        elif block_type == 'contact-info' and 'items' in config:
            settings = self.config.get('global_settings', {})
            content_map['CONTACT_ADDRESS'] = settings.get('address', '')
            content_map['CONTACT_PHONE'] = settings.get('phone', '')
            content_map['CONTACT_EMAIL'] = settings.get('email', '')
        
        elif block_type == 'contact-form' and 'fields' in config:
            content_map['FORM_SUBMIT_TEXT'] = config.get('submit_text', 'Absenden')
            for i, field in enumerate(config['fields'][:10]):
                content_map[f'FIELD_{i}_LABEL'] = field.get('label', '')
                content_map[f'FIELD_{i}_PLACEHOLDER'] = field.get('placeholder', '')
                content_map[f'FIELD_{i}_REQUIRED'] = 'yes' if field.get('required') else 'no'
        
        elif block_type == 'map':
            content_map['MAP_ADDRESS'] = config.get('address', self.config.get('global_settings', {}).get('address', ''))
            content_map['MAP_ZOOM'] = config.get('zoom', 15)
            content_map['MAP_LAT'] = config.get('lat', '')
            content_map['MAP_LNG'] = config.get('lng', '')
        
        elif block_type == 'video-section':
            content_map['VIDEO_URL'] = config.get('video_url', '')
            content_map['VIDEO_POSTER'] = config.get('poster', '')
        
        elif block_type in ['text-image', 'image-text']:
            content_map['TEXT_CONTENT'] = config.get('content', '')
            content_map['IMAGE_URL'] = config.get('image', '')
        
        # Globale Settings anwenden
        if self.config and 'global_settings' in self.config:
            settings = self.config['global_settings']
            content_map['COMPANY_NAME'] = settings.get('company_name', 'RIMAN GmbH')
            content_map['PRIMARY_COLOR'] = settings.get('primary_color', '#333399')
            content_map['SECONDARY_COLOR'] = settings.get('secondary_color', '#FF0000')
        
        return content_map
    
    def generate_wordpress_xml(self) -> str:
        """Generiere WordPress XML aus assemblierter Struktur"""
        # XML-Struktur aufbauen
        root = ET.Element('rss', {
            'version': '2.0',
            'xmlns:excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:wfw': 'http://wellformedweb.org/CommentAPI/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:wp': 'http://wordpress.org/export/1.2/'
        })
        
        channel = ET.SubElement(root, 'channel')
        
        # Site-Informationen
        site_config = self.config.get('site', {})
        ET.SubElement(channel, 'title').text = site_config.get('title', 'RIMAN GmbH')
        ET.SubElement(channel, 'link').text = site_config.get('url', 'http://localhost:8082')
        ET.SubElement(channel, 'description').text = site_config.get('description', '')
        ET.SubElement(channel, 'language').text = 'de-DE'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        
        # Autor
        author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = '1'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = 'info@riman.de'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = 'Administrator'
        
        # Kategorien
        categories = ['Rechtliches', 'Schadstoffe', 'Umwelt', 'Sicherheit', 'News']
        for i, cat_name in enumerate(categories, start=1):
            category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = str(i)
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = cat_name.lower()
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = cat_name
        
        # Menüs generieren
        self._generate_menus(channel)
        
        # Seiten generieren
        page_id = 1000
        for page_config in self.config.get('pages', []):
            page_data = self.assemble_page(page_config)
            self._add_page_to_xml(channel, page_data, page_id)
            page_id += 1
            self.generated_pages.append(page_data)
        
        # Blog-Posts generieren
        post_id = 2000
        for post_config in self.config.get('posts', []):
            self._add_post_to_xml(channel, post_config, post_id)
            post_id += 1
        
        # XML formatieren
        xml_string = ET.tostring(root, encoding='unicode')
        
        # DOCTYPE hinzufügen
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_string
        
        return xml_output
    
    def _generate_menus(self, channel):
        """Generiere WordPress-Menüs"""
        for menu_config in self.config.get('menus', []):
            # Menü-Term
            menu_term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
            ET.SubElement(menu_term, '{http://wordpress.org/export/1.2/}term_id').text = str(menu_config['id'])
            ET.SubElement(menu_term, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'nav_menu'
            ET.SubElement(menu_term, '{http://wordpress.org/export/1.2/}term_slug').text = menu_config.get('id', 'main-menu')
            ET.SubElement(menu_term, '{http://wordpress.org/export/1.2/}term_name').text = menu_config.get('name', 'Hauptmenü')
            
            # Menü-Items
            for item in menu_config.get('items', []):
                self._add_menu_item_to_xml(channel, item, menu_config['id'])
    
    def _add_menu_item_to_xml(self, channel, item_config, menu_id):
        """Füge Menü-Item zu XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = item_config.get('title', '')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_config.get('id', 0))
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'nav_menu_item'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        
        # Menü-Metadaten
        menu_meta = {
            '_menu_item_type': 'post_type',
            '_menu_item_object': 'page',
            '_menu_item_object_id': str(item_config.get('page_id', 0)),
            '_menu_item_menu_item_parent': '0',
            '_menu_item_position': str(item_config.get('order', 1))
        }
        
        for key, value in menu_meta.items():
            postmeta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_key').text = key
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_value').text = value
        
        # Submenü-Items
        if 'submenu' in item_config:
            for sub_item in item_config['submenu']:
                sub_item['parent_id'] = item_config.get('id', 0)
                self._add_menu_item_to_xml(channel, sub_item, menu_id)
    
    def _add_page_to_xml(self, channel, page_data: Dict, page_id: int):
        """Füge Seite zu XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = page_data['title']
        ET.SubElement(item, 'link').text = f"http://localhost:8082/{page_data['slug']}"
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"http://localhost:8082/?page_id={page_id}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(page_id)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page_data['slug']
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        
        # Elementor-Daten
        if 'elementor_data' in page_data:
            postmeta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_value').text = json.dumps(page_data['elementor_data'])
            
            # Elementor-Einstellungen
            postmeta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_edit_mode'
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_value').text = 'builder'
            
            postmeta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_page_template'
            ET.SubElement(postmeta, '{http://wordpress.org/export/1.2/}meta_value').text = page_data.get('template', 'elementor_canvas')
    
    def _add_post_to_xml(self, channel, post_config: Dict, post_id: int):
        """Füge Blog-Post zu XML hinzu"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = post_config.get('title', '')
        ET.SubElement(item, 'link').text = f"http://localhost:8082/{post_config.get('slug', '')}"
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = post_config.get('author', 'admin')
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = f"http://localhost:8082/?p={post_id}"
        ET.SubElement(item, 'description').text = post_config.get('excerpt', '')
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = post_config.get('content', '')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(post_id)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = post_config.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = post_config.get('slug', '')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        
        # Kategorie
        category = ET.SubElement(item, 'category', {'domain': 'category'})
        category.text = post_config.get('category', 'News')
    
    def process(self):
        """Hauptverarbeitungsmethode"""
        print("\n🚀 RIMAN Website Block Processor")
        print("="*50)
        
        # Lade Konfiguration
        if not self.load_config():
            return False
        
        # Lade Block-Library
        print(f"📚 Lade Block-Library...")
        self.load_block_library()
        
        # Generiere WordPress XML
        print(f"\n📝 Generiere WordPress XML...")
        
        # Assembliere alle Seiten
        print(f"\n🔨 Assembliere {len(self.config.get('pages', []))} Seiten...")
        for page_config in self.config.get('pages', []):
            print(f"\n📄 Verarbeite: {page_config.get('title', 'Untitled')}")
            page_data = self.assemble_page(page_config)
            self.generated_pages.append(page_data)
        
        # Generiere XML
        xml_output = self.generate_wordpress_xml()
        
        # Speichere XML
        output_file = 'riman-complete.xml'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_output)
        
        print(f"\n✅ XML generiert: {output_file} ({len(xml_output)} bytes)")
        print(f"📊 {len(self.generated_pages)} Seiten assembliert")
        print(f"📊 {len(self.config.get('posts', []))} Blog-Posts erstellt")
        print(f"📊 {len(self.config.get('menus', []))} Menüs konfiguriert")
        
        print(f"\n✅ RIMAN Website bereit zum Import!")
        print(f"   Output: {output_file}")
        
        return True

def main():
    """Hauptausführung"""
    processor = RIMANBlockProcessor('riman-relaunch-complete.yaml')
    success = processor.process()
    return success

if __name__ == "__main__":
    main()