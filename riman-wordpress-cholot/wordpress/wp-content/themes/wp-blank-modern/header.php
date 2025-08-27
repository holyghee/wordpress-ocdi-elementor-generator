<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header" id="masthead">
    <div class="header-container">
        <div class="site-branding">
            <?php if (has_custom_logo()) : ?>
                <?php the_custom_logo(); ?>
            <?php else : ?>
                <?php if (is_front_page() && is_home()) : ?>
                    <h1 class="site-title"><a href="<?php echo esc_url(home_url('/')); ?>" rel="home"><?php bloginfo('name'); ?></a></h1>
                <?php else : ?>
                    <p class="site-title"><a href="<?php echo esc_url(home_url('/')); ?>" rel="home"><?php bloginfo('name'); ?></a></p>
                <?php endif; ?>
                <?php
                $description = get_bloginfo('description', 'display');
                if ($description || is_customize_preview()) :
                    ?>
                    <p class="site-description"><?php echo $description; ?></p>
                <?php endif; ?>
            <?php endif; ?>
        </div>

        <nav id="site-navigation" class="main-navigation">
            <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">☰</button>
            <?php
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'menu_id'        => 'primary-menu',
                'fallback_cb'    => 'wp_blank_modern_fallback_menu', // Definiert in functions.php
            ));
            ?>
        </nav>
    </div>
</header>
