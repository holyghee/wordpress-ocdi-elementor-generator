<?php
// WordPress Bootstrap
define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Import using One Click Demo Import
require_once WP_PLUGIN_DIR . '/one-click-demo-import/vendor/awesomemotive/wp-content-importer-v2/src/WPImporterLogger.php';
require_once WP_PLUGIN_DIR . '/one-click-demo-import/vendor/awesomemotive/wp-content-importer-v2/src/WPImporterLoggerCLI.php';
require_once WP_PLUGIN_DIR . '/one-click-demo-import/vendor/awesomemotive/wp-content-importer-v2/src/WXRImporter.php';
require_once WP_PLUGIN_DIR . '/one-click-demo-import/inc/WXRImporter.php';

$file = 'riman-xl-site-no-images.xml';

if ( ! file_exists( $file ) ) {
    die( "Error: XML file not found: $file\n" );
}

echo "🚀 Starting import of $file\n";

// Create logger
$logger = new \AwesomeMotive\WPContentImporter2\WPImporterLoggerCLI();

// Create importer
$options = array(
    'fetch_attachments' => false,
    'default_author' => 1,
);

$importer = new \OCDI\WXRImporter( $options );
$importer->set_logger( $logger );

// Run import
$result = $importer->import( $file );

if ( is_wp_error( $result ) ) {
    echo "❌ Import failed: " . $result->get_error_message() . "\n";
} else {
    echo "✅ Import completed\n";
}

echo "\n--- Checking Results ---\n\n";

// Check if menu was created
$menus = wp_get_nav_menus();
echo "📋 Navigation Menus found: " . count($menus) . "\n";

if ( ! empty( $menus ) ) {
    foreach ( $menus as $menu ) {
        echo "  ✓ " . $menu->name . " (ID: " . $menu->term_id . ", Slug: " . $menu->slug . ")\n";
        
        // Get menu items
        $menu_items = wp_get_nav_menu_items( $menu->term_id );
        echo "    Items: " . count($menu_items) . "\n";
        
        if ( $menu_items ) {
            foreach ( $menu_items as $item ) {
                $indent = $item->menu_item_parent ? "      ↳ " : "      - ";
                echo $indent . $item->title . " (" . $item->type . ")\n";
            }
        }
    }
} else {
    echo "❌ No menus found!\n";
    
    // Debug: Check nav_menu terms
    $terms = get_terms( array(
        'taxonomy' => 'nav_menu',
        'hide_empty' => false,
    ) );
    
    echo "\n🔍 Debug - nav_menu taxonomy terms: " . count($terms) . "\n";
    if ( $terms ) {
        foreach ( $terms as $term ) {
            echo "  - Term: " . $term->name . " (ID: " . $term->term_id . ", Count: " . $term->count . ")\n";
        }
    }
    
    // Debug: Check nav_menu_items
    $menu_items = get_posts( array(
        'post_type' => 'nav_menu_item',
        'numberposts' => -1,
        'post_status' => 'publish',
    ) );
    
    echo "\n🔍 Debug - nav_menu_item posts: " . count($menu_items) . "\n";
    if ( $menu_items ) {
        foreach ( $menu_items as $item ) {
            $menu_terms = get_the_terms( $item->ID, 'nav_menu' );
            $menu_name = $menu_terms ? $menu_terms[0]->name : 'No menu';
            echo "  - " . get_the_title($item) . " (ID: " . $item->ID . ", Menu: " . $menu_name . ")\n";
        }
    }
}

// Check pages
echo "\n📄 Pages imported:\n";
$pages = get_pages();
foreach ( $pages as $page ) {
    echo "  - " . $page->post_title . " (ID: " . $page->ID . ")\n";
}