<?php get_header(); ?>

<main class="site-main">
    <?php
    if (have_posts()) :
        while (have_posts()) : the_post();
            ?>
            <article <?php post_class(); ?>>
                <?php the_content(); ?>
            </article>
            <?php
        endwhile;
    else :
        // If no content, show a default message
        ?>
        <div class="no-content">
            <p><?php _e('No content found. Please add content using the WordPress block editor.', 'riman-modern'); ?></p>
        </div>
        <?php
    endif;
    ?>
</main>

<?php get_footer(); ?>