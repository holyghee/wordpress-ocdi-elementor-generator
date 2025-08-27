<?php
/**
 * Convert Cholot Elementor Templates to HTML
 */

function convert_xml_to_html($xml_file) {
    $xml = simplexml_load_file($xml_file);
    if (!$xml) {
        return false;
    }
    
    $html = '';
    
    // Process each item in the XML
    foreach ($xml->channel->item as $item) {
        $title = (string)$item->title;
        $content = (string)$item->children('content', true)->encoded;
        
        // Convert WordPress blocks to HTML
        $content = preg_replace('/<!-- wp:paragraph -->(.*?)<!-- \/wp:paragraph -->/s', '<p>$1</p>', $content);
        $content = preg_replace_callback('/<!-- wp:heading(.*?)-->(.*?)<!-- \/wp:heading -->/s', function($matches) {
            preg_match('/"level":(\d)/', $matches[1], $level);
            $h = isset($level[1]) ? $level[1] : 2;
            preg_match('/"textAlign":"(.*?)"/', $matches[1], $align);
            $class = isset($align[1]) ? ' class="text-' . $align[1] . '"' : '';
            return '<h' . $h . $class . '>' . strip_tags($matches[2]) . '</h' . $h . '>';
        }, $content);
        
        // Convert columns
        $content = preg_replace('/<!-- wp:columns(.*?)-->/s', '<div class="columns">', $content);
        $content = str_replace('<!-- /wp:columns -->', '</div>', $content);
        $content = preg_replace('/<!-- wp:column(.*?)-->/s', '<div class="column">', $content);
        $content = str_replace('<!-- /wp:column -->', '</div>', $content);
        
        // Convert lists
        $content = preg_replace('/<!-- wp:list -->(.*?)<!-- \/wp:list -->/s', '$1', $content);
        
        // Convert buttons
        $content = preg_replace_callback('/<!-- wp:buttons(.*?)-->(.*?)<!-- \/wp:buttons -->/s', function($matches) {
            return '<div class="buttons">' . $matches[2] . '</div>';
        }, $content);
        $content = preg_replace_callback('/<!-- wp:button(.*?)-->(.*?)<!-- \/wp:button -->/s', function($matches) {
            return str_replace('wp-block-button__link', 'btn', $matches[2]);
        }, $content);
        
        // Clean up remaining WordPress comments
        $content = preg_replace('/<!--.*?-->/s', '', $content);
        
        // Clean up classes
        $content = str_replace('wp-block-button', 'button-wrapper', $content);
        $content = str_replace('wp-block-', '', $content);
        
        $html .= '<section class="template-section">
            <h1>' . htmlspecialchars($title) . '</h1>
            ' . $content . '
        </section>';
    }
    
    return $html;
}

// Convert all template files
$template_dir = '/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/wp-content/plugins/one-click-demo-import/assets/demo-content/';
$templates = [
    'services-page.xml' => 'Services',
    'about-page.xml' => 'About',
    'contact-page.xml' => 'Contact',
    'portfolio-page.xml' => 'Portfolio',
    'testimonials-page.xml' => 'Testimonials',
    'faq-page.xml' => 'FAQ',
    'shop-page.xml' => 'Shop'
];

$all_html = '<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cholot Templates - Converted to HTML</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        
        .template-section {
            max-width: 1200px;
            margin: 40px auto;
            padding: 40px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .template-section h1 {
            color: #C8A882;
            border-bottom: 3px solid #C8A882;
            padding-bottom: 20px;
            margin-bottom: 30px;
            font-size: 36px;
            font-weight: 300;
        }
        
        h2, h3, h4 {
            margin: 20px 0;
            font-weight: 300;
        }
        
        h2 { font-size: 32px; }
        h3 { font-size: 24px; }
        
        .text-center { text-align: center; }
        
        p {
            margin: 15px 0;
            color: #666;
        }
        
        .columns {
            display: flex;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .column {
            flex: 1;
            min-width: 280px;
            padding: 30px;
            background: #f8f8f8;
            border-radius: 8px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .column:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .has-gray-background-color {
            background: #f8f8f8;
            padding: 40px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        ul {
            margin: 20px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 10px 0;
            color: #666;
        }
        
        .buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 30px 0;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: #C8A882;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 14px;
        }
        
        .btn:hover {
            background: #a08968;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(200,168,130,0.4);
        }
        
        .divider {
            height: 2px;
            background: linear-gradient(to right, transparent, #C8A882, transparent);
            margin: 60px 0;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .columns {
                flex-direction: column;
            }
            
            .template-section {
                margin: 20px;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div style="text-align: center; padding: 40px; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h1 style="color: #333; margin-bottom: 10px;">Cholot Template Collection</h1>
        <p style="color: #666;">Converted from WordPress/Elementor XML to Static HTML</p>
    </div>
';

foreach ($templates as $file => $name) {
    $xml_path = $template_dir . $file;
    if (file_exists($xml_path)) {
        echo "Converting $name ($file)...\n";
        $converted = convert_xml_to_html($xml_path);
        if ($converted) {
            $all_html .= $converted;
            $all_html .= '<div class="divider"></div>';
        }
    }
}

$all_html .= '
</body>
</html>';

// Save the complete HTML file
file_put_contents('cholot-templates-converted.html', $all_html);
echo "\n✓ All templates converted and saved to: cholot-templates-converted.html\n";

// Also save individual files
foreach ($templates as $file => $name) {
    $xml_path = $template_dir . $file;
    if (file_exists($xml_path)) {
        $converted = convert_xml_to_html($xml_path);
        if ($converted) {
            $individual_html = '<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>' . $name . ' - Cholot Template</title>
    <link rel="stylesheet" href="cholot-style.css">
</head>
<body>
' . $converted . '
</body>
</html>';
            
            $output_name = str_replace('.xml', '.html', $file);
            file_put_contents('exports/' . $output_name, $individual_html);
            echo "✓ Individual file saved: exports/$output_name\n";
        }
    }
}

echo "\nConversion complete!\n";