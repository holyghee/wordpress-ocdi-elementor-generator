<?php

namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Utils;
use Elementor\Group_Control_Border;
use Elementor\Icons_Manager;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Button_Text extends Widget_Base
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
		return 'cholot-button-text';
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
		return __('Cholot Button with Subtitle', 'cholot_plugin');
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
		return 'fa fa-square';
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
			'section_content_style',
			[
				'label' => __('Button Settings', 'cholot_plugin')
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
			'btn_sub',
			[
				'label' => __('Button Subtitle', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'label_block' => true,
				'label_block' => true,
				'placeholder' => 'Insert your button subtitle text here..',
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
			'selected_icon',
			[
				'label' => __('Icon', 'elementor'),
				'type' => Controls_Manager::ICONS,
				'label_block' => true,
				'fa4compatibility' => 'icon',
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
					'selected_icon[value]!' => '',
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
					'selected_icon[value]!' => '',
				],
				'selectors' => [
					'{{WRAPPER}} .content-btn.content-btn-right .button-text' => 'margin-right: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .content-btn.content-btn-right .button-sub' => 'margin-right: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .content-btn.content-btn-left .button-text' => 'margin-left: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .content-btn.content-btn-left .button-sub' => 'margin-left: {{SIZE}}{{UNIT}};',
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
			'btn_sub_settings',
			[
				'label' => __('Button Subtitle Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'btn_sub_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .content-btn .button-sub',
			]
		);

		$this->add_responsive_control(
			'btn_sub_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn .button-sub' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'btn_sub_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn .button-sub' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'btn_subcolor',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn .button-sub' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'btn_subcolor_hover',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn:hover .button-sub' => 'color: {{VALUE}};',
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
					'{{WRAPPER}} .content-btn:hover:after' => 'background-color: {{VALUE}};',
					'{{WRAPPER}} .content-btn:hover:before' => 'background-color: {{VALUE}};',
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

		$this->end_controls_section();


		$this->start_controls_section(
			'btn_color_section_hover',
			[
				'label' => __('Button on Hover Color Scheme Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);


		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'icon_hover_bordering',
				'placeholder' => '1px',
				'default' => '',
				'selector' => '{{WRAPPER}} .content-btn:hover',
				'separator' => 'before',
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
			'icon_section_settings',
			[
				'label' => __('Icon Setting', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);
		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'icn_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .content-btn-button-icon',
			]
		);


		$this->add_responsive_control(
			'icon_box_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn-button-icon' => 'margin:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'icon_box_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .content-btn-button-icon' => 'padding:{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'icon_box_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn-button-icon' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'icon_box_color_hover',
			[
				'label' => __('Color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn:hover .content-btn-button-icon' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'icon_bg_box_color',
			[
				'label' => __('Background color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn-button-icon' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'icon_bg_box_color_hover',
			[
				'label' => __('Background color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn:hover .content-btn-button-icon' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'icon_border_box',
				'placeholder' => '1px',
				'default' => '',
				'selector' => '{{WRAPPER}} .content-btn-button-icon',
				'separator' => 'before',
			]
		);


		$this->add_control(
			'icon_box_border_color_hover',
			[
				'label' => __('Border Color on  Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .content-btn:hover .content-btn-button-icon' => 'border-color: {{VALUE}};',
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
		$this->add_render_attribute('icon-align', 'class', 'content-btn-button-icon btn-text-special');
		$migrated = isset($settings['__fa4_migrated']['selected_icon']);
		$is_new = empty($settings['icon']) && Icons_Manager::is_migration_allowed();
		if (!$is_new && empty($settings['icon_align'])) {
			// @todo: remove when deprecated
			// added as bc in 2.6
			//old default
			$settings['icon_align'] = $this->get_settings('icon_align');
		}
		?>
<?php if ($settings['btn_text'] != '' && $settings['link']['url'] != '') { ?>

<a class="content-btn content-btn-<?php echo esc_attr($settings['icon_align']); ?>"
    href="<?php echo esc_url($settings['link']['url']); ?>">

    <?php if (!empty($settings['icon']) || !empty($settings['selected_icon']['value'])) : ?>
    <span <?php echo $this->get_render_attribute_string('icon-align'); ?>>
        <?php if ($is_new || $migrated) :
						Icons_Manager::render_icon($settings['selected_icon'], ['aria-hidden' => 'true']);
					else : ?>
        <i class="<?php echo esc_attr($settings['icon']); ?>" aria-hidden="true"></i>
        <?php endif; ?>
    </span>
    <?php endif; ?>

    <span class="button-text"><?php echo esc_attr($settings['btn_text']); ?></span>
    <span class="button-sub"><?php echo esc_attr($settings['btn_sub']); ?></span>
</a>

<?php } ?>

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