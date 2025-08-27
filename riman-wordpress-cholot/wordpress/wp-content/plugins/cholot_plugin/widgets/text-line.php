<?php

namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Border;
use Elementor\Utils;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_TextLine extends Widget_Base
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
		return 'cholot-text-line';
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
		return __('Cholot Text with Line', 'cholot_plugin');
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
		return 'fa fa-pencil-square';
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
			'section_content',
			[
				'label' => __('Settings', 'cholot_plugin'),
			]
		);


		$this->add_responsive_control(
			'title_text_margin',
			[
				'label' => __('Title & Subtitle Spacing', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 6,
						'max' => 300,
					],
				],
				'condition' => [
					'icon_style' => 'left',
				],
				'selectors' => [
					'{{WRAPPER}} .box-with-icon .icon-title' => 'padding-left: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .box-with-icon .icon-subtitle' => 'padding-left: {{SIZE}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'title',
			[
				'label' => __('Title', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'placeholder' => 'Insert your title..',
				'default' => 'Title Here'
			]
		);

		$this->add_control(
			'subtitle',
			[
				'label' => __('Subtitle', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'placeholder' => 'Leave it blank if you don\'t want to use this subtitle',
				'default' => 'Text Here'
			]
		);

		$this->add_control(
			'text',
			[
				'label' => __('Text', 'cholot_plugin'),
				'type' => Controls_Manager::WYSIWYG,
				'label_block' => true,
				'placeholder' => 'Insert your text..',
			]
		);


		$this->add_responsive_control(
			'line',
			[
				'label' => __('Line Width', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'size_units' => ['px', '%'],
				'range' => [
					'px' => [
						'max' => 1000,
					],
					'%' => [
						'max' => 100,
					],
				],
				'default' => [
					'unit' => '%',
					'size' => 100,
				],
				'selectors' => [
					'{{WRAPPER}} .cholot-line' => 'width: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .cholot-line' => 'width: {{SIZE}}{{UNIT}};',
				],
			]
		);
		$this->add_responsive_control(
			'line_height',
			[
				'label' => __('Line Height', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'size_units' => ['px', '%'],
				'range' => [
					'px' => [
						'max' => 100,
					],
					'%' => [
						'max' => 100,
					],
				],
				'default' => [
					'unit' => 'px',
					'size' => 3,
				],
				'selectors' => [
					'{{WRAPPER}} .cholot-line' => 'heigh: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .cholot-line' => 'height: {{SIZE}}{{UNIT}};',
				],
			]
		);
		$this->add_control(
			'btn_text',
			[
				'label' => __('Button Text', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'label_block' => true,
				'placeholder' => 'Insert your button text here..',
			]
		);

		$this->add_control(
			'link',
			[
				'label' => __('Button Link', 'cholot_plugin'),
				'type' => Controls_Manager::URL,
				'placeholder' => 'Leave it blank if you don\'t want to use this button',
			]
		);

		$this->add_control(
			'icon_btn',
			[
				'label' => __('Button Icon', 'cholot_plugin'),
				'type' => Controls_Manager::ICON,
				'label_block' => true,
				'default' => '',
				'condition' => [
					'link!' => '',
				],
			]
		);

		$this->add_control(
			'icon_align',
			[
				'label' => __('Button Icon Position', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'default' => 'left',
				'options' => [
					'left' => __('Before', 'cholot_plugin'),
					'right' => __('After', 'cholot_plugin'),
				],
				'condition' => [
					'link!' => '',
					'icon_btn!' => '',
				],
			]
		);

		$this->add_control(
			'icon_indent',
			[
				'label' => __('Button Icon Spacing', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'max' => 50,
					],
				],
				'condition' => [
					'link!' => '',
					'icon_btn!' => '',
				],
				'selectors' => [
					'{{WRAPPER}} .content-btn .content-btn-align-icon-right' => 'margin-left: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .content-btn .content-btn-align-icon-left' => 'margin-right: {{SIZE}}{{UNIT}};',
				],
			]
		);




		$this->add_control(
			'bg_img',
			[
				'label' => __('Background Image', 'cholot_plugin'),
				'type' => Controls_Manager::MEDIA,
				'default' => [
					'url' => \Elementor\Utils::get_placeholder_image_src(),
				],
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover' => 'background-image: url("{{url}}");',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'title_settings',
			[
				'label' => __('Title Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'title_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .icon-title',
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .icon-title' => 'color: {{VALUE}};',
				],
			]
		);


		$this->add_control(
			'title_color_hover',
			[
				'label' => __('Color on hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .icon-title' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'title_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .icon-title' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'subtitle_settings',
			[
				'label' => __('Subtitle Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'subtitle_typography',
				'label'     => __('Subtitle Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .icon-subtitle',
			]
		);
		$this->add_control(
			'sb_type',
			[
				'label' => __('Subtitle Display', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'block' => __('Block', 'cholot_plugin'),
					'inline-block' => __('Inline Block', 'cholot_plugin'),
				],
				'default' => 'block',
				'selectors' => [
					'{{WRAPPER}} .icon-subtitle' => 'display: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'sb_padding',
			[
				'label' => __('Subtitle Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .box-with-icon .icon-subtitle' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'sb_margin',
			[
				'label' => __('Subtitle Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .icon-subtitle' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'subtitle_color',
			[
				'label' => __('Subtitle Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .icon-subtitle' => 'color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'subtitle_color_hover',
			[
				'label' => __('Subtitle Color on hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .icon-subtitle' => 'color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'subtitle_bgcolor',
			[
				'label' => __('Subtitle Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .icon-subtitle' => 'background-color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'subtitle_bgcolor_hover',
			[
				'label' => __('Subtitle Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .icon-subtitle' => 'background-color: {{VALUE}};',
				],
			]
		);


		$this->end_controls_section();

		$this->start_controls_section(
			'text_settings',
			[
				'label' => __('Text Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'text_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .icon-text',
			]
		);

		$this->add_control(
			'text_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .icon-text' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'text_color_hover',
			[
				'label' => __('Color on hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .icon-text' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'text_margin',
			[
				'label' => __('Margin)', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .icon-text' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->end_controls_section();


		$this->start_controls_section(
			'line_style_settings',
			[
				'label' => __('Line Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'line_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-line' => 'background-color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'line_color_hover',
			[
				'label' => __('Color on hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .cholot-line:after' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'line_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .cholot-line' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'btn_settings',
			[
				'label' => __('Button Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'btn_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .content-btn',
			]
		);

		$this->add_responsive_control(
			'btn_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'btn_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'btn_border_radius',
			[
				'label' => __('Border Radius', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn' => 'border-radius:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'btn_color_section',
			[
				'label' => __('Button Color Scheme Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'btn_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .content-btn' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_bg',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .content-btn::before' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_bg_hover',
			[
				'label' => __('Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .content-btn' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .content-btn::after' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'icon_bordering',
				'placeholder' => '1px',
				'default' => '',
				'selector' => '{{WRAPPER}} .content-btn',
				'separator' => 'before',
			]
		);

		$this->add_responsive_control(
			'btn_border_hover',
			[
				'label' => __('Border on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn:hover' => 'border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);


		$this->add_control(
			'btn_border_color_hover',
			[
				'label' => __('Border Color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn:hover' => 'border-color: {{VALUE}};',
				],
			]
		);


		$this->end_controls_section();

		$this->start_controls_section(
			'content_setting',
			[
				'label' => __('Content Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);
		$this->add_responsive_control(
			'wline_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .text-wline' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);



		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'port_border',
				'placeholder' => '1px',
				'default' => '',
				'selector' => '{{WRAPPER}} .text-wline-inner',
				'separator' => 'before',
			]
		);

		$this->add_control(
			'ct_border_color_hover',
			[
				'label' => __('Border Color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .text-wline-inner' => 'border-color: {{VALUE}};',
				],
			]
		);
		$this->add_responsive_control(
			'wline_margin',
			[
				'label' => __('Border Margin on hover', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .wline-outer' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'wline_bg',
			[
				'label' => __('Content Background', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline .wline-outer' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'wline_hover_bg',
			[
				'label' => __('Content Background on hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .text-wline:hover .wline-outer' => 'background-color: {{VALUE}};',
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
		$this->add_render_attribute('subtitle', 'class', 'box-sub-title');
		$this->add_inline_editing_attributes('title', 'basic');
		$this->add_inline_editing_attributes('subtitle', 'basic');
		$this->add_inline_editing_attributes('text', 'basic');
		$this->add_render_attribute('title', 'class', 'icon-title');
		$this->add_render_attribute('subtitle', 'class', 'icon-subtitle');
		$this->add_render_attribute('text', 'class', 'icon-text');
		$this->add_render_attribute('icon-align', 'class', 'content-btn-align-icon-' . $settings['icon_align']);
		$this->add_render_attribute('icon-align', 'class', 'content-btn-button-icon');
		?>

<div class="text-wline">
    <div class="wline-outer">
        <div class="text-wline-inner">
        </div>
    </div>

    <?php if ($settings['subtitle'] != '') { ?>
    <p <?php echo $this->get_render_attribute_string('subtitle'); ?>><?php echo esc_attr($settings['subtitle']); ?>
    </p>
    <?php } ?>

    <h3 <?php echo $this->get_render_attribute_string('title'); ?>><?php echo $settings['title']; ?></h3>

    <div class="cholot-line clearfix"></div>

    <?php if ($settings['text'] != '') { ?>
    <div <?php echo $this->get_render_attribute_string('text'); ?>><?php echo wp_kses_post($settings['text']); ?>
    </div>
    <?php } ?>



    <?php if ($settings['btn_text'] != '' && $settings['link']['url'] != '') { ?>

    <a class="content-btn" href="<?php echo esc_url($settings['link']['url']); ?>">

        <?php if (!empty($settings['icon_btn'])) : ?>
        <span <?php echo $this->get_render_attribute_string('icon-align'); ?>>
            <i class="<?php echo esc_attr($settings['icon_btn']); ?>" aria-hidden="true"></i>
        </span>
        <?php endif; ?>

        <?php echo esc_attr($settings['btn_text']); ?>
    </a>
    <?php } ?>

</div>
<!--/.box-small-icon-->



<?php }

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