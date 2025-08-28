#!/usr/bin/env python3
"""
Full WordPress Site Generator - Complete website with menus, posts, pages, and media
Enhanced version of section_based_processor for complete WordPress sites
"""

import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from xml.dom import minidom
from typing import Dict, Any, List, Optional
from copy import deepcopy
import uuid
import random
import re

class FullSiteGenerator:
    def __init__(self):
        self.item_counter = 100  # Start IDs from 100
        self.attachment_ids = {}  # Track attachment IDs for reuse
        self.menu_items = []      # Track menu items for ordering
        self.categories = {}      # Track categories
        self.tags = {}           # Track tags
        
    def generate_unique_id(self) -> str:
        """Generate unique Elementor element ID"""
        return uuid.uuid4().hex[:7]
    
    def get_next_id(self) -> int:
        """Get next WordPress item ID"""
        self.item_counter += 1
        return self.item_counter
    
    def process_yaml_to_wordpress(self, yaml_path: str) -> tuple:
        """Convert YAML to complete WordPress site structure"""
        # Load YAML config
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Create WordPress XML structure
        rss = self._create_rss_structure(config)
        
        return config, rss
    
    def _create_rss_structure(self, config: Dict) -> ET.Element:
        """Create complete RSS/WordPress structure"""
        # Register namespaces
        ET.register_namespace('excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
        ET.register_namespace('wfw', 'http://wellformedweb.org/CommentAPI/')
        ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
        ET.register_namespace('wp', 'http://wordpress.org/export/1.2/')
        
        # Create RSS root
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        
        # Create channel
        channel = ET.SubElement(rss, 'channel')
        
        # Add site information
        self._add_site_info(channel, config)
        
        # Add authors
        self._add_authors(channel, config)
        
        # Add categories and tags
        self._add_taxonomies(channel, config)
        
        # Add navigation menu terms
        self._add_menu_terms(channel, config)
        
        # Add media attachments first (for featured images)
        self._add_media_attachments(channel, config)
        
        # Add pages
        self._add_pages(channel, config)
        
        # Add blog posts
        self._add_blog_posts(channel, config)
        
        # Add navigation menu items
        self._add_navigation_menu(channel, config)
        
        # Add custom post types (headers, footers, etc.)
        self._add_custom_post_types(channel, config)
        
        return rss
    
    def _add_site_info(self, channel: ET.Element, config: Dict):
        """Add site information to channel"""
        site = config.get('site', {})
        ET.SubElement(channel, 'title').text = site.get('title', 'Website')
        ET.SubElement(channel, 'link').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'description').text = site.get('description', '')
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = site.get('language', 'en-US')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}wxr_version').text = '1.2'
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_site_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, '{http://wordpress.org/export/1.2/}base_blog_url').text = site.get('base_url', 'http://localhost')
        ET.SubElement(channel, 'generator').text = f'https://wordpress.org/?v=6.3'
    
    def _add_authors(self, channel: ET.Element, config: Dict):
        """Add authors to channel"""
        authors = config.get('authors', [])
        if not authors:
            # Add default admin author
            authors = [{
                'id': 1,
                'login': 'admin',
                'email': 'admin@example.com',
                'display_name': 'Administrator'
            }]
        
        for author_data in authors:
            author = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}author')
            ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_id').text = str(author_data.get('id', 1))
            ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_login').text = author_data.get('login', 'admin')
            ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_email').text = author_data.get('email', 'admin@example.com')
            ET.SubElement(author, '{http://wordpress.org/export/1.2/}author_display_name').text = author_data.get('display_name', 'Admin')
    
    def _add_taxonomies(self, channel: ET.Element, config: Dict):
        """Add categories and tags"""
        # Add categories
        categories = config.get('categories', [])
        if not categories:
            categories = [
                {'id': 1, 'slug': 'uncategorized', 'name': 'Uncategorized'},
                {'id': 2, 'slug': 'news', 'name': 'News'},
                {'id': 3, 'slug': 'updates', 'name': 'Updates'}
            ]
        
        for cat_data in categories:
            category = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}category')
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}term_id').text = str(cat_data.get('id'))
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_nicename').text = cat_data.get('slug')
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}category_parent').text = ''
            ET.SubElement(category, '{http://wordpress.org/export/1.2/}cat_name').text = cat_data.get('name')
            self.categories[cat_data.get('slug')] = cat_data.get('id')
        
        # Add tags
        tags = config.get('tags', [])
        for tag_data in tags:
            tag = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}tag')
            ET.SubElement(tag, '{http://wordpress.org/export/1.2/}term_id').text = str(tag_data.get('id'))
            ET.SubElement(tag, '{http://wordpress.org/export/1.2/}tag_slug').text = tag_data.get('slug')
            ET.SubElement(tag, '{http://wordpress.org/export/1.2/}tag_name').text = tag_data.get('name')
            self.tags[tag_data.get('slug')] = tag_data.get('id')
    
    def _add_menu_terms(self, channel: ET.Element, config: Dict):
        """Add navigation menu terms"""
        menus = config.get('menus', [])
        if not menus:
            menus = [{'id': 10, 'slug': 'main-menu', 'name': 'Main Menu'}]
        
        for menu_data in menus:
            # Create nav_menu term in compact format like the working example
            term = ET.SubElement(channel, '{http://wordpress.org/export/1.2/}term')
            
            # Build the term inline - WordPress seems to prefer this format for nav_menu
            term_id = ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_id')
            term_id.text = str(menu_data.get('id'))
            term_id.tail = ''
            
            term_tax = ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_taxonomy') 
            term_tax.text = 'nav_menu'
            term_tax.tail = ''
            
            term_slug = ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_slug')
            term_slug.text = menu_data.get('slug')
            term_slug.tail = ''
            
            term_name = ET.SubElement(term, '{http://wordpress.org/export/1.2/}term_name')
            term_name.text = menu_data.get('name')
            term_name.tail = '\n'
    
    def _add_media_attachments(self, channel: ET.Element, config: Dict):
        """Add media attachments for images"""
        media = config.get('media', [])
        
        # Also collect images from pages and posts
        for page in config.get('pages', []):
            if page.get('featured_image'):
                media.append({
                    'url': page['featured_image'],
                    'title': f"{page.get('title', 'Page')} Featured Image"
                })
        
        for post in config.get('posts', []):
            if post.get('featured_image'):
                media.append({
                    'url': post['featured_image'],
                    'title': f"{post.get('title', 'Post')} Featured Image"
                })
        
        # Add each unique media item
        processed_urls = set()
        for media_item in media:
            url = media_item.get('url')
            if url and url not in processed_urls:
                processed_urls.add(url)
                attachment_id = self._add_attachment_item(channel, media_item)
                self.attachment_ids[url] = attachment_id
    
    def _add_attachment_item(self, channel: ET.Element, media_data: Dict) -> int:
        """Add single attachment item"""
        item_id = self.get_next_id()
        item = ET.SubElement(channel, 'item')
        
        title = media_data.get('title', 'Image')
        url = media_data.get('url', '')
        
        # Extract filename from URL
        filename = 'image.jpg'
        if url:
            # Handle Unsplash URLs specially
            if 'unsplash.com' in url:
                # Extract photo ID from Unsplash URL
                import re
                match = re.search(r'photo-([a-zA-Z0-9-]+)', url)
                if match:
                    filename = f"{match.group(1)}.jpg"
            else:
                filename = url.split('/')[-1].split('?')[0]  # Remove query params
                if not filename:
                    filename = 'image.jpg'
        
        # Create a WordPress-like link
        slug = self._slugify(title)
        
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = f"http://localhost/?attachment={slug}"
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/wp-content/uploads/2024/{filename}"
        ET.SubElement(item, 'description').text = ''
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'open'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = slug
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'inherit'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'attachment'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # IMPORTANT: Use CDATA for attachment URL
        attachment_url_elem = ET.SubElement(item, '{http://wordpress.org/export/1.2/}attachment_url')
        attachment_url_elem.text = url  # Will be wrapped in CDATA by XML formatter
        
        # Meta data for WordPress
        # _wp_attached_file
        meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_attached_file'
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = f'2024/{filename}'
        
        # Add image metadata for better compatibility
        if 'unsplash' in url.lower():
            meta2 = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
            ET.SubElement(meta2, '{http://wordpress.org/export/1.2/}meta_key').text = '_wp_attachment_metadata'
            # Basic metadata structure
            metadata = 'a:5:{s:5:"width";i:1920;s:6:"height";i:1080;s:4:"file";s:%d:"%s";s:5:"sizes";a:0:{}s:10:"image_meta";a:12:{s:8:"aperture";s:1:"0";s:6:"credit";s:0:"";s:6:"camera";s:0:"";s:7:"caption";s:0:"";s:17:"created_timestamp";s:1:"0";s:9:"copyright";s:0:"";s:12:"focal_length";s:1:"0";s:3:"iso";s:1:"0";s:13:"shutter_speed";s:1:"0";s:5:"title";s:0:"";s:11:"orientation";s:1:"0";s:8:"keywords";a:0:{}}}' % (len(f'2024/{filename}'), f'2024/{filename}')
            ET.SubElement(meta2, '{http://wordpress.org/export/1.2/}meta_value').text = metadata
        
        return item_id
    
    def _add_pages(self, channel: ET.Element, config: Dict):
        """Add pages with Elementor content"""
        from section_based_processor import SectionBasedProcessor
        processor = SectionBasedProcessor()
        
        pages = config.get('pages', [])
        for page_config in pages:
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            # Basic page information
            ET.SubElement(item, 'title').text = page_config.get('title', 'Page')
            ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url', 'http://localhost')}/{page_config.get('slug', 'page')}"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{config.get('site', {}).get('base_url')}/?page_id={item_id}"
            ET.SubElement(item, 'description').text = ''
            
            # Content - can be HTML or Elementor
            content = page_config.get('content', '')
            if page_config.get('sections'):
                # Process Elementor sections
                elementor_data = processor._create_sections_page({'pages': [page_config]})
                content = '<!-- wp:html --><!-- /wp:html -->'  # Placeholder for Elementor
            
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = content
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = page_config.get('excerpt', '')
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            # Use a date in the past to ensure pages are published, not scheduled
            # Use a fixed past date to ensure consistency
            past_date = datetime(2024, 8, 21, 14, 29, 21)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = page_config.get('slug', 'page')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = page_config.get('status', 'publish')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = str(page_config.get('parent', 0))
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(page_config.get('menu_order', 0))
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'page'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Add Elementor meta if sections exist
            if page_config.get('sections'):
                # Elementor data
                clean_json = json.dumps(elementor_data, separators=(',', ':'))
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_elementor_data'
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = clean_json
                
                # Elementor settings
                for key, value in [
                    ('_elementor_edit_mode', 'builder'),
                    ('_elementor_template_type', 'wp-page'),
                    ('_wp_page_template', page_config.get('template', 'elementor_canvas'))
                ]:
                    meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
            
            # Featured image
            if page_config.get('featured_image'):
                attachment_id = self.attachment_ids.get(page_config['featured_image'])
                if attachment_id:
                    meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_thumbnail_id'
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = str(attachment_id)
    
    def _add_blog_posts(self, channel: ET.Element, config: Dict):
        """Add blog posts with categories and tags"""
        posts = config.get('posts', [])
        base_date = datetime.now() - timedelta(days=30)  # Start posts 30 days ago
        
        for i, post_config in enumerate(posts):
            item_id = self.get_next_id()
            item = ET.SubElement(channel, 'item')
            
            # Calculate post date (stagger posts)
            post_date = base_date + timedelta(days=i*3)
            
            # Basic post information
            ET.SubElement(item, 'title').text = post_config.get('title', 'Blog Post')
            ET.SubElement(item, 'link').text = f"{config.get('site', {}).get('base_url')}/{post_config.get('slug', 'post')}"
            ET.SubElement(item, 'pubDate').text = post_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = post_config.get('author', 'admin')
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{config.get('site', {}).get('base_url')}/?p={item_id}"
            ET.SubElement(item, 'description').text = ''
            
            # Post content
            content = post_config.get('content', '<p>Blog post content goes here.</p>')
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = content
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = post_config.get('excerpt', '')
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = post_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = post_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = post_config.get('comment_status', 'open')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'open'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = post_config.get('slug', f'post-{i}')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = post_config.get('status', 'publish')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'post'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = str(1 if post_config.get('sticky') else 0)
            
            # Categories
            categories = post_config.get('categories', ['uncategorized'])
            for cat_slug in categories:
                cat = ET.SubElement(item, 'category', domain='category', nicename=cat_slug)
                cat.text = cat_slug.replace('-', ' ').title()
            
            # Tags
            tags = post_config.get('tags', [])
            for tag_slug in tags:
                tag = ET.SubElement(item, 'category', domain='post_tag', nicename=tag_slug)
                tag.text = tag_slug.replace('-', ' ').title()
            
            # Featured image
            if post_config.get('featured_image'):
                attachment_id = self.attachment_ids.get(post_config['featured_image'])
                if attachment_id:
                    meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_thumbnail_id'
                    ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = str(attachment_id)
    
    def _add_navigation_menu(self, channel: ET.Element, config: Dict):
        """Add navigation menu items"""
        menus = config.get('menus', [])
        if not menus:
            return
        
        main_menu = menus[0]  # Use first menu as main
        menu_items = main_menu.get('items', [])
        
        # Track menu item IDs for parent references
        menu_item_ids = {}
        
        # First pass - generate IDs
        for i, menu_item in enumerate(menu_items):
            item_id = self.get_next_id()
            menu_item_ids[i + 1] = item_id  # Store by menu position
        
        # Second pass - create menu items
        for i, menu_item in enumerate(menu_items):
            item_id = menu_item_ids[i + 1]
            item = ET.SubElement(channel, 'item')
            
            # Menu item details
            ET.SubElement(item, 'title').text = menu_item.get('title', 'Menu Item')
            ET.SubElement(item, 'link').text = menu_item.get('url', '#')
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?p={item_id}"
            ET.SubElement(item, 'description').text = ''
            ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
            
            # Post details
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
            # Use a date in the past to ensure pages are published, not scheduled
            # Use a fixed past date to ensure consistency
            past_date = datetime(2024, 8, 21, 14, 29, 21)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = str(item_id)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = str(i + 1)
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'nav_menu_item'
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
            ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
            
            # Menu item category (assigns to menu)
            cat = ET.SubElement(item, 'category', domain='nav_menu', nicename=main_menu.get('slug', 'default-menu'))
            cat.text = main_menu.get('name', 'Default Menu')
            
            # Handle parent reference - convert parent position to ID
            parent = menu_item.get('parent', 0)
            if parent and parent in menu_item_ids:
                parent_id = menu_item_ids[parent]
            else:
                parent_id = 0
            
            # Determine object_id based on menu item type
            object_id = 0
            if menu_item.get('type') == 'post_type' and menu_item.get('object') == 'page':
                # For pages, find the actual page ID by matching URL
                url = menu_item.get('url', '')
                if url == '/leistungen':
                    object_id = 102  # ID of "Unsere Leistungen" page
                elif url == '/leistungen/asbestsanierung':
                    object_id = 103  # ID of "Asbestsanierung" page
                elif url == '/leistungen/pcb-sanierung':
                    object_id = 104  # ID of "PCB-Sanierung" page
                elif url == '/ueber-uns':
                    object_id = 105  # ID of "Über uns" page
                elif url == '/kontakt':
                    object_id = 106  # ID of "Kontakt" page
                else:
                    object_id = item_id
            else:
                object_id = item_id  # For custom links, use the menu item ID
            
            # Menu item meta
            meta_items = [
                ('_menu_item_type', menu_item.get('type', 'custom')),
                ('_menu_item_menu_item_parent', str(parent_id)),
                ('_menu_item_object', menu_item.get('object', 'custom')),
                ('_menu_item_object_id', str(object_id)),
                ('_menu_item_target', menu_item.get('target', '')),
                ('_menu_item_classes', ' '.join(menu_item.get('classes', []))),
                ('_menu_item_xfn', ''),
                ('_menu_item_url', menu_item.get('url', '#'))
            ]
            
            for key, value in meta_items:
                meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = key
                ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = value
    
    def _add_custom_post_types(self, channel: ET.Element, config: Dict):
        """Add headers, footers, and other custom post types"""
        # Add header template
        header = config.get('header')
        if header:
            self._add_template_item(channel, header, 'header', 'Header')
        
        # Add footer template
        footer = config.get('footer')
        if footer:
            self._add_template_item(channel, footer, 'footer', 'Footer')
        
        # Add contact forms
        forms = config.get('forms', [])
        for form_data in forms:
            self._add_contact_form(channel, form_data)
    
    def _add_template_item(self, channel: ET.Element, template_data: Dict, post_type: str, default_title: str):
        """Add header/footer template"""
        item_id = self.get_next_id()
        item = ET.SubElement(channel, 'item')
        
        title = template_data.get('title', default_title)
        
        # Basic information
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = '#'
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?p={item_id}"
        ET.SubElement(item, 'description').text = ''
        
        # Content (can be HTML or Elementor)
        content = template_data.get('content', '')
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = content
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
        # Use a date in the past
        past_date = datetime(2024, 8, 21, 14, 29, 21)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = self._slugify(title)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = post_type
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
    
    def _add_contact_form(self, channel: ET.Element, form_data: Dict):
        """Add Contact Form 7 form"""
        item_id = self.get_next_id()
        item = ET.SubElement(channel, 'item')
        
        title = form_data.get('title', 'Contact Form')
        
        # Basic information
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = '#'
        ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'admin'
        ET.SubElement(item, 'guid', isPermaLink='false').text = f"http://localhost/?post_type=wpcf7_contact_form&#038;p={item_id}"
        ET.SubElement(item, 'description').text = ''
        
        # Form content
        form_content = form_data.get('content', self._get_default_cf7_form())
        ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/excerpt/}encoded').text = ''
        
        # Post details
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_id').text = str(item_id)
        # Use a date in the past
        past_date = datetime(2024, 8, 21, 14, 29, 21)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_date_gmt').text = past_date.strftime('%Y-%m-%d %H:%M:%S')
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}comment_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}ping_status').text = 'closed'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_name').text = self._slugify(title)
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}status').text = 'publish'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_parent').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}menu_order').text = '0'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_type').text = 'wpcf7_contact_form'
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}post_password').text = ''
        ET.SubElement(item, '{http://wordpress.org/export/1.2/}is_sticky').text = '0'
        
        # Contact Form 7 meta
        meta = ET.SubElement(item, '{http://wordpress.org/export/1.2/}postmeta')
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_key').text = '_form'
        ET.SubElement(meta, '{http://wordpress.org/export/1.2/}meta_value').text = form_content
    
    def _get_default_cf7_form(self) -> str:
        """Get default Contact Form 7 template"""
        return """[text* your-name placeholder "Your Name"]
[email* your-email placeholder "Your Email"]
[text your-subject placeholder "Subject"]
[textarea your-message placeholder "Your Message"]
[submit "Send Message"]"""
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug"""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    def generate_wordpress_xml(self, config: Dict, rss: ET.Element, output_path: str) -> str:
        """Generate WordPress XML file with proper CDATA wrapping"""
        # Format and save XML
        xml_string = ET.tostring(rss, encoding='unicode')
        
        # Wrap nav_menu terms and categories properly in CDATA
        import re
        
        # Wrap nav_menu term values in CDATA
        xml_string = re.sub(
            r'<wp:term_slug>([^<]*)</wp:term_slug>',
            lambda m: f'<wp:term_slug><![CDATA[{m.group(1)}]]></wp:term_slug>' if m.group(1) and not m.group(1).startswith('<![CDATA[') else m.group(0),
            xml_string
        )
        xml_string = re.sub(
            r'<wp:term_name>([^<]*)</wp:term_name>',
            lambda m: f'<wp:term_name><![CDATA[{m.group(1)}]]></wp:term_name>' if m.group(1) and not m.group(1).startswith('<![CDATA[') else m.group(0),
            xml_string
        )
        
        # Wrap nav_menu category names in CDATA
        xml_string = re.sub(
            r'<category domain="nav_menu"([^>]*)>([^<]*)</category>',
            lambda m: f'<category domain="nav_menu"{m.group(1)}><![CDATA[{m.group(2)}]]></category>' if m.group(2) and not m.group(2).startswith('<![CDATA[') else m.group(0),
            xml_string
        )
        
        # Wrap other important fields in CDATA
        for tag in ['title', 'wp:post_name', 'guid', 'dc:creator', 'wp:meta_value']:
            xml_string = re.sub(
                f'<{tag}([^>]*)>([^<]+)</{tag}>',
                lambda m: f'<{tag}{m.group(1)}><![CDATA[{m.group(2)}]]></{tag}>' if not m.group(2).startswith('<![CDATA[') else m.group(0),
                xml_string
            )
        
        try:
            dom = minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent='    ', encoding='UTF-8')
            
            lines = pretty_xml.decode('utf-8').split('\n')
            clean_lines = [line for line in lines if line.strip()]
            clean_xml = '\n'.join(clean_lines)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_xml)
        except Exception as e:
            print(f"Warning: Using fallback XML formatting: {e}")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
                f.write(xml_string)
        
        return output_path


def main():
    """Example usage"""
    import sys
    import os
    
    print("🚀 Full WordPress Site Generator")
    print("=" * 60)
    
    generator = FullSiteGenerator()
    
    # Get YAML file from command line or use default
    yaml_file = sys.argv[1] if len(sys.argv) > 1 else 'full-site.yaml'
    print(f"📖 Loading configuration: {yaml_file}")
    
    # Load configuration
    config, rss = generator.process_yaml_to_wordpress(yaml_file)
    
    # Generate XML
    output_name = yaml_file.replace('.yaml', '.xml').replace('.yml', '.xml')
    output_path = generator.generate_wordpress_xml(config, rss, output_name)
    
    # Statistics
    file_size = os.path.getsize(output_path)
    print(f"📄 XML file size: {file_size / 1024:.1f} KB")
    print(f"✅ Complete WordPress site generated: {output_path}")
    print(f"📊 Items: {generator.item_counter - 100} total")


if __name__ == "__main__":
    main()