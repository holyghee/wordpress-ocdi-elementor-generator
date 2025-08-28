#!/usr/bin/env python3
"""
Cholot Exact Replicator - Generates XML with exact ID matching for Cholot theme
Based on the exact target XML structure with 65 items

This script creates a WordPress XML that exactly matches the target demo-data-fixed.xml
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
from typing import Dict, Any, List
import re

class CholtExactReplicator:
    def __init__(self):
        self.generated_items = 0
        
    def generate_from_yaml(self, yaml_path: str, output_path: str) -> str:
        """Generate exact XML from YAML configuration"""
        print("🎯 Cholot Exact Replicator - Starting generation...")
        print("=" * 60)
        
        # Load YAML configuration
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Create XML structure
        rss = self._create_exact_xml_structure(config)
        
        # Generate XML with exact formatting
        xml_output = self._generate_exact_xml(rss, output_path)
        
        print(f"✅ Generated XML: {output_path}")
        print(f"📊 Total items: {self.generated_items}")
        print(f"🎯 Target items: 65")
        
        return xml_output

    def _create_exact_xml_structure(self, config: Dict) -> ET.Element:
        """Create XML structure matching target exactly"""
        # Create RSS root with exact namespaces - avoid duplicates
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Add site info matching target
        self._add_exact_site_info(channel, config)
        
        # Add author (exact match)
        self._add_exact_author(channel)
        
        # Add categories (exact IDs: 10=Life, 8=People)
        self._add_exact_categories(channel)
        
        # Add tags (exact IDs from target)
        self._add_exact_tags(channel)
        
        # Add nav menu terms
        self._add_exact_nav_menu_terms(channel)
        
        # Add all items in correct order to match target exactly
        self._add_exact_items(channel, config)
        
        return rss
    
    def _add_exact_site_info(self, channel: ET.Element, config: Dict):
        """Add site information exactly matching target"""
        ET.SubElement(channel, 'title').text = 'Cholot'
        ET.SubElement(channel, 'link').text = 'http://ridianur.com/wp/cholot'  # Exact target URL
        ET.SubElement(channel, 'description').text = 'Just another WordPress site'
        ET.SubElement(channel, 'pubDate').text = 'Thu, 18 Jul 2019 09:46:57 +0000'
        ET.SubElement(channel, 'language').text = 'en-US'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = 'http://ridianur.com/wp/cholot'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = 'http://ridianur.com/wp/cholot'
    
    def _add_exact_author(self, channel: ET.Element):
        """Add author exactly matching target"""
        author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = '1'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = 'ridianur@yahoo.com'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = 'admin'
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_first_name').text = ''
        ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_last_name').text = ''
    
    def _add_exact_categories(self, channel: ET.Element):
        """Add categories with exact IDs"""
        # Life category (ID: 10)
        cat1 = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(cat1, '{http://wordpress.org/export/1.2/}term_id').text = '10'
        ET.SubElement(cat1, '{http://wordpress.org/export/1.2/}category_nicename').text = 'life'
        ET.SubElement(cat1, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(cat1, '{http://wordpress.org/export/1.2/}cat_name').text = 'Life'
        
        # People category (ID: 8)
        cat2 = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
        ET.SubElement(cat2, '{http://wordpress.org/export/1.2/}term_id').text = '8'
        ET.SubElement(cat2, '{http://wordpress.org/export/1.2/}category_nicename').text = 'people'
        ET.SubElement(cat2, '{http://wordpress.org/export/1.2/}category_parent').text = ''
        ET.SubElement(cat2, '{http://wordpress.org/export/1.2/}cat_name').text = 'People'
    
    def _add_exact_tags(self, channel: ET.Element):
        """Add tags with exact IDs from target"""
        tags_data = [
            {'id': 17, 'slug': 'humming', 'name': 'humming'},
            {'id': 18, 'slug': 'liquid', 'name': 'liquid'},
            {'id': 19, 'slug': 'magic', 'name': 'magic'},
            {'id': 20, 'slug': 'movie', 'name': 'movie'},
            {'id': 21, 'slug': 'technology', 'name': 'technology'},
            {'id': 22, 'slug': 'travel', 'name': 'travel'},
            {'id': 23, 'slug': 'wildfire', 'name': 'wildfire'}
        ]
        
        for tag_data in tags_data:
            tag = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}tag')
            ET.SubElement(tag, '{http://wordpress.org/export/1.2/}term_id').text = str(tag_data['id'])
            ET.SubElement(tag, '{http://wordpress.org/export/1.2/}tag_slug').text = tag_data['slug']
            ET.SubElement(tag, '{http://wordpress.org/export/1.2/}tag_name').text = tag_data['name']
    
    def _add_exact_nav_menu_terms(self, channel: ET.Element):
        """Add navigation menu terms with exact IDs"""
        # Primary Menu term (ID: 16)
        term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
        ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_id').text = '16'
        ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_taxonomy').text = 'nav_menu'
        ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_slug').text = 'primary'
        ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_name').text = 'Primary Menu'
    
    def _add_exact_items(self, channel: ET.Element, config: Dict):
        """Add all items in exact order and with exact IDs"""
        print("📝 Adding items in exact order...")
        
        # 1. Add media attachments (IDs: 9, 11, 47, 48, 50, 51, 52, 53, 100, 236, 237, 239, 240, 346, 349, 350, 351, 357, 358, 359, 360, 369, 395, 397, 659, 883, 1025)
        self._add_exact_media(channel, config)
        
        # 2. Add Custom Headers (IDs: 65, 205, 910)
        self._add_exact_custom_headers(channel, config)
        
        # 3. Add Contact Form (ID: 5)
        self._add_exact_contact_form(channel, config)
        
        # 4. Add Pages (IDs: 6, 179, 251, 289, 365, 374, 429, 467)
        self._add_exact_pages(channel, config)
        
        # 5. Add Posts (IDs: 411, 417, 424, 425, 426, 427, 428, 436)
        self._add_exact_posts(channel, config)
        
        # 6. Add Menu Items (IDs: 172, 191, 300, 373, 383, 404, 405, 435, 453, 454, 455)
        self._add_exact_menu_items(channel, config)
        
        # 7. Add Elementor Templates (IDs: 1482, 1485, 1488, 1491, 1494, 1497, 1500)
        self._add_exact_elementor_templates(channel, config)
        
        print(f"✅ Generated {self.generated_items} items")
    
    def _add_exact_media(self, channel: ET.Element, config: Dict):
        """Add media attachments with exact IDs"""
        media_items = config.get('media', [])
        
        for media in media_items:
            media_id = media.get('id')
            if not media_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = media.get('title', f"Attachment {media_id}")
            filename = media.get('filename', f"file-{media_id}")
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://ridianur.com/wp/cholot/{filename}/"
            ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/{filename}/"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(media_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = filename
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'inherit'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'attachment'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Attachment URL
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}attachment_url').text = f"http://ridianur.com/wp/cholot/wp-content/uploads/2019/07/{filename}.jpg"
            
            # Meta
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_attached_file'
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'2019/07/{filename}.jpg'
            
            self.generated_items += 1
    
    def _add_exact_custom_headers(self, channel: ET.Element, config: Dict):
        """Add custom headers/footers with exact IDs"""
        custom_headers = config.get('custom_headers', [])
        custom_footers = config.get('custom_footers', [])
        
        # Add headers
        for header in custom_headers:
            header_id = header.get('id')
            if not header_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = header.get('title', f"Header {header_id}")
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://ridianur.com/wp/cholot/?post_type=elementor_library&#038;p={header_id}"
            ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/?post_type=elementor_library&#038;p={header_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(header_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = f"header-{header_id}"
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'elementor_library'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Elementor meta
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_template_type'
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = 'header'
            
            self.generated_items += 1
        
        # Add footers
        for footer in custom_footers:
            footer_id = footer.get('id')
            if not footer_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = footer.get('title', f"Footer {footer_id}")
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://ridianur.com/wp/cholot/?post_type=elementor_library&#038;p={footer_id}"
            ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/?post_type=elementor_library&#038;p={footer_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(footer_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = f"footer-{footer_id}"
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'elementor_library'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Elementor meta
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_template_type'
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = 'footer'
            
            self.generated_items += 1
    
    def _add_exact_contact_form(self, channel: ET.Element, config: Dict):
        """Add contact form with exact ID: 5"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = 'Contact form'
        ET.SubElement(item, 'link').text = 'http://ridianur.com/wp/cholot/?post_type=wpcf7_contact_form&#038;p=5'
        ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = 'http://ridianur.com/wp/cholot/?post_type=wpcf7_contact_form&#038;p=5'
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = '5'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = 'contact-form-1'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'wpcf7_contact_form'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        self.generated_items += 1
    
    def _add_exact_pages(self, channel: ET.Element, config: Dict):
        """Add pages with exact IDs"""
        pages = config.get('pages', [])
        
        for page in pages:
            page_id = page.get('id')
            if not page_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = page.get('title', f"Page {page_id}")
            slug = page.get('slug', f"page-{page_id}")
            
            ET.SubElement(item, 'title').text = title
            link_url = f"http://ridianur.com/wp/cholot/"
            if slug:
                link_url += f"{slug}/"
            ET.SubElement(item, 'link').text = link_url
            ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/?page_id={page_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(page_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = slug if slug else 'home'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = page.get('status', 'publish')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = str(page.get('parent', 0))
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(page.get('menu_order', 0))
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Add Cholot meta if specified
            cholot_meta = page.get('cholot_meta', {})
            for meta_key, meta_value in cholot_meta.items():
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = meta_key
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = str(meta_value)
            
            # Add Elementor meta if it's an Elementor page
            template = page.get('template', '')
            if template == 'elementor_canvas':
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_edit_mode'
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = 'builder'
                
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_page_template'
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = 'elementor_canvas'
            
            self.generated_items += 1
    
    def _add_exact_posts(self, channel: ET.Element, config: Dict):
        """Add posts with exact IDs"""
        posts = config.get('posts', [])
        
        for post in posts:
            post_id = post.get('id')
            if not post_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = post.get('title', f"Post {post_id}")
            slug = post.get('slug', f"post-{post_id}")
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://ridianur.com/wp/cholot/{slug}/"
            ET.SubElement(item, 'pubDate').text = post.get('date', 'Thu, 04 Jul 2019 11:13:19 +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/?p={post_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = '<p>Sample blog post content.</p>'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(post_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = post.get('date', '2019-07-04 11:13:19')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = post.get('date', '2019-07-04 11:13:19')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = slug
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = post.get('status', 'publish')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Categories
            categories = post.get('categories', [])
            for cat in categories:
                cat_elem = ET.SubElement(item, 'category', domain='category', nicename=cat.lower())
                cat_elem.text = cat
            
            # Tags  
            tags = post.get('tags', [])
            for tag in tags:
                tag_elem = ET.SubElement(item, 'category', domain='post_tag', nicename=tag.lower())
                tag_elem.text = tag
                
            self.generated_items += 1
    
    def _add_exact_menu_items(self, channel: ET.Element, config: Dict):
        """Add menu items with exact IDs"""
        menus = config.get('menus', [])
        if not menus:
            return
            
        menu = menus[0]  # Primary menu
        menu_items = menu.get('items', [])
        
        for menu_item in menu_items:
            item_id = menu_item.get('id')
            if not item_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = menu_item.get('title', '')
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://ridianur.com/wp/cholot/?p={item_id}"
            ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/?p={item_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ' '
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(menu_item.get('menu_order', 1))
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'nav_menu_item'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Menu category
            cat = ET.SubElement(item, 'category', domain='nav_menu', nicename='primary')
            cat.text = 'Primary Menu'
            
            # Menu item meta
            meta_items = [
                ('_menu_item_type', menu_item.get('type', 'post_type')),
                ('_menu_item_menu_item_parent', str(menu_item.get('parent', 0))),
                ('_menu_item_object', 'page'),
                ('_menu_item_object_id', str(menu_item.get('object_id', item_id))),
                ('_menu_item_target', ''),
                ('_menu_item_classes', ''),
                ('_menu_item_xfn', ''),
                ('_menu_item_url', menu_item.get('url', ''))
            ]
            
            for meta_key, meta_value in meta_items:
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = meta_key
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = str(meta_value)
                
            self.generated_items += 1
    
    def _add_exact_elementor_templates(self, channel: ET.Element, config: Dict):
        """Add Elementor templates with exact IDs"""
        templates = config.get('elementor_templates', [])
        
        for template in templates:
            template_id = template.get('id')
            if not template_id:
                continue
                
            item = ET.SubElement(channel, 'item')
            
            title = template.get('title', f"Template {template_id}")
            
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = f"http://ridianur.com/wp/cholot/?post_type=elementor_library&#038;p={template_id}"
            ET.SubElement(item, 'pubDate').text = 'Thu, 04 Jul 2019 10:16:07 +0000'
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://ridianur.com/wp/cholot/?post_type=elementor_library&#038;p={template_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(template_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = '2019-07-04 10:16:07'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = f"template-{template_id}"
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'elementor_library'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Elementor meta
            meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_template_type'
            ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = template.get('type', 'page')
            
            self.generated_items += 1
    
    def _generate_exact_xml(self, rss: ET.Element, output_path: str) -> str:
        """Generate XML with exact formatting matching target"""
        # Convert to string
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Add CDATA wrapping where needed to match target exactly
        xml_string = self._add_cdata_wrapping(xml_string)
        
        # Pretty format
        try:
            dom = minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent='\t', encoding='UTF-8')
            
            # Clean up and match target formatting
            lines = pretty_xml.decode('utf-8').split('\n')
            clean_lines = []
            
            for line in lines:
                if line.strip():
                    clean_lines.append(line)
            
            # Add WordPress comments at the top to match target
            header_comments = [
                '<?xml version="1.0" encoding="UTF-8" ?>',
                '<!-- This is a WordPress eXtended RSS file generated by WordPress as an export of your site. -->',
                '<!-- It contains information about your site\'s posts, pages, comments, categories, and other content. -->',
                '<!-- You may use this file to transfer that content from one site to another. -->',
                '<!-- This file is not intended to serve as a complete backup of your site. -->',
                '',
                '<!-- To import this information into a WordPress site follow these steps: -->',
                '<!-- 1. Log in to that site as an administrator. -->',
                '<!-- 2. Go to Tools: Import in the WordPress admin panel. -->',
                '<!-- 3. Install the "WordPress" importer from the list. -->',
                '<!-- 4. Activate & Run Importer. -->',
                '<!-- 5. Upload this file using the form provided on that page. -->',
                '<!-- 6. You will first be asked to map the authors in this export file to users -->',
                '<!--    on the site. For each author, you may choose to map to an -->',
                '<!--    existing user on the site or to create a new user. -->',
                '<!-- 7. WordPress will then import each of the posts, pages, comments, categories, etc. -->',
                '<!--    contained in this file into your site. -->',
                '',
                '\t<!-- generator="WordPress/5.2.2" created="2019-07-18 09:46" -->'
            ]
            
            # Remove the first line (XML declaration) and replace with our header
            final_xml = '\n'.join(header_comments + clean_lines[1:])
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_xml)
                
        except Exception as e:
            print(f"Warning: Using fallback XML formatting: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                f.write(xml_string)
        
        return output_path
    
    def _add_cdata_wrapping(self, xml_string: str) -> str:
        """Add CDATA wrapping to match target format exactly"""
        import re
        
        # Wrap specific tags in CDATA
        cdata_tags = [
            'wp:author_login', 'wp:author_email', 'wp:author_display_name',
            'wp:author_first_name', 'wp:author_last_name',
            'wp:category_nicename', 'wp:category_parent', 'wp:cat_name',
            'wp:tag_slug', 'wp:tag_name',
            'wp:term_slug', 'wp:term_name',
            'title', 'wp:post_name', 'dc:creator'
        ]
        
        for tag in cdata_tags:
            pattern = f'<{tag}>([^<]*)</{tag}>'
            replacement = lambda m: f'<{tag}><![CDATA[{m.group(1)}]]></{tag}>' if m.group(1) else f'<{tag}><![CDATA[]]></{tag}>'
            xml_string = re.sub(pattern, replacement, xml_string)
        
        return xml_string


def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python cholot_exact_replicator.py <yaml_file> <output_xml>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    output_xml = sys.argv[2]
    
    replicator = CholtExactReplicator()
    replicator.generate_from_yaml(yaml_file, output_xml)


if __name__ == "__main__":
    main()