<?php get_header(); ?>

<div class="page-header">
    <div class="container">
        <h1 class="page-title"><?php _e('404 - Seite nicht gefunden', 'wp-blank-modern'); ?></h1>
    </div>
</div>

<main class="site-main">
    <div class="content-area">
        <article>
            <div class="entry-content">
                <p><?php _e('Die angeforderte Seite konnte leider nicht gefunden werden. Vielleicht hilft eine Suche?', 'wp-blank-modern'); ?></p>
                <?php get_search_form(); ?>
                <p><a href="<?php echo esc_url(home_url('/')); ?>"><?php _e('Zur Startseite', 'wp-blank-modern'); ?></a></p>
            </div>
        </article>
    </div>
</main>

<?php get_footer(); ?>
