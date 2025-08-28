<?php
/**
 * Direct OCDI WXRImporter test
 */

define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Load OCDI plugin
require_once WP_PLUGIN_DIR . '/one-click-demo-import/vendor/autoload.php';

echo "🚀 Direct OCDI WXRImporter Test\n";
echo "================================\n\n";

$import_file = ABSPATH . 'riman-xl-site-no-images.xml';

// Create logger
$logger = new \OCDI\Logger();
$logger->min_level = 'info'; // Show all logs

// Create WXRImporter instance directly
$options = array(
    'fetch_attachments' => false,
    'default_author' => 1,
);

$importer = new \OCDI\WXRImporter( $options );
$importer->set_logger( $logger );

echo "📄 Importing: $import_file\n\n";

// Import the file
$result = $importer->import( $import_file );

if ( is_wp_error( $result ) ) {
    echo "❌ Import failed: " . $result->get_error_message() . "\n";
} else {
    echo "✅ Import completed!\n";
    
    // Show import stats
    echo "\n📊 Import Stats:\n";
    echo "-----------------\n";
    
    $import_data = $importer->get_importer_data();
    
    if ( ! empty( $import_data['mapping']['post'] ) ) {
        echo "\nPost ID mappings:\n";
        foreach ( $import_data['mapping']['post'] as $old_id => $new_id ) {
            echo "  Old ID $old_id -> New ID $new_id\n";
        }
    }
}

// Check results
echo "\n📊 Database Results:\n";
echo "--------------------\n";

// Check pages
$pages = get_pages();
echo "\n📄 Pages: " . count( $pages ) . "\n";
foreach ( $pages as $page ) {
    $elementor_data = get_post_meta( $page->ID, '_elementor_data', true );
    $has_elementor = ! empty( $elementor_data ) ? ' ✅ Has Elementor' : '';
    echo "  - " . $page->post_title . " (ID: " . $page->ID . ")$has_elementor\n";
}

// Check menus
$menus = wp_get_nav_menus();
echo "\n📋 Menus: " . count( $menus ) . "\n";
foreach ( $menus as $menu ) {
    $items = wp_get_nav_menu_items( $menu->term_id );
    echo "  - " . $menu->name . " (ID: " . $menu->term_id . ", Items: " . count( $items ) . ")\n";
}