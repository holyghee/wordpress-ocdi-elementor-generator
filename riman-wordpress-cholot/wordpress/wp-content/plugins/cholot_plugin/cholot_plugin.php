<?php

/**
 * Plugin Name: Cholot WordPress Theme Plugin Bundle
 * Plugin URI: http://themeforest.net/user/ridianur
 * Description: This is plugin bundle for Cholot WordPress Theme.
 * Author: ridianur
 * Author URI: http://themeforest.net/user/ridianur
 * Version: 1.1
 */

define('CHOLOT__FILE__', __FILE__);
define('CHOLOT_URL', plugins_url('/', CHOLOT__FILE__));

function cholot_plugin_load()
{
    // Load localization file
    load_plugin_textdomain('cholot_plugin');
    // Require the main elementor widget plugin file
    require __DIR__ . '/plugin.php';

    //only include the files if kirki plugin is installed & activated
    if (class_exists('Kirki')) {
        include 'inc/customizer.php';
        include 'inc/preloader.php';
        include 'inc/output-css.php';
    }

    //only include the files if cmb2 plugin is installed & activated
    if (defined('CMB2_LOADED')) {
        //post metabox
        include 'inc/post-metabox.php';
        //page metabox
        include 'inc/metabox.php';
        //header metabox
        include 'inc/header-metabox.php';
        //footer metabox
        include 'inc/footer-metabox.php';
    }
}
add_action('plugins_loaded', 'cholot_plugin_load');


//plugin translation
function rdn_cholot_plugin_translation()
{
    load_plugin_textdomain('cholot_plugin', false, dirname(plugin_basename(__FILE__)) . '/lang/');
} // end custom_theme_setup
add_action('after_setup_theme', 'rdn_cholot_plugin_translation');

function cholot_plugin_fail_load_out_of_date()
{
    if (!current_user_can('update_plugins')) {
        return;
    }

    $file_path = 'elementor/elementor.php';

    $upgrade_link = wp_nonce_url(self_admin_url('update.php?action=upgrade-plugin&plugin=') . $file_path, 'upgrade-plugin_' . $file_path);
    $message = '<p>' . __('Cholot Plugin is not working because you are using an old version of Elementor.', 'cholot_plugin') . '</p>';
    $message .= '<p>' . sprintf('<a href="%s" class="button-primary">%s</a>', $upgrade_link, __('Update Elementor Now', 'cholot_plugin')) . '</p>';

    echo '<div class="error">' . $message . '</div>';
}

//include function to removing default customizer
include 'inc/removing.php';


//include breadcrumb
include 'inc/breadcrumb.php';

//CUSTOM POST TYPE
//include  custom post type (header)
include 'inc/header.php';
//include  custom post type (footer)
include 'inc/footer.php';

//include elementor addon
include 'inc/elementor-addon.php';



//custom widget
//include about us widget
include 'inc/about-us.php';
//flickrfeed widget & shortcode
include 'inc/flickr-feed.php';
include 'inc/flickr-widget.php';

//included sharing
include 'inc/sharebox.php';

//included one click importer
include 'inc/one-click.php';