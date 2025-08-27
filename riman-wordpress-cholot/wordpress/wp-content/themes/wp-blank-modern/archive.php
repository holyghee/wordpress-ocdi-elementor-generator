<?php get_header(); ?>

<div class="page-header">
    <div class="container">
        <h1 class="page-title">
            <?php
            if (is_category()) {
                single_cat_title();
            } elseif (is_tag()) {
                single_tag_title();
            } elseif (is_author()) {
                echo __('Artikel von ', 'wp-blank-modern') . get_the_author();
            } elseif (is_date()) {
                echo __('Archiv: ', 'wp-blank-modern');
                if (is_day()) {
                    echo get_the_date();
                } elseif (is_month()) {
                    echo get_the_date(_x('F Y', 'monatliches Datumsformat', 'wp-blank-modern'));
                } elseif (is_year()) {
                    echo get_the_date(_x('Y', 'jährliches Datumsformat', 'wp-blank-modern'));
                }
            } elseif (is_post_type_archive()) {
                post_type_archive_title();
            } else {
                echo __('Archiv', 'wp-blank-modern');
            }
            ?>
        </h1>
        <?php
        // Zeige eine optionale Term-Beschreibung.
        $term_description = term_description();
        if (!empty($term_description)) :
            printf('<div class="taxonomy-description">%s</div>', $term_description);
        endif;
        ?>
    </div>
</div>

<main class="site-main">
    <div class="content-area">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                    <header class="entry-header">
                        <h2 class="entry-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h2>
                        <?php if ('post' === get_post_type()) : ?>
                        <div class="entry-meta">
                            <time datetime="<?php echo get_the_date('c'); ?>">
                                <?php echo get_the_date(); ?>
                            </time>
                            <?php if (get_the_author()) : ?>
                                <span class="byline"> <?php _e('von', 'wp-blank-modern'); ?> <?php the_author_posts_link(); ?></span>
                            <?php endif; ?>
                        </div>
                        <?php endif; ?>
                    </header>

                    <div class="entry-content">
                        <?php the_excerpt(); ?>
                    </div>
                </article>
            <?php endwhile; ?>
            
            <div class="pagination">
                <?php 
                the_posts_pagination(array(
                    'prev_text' => '&laquo; ' . __('Vorherige', 'wp-blank-modern'),
                    'next_text' => __('Nächste', 'wp-blank-modern') . ' &raquo;'
                )); 
                ?>
            </div>
        <?php else : ?>
            <article>
                <h1><?php _e('Nichts gefunden', 'wp-blank-modern'); ?></h1>
                <p><?php _e('Es wurden keine Inhalte für dieses Archiv gefunden.', 'wp-blank-modern'); ?></p>
            </article>
        <?php endif; ?>
    </div>
</main>

<?php get_footer(); ?>
