<?php
// WordPress Bootstrap
define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Import the XML
$file = 'riman-xl-site-no-images.xml';

if ( ! file_exists( $file ) ) {
    die( "Error: XML file not found: $file\n" );
}

// Check if WordPress Importer is active
if ( ! class_exists( 'WP_Import' ) ) {
    $importer_file = WP_PLUGIN_DIR . '/wordpress-importer/wordpress-importer.php';
    if ( file_exists( $importer_file ) ) {
        require_once $importer_file;
    } else {
        die( "Error: WordPress Importer plugin not found\n" );
    }
}

echo "🚀 Starting import of $file\n";

// Create importer instance
$importer = new WP_Import();
$importer->fetch_attachments = false; // Don't download attachments

// Import the file
ob_start();
$importer->import( $file );
$output = ob_get_clean();

echo "✅ Import completed\n\n";

// Check if menu was created
$menus = wp_get_nav_menus();
echo "📋 Navigation Menus found: " . count($menus) . "\n";

if ( ! empty( $menus ) ) {
    foreach ( $menus as $menu ) {
        echo "  - " . $menu->name . " (ID: " . $menu->term_id . ", Slug: " . $menu->slug . ")\n";
        
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
    
    // Check nav_menu terms directly
    $terms = get_terms( array(
        'taxonomy' => 'nav_menu',
        'hide_empty' => false,
    ) );
    
    echo "\n🔍 Checking nav_menu taxonomy terms: " . count($terms) . "\n";
    foreach ( $terms as $term ) {
        echo "  - Term: " . $term->name . " (ID: " . $term->term_id . ")\n";
    }
    
    // Check nav_menu_items
    $menu_items = get_posts( array(
        'post_type' => 'nav_menu_item',
        'numberposts' => -1,
    ) );
    
    echo "\n🔍 Checking nav_menu_item posts: " . count($menu_items) . "\n";
    foreach ( $menu_items as $item ) {
        echo "  - " . get_the_title($item) . " (ID: " . $item->ID . ")\n";
    }
}

// Check pages
$pages = get_pages();
echo "\n📄 Pages imported: " . count($pages) . "\n";
foreach ( $pages as $page ) {
    echo "  - " . $page->post_title . " (ID: " . $page->ID . ")\n";
}