<footer class="site-footer">
    <div class="footer-container">
        <div class="site-info">
            <p>&copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. <?php _e('Alle Rechte vorbehalten.', 'wp-blank-modern'); ?></p>
            <?php if (function_exists('the_privacy_policy_link')) {
                the_privacy_policy_link('', '<span role="separator" aria-hidden="true"></span>');
            } ?>
        </div>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
