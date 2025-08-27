<?php

//removing the default customizer section & panel
add_action( "customize_register", "cholot_remove_default_customizer" ,999,1);    

function cholot_remove_default_customizer( $wp_customize) {
 
 //=============================================================
 // Remove header image and widgets option from theme customizer
 //=============================================================
 $wp_customize->remove_control("header_image");

 //=============================================================
 // Remove Colors, Background image, and Static front page 
 // option from theme customizer     
 //=============================================================
 $wp_customize->remove_section("colors");
 $wp_customize->remove_section("background_image");
}


/**
 * Removes the core 'Menus' panel from the Customizer.
 *
 * @param array $components Core Customizer components list.
 * @return array (Maybe) modified components list.
 */
function cholot_remove_nav_menus_panel( $components ) {
    $i = array_search( 'nav_menus', $components );
    if ( false !== $i ) {
        unset( $components[ $i ] );
    }
    return $components;
}
add_filter( 'customize_loaded_components', 'cholot_remove_nav_menus_panel' );
