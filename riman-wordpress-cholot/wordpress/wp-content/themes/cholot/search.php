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

        <h1 class="blog-title">
            <?php echo esc_html__('Search results for: ', 'cholot') . get_search_query(); ?></h1>
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
                <?php if (have_posts()) : ?>

                <?php while (have_posts()) : the_post();
                        get_template_part('loop/loop', 'post');
                    endwhile  ?>

                <?php else : ?>
                <p><?php esc_html_e('Sorry, no results found, try a different search. ', 'cholot'); ?></p>

                <div class="searchform-page">
                    <?php get_search_form(); ?>
                </div>

                <?php endif; ?>
                <!--BLOG POST END-->

                <ul class="pagination clearfix">
                    <li><?php previous_posts_link();  ?></li>
                    <li><?php next_posts_link(); ?> </li>
                </ul>
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