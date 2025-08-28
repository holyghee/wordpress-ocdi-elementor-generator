<?php
define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Check registered menu locations
$locations = get_registered_nav_menus();

echo "📍 Registered Menu Locations:\n";
if ( empty( $locations ) ) {
    echo "  ❌ No menu locations registered by the theme!\n";
} else {
    foreach ( $locations as $location => $description ) {
        echo "  - $location: $description\n";
    }
}

echo "\n📋 Current Menu Assignments:\n";
$menu_locations = get_nav_menu_locations();
if ( empty( $menu_locations ) ) {
    echo "  No menus assigned to locations\n";
} else {
    foreach ( $menu_locations as $location => $menu_id ) {
        $menu = wp_get_nav_menu_object( $menu_id );
        $menu_name = $menu ? $menu->name : 'Unknown';
        echo "  - $location => $menu_name (ID: $menu_id)\n";
    }
}

echo "\n🎨 Active Theme: " . get_option('stylesheet') . "\n";