<?php

//oneclick importer
function ocdi_import_files()
{
	return array(
		array(
			'import_file_name'           => 'All Demo Content',
			'import_file_url'            => plugins_url('/demo-data/cholot.xml', __FILE__),
			'import_widget_file_url'     => plugins_url('/demo-data/cholot.wie', __FILE__),
			'import_preview_image_url'   => plugins_url('/demo-data/cholot.jpg', __FILE__),
			'import_customizer_file_url' => plugins_url('/demo-data/cholot.dat', __FILE__),
			'import_notice'                => __('<p>To prevent any error, please use the clean wordpress site to import the demo data. </p><p>Or you can use this plugin 
			<a href="https://wordpress.org/plugins/wordpress-database-reset/" target="_blank">WordPress Database Reset</a> to reset/clear the database first.</p><p>After you import this demo, you will have to setup the elementor page builder & flickr settings separately.</p>', 'cholot_plugin'),
			'preview_url'                => 'https://theme.winnertheme.com/cholot',
		),
		array(
			'import_file_name'           => 'Library/Page Template Only',
			'import_file_url'            => '',
			'import_preview_image_url'   => plugins_url('/demo-data/library.jpg', __FILE__),
			'preview_url'                => 'https://theme.winnertheme.com/cholot',
		),
	);
}
add_filter('pt-ocdi/import_files', 'ocdi_import_files');


add_filter('pt-ocdi/disable_pt_branding', '__return_true');


function ocdi_after_import($selected_import)
{

	// Assign menus to their locations.
	$multi_page = get_term_by('name', 'Default Menu', 'nav_menu');
	set_theme_mod(
		'nav_menu_locations',
		array(
			'ridianur-homepage-menu' => $multi_page->term_id,
		)
	);

	if ('All Demo Content' === $selected_import['import_file_name']) {


		// Assign front page and posts page (blog page).
		$front_page_id = get_page_by_title('Home');

		update_option('show_on_front', 'page');
		update_option('page_on_front', $front_page_id->ID);
	}

	//import elementor library
	if ('Library/Page Template Only' === $selected_import['import_file_name']) {
		$files = ['1', '2', '3', '4', '5', '6', '7'];

		foreach ($files as $file) {
			$path = plugins_url('demo-data/json/' . $file . '.json', __FILE__);
			$fileContent = file_get_contents($path);
			\Elementor\Plugin::instance()->templates_manager->import_template(
				[
					'fileData' => base64_encode($fileContent),
					'fileName' => 'cholots.json',
				]
			);
		}
	}
}
add_action('pt-ocdi/after_import', 'ocdi_after_import');