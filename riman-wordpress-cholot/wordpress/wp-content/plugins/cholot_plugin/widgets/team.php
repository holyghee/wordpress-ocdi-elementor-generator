<?php

namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Utils;
use Elementor\Icons_Manager;
use Elementor\Group_Control_Border;
use Elementor\Repeater;
use Elementor\Group_Control_Box_Shadow;
use Elementor\Group_Control_Background;

if (!defined('ABSPATH')) exit; // Exit if accessed directly



/**
 * @since 1.1.0
 */
class Cholot_Team extends Widget_Base
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
		return 'cholot-team';
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
		return __('Cholot Team', 'cholot_plugin');
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
		return 'fa fa-address-card';
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
				'label' => __('Team Settings', 'cholot_plugin'),
			]
		);

		$this->add_control(
			'title',
			[
				'label' => __('Team Title', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'default' => __('Team Name', 'cholot_plugin'),
				'label_block' => true,
			]
		);

		$this->add_control(
			'text',
			[
				'label' => __('Team Position', 'cholot_plugin'),
				'type' => Controls_Manager::TEXT,
				'default' => __('Web Designer', 'cholot_plugin'),
				'label_block' => true,
			]
		);

		$this->add_control(
			'image',
			[
				'label' => __('Team Image', 'cholot_plugin'),
				'type' => Controls_Manager::MEDIA,
				'default' => [
					'url' => Utils::get_placeholder_image_src(),
				],
			]
		);

		$this->add_responsive_control(
			'team_height',
			[
				'label' => __('Team Image Height', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1000,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .port-box' => 'padding: {{SIZE}}px 0 0 0;',
				],
			]
		);

		$this->add_responsive_control(
			'image_position',
			[
				'label' => __('Team Image Position', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'top center' => __('Top', 'cholot_plugin'),
					'bottom center' => __('Bottom', 'cholot_plugin'),
					'center center' => __('Center', 'cholot_plugin'),
				],
				'default' => 'center center',
				'selectors' => [
					'{{WRAPPER}} .port-img' => 'background-position: {{VALUE}};',
				],
			]
		);

		$repeater = new Repeater();

		$repeater->add_control(
			'social_icon',
			[
				'label' => __('Icon', 'elementor'),
				'type' => Controls_Manager::ICONS,
				'fa4compatibility' => 'social',
				'label_block' => true,
				'default' => [
					'value' => 'fab fa-wordpress',
					'library' => 'fa-brands',
				],
				'recommended' => [
					'fa-brands' => [
						'android',
						'apple',
						'behance',
						'bitbucket',
						'codepen',
						'delicious',
						'deviantart',
						'digg',
						'dribbble',
						'envelope',
						'facebook',
						'flickr',
						'foursquare',
						'free-code-camp',
						'github',
						'gitlab',
						'globe',
						'google-plus',
						'houzz',
						'instagram',
						'jsfiddle',
						'link',
						'linkedin',
						'medium',
						'meetup',
						'mixcloud',
						'odnoklassniki',
						'pinterest',
						'product-hunt',
						'reddit',
						'rss',
						'shopping-cart',
						'skype',
						'slideshare',
						'snapchat',
						'soundcloud',
						'spotify',
						'stack-overflow',
						'steam',
						'stumbleupon',
						'telegram',
						'thumb-tack',
						'tripadvisor',
						'tumblr',
						'twitch',
						'twitter',
						'viber',
						'vimeo',
						'vk',
						'weibo',
						'weixin',
						'whatsapp',
						'wordpress',
						'xing',
						'yelp',
						'youtube',
						'500px',
					],
				],
			]
		);

		$repeater->add_control(
			'link',
			[
				'label' => __('Link', 'elementor'),
				'type' => Controls_Manager::URL,
				'label_block' => true,
				'default' => [
					'is_external' => 'true',
				],
				'dynamic' => [
					'active' => true,
				],
				'placeholder' => __('https://your-link.com', 'elementor'),
			]
		);

		$repeater->add_control(
			'item_icon_color',
			[
				'label' => __('Color', 'elementor'),
				'type' => Controls_Manager::SELECT,
				'default' => 'default',
				'options' => [
					'default' => __('Official Color', 'elementor'),
					'custom' => __('Custom', 'elementor'),
				],
			]
		);

		$repeater->add_control(
			'item_icon_primary_color',
			[
				'label' => __('Primary Color', 'elementor'),
				'type' => Controls_Manager::COLOR,
				'condition' => [
					'item_icon_color' => 'custom',
				],
				'selectors' => [
					'{{WRAPPER}} {{CURRENT_ITEM}}' => 'background-color: {{VALUE}};',
				],
			]
		);

		$repeater->add_control(
			'item_icon_secondary_color',
			[
				'label' => __('Secondary Color', 'elementor'),
				'type' => Controls_Manager::COLOR,
				'condition' => [
					'item_icon_color' => 'custom',
				],
				'selectors' => [
					'{{WRAPPER}} {{CURRENT_ITEM}} i' => 'color: {{VALUE}};',
					'{{WRAPPER}} {{CURRENT_ITEM}} svg' => 'fill: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'social_icon_list',
			[
				'label' => __('Social Icons', 'elementor'),
				'type' => Controls_Manager::REPEATER,
				'fields' => $repeater->get_controls(),
				'default' => [
					[
						'social_icon' => [
							'value' => 'fab fa-facebook',
							'library' => 'fa-brands',
						],
					],
					[
						'social_icon' => [
							'value' => 'fab fa-twitter',
							'library' => 'fa-brands',
						],
					],
					[
						'social_icon' => [
							'value' => 'fab fa-google-plus',
							'library' => 'fa-brands',
						],
					],
				],
				'title_field' => '<# var migrated = "undefined" !== typeof __fa4_migrated, social = ( "undefined" === typeof social ) ? false : social; #>{{{ elementor.helpers.getSocialNetworkNameFromIcon( social_icon, social, true, migrated, true ) }}}',
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'section_content_style',
			[
				'label' => __('Content Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);



		$this->add_responsive_control(
			'port_content',
			[
				'label' => __('Content Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}}  .team-box' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);



		$this->add_responsive_control(
			'port_padding',
			[
				'label' => __('Content Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-box' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_group_control(
			Group_Control_Border::get_type(),
			[
				'name' => 'port_border',
				'placeholder' => '1px',
				'default' => '',
				'selector' => '{{WRAPPER}} .team-box',
				'separator' => 'before',
			]
		);

		$this->add_group_control(
			Group_Control_Box_Shadow::get_type(),
			[
				'name' => 'box_shadow',
				'selector' => '{{WRAPPER}} .team-box',
			]
		);



		$this->add_group_control(
			Group_Control_Background::get_type(),
			[
				'name' => 'background',
				'label' => __('Content Background', 'plugin-domain'),
				'types' => ['classic', 'gradient'],
				'selector' => '{{WRAPPER}} .team-box',
			]
		);

		$this->add_control(
			'selected_icon',
			[
				'label' => __('Content background icon', 'elementor'),
				'type' => Controls_Manager::ICONS,
				'fa4compatibility' => 'icon',
				'default' => [
					'value' => 'fas fa-star',
					'library' => 'fa-solid',
				],
			]
		);

		$this->add_control(
			'bg_icon_color',
			[
				'label' => __('Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .cholot-bg-icon' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'bg_icon_size',
			[
				'label' => __('Icon Size', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'size_units' => ['px', '%'],
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 500,
						'step' => 1,
					],
					'%' => [
						'min' => 0,
						'max' => 100,
						'step' => 1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .cholot-bg-icon' => 'font-size: {{SIZE}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'bg_icon_rotate',
			[
				'label' => __('Rotate Icon', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => -360,
						'max' => 360,
						'step' => 1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .cholot-bg-icon' => 'transform: rotate({{SIZE}}deg);',
				],
			]
		);

		$this->add_responsive_control(
			'content_align',
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
					'{{WRAPPER}} .team-box-relative' => 'text-align: {{VALUE}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'section_content_style_hover',
			[
				'label' => __('Content Settings on hover', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_responsive_control(
			'port_content_hover',
			[
				'label' => __('Content Margin on hover', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}}:hover .team-box ' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);


		$this->add_group_control(
			Group_Control_Box_Shadow::get_type(),
			[
				'name' => 'box_shadow_hover',
				'selector' => '{{WRAPPER}}:hover .team-box',
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'title_typo',
			[
				'label' => __('Title Content Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'cport_typography',
				'label'     => __('Title Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .team-box-relative h3',
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
					'{{WRAPPER}} .team-box-relative h3' => 'display: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'title_cl',
			[
				'label' => __('Title Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-box-relative h3' => 'color: {{VALUE}};',
				],
			]
		);
		$this->add_control(
			'title_bgl',
			[
				'label' => __('Title Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-box-relative h3' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'titlep_padding',
			[
				'label' => __('Title Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-box-relative h3' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'titlep_margin',
			[
				'label' => __('Title Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-box-relative h3' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);



		$this->end_controls_section();

		$this->start_controls_section(
			'sub_typo',
			[
				'label' => __('Text Content Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);

		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'ctext_typography',
				'label'     => __('Text Typography', 'cholot_plugin'),
				'selector'  => '{{WRAPPER}} .team-box-relative p',
			]
		);

		$this->add_control(
			'text_type',
			[
				'label' => __('Text Display', 'cholot_plugin'),
				'type' => Controls_Manager::SELECT,
				'options' => [
					'block' => __('Block', 'cholot_plugin'),
					'inline-block' => __('Inline Block', 'cholot_plugin'),
				],
				'default' => 'block',
				'selectors' => [
					'{{WRAPPER}} .team-box-relative p' => 'display: {{VALUE}};',
				],
			]
		);


		$this->add_control(
			'txt_cl',
			[
				'label' => __('Text Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-box-relative p' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'txt_bg',
			[
				'label' => __('Text Background Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-box-relative p' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_responsive_control(
			'tx_padding',
			[
				'label' => __('Text Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-box-relative p' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'tx_margin',
			[
				'label' => __('Text Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-box-relative p' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->end_controls_section();

		$this->start_controls_section(
			'icon_section_setting',
			[
				'label' => __('Icon Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);




		$this->add_control(
			'icon_hcolor',
			[
				'label' => __('Color on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a:hover i' => 'color: {{VALUE}};',
					'{{WRAPPER}} .team-sicon li a:hover svg' => 'color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'icon_hbg',
			[
				'label' => __('Background on Hover', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'icon_opacity',
			[
				'label' => __('Opacity on hover', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1,
						'step' => 0.1,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a:hover' => 'opacity: {{SIZE}};',
				],
			]
		);

		$this->add_responsive_control(
			'icon_radius',
			[
				'label' => __('Border Radius', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a' => 'border-radius: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'icon_size',
			[
				'label' => __('Size', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 100,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a' => 'font-size: {{SIZE}}{{UNIT}};line-height: {{SIZE}}{{UNIT}};',
					'{{WRAPPER}} .team-sicon li a .fa' => 'width: {{SIZE}}{{UNIT}};height: {{SIZE}}{{UNIT}};line-height: {{SIZE}}{{UNIT}};'
				],
			]
		);


		$this->add_responsive_control(
			'icon_padding',
			[
				'label' => __('Padding', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_responsive_control(
			'icon_margin',
			[
				'label' => __('Margin', 'cholot_plugin'),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => ['px', '%'],
				'selectors' => [
					'{{WRAPPER}} .team-sicon li a' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);

		$this->add_control(
			'hover_animation',
			[
				'label' => __('Hover Animation', 'elementor'),
				'type' => Controls_Manager::HOVER_ANIMATION,
			]
		);

		$this->end_controls_section();



		$this->start_controls_section(
			'port_mask',
			[
				'label' => __('Mask Settings', 'cholot_plugin'),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);


		$this->add_control(
			'mask_color',
			[
				'label' => __('Mask Color', 'cholot_plugin'),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}}:hover .port-box' => 'background-color: {{VALUE}};',
				],
			]
		);

		$this->add_control(
			'mask_color_opacity',
			[
				'label' => __('Mask Color Opacity(on hover)', 'cholot_plugin'),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' => 0,
						'max' => 1,
						'step' => 0.1,
					],
				],
				'selectors' => [
					'{{WRAPPER}}:hover .port-box' => 'opacity: {{SIZE}};',
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
		$settings = $this->get_settings_for_display();
		$fallback_defaults = [
			'fa fa-facebook',
			'fa fa-twitter',
			'fa fa-google-plus',
		];
		$this->add_inline_editing_attributes('title');
		$this->add_inline_editing_attributes('text');
		$migrated = isset($settings['__fa4_migrated']['selected_icon']);
		$is_new = empty($settings['icon']) && Icons_Manager::is_migration_allowed();
		$migration_allowed = Icons_Manager::is_migration_allowed();
		$class_animation = '';

		if (!empty($settings['hover_animation'])) {
			$class_animation = ' elementor-animation-' . $settings['hover_animation'];
		}

		?>
<div class="clearfix">
    <div class="port-inner team-innerbox">
        <div class="port-box"></div>
        <div class="port-img width-img img-bg"
            style="background-image:url(<?php echo esc_url($settings['image']['url']); ?>);"></div>
        <div class="img-mask"></div>
    </div>
    <div class="team-box">
        <div class="team-box-relative">
            <h3 <?php echo $this->get_render_attribute_string('title'); ?>><?php echo $settings['title']; ?></h3>
            <p <?php echo $this->get_render_attribute_string('text'); ?>><?php echo $settings['text']; ?></p>

            <?php if (!empty($settings['icon']) || !empty($settings['selected_icon']['value'])) :  if ($is_new || $migrated) :
						Icons_Manager::render_icon($settings['selected_icon'], ['class' => 'cholot-bg-icon']);
					else : ?>
            <i class="cholot-bg-icon <?php echo esc_attr($settings['icon']); ?>" aria-hidden="true"></i>
            <?php endif;
				endif; ?>

            <ul class="team-sicon">
                <?php
					foreach ($settings['social_icon_list'] as $index => $item) {
						$migrated = isset($item['__fa4_migrated']['social_icon']);
						$is_new = empty($item['social']) && $migration_allowed;
						$social = '';

						// add old default
						if (empty($item['social']) && !$migration_allowed) {
							$item['social'] = isset($fallback_defaults[$index]) ? $fallback_defaults[$index] : 'fa fa-wordpress';
						}

						if (!empty($item['social'])) {
							$social = str_replace('fa fa-', '', $item['social']);
						}

						if (($is_new || $migrated) && 'svg' !== $item['social_icon']['library']) {
							$social = explode(' ', $item['social_icon']['value'], 2);
							if (empty($social[1])) {
								$social = '';
							} else {
								$social = str_replace('fa-', '', $social[1]);
							}
						}
						if ('svg' === $item['social_icon']['library']) {
							$social = '';
						}

						$link_key = 'link_' . $index;

						$this->add_render_attribute($link_key, 'href', $item['link']['url']);

						$this->add_render_attribute($link_key, 'class', [
							'elementor-icon',
							'elementor-social-icon',
							'elementor-social-icon-' . $social . $class_animation,
							'elementor-repeater-item-' . $item['_id'],
						]);

						if ($item['link']['is_external']) {
							$this->add_render_attribute($link_key, 'target', '_blank');
						}

						if ($item['link']['nofollow']) {
							$this->add_render_attribute($link_key, 'rel', 'nofollow');
						}

						?>
                <li>
                    <a <?php echo $this->get_render_attribute_string($link_key); ?>>
                        <span class="elementor-screen-only"><?php echo ucwords($social); ?></span>
                        <?php
								if ($is_new || $migrated) {
									Icons_Manager::render_icon($item['social_icon']);
								} else { ?>
                        <i class="<?php echo esc_attr($item['social']); ?>"></i>
                        <?php } ?>
                    </a>
                </li>
                <?php } ?>



            </ul>
        </div>
    </div>
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