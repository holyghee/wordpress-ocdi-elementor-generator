<?php

add_action('after_setup_theme', 'cholot_theme_setup');
function cholot_theme_setup()
{
	/* Add filters, actions, and theme-supported features. */

	//THEME SUPORT FUNCTION
	//add thumbnail
	add_theme_support('post-thumbnails');
	//custom background
	add_theme_support('custom-background');
	add_theme_support('title-tag');

	//automatic feed
	add_theme_support('automatic-feed-links');
	//add menu homepage,portfolio and blog
	add_action('init', 'cholot_register_menu');
	// Retrieve the directory for the localization files
	$lang_dir = (get_template_directory() . '/lang');

	// Set the theme's text domain using the unique identifier from above
	load_theme_textdomain('cholot', $lang_dir);

	//width content
	if (!isset($content_width)) $content_width = 1170;

	//theme default script and styles
	add_action('wp_enqueue_scripts', 'cholot_theme_scripts');
	add_action('wp_enqueue_scripts', 'cholot_theme_styles');

	//register sidebar
	add_action('widgets_init', 'cholot_sidebar');

	//add pingback
	add_action('wp_head', 'cholot_pingback_header');




	//CUSTOM FILTER
	//custom search setting
	add_filter('get_search_form', 'cholot_search_form');
	//custom excerpt
	add_filter('excerpt_length', 'cholot_excerpt_length', 10);
	//remove [..] in excerpt
	add_filter('get_the_excerpt', 'cholot_trim_excerpt');
	//custom comment styles
	add_filter('comment_form_default_fields', 'cholot_modify_comment_form_fields');
	add_filter('comment_form_fields', 'cholot_move_comment_field');
	add_filter('comment_form_field_comment', 'cholot_comment_custom_textarea');


	//tag cloud filter
	add_filter('wp_generate_tag_cloud', 'cholot_tag_cloud', 10, 1);


	//Add "title=" to previous_post_link and next_post_link

	add_filter('next_post_link', function ($link) {
		$next_post = get_next_post();
		$link = str_replace('href=', 'title="' . esc_attr($next_post->post_title) . '" href=', $link);
		return $link;
	});

	add_filter('previous_post_link', function ($link) {
		$previous_post = get_previous_post();
		$link = str_replace('href=', 'title="' . esc_attr($previous_post->post_title) . '" href=', $link);
		return $link;
	});




	//add image size
	add_image_size('cholot-related-post', 500, 300, array('center', 'center'));



	//comment reply
	add_action('wp_enqueue_scripts', 'cholot_enqueue_comments_reply');

	//custom header
	add_action('cholot-custom-header', 'cholot_header_start');
	add_action('cholot-header-page', 'cholot_custom_header_page');
	add_action('cholot-header-global', 'cholot_custom_header_global');

	//custom footer
	add_action('cholot-custom-footer', 'cholot_footer_start');
}



//tag cloud filter
function cholot_tag_cloud($input)
{
	return preg_replace('/ style=("|\')(.*?)("|\')/', '', $input);
}

//add menu for all page
function cholot_register_menu()
{
	register_nav_menu('ridianur-homepage-menu', esc_html__('Menu that display in All page', 'cholot'));
}

//custom excerpt function
function cholot_excerpt_length($length)
{
	return 60;
}
// Remove [...]
function cholot_trim_excerpt($text)
{
	$text = str_replace('[', '', $text);
	$text = str_replace(']', '', $text);
	return $text;
}
//adding sidebar widget
function cholot_sidebar()
{
	register_sidebar(array(
		'name' => esc_html__('Default Sidebar', 'cholot'),
		'id' => 'default-sidebar',
		'description' => esc_html__('Appears as the sidebar on blog and pages', 'cholot'),
		'before_widget' => '<div  id="%1$s" class="widget %2$s clearfix">', 'after_widget' => '</div>',
		'before_title' => '<h3 class="widgettitle">',
		'after_title' => '</h3> <div class="widget-border"></div>',
	));
}


/* Replacing the default WordPress search form with an HTML5 version */
function cholot_search_form($form)
{
	$form = '<form role="search" method="get" class="searchform" action="' . home_url('/') . '" > 
		<input type="search" placeholder="' . esc_attr__('Search and hit enter...', 'cholot') . '" value="' . get_search_query() . '" name="s" class="search-input-form" />
		<input type="submit" class="searchsubmit" />
		</form>';
	return $form;
}
//custom comment form
function cholot_modify_comment_form_fields($fields)
{
	$req = get_option('require_name_email');
	$commenter = wp_get_current_commenter();
	$aria_req = ($req ? " aria-required='true'" : '');

	$fields['author'] = '<p class="cholot-form-field comment-form-author">' . '<label class="cholot-label" for="author">' . esc_html__('Name', 'cholot') . '</label> ' . ($req ? '' : '') .

		'<input id="author" name="author" type="text" placeholder="' . esc_attr__('Your Name ...', 'cholot') . '" value="' .

		esc_attr($commenter['comment_author']) . '" size="30"' . $aria_req . ' /></p>';

	$fields['email'] = '<p class="cholot-form-field  comment-form-email"><label class="cholot-label" for="email">' . esc_html__('Email', 'cholot') . '</label> ' . ($req ? '' : '') .

		'<input id="email" name="email" type="text" placeholder="' . esc_attr__('Your Email ...', 'cholot') . '"  value="' .

		esc_attr($commenter['comment_author_email']) . '" size="30"' . $aria_req . ' /></p>';

	unset($fields['url']);

	return $fields;
}
//move the textarea 
function cholot_move_comment_field($fields)
{
	$comment_field = $fields['comment'];
	unset($fields['comment']);
	$fields['comment'] = $comment_field;
	return $fields;
}


//for comment textarea
function cholot_comment_custom_textarea($comment_field)
{

	$comment_field =
		'<p class="comment-form-comment">
			  <label class="cholot-label" for="comment">' . esc_html__("Comment", "cholot") . '</label>
			  <textarea required id="comment" name="comment" placeholder="' . esc_attr__("Enter comment here...", "cholot") . '" cols="45" rows="5" aria-required="true"></textarea>
		  </p>';

	return $comment_field;
}



//comment reply script
function cholot_enqueue_comments_reply()
{
	if (is_single()) {
		wp_enqueue_script("comment-reply");
	}
}

//Add a pingback url auto-discovery header for single posts, pages, or attachments.
function cholot_pingback_header()
{
	if (is_singular() && pings_open()) {
		echo '<link rel="pingback" href="', esc_url(get_bloginfo('pingback_url')), '">';
	}
}

/**
 * Registers an editor stylesheet for the theme.
 */
function cholot_add_editor_styles()
{
	add_editor_style('custom-editor-style.css');
}


//THEME SCRIPTS & STYLES
// include theme-script
include(get_template_directory() . '/inc/theme-style.php');
include(get_template_directory() . '/inc/theme-script.php');

//include comment template
include(get_template_directory() . '/inc/comment-template.php');

//include related post
include(get_template_directory() . '/inc/related-post.php');

//pagination
include(get_template_directory() . '/inc/pagination.php');
//include TGM activation
include(get_template_directory() . '/inc/plugin-install.php');


//include custom header
include(get_template_directory() . '/inc/custom-header.php');

//include custom footer
include(get_template_directory() . '/inc/custom-footer.php');
/* Contact Form White Styles laden */
wp_enqueue_style("contact-form-white", get_template_directory_uri() . "/contact-form-white.css");

