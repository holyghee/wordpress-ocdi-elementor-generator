<?php 



//CMB2 metabox
add_action( 'cmb2_admin_init', 'cholot_register_footer_metabox' );
function cholot_register_footer_metabox() {
	

	/**
	 * Title & text metabox
	 */
	$cholot_footer_metabox_cmb2 = new_cmb2_box( array(
		'id'            => 'cholot_footer_metabox',
		'title'         => esc_html__( 'Notice', 'cholot_plugin' ),
		'object_types'  => array( 'footer' ), // Post type
	) );

	$cholot_footer_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Please Read:', 'cholot_plugin' ),
		'id'            => 'cholot_footer_title_text',
		'desc' => wp_kses_post( 'You can build your custom footer with <strong>elementor</strong> and use it in any page using the <strong>page settings</strong>.<br> For <strong>global settings</strong>, you can set it on <strong>the customizer -> Footer Settings</strong>. <br>
		To be able to edit this footer with <strong>elementor</strong>, make sure you have checklist the <strong>Custom Footer</strong> in <strong>Elementor Settings -> Post Type</strong>', 'cholot_plugin' ),
		'type'             => 'title',
	) );
	
	
}








