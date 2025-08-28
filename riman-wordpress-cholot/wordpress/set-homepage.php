<?php
/**
 * Set Homepage after OCDI Import
 * 
 * Automatische Homepage-Konfiguration nach WordPress Import
 * Teil der CHOLOT TEST SUITE
 * 
 * Usage: php set-homepage.php [page-title]
 * 
 * Author: Claude Code Assistant (OCDI TEST SUITE BUILDER)  
 * Date: 2025-08-28
 */

define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Command line argument for page title
$page_title = $argv[1] ?? 'Home';

echo "🏠 HOMEPAGE SETUP UTILITY\n";
echo "=========================\n";
echo "Target Site: " . get_site_url() . "\n";
echo "Looking for page: '$page_title'\n";
echo "=========================\n\n";

// Find the specified page
$home_page = get_page_by_title( $page_title );

if ( $home_page ) {
    // Set as front page
    $previous_front_page = get_option( 'page_on_front' );
    
    update_option( 'page_on_front', $home_page->ID );
    update_option( 'show_on_front', 'page' );
    
    echo "✅ SUCCESS: Homepage configured\n";
    echo "   Page: " . $home_page->post_title . "\n";
    echo "   ID: " . $home_page->ID . "\n";
    echo "   Status: " . $home_page->post_status . "\n";
    echo "   Previous front page ID: " . ( $previous_front_page ?: 'none' ) . "\n\n";
    
    // Verify the change
    $current_front_page = get_option( 'page_on_front' );
    $show_on_front = get_option( 'show_on_front' );
    
    echo "✅ VERIFICATION:\n";
    echo "   Current front page ID: " . $current_front_page . "\n";
    echo "   Show on front: " . $show_on_front . "\n";
    
    if ( $current_front_page == $home_page->ID && $show_on_front == 'page' ) {
        echo "   Status: ✅ Homepage correctly set\n\n";
        
        // Check if page has Elementor data
        $elementor_data = get_post_meta( $home_page->ID, '_elementor_data', true );
        if ( $elementor_data ) {
            $data = json_decode( $elementor_data, true );
            if ( is_array( $data ) && count( $data ) > 0 ) {
                echo "🎨 ELEMENTOR DATA FOUND:\n";
                echo "   Sections: " . count( $data ) . "\n";
                
                // Count widgets
                $widget_count = 0;
                foreach ( $data as $section ) {
                    if ( isset( $section['elements'] ) ) {
                        foreach ( $section['elements'] as $column ) {
                            if ( isset( $column['elements'] ) ) {
                                $widget_count += count( $column['elements'] );
                            }
                        }
                    }
                }
                echo "   Widgets: " . $widget_count . "\n";
                echo "   Edit Mode: " . get_post_meta( $home_page->ID, '_elementor_edit_mode', true ) . "\n\n";
            } else {
                echo "⚠️  Elementor data exists but appears invalid\n\n";
            }
        } else {
            echo "⚠️  No Elementor data found for homepage\n\n";
        }
        
        echo "🔗 HOMEPAGE URL: " . get_permalink( $home_page->ID ) . "\n";
        echo "🌐 SITE URL: " . home_url() . "\n\n";
        
    } else {
        echo "   Status: ❌ Configuration failed\n\n";
    }
    
} else {
    echo "❌ ERROR: Page '$page_title' not found\n\n";
    
    // Show all available pages
    $pages = get_pages( array(
        'sort_column' => 'menu_order,post_title',
        'post_status' => 'publish'
    ) );
    
    if ( ! empty( $pages ) ) {
        echo "📄 AVAILABLE PAGES:\n";
        echo "===================\n";
        
        foreach ( $pages as $page ) {
            $elementor_indicator = get_post_meta( $page->ID, '_elementor_data', true ) ? ' 🎨' : '';
            echo sprintf( "   %-20s (ID: %d)%s\n", 
                $page->post_title, 
                $page->ID,
                $elementor_indicator
            );
        }
        
        echo "\nUsage: php set-homepage.php \"[Page Title]\"\n";
        echo "Example: php set-homepage.php \"Home\"\n";
        echo "Example: php set-homepage.php \"Welcome\"\n\n";
    } else {
        echo "❌ No published pages found!\n";
        echo "Please import content first or check page status.\n\n";
    }
    
    exit( 1 );
}

// Additional homepage optimizations
echo "🔧 ADDITIONAL OPTIMIZATIONS:\n";
echo "=============================\n";

// Clear any caches
if ( function_exists( 'wp_cache_flush' ) ) {
    wp_cache_flush();
    echo "✅ Object cache cleared\n";
}

// Flush rewrite rules
flush_rewrite_rules();
echo "✅ Permalink structure refreshed\n";

// Update .htaccess if possible
if ( got_mod_rewrite() ) {
    $rules = get_htaccess_file();
    if ( $rules ) {
        echo "✅ .htaccess rules updated\n";
    }
}

echo "\n🎉 HOMEPAGE SETUP COMPLETED!\n";
echo "===========================\n";
echo "Next steps:\n";
echo "1. Visit: " . home_url() . "\n";
echo "2. Check page display and layout\n";
echo "3. Test navigation and menus\n";
echo "4. Verify Elementor functionality\n";
echo "\n";