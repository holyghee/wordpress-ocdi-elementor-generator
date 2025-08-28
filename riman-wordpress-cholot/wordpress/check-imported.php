<?php
define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

global $wpdb;

echo "🔍 Checking all posts in database\n";
echo "==================================\n\n";

// Get all posts directly from database
$posts = $wpdb->get_results( "
    SELECT ID, post_title, post_type, post_status, post_parent 
    FROM {$wpdb->posts} 
    WHERE post_status NOT IN ('auto-draft', 'trash')
    ORDER BY post_type, ID
" );

// Group by post type
$grouped = [];
foreach ( $posts as $post ) {
    if ( ! isset( $grouped[$post->post_type] ) ) {
        $grouped[$post->post_type] = [];
    }
    $grouped[$post->post_type][] = $post;
}

foreach ( $grouped as $type => $type_posts ) {
    echo "\n📄 $type (" . count( $type_posts ) . "):\n";
    echo str_repeat( '-', 30 ) . "\n";
    foreach ( $type_posts as $post ) {
        $parent = $post->post_parent ? " (parent: $post->post_parent)" : "";
        echo "  ID: {$post->ID} | {$post->post_title} | Status: {$post->post_status}{$parent}\n";
        
        // Check for Elementor data if it's a page
        if ( $type === 'page' ) {
            $elementor_data = get_post_meta( $post->ID, '_elementor_data', true );
            if ( $elementor_data ) {
                $data = json_decode( $elementor_data, true );
                $sections = is_array( $data ) ? count( $data ) : 0;
                echo "    ✅ Has Elementor data ($sections sections)\n";
            }
        }
    }
}

// Check menu assignments
echo "\n📋 Menu Assignments:\n";
echo "--------------------\n";
$menus = wp_get_nav_menus();
foreach ( $menus as $menu ) {
    $items = wp_get_nav_menu_items( $menu->term_id );
    echo "\n$menu->name (ID: $menu->term_id):\n";
    foreach ( $items as $item ) {
        $object_id = get_post_meta( $item->ID, '_menu_item_object_id', true );
        $type = get_post_meta( $item->ID, '_menu_item_type', true );
        $object = get_post_meta( $item->ID, '_menu_item_object', true );
        echo "  - $item->title | Object: $object (ID: $object_id) | Type: $type\n";
    }
}