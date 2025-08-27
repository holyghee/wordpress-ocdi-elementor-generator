#!/bin/bash

# Image Processing Script for RIMAN WordPress Images
# Converts, optimizes and renames images with SEO-friendly German names

SOURCE_DIR="/Users/holgerbrandt/dev/claude-code/tools/midjourney-mcp-server/midjourney-images"
TARGET_DIR="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/wp-content/uploads/2025/08"
YEAR_DIR="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/wp-content/uploads/2025"

# Create upload directories if they don't exist
mkdir -p "$TARGET_DIR"

# Function to process single image
process_image() {
    local source_file="$1"
    local target_name="$2"
    local format="$3"
    
    if [ -f "$SOURCE_DIR/$source_file" ]; then
        echo "Processing: $source_file -> $target_name.$format"
        
        # Convert and optimize based on format
        if [ "$format" = "jpg" ]; then
            # Convert to JPEG with 85% quality for web
            convert "$SOURCE_DIR/$source_file" \
                -quality 85 \
                -strip \
                -resize "2048x2048>" \
                -interlace Plane \
                -gaussian-blur 0.05 \
                -colorspace sRGB \
                "$TARGET_DIR/$target_name.jpg"
            
            # Create WebP version for modern browsers
            convert "$SOURCE_DIR/$source_file" \
                -quality 85 \
                -define webp:method=6 \
                -resize "2048x2048>" \
                "$TARGET_DIR/$target_name.webp"
                
            # Create thumbnail version (300x300)
            convert "$SOURCE_DIR/$source_file" \
                -quality 80 \
                -strip \
                -resize "300x300^" \
                -gravity center \
                -crop 300x300+0+0 \
                "$TARGET_DIR/${target_name}-300x300.jpg"
                
            # Create medium version (768x768)
            convert "$SOURCE_DIR/$source_file" \
                -quality 85 \
                -strip \
                -resize "768x768>" \
                "$TARGET_DIR/${target_name}-768x768.jpg"
                
        elif [ "$format" = "png" ]; then
            # Optimize PNG with pngquant
            convert "$SOURCE_DIR/$source_file" \
                -strip \
                -resize "1024x1024>" \
                "$TARGET_DIR/$target_name.png"
                
            # Additional PNG optimization if pngquant is available
            if command -v pngquant &> /dev/null; then
                pngquant --quality=80-95 \
                    --strip \
                    --force \
                    --output "$TARGET_DIR/$target_name-optimized.png" \
                    "$TARGET_DIR/$target_name.png"
                mv "$TARGET_DIR/$target_name-optimized.png" "$TARGET_DIR/$target_name.png"
            fi
        fi
        
        echo "✅ Completed: $target_name.$format"
    else
        echo "❌ Source file not found: $source_file"
    fi
}

# Process all images based on mapping
echo "🖼️  Starting RIMAN Image Processing..."
echo "=================================="

# Hero and main content images
process_image "midjourney_upscaled_1756308379995.png" "schadstoffsanierung-industrieanlage-riman-gmbh" "jpg"
process_image "midjourney_upscaled_1756308481881.png" "umweltingenieur-bodenproben-analyse-labor" "jpg"
process_image "midjourney_upscaled_1756308562681.png" "nachhaltiger-rueckbau-baustelle-recycling" "jpg"
process_image "midjourney_upscaled_1756308647568.png" "bim-planung-digitalisierung-baumanagement" "jpg"
process_image "midjourney_upscaled_1756308769362.png" "asbestsanierung-schutzausruestung-fachpersonal" "jpg"
process_image "midjourney_upscaled_1756308848918.png" "systematischer-gebaeuderueckbau-kreislaufwirtschaft" "jpg"
process_image "midjourney_upscaled_1756308931737.png" "altlastensanierung-grundwasser-bodenschutz" "jpg"
process_image "midjourney_upscaled_1756309023055.png" "baumediation-konfliktloesung-projektmanagement" "jpg"

# Process steps
process_image "midjourney_upscaled_1756309240187.png" "standortbewertung-umweltanalyse-schritt-1" "jpg"
process_image "midjourney_upscaled_1756309322397.png" "projektplanung-bim-visualisierung-schritt-2" "jpg"
process_image "midjourney_upscaled_1756309407197.png" "sicherheitsvorbereitung-schutzausruestung-schritt-3" "jpg"
process_image "midjourney_upscaled_1756309522825.png" "sanierung-durchfuehrung-fachgerecht-schritt-4" "jpg"
process_image "midjourney_upscaled_1756309602530.png" "luftqualitaet-monitoring-echtzeitdaten-schritt-5" "jpg"
process_image "midjourney_upscaled_1756309683117.png" "materialverarbeitung-entsorgung-vorschriften-schritt-6" "jpg"
process_image "midjourney_upscaled_1756309776542.png" "qualitaetskontrolle-abnahme-pruefung-schritt-7" "jpg"
process_image "midjourney_upscaled_1756309862567.png" "zertifizierung-dokumentation-abschluss-schritt-8" "jpg"

# Team images
process_image "midjourney_upscaled_1756310036850.png" "dr-michael-riman-geschaeftsfuehrer" "jpg"
process_image "midjourney_upscaled_1756310052257.png" "sabine-weber-projektleitung" "jpg"
process_image "midjourney_upscaled_1756310073197.png" "thomas-mueller-technische-leitung" "jpg"

# Logo and brand elements
process_image "midjourney_upscaled_1756310088407.png" "riman-gmbh-logo" "png"
process_image "midjourney_upscaled_1756310121399.png" "riman-gmbh-logo-weiss" "png"
process_image "midjourney_upscaled_1756310155296.png" "riman-gmbh-firmenschild-gebaeude" "jpg"

# Backgrounds
process_image "midjourney_upscaled_1756310173757.png" "umweltschutz-molekularstruktur-hintergrund" "jpg"
process_image "midjourney_upscaled_1756310193524.png" "schadstoffsanierung-detailaufnahme-ausruestung" "jpg"

echo "=================================="
echo "✅ Image processing complete!"
echo "📁 Images saved to: $TARGET_DIR"

# Generate file size report
echo ""
echo "📊 File Size Report:"
echo "-------------------"
du -sh "$TARGET_DIR"/*.{jpg,png,webp} 2>/dev/null | sort -h

echo ""
echo "🎯 Total images processed: $(ls -1 $TARGET_DIR/*.{jpg,png,webp} 2>/dev/null | wc -l)"
echo "💾 Total size: $(du -sh $TARGET_DIR | cut -f1)"