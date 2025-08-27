<?php

namespace CholotPlugin;

use CholotPlugin\Widgets\Cholot_Contact;
use CholotPlugin\Widgets\Cholot_Gallery;
use CholotPlugin\Widgets\Cholot_Logo;
use CholotPlugin\Widgets\Cholot_Button;
use CholotPlugin\Widgets\Cholot_MasonGallery;
use CholotPlugin\Widgets\Cholot_Menu;
use CholotPlugin\Widgets\Cholot_Post;
use CholotPlugin\Widgets\Cholot_PostFour;
use CholotPlugin\Widgets\Cholot_PostSlider;
use CholotPlugin\Widgets\Cholot_PostThree;
use CholotPlugin\Widgets\Cholot_PostTwo;
use CholotPlugin\Widgets\Cholot_Share;
use CholotPlugin\Widgets\Cholot_Sidebar;
use CholotPlugin\Widgets\Cholot_Team;
use CholotPlugin\Widgets\Cholot_TeamHover;
use CholotPlugin\Widgets\Cholot_Testimonial;
use CholotPlugin\Widgets\Cholot_TextIcon;
use CholotPlugin\Widgets\Cholot_TextIconHover;
use CholotPlugin\Widgets\Cholot_TextLine;
use CholotPlugin\Widgets\Cholot_Title;
use CholotPlugin\Widgets\Rdn_Slider;
use CholotPlugin\Widgets\Cholot_Button_Text;
use CholotPlugin\Widgets\Cholot_Testimonial_Two;

if (!defined('ABSPATH')) {
    exit;
}
// Exit if accessed directly

/**
 * Main Plugin Class
 *
 * Register new elementor widget.
 *
 * @since 1.0.0
 */
class CholotPlugin
{

    /**
     * Constructor
     *
     * @since 1.0.0
     *
     * @access public
     */
    public function __construct()
    {
        $this->add_actions();
    }

    /**
     * Add Actions
     *
     * @since 1.0.0
     *
     * @access private
     */
    private function add_actions()
    {
        //register all script
        add_action('elementor/widgets/widgets_registered', [$this, 'on_widgets_registered']);
        //isotope script
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('jquery-isotope', CHOLOT_URL . 'widgets/js/isotope.pkgd.js', array('jquery'), null, true);
        });

        //blog masonry script
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-blog-masonry', CHOLOT_URL . 'widgets/js/blog-mason.js', array('jquery'), null, true);
        });
        //slider script
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('jquery-slick', CHOLOT_URL . 'widgets/js/slick.min.js.js', array('jquery'), null, true);
        });
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-animation', CHOLOT_URL . 'widgets/js/slick-animation.js', array('jquery'), null, true);
        });
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-slider-script', CHOLOT_URL . 'widgets/js/slider.js', array('jquery'), null, true);
        });
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-blog-slider-script', CHOLOT_URL . 'widgets/js/blog-slider.js', array('jquery'), null, true);
        });
        //gallery popup
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('jquery-magnificpopup', CHOLOT_URL . 'widgets/js/jquery.magnific-popup.min.js', array('jquery'), null, true);
        });
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-gallery-popup', CHOLOT_URL . 'widgets/js/popup-gallery.js', array('jquery'), null, true);
        });
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-blog-script', CHOLOT_URL . 'widgets/js/blog.js', array('jquery'), null, true);
        });

        //gallery  masonry
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-masonry-gallery', CHOLOT_URL . 'widgets/js/mason-gallery.js', array('jquery'), null, true);
        });

        //share script
        add_action('elementor/frontend/after_register_scripts', function () {
            wp_register_script('cholot-share', CHOLOT_URL . 'widgets/js/share.js', array('jquery'), null, true);
        });
    }

    /**
     * On Widgets Registered
     *
     * @since 1.0.0
     *
     * @access public
     */
    public function on_widgets_registered()
    {
        $this->includes();
        $this->register_widget();
    }

    /**
     * Includes
     *
     * @since 1.0.0
     *
     * @access private
     */
    private function includes()
    {
        require __DIR__ . '/widgets/rdn-slider.php';
        require __DIR__ . '/widgets/title.php';
        require __DIR__ . '/widgets/testimonial.php';
        require __DIR__ . '/widgets/testimonial-two.php';
        require __DIR__ . '/widgets/team.php';
        require __DIR__ . '/widgets/team-hover.php';
        require __DIR__ . '/widgets/text-line.php';
        require __DIR__ . '/widgets/text-icon.php';
        require __DIR__ . '/widgets/text-icon-hover.php';
        require __DIR__ . '/widgets/post.php';
        require __DIR__ . '/widgets/post-two.php';
        require __DIR__ . '/widgets/post-three.php';
        require __DIR__ . '/widgets/post-four.php';
        require __DIR__ . '/widgets/post-slider.php';
        require __DIR__ . '/widgets/menu.php';
        require __DIR__ . '/widgets/contact.php';
        require __DIR__ . '/widgets/gallery.php';
        require __DIR__ . '/widgets/mason-gallery.php';
        require __DIR__ . '/widgets/logo.php';
        require __DIR__ . '/widgets/sidebar.php';
        require __DIR__ . '/widgets/share.php';
        require __DIR__ . '/widgets/button.php';
        require __DIR__ . '/widgets/button-text.php';
    }

    /**
     * Register Widget
     *
     * @since 1.0.0
     *
     * @access private
     */
    private function register_widget()
    {
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Rdn_Slider());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Title());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Team());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_TeamHover());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Testimonial());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Testimonial_Two());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_TextIcon());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_TextLine());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_TextIconHover());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Post());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_PostTwo());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_PostThree());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_PostFour());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_PostSlider());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Menu());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Contact());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Gallery());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_MasonGallery());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Logo());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Sidebar());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Share());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Button());
        \Elementor\Plugin::instance()->widgets_manager->register_widget_type(new Cholot_Button_Text());
    }
}


new CholotPlugin();