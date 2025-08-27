<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header">
    <div class="header-container">
        <div class="site-logo">
            <a href="<?php echo esc_url(home_url('/')); ?>">
                <span class="company-name">RIMAN GmbH</span>
                <span class="tagline">Rückbaumanagement & Sanierung</span>
            </a>
        </div>
        
        <nav class="main-navigation">
            <?php
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'menu_id' => 'primary-menu',
                'fallback_cb' => 'riman_default_menu'
            ));
            ?>
        </nav>
    </div>
</header>