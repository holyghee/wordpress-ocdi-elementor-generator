<?php

namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Box_Shadow;
use Elementor\Utils;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Rdn_Slider extends Widget_Base
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
		return 'rdn-slider';
	}

	//script depend
	public function get_script_depends()
	{
		return ['jquery-slick', 'cholot-animation', 'cholot-slider-script'];
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
		return __('Cholot Slider', 'cholot_plugin');
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
		return 'fa fa-sliders';
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
				'label' => __('Slider Settings', 'cholot_plugin'),
			]
		);



		$slides = new \Elementor\Repeater();

		$slides->add_control(
			'title',
			[
				'label' => __('Slider Heading Title, You can use &lt;span&gt; tag.', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'placeholder' => __('Insert your slider heading title here..', 'cholot_plugin'),
				'default' => __('Slider Heading Title',  'cholot_plugin'),
			]
		);

		$slides->add_control(
			'subtitle',
			[
				'label' => __('Slider Subtitle', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'placeholder' => __('Insert your slider subtitle here..', 'cholot_plugin'),
				'default' => __('Slider Subtitle',  'cholot_plugin'),
			]
		);

		$slides->add_control(
			'text',
			[
				'label' => __('Slider Text', 'cholot_plugin'),
				'type' => Controls_Manager::TEXTAREA,
				'label_block' => true,
				'default' => __('Slider Text',  'cholot_plugin'),
			]
		);

		$slides->add_control(
			'btn_text',
			[
				'label' => __('Button Text', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
			]
		);

		$slides->add_control(
			'btn_link',
			[
				'label' => __('Button Link', 'cholot_plugin'),
				'type' => Controls_Manager::URL,
				'label_block' => true,
				'placeholder' => __('Leave it blank if you don\'t need this button', 'cholot_plugin'),
			]
		);

		$slides->add_control(
			'image',
			[
				'name' => 'image',
				'label' => __('Slider Image', 'cholot_plugin'),
				'type' => Controls_Manager::MEDIA,
				'default' => [
					'url' => Utils::get_placeholder_image_src(),
				],
			]
		);

		
		

		$this->add_control(
			'slider_list',
			[
				'label' => __('Slider List', 'cholot_plugin'),
				'type' => Controls_Manager::REPEATER,
				'default' => [
					[
						'title' => __('Slider Heading Title', 'cholot_plugin'),
						'subtitle' => __('Slider subtitle', 'cholot_plugin'),
						'text' => __('Slider text', 'cholot_plugin'),
					],
					[
						'title' => __('Slider Heading Title', 'cholot_plugin'),
						'subtitle' => __('Slider subtitle', 'cholot_plugin'),
						'text' => __('Slider text', 'cholot_plugin'),
					],
					[
						'title' => __('Slider Heading Title', 'cholot_plugin'),
						'subtitle' => __('Slider subtitle', 'cholot_plugin'),
						'text' => __('Slider text', 'cholot_plugin'),
					],
				],
				'fields' => $slides->get_controls(),
				
				'title_field' => '{{{ title }}}',
			]
		);

		$this->add_responsive_control(
			'slider_width',
			[
				'label' => __('Slider Container Max Width (px)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 100,
						'max' => 4000,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider-box ' => 'max-width: {{SIZE}}px;',
				],
			]
		);

		$this->add_responsive_control(
			'slider_content',
			[
				'label' => __('Slider Content Max Width (px)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 100,
						'max' => 4000,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider-content ' => 'max-width: {{SIZE}}px;',
				],
			]
		);

		$this->add_responsive_control(
			'slider_height',
			[
				'label' => __('Slider Top Padding (%)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 50,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider-box ' => 'padding-top: {{SIZE}}%;',
				],
			]
		);

		$this->add_responsive_control(
			'slider_height_bottom',
			[
				'label' => __('Slider Bottom Padding (%)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 50,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider-box ' => 'padding-bottom: {{SIZE}}%;',
				],
			]
		);

		$this->add_control(
			'slider_speed',
			[
				'label' => __('Slider Speed', 'cholot_plugin'),
				'type' => Controls_Manager::NUMBER,
				'default' => 5000,
				'frontend_available' => true,
			]
		);

		$this->add_control(
			'show_line',
			[
				'label' => __('Show Line', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'show' => __('Show', 'cholot_plugin'),
					'hide' => __('Hide', 'cholot_plugin'),
				],
				'default' => 'show',
			]
		);

		$this->add_control(
			'pos_line',
			[
				'label' => __('Line Position', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'top' => __('Top', 'cholot_plugin'),
					'bottom' => __('Bottom', 'cholot_plugin'),
				],
				'default' => 'bottom',
				'condition' => [
					'show_line' => 'show',
				],
			]

		);

		$this->add_control(
			'show_arrows',
			[
				'label' => __('Show Arrows', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'visible' => __('Show', 'cholot_plugin'),
					'hidden' => __('Hide', 'cholot_plugin'),
				],
				'default' => 'visible',
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow' => 'visibility: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'align',
			[
				'label' => __('Slider Alignment', 'cholot_plugin'),
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
				'default' => 'center',
				'selectors' => [
					'{{WRAPPER}} .slider-box' => 'text-align: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'title_section',
			[
				'label' => __('Slider Title Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'title_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-title' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'title_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-title' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'title_typo',
				'label'     => __('Title Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .slider-title',
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-title' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'title_bgcolor',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-title' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'title_type',
			[
				'label' => __('Title Display', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'block' => __('Block', 'cholot_plugin'),
					'inline-block' => __('Inline Block', 'cholot_plugin'),
				],
				'default' => 'block',
				'selectors' => [
					'{{WRAPPER}} .slider-title' => 'display: {{VALUE}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'span_title_typo',
				'label'     => __('Title Span Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .slider-title span',
			]
		);

		$this->add_control(
			'span_title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-title span' => 'color: {{VALUE}};',
				],
			]
		);


		$this->end_controls_section();



		$this->start_controls_section(
			'subtitle_section',
			[
				'label' => __('Slider Subtitle Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'subtitle_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-subtitle' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_responsive_control(
			'subtitle_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-subtitle' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'subtitle_typo',
				'label'     => __('Subtitle Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .slider-subtitle',
			]
		);

		$this->add_control(
			'subtitle_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-subtitle' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'subtitle_bgcolor',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-subtitle' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'subtitle_type',
			[
				'label' => __('Subtitle Display', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'block' => __('Block', 'cholot_plugin'),
					'inline-block' => __('Inline Block', 'cholot_plugin'),
				],
				'default' => 'block',
				'selectors' => [
					'{{WRAPPER}} .slider-subtitle' => 'display: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'textsetting_section',
			[
				'label' => __('Slider Text Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'text_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-text' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_responsive_control(
			'text_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-text' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'text_typo',
				'label'     => __('Text Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .slider-text',
			]
		);

		$this->add_control(
			'text_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-text' => 'color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'text_bgcolor',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-text' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'text_type',
			[
				'label' => __('Subtitle Display', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'block' => __('Block', 'cholot_plugin'),
					'inline-block' => __('Inline Block', 'cholot_plugin'),
					'none' => __('None', 'cholot_plugin'),
				],
				'default' => 'block',
				'selectors' => [
					'{{WRAPPER}} .slider-text' => 'display: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();



		$this->start_controls_section(
			'sl_line_section',
			[
				'label' => __('Slider Line Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
				'condition' => [
					'show_line' => 'show',
				],
			]
		);

		$this->add_responsive_control(
			'line_width',
			[
				'label' => __('Slider Line Width', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 10,
						'max' => 2000,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider-line ' => 'width: {{SIZE}}px;max-width:100%;',
				],
			]
		);

		$this->add_responsive_control(
			'line_height',
			[
				'label' => __('Slider Line Height', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 10,
						'max' => 500,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider-line ' => 'height: {{SIZE}}px;',
				],
			]
		);

		$this->add_control(
			'linecolor',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-line' => 'background-color: {{VALUE}};',
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
					'{{WRAPPER}} .slider-line' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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

		$this->add_control(
			'icon',
			[
				'label' => __('Button Icon', 'cholot_plugin'),
				'type' => Controls_Manager::ICON,
				'label_block' => true,
				'default' => '',
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
					'icon!' => '',
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
					'icon!' => '',
				],
				'selectors' => [
					'{{WRAPPER}} .slider-btn .content-btn-align-icon-right' => 'margin-left: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .slider-btn .content-btn-align-icon-left' => 'margin-right: {{SIZE}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'btn_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .slider-btn',
			]
		);

		$this->add_responsive_control(
			'btn_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-btn' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .slider-btn' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .slider-btn' => 'border-radius:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Box_Shadow::get_type(),
			[
				'name' => 'button_box_shadow',
				'selector' => '{{WRAPPER}} .slider-btn',
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
					'{{WRAPPER}} .slider-btn' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .slider-btn:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_bg',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .slider-btn' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .slider-btn::before' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_bg_hover',
			[
				'label' => __('Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .slider-btn:hover' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .slider-btn:hover:before' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .slider-btn:hover:after' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'btn_border',
			[
				'label' => __('Border', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-btn' => 'border-style:solid;border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',

				],
			]
		);

		$this->add_responsive_control(
			'btn_border_hover',
			[
				'label' => __('Border on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slider-btn:hover' => 'border-style:solid;border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',

				],
			]
		);

		$this->add_control(
			'btn_border_color',
			[
				'label' => __('Border Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .slider-btn' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_border_color_hover',
			[
				'label' => __('Border Color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .slider-btn:hover' => 'border-color: {{VALUE}};',
				],
			]
		);


		$this->end_controls_section();

		$this->start_controls_section(
			'sl_mask',
			[
				'label' => __('Slider Mask Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'slider_mask',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider-mask' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();


		$this->start_controls_section(
			'sl_arrow',
			[
				'label' => __('Slider Arrows Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
				'condition' => [
					'show_arrows' => 'visible',
				],
			]
		);

		$this->add_responsive_control(
			'arrow_width',
			[
				'label' => __('Slider arrow size', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 10,
						'max' => 400,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow ' => 'width: {{SIZE}}px;height: {{SIZE}}px;line-height: {{SIZE}}px;',
				],
			]
		);
		$this->add_responsive_control(
			'arrow_margin',
			[
				'label' => __('Arrow Margin Bottom', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => -200,
						'max' => 200,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow ' => 'margin-bottom: {{SIZE}}px;',
				],
			]
		);

		$this->add_control(
			'arrow_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow' => 'color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'arrow_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'arrow_bg_color',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'arrow_bg_color_hover',
			[
				'label' => __('Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slider .slick-arrow:hover' => 'background-color: {{VALUE}};',
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
		$this->add_render_attribute('icon-align', 'class', 'content-btn-align-icon-' . $settings['icon_align']);
		$this->add_render_attribute('icon-align', 'class', 'content-btn-button-icon');

		?>


<div class="slider home-slider  ani-slider  clearfix"
    data-slick='{"autoplaySpeed": <?php echo esc_attr($settings['slider_speed']) ?>}'>

    <?php foreach ($settings['slider_list'] as $index => $item) : ?>

    <div class="item slide clearfix">

        <div class="slider-img-bg" data-animation="puffIn" data-delay="0.2s" data-animation-duration="0.7s"
            style="background-image:url(<?php echo esc_url($item['image']['url']); ?>);"></div>

        <div class="slider-mask" data-animation="slideUpReturn" data-delay="0.1s"></div>

        <div class="caption-box clearfix">

            <div class="slider-box container-fluid">
                <div class="slider-content">



                    <?php if ($settings['show_line'] == 'show' && $settings['pos_line'] == 'top') { ?>
                    <div class="slider-line" data-animation="swashIn" data-delay="0.5s"></div>
                    <?php } ?>

                    <?php if ($item['subtitle']) { ?>
                    <p class="slider-subtitle" data-animation="fadeIn" data-delay="1.5s">
                        <?php echo wp_kses_post($item['subtitle']); ?>
                    </p>
                    <div class="clearfix"></div>
                    <?php } ?>

                    <div class="slider-hidden">
                        <h3 class="slider-title" data-animation="fadeInUp" data-delay="0.8s">
                            <?php echo wp_kses_post($item['title']); ?></h3>
                    </div>
                    <!--/.slider-hidden-->


                    <?php if ($settings['show_line'] == 'show' && $settings['pos_line'] == 'bottom') { ?>
                    <div class="slider-line" data-animation="swashIn" data-delay="0.5s"></div>
                    <?php } ?>

                    <?php if ($item['text']) { ?>
                    <p class="slider-text" data-animation="fadeInDown" data-delay="1s">
                        <?php echo wp_kses_post($item['text']); ?>
                    </p>
                    <?php } ?>

                    <?php if ($item['btn_link'] && $item['btn_text']) { ?>
                    <div class="btn-relative" data-animation="swashIn" data-delay="1.8s" data-animation-duration="1s">
                        <?php if (!empty($item['btn_link']['url'])) {
										$link_key = 'link_' . $index;

										$this->add_render_attribute($link_key, 'href', $item['btn_link']['url']);

										if ($item['btn_link']['is_external']) {
											$this->add_render_attribute($link_key, 'target', '_blank');
										}

										if ($item['btn_link']['nofollow']) {
											$this->add_render_attribute($link_key, 'rel', 'nofollow');
										}

										echo '<a class="slider-btn" ' . $this->get_render_attribute_string($link_key) . '>';
									} ?>
                        <?php if (!empty($settings['icon'])) : ?>
                        <span <?php echo $this->get_render_attribute_string('icon-align'); ?>>
                            <i class="<?php echo esc_attr($settings['icon']); ?>" aria-hidden="true"></i>
                        </span>
                        <?php endif; ?>

                        <?php echo esc_attr($item['btn_text']); ?>
                        </a>
                    </div>
                    <!--/.btn-relative-->
                    <?php } ?>

                </div>
                <!--/.slider-content-->
            </div>
            <!--/.slider-box-->



        </div>
        <!--/.caption-box-->
    </div>
    <!--/.slide-->

    <?php

		endforeach;

		?>
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