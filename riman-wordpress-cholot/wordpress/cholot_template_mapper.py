#!/usr/bin/env python3
"""
Cholot Template Mapper - Maps existing templates to target pages for exact replication.

This script analyzes the target structure and creates precise mappings between:
- Target pages and available templates
- Page sections and Elementor blocks
- Widget types and configurations

Author: Template Mapper Agent
Created: 2025-08-28
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

class CholotTemplateMapper:
    """Maps templates and blocks to target pages for exact replication."""
    
    def __init__(self, work_dir: str = '.'):
        self.work_dir = Path(work_dir)
        self.templates_dir = self.work_dir / 'templates'
        self.blocks_dir = self.work_dir / 'elemetor blocks'
        self.target_structure = {}
        self.mappings = {}
        
    def load_target_structure(self) -> bool:
        """Load the target structure file created by XML analyzer."""
        try:
            structure_file = self.work_dir / 'cholot_target_structure.json'
            if structure_file.exists():
                print(f"Loading target structure from {structure_file}")
                with open(structure_file, 'r', encoding='utf-8') as f:
                    self.target_structure = json.load(f)
                return True
            else:
                print(f"Target structure file not found: {structure_file}")
                return False
        except Exception as e:
            print(f"Error loading target structure: {e}")
            return False
    
    def analyze_available_templates(self) -> Dict[str, Dict]:
        """Analyze all available templates and their characteristics."""
        templates = {}
        
        if not self.templates_dir.exists():
            print(f"Templates directory not found: {self.templates_dir}")
            return templates
            
        for template_file in self.templates_dir.glob('*.json'):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    
                template_name = template_file.stem
                templates[template_name] = {
                    'file': str(template_file),
                    'type': self._determine_template_type(template_name, template_data),
                    'widgets': self._extract_widget_types(template_data),
                    'sections': self._count_sections(template_data),
                    'complexity': self._assess_complexity(template_data)
                }
                print(f"Analyzed template: {template_name}")
                
            except Exception as e:
                print(f"Error analyzing template {template_file}: {e}")
                
        return templates
    
    def analyze_available_blocks(self) -> Dict[str, Dict]:
        """Analyze all available Elementor blocks."""
        blocks = {}
        
        if not self.blocks_dir.exists():
            print(f"Blocks directory not found: {self.blocks_dir}")
            return blocks
            
        for block_file in self.blocks_dir.glob('*.json'):
            try:
                with open(block_file, 'r', encoding='utf-8') as f:
                    block_data = json.load(f)
                    
                block_name = block_file.stem
                blocks[block_name] = {
                    'file': str(block_file),
                    'type': self._determine_block_type(block_name, block_data),
                    'widgets': self._extract_widget_types(block_data),
                    'purpose': self._infer_block_purpose(block_name),
                    'compatibility': self._assess_block_compatibility(block_data)
                }
                print(f"Analyzed block: {block_name}")
                
            except Exception as e:
                print(f"Error analyzing block {block_file}: {e}")
                
        return blocks
    
    def map_pages_to_templates(self, pages: List[Dict], templates: Dict[str, Dict]) -> Dict[str, str]:
        """Map each target page to the best matching template."""
        page_mappings = {}
        
        for page in pages:
            page_slug = page.get('post_name', '')
            page_title = page.get('title', '')
            page_type = page.get('post_type', 'page')
            
            if page_type != 'page':
                continue
                
            # Find best matching template
            best_template = self._find_best_template_match(page_slug, page_title, templates)
            page_mappings[page_slug] = best_template
            print(f"Mapped page '{page_slug}' to template '{best_template}'")
            
        return page_mappings
    
    def map_sections_to_blocks(self, blocks: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Map page sections to appropriate Elementor blocks."""
        section_mappings = {
            'hero': ['elementor-hero-home-1656-2025-08-28'],
            'service_cards': ['elementor-service-cards-home-1659-2025-08-28'],
            'overview': ['elementor-overview-home-1663-2025-08-28'],
            'team': ['elementor-team-home-1666-2025-08-28'],
            'testimonials': ['elementor-testemonials-home-1672-2025-08-28'],
            'posts': ['elementor-block-posts-home-1678-2025-08-28'],
            'contact': ['elementor-contact-box-home-1681-2025-08-28'],
            'service_hero': ['elementor-service-hero-services-1684-2025-08-28'],
            'header': ['elementor-heading-section-home-1675-2025-08-28']
        }
        
        return section_mappings
    
    def create_widget_mappings(self) -> Dict[str, Dict]:
        """Create mappings for widget types and their configurations."""
        widget_mappings = {
            'cholot-texticon': {
                'purpose': 'Icon with text content blocks',
                'usage': 'Service descriptions, feature highlights',
                'template_files': ['cholot-texticon.template.json']
            },
            'cholot-team': {
                'purpose': 'Team member display',
                'usage': 'About page team sections',
                'template_files': ['cholot-team.template.json']
            },
            'cholot-testimonial-two': {
                'purpose': 'Customer testimonials carousel',
                'usage': 'Social proof sections',
                'template_files': ['cholot-testimonial-two.template.json']
            },
            'cholot-title': {
                'purpose': 'Styled page titles and headings',
                'usage': 'Section headers across all pages',
                'template_files': ['cholot-title.template.json']
            },
            'cholot-contact': {
                'purpose': 'Contact forms integration',
                'usage': 'Contact page, lead generation',
                'template_files': ['cholot-contact.template.json']
            },
            'cholot-text-line': {
                'purpose': 'Text with decorative line elements',
                'usage': 'Service descriptions, content sections',
                'template_files': ['cholot-text-line.template.json']
            },
            'rdn-slider': {
                'purpose': 'Hero image sliders',
                'usage': 'Homepage hero sections',
                'template_files': ['rdn-slider.template.json']
            },
            'image': {
                'purpose': 'Image display with various styling options',
                'usage': 'All pages for visual content',
                'template_files': ['image.template.json']
            },
            'video': {
                'purpose': 'Video content embedding',
                'usage': 'Homepage, service pages',
                'template_files': ['video.template.json']
            },
            'text-editor': {
                'purpose': 'Rich text content',
                'usage': 'All pages for text content',
                'template_files': ['text-editor.template.json']
            },
            'divider': {
                'purpose': 'Visual section separators',
                'usage': 'All pages for content separation',
                'template_files': ['divider.template.json']
            },
            'icon': {
                'purpose': 'Standalone icons',
                'usage': 'Service sections, feature highlights',
                'template_files': ['icon.template.json']
            }
        }
        
        return widget_mappings
    
    def generate_complete_mapping(self) -> Dict[str, Any]:
        """Generate the complete mapping configuration."""
        print("Starting complete mapping generation...")
        
        if not self.load_target_structure():
            return {}
            
        # Analyze available resources
        templates = self.analyze_available_templates()
        blocks = self.analyze_available_blocks()
        
        # Extract pages from target structure
        pages = []
        if 'pages' in self.target_structure:
            pages = []
            for page_id, page_data in self.target_structure['pages'].items():
                if isinstance(page_data, dict):
                    page_data['post_name'] = self._extract_slug_from_link(page_data.get('link', ''))
                    page_data['post_type'] = 'page'
                    pages.append(page_data)
        
        # Create mappings
        page_mappings = self.map_pages_to_templates(pages, templates)
        section_mappings = self.map_sections_to_blocks(blocks)
        widget_mappings = self.create_widget_mappings()
        
        # Generate complete mapping
        complete_mapping = {
            'metadata': {
                'created': '2025-08-28',
                'version': '1.0',
                'description': 'Cholot template mappings for exact replication',
                'total_pages': len(pages),
                'total_templates': len(templates),
                'total_blocks': len(blocks)
            },
            'page_mappings': page_mappings,
            'section_mappings': section_mappings,
            'widget_mappings': widget_mappings,
            'templates_analysis': templates,
            'blocks_analysis': blocks,
            'replication_strategy': {
                'approach': 'exact_match',
                'priority_order': ['home', 'about', 'service', 'contact'],
                'fallback_templates': {
                    'home': 'home-page',
                    'about': 'about-page',
                    'service': 'service-page',
                    'contact': 'contact-page',
                    'default': 'home-page'
                }
            }
        }
        
        return complete_mapping
    
    def _determine_template_type(self, name: str, data: Any) -> str:
        """Determine the type of template based on name and content."""
        name_lower = name.lower()
        if 'home' in name_lower:
            return 'homepage'
        elif 'about' in name_lower:
            return 'about_page'
        elif 'service' in name_lower:
            return 'service_page'
        elif 'contact' in name_lower:
            return 'contact_page'
        elif 'blog' in name_lower:
            return 'blog_page'
        else:
            return 'generic_page'
    
    def _determine_block_type(self, name: str, data: Any) -> str:
        """Determine the type of Elementor block based on name and content."""
        name_lower = name.lower()
        if 'hero' in name_lower:
            return 'hero_section'
        elif 'service' in name_lower:
            return 'service_section'
        elif 'team' in name_lower:
            return 'team_section'
        elif 'testimonial' in name_lower:
            return 'testimonial_section'
        elif 'contact' in name_lower:
            return 'contact_section'
        elif 'header' in name_lower or 'heading' in name_lower:
            return 'header_section'
        elif 'overview' in name_lower:
            return 'overview_section'
        elif 'post' in name_lower:
            return 'posts_section'
        else:
            return 'content_section'
    
    def _extract_widget_types(self, data: Any) -> List[str]:
        """Extract widget types from template or block data."""
        widgets = []
        
        def extract_from_element(element):
            if isinstance(element, dict):
                if 'widgetType' in element:
                    widgets.append(element['widgetType'])
                if 'elements' in element:
                    for sub_element in element['elements']:
                        extract_from_element(sub_element)
        
        if isinstance(data, list):
            for item in data:
                extract_from_element(item)
        elif isinstance(data, dict):
            if 'content' in data:
                extract_from_element(data['content'])
            else:
                extract_from_element(data)
                
        return list(set(widgets))  # Remove duplicates
    
    def _count_sections(self, data: Any) -> int:
        """Count the number of sections in template data."""
        sections = 0
        
        def count_from_element(element):
            nonlocal sections
            if isinstance(element, dict):
                if element.get('elType') == 'section':
                    sections += 1
                if 'elements' in element:
                    for sub_element in element['elements']:
                        count_from_element(sub_element)
        
        if isinstance(data, list):
            for item in data:
                count_from_element(item)
        elif isinstance(data, dict):
            if 'content' in data:
                count_from_element(data['content'])
            else:
                count_from_element(data)
                
        return sections
    
    def _assess_complexity(self, data: Any) -> str:
        """Assess the complexity of template data."""
        widget_count = len(self._extract_widget_types(data))
        section_count = self._count_sections(data)
        
        if widget_count > 10 or section_count > 8:
            return 'high'
        elif widget_count > 5 or section_count > 4:
            return 'medium'
        else:
            return 'low'
    
    def _infer_block_purpose(self, name: str) -> str:
        """Infer the purpose of a block from its name."""
        name_lower = name.lower()
        if 'hero' in name_lower:
            return 'Landing section with large image/video and call-to-action'
        elif 'service' in name_lower:
            return 'Service offerings display with icons and descriptions'
        elif 'team' in name_lower:
            return 'Team member profiles with photos and social links'
        elif 'testimonial' in name_lower:
            return 'Customer testimonials with quotes and ratings'
        elif 'contact' in name_lower:
            return 'Contact forms and information display'
        elif 'overview' in name_lower:
            return 'Content overview with statistics or highlights'
        elif 'post' in name_lower:
            return 'Blog posts or news display'
        else:
            return 'General content section'
    
    def _assess_block_compatibility(self, data: Any) -> List[str]:
        """Assess which page types this block is compatible with."""
        widgets = self._extract_widget_types(data)
        compatibility = []
        
        if 'rdn-slider' in widgets:
            compatibility.append('homepage')
        if 'cholot-team' in widgets:
            compatibility.append('about_page')
        if 'cholot-contact' in widgets:
            compatibility.append('contact_page')
        if 'cholot-texticon' in widgets:
            compatibility.extend(['service_page', 'homepage'])
        if 'cholot-testimonial-two' in widgets:
            compatibility.extend(['homepage', 'about_page'])
        
        return list(set(compatibility)) if compatibility else ['any']
    
    def _find_best_template_match(self, page_slug: str, page_title: str, templates: Dict[str, Dict]) -> str:
        """Find the best matching template for a page."""
        # Direct slug matches
        for template_name in templates:
            if page_slug in template_name.lower():
                return template_name
        
        # Title-based matches
        title_lower = page_title.lower()
        for template_name, template_data in templates.items():
            template_lower = template_name.lower()
            if any(word in template_lower for word in title_lower.split()):
                return template_name
        
        # Fallback mapping
        fallback_map = {
            'home': 'home-page',
            'about': 'about-page',
            'service': 'service-page',
            'services': 'service-page',
            'contact': 'contact-page',
            'blog': 'blog-page'
        }
        
        for keyword, template in fallback_map.items():
            if keyword in page_slug.lower():
                return template if template in templates else 'home-page'
        
        return 'home-page'  # Ultimate fallback

def main():
    """Main execution function."""
    mapper = CholotTemplateMapper()
    
    print("=== Cholot Template Mapper ===")
    print("Generating template mappings for exact replication...")
    
    # Generate complete mapping
    mappings = mapper.generate_complete_mapping()
    
    if mappings:
        # Save to file
        output_file = mapper.work_dir / 'cholot_template_mappings.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Template mappings saved to: {output_file}")
        print(f"📊 Mapping Summary:")
        print(f"   • Pages mapped: {len(mappings.get('page_mappings', {}))}")
        print(f"   • Templates analyzed: {mappings['metadata']['total_templates']}")
        print(f"   • Blocks analyzed: {mappings['metadata']['total_blocks']}")
        print(f"   • Widget types: {len(mappings.get('widget_mappings', {}))}")
        
        # Display key mappings
        if 'page_mappings' in mappings:
            print(f"\n📋 Page → Template Mappings:")
            for page, template in mappings['page_mappings'].items():
                print(f"   • {page} → {template}")
        
        return True
    else:
        print("❌ Failed to generate mappings")
        return False

if __name__ == "__main__":
    main()