<?php

namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Text_Shadow;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Title extends Widget_Base
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
		return 'cholot-title';
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
		return __('Cholot Heading', 'cholot_plugin');
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
		return 'fa fa-text-height';
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
				'label' => __('Title', 'cholot_plugin'),
			]
		);

		$this->add_control(
			'title',
			[
				'label' => __('Title. <br/><small>You can use &lt;span&gt;&lt;/span&gt; tag for text color.</small>', 'cholot_plugin'),
				'type' => Controls_Manager::TEXTAREA,
				'placeholder' => __('Enter your title', 'cholot_plugin'),
				'default' => __('This is heading element', 'cholot_plugin'),
			]
		);


		$this->add_control(
			'header_size',
			[
				'label' => __('HTML Tag', 'elementor'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'h1' => __('H1', 'elementor'),
					'h2' => __('H2', 'elementor'),
					'h3' => __('H3', 'elementor'),
					'h4' => __('H4', 'elementor'),
					'h5' => __('H5', 'elementor'),
					'h6' => __('H6', 'elementor'),
					'div' => __('div', 'elementor'),
					'span' => __('span', 'elementor'),
					'p' => __('p', 'elementor'),
				],
				'default' => 'h2',
			]
		);

		$this->add_control(
			'title+display',
			[
				'label' => __('Display', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'block' => __('Block', 'cholot_plugin'),
					'inline-block' => __('Inline-block', 'cholot_plugin'),
				],
				'default' => 'block',
				'selectors' => [
					'{{WRAPPER}} .content-title' => 'display: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'align',
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
					'justify' => [
						'title' => __('Justified', 'cholot_plugin'),
						'icon' => 'fa fa-align-justify',
					],
				],
				'default' => '',
				'selectors' => [
					'{{WRAPPER}}' => 'text-align: {{VALUE}};',
				],
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'section_title_style',
			[
				'label' => __('Title.', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Text Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-title' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'title_bg_color',
			[
				'label' => __('Text Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-title' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'title_margin',
			[
				'label' => __('Margin)', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-title' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'title_padding',
			[
				'label' => __('Padding)', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-title' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'desc_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .content-title',
			]
		);

		$this->add_group_control(
			Group_Control_Text_Shadow::get_type(),
			[
				'name' => 'text_shadow',
				'selector' => '{{WRAPPER}} .content-title',
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'span_title_typo',
				'label'     => __('Title Span Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .content-title span',
			]
		);

		$this->add_control(
			'span_title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .content-title span' => 'color: {{VALUE}};',
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

		if (empty($settings['title'])) {
			return;
		}

		$this->add_render_attribute('title', 'class', 'content-title');


		$this->add_inline_editing_attributes('title');

		$title = $settings['title'];

		$title_html = sprintf('<%1$s %2$s>%3$s</%1$s>', $settings['header_size'], $this->get_render_attribute_string('title'), $title);

		echo $title_html;
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