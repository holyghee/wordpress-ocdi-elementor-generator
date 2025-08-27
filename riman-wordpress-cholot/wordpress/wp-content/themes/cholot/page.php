<?php

get_header();


//custom header
if (class_exists('Kirki')) {
    do_action('cholot-custom-header', 'cholot_header_start');
} else { ?>

<!--Fall back if no kirki installed-->
<!--HOME START-->
<div class="default-header clearfix">
    <!--HEADER START-->
    <?php get_template_part('loop/menu', 'normal'); ?>
    <!--HEADER END-->
</div>
<!--/home end-->
<!--HOME END-->

<?php } ?>

<!--breadcrumb if available-->
<?php if (function_exists('cholot_breadcrumb')) { ?>
<div class="box-crumb clearfix">
    <div class="slider-mask"></div>
    <div class="container">
        <?php if (function_exists('cholot_breadcrumb')) {
                cholot_breadcrumb();
            } ?>

        <h1 class="blog-title"><?php the_title(); ?></h1>
        <div class="bread-line"></div>
    </div>

</div>
<?php } ?>

<div class="content blog-wrapper">
    <div class="container-fluid clearfix">
        <div class="row clearfix">
            <div class="blog-content
			<?php if (function_exists('dynamic_sidebar')) {
                if (is_active_sidebar('default-sidebar')) {
                    echo 'col-md-8';
                } else {
                    echo 'col-md-12';
                }
            } ?>">

                <!--BLOG POST START-->
                <?php while (have_posts()) : the_post(); ?>

                <article id="post-<?php the_ID(); ?>" <?php post_class('clearfix blog-post'); ?>>

                    <?php the_post_thumbnail(); ?>

                    <!--only display if no breadcrumb -->
                    <?php if (!function_exists('cholot_breadcrumb')) { ?>
                    <div class="blogtitle-box clearfix">
                        <h1 class="blog-title"><?php the_title(); ?></h1>
                    </div>
                    <?php } ?>

                    <div class="spacing30 clearfix"></div>

                    <?php the_content(); ?>
                    <div class="spacing40 clearfix"></div>

                    <div class="post-pager clearfix">
                        <?php wp_link_pages(); ?>
                    </div>
                    <div class="blog-bottom-box">

                        <ul class="post-detail single-post-detail">

                            <li><i class="fa fa-calendar-o"></i> <?php echo get_the_date(); ?> </li>

                        </ul>

                    </div>
                    <div class="clearboth spacing40"></div>

                </article>
                <!--/.blog-post-->
                <?php endwhile; ?>
                <!--BLOG POST END-->
                <?php if (comments_open()) { ?>
                <div id="comments" class="comments clearfix"><?php comments_template(); ?></div>
                <?php } ?>

                <div class="spacing40 clearfix"></div>
            </div>
            <!--/.col-md-8-->

            <?php if (function_exists('dynamic_sidebar')) {
                if (is_active_sidebar('default-sidebar')) {
                    get_sidebar();
                }
            } ?>
        </div>
        <!--/.row-->
    </div>
    <!--/.container-->
</div>
<!--/.blog-wrapper-->

<?php
//custom footer
if (class_exists('Kirki')) {
    do_action('cholot-custom-footer', 'cholot_footer_start');
} else {
    //fallback if no kirki installed
    get_template_part('loop/bottom', 'footer');
}

get_footer(); ?>