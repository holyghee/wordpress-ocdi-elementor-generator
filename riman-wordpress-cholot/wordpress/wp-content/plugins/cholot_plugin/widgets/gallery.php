<?php
namespace CholotPlugin\Widgets;

use Elementor\Controls_Manager;
use Elementor\Group_Control_Typography;
use Elementor\Widget_Base;

if (!defined('ABSPATH')) {
    exit;
}
// Exit if accessed directly

/**
 * @since 1.1.0
 */
class Cholot_Gallery extends Widget_Base
{

    /**
     * Retrieve the widget name.
     *
     * @since 1.1.0
     *
     * @access public
     *
     * @return string Widget name.
     */
    public function get_name()
    {
        return 'cholot-gallery';
    }

    public function get_script_depends()
    {
        return ['jquery-magnific-popup', 'cholot-gallery-popup'];
    }

    /**
     * Retrieve the widget title.
     *
     * @since 1.1.0
     *
     * @access public
     *
     * @return string Widget title.
     */
    public function get_title()
    {
        return __('Cholot Gallery', 'cholot_plugin');
    }

    /**
     * Retrieve the widget icon.
     *
     * @since 1.1.0
     *
     * @access public
     *
     * @return string Widget icon.
     */
    public function get_icon()
    {
        return 'eicon-gallery-grid';
    }

    /**
     * Retrieve the list of categories the widget belongs to.
     *
     * Used to determine where to display the widget in the editor.
     *
     * Note that currently Elementor supports only one category.
     * When multiple categories passed, Elementor uses the first one.
     *
     * @since 1.1.0
     *
     * @access public
     *
     * @return array Widget categories.
     */
    public function get_categories()
    {
        return ['cholot-elements'];
    }

