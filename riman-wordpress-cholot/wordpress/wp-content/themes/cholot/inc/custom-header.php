<?php

//function custom header by global settings
function cholot_custom_header_global()
{

    global $post;
    $header_id = get_theme_mod('cholot_select_header');

    $cholot_header = new WP_Query(array(
        'posts_per_page' => -1,
        'post_type' => 'header',
        'p' => $header_id,
    ));

    if ($cholot_header->have_posts()) : while ($cholot_header->have_posts()) : $cholot_header->the_post(); ?>

            <nav class="cholot-custom-header clearfix <?php echo esc_attr(get_post_meta(get_the_ID(), 'cholot_header_position', true)) ?>">

                <?php the_content(); ?>
            </nav>

        <?php endwhile;
    endif;
    wp_reset_postdata();
}

//function custom header by page settings
function cholot_custom_header_page()
{
    global $post;
    $header_id = get_post_meta(get_the_ID(), 'cholot_meta_choose_header', true);

    $cholot_header = new WP_Query(array(
        'posts_per_page' => 1,
        'post_type' => 'header',
        'p' => $header_id,
    ));

    if ($cholot_header->have_posts()) : while ($cholot_header->have_posts()) : $cholot_header->the_post(); ?>

            <nav class="cholot-custom-header clearfix <?php echo esc_attr(get_post_meta($post->ID, 'cholot_header_position', true)) ?>">
                <?php the_content(); ?>
            </nav>

        <?php endwhile;
    endif;
    wp_reset_postdata();
}

//function for output custom header
function cholot_header_start()
{
    if (is_singular()) { //if single page/post
        global $post;
        if (get_post_meta($post->ID, 'cholot_header_option', true) == 'custom' && get_post_meta($post->ID, 'cholot_meta_choose_header', true)) {

            //if page setting choose header custom
            do_action('cholot-header-page', 'cholot_custom_header_page');
        }

        //if page setting choose header global
        else if (get_post_meta($post->ID, 'cholot_header_option', true) == 'global') {

            //if custom header & list are selected in theme options
            if (get_theme_mod('custom_header_setting_value') == 'custom' && get_theme_mod('cholot_select_header') != '') {

                do_action('cholot-header-global', 'cholot_custom_header_global');
            } else {
                get_template_part('loop/menu', 'normal');
            }
        }

        //if page setting choose no header
        else if (get_post_meta($post->ID, 'cholot_header_option', true) == 'none') {
            //display nothing
        }

        //if page setting choose header standard
        else { ?>

            <!--HEADER START-->
            <?php get_template_part('loop/menu'); ?>
            <!--HEADER END-->

        <?php }
    } else { //if not single page/post

        //if custom header & list are selected in theme options
        if (get_theme_mod('custom_header_setting_value') == 'custom' && get_theme_mod('cholot_select_header') != '') {

            do_action('cholot-header-global', 'cholot_custom_header_global');
        } else { //if not use normal menu
            get_template_part('loop/menu', 'normal');
        }
    }
} ?>