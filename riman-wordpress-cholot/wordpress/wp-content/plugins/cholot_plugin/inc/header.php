<?php
// Registers the new post type 

function cholot_header_post_type() {
	register_post_type( 'header',
		array(
			'labels' => array(
				'name' => __( 'Custom Header', 'cholot_plugin' ),
				'singular_name' => __( 'Custom Header' , 'cholot_plugin'),
				'add_new' => __( 'Add New Custom Header', 'cholot_plugin' ),
				'add_new_item' => __( 'Add New Custom Header', 'cholot_plugin' ),
				'edit_item' => __( 'Edit Custom Header', 'cholot_plugin' ),
				'new_item' => __( 'Add New Custom Header', 'cholot_plugin' ),
				'view_item' => __( 'View Custom Header', 'cholot_plugin' ),
				'search_items' => __( 'Search Custom Header', 'cholot_plugin' ),
				'not_found' => __( 'No Custom Header found', 'cholot_plugin' ),
				'not_found_in_trash' => __( 'No Custom Header found in trash', 'cholot_plugin' )
			),
			'public' => true,
			'supports' => array( 'title'),
			'capability_type' => 'post',
			'rewrite' => array("slug" => "header"), // Permalinks format
			'menu_position' => 5,
			'menu_icon'           => 'dashicons-menu',
			'exclude_from_search' => true 
		)
	);

}

add_action( 'init', 'cholot_header_post_type' );


//add background in elementor editor
add_filter( 'body_class','my_body_classes' );

function my_body_classes( $classes ) {
 	if ( is_singular('header') ) {
	global $post;
    $classes[] = get_post_meta($post->ID, 'cholot_dark_bg', true);  
    }  
    return $classes;

}

