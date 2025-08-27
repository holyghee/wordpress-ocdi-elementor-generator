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
        <ul class="post-detail single-post-detail">

            <?php if (has_category()) { ?>
            <li><i class="fa fa-archive"></i> <?php the_category(', '); ?></li>
            <?php } ?>

            <?php if (get_the_tag_list()) { ?>
            <li><i class="fa fa-tags"></i>
                <?php the_tags('', ', '); ?>
            </li>
            <?php } ?>
            <li><i class="fa fa-calendar-o"></i> <?php echo get_the_date(); ?> </li>

        </ul>


    </div>

</div>
<?php } ?>

<div class="content blog-wrapper">
    <div class="container-fluid clearfix">
        <div class="row clearfix">

            <div class="blog-content
			<?php if (function_exists('dynamic_sidebar')) {
                if (is_active_sidebar('default-sidebar')) {
                    if (get_post_meta(get_the_ID(), 'post_sidebar', true) == '' || get_post_meta($post->ID, 'post_sidebar', true) == 'show') {
                        echo 'col-md-8';
                    } else {
                        echo 'col-md-12';
                    }
                } else {

                    echo 'col-md-12';
                }
            } ?>">
                <!--BLOG POST START-->
                <?php while (have_posts()) : the_post(); ?>

                <article id="post-<?php the_ID(); ?>" <?php post_class('clearfix blog-post'); ?>>



                    <!--if post is standard-->
                    <?php if (get_post_meta(get_the_ID(), 'post_format', true) == '') {
                            the_post_thumbnail();
                        } ?>
                    <?php if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_standard') { ?>
                    <?php the_post_thumbnail('full', array('class' => 'full-size-img')); ?>
                    <!--if post is gallery-->
                    <?php } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_gallery') { ?>
                    <div class="blog-gallery clearboth clearfix">

                        <?php /* get the gallery list array */
                                $lists = get_post_meta(get_the_ID(), 'post_gallery_setting',  1);

                                if (!empty($lists)) {
                                    foreach ((array) $lists as $list => $attachment_url) { ?>
                        <div>
                            <a class="blog-popup-img"
                                href="<?php echo esc_url(wp_get_attachment_image_url($list, 'full'));  ?>">
                                <span>
                                    <i class="fa fa-search"></i>
                                </span>
                                <?php echo wp_get_attachment_image($list, 'full') ?>
                            </a>
                        </div>
                        <?php }
                                } ?>

                    </div>

                    <?php //if post is slider
                        } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_slider') { ?>

                    <div class="blog-slider ani-slider slider" data-slick='{"autoplaySpeed":
                            <?php if (class_exists('Kirki') && get_theme_mod('cholot_blog_slider_delay') != '') {
                                echo esc_attr(get_theme_mod('cholot_blog_slider_delay'));
                            } else {
                                echo '8000';
                            } ?> }'>

                        <?php /* get the gallery list array */
                                $sliders = get_post_meta(get_the_ID(), 'post_slider_setting',  1);

                                if (!empty($sliders)) {
                                    foreach ((array) $sliders as $slider => $attachment_url) { ?>
                        <div class="slide">
                            <div class="slider-mask" data-animation="slideLeftReturn" data-delay="0.1s"></div>
                            <div class="slider-img-bg blog-img-bg" data-animation="fadeIn" data-delay="0.2s"
                                data-animation-duration="0.7s"
                                data-background="<?php echo esc_url(wp_get_attachment_image_url($slider, 'full'));  ?>">
                            </div>
                            <div class="blog-slider-box">
                                <div class="slider-content"></div>
                            </div>
                            <!--/.blog-slider-box-->
                        </div>
                        <!--/.slide-->
                        <?php }
                                } ?>
                    </div>



                    <?php //if post video	
                        } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_video') {
                            echo '<div class="video"><iframe width="560" height="315" 
								src="' . esc_attr(get_post_meta(get_the_ID(), 'post_video_setting', true)) . '?wmode=opaque;rel=0;showinfo=0;controls=0;iv_load_policy=3"></iframe></div>';

                            //if post audio
                        } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_audio') { ?>
                    <div class="audio">
                        <?php $cholot_audio = get_post_meta(get_the_ID(), 'post_audio_setting', true);
                                echo wp_kses($cholot_audio, array(
                                    'iframe' => array(
                                        'src' => array(),
                                        'width' => array(),
                                        'height' => array(),
                                        'scrolling' => array(),
                                        'frameborder' => array(),
                                    ),
                                )); ?>
                    </div>
                    <?php } ?>

                    <!--only display if no breadcrumb -->
                    <?php if (!function_exists('cholot_breadcrumb')) { ?>
                    <div class="blogtitle-box clearfix">
                        <h1 class="blog-title"><?php the_title(); ?></h1>
                        <div class="spacing30"></div>
                    </div>
                    <ul class="post-detail">

                        <?php if (has_category()) { ?>
                        <li><i class="fa fa-archive"></i> <?php the_category(', '); ?></li>
                        <?php } ?>

                        <?php if (get_the_tag_list()) { ?>
                        <li><i class="fa fa-tags"></i>
                            <?php the_tags('', ', '); ?>
                        </li>
                        <?php } ?>
                        <li><i class="fa fa-calendar-o"></i> <?php echo get_the_date(); ?> </li>

                    </ul>
                    <?php } ?>

                    <div class="spacing30 clearfix"></div>

                    <?php the_content(); ?>
                    <div class="spacing30 clearfix"></div>
                    <div class="post-pager clearfix">
                        <?php wp_link_pages(); ?>
                    </div>

                    <!--RELATED POST-->

                    <?php if (function_exists('dynamic_sidebar')) {
                            if (is_active_sidebar('default-sidebar')) {
                                if (get_post_meta(get_the_ID(), 'post_sidebar', true) == '' || get_post_meta($post->ID, 'post_sidebar', true) == 'show') {
                                    get_template_part('loop/related', 'post');
                                } else {
                                    get_template_part('loop/related', 'post-two');
                                }
                            } else {

                                get_template_part('loop/related', 'post-two');
                            }
                        } ?>

                    <!--RELATED POST END-->

                    <?php if (!post_password_required()) { //only show comment if post not password protected

                            // If comments are open or we have at least one comment, load up the comment template.
                            if (comments_open() || get_comments_number()) :
                                comments_template();

                            endif;
                        } ?>

                </article>
                <!--/.blog-post-->
                <!--BLOG POST END-->


                <?php endwhile; ?>

                <div class="img-pagination">
                    <?php $cholot_prevPost = get_previous_post();
                    if ($cholot_prevPost) { ?>
                    <div class="pagi-nav-box previous">
                        <?php $cholot_prevthumbnail = get_the_post_thumbnail($cholot_prevPost->ID, array(300, 300));
                            $cholot_prev = esc_html__('Previous post', 'cholot'); ?>
                        <?php previous_post_link('%link', "<div class='img-pagi'><i class='fa fa-arrow-left'></i> 
								<div class='pagimgbox'>$cholot_prevthumbnail</div></div>  <div class='imgpagi-box'><h4 class='pagi-title'>%title</h4> <p>$cholot_prev</p></div>"); ?>
                    </div>

                    <?php }
                    $cholot_nextPost = get_next_post();
                    if ($cholot_nextPost) { ?>
                    <div class="pagi-nav-box next">
                        <?php $cholot_nextthumbnail = get_the_post_thumbnail($cholot_nextPost->ID, array(300, 300));
                            $cholot_next = esc_html__('Next post', 'cholot'); ?>
                        <?php next_post_link('%link', "<div class='imgpagi-box'><h4 class='pagi-title'>%title</h4> <p>$cholot_next</p></div> <div class='img-pagi'><i class='fa 
								fa-arrow-right'></i><div class='pagimgbox'>$cholot_nextthumbnail</div></div> "); ?>
                    </div>
                    <?php } ?>
                </div>
                <!--/.img-pagination-->

            </div>
            <!--/.col-md-8-->

            <?php if (get_post_meta(get_the_ID(), 'post_sidebar', true) == '' || get_post_meta($post->ID, 'post_sidebar', true) == 'show') { ?>
            <?php if (function_exists('dynamic_sidebar')) {
                    if (is_active_sidebar('default-sidebar')) {
                        get_sidebar();
                    }
                } ?>
            <?php } ?>

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