<?php get_header(); ?>

<?php if (have_posts()) : ?>
    <?php while (have_posts()) : the_post(); ?>
        <div class="page-header <?php if (has_post_thumbnail()) { echo 'has-background'; } ?>" 
             <?php if (has_post_thumbnail()) : ?>style="background-image: url('<?php the_post_thumbnail_url('full'); ?>');"<?php endif; ?>>
            <div class="container">
                <h1 class="page-title"><?php the_title(); ?></h1>
            </div>
        </div>

        <main class="site-main">
            <div class="content-area">
                <article id="page-<?php the_ID(); ?>" <?php post_class(); ?>>
                    <div class="entry-content">
                        <?php the_content(); ?>
                        <?php
                        wp_link_pages(array(
                            'before' => '<div class="page-links">' . __('Seiten:', 'wp-blank-modern'),
                            'after'  => '</div>',
                        ));
                        ?>
                    </div>
                </article>
                
                <?php
                // Wenn Kommentare offen sind oder wir mindestens einen Kommentar haben, laden wir das Kommentar-Template.
                if (comments_open() || get_comments_number()) :
                    comments_template();
                endif;
                ?>
            </div>
        </main>
    <?php endwhile; ?>
<?php endif; ?>

<?php get_footer(); ?>
