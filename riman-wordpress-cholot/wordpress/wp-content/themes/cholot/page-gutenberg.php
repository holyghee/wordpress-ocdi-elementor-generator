<?php
/**
 * Template Name: Gutenberg Full Width
 * Template for displaying Gutenberg block content
 */

get_header();
?>

<div id="primary" class="content-area">
    <main id="main" class="site-main">
        <?php
        while ( have_posts() ) :
            the_post();
            ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <div class="entry-content">
                    <?php
                    the_content();
                    
                    wp_link_pages( array(
                        'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'cholot' ),
                        'after'  => '</div>',
                    ) );
                    ?>
                </div>
            </article>
        <?php
        endwhile;
        ?>
    </main>
</div>

<style>
/* Override Cholot theme styles for Gutenberg blocks */
.entry-content {
    max-width: 100%;
    margin: 0;
    padding: 0;
}

.wp-block-cover.alignfull {
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
}

.site-main {
    padding: 0;
    margin: 0;
}

#primary {
    width: 100%;
    max-width: 100%;
}
</style>

<?php
get_footer();