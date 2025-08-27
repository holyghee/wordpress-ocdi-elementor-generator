<?php

namespace CholotPlugin\Widgets;

use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Group_Control_Box_Shadow;
use Elementor\Group_Control_Border;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_PostThree extends Widget_Base
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
		return 'cholot-post-three';
	}

	//script depend
	public function get_script_depends()
	{
		return ['jquery-isotope', 'cholot-blog-masonry'];
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
		return __('Cholot Post List Style 3', 'cholot_plugin');
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
		return 'fa fa-newspaper-o';
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
		return ['cholot-blog-elements'];
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
				'label' => __('Blog Post Settings', 'cholot_plugin'),
			]
		);



		$this->add_control(
			'blog_post',
			[
				'label' => __('Blog Post to show', 'cholot_plugin'),
				'type' => Controls_Manager::NUMBER,
				'default' => '6',

			]
		);

		$this->add_control(
			'sort_cat',
			[
				'label' => __('Sort post by Category', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => 'no',
				'label_on' => __('Yes', 'cholot_plugin'),
				'label_off' => __('No', 'cholot_plugin'),
				'return_value' => 'yes',
			]
		);

		$this->add_control(
			'blog_cat',
			[
				'label'   => __('Category', 'cholot_plugin'),
				'type'    => Controls_Manager::SELECT2, 'options' => category_choice(),
				'condition' => [
					'sort_cat' => 'yes',
				],
				'multiple'   => 'true',
			]
		);

		$this->add_control(
			'paged_on',
			[
				'label' => __('Always show the same list on every page(not paged).', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => '',
				'label_on' => __('Yes', 'cholot_plugin'),
				'label_off' => __('No', 'cholot_plugin'),
				'return_value' => 'yes',
			]
		);

		$this->add_control(
			'show_excerpt',
			[
				'label' => __('Show Exerpt', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => 'yes',
				'label_on' => __('Show', 'cholot_plugin'),
				'label_off' => __('Hide', 'cholot_plugin'),
				'return_value' => 'yes',
			]
		);

		$this->add_control(
			'excerpt',
			[
				'label' => __('Blog Excerpt Length', 'cholot_plugin'),
				'type' => Controls_Manager::NUMBER,
				'default' => '150',
				'min' => 10,
				'condition' => [
					'show_excerpt' => 'yes',
				],
			]
		);

		$this->add_control(
			'excerpt_after',
			[
				'label' => __('After Excerpt text/symbol', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'condition' => [
					'show_excerpt' => 'yes',
				],
				'default' => '...',
			]
		);

		$this->add_control(
			'blog_column',
			[
				'label' => __('Blog Columns', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'one' => __('One Column', 'cholot_plugin'),
					'two' => __('Two Columns', 'cholot_plugin'),
					'three' => __('Three Columns', 'cholot_plugin'),
					'four' => __('Four Columns', 'cholot_plugin'),
				],
				'default' => 'two',
			]
		);


		$this->add_control(
			'button_show',
			[
				'label' => __('Show Button', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => '',
				'label_on' => __('Show', 'cholot_plugin'),
				'label_off' => __('Hide', 'cholot_plugin'),
				'return_value' => 'yes',
			]
		);

		$this->add_control(
			'button',
			[
				'label' => __('Button Text', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'default' => __('Read More', 'cholot_plugin'),
				'label_block' => true,
				'condition' => [
					'button_show' => 'yes',
				],
			]
		);
		$this->add_control(
			'icon',
			[
				'label' => __('Button Icon', 'cholot_plugin'),
				'type' => Controls_Manager::ICON,
				'label_block' => true,
				'default' => '',
				'condition' => [
					'button_show' => 'yes',
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
					'button_show' => 'yes',
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
					'button_show' => 'yes',
					'icon!' => '',
				],
				'selectors' => [
					'{{WRAPPER}} .content-btn .content-btn-align-icon-right' => 'margin-left: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .content-btn .content-btn-align-icon-left' => 'margin-right: {{SIZE}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'meta_show',
			[
				'label' => __('Show Post Meta', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => 'yes',
				'label_on' => __('Show', 'cholot_plugin'),
				'label_off' => __('Hide', 'cholot_plugin'),
				'return_value' => 'yes',
			]
		);

		$this->add_control(
			'cat_show',
			[
				'label' => __('Show Post Category', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => 'yes',
				'label_on' => __('Show', 'cholot_plugin'),
				'label_off' => __('Hide', 'cholot_plugin'),
				'return_value' => 'yes',
			]
		);

		$this->add_control(
			'colors_warning',
			[
				'type' =>  Controls_Manager::RAW_HTML,
				'raw' => __('<b>Note:</b> Try to show pagination only for (single) blog page.', 'cholot_plugin'),
				'content_classes' => 'elementor-panel-alert elementor-panel-alert-warning',
				'condition' => [
					'paged_on' => '',
				],
			]
		);

		$this->add_control(
			'page_show',
			[
				'label' => __('Show Pagination', 'cholot_plugin'),
				'type' => Controls_Manager::SWITCHER,
				'default' => '',
				'label_on' => __('Show', 'cholot_plugin'),
				'label_off' => __('Hide', 'cholot_plugin'),
				'return_value' => 'yes',
				'condition' => [
					'paged_on' => '',
				],
			]
		);

		$this->add_control(
			'width_warning',
			[
				'type' =>  Controls_Manager::RAW_HTML,
				'raw' => __('<b>Note:</b> Make sure Image Area + Content Area width is 100%.', 'cholot_plugin'),
				'content_classes' => 'elementor-panel-alert elementor-panel-alert-warning',
			]
		);

		$this->add_responsive_control(
			'image_width',
			[
				'label' => __('Image Area Width (%)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 100,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .blog-style-three .blog-link-img' => 'width: {{SIZE}}%;',
				],
			]
		);

		$this->add_responsive_control(
			'content_width',
			[
				'label' => __('Content Area Width (%)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 100,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .blog-style-three .excerpt-box' => 'width: {{SIZE}}%;',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'title_section',
			[
				'label' => __('Title Settings', 'cholot_plugin'),
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
					'{{WRAPPER}} .blog-post-list h3' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'title_typo',
				'label'     => __('Title Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .blog-post-list h3',
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .blog-post-list h3' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'title_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .blog-post-list h3:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'text_section',
			[
				'label' => __('Text Settings', 'cholot_plugin'),
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
					'{{WRAPPER}} .blog-post-list p' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'text_typo',
				'label'     => __('Text Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .blog-post-list p',
			]
		);

		$this->add_control(
			'text_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .blog-post-list p' => 'color: {{VALUE}};',
				],
			]
		);


		$this->end_controls_section();

		$this->start_controls_section(
			'meta_section',
			[
				'label' => __('Post Meta Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
				'condition' => [
					'meta_show' => 'yes',
				],
			]
		);

		$this->add_responsive_control(
			'meta_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .post-meta' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'meta_typo',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .post-meta',
			]
		);

		$this->add_control(
			'meta_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .post-meta' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'meta_link',
			[
				'label' => __('Link Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .post-meta a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'meta_link_hover',
			[
				'label' => __('Link Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .post-meta a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'meta_icon',
			[
				'label' => __('Icon Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .post-meta .fa' => 'color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'cat_section_setting',
			[
				'label' => __('Post Category Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
				'condition' => [
					'cat_show' => 'yes',
				],
			]
		);

		$this->add_responsive_control(
			'cat_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .box-cat-post' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'cat_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .box-cat-post' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'cat_typo',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .box-cat-post',
			]
		);

		$this->add_control(
			'cat_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .box-cat-post' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'cat_bg',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .box-cat-post' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'btn_settings',
			[
				'label' => __('Button Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
				'condition' => [
					'button_show' => 'yes',
				],
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
				'condition' => [
					'button_show' => 'yes',
				],
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
					'{{WRAPPER}} .content-btn:hover' => 'color: {{VALUE}};',
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
					'{{WRAPPER}} .content-btn:hover' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .content-btn::after' => 'background-color: {{VALUE}};',
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
					'{{WRAPPER}} .content-btn' => 'border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .content-btn:hover' => 'border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'btn_border_color',
			[
				'label' => __('Border Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn' => 'border-color: {{VALUE}};',
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

		$this->add_group_control(
			Group_Control_Box_Shadow::get_type(),
			[
				'name' => 'box_shadow',
				'selector' => '{{WRAPPER}} .content-btn',
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'pagination_setting',
			[
				'label' => __('Pagination Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'pagi-align',
			[
				'label' => __('Pagination Alignment', 'gehou_plg'),
				'type' => Controls_Manager::CHOOSE,
				'options' => [
					'left' => [
						'title' => __('Left', 'gehou_plg'),
						'icon' => 'fa fa-align-left',
					],
					'center' => [
						'title' => __('Center', 'gehou_plg'),
						'icon' => 'fa fa-align-center',
					],
					'right' => [
						'title' => __('Right', 'gehou_plg'),
						'icon' => 'fa fa-align-right',
					],
				],
				'selectors' => [
					'{{WRAPPER}} .pagination' => 'text-align: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'pagi_border_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .pagination li a' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'pagi_border_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .pagination li a' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'page_border',
				'placeholder' => '1px',
				'default' => '1px',
				'selector' => '{{WRAPPER}} .pagination li a',
				'separator' => 'before',
			]
		);
		$this->add_responsive_control(
			'pagi_border_radius',
			[
				'label' => __('Border Radius', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .pagination li a' => 'border-radius:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'page_color',
			[
				'label' => __('Pagination Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .pagination > li > a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'page_color_hover',
			[
				'label' => __('Pagination Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .pagination > li > a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'page_color_bg',
			[
				'label' => __('Pagination Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .pagination > li > a' => 'background-color: {{VALUE}};border-color:{{VALUE}};',
				],
			]
		);

		$this->add_control(
			'page_color_hover_bg',
			[
				'label' => __('Pagination Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .pagination > li > a:hover' => 'background-color: {{VALUE}};border-color:{{VALUE}};',
				],
			]
		);

		$this->add_control(
			'page_color_active',
			[
				'label' => __('Pagination Color on Active', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .pagination > .active > a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'page_color_hover_bg_active',
			[
				'label' => __('Pagination Background Color on Active', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .pagination > .active > a' => 'background-color: {{VALUE}};border-color:{{VALUE}};',
					'{{WRAPPER}} .pagination > .active > a:hover' => 'background-color: {{VALUE}};border-color:{{VALUE}};',
				],
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'content_padding_setting',
			[
				'label' => __('Text & Button Content Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'content_bg',
			[
				'label' => __('Background', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .excerpt-box' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'excerpt_padding_box',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .excerpt-box' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'excerpt_pmargin_box',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .blog-style-three' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Box_Shadow::get_type(),
			[
				'name' => 'boxbutton_shadow',
				'selector' => '{{WRAPPER}} .blog-col-inner',
			]
		);


		$this->end_controls_section();

		$this->start_controls_section(
			'image_settings',
			[
				'label' => __('Image Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'image_border',
				'placeholder' => '1px',
				'default' => '',
				'selector' => '{{WRAPPER}} .blog-imgbg ',
				'separator' => 'before',
			]
		);

		$this->add_control(
			'img_hover_border',
			[
				'label' => __('Border Color on hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .blog-col-inner:hover .blog-imgbg' => 'border-color: {{VALUE}};',
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
		if ($settings['paged_on']  != 'yes') {
			$cholot_paged = (get_query_var('paged')) ? get_query_var('paged') : 1;
		} else {
			$cholot_paged = '';
		}
		if ($settings['sort_cat']  == 'yes') {
			$query = new \WP_Query(array(
				'posts_per_page'   => $settings['blog_post'],
				'paged' => $cholot_paged,
				'post_type' => 'post',
				'cat' => $settings['blog_cat']

			));
		} else {
			$query = new \WP_Query(array(
				'posts_per_page'   => $settings['blog_post'],
				'paged' => $cholot_paged,
				'post_type' => 'post'
			));
		}

		$this->add_render_attribute('icon-align', 'class', 'content-btn-align-icon-' . $settings['icon_align']);
		$this->add_render_attribute('icon-align', 'class', 'content-btn-button-icon');

		?>
<div class="blog-post-list row clearfix blog-body">
    <?php while ($query->have_posts()) : $query->the_post(); ?>
    <div class="<?php if ($settings['blog_column'] == 'one') {
							echo "col-md-12";
						} else if ($settings['blog_column'] == 'two') {
							echo "col-md-6";
						}
						if ($settings['blog_column'] == 'three') {
							echo "col-md-4";
						}
						if ($settings['blog_column'] == 'four') {
							echo "col-md-3";
						} ?>">
        <div class="blog-col-inner blog-style-three">
            <?php if (has_post_thumbnail()) { ?>
            <a class="blog-link-img blog-imgbg" href="<?php the_permalink(); ?>"
                style="background-image:url(<?php echo get_the_post_thumbnail_url(); ?>)">

                <?php if ($settings['cat_show'] == 'yes') { ?>
                <div class="box-cat-post cat-absolute">
                    <?php $cat = '';
									foreach ((get_the_category()) as $category) {
										$cat .= $category->cat_name . ', ';
									}
									echo rtrim($cat, ', '); ?>
                </div>
                <?php } ?>

                <div class="blogmask"></div>
            </a>
            <?php } else { ?>
            <a class="blog-link-img blog-imgbg" href="<?php the_permalink(); ?>"
                style="background-image:url(<?php echo CHOLOT_URL ?>images/no-image.jpg)">

                <?php if ($settings['cat_show'] == 'yes') { ?>
                <div class="box-cat-post cat-absolute">
                    <?php $cat = '';
									foreach ((get_the_category()) as $category) {
										$cat .= $category->cat_name . ', ';
									}
									echo rtrim($cat, ', '); ?>
                </div>
                <?php } ?>

                <div class="blogmask"></div>
            </a>
            <?php } ?>



            <div class="excerpt-box">
                <a href="<?php the_permalink(); ?>">
                    <h3><?php the_title(); ?></h3>
                </a>

                <?php if ($settings['meta_show'] == 'yes') { ?>
                <ul class="post-meta">
                    <li><i class="fa fa-user"></i> <?php the_author_posts_link(); ?></li>
                    <li><i class="fa fa-clock-o"></i> <?php echo get_the_date();  ?></li>
                </ul>
                <?php } ?>

                <?php if ($settings['show_excerpt'] == 'yes') { ?>
                <p>
                    <?php $excerpt = get_the_excerpt();
								$excerpt = substr($excerpt, 0, $settings['excerpt']);
								echo $excerpt;
								echo esc_attr($settings['excerpt_after']) ?>
                </p>
                <?php } ?>

                <?php if ($settings['show_excerpt'] == 'yes' && $settings['button_show'] != 'yes') { ?>
                <div class="spacing20 clearfix"></div>
                <?php } ?>

                <?php if ($settings['button_show'] == 'yes') { ?>
                <div class="spacing20 clearboth"></div>
                <a class="content-btn" href="<?php the_permalink(); ?>">

                    <?php if (!empty($settings['icon'])) : ?>
                    <span <?php echo $this->get_render_attribute_string('icon-align'); ?>>
                        <i class="<?php echo esc_attr($settings['icon']); ?>" aria-hidden="true"></i>
                    </span>
                    <?php endif; ?>

                    <?php echo esc_attr($settings['button']); ?>
                </a>
                <?php  } ?>
            </div>

        </div>
    </div>

    <?php endwhile;
		wp_reset_postdata(); ?>
</div>

<!--pagination-->
<?php if ($settings['paged_on']  != 'yes') {
		if ($settings['page_show'] == 'yes') {
			cholot_pagination($query->max_num_pages);
		}
	}
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
protected function cholot_custom_pagination()
{ }
}