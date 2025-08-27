<!DOCTYPE html>
<html <?php language_attributes(); ?>>

<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <link rel="profile" href="//gmpg.org/xfn/11" />
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>


    <!--preloader function-->
    <?php if (class_exists('Kirki')) : if (get_theme_mod('cholot_preloader_show')) :
            $cholot_preload =  get_theme_mod('cholot_preloader_show');
            if ($cholot_preload == 'home') {  ?>

    <?php if (is_front_page()) { ?>
    <!-- Preloader -->
    <div id="preloader">
        <div id="status">
            <div class="sk-folding-cube">
                <div class="sk-cube1 sk-cube"></div>
                <div class="sk-cube2 sk-cube"></div>
                <div class="sk-cube4 sk-cube"></div>
                <div class="sk-cube3 sk-cube"></div>
            </div>
        </div>
        <!--status-->
    </div>
    <!--/preloader-->

    <?php }
            } else if ($cholot_preload == 'all') { ?>

    <!-- Preloader -->
    <div id="preloader">
        <div id="status">
            <div class="sk-folding-cube">
                <div class="sk-cube1 sk-cube"></div>
                <div class="sk-cube2 sk-cube"></div>
                <div class="sk-cube4 sk-cube"></div>
                <div class="sk-cube3 sk-cube"></div>
            </div>
        </div>
        <!--status-->
    </div>
    <!--/preloader-->

    <?php  }
        endif;
    endif; ?>