<?php 



//CMB2 metabox
add_action( 'cmb2_admin_init', 'cholot_register_postsetting_metabox' );
function cholot_register_postsetting_metabox() {
	

	/**
	 * Custom Header Metabox
	 */
	$cholot_post_metabox_cmb2 = new_cmb2_box( array(
		'id'            => 'cholot_header_title_metabox',
		'title'         => esc_html__( 'Header Settings', 'cholot_plugin' ),
		'object_types'  => array( 'post','page','portfolio' ), // Post type
	) );

	
	$cholot_post_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Header Options', 'cholot_plugin' ),
		'id'               => 'cholot_header_option',
		'type'             => 'select',
		'default' => 'global',
		'options'          => array(
			'global' => esc_html__( 'Use Global Setting (from Customizer).', 'cholot_plugin' ),
			'default'   => esc_html__( 'Use Default Header', 'cholot_plugin' ),
			'custom'   => esc_html__( 'Use Custom Header', 'cholot_plugin' ),
			'none'     => esc_html__( 'No Header', 'cholot_plugin' ),
		),
	) );
	
	$cholot_post_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Header Format', 'cholot_plugin' ),
		'id'               => 'cholot_default_header',
		'type'             => 'select',
		'default' => 'head_clean',
		'options'          => array(
			'head_clean' => esc_html__( 'Black Text with White Background Header in Relative Position', 'cholot_plugin' ),
			'head_standard'   => esc_html__( 'White Text with Transparent Background Header in Absolute Position', 'cholot_plugin' ),
		),
	) );
	
	$cholot_post_metabox_cmb2->add_field( array(

		'name' => 'Choose Custom Header',
		'desc' => 'The Custom Header only appear on the actual page, not in elementor editor.',
		'id' => 'cholot_meta_choose_header',
		'type' => 'select',
		'options' =>choose_header(),
	) );
	
	/**
	 * Custom Footer Metabox
	 */
	$cholot_post_metabox_cmb2 = new_cmb2_box( array(
		'id'            => 'cholot_footer_title_metabox',
		'title'         => esc_html__( 'Footer Settings', 'cholot_plugin' ),
		'object_types'  => array( 'post','page','portfolio' ), // Post type
	) );

	
	$cholot_post_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Footer Options', 'cholot_plugin' ),
		'id'               => 'cholot_footer_option',
		'type'             => 'select',
		'default' => 'global',
		'options'          => array(
			'global' => esc_html__( 'Use Global Setting (from Customizer).', 'cholot_plugin' ),
			'default'   => esc_html__( 'Use Default Footer', 'cholot_plugin' ),
			'custom'   => esc_html__( 'Use Custom Footer', 'cholot_plugin' ),
			'none'     => esc_html__( 'No Footer', 'cholot_plugin' ),
		),
	) );
	
	
	$cholot_post_metabox_cmb2->add_field( array(

		'name' => 'Choose Custom Footer',
		'desc' => 'The Custom Footer only appear on the actual page, not in elementor editor.',
		'id' => 'cholot_meta_choose_footer',
		'type' => 'select',
		'options' =>choose_footer(),
	) );
	

	
	
}//function end

//display header  list
function choose_header() {
    $header_posts = get_posts(['post_type' => 'header'] );
	$header = array();
	$i     = 0;
	foreach ( $header_posts as $header_post ) {
		if ( $i == 0 ) {
			$header_title = $header_post->post_title ;
			$i ++;
		}
		$header[ $header_post->ID ] = $header_post->post_title;
	}
	return $header;
}

//display footer  list
function choose_footer() {
    $footer_posts = get_posts(['post_type' => 'footer'] );
	$footer = array();
	$i     = 0;
	foreach ( $footer_posts as $footer_post ) {
		if ( $i == 0 ) {
			$footer_title = $footer_post->post_title ;
			$i ++;
		}
		$footer[ $footer_post->ID ] = $footer_post->post_title;
	}
	return $footer;
}



function cholot_metabox_scripts() {


// Registering and adding custom admin css
wp_enqueue_style( 'cholot_plugin_css', CHOLOT_URL  . 'inc/css/plugin-style.css', false, '1.0.0' );

// Adding custom admin scripts file
wp_enqueue_script( 'cholot_plugin_custom_script', CHOLOT_URL  . 'inc/js/plugin-script.js');
}

add_action( 'admin_enqueue_scripts', 'cholot_metabox_scripts' );


