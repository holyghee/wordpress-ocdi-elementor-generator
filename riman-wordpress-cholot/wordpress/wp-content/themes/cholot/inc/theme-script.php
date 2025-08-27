<?php
//load all theme jquery script
function cholot_theme_scripts() {
		wp_enqueue_script( 'modernizr', get_template_directory_uri() . '/js/modernizr.js',array('jquery'), false, '', false);
		wp_enqueue_script( 'boostrap', get_template_directory_uri() . '/js/bootstrap.min.js',array(),'', 'in_footer');
		wp_enqueue_script( 'jquery-superfish', get_template_directory_uri() . '/js/superfish.js',array(),'', 'in_footer');
		wp_enqueue_script( 'jquery-fitvids', get_template_directory_uri() . '/js/jquery.fitvids.js',array(),'', 'in_footer');
		wp_enqueue_script( 'jquery-popup', get_template_directory_uri() . '/js/jquery.magnific-popup.min.js',array(),'', 'in_footer');
		wp_enqueue_script( 'jquery-sticky', get_template_directory_uri() . '/js/jquery.sticky.js',array(),'', 'in_footer');
		wp_enqueue_script( 'imagesloaded'); 	
		wp_enqueue_script( 'jquery-slick', get_template_directory_uri() . '/js/slick.min.js',array(),'', 'in_footer');
		wp_enqueue_script( 'jquery-slicknav', get_template_directory_uri() . '/js/jquery.slicknav.js',array(),'', 'in_footer');
		wp_enqueue_script( 'cholot-animation', get_template_directory_uri() . '/js/slick-animation.js',array(),'', 'in_footer');
		wp_enqueue_script( 'cholot-totop', get_template_directory_uri() . '/js/totop.js',array(),'', 'in_footer');
		wp_enqueue_script( 'cholot-scripts', get_template_directory_uri() . '/js/script.js',array(),'', 'in_footer');
}    




