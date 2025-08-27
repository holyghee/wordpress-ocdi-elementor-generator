<?php
/*
* Related Post
*/ ?>

<?php
$related = cholot_related_post(get_the_ID(), 3);
if ($related->have_posts()) :
    ?>

<div id="related_posts" class="clearfix">
    <div class="rel-inner">
        <p class="rel-sub"><?php esc_html_e('You may also like', 'cholot'); ?></p>
        <h4 class="title-related-post">
            <?php esc_html_e('Other related posts', 'cholot'); ?>
        </h4>
    </div>

    <div class="row">
        <?php
            while ($related->have_posts()) :
                $related->the_post();
                ?>
        <div class="col-sm-4 col-xs-12">

            <?php if (class_exists('Kirki') && get_theme_mod('cholot_related_image') == 'show') {  ?>
            <a class="rl-image" href="<?php the_permalink()  ?>" rel="bookmark" title="<?php the_title_attribute(); ?>">
                <?php the_post_thumbnail('cholot-related-post'); ?>

                <?php if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_slider') { ?>
                <i class="rl-icon fa fa-sticky-note-o"></i>
                <?php } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_gallery') { ?>
                <i class="rl-icon fa fa-newspaper-o"></i>
                <?php } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_video') {  ?>
                <i class="rl-icon fa fa-film"></i>
                <?php } else if (get_post_meta(get_the_ID(), 'post_format', true) == 'post_audio') { ?>
                <i class="rl-icon fa fa-headphones"></i>
                <?php } else { ?>
                <i class="rl-icon fa fa-photo"></i>
                <?php } ?>
            </a>
            <?php } ?>
            <div class="<?php if (class_exists('Kirki') && get_theme_mod('cholot_related_image') == 'show') {
                                    echo 'rel-img';
                                } ?> related-inner clerfix">
                <a href="<?php the_permalink()  ?>" rel="bookmark" title="<?php the_title_attribute(); ?>">

                    <p class="related-cat">
                        <?php $category = get_the_category();
                                if (isset($category) && isset($category[0])) {
                                    echo wp_kses_post($category[0]->cat_name);
                                } ?>
                    </p>
                    <h3 class="related-title">
                        <?php the_title(); ?>
                    </h3>

                    <?php $rel_main_excerpt = get_the_excerpt();
                            $rel_excerpt = substr($rel_main_excerpt, 0, 65);
                            if ($rel_excerpt != '') { ?>

                    <div class="widget-border"></div>

                    <?php } ?>
                </a>
            </div>
        </div>
        <!--/.col-sm-4-->
        <?php endwhile; ?>
    </div>
    <!--/.row-->
</div>
<!--related-post-->
<?php endif;
wp_reset_postdata(); ?>