<?php
namespace CholotPlugin\Widgets;

use Elementor\Group_Control_Typography;
use Elementor\Scheme_Typography;
use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Utils;

if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly


		
/**
 * @since 1.1.0
 */
class Cholot_TeamHover extends Widget_Base {

	/**
	 * Retrieve the widget name.
	 *
	 * @since 1.1.0
	 *
	 * @access public
	 *
	 * @return string Widget name.
	 */
	public function get_name() {
		return 'cholot-team-hover';
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
	public function get_title() {
		return __( 'Cholot Team Text in Hover', 'cholot_plugin' );
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
	public function get_icon() {
		return 'fa fa-user-o';
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
	public function get_categories() {
		return [ 'cholot-elements' ];
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
	protected function _register_controls() {
	
		$this->start_controls_section(
			'section_content',
			[
				'label' => __( 'Team Settings', 'cholot_plugin' ),
			]
		);
		
		$this->add_control(
            'title',
            [
                'label' => __( 'Team Title', 'cholot_plugin'),
                'type' => Controls_Manager::TEXT,
				'default' => __( 'Team Name', 'cholot_plugin' ),
				'label_block' => true,
            ]
        );
		
		$this->add_control(
            'text',
            [
                'label' => __( 'Team Position', 'cholot_plugin'),
                'type' => Controls_Manager::TEXT,
				'default' => __( 'Web Designer', 'cholot_plugin' ),
				'label_block' => true,
            ]
        );

		$this->add_control(
			'team_icon',
			[
				'label' => __( 'Team Social Icon', 'cholot_plugin' ),
				'type' => Controls_Manager::REPEATER,
				'default' => [
					[
						'icon' => 'fa fa-facebook',
					],
					[
						'icon' => 'fa fa-twitter',
					],
					[
						'icon' => 'fa fa-instagram',
					],
				],
				'fields' => [
					[
						'name' => 'link',
						'label' => __( 'Social Link', 'cholot_plugin' ),
						'type' => Controls_Manager::URL,
						'label_block' => true,
						'placeholder' => __( 'Your social link..', 'cholot_plugin' ),
					],
					
					[
						'name' => 'icon',
						'label' => __( 'Icon', 'cholot_plugin' ),
						'type' => Controls_Manager::ICON,
						'label_block' => true,
						'default' => 'fa fa-facebook',
						'include' => [
							'fa fa-apple',
							'fa fa-behance',
							'fa fa-bitbucket',
							'fa fa-codepen',
							'fa fa-delicious',
							'fa fa-digg',
							'fa fa-dribbble',
							'fa fa-envelope',
							'fa fa-facebook',
							'fa fa-flickr',
							'fa fa-foursquare',
							'fa fa-github',
							'fa fa-google-plus',
							'fa fa-houzz',
							'fa fa-instagram',
							'fa fa-jsfiddle',
							'fa fa-linkedin',
							'fa fa-medium',
							'fa fa-odnoklassniki',
							'fa fa-pinterest',
							'fa fa-product-hunt',
							'fa fa-reddit',
							'fa fa-shopping-cart',
							'fa fa-slideshare',
							'fa fa-snapchat',
							'fa fa-soundcloud',
							'fa fa-spotify',
							'fa fa-stack-overflow',
							'fa fa-telegram',
							'fa fa-tripadvisor',
							'fa fa-tumblr',
							'fa fa-twitch',
							'fa fa-twitter',
							'fa fa-vimeo',
							'fa fa-vk',
							'fa fa-weibo',
							'fa fa-weixin',
							'fa fa-whatsapp',
							'fa fa-wordpress',
							'fa fa-xing',
							'fa fa-yelp',
							'fa fa-youtube',
						],
					],
				],
				'title_field' => '<i class="{{ icon }}"></i> {{{ icon.replace( \'fa fa-\',\'\' ).replace( \'-\',\' \' ).replace( /\b\w/g, function( letter ){ return letter.toUpperCase() } ) }}}',
			]
		);
		
		
		$this->end_controls_section();
		
		
		
		$this->start_controls_section(
			'title_typo',
			[
				'label' => __( 'Title Content Settings', 'cholot_plugin' ),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);
		
		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'cport_typography',
				'label'     => __( 'Title Typography', 'cholot_plugin' ),
				'selector'  => '{{WRAPPER}} .team-name',
			]
		);
		
		$this->add_control(
			'title_cl',
			[
				'label' => __( 'Title Color', 'cholot_plugin' ),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-name' => 'color: {{VALUE}};',
				],
			]
		);
		
		
		$this->end_controls_section();
		
		$this->start_controls_section(
			'sub_typo',
			[
				'label' => __( 'Text Content Settings', 'cholot_plugin' ),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);
		
		$this->add_group_control(
			Group_Control_Typography::get_type(),
			[
				'name'      => 'ctext_typography',
				'label'     => __( 'Text Typography', 'cholot_plugin' ),
				'selector'  => '{{WRAPPER}} .team-post',
			]
		);
		
		$this->add_control(
			'txt_cl',
			[
				'label' => __( 'Text Color', 'cholot_plugin' ),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-post' => 'color: {{VALUE}};',
				],
			]
		);
		
		$this->end_controls_section();
		
		$this->start_controls_section(
			'icon_section_setting',
			[
				'label' => __( 'Icon Settings', 'cholot_plugin' ),
				'tab' => Controls_Manager::TAB_STYLE,
			]
		);
		
		$this->add_control(
			'icon_color',
			[
				'label' => __( 'Color', 'cholot_plugin' ),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a' => 'color: {{VALUE}};',
				],
			]
		);
		
		$this->add_control(
			'icon_color_hover',
			[
				'label' => __( 'Color on Hover', 'cholot_plugin' ),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a:hover' => 'color: {{VALUE}};',
				],
			]
		);
		
		$this->add_control(
			'icon_bg',
			[
				'label' => __( 'Background', 'cholot_plugin' ),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a' => 'background-color: {{VALUE}};',
				],
			]
		);
		
