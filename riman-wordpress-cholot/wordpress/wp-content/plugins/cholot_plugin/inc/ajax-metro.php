<?php
add_action('wp_ajax_load_metro_by_ajax', 'load_metro_by_ajax_callback');
add_action('wp_ajax_nopriv_load_metro_by_ajax', 'load_metro_by_ajax_callback');

function load_metro_by_ajax_callback()
{
    check_ajax_referer('load_more_metro_ajax', 'security');
    $paged = $_POST['page'];
    $args = array(
        'post_type' => 'portfolio',
        'posts_per_page' => $_POST['portfolio_item'],
        'order' => $_POST['order_value'],
        'paged' => $paged,
    );
    $my_posts = new WP_Query($args);
    if ($my_posts->have_posts()) {
        $i = 0;
        ?>
<?php while ($my_posts->have_posts()) :
            $i++;
            $my_posts->the_post();
            global $post;
            $ridianur_terms = get_the_terms(get_the_ID(), 'portfolio_category'); ?>
<div class="<?php $ridianur_terms = get_the_terms(get_the_ID(), 'portfolio_category');
                        if (is_array($ridianur_terms) && count($ridianur_terms) > 0) {
                            foreach ($ridianur_terms as $ridianur_term) {
                                echo strtolower(preg_replace('/[^a-zA-Z]+/', '-', $ridianur_term->name)) . ' ';
                            }
                        }
                        $ridianur_allClasses = get_post_class();
                        foreach ($ridianur_allClasses as $ridianur_class) {
                            echo esc_attr($ridianur_class . " ");
                        }
                        if ($i  == 1  || $i % 6 == 0) {
                            echo "col-md-6 ";
                        } else {
                            echo "col-md-3 ";
                        } ?> rcol new-rcol port-item" id="post-<?php the_ID(); ?>">

    <div class="port-inner">
        <a class="port-link" href="<?php the_permalink(); ?>"></a>
        <div class="port-box"></div>
        <div class="port-img width-img img-bg"
            style="background-image:url(<?php echo get_the_post_thumbnail_url(); ?>);"></div>
        <div class="img-mask"></div>
        <div class="port-dbox">
            <div class="dbox-relative">
                <h3><?php the_title(); ?></h3>
                <div class="cleaboth clearfix"></div>
                <?php $ridianur_taxonomy = 'portfolio_category';
                            $ridianur_taxs = wp_get_post_terms($post->ID, $ridianur_taxonomy); ?>
                <p><?php $ridianur_cats = array();
                                foreach ($ridianur_taxs as $ridianur_tax) {
                                    $ridianur_cats[] = $ridianur_tax->name;
                                }
                                echo implode(', ', $ridianur_cats); ?></p>
            </div>
            <!--/.dbox-relative-->
        </div>
        <!--/.port-dbox-->
    </div>
    <!--/.port-inner-->



</div>
<!--.port-item-->

<?php endwhile ?>
<?php
} else { ?>
<div class="npsp no-more new-rcol port-item">
    <div class="port-inner nom-btn"><?php echo $_POST['nomore']; ?></div>
</div>

<?php
}

wp_die();
}