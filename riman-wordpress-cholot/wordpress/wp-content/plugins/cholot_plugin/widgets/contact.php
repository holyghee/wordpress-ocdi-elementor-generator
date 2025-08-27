<?php

namespace cholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class cholot_Contact extends Widget_Base
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
		return 'cholot-contact';
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
		return __('Cholot Contact Form Shortcode', 'cholot_plugin');
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
		return 'fa fa-wpforms';
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
			'shortcode',
			[
				'label' => __('Insert your contact form shortcode here', 'cholot_plugin'),
				'type' => Controls_Manager::TEXTAREA,
				'placeholder' => '[contact-form-7 id="95" title="Contact Form"]',
				'default' => '',
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'form_settings',
			[
				'label' => __('Form Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'form_placeholder',
			[
				'label' => __('Placeholder Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} ::-webkit-input-placeholder' => 'color: {{VALUE}};',
					'{{WRAPPER}} ::-moz-placeholder' => 'color: {{VALUE}};',
					'{{WRAPPER}} :-ms-input-placeholder' => 'color: {{VALUE}};',
					'{{WRAPPER}} :-moz-placeholder' => 'color: {{VALUE}};',
				],
			]
		);


		$this->add_control(
			'form_text',
			[
				'label' => __('Text Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}}  input:not(.wpcf7-submit) ' => 'color: {{VALUE}};',
					'{{WRAPPER}} textarea' => 'color: {{VALUE}};',
					'{{WRAPPER}} .wpcf7 select' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'form_bg',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}}  input' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} textarea' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .wpcf7 select' => 'background-color: {{VALUE}};',
				],
			]
		);


		$this->add_control(
			'form_border_color',
			[
				'label' => __('Border Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}}  input' => 'border-color: {{VALUE}};',
					'{{WRAPPER}} textarea' => 'border-color: {{VALUE}};',
					'{{WRAPPER}} .wpcf7 select' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'form_border_color_active',
			[
				'label' => __('Border Color on Focus', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} input:focus' => 'border-color: {{VALUE}};',
					'{{WRAPPER}} textarea:focus' => 'border-color: {{VALUE}};',
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
				'selector'  => '{{WRAPPER}} .wpcf7-submit',
			]
		);

		$this->add_control(
			'btn_width',
			[
				'type' => Controls_Manager::SELECT,
				'label'     => __('Width', 'cholot_plugin'),
				'options' => [
					'auto' => __('Narrow', 'cholot_plugin'),
					'100%' => __('Fullwidth', 'cholot_plugin'),
				],
				'default' => 'auto',
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit' => 'width:{{VALUE}};',
				],
			]
		);


		$this->add_responsive_control(
			'btn_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .wpcf7-submit' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .wpcf7-submit' => 'border-radius:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .wpcf7-submit' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_bg',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .wpcf7-submit::before' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_bg_hover',
			[
				'label' => __('Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit:hover' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .wpcf7-submit::after' => 'background-color: {{VALUE}};',
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
					'{{WRAPPER}} .wpcf7-submit' => 'border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .wpcf7-submit:hover' => 'border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'btn_border_color',
			[
				'label' => __('Border Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_border_color_hover',
			[
				'label' => __('Border Color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .wpcf7-submit:hover' => 'border-color: {{VALUE}};',
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

		$shortcode = $this->get_settings('shortcode');

		$shortcode = do_shortcode(shortcode_unautop($shortcode));
		?>
	<div class="cholot-contact-shortcode"><?php echo $shortcode; ?></div>
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
