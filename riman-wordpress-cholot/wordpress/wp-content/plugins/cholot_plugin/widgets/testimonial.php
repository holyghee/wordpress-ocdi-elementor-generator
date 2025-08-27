<?php

namespace CholotPlugin\Widgets;

use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Utils;
use Elementor\Repeater;
use Elementor\Group_Control_Image_Size;
use Elementor\Group_Control_Border;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Testimonial extends Widget_Base
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
		return 'cholot-testimonial';
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
		return __('Cholot Testimonial', 'cholot_plugin');
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
		return 'fa fa-quote-right';
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
				'label' => __('Testimonial Settings', 'cholot_plugin'),
			]
		);

		$testi = new \Elementor\Repeater();

		$testi->add_control(
			'title',
			[
				'label' => __('Testimonial Name', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'placeholder' => __('Testimonial Name..', 'cholot_plugin'),
			]
		);



		$testi->add_control(
			'text',
			[
				'label' => __('Testimonial Text', 'cholot_plugin'),
				'type' => Controls_Manager::TEXTAREA,
				'label_block' => true,
				'placeholder' => __('Testimonial Text..', 'cholot_plugin'),
			]
		);

		$testi->add_control(
			'position',
			[
				'label' => __('Testimonial Position', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'placeholder' => __('Testimonial Position..', 'cholot_plugin'),
			]
		);

		$testi->add_control(
			'image',
			[
				'label' => __('Team Image', 'cholot_plugin'),
				'type' => Controls_Manager::MEDIA,
				'default' => [
					'url' => Utils::get_placeholder_image_src(),
				],
			]
		);

		$testi->add_group_control(
			Group_Control_Image_Size::get_type(),
			[
				'name' => 'image2', // Usage: `{name}_size` and `{name}_custom_dimension`, in this case `image_size` and `image_custom_dimension`.
				'default' => 'large',
				'separator' => 'none',
			]
		);
		$this->add_control(
			'testi_list',
			[
				'label' => __('Testimonial List', 'cholot_plugin'),
				'type' => Controls_Manager::REPEATER,
				'default' => [
					[
						'title' => 'Testimonial Name',
						'position' => 'Testimonial Position',
						'text' => 'Testimonial Text',
					],
					[
						'title' => 'Testimonial Name',
						'position' => 'Testimonial Position',
						'text' => 'Testimonial Text',
					],
					[
						'title' => 'Testimonial Name',
						'position' => 'Testimonial Position',
						'text' => 'Testimonial Text',
					],
				],
				'fields' => $testi->get_controls(),
				'title_field' => '{{ title }}',
			]
		);
		$this->end_controls_section();

		$this->start_controls_section(
			'title_settting',
			[
				'label' => __('Text Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .testimonial .testi-text' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'title_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .testimonial .testi-text',
			]
		);

		$this->end_controls_section();


		$this->start_controls_section(
			'name_settings',
			[
				'label' => __('Name Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'name_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .testimonial h3' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'name_typography',
				'label'     => __('Name Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .testimonial h3',
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'post_settting',
			[
				'label' => __('Position Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_control(
			'post_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .testimonial .testi-from' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'post_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .testimonial .testi-from',
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'image_setting',
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
				'selector' => '{{WRAPPER}} .testi-img',
				'separator' => 'before',
			]
		);

		$this->add_responsive_control(
			'img_size',
			[
				'label' => __('Image Size', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 200,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .testi-img' => 'width: {{SIZE}}{{UNIT}};',
				],
			]
		);



		$this->add_responsive_control(
			'img_radius',
			[
				'label' => __('Border Radius', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .testi-img' => 'border-radius:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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


<div class="testi-slider testimonial">
    <?php foreach ($settings['testi_list'] as $index => $item) :
			?>
    <div>

        <p class="testi-text">
            <?php echo  $item['text']; ?>
        </p>
        <div class="testi-box clearfix">
            <div class="testi-img">
                <?php echo Group_Control_Image_Size::get_attachment_image_html($item, 'image2', 'image'); ?>
            </div>

            <h3><?php echo  $item['title']; ?></h3>

            <p class="testi-from"><?php echo  $item['position']; ?></p>
        </div>
    </div>

    <?php endforeach; ?>
</div>
<!--/.testimonial-->


<?php
	wp_enqueue_script('jquery-slick', plugins_url('/js/slick.min.js', __FILE__), array('jquery'), null, true);
	wp_enqueue_script('cholot-testimonial', plugins_url('/js/testimonial.js', __FILE__), array('jquery'), null, true);
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