<?php
/**
 * Save WordPress page as static HTML
 * Run this from command line: php save-page-as-html.php
 */

// Simulate a web request
$_SERVER['HTTP_HOST'] = 'localhost:8080';
$_SERVER['REQUEST_URI'] = '/';
$_SERVER['SERVER_NAME'] = 'localhost';

// Load WordPress
require_once('wp-load.php');

function save_page_as_static_html($url, $filename) {
    // Get the page content
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible; WordPress HTML Exporter)');
    
    $html = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($http_code == 200 && $html) {
        // Make URLs relative
        $html = str_replace('http://localhost:8080/', '/', $html);
        $html = str_replace('https://localhost:8080/', '/', $html);
        
        // Save the HTML
        file_put_contents($filename, $html);
        return true;
    }
    
    return false;
}

// Get all published pages
$pages = get_pages(array(
    'post_status' => 'publish'
));

echo "Found " . count($pages) . " pages\n\n";

foreach ($pages as $page) {
    $permalink = get_permalink($page->ID);
    $filename = 'export/' . $page->post_name . '.html';
    
    echo "Exporting: {$page->post_title}\n";
    echo "URL: $permalink\n";
    
    // Create export directory if not exists
    if (!file_exists('export')) {
        mkdir('export', 0755, true);
    }
    
    if (save_page_as_static_html($permalink, $filename)) {
        echo "✓ Saved to: $filename\n\n";
    } else {
        echo "✗ Failed to export\n\n";
    }
}

echo "Export complete!\n";