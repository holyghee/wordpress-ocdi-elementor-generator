#!/bin/bash

echo "🚀 Generating XML files for all Cholot templates..."
echo "=================================================="

# Generate individual page XMLs
echo ""
echo "📄 Generating individual page XMLs..."

python generate_wordpress_xml.py -i templates/home-page.yaml -o templates/home-page.xml
echo "✅ home-page.xml"

python generate_wordpress_xml.py -i templates/service-page.yaml -o templates/service-page.xml  
echo "✅ service-page.xml"

python generate_wordpress_xml.py -i templates/single-service-1.yaml -o templates/single-service-1.xml
echo "✅ single-service-1.xml"

python generate_wordpress_xml.py -i templates/single-service-2.yaml -o templates/single-service-2.xml
echo "✅ single-service-2.xml"

python generate_wordpress_xml.py -i templates/blog-page.yaml -o templates/blog-page.xml
echo "✅ blog-page.xml"

python generate_wordpress_xml.py -i templates/about-page.yaml -o templates/about-page.xml
echo "✅ about-page.xml"

python generate_wordpress_xml.py -i templates/contact-page.yaml -o templates/contact-page.xml
echo "✅ contact-page.xml"

# Generate master XML with all pages
echo ""
echo "📦 Generating master XML with all pages..."
python generate_wordpress_xml.py -i templates/cholot-complete-site.yaml -o templates/cholot-complete-site.xml
echo "✅ cholot-complete-site.xml"

echo ""
echo "=================================================="
echo "✨ All XML files generated successfully!"
echo ""
echo "📂 Location: templates/"
echo ""
echo "Import instructions:"
echo "1. For individual pages: Import templates/[page-name].xml"
echo "2. For complete site: Import templates/cholot-complete-site.xml"
echo ""
echo "All images will load from demo.ridianur.com automatically!"