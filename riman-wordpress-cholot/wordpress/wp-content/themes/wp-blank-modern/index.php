<?php get_header(); ?>

<main class="site-main">
    <div class="content-area">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                    <header class="entry-header">
                        <?php if (is_singular()) : ?>
                            <h1 class="entry-title"><?php the_title(); ?></h1>
                        <?php else : ?>
                            <h2 class="entry-title">
                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                            </h2>
                        <?php endif; ?>
                        
                        <?php if (!is_page()) : ?>
                            <div class="entry-meta">
                                <time datetime="<?php echo get_the_date('c'); ?>">
                                    <?php echo get_the_date(); ?>
                                </time>
                                <?php if (get_the_author()) : ?>
                                    von <?php the_author(); ?>
                                <?php endif; ?>
                            </div>
                        <?php endif; ?>
                    </header>

                    <div class="entry-content">
                        <?php 
                        if (is_singular()) {
                            the_content();
                        } else {
                            the_excerpt();
                        }
                        ?>
                    </div>
                </article>
            <?php endwhile; ?>
            
            <?php if (!is_singular()) : ?>
                <div class="pagination">
                    <?php 
                    the_posts_pagination(array(
                        'prev_text' => '&laquo; Vorherige',
                        'next_text' => 'Nächste &raquo;'
                    )); 
                    ?>
                </div>
            <?php endif; ?>
            
        <?php else : ?>
            <article>
                <h1>Nichts gefunden</h1>
                <p>Es wurden keine Inhalte gefunden.</p>
            </article>
        <?php endif; ?>
    </div>
</main>

<?php get_footer(); ?>
