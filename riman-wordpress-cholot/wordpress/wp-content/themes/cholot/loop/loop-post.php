<?php
/**
 * Blog Post Loop
 */
?>


<!--BLOG POST START-->


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
                foreach ((array)$lists as $list => $attachment_url) { ?>
        <div>
            <a class="blog-popup-img" href="<?php echo esc_url(wp_get_attachment_image_url($list, 'full'));  ?>">
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
                foreach ((array)$sliders as $slider => $attachment_url) { ?>
        <div class="slide">
            <div class="slider-mask" data-animation="slideLeftReturn" data-delay="0.1s"></div>
            <div class="slider-img-bg blog-img-bg" data-animation="fadeIn" data-delay="0.2s"
                data-animation-duration="0.7s"
                data-background="<?php echo esc_url(wp_get_attachment_image_url($slider, 'full'));  ?>"></div>
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

    <div class="spacing30 clearfix"></div>

    <a href="<?php the_permalink(); ?>">
        <h2 class="blog-title"><?php the_title(); ?></h2>
    </a>


    <div class="spacing30 clearfix"></div>
    <?php the_excerpt(); ?>
    <div class="spacing20 clearfix"></div>
    <a class="content-btn" href="<?php the_permalink(); ?>">
        <?php echo esc_html__('Read More', 'cholot') ?>
    </a>
    <div class="spacing30 clearfix"></div>
    <ul class="post-detail">
        <?php if (has_category()) { ?>
        <li><i class="fa fa-archive"></i> <?php the_category(', '); ?></li>
        <?php } ?>

        <?php if (get_the_tag_list()) { ?>
        <li><i class="fa fa-tags"></i>
            <?php the_tags('', ', '); ?>
        </li>
        <?php } ?>
        <li><i class="fa fa-clock-o"></i> <?php echo get_the_date(); ?> </li>
    </ul>

    <div class="border-post clearfix"></div>
    <div class="clearboth spacing30"></div>
</article>
<!--/.blog-post-->

<!--BLOG POST END-->