		$this->add_control(
			'icon_bg_hover',
			[
				'label' => __( 'Background on Hover', 'cholot_plugin' ),
				'type' => Controls_Manager::COLOR,
				'default' => '',
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a:hover' => 'background-color: {{VALUE}};',
				],
			]
		);
		
		$this->add_responsive_control(
			'icon_radius',
			[
				'label' => __( 'Border Radius', 'cholot_plugin' ),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => [ 'px', '%' ],
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a' => 'border-radius: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
				],
			]
		);
		
		$this->add_responsive_control(
			'icon_size',
			[
				'label' => __( 'Size', 'cholot_plugin' ),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' =>0,
						'max' => 100,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a' => 'font-size: {{SIZE}}{{UNIT}};',
				],
			]
		);
		
		
		$this->add_responsive_control(
			'bg_size',
			[
				'label' => __( 'Background Size', 'cholot_plugin' ),
				'type' => Controls_Manager::SLIDER,
				'range' => [
					'px' => [
						'min' =>0,
						'max' => 100,
					],
				],
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a' => 'width: {{SIZE}}{{UNIT}};height: {{SIZE}}{{UNIT}};line-height: {{SIZE}}{{UNIT}};',
				],
			]
		);
		
		$this->add_responsive_control(
			'icon_margin',
			[
				'label' => __( 'Margin', 'cholot_plugin' ),
				'type' => Controls_Manager::DIMENSIONS,
				'size_units' => [ 'px', '%' ],
				'selectors' => [
					'{{WRAPPER}} .team-soc-list li a' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
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
	protected function render() { 
	$settings = $this->get_settings();
	$this->add_inline_editing_attributes( 'title' );
	$this->add_render_attribute( 'title','class','team-name' );
	$this->add_inline_editing_attributes( 'text' );
	$this->add_render_attribute( 'text','class','icon-cell-sub team-post' );
	
	?>
    
    <div class="box-padding">
        <h3 <?php echo $this->get_render_attribute_string( 'title' ); ?>><?php echo $settings['title']; ?></h3>
        <p <?php echo $this->get_render_attribute_string( 'text' ); ?>><?php echo $settings['text']; ?></p>
        <ul class="team-soc-list">
            <?php foreach ( $settings['team_icon'] as $index => $item ) : 
			$link_key = 'link_' . $index;
			$this->add_render_attribute( $link_key, 'href',esc_url ($item['link']['url']) );

			if ( $item['link']['is_external'] ) {
				$this->add_render_attribute( $link_key, 'target', '_blank' );
			}

			if ( $item['link']['nofollow'] ) {
				$this->add_render_attribute( $link_key, 'rel', 'nofollow' );
			}
			?>
			<li>
				<?php echo '<a ' . $this->get_render_attribute_string( $link_key ) . '>'; ?>
					<i class="<?php echo esc_attr ( $item['icon']); ?>"></i>
				</a>
			</li>
			<?php endforeach; ?>
        </ul>
    </div><!--/.box-padding-->
    
                    
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
	protected function _content_template() {
		
		
	}
}


