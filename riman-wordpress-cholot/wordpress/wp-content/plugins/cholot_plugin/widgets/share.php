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
class Cholot_Share extends Widget_Base
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
		return 'cholot-share';
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
		return __('Cholot Share Box', 'cholot_plugin');
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
		return 'eicon-facebook-like-box';
	}

	//script depend
	public function get_script_depends()
	{
		return ['cholot-share'];
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
				'label' => __('Share Box Settings', 'cholot_plugin'),
			]
		);

		$this->add_control(
			'title',
			[
				'label' => __('Text', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'default' => __('Share This:', 'cholot_plugin'),
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
				],
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .share-box' => 'text-align: {{VALUE}};',
				],
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'section_title_style',
			[
				'label' => __('Share Box Style.', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'desc_typography',
				'label'     => __('Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .share-text',
			]
		);

		$this->add_control(
			'title_color',
			[
				'label' => __('Text Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .share-text' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'title_margin',
			[
				'label' => __('Text Margin)', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .share-text' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'icon_size',
			[
				'label' => __('Icon Size (px)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 1,
						'max' => 50,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .share-box a ' => 'font-size: {{SIZE}}px;',
				],
			]
		);

		$this->add_responsive_control(
			'icon_spacing',
			[
				'label' => __('Icon Spacing (px)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 1,
						'max' => 50,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .share-box a ' => 'margin-left: {{SIZE}}px;',
				],
			]
		);

		$this->add_control(
			'icon_color',
			[
				'label' => __('Icon Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .share-box a' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'icon_color_hover',
			[
				'label' => __('Icon Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'selectors' => [
					'{{WRAPPER}} .share-box a:hover' => 'color: {{VALUE}};',
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

<div class="share-box cholot-share-box">
    <span class="share-text"><?php echo $settings['title']; ?></span>
    <a class="tw-share"
        href="http://twitter.com/home/?status=<?php echo rawurlencode(get_the_title());  ?>%20-%20<?php the_permalink(); ?>"
        title="<?php esc_html_e("Tweet this", "cholot_plugin"); ?>">
        <i class="fa fa-twitter"></i>
    </a>
    <a class="fb-share"
        href="http://www.facebook.com/sharer.php?u=<?php the_permalink(); ?>&amp;t=<?php echo rawurlencode(get_the_title());  ?>"
        title="<?php esc_html_e("Share on Facebook", "cholot_plugin"); ?>">
        <i class="fa fa-facebook"></i>
    </a>
    <a href="http://pinterest.com/pin/create/button/?url=<?php the_permalink(); ?>&media=<?php
																								global $post;
																								$url = wp_get_attachment_url(get_post_thumbnail_id($post->ID));
																								echo $url; ?>" title="<?php esc_html_e("Pin This", "cholot_plugin"); ?>">
        <i class="fa fa-pinterest"></i>
    </a>
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