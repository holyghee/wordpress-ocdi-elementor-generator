<?php
// Registers the new post type 

function cholot_footer_post_type() {
	register_post_type( 'footer',
		array(
			'labels' => array(
				'name' => __( 'Custom Footer', 'cholot_plugin' ),
				'singular_name' => __( 'Custom Footer' , 'cholot_plugin'),
				'add_new' => __( 'Add New Custom Footer', 'cholot_plugin' ),
				'add_new_item' => __( 'Add New Custom Footer', 'cholot_plugin' ),
				'edit_item' => __( 'Edit Custom Footer', 'cholot_plugin' ),
				'new_item' => __( 'Add New Custom Footer', 'cholot_plugin' ),
				'view_item' => __( 'View Custom Footer', 'cholot_plugin' ),
				'search_items' => __( 'Search Custom Footer', 'cholot_plugin' ),
				'not_found' => __( 'No Custom Footer found', 'cholot_plugin' ),
				'not_found_in_trash' => __( 'No Custom Footer found in trash', 'cholot_plugin' )
			),
			'public' => true,
			'supports' => array( 'title'),
			'capability_type' => 'post',
			'rewrite' => array("slug" => "footer"), // Permalinks format
			'menu_position' => 5,
			'menu_icon'           => 'dashicons-art',
			'exclude_from_search' => true 
		)
	);

}

add_action( 'init', 'cholot_footer_post_type' );


