<?php
//preloader custom setting
function cholot_preloader_set()
{

	$pr_color =  get_theme_mod('cholot_bg_preloader');
	$loader_bg = "
		#preloader{background-color: $pr_color;}";
	if ($pr_color != '') {
		wp_add_inline_style('cholot-styles', $loader_bg);
	}
}
//CSS ouput script
add_action('wp_enqueue_scripts', 'cholot_preloader_set', 11);

function cholot_preloader()
{
	if (get_theme_mod('cholot_preloader_show') == 'home' ||  get_theme_mod('cholot_preloader_show') == 'all') {
		wp_enqueue_script('preloader', plugin_dir_url(__FILE__) . 'js/loader.js', array('jquery'), '1.0.0', false);
	}
}

//CSS ouput script
add_action('wp_enqueue_scripts', 'cholot_preloader');