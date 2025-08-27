<?php
/**
 * Convert Elementor XML Export to Static HTML
 */

function elementor_xml_to_html($xml_file) {
    if (!file_exists($xml_file)) {
        die("XML file not found: $xml_file\n");
    }
    
    $xml = simplexml_load_file($xml_file);
    if (!$xml) {
        die("Failed to parse XML\n");
    }
    
    $html = '<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted from Elementor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .section { padding: 60px 0; }
        .row { display: flex; flex-wrap: wrap; margin: -15px; }
        .col { flex: 1; padding: 15px; min-width: 300px; }
        h1, h2, h3 { margin-bottom: 20px; font-weight: 300; }
        h1 { font-size: 48px; }
        h2 { font-size: 36px; }
        h3 { font-size: 24px; }
        p { margin-bottom: 15px; }
        img { max-width: 100%; height: auto; }
        .btn { display: inline-block; padding: 12px 30px; background: #C8A882; color: white; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s; }
        .btn:hover { background: #a08968; }
        .hero { background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), #333; color: white; text-align: center; padding: 100px 0; }
        .hero h1, .hero p { color: white; }
        .service-card { background: white; padding: 30px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 30px; }
        @media (max-width: 768px) { 
            .row { flex-direction: column; }
            h1 { font-size: 32px; }
        }
    </style>
</head>
<body>
';
    
    // Parse WordPress posts/pages from XML
    foreach ($xml->channel->item as $item) {
        $title = (string)$item->title;
        $content = (string)$item->children('content', true)->encoded;
        
        // Check if it contains Elementor data
        if (strpos($content, 'elementor') !== false) {
            // Try to extract text content
            $content = strip_tags($content, '<h1><h2><h3><h4><h5><h6><p><a><img><ul><li><ol><div><section>');
            
            $html .= '<div class="section">
                <div class="container">
                    <h2>' . htmlspecialchars($title) . '</h2>
                    ' . $content . '
                </div>
            </div>';
        }
    }
    
    $html .= '
</body>
</html>';
    
    return $html;
}

// Usage
if ($argc > 1) {
    $xml_file = $argv[1];
    $html = elementor_xml_to_html($xml_file);
    $output_file = str_replace('.xml', '.html', $xml_file);
    file_put_contents($output_file, $html);
    echo "Converted to: $output_file\n";
} else {
    echo "Usage: php elementor-xml-to-html.php <xml-file>\n";
}