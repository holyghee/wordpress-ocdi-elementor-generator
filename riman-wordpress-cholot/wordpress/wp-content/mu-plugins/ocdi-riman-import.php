<?php
/**
 * One Click Demo Import Configuration for RIMAN Site
 */

// Define demo import files
function riman_ocdi_import_files() {
    return array(
        array(
            'import_file_name'           => 'RIMAN GmbH - Complete Site',
            'categories'                 => array( 'Business', 'Elementor' ),
            'local_import_file'          => ABSPATH . 'riman-xl-site-no-images.xml',
            'import_preview_image_url'   => '',
            'preview_url'                => 'http://localhost:8082',
            'import_notice'              => 'This will import the complete RIMAN GmbH website including pages, posts, and navigation menu.',
        ),
    );
}
add_filter( 'ocdi/import_files', 'riman_ocdi_import_files' );

// After import setup
function riman_ocdi_after_import_setup() {
    // Assign front page and posts page (blog page)
    $front_page_id = get_page_by_path( 'startseite' );
    $blog_page_id  = get_page_by_path( 'blog' );

    if ( $front_page_id ) {
        update_option( 'show_on_front', 'page' );
        update_option( 'page_on_front', $front_page_id->ID );
    }

    if ( $blog_page_id ) {
        update_option( 'page_for_posts', $blog_page_id->ID );
    }

    // Assign menu to location
    $main_menu = get_term_by( 'slug', 'default-menu', 'nav_menu' );
    
    if ( $main_menu ) {
        $locations = get_theme_mod( 'nav_menu_locations' );
        
        // Try different common menu location names
        $possible_locations = array( 'primary', 'main', 'main-menu', 'header', 'top' );
        
        foreach ( $possible_locations as $location ) {
            if ( array_key_exists( $location, $locations ) ) {
                $locations[ $location ] = $main_menu->term_id;
                set_theme_mod( 'nav_menu_locations', $locations );
                break;
            }
        }
        
        // If no location found, just set to primary
        if ( ! in_array( $main_menu->term_id, $locations ) ) {
            $locations['primary'] = $main_menu->term_id;
            set_theme_mod( 'nav_menu_locations', $locations );
        }
    }

    // Flush rewrite rules
    flush_rewrite_rules();
}
add_action( 'ocdi/after_import', 'riman_ocdi_after_import_setup' );

// Disable generation of default content
add_filter( 'ocdi/plugin_page_setup', 'riman_ocdi_plugin_page_setup' );
function riman_ocdi_plugin_page_setup( $default_settings ) {
    $default_settings['parent_slug'] = 'themes.php';
    $default_settings['page_title']  = esc_html__( 'RIMAN Demo Import' , 'one-click-demo-import' );
    $default_settings['menu_title']  = esc_html__( 'Import RIMAN Demo' , 'one-click-demo-import' );
    $default_settings['capability']  = 'import';
    $default_settings['menu_slug']   = 'riman-demo-import';

    return $default_settings;
}

// Time limit
add_filter( 'ocdi/time_for_one_ajax_call', 'riman_ocdi_change_time_of_single_ajax_call' );
function riman_ocdi_change_time_of_single_ajax_call() {
    return 30; // 30 seconds
}

// Disable the ProteusThemes branding notice
add_filter( 'ocdi/disable_pt_branding', '__return_true' );