<?php
add_action('wp_enqueue_scripts', 'cholot_parent_style', 3);
function cholot_parent_style()
{

  // Register the style for the theme
  wp_enqueue_style(
    'bootstrap',
    get_template_directory_uri() . '/css/bootstrap.min.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'fontawesome',
    get_template_directory_uri() . '/css/font-awesome.min.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'magnificpopup',
    get_template_directory_uri() . '/css/magnific-popup.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'preloader',
    get_template_directory_uri() . '/css/preloader.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'animate',
    get_template_directory_uri() . '/css/animate.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'magiccss',
    get_template_directory_uri() . '/css/magic.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'slick',
    get_template_directory_uri() . '/css/slick.css',
    array(),
    '1',
    'all'
  );
  wp_enqueue_style(
    'fatnav',
    get_template_directory_uri() . '/css/jquery.fatNav.css',
    array(),
    '1',
    'all'
  );

  wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
}