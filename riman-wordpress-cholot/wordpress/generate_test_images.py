#!/usr/bin/env python3
"""
Generate test images for RIMAN website
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory
os.makedirs('images', exist_ok=True)

def create_test_image(filename, title, color):
    """Create a test image with text"""
    # Create image
    img = Image.new('RGB', (1920, 1080), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    except:
        font = ImageFont.load_default()
    
    # Center text
    text = title
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((1920 - text_width) // 2, (1080 - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    # Save
    img.save(f'images/{filename}')
    print(f"✅ Created {filename}")

# Hero images
create_test_image('hero-sanierung.jpg', 'RIMAN Schadstoffsanierung', (70, 90, 120))
create_test_image('hero-umwelt.jpg', 'RIMAN Umweltschutz', (90, 120, 70))

# Service images
create_test_image('asbestsanierung-schutzausruestung-fachpersonal.jpg', 'Asbestsanierung', (182, 140, 47))
create_test_image('schadstoffsanierung-industrieanlage-riman-gmbh.jpg', 'PCB-Sanierung', (140, 100, 47))
create_test_image('umweltingenieur-bodenproben-analyse-labor.jpg', 'Schimmelsanierung', (100, 140, 47))

print("\n✅ All test images generated!")
print("📁 Images saved in: images/")