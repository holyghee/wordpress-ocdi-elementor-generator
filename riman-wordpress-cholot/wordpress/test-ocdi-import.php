<?php
/**
 * Test OCDI Import programmatically
 */

define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Load OCDI plugin
require_once WP_PLUGIN_DIR . '/one-click-demo-import/vendor/autoload.php';

echo "🚀 Starting OCDI Import Test\n";
echo "================================\n\n";

// Get import files from filter
$import_files = apply_filters( 'ocdi/import_files', array() );

if ( empty( $import_files ) ) {
    die( "❌ No import files defined!\n" );
}

echo "📦 Found " . count( $import_files ) . " import configuration(s)\n";

foreach ( $import_files as $index => $import ) {
    echo "  " . ( $index + 1 ) . ". " . $import['import_file_name'] . "\n";
}

$selected_import = $import_files[0];
echo "\n✅ Using: " . $selected_import['import_file_name'] . "\n";
echo "📄 File: " . $selected_import['local_import_file'] . "\n";

// Check if file exists
if ( ! file_exists( $selected_import['local_import_file'] ) ) {
    die( "❌ Import file not found!\n" );
}

echo "\n📊 Starting import...\n";
echo "--------------------\n";

// Create OCDI instance
$ocdi = \OCDI\OneClickDemoImport::get_instance();

// Set selected import files
$ocdi->import_files = $import_files;
$ocdi->selected_index = 0;

// Create importer instance
$logger = new \OCDI\Logger();
$importer_instance = new \OCDI\Importer( array( 'fetch_attachments' => false ), $logger );

// Import content
echo "📄 Importing content...\n";
$importer_instance->import_content( $selected_import['local_import_file'] );

// Run after import actions
echo "\n🔧 Running after import actions...\n";
do_action( 'ocdi/after_import', $selected_import );

echo "\n================================\n";
echo "✅ Import process completed!\n\n";

// Check results
echo "📊 Import Results:\n";
echo "------------------\n";

// Check pages
$pages = get_pages();
echo "\n📄 Pages: " . count( $pages ) . "\n";
foreach ( $pages as $page ) {
    echo "  - " . $page->post_title . " (ID: " . $page->ID . ")\n";
}

// Check menus
$menus = wp_get_nav_menus();
echo "\n📋 Menus: " . count( $menus ) . "\n";
foreach ( $menus as $menu ) {
    $items = wp_get_nav_menu_items( $menu->term_id );
    echo "  - " . $menu->name . " (ID: " . $menu->term_id . ", Items: " . count( $items ) . ")\n";
    
    // Check if menu is assigned to location
    $locations = get_nav_menu_locations();
    $assigned_to = array();
    foreach ( $locations as $location => $menu_id ) {
        if ( $menu_id == $menu->term_id ) {
            $assigned_to[] = $location;
        }
    }
    if ( ! empty( $assigned_to ) ) {
        echo "    ✅ Assigned to: " . implode( ', ', $assigned_to ) . "\n";
    } else {
        echo "    ⚠️  Not assigned to any location\n";
    }
}

// Check posts
$posts = get_posts( array( 'numberposts' => -1 ) );
echo "\n📝 Posts: " . count( $posts ) . "\n";
foreach ( $posts as $post ) {
    echo "  - " . $post->post_title . "\n";
}

// Check if Elementor data was imported
$elementor_pages = get_posts( array(
    'post_type' => 'page',
    'meta_key' => '_elementor_data',
    'numberposts' => -1,
) );
echo "\n🎨 Pages with Elementor data: " . count( $elementor_pages ) . "\n";
foreach ( $elementor_pages as $page ) {
    $data = get_post_meta( $page->ID, '_elementor_data', true );
    $sections = json_decode( $data, true );
    $section_count = is_array( $sections ) ? count( $sections ) : 0;
    echo "  - " . $page->post_title . " (" . $section_count . " sections)\n";
}