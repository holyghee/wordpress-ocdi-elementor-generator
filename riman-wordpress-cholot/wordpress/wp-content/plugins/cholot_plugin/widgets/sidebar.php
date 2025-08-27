<?php

namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Box_Shadow;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Sidebar extends Widget_Base
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
		return 'cholot-sidebar';
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
		return __('Cholot Sidebar', 'cholot_plugin');
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
		return 'fa fa-ellipsis-v';
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
	 * Adds different input:not(#searchsubmit) fields to allow the user to change and customize the widget settings.
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
			'colors_warning',
			[
				'type' =>  Controls_Manager::RAW_HTML,
				'raw' => __('<b>Note:</b> You need to set the widget to display in sidebar first in widgets page.', 'cholot_plugin'),
				'content_classes' => 'elementor-panel-alert elementor-panel-alert-warning',
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
				'label' => __('Widget Title', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .widgettitle' => 'color: {{VALUE}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'title_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .widgettitle',
			]
		);

		$this->add_responsive_control(
			'title_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .widgettitle' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
					'{{WRAPPER}} .widgettitle' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->end_controls_section();

		$this->start_controls_section(
			'widget_boder',
			[
				'label' => __('Title Divider Style', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'divider_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .widget-border' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_control(
			'height',
			[
				'label' => __('Height', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 50,
						'step' => 1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .widget-border' => 'height: {{SIZE}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'width',
			[
				'label' => __('Width', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'size_units' => ['px', '%'],
				'range' => [
					'px' => [
						'min' => 5,
						'max' => 500,
						'step' => 1,
					], '%' => [
						'min' => 0,
						'max' => 100,
						'step' => 1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .widget-border' => 'width: {{SIZE}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'divier_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .widget-border' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'section_text_style',
			[
				'label' => __('Widget Text', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'text_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'text_color_link',
			[
				'label' => __('Link Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'text_color_link_hover',
			[
				'label' => __('Link Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar a:hover' => 'color: {{VALUE}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .cholot-sidebar',
			]
		);


		$this->end_controls_section();

		$this->start_controls_section(
			'section_widget_content',
			[
				'label' => __('Widget Content', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'widget_bg',
			[
				'label' => __('Background', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .widget' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'widget_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .widget' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'widget_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .widget' => 'marghin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Box_Shadow::get_type(),
			[
				'name' => 'box_shadow',
				'selector' => '{{WRAPPER}} .widget',
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'search_bar_style',
			[
				'label' => __('Search Widget Style', 'cholot_plugin'),
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
					'{{WRAPPER}}  input:not(#searchsubmit)' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'form_bg',
			[
				'label' => __('Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}}  input:not(#searchsubmit)' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'form_border_color',
			[
				'label' => __('Border Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}}  input:not(#searchsubmit)' => 'border-color: {{VALUE}};',
					'{{WRAPPER}} textarea' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'form_border_color_active',
			[
				'label' => __('Border Color on Focus', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} input:not(#searchsubmit):focus' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'form_border',
			[
				'label' => __('Border', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} input:not(#searchsubmit)' => 'border-width:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'form_border_radius',
			[
				'label' => __('Border Radius', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} input:not(#searchsubmit)' => 'border-radius:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'form_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} input:not(#searchsubmit)' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};height:auto;',
				],
			]
		);

		$this->add_responsive_control(
			'form_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} input:not(#searchsubmit)' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'search_btn',
			[
				'label' => __('Button Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} #searchsubmit' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'search_btn_hover',
			[
				'label' => __('Button Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} #searchsubmit:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'tag_cloud_style',
			[
				'label' => __('Tag Cloud Widget Style', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'tag_color_link',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'tag_color_link_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'tag_color_link_bg',
			[
				'label' => __('Background', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud a' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'tag_color_link_hover_bg',
			[
				'label' => __('Background on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'tagboder_color_link',
			[
				'label' => __('Border Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud a' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'tagboder_color_link_hover',
			[
				'label' => __('Border Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a:hover' => 'border-color: {{VALUE}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'tag_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .cholot-sidebar .tagcloud  a',
			]
		);

		$this->add_responsive_control(
			'tag_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'tag__margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'tag__border',
			[
				'label' => __('Border', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a' => 'border-width: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'tag__border_radius',
			[
				'label' => __('Border Radius', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .cholot-sidebar .tagcloud  a' => 'border-radius: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
		$settings = $this->get_settings(); ?>
<!--SIDEBAR START-->
<div class="cholot-sidebar sidebar clearfix">
    <?php if (function_exists('dynamic_sidebar')) {
			if (is_active_sidebar('default-sidebar')) {
				dynamic_sidebar('default-sidebar');
			}
		} ?>
</div>
<!--/.sidebar-->
<!--SIDEBAR END-->
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