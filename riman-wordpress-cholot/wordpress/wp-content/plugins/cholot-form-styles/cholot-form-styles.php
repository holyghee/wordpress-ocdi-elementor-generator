<?php
/**
 * Plugin Name: Cholot Form Styles
 * Description: Custom styling for Contact Form 7 to match Cholot theme
 * Version: 1.0
 * Author: RIMAN GmbH
 */

function cholot_form_enqueue_styles() {
    wp_enqueue_style(
        'cholot-contact-form-styles',
        plugin_dir_url(__FILE__) . 'cholot-contact-form-styles.css',
        array(),
        '1.0.0'
    );
}
add_action('wp_enqueue_scripts', 'cholot_form_enqueue_styles');