    /**
     * Register the widget controls.
     *
     * Adds different input fields to allow the user to change and customize the widget settings.
     *
     * @since 1.1.0
     *
     * @access protected
     */
    protected function _register_controls()
    {

        $this->start_controls_section(
            'section_title',
            [
                'label' => __('Gallery', 'cholot_plugin'),
            ]
        );

        $this->add_control(
            'gallery',
            [
                'label' => __('Add Images', 'elementor'),
                'type' => Controls_Manager::GALLERY,
            ]
        );

        $this->add_control(
            'port_column',
            [
                'label' => __('Gallery Columns', 'cholot_plugin'),
                'type' => Controls_Manager::SELECT,
                'options' => [
                    'col-md-6' => __('Two Columns', 'cholot_plugin'),
                    'col-md-4' => __('Three Columns', 'cholot_plugin'),
                    'col-md-3' => __('Four Columns', 'cholot_plugin'),
                ],
                'default' => 'col-md-3',
            ]
        );

        $this->add_responsive_control(
            'gallery_height',
            [
                'label' => __('Gallery Item Height', 'cholot_plugin'),
                'type' => Controls_Manager::SLIDER,
                'range' => [
                    'px' => [
                        'min' => 1,
                        'max' => 100,
                    ],
                ],
                'selectors' => [
                    '{{WRAPPER}} .port-box ' => 'padding: {{SIZE}}% 0;',
                ],
            ]
        );

        $this->add_responsive_control(
            'gallery_margin',
            [
                'label' => __('Gallery Item Margin', 'cholot_plugin'),
                'type' => Controls_Manager::SLIDER,
                'range' => [
                    'px' => [
                        'min' => 1,
                        'max' => 100,
                    ],
                ],
                'selectors' => [
                    '{{WRAPPER}} .port-item' => 'padding: {{SIZE}}{{UNIT}};',
                    '{{WRAPPER}} .cholot-gallery' => 'margin: -{{SIZE}}{{UNIT}};overflow:hidden;',
                ],
            ]
        );

        $this->add_control(
            'image_position',
            [
                'label' => __('Image Position', 'cholot_plugin'),
                'type' => Controls_Manager::SELECT,
                'options' => [
                    'center center' => __('Center Center', 'cholot_plugin'),
                    'center left' => __('Center Left', 'cholot_plugin'),
                    'center right' => __('Center Right', 'cholot_plugin'),
                    'top center' => __('Top Center', 'cholot_plugin'),
                    'top left' => __('Top Left', 'cholot_plugin'),
                    'top right' => __('Top Right', 'cholot_plugin'),
                    'bottom center' => __('Bottom Center', 'cholot_plugin'),
                    'bottom left' => __('Bottom Left', 'cholot_plugin'),
                    'bottom right' => __('Bottom Right', 'cholot_plugin'),
                ],
                'default' => 'center center',
                'selectors' => [
                    '{{WRAPPER}} .port-img ' => 'background-position: {{VALUE}};',
                ],
            ]
        );

        $this->add_control(
            'title_show',
            [
                'label' => __('Show Image Title', 'cholot_plugin'),
                'type' => Controls_Manager::SWITCHER,
                'default' => 'yes',
                'label_on' => __('Show', 'cholot_plugin'),
                'label_off' => __('Hide', 'cholot_plugin'),
                'return_value' => 'yes',
            ]
        );

        $this->add_control(
            'caption_show',
            [
                'label' => __('Show Image Caption', 'cholot_plugin'),
                'type' => Controls_Manager::SWITCHER,
                'default' => 'yes',
                'label_on' => __('Show', 'cholot_plugin'),
                'label_off' => __('Hide', 'cholot_plugin'),
                'return_value' => 'yes',
            ]
        );

        $this->end_controls_section();

        $this->start_controls_section(
            'section_content_style',
            [
                'label' => __('Content Settings', 'cholot_plugin'),
                'tab' => Controls_Manager::TAB_STYLE,
            ]
        );

        $this->add_responsive_control(
            'port_content',
            [
                'label' => __('Content Margin (on hover)', 'cholot_plugin'),
                'type' => Controls_Manager::DIMENSIONS,
                'size_units' => ['px', '%'],
                'selectors' => [
                    '{{WRAPPER}} .dbox-relative' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
                ],
            ]
        );

        $this->add_responsive_control(
            'port_padding',
            [
                'label' => __('Content Padding (on hover)', 'cholot_plugin'),
                'type' => Controls_Manager::DIMENSIONS,
                'size_units' => ['px', '%'],
                'selectors' => [
                    '{{WRAPPER}} .dbox-relative' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
                ],
            ]
        );

        $this->add_control(
            'bg_content',
            [
                'label' => __('Content Background', 'cholot_plugin'),
                'type' => Controls_Manager::COLOR,
                'default' => '',
                'selectors' => [
                    '{{WRAPPER}} .dbox-relative' => 'background-color: {{VALUE}};',
                ],
            ]
        );

        $this->add_responsive_control(
            'content_align',
            [
                'label' => __('Alignment', 'cholot_plugin'),
                'type' => Controls_Manager::CHOOSE,
                'options' => [
                    'left' => [
                        'title' => __('Left', 'cholot_plugin'),
                        'icon' => 'fa fa-align-left',
                    ],
                    'center' => [
                        'title' => __('Center', 'cholot_plugin'),
                        'icon' => 'fa fa-align-center',
                    ],
                    'right' => [
                        'title' => __('Right', 'cholot_plugin'),
                        'icon' => 'fa fa-align-right',
                    ],
                ],
                'default' => '',
                'selectors' => [
                    '{{WRAPPER}} .dbox-relative' => 'text-align: {{VALUE}};',
                ],
            ]
        );

        $this->end_controls_section();

        $this->start_controls_section(
            'title_typo',
            [
                'label' => __('Title Settings', 'cholot_plugin'),
                'tab' => Controls_Manager::TAB_STYLE,
            ]
        );

        $this->add_group_control(
            Group_Control_Typography::get_type(),
            [
                'name' => 'cport_typography',
                'label' => __('Typography', 'cholot_plugin'),
                'selector' => '{{WRAPPER}} .dbox-relative h3',
            ]
        );

        $this->add_control(
            'title_cl',
            [
                'label' => __('Color', 'cholot_plugin'),
                'type' => Controls_Manager::COLOR,
                'default' => '',
                'selectors' => [
                    '{{WRAPPER}} .dbox-relative h3' => 'color: {{VALUE}};',
                ],
            ]
        );

        $this->end_controls_section();

        $this->start_controls_section(
            'sub_typo',
            [
                'label' => __('Caption Settings', 'cholot_plugin'),
                'tab' => Controls_Manager::TAB_STYLE,
            ]
        );

        $this->add_group_control(
            Group_Control_Typography::get_type(),
            [
                'name' => 'ctext_typography',
                'label' => __('Text Typography', 'cholot_plugin'),
                'selector' => '{{WRAPPER}} .dbox-relative p',
            ]
        );

        $this->add_control(
            'txt_cl',
            [
                'label' => __('Text Color', 'cholot_plugin'),
                'type' => Controls_Manager::COLOR,
                'default' => '',
                'selectors' => [
                    '{{WRAPPER}} .dbox-relative p' => 'color: {{VALUE}};',
                ],
            ]
        );

        $this->end_controls_section();

        $this->start_controls_section(
            'port_mask',
            [
                'label' => __('Mask Settings', 'cholot_plugin'),
                'tab' => Controls_Manager::TAB_STYLE,
            ]
        );

        $this->add_control(
            'mask_color',
            [
                'label' => __('Mask Color', 'cholot_plugin'),
                'type' => Controls_Manager::COLOR,
                'default' => '',
                'selectors' => [
                    '{{WRAPPER}} .port-inner:hover .port-box' => 'background-color: {{VALUE}};',
                ],
            ]
        );

        $this->add_control(
            'mask_color_opacity',
            [
                'label' => __('Mask Color Opacity(on hover)', 'cholot_plugin'),
                'type' => Controls_Manager::SLIDER,
                'range' => [
                    'px' => [
                        'min' => 0,
                        'max' => 1,
                        'step' => 0.1,
                    ],
                ],
                'selectors' => [
                    '{{WRAPPER}} .port-inner:hover .port-box' => 'opacity: {{SIZE}};',
                ],
            ]
        );

        $this->end_controls_section();
    }

