<?php

get_header();



//custom header
if (class_exists('Kirki')) {
    do_action('cholot-custom-header', 'cholot_header_start');
} else { ?>

<!--Fall back if no kirki plugin installed-->
<!--HOME START-->
<div class="default-header clearfix">
    <!--HEADER START-->
    <?php get_template_part('loop/menu', 'normal'); ?>
    <!--HEADER END-->
</div>
<!--/home end-->
<!--HOME END-->

<?php }  ?>

<!--breadcrumb if available-->
<?php if (function_exists('cholot_breadcrumb')) { ?>
<div class="box-crumb clearfix">
    <div class="slider-mask"></div>
    <div class="container">
        <?php if (function_exists('cholot_breadcrumb')) {
                cholot_breadcrumb();
            } ?>

        <h1 class="blog-title">
            <?php if (is_front_page()) {
                    echo esc_html__('Home', 'cholot');
                } else if (is_category()) {
                    echo esc_html__('Archive by category: ', 'cholot') . single_cat_title('', false);
                } else if (is_tag()) {
                    echo esc_html__('Posts tagged: ', 'cholot') . single_tag_title('', false);
                } ?></h1>
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
                <?php while (have_posts()) : the_post();
                    get_template_part('loop/loop', 'post');
                endwhile ?>

                <ul class="pagination clearfix">
                    <li><?php previous_posts_link(esc_html__('Previous Page', 'cholot')); ?></li>
                    <li><?php next_posts_link(esc_html__('Next Page', 'cholot')); ?> </li>
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
} ?>



<?php get_footer(); ?>