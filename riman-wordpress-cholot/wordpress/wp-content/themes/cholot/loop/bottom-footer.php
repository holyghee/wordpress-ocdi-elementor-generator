<?php
/*
* Bottom Footer
*/ ?>

<footer class="footer">

    <div class="container-fluid">


        <?php if (class_exists('Kirki') && get_theme_mod('cholot_footer_logo')) { ?>
        <img class="footer-img" src="<?php echo esc_url(get_theme_mod('cholot_footer_logo')); ?>"
            alt="<?php esc_attr_e('Logo', 'cholot'); ?>">
        <?php }  ?>

        <?php if (class_exists('Kirki') && get_theme_mod('cholot_footer_text')) {
            $cholot_fot_text = get_theme_mod('cholot_footer_text');
            echo '<div class="spacing30 clearfix"></div>';
            echo wp_kses_post($cholot_fot_text);
            echo '<div class="spacing30 clearfix"></div>';
        } ?>

        <ul class="footer-icon  <?php if (class_exists('Kirki') && get_theme_mod('cholot_footer_text') == '') {
                                    echo 'with-margin';
                                } ?>">
            <?php if (class_exists('Kirki')) : if (get_theme_mod('fb_social_foot')) :  ?>
            <li><a href="<?php echo esc_url(get_theme_mod('fb_social_foot')); ?>"><i class="fa fa-facebook"></i></a>
            </li>
            <?php endif;
            endif; ?>
            <?php if (class_exists('Kirki')) : if (get_theme_mod('lkd_social_foot')) :  ?>
            <li><a href="<?php echo esc_url(get_theme_mod('fb_social_foot')); ?>"><i class="fa fa-linkedin"></i></a>
            </li>
            <?php endif;
            endif; ?>
            <?php if (class_exists('Kirki')) : if (get_theme_mod('tw_social_foot')) :  ?>
            <li><a href="<?php echo esc_url(get_theme_mod('fb_social_foot')); ?>"><i class="fa fa-twitter"></i></a></li>
            <?php endif;
            endif; ?>

            <!--ANOTHER SOCIAL ICON LIST-->
            <?php if (class_exists('Kirki')) {
                if (get_theme_mod('social_icon_footer')) {
                    $rdn_socials = get_theme_mod('social_icon_footer');
                    foreach ($rdn_socials as $rdn_social) {
                        if ($rdn_social['link_url_foot'] || $rdn_social['link_text_foot']) { ?>
            <li>
                <a href="<?php echo esc_url($rdn_social['link_url_foot']); ?>">
                    <i class="fa <?php echo esc_attr($rdn_social['link_text_foot']); ?>"></i>
                </a>
            </li>
            <?php }
                    }
                }
            } ?>
            <!--ANOTHER SOCIAL ICON LIST END-->
        </ul>
        <!--/.footer-icon-->







    </div>
    <!--/.container-fluid-->
</footer>
<!--/.footer-->