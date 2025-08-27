<?php
/**
 * Initialize the Portfolio Post Meta Boxes. 
 */
add_action( 'cmb2_admin_init', 'portfolio_mb' );
function portfolio_mb() {
	
	
	$cholot_portfolio_metabox_cmb2 = new_cmb2_box( array(
		'id'            => 'cholot_portfolio_metabox',
		'title'         => esc_html__( 'Portfolio Settings', 'cholot_plugin' ),
		'object_types'  => array( 'portfolio' ), // Post type
		'priority'      => 'high',
	) );
  
  	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Please Read:', 'cholot_plugin' ),
		'id'            => 'cholot_ptitle_text',
		'desc' => wp_kses_post( 'Recommended size for portfolio <strong>featured images</strong> is <strong>800x582px</strong> or <strong>800x1164px</strong>
		<br> To be able to edit this portfolio with <strong>elementor</strong>, make sure you have checklist the <strong>Portfolio</strong> in <strong>Elementor Settings -> Post Type</strong>. 
		<br>You choose the <strong>Blank Page Builder</strong> template if you want to build this portfolio using only the <strong>elementor</strong> page builder.', 'cholot_plugin' ),
		'type'             => 'title',
	) );
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Portfolio Format', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Choose Portfolio Format Here', 'cholot_plugin' ),
		'id'               => 'port_format',
		'type'             => 'select',
		'default' => 'port_standard',
		'options'          => array(
			'port_standard' => esc_html__( 'Portfolio Gallery at Top', 'cholot_plugin' ),
			'port_two'   => esc_html__( 'Portfolio Gallery at Right', 'cholot_plugin' )
		),
	) );
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Top Content Format', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Choose Portfolio Format Here', 'cholot_plugin' ),
		'id'               => 'top_type',
		'type'             => 'select',
		'default' => 'top_content_slider',
		'options'          => array(
			'top_content_slider' => esc_html__( 'Images Background', 'cholot_plugin' ),
			'top_content_video'   => esc_html__( 'Video Background', 'cholot_plugin' ),
			'top_content_youtube'   => esc_html__( 'Youtube Background', 'cholot_plugin' )
		),
	) );
	
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Youtube ID', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Insert Youtube ID here. e.g EMy5krGcoOU', 'cholot_plugin' ),
		'id'               => 'port_youtube_link',
		'type'             => 'text',
	) );
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Youtube Quality', 'cholot_plugin' ),
		'desc'             => wp_kses_post( 'Insert Youtube video quality here. You can input <b>small, medium, large, hd720, hd1080, highres</b>. Default value is <b>large</b>', 'cholot_plugin' ),
		'id'               => 'port_youtube_quality',
		'type'             => 'text',
	) );
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Video Link', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Insert the video directlink here. eg. https://www.quirksmode.org/html5/videos/big_buck_bunny.mp4', 'cholot_plugin' ),
		'id'               => 'port_video_link',
		'type'             => 'text',
	) );
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Portfolio Top Image', 'cholot_plugin' ),
		'desc'             => wp_kses_post( 'Upload Your Top Image here. <br/>You still need to fill this if you choose the <strong>video/youtube background</strong>. So the image will <strong>replace</strong> the video/youtube background in <strong>touch devices</strong>.', 'cholot_plugin' ),
		'id'      => 'port_slider_setting',
		'type'    => 'file',
		// Optional:
		'options' => array(
			'url' => false, // Hide the text input for the url
			),
		'text'    => array(
			'add_upload_file_text' => 'Add Image' // Change upload button text. Default: "Add or Upload File"
			),
		'query_args' => array(
			'type' => array(
				'image/gif',
				'image/jpeg',
				'image/png',	
				),
		),
		'preview_size' => 'large', // Image size to use when previewing in the admin.
	) );
	
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Portfolio Gallery Images', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Create your gallery here. You can leave it blank if you don\'t want it.', 'cholot_plugin' ),
		'id'   => 'gallery_list',
		'type' => 'file_list',
		'text' => array(
			'add_upload_files_text' => 'Upload images',
		),
		'preview_size' => array( 100, 100 ), // Default: array( 50, 50 )
		'query_args' => array( 'type' => 'image' ), // Only images attachment
	) );
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Portfolio Button Link', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Insert your button link here. Leave it blank if you dont want it.', 'cholot_plugin' ),
		'id'               => 'port_item_btn_link',
		'type'             => 'text',
	) );
	
	
	$cholot_portfolio_metabox_cmb2->add_field( array(
		'name'             => esc_html__( 'Portfolio Button Text', 'cholot_plugin' ),
		'desc'             => esc_html__( 'Insert your button text here. Leave it blank if you dont want it.', 'cholot_plugin' ),
		'id'               => 'port_item_btn_text',
		'type'             => 'text',
	) );
	
	
 

}



