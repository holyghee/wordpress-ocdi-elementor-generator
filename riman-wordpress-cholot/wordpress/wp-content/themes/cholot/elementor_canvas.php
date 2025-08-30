<?php
/*
Template Name: Elementor Canvas
Template Post Type: page
Description: Elementor Canvas Template - Full width page with no header/footer.
*/

// No header or footer - just the content
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php if (! current_user_can('manage_options')) : ?>
        <meta name="robots" content="noindex, nofollow">
    <?php endif; ?>
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php
while (have_posts()) : the_post();
    // This will render the Elementor content
    the_content();
endwhile;
?>
<?php wp_footer(); ?>
</body>
</html>