<?php 



//CMB2 metabox
add_action( 'cmb2_admin_init', 'cholot_register_header_metabox' );
function cholot_register_header_metabox() {
	

	/**
	 * CUSTOM HEADER SETTINGS
	 */
	$cholot_header_metabox_cmb2 = new_cmb2_box( array(
		'id'            => 'cholot_header_metabox',
		'title'         => esc_html__( 'Header Settings', 'cholot_plugin' ),
		'object_types'  => array( 'header' ), // Post type
	) );

	$cholot_header_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Please Read:', 'cholot_plugin' ),
		'id'            => 'cholot_title_text',
		'desc' => wp_kses_post( 'You can build your custom header with <strong>elementor</strong> and use it in any page using the <strong>page settings</strong>.<br> For <strong>global settings</strong>, you can set it on <strong>the customizer -> Header Settings</strong>. <br>
		To be able to edit this header with <strong>elementor</strong>, make sure you have checklist the <strong>Custom Header</strong> in <strong>Elementor Settings -> Post Type</strong>', 'cholot_plugin' ),
		'type'             => 'title',
	) );
	
	$cholot_header_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Header Position', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Choose the Header Position', 'cholot_plugin' ),
		'id'               => 'cholot_header_position',
		'type'             => 'select',
		'default' => 'default',
		'options'          => array(
			'default' => esc_html__( 'Relative Header', 'cholot_plugin' ),
			'custom-absolute-menu'   => esc_html__( 'Absolute Header', 'cholot_plugin' ),
			'custom-fixed-menu'   => esc_html__( 'Fixed Header', 'cholot_plugin' ),
			'custom-sticky-menu'     => esc_html__( 'Sticky Header', 'cholot_plugin' ),
			'custom-sticky-menu custom-absolute-menu'     => esc_html__( 'Absolute then Sticky(on scroll) Header', 'cholot_plugin' ),
		),
	) );
	
	$cholot_header_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Use Dark Background Page', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Only for preview/editor purpose only. For better preview in header element with white/bright color or with opacity.', 'cholot_plugin' ),
		'id'               => 'cholot_dark_bg',
		'type'             => 'select',
		'default' => 'default',
		'options'          => array(
			'default' => esc_html__( 'Use Default Background', 'cholot_plugin' ),
			'dark-page'   => esc_html__( 'Use Dark Background', 'cholot_plugin' ),
		),
	) );
	
	
}




