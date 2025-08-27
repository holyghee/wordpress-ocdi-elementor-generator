<?php
namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Utils;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Logo extends Widget_Base
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
		return 'cholot-logo';
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
		return __('Site Logo/Branding', 'cholot_plugin');
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
		return 'eicon-logo';
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
				'label' => __('Logo Settings', 'cholot_plugin'),
			]
		);

		$this->add_control(
			'logo_img',
			[
				'label' => __('Image', 'cholot_plugin'),
				'type' => Controls_Manager::MEDIA,
				'default' => [
					'url' => Utils::get_placeholder_image_src(),
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
					]
				],
				'default' => '',
				'selectors' => [
					'{{WRAPPER}}' => 'text-align: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'height',
			[
				'label' => __('Logo Image max Height', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 5,
						'max' => 500,
						'step' => 1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .custom-logo .logo1' => 'max-height: {{SIZE}}{{UNIT}};',
				],
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'logo_settings',
			[
				'label' => __('Logo Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'logo_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .custom-logo a' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		$this->add_responsive_control(
			'logo_margin',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .custom-logo a' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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

	<div class="custom-logo">
		<a href="<?php echo esc_url(home_url('/')); ?>"><img class="logo1" alt="logo" src="<?php echo esc_url($settings['logo_img']['url']); ?>" /></a>
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
