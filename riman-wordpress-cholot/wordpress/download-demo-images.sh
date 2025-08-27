#!/bin/bash

# Download demo images from Cholot theme demo site
# These images are needed for the imported page to display correctly

echo "📥 Downloading Cholot demo images..."

# Create directories if they don't exist
WP_CONTENT="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/wp-content"
mkdir -p "$WP_CONTENT/uploads/2019/06"
mkdir -p "$WP_CONTENT/uploads/2019/07"

# List of images from the demo
IMAGES_06=(
    "esther-town-492626-unsplash-1.jpg"
    "huy-phan-100866-unsplash-1.jpg"
    "val-vesa-410839-unsplash.jpg"
    "matteo-vistocco-537858-unsplash.jpg"
    "anthony-metcalfe-580436-unsplash.jpg"
    "damir-bosnjak-366766-unsplash.jpg"
    "esther-town-492626-unsplash.jpg"
    "josh-appel-423804-unsplash.jpg"
    "vlad-sargu-479334-unsplash.jpg"
)

IMAGES_07=(
    "5.jpg"
    "5.png"
    "6.jpg"
    "7.jpg"
    "team1-1.jpg"
    "team2-1.jpg"
    "team3-1.jpg"
    "bg-ab.png"
    "1.jpg"
    "2.jpg"
)

# Download June 2019 images
for img in "${IMAGES_06[@]}"; do
    if [ ! -f "$WP_CONTENT/uploads/2019/06/$img" ]; then
        echo "Downloading $img..."
        curl -s "https://theme.winnertheme.com/cholot/wp-content/uploadz/2019/06/$img" -o "$WP_CONTENT/uploads/2019/06/$img" 2>/dev/null
        if [ $? -eq 0 ] && [ -s "$WP_CONTENT/uploads/2019/06/$img" ]; then
            echo "✅ Downloaded $img"
        else
            echo "❌ Failed to download $img"
            rm -f "$WP_CONTENT/uploads/2019/06/$img"
        fi
    else
        echo "⏭️  $img already exists"
    fi
done

# Download July 2019 images
for img in "${IMAGES_07[@]}"; do
    if [ ! -f "$WP_CONTENT/uploads/2019/07/$img" ]; then
        echo "Downloading $img..."
        curl -s "https://theme.winnertheme.com/cholot/wp-content/uploadz/2019/07/$img" -o "$WP_CONTENT/uploads/2019/07/$img" 2>/dev/null
        if [ $? -eq 0 ] && [ -s "$WP_CONTENT/uploads/2019/07/$img" ]; then
            echo "✅ Downloaded $img"
        else
            echo "❌ Failed to download $img"
            rm -f "$WP_CONTENT/uploads/2019/07/$img"
        fi
    else
        echo "⏭️  $img already exists"
    fi
done

echo ""
echo "🎉 Image download complete!"
echo ""
echo "📝 Next steps:"
echo "1. Import cholot-fixed-urls.xml into WordPress"
echo "2. The page should now display with all images"