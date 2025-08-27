<?php
/**
 * Initialize the Post Post Meta Boxes. 
 */
add_action('cmb2_admin_init', 'cholot_post_mb');
function cholot_post_mb()
{

	$cholot_post_metabox_cmb2 = new_cmb2_box(array(
		'id'            => 'cholot_post_metabox',
		'title'         => esc_html__('Post Settings', 'cholot_plugin'),
		'object_types'  => array('post'), // Post type
		'priority'      => 'high',
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Please Read:', 'cholot_plugin'),
		'id'            => 'cholot_post_title_text',
		'desc' => wp_kses_post('Always use the same ratio/size for images in slider/gallery below.
		<br> To be able to edit this post with <strong>elementor</strong>, make sure you have checklist the <strong>Posts</strong> in <strong>Elementor Settings -> Post Type</strong>.', 'cholot_plugin'),
		'type'             => 'title',
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Post Format', 'cholot_plugin'),
		'desc'             => esc_html__('Choose Post Format Here', 'cholot_plugin'),
		'id'               => 'post_format',
		'type'             => 'select',
		'default' => 'post_standard',
		'options'          => array(
			'post_standard' => esc_html__('Post Standard', 'cholot_plugin'),
			'post_gallery'   => esc_html__('Post Gallery', 'cholot_plugin'),
			'post_slider'   => esc_html__('Post Slider', 'cholot_plugin'),
			'post_video'   => esc_html__('Post Video', 'cholot_plugin'),
			'post_audio'   => esc_html__('Post Audio', 'cholot_plugin'),
		),
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Gallery Setting', 'cholot_plugin'),
		'desc'             => esc_html__('Create your Post Gallery here. Try to use same ratio for each image.', 'cholot_plugin'),
		'id'   => 'post_gallery_setting',
		'type' => 'file_list',
		'text' => array(
			'add_upload_files_text' => 'Upload images',
		),
		'preview_size' => array(100, 100), // Default: array( 50, 50 )
		'query_args' => array('type' => 'image'), // Only images attachment
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Slider Setting', 'cholot_plugin'),
		'desc'             => esc_html__('Create your Post Slider here. Try to use same ratio for each image.', 'cholot_plugin'),
		'id'   => 'post_slider_setting',
		'type' => 'file_list',
		'text' => array(
			'add_upload_files_text' => 'Upload images',
		),
		'preview_size' => array(100, 100), // Default: array( 50, 50 )
		'query_args' => array('type' => 'image'), // Only images attachment
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Video Setting', 'cholot_plugin'),
		'desc'             => wp_kses_post('Insert the link for video embed here.<br/> For video from youtube/vimeo just put the link without any attribute like ?wmode=opaque.<br/>eg: http://www.youtube.com/embed/IzgAYZTuBA8 <br>For <b>vimeo</b> video, you can use the post type audio format.', 'cholot_plugin'),
		'id'               => 'post_video_setting',
		'type'             => 'text',
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Audio Setting', 'cholot_plugin'),
		'desc'             => wp_kses_post('Insert your iframe/embedded code for audio here.<br/>
		You can input iframe/embed code from youtube/vimeo here too, if you don\'t like the default style of Post video.', 'cholot_plugin'),
		'id'               => 'post_audio_setting',
		'type'             => 'textarea',
		'sanitization_cb' => false,
	));

	$cholot_post_metabox_cmb2->add_field(array(
		'name'             => esc_html__('Sidebar Setting', 'cholot_plugin'),
		'desc'             => esc_html__('You can show/hide the sidebar here.', 'cholot_plugin'),
		'id'               => 'post_sidebar',
		'type'             => 'select',
		'default' => 'show',
		'options'          => array(
			'show' => esc_html__('Show Sidebar', 'cholot_plugin'),
			'hide'   => esc_html__('Hide Sidebar', 'cholot_plugin'),
		),
	));
}