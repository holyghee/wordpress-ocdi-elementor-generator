<?php
/**
 * Convert Elementor XML to HTML
 * 
 * This script helps convert Elementor content to static HTML
 */

// Set up proper server variables to avoid warnings
$_SERVER['HTTP_HOST'] = 'localhost:8080';
$_SERVER['REQUEST_URI'] = '/';
$_SERVER['SERVER_NAME'] = 'localhost';

// Load WordPress
require_once('wp-load.php');

// Function to get page HTML
function get_page_as_html($page_id) {
    $page = get_post($page_id);
    if (!$page) {
        return false;
    }
    
    // Get the content
    $content = apply_filters('the_content', $page->post_content);
    
    // Build complete HTML
    ob_start();
    ?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php echo get_the_title($page_id); ?></title>
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
    <div class="page-content">
        <?php echo $content; ?>
    </div>
    <?php wp_footer(); ?>
</body>
</html>
    <?php
    return ob_get_clean();
}

// Get all pages
$pages = get_pages();

echo "Available pages:\n";
foreach ($pages as $page) {
    echo "ID: {$page->ID} - Title: {$page->post_title}\n";
}

// Example: Export specific page
$page_id = 2; // Change this to your page ID
$html = get_page_as_html($page_id);

if ($html) {
    file_put_contents("page-{$page_id}.html", $html);
    echo "\nPage exported to page-{$page_id}.html\n";
}