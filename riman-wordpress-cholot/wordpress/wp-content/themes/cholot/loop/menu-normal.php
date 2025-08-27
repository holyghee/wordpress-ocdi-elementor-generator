<?php
/*
* Header menu Normal Loop
*/
?>
<nav class="header clean-header white-header clearfix">
    <div class="nav-box">
        <div class="for-sticky">
            <div class="container-fluid">
                <div class="logo-clean">
                    <a href="<?php echo esc_url(home_url('/')); ?>">
                        <img alt="<?php esc_attr_e('Logo', 'cholot'); ?>" class="logo1" src="
                        <?php if (class_exists('Kirki') && get_theme_mod('cholot_logo_image')) {
                            echo esc_url(get_theme_mod('cholot_logo_image'));
                        } else {
                            echo get_template_directory_uri(); ?>/images/logo-white.png <?php } ?>">
                    </a>
                </div>
                <!--/.logo-clean-->
                <div class="box-header hidden-xs hidden-sm">
                    <div class="menu-box">
                        <?php wp_nav_menu(array('items_wrap' => '<ul id="%1$s" class="home-nav navigation %2$s">%3$s</ul>', 'theme_location' => 'ridianur-homepage-menu')); ?>
                    </div>
                    <!--/.menu-box-->
                    <ul class="header-icon hidden-sm hidden-xs">
                        <?php if (class_exists('Kirki')) : if (get_theme_mod('fb_social_head')) :  ?>
                        <li>
                            <a href="<?php echo esc_url(get_theme_mod('fb_social_head')); ?>">
                                <i class="fa fa-facebook">
                                </i>
                            </a>
                        </li>
                        <?php endif;
                        endif; ?>
                        <?php if (class_exists('Kirki')) : if (get_theme_mod('lkd_social_head')) :  ?>
                        <li>
                            <a href="<?php echo esc_url(get_theme_mod('lkd_social_head')); ?>">
                                <i class="fa fa-linkedin">
                                </i>
                            </a>
                        </li>
                        <?php endif;
                        endif; ?>
                        <?php if (class_exists('Kirki')) : if (get_theme_mod('tw_social_head')) :  ?>
                        <li>
                            <a href="<?php echo esc_url(get_theme_mod('tw_social_head')); ?>">
                                <i class="fa fa-twitter">
                                </i>
                            </a>
                        </li>
                        <?php endif;
                        endif; ?>
                        <!--ANOTHER SOCIAL ICON LIST-->
                        <?php if (class_exists('Kirki')) {
                            if (get_theme_mod('social_icon')) {
                                $rdn_socials = get_theme_mod('social_icon');
                                foreach ($rdn_socials as $rdn_social) {
                                    if ($rdn_social['link_url'] || $rdn_social['link_text']) { ?>
                        <li>
                            <a href="<?php echo esc_url($rdn_social['link_url']); ?>">
                                <i class="fa <?php echo esc_attr($rdn_social['link_text']); ?>"></i>
                            </a>
                        </li>
                        <?php }
                                }
                            }
                        } ?>
                        <!--ANOTHER SOCIAL ICON LIST END-->
                    </ul>
                    <!--/.team-icon-->
                </div>
                <!--/.box-header-->
                <div class="box-mobile hidden-lg hidden-md">
                    <div class="mobile-menu-container">
                    </div>
                </div>
                <!--/.box-mobile-->
            </div>
            <!--/.container-fluid-->
        </div>
        <!--/.for-sticky-->
    </div>
    <!--/.nav-box-->
</nav>
<!--/.header-->