    /**
     * Render the widget output on the frontend.
     *
     * Written in PHP and used to generate the final HTML.
     *
     * @since 1.1.0
     *
     * @access protected
     */
    protected function render()
    {
        $settings = $this->get_settings();
        $images = $this->get_settings('gallery');
        ?>


    <div class="cholot-gallery clearfix">
        <?php foreach ($images as $image) {
            $img = get_post($image['id']);
            //get the image title
            $image_title = $img->post_title;
            //get the image caption
            $image_caption = $img->post_excerpt;
            ?>

            <div class="<?php echo esc_attr($settings['port_column']); ?> port-item">

                <div class="port-inner">
                    <a href="<?php echo esc_url($image['url']); ?>" class="port-link popup-portfolio" <?php if ($settings['title_show'] == 'yes') { ?> title="<?php echo esc_attr($image_title) ?>" <?php } ?>></a>

                    <div class="port-box"></div>
                    <div class="port-img width-img img-bg" style="background-image:url(<?php echo esc_url($image['url']); ?>);"></div>
                    <div class="img-mask"></div>
                    <div class="port-dbox">

                        <?php if ($settings['title_show'] == 'yes' || $settings['caption_show'] == 'yes') { ?>
                            <div class="dbox-relative">

                                <?php if ($settings['title_show'] == 'yes') { ?>
                                    <h3><?php echo esc_attr($image_title) ?></h3>
                                <?php } ?>

                                <?php if ($settings['caption_show'] == 'yes' && $image_caption) { ?>
                                    <p><?php echo esc_attr($image_caption) ?></p>
                                <?php } ?>
                            </div>
                            <!--/.dbox-relative-->
                        <?php } ?>

                    </div>
                    <!--/.port-dbox-->


                </div>
                <!--/.port-inner-->

            </div>
            <!--.port-item-->

        <?php

    } ?>
    </div>
<?php
}

/**
 * Render the widget output in the editor.
 *
 * Written as a Backbone JavaScript template and used to generate the live preview.
 *
 * @since 1.1.0
 *
 * @access protected
 */
protected function _content_template()
{ }
}
