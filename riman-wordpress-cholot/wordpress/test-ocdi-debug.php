<?php
/**
 * Debug OCDI Import to see what's happening
 */

define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Load OCDI plugin
require_once WP_PLUGIN_DIR . '/one-click-demo-import/vendor/autoload.php';

echo "🔍 OCDI Import Debug\n";
echo "====================\n\n";

// Get import files from filter
$import_files = apply_filters( 'ocdi/import_files', array() );
$selected_import = $import_files[0];

// Parse XML file to check structure
$xml_content = file_get_contents( $selected_import['local_import_file'] );
$xml = simplexml_load_string( $xml_content );

// Register namespaces
$xml->registerXPathNamespace('content', 'http://purl.org/rss/1.0/modules/content/');
$xml->registerXPathNamespace('excerpt', 'http://wordpress.org/export/1.2/excerpt/');
$xml->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');

echo "📄 XML Analysis:\n";
echo "----------------\n";

// Count items
$items = $xml->xpath('//item');
echo "Total items in XML: " . count($items) . "\n\n";

// Analyze item types
$types = [];
foreach ( $items as $item ) {
    $item->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');
    $post_type = (string) $item->xpath('wp:post_type')[0];
    if ( ! isset( $types[$post_type] ) ) {
        $types[$post_type] = 0;
    }
    $types[$post_type]++;
}

echo "Item types:\n";
foreach ( $types as $type => $count ) {
    echo "  - $type: $count\n";
}

// Check pages specifically
echo "\n📄 Pages in XML:\n";
$pages = $xml->xpath('//item[wp:post_type="page"]');
foreach ( $pages as $page ) {
    $page->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');
    $title = (string) $page->title;
    $status = (string) $page->xpath('wp:status')[0];
    $id = (string) $page->xpath('wp:post_id')[0];
    echo "  - ID: $id, Title: $title, Status: $status\n";
}

// Check menus
echo "\n📋 Menus in XML:\n";
$menus = $xml->xpath('//wp:term[wp:term_taxonomy="nav_menu"]');
foreach ( $menus as $menu ) {
    $name = (string) $menu->xpath('wp:term_name')[0];
    $slug = (string) $menu->xpath('wp:term_slug')[0];
    echo "  - $name (slug: $slug)\n";
}

// Check menu items
echo "\n📍 Menu Items in XML:\n";
$menu_items = $xml->xpath('//item[wp:post_type="nav_menu_item"]');
foreach ( $menu_items as $item ) {
    $item->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');
    $title = (string) $item->title;
    $menu_order = (string) $item->xpath('wp:menu_order')[0];
    
    // Get menu item object ID
    $postmeta = $item->xpath('wp:postmeta');
    $object_id = '';
    foreach ( $postmeta as $meta ) {
        if ( (string) $meta->xpath('wp:meta_key')[0] == '_menu_item_object_id' ) {
            $object_id = (string) $meta->xpath('wp:meta_value')[0];
            break;
        }
    }
    
    echo "  - Order: $menu_order, Title: $title, Object ID: $object_id\n";
}

echo "\n🔧 Testing OCDI Import Filters:\n";
echo "---------------------------------\n";

// Test if pages are being filtered
$test_page_data = [
    'post_type' => 'page',
    'post_status' => 'publish',
    'post_title' => 'Test Page',
];

// Apply OCDI filters
$filtered = apply_filters( 'wxr_importer.pre_process.post', $test_page_data );

if ( $filtered === false ) {
    echo "❌ Pages are being filtered out!\n";
} else {
    echo "✅ Pages should import normally\n";
}

// Check for active filters
echo "\n📝 Active filters on wxr_importer.pre_process.post:\n";
global $wp_filter;
if ( isset( $wp_filter['wxr_importer.pre_process.post'] ) ) {
    foreach ( $wp_filter['wxr_importer.pre_process.post'] as $priority => $hooks ) {
        foreach ( $hooks as $hook ) {
            $callback = $hook['function'];
            if ( is_array( $callback ) ) {
                if ( is_object( $callback[0] ) ) {
                    $class = get_class( $callback[0] );
                    echo "  - Priority $priority: $class::{$callback[1]}()\n";
                } else {
                    echo "  - Priority $priority: {$callback[0]}::{$callback[1]}()\n";
                }
            } elseif ( is_object( $callback ) ) {
                echo "  - Priority $priority: Closure\n";
            } else {
                echo "  - Priority $priority: $callback()\n";
            }
        }
    }
} else {
    echo "  No filters registered\n";
}