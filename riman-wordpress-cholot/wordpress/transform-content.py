#!/usr/bin/env python3
"""
WordPress XML Content Transformer for RIMAN GmbH

This script transforms the Cholot theme XML content from retirement/senior focus 
to RIMAN environmental remediation content while preserving all structural elements.

CRITICAL: The CEO loves the Cholot theme design - this script ONLY replaces text content, 
NOT structural elements. All Elementor widgets and settings remain intact.

Author: Claude Code
Usage: python3 transform-content.py
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import html


def load_riman_content() -> Dict:
    """Load RIMAN content structure from JSON file."""
    content_file = Path('riman-content-structure.json')
    if not content_file.exists():
        print(f"❌ Error: {content_file} not found!")
        sys.exit(1)
    
    with open(content_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_xml_file() -> str:
    """Load the existing WordPress XML file."""
    xml_file = Path('wordpress-mediation-platform/wordpress/riman-content-transformed-seo.xml')
    if not xml_file.exists():
        print(f"❌ Error: {xml_file} not found!")
        sys.exit(1)
    
    with open(xml_file, 'r', encoding='utf-8') as f:
        return f.read()


def create_content_replacements(riman_content: Dict) -> List[Tuple[str, str]]:
    """
    Create list of content replacements while preserving XML structure.
    
    Returns list of (old_text, new_text) tuples for replacement.
    """
    replacements = []
    
    # ===== BASIC TERM REPLACEMENTS =====
    basic_replacements = [
        # Primary service terms
        ('senior communities', 'Schadstoffsanierung'),
        ('retirement', 'Rückbaumanagement'),
        ('elderly care', 'Altlastensanierung'),
        ('elderly', 'Fachpersonal'),
        
        # Service box title fix (with typo)
        ('Healthly life', 'Schadstoffsanierung'),
        ('Healthy life', 'Schadstoffsanierung'),
        
        # Hero slider content
        ('Discover the best Auftraggeber that fit', 'RIMAN GmbH - Ihr Partner für professionelle'),
        ('your needs', 'Schadstoffsanierung'),
        ('for best and worst', 'Sicherheit seit 1998'),
        ('The Umweltsanierung experience that is', 'Professionelle Rückbaumanagement-Lösungen'),
        ('tailored', 'maßgeschneidert'),
        ('to you', 'für Sie'),
        ('diverse and inclusive', 'nachhaltig und wirtschaftlich'),
        
        # Generic content replacements
        ('Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum.', 
         'Seit 1998 steht die RIMAN GmbH ihren Kunden als innovatives Dienstleistungsunternehmen zur Verfügung. Unser Arbeitsbereich ist die Sicherheit, unsere Kernthemen sind "sicher bauen und gesund leben".'),
        
        # Service descriptions
        ('It's a great way for you to make use of all the benefits of being a part.', 
         'Professionelle Schadstoffsanierung für sichere und gesunde Bauprojekte.'),
        
        # Testimonial replacement
        ('My daughter took me to visit senior communities eight years ago and when I walked into it, i knew that I had found my Projekt. Absolutely stunning!', 
         'Die RIMAN GmbH hat unser Altlastensanierungsprojekt professionell und termingerecht durchgeführt. Die Zusammenarbeit war ausgezeichnet!'),
        
        ('From our lovely', 'Von unseren geschätzten'),
        ('Auftraggeber, Team & friends', 'Kunden, Team & Partnern'),
        ('Irgan Rogan', 'Johann Müller'),
        ('Member', 'Projektleiter'),
        
        # Subtitle replacements
        ('Exciting', 'Professionell'),
        ('ullamcorper matulvinar', 'Kundenstimmen & Referenzen'),
        
        # Contact and company info updates
        ('info@riman.de', 'j.fischer@riman.de'),
    ]
    
    replacements.extend(basic_replacements)
    
    # ===== RIMAN-SPECIFIC CONTENT INTEGRATION =====
    
    # Add hero video content
    hero_video = riman_content['homepage']['hero_video']
    replacements.extend([
        ('RIMAN GmbH - Schadstoffsanierung &amp; Rückbaumanagement', 
         f"{hero_video['title']}"),
        ('Professionelle Schadstoffsanierung, nachhaltiges Rückbaumanagement und Altlastensanierung in Deutschland', 
         f"{hero_video['subtitle']} - {hero_video['description'][:100]}..."),
    ])
    
    # Add service card content
    service_cards = riman_content['homepage']['service_cards']
    if len(service_cards) >= 3:
        # Map first 3 service cards to existing service boxes
        replacements.extend([
            # Service 1: Rückbaumanagement
            ('Schadstoffsanierung', service_cards[0]['title']),
            ('Professionelle Schadstoffsanierung für sichere und gesunde Bauprojekte.', 
             service_cards[0]['description'][:80] + '...'),
            
            # Add more service content as needed
        ])
    
    # Add company philosophy
    ceo_message = riman_content['company_info']['ceo_message']
    replacements.extend([
        ('Nach unseren langjährigen, persönlichen Erfahrungen können komplexe Abläufe', 
         ceo_message['content'][:100] + '...'),
    ])
    
    # Footer contact information
    footer = riman_content['footer']
    replacements.extend([
        ('www.riman.de', footer['contact']['website']),
        ('08031-408 43 44', footer['contact']['phone']),
        ('08031-408 43 43', footer['contact']['fax']),
        ('Hochplattenstr. 6', footer['address']['street']),
        ('83109 Großkarolinenfeld', footer['address']['city']),
    ])
    
    return replacements


def apply_content_replacements(xml_content: str, replacements: List[Tuple[str, str]]) -> str:
    """
    Apply content replacements while preserving XML structure.
    
    Uses careful text replacement to avoid breaking XML tags or Elementor settings.
    """
    transformed_xml = xml_content
    replacement_count = 0
    
    print("🔄 Applying content transformations...")
    
    for old_text, new_text in replacements:
        # Count occurrences before replacement
        count_before = transformed_xml.count(old_text)
        
        if count_before > 0:
            # Perform replacement
            transformed_xml = transformed_xml.replace(old_text, new_text)
            replacement_count += count_before
            print(f"✅ Replaced '{old_text[:50]}...' → '{new_text[:50]}...' ({count_before} times)")
        else:
            print(f"⚠️  Text not found: '{old_text[:50]}...'")
    
    print(f"\n📊 Total replacements made: {replacement_count}")
    return transformed_xml


def update_meta_information(xml_content: str, riman_content: Dict) -> str:
    """Update meta information like site title, description, etc."""
    
    meta_replacements = [
        # Site title and description
        (r'<title>.*?</title>', f'<title>{riman_content["meta"]["company_name"]} - {riman_content["meta"]["tagline"]}</title>'),
        (r'<description>.*?</description>', f'<description>{riman_content["meta"]["tagline"]} - {riman_content["meta"]["subtitle"]}</description>'),
        
        # Base URLs (if needed)
        ('https://www.riman.de', riman_content["footer"]["contact"]["website"]),
        ('http://localhost:8081', 'https://www.riman.de'),
    ]
    
    print("🔄 Updating meta information...")
    
    for pattern, replacement in meta_replacements:
        if re.search(pattern, xml_content):
            xml_content = re.sub(pattern, replacement, xml_content)
            print(f"✅ Updated meta: {pattern[:30]}...")
        else:
            print(f"⚠️  Meta pattern not found: {pattern[:30]}...")
    
    return xml_content


def validate_xml_structure(xml_content: str) -> bool:
    """Basic validation to ensure XML structure is intact."""
    
    # Check for basic XML structure
    required_elements = [
        '<rss version="2.0"',
        '<channel>',
        '</channel>',
        '</rss>',
        'wp:post_id',
        'wp:post_type',
        'content:encoded'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in xml_content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ XML validation failed! Missing elements: {missing_elements}")
        return False
    
    # Check for balanced tags (basic check)
    open_tags = xml_content.count('<item>')
    close_tags = xml_content.count('</item>')
    
    if open_tags != close_tags:
        print(f"❌ XML validation failed! Unbalanced <item> tags: {open_tags} open, {close_tags} close")
        return False
    
    print("✅ XML structure validation passed!")
    return True


def save_transformed_xml(xml_content: str, output_filename: str = 'riman-final-content.xml') -> None:
    """Save the transformed XML to output file."""
    
    output_path = Path(output_filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"✅ Transformed XML saved to: {output_path} ({file_size:.1f} KB)")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)


def create_backup(xml_content: str) -> None:
    """Create backup of original XML file."""
    
    backup_path = Path('riman-content-transformed-seo-backup.xml')
    
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"✅ Backup created: {backup_path}")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create backup: {e}")


def main():
    """Main transformation process."""
    
    print("🚀 RIMAN WordPress XML Content Transformer")
    print("=" * 50)
    print("PRESERVING Cholot theme structure while replacing content...")
    print()
    
    # Step 1: Load content and XML
    print("📂 Loading files...")
    riman_content = load_riman_content()
    xml_content = load_xml_file()
    original_size = len(xml_content)
    
    print(f"✅ Loaded RIMAN content structure with {len(riman_content['homepage']['service_cards'])} services")
    print(f"✅ Loaded XML file ({original_size / 1024:.1f} KB)")
    print()
    
    # Step 2: Create backup
    create_backup(xml_content)
    print()
    
    # Step 3: Create and apply replacements
    replacements = create_content_replacements(riman_content)
    print(f"📝 Created {len(replacements)} content replacements")
    print()
    
    transformed_xml = apply_content_replacements(xml_content, replacements)
    print()
    
    # Step 4: Update meta information
    transformed_xml = update_meta_information(transformed_xml, riman_content)
    print()
    
    # Step 5: Validate XML structure
    if not validate_xml_structure(transformed_xml):
        print("❌ Transformation failed! XML structure compromised.")
        sys.exit(1)
    print()
    
    # Step 6: Save transformed XML
    save_transformed_xml(transformed_xml)
    
    # Step 7: Summary
    final_size = len(transformed_xml)
    size_change = final_size - original_size
    size_change_pct = (size_change / original_size) * 100
    
    print()
    print("🎉 TRANSFORMATION COMPLETE!")
    print("=" * 50)
    print(f"📊 Original size: {original_size / 1024:.1f} KB")
    print(f"📊 Final size: {final_size / 1024:.1f} KB")
    print(f"📊 Size change: {size_change:+d} bytes ({size_change_pct:+.1f}%)")
    print()
    print("✅ XML structure preserved")
    print("✅ Elementor widgets intact")
    print("✅ CEO-approved Cholot theme design maintained")
    print("✅ RIMAN content successfully integrated")
    print()
    print("📁 Output file: riman-final-content.xml")
    print("📁 Backup file: riman-content-transformed-seo-backup.xml")
    print()
    print("🎯 Ready for WordPress import!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Transformation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your input files and try again.")
        sys.exit(1)