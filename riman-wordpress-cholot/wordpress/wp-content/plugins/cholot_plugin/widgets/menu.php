<?php

namespace CholotPlugin\Widgets;

use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Menu extends Widget_Base
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
		return 'cholot-menu';
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
		return __('Cholot Menu', 'cholot_plugin');
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
		return 'fa fa-th-large';
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
		return ['cholot-menu-elements'];
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
				'label' => __('Menu to Display', 'cholot_plugin'),
			]
		);

		$this->add_control(
			'cholot_menu',
			[
				'label'   => __('Select Menu', 'cholot_plugin'),
				'type'    => Controls_Manager::SELECT, 'options' => navmenu_navbar_menu_choices(),
				'default' => '',
			]
		);


		$this->add_control(
			'menu_type',
			[
				'label' => __('Drop Down Type', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'left' => __('From Left', 'cholot_plugin'),
					'right' => __('From Right', 'cholot_plugin'),
				],
				'default' => 'left',
			]
		);

		$this->add_responsive_control(
			'align',
			[
				'label' => __('Parent Menu Alignment', 'cholot_plugin'),
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
					'{{WRAPPER}} .white-header' => 'text-align: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'align_child',
			[
				'label' => __('Child Menu Alignment', 'cholot_plugin'),
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
					'{{WRAPPER}} .menu-box ul li ul' => 'text-align: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'desktop_menu',
			[
				'label' => __('Desktop Menu', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'inline-block' => __('Show', 'cholot_plugin'),
					'none' => __('Hide', 'cholot_plugin'),
				],
				'default' => 'inline-block',
				'label_block' => true,
				'selectors' => [
					'{{WRAPPER}} .menu-box' => 'display: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'mobile_menu',
			[
				'label' => __('Mobile Menu', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'inline-block' => __('Show', 'cholot_plugin'),
					'none' => __('Hide', 'cholot_plugin'),
				],
				'default' => 'inline-block',
				'label_block' => true,
				'selectors' => [
					'{{WRAPPER}} .box-mobile' => 'display: {{VALUE}};',
				],
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'menu_section',
			[
				'label' => __('Menu Settings (parent)', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'menu_margin',
			[
				'label' => __('Margin ', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'border_type',
			[
				'label' => __('Boder Type', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'none' => __('None', 'cholot_plugin'),
					'solid' => __('Solid', 'cholot_plugin'),
					'dotted' => __('Dotted', 'cholot_plugin'),
					'double' => __('Double', 'cholot_plugin'),
					'dashed' => __('Dashed', 'cholot_plugin'),

				],
				'default' => 'none',
				'label_block' => true,
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li > a' => 'border-style: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'menu_border',
			[
				'label' => __('Border ', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li > a' => 'border-width: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'menu_border_radius',
			[
				'label' => __('Border Radius ', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li > a' => 'border-radius: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'menu_border_color',
			[
				'label' => __('Border Color ', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li > a' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'menu_border_color_hover',
			[
				'label' => __('Border Color on Hover ', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li > a:hover' => 'border-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'menu_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li >a' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'menu_typo',
				'label'     => __('Title Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .menu-box >div>ul> li> a',
			]
		);

		$this->add_control(
			'menu_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_bg',
			[
				'label' => __('Background', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> a' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_bg_hover',
			[
				'label' => __('Background on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_in_opacity',
			[
				'label' => __('Opacity', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1,
						'step' => 0.1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> a' => 'opacity: {{SIZE}};',
				],
			]
		);

		$this->add_control(
			'opacity_hover',
			[
				'label' => __('Opacity on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1,
						'step' => 0.1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> a:hover' => 'opacity: {{SIZE}};',
					'{{WRAPPER}} .menu-box >div>ul.navigation > .current_page_item > a' =>  'opacity: {{SIZE}};',
					'{{WRAPPER}} .menu-box >div>ul.navigation > .current-menu-parent > a' =>  'opacity: {{SIZE}};',
				],
			]
		);

		$this->add_control(
			'menu_stick_color',
			[
				'label' => __('Color on Sticky Menu', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>.cholot-stick> li> a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_stick_color_hover',
			[
				'label' => __('Color on Sticky Menu (hover)', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}}  .menu-box >div>.cholot-stick> li> a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'menu_child_section',
			[
				'label' => __('Menu Settings (dropdown)', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);


		$this->add_control(
			'child_margin',
			[
				'label' => __('Top Margin (dropdown parent only)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 100,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul > li > ul' => 'margin-top: {{SIZE}}{{UNIT}};',
				],
			]
		);


		$this->add_responsive_control(
			'menu_child_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul li  ul li a' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'menu_child_typo',
				'label'     => __('Title Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .menu-box >div>ul> li> ul li a',
			]
		);

		$this->add_responsive_control(
			'box_child_padding',
			[
				'label' => __('Box Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .menu-box ul li ul' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_control(
			'menu_box_color',
			[
				'label' => __('Box Background color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box ul li ul' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_child_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> ul li a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_child_color_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> ul li a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_child_bg',
			[
				'label' => __('Background', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> ul li a' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'menu_child_bg_hover',
			[
				'label' => __('Background on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> ul li a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'opacity',
			[
				'label' => __('Opacity', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1,
						'step' => 0.1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> ul li a' => 'opacity: {{SIZE}};',
				],
			]
		);

		$this->add_control(
			'slider_opacity_hover',
			[
				'label' => __('Opacity on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1,
						'step' => 0.1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .menu-box >div>ul> li> ul li a:hover' => 'opacity: {{SIZE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'menumobile_section',
			[
				'label' => __('Mobile Menu Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'hamb_color',
			[
				'label' => __('Hamburger Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slicknav_icon-bar' => 'background-color: {{VALUE}};',
				],
			]

		);

		$this->add_control(
			'hab_stick',
			[
				'label' => __('Hamburger Color on Sticky Menu', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .cholot-stick .slicknav_icon-bar' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'hamb_margin',
			[
				'label' => __('Hamburger Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slicknav_icon.slicknav_no-text' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'hamb_padding',
			[
				'label' => __('Hamburger Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .slicknav_icon.slicknav_no-text' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'child_menu_mobile_margin',
			[
				'label' => __('Child Menu (when opened) Position', 'cholot_plugin'),
				'size_units' => ['px', '%'],
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 200,
						'step' => 1,
					],
					'%' => [
						'min' => 0,
						'max' => 200,
						'step' => 1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .custom-mb-menu .slicknav_nav' => 'top: {{SIZE}}{{UNIT}};',
				],
			]
		);


		$this->add_control(
			'fat_nav_bg',
			[
				'label' => __('Mobile Menu Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slicknav_nav' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mobile_color',
			[
				'label' => __('Link Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slicknav_nav a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mobile_color_hover',
			[
				'label' => __('Link Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slicknav_nav a:hover' => 'color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'mobile_bg_hover',
			[
				'label' => __('Link Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .slicknav_nav a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mobile_the_child_color',
			[
				'label' => __('The Child Menu (when opened)  Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} ul .slicknav_open ul a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mobile_the_child_color_hover',
			[
				'label' => __('The Child Menu (when opened) Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} ul .slicknav_open ul a:hover' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mobile_bg_child',
			[
				'label' => __('The Child Menu (when opened)  Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} ul .slicknav_open ul' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mobile_bg_child_hover',
			[
				'label' => __('The Child Menu (when opened) Background Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} ul .slicknav_open ul a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'mobile_padding_text',
			[
				'label' => __('Link Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .fat-nav li a' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};display:block;',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'mobile_typo',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .fat-nav li a',
			]
		);


		$this->add_responsive_control(
			'mobile_align',
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
					'{{WRAPPER}} .fat-nav li' => 'text-align: {{VALUE}};',
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

<!--HEADER START-->

<div class="white-header no-bg">
    <div class="menu-box <?php if ($settings['menu_type'] == 'right') {
									echo 'cholot-right-menu';
								} else {
									echo 'cholot-left-menu';
								} ?> ">
        <?php wp_nav_menu(array('menu' => $settings['cholot_menu'], 'items_wrap' => '<ul id="%1$s" class="cholot-nav navigation %2$s">%3$s</ul>')); ?>
    </div>
    <!--/.menu-box-->
    <!--/.box-header-->
    <div class="box-mobile">
        <div class="mobile-menu-container custom-mb-menu">
        </div>
    </div>
    <!--/.box-mobile-->
</div>




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