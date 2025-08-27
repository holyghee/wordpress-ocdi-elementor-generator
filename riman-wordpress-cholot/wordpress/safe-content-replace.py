#!/usr/bin/env python3
"""
Safe content replacement - preserves ALL structure, only replaces text content.
"""
import re
from pathlib import Path

def safe_replace_content():
    """Replace ONLY text content without breaking structure."""
    
    # Use the ORIGINAL demo file that works
    original_file = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/demo-data-fixed.xml")
    output_file = Path("riman-safe-content.xml")
    
    print(f"Reading original working XML: {original_file}")
    with open(original_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print("Applying safe text replacements...")
    
    # 1. Main site title
    xml_content = xml_content.replace(
        '<title>Cholot - Retirement Community</title>',
        '<title>RIMAN GmbH - Schadstoffsanierung und Rückbaumanagement</title>'
    )
    
    # 2. Replace specific text content in posts/pages
    text_replacements = {
        # Hero slider
        'Discover the best retirement that fit <span>your needs</span>': 
            'Professionelle Schadstoffsanierung für <span>Ihre Sicherheit</span>',
        'for best and worst': 'Kompetenz seit 1998',
        'The retirement experience that is <span>tailored</span> to you': 
            'Rückbaumanagement mit <span>Expertise</span> und Sorgfalt',
        'diverse and inclusive': 'Sicher und nachhaltig',
        
        # Service boxes - keep structure, change text only
        'Healthly life': 'Schadstoffsanierung',
        'Improving life': 'Rückbaumanagement',
        'Relationship': 'Altlastensanierung',
        'Exciting': 'Professionell',
        'retired': 'Zertifiziert',
        
        # About section
        'Building with our residents is something we keep close to our heart':
            'Sicherheit und Umweltschutz sind unsere oberste Priorität',
        
        # Testimonial
        'My daughter took me to visit senior communities':
            'RIMAN GmbH hat unser Projekt professionell durchgeführt',
        
        # Keep Cholot references for theme compatibility!
        # Don't change: cholot_header_position, cholot-*, widgetType names
    }
    
    for old_text, new_text in text_replacements.items():
        xml_content = xml_content.replace(old_text, new_text)
    
    # 3. Update contact info in footer
    xml_content = xml_content.replace(
        'Buah Batu Street 886 - ID',
        'Hochplattenstr. 6, 83109 Großkarolinenfeld'
    )
    xml_content = xml_content.replace(
        '+122 - 000 - 000',
        '+49 8031 408 43 44'
    )
    xml_content = xml_content.replace(
        'email@email.com',
        'j.fischer@riman.de'
    )
    
    # 4. Update image URLs to our server
    xml_content = xml_content.replace(
        'https://theme.winnertheme.com/cholot/wp-content/uploads/',
        'http://localhost:8082/'
    )
    
    # 5. Update site URL
    xml_content = xml_content.replace(
        'https://theme.winnertheme.com/cholot',
        'http://localhost:8081'
    )
    
    print(f"Writing safe content XML to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("✅ Created safe content replacement")
    print("⚠️  This preserves ALL Cholot theme structure")
    print("📁 Import: riman-safe-content.xml")

if __name__ == "__main__":
    safe_replace_content()