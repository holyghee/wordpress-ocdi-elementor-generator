<?php


//display menu list
function navmenu_navbar_menu_choices()
{
	$menus = wp_get_nav_menus();
	$items = array();
	$i     = 0;
	foreach ($menus as $menu) {
		if ($i == 0) {
			$default = $menu->slug;
			$i++;
		}
		$items[$menu->slug] = $menu->name;
	}

	return $items;
}

//display portfolio  list
function choose_portfolio_list()
{
	$port_posts = get_posts(['post_type' => 'portfolio']);
	$port = array();
	$i     = 0;
	foreach ($port_posts as $port_post) {
		if ($i == 0) {
			$port_title = $port_post->post_title;
			$i++;
		}
		$port[$port_post->ID] = $port_post->post_title;
	}
	return $port;
}

//display category blog list
function category_choice()
{
	$categories = get_categories();
	$blogs = array();
	$i     = 0;
	foreach ($categories as $category) {
		if ($i == 0) {
			$default = $category->name;
			$i++;
		}
		$blogs[$category->term_id] = $category->name;
	}
	return $blogs;
}

//display taxnonomy
function tax_choice()
{
	$categories = get_terms('portfolio_category');
	$blogs = array();
	$i     = 0;
	foreach ($categories as $category) {
		if ($i == 0) {
			$default = $category->name;
			$i++;
		}
		$blogs[$category->term_id] = $category->name;
	}
	return $blogs;
}

//for imagesloaded 
add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script('imagesloaded');
});

//for isotope
add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script(
		'jquery-isotope',
		CHOLOT_URL . 'widgets/js/isotope.pkgd.js',
		array('jquery'),
		'1',
		true // in_footer
	);
});

//for slick slider
add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script(
		'jquery-slick',
		CHOLOT_URL . 'widgets/js/slick.min.js',
		array('jquery'),
		'1',
		true // in_footer
	);
});


//for sticky
add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script(
		'jquery-sticky',
		CHOLOT_URL . 'widgets/js/jquery.sticky.js',
		array('jquery'),
		'1',
		true // in_footer
	);
});


//for superfish script
add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script(
		'jquery-superfish',
		CHOLOT_URL . 'widgets/js/superfish.js',
		array('jquery'),
		'1',
		true // in_footer
	);
});

//for fitvids script
add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script(
		'jquery-fitvids',
		CHOLOT_URL . 'widgets/js/jquery.fitvids.js',
		array('jquery'),
		'1',
		true // in_footer
	);
});

add_action('elementor/editor/after_enqueue_scripts', function () {
	wp_enqueue_script(
		'rdn-elementor',
		CHOLOT_URL . 'widgets/js/rdn-elementor.js',
		array('jquery'),
		'1',
		true // in_footer
	);
});

//add new category elementor
add_action('elementor/init', function () {
	$elementsManager = Elementor\Plugin::instance()->elements_manager;
	$elementsManager->add_category(
		'cholot-elements',
		array(
			'title' => 'Cholot General Elements',
			'icon'  => 'font',
		),
		1
	);
});

//add new category elementor
add_action('elementor/init', function () {
	$elementsManager = Elementor\Plugin::instance()->elements_manager;
	$elementsManager->add_category(
		'cholot-menu-elements',
		array(
			'title' => 'Cholot Custom Menu Elements',
			'icon'  => 'font',
		),
		2
	);
});

//add new category elementor
add_action('elementor/init', function () {
	$elementsManager = Elementor\Plugin::instance()->elements_manager;
	$elementsManager->add_category(
		'cholot-portfolio-elements',
		array(
			'title' => 'Cholot Single Portfolio Elements',
			'icon'  => 'font',
		),
		3
	);
});

//add new category elementor
add_action('elementor/init', function () {
	$elementsManager = Elementor\Plugin::instance()->elements_manager;
	$elementsManager->add_category(
		'cholot-blog-elements',
		array(
			'title' => 'Cholot Blog Post Elements',
			'icon'  => 'font',
		),
		4
	);
});




add_action('elementor/element/before_section_end', function ($section, $section_id, $args) {
	if ($section->get_name() == 'google_maps' && $section_id == 'section_map') {
		// we are at the end of the "section_image" area of the "image-box"
		$section->add_control(
			'map_style',
			[
				'label'        => 'Map Style',
				'type'         => Elementor\Controls_Manager::SELECT,
				'default'      => 'default',
				'options'      => array('default' => 'Default', 'gray' => 'Grayscale Map'),
				'prefix_class' => 'map-',
				'label_block'  => true,
			]
		);
	}
}, 10, 3);
