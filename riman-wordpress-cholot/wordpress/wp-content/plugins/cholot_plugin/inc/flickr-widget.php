<?php
//load all script for flickr feed
function rdn_flickr_load() {
	if ( is_active_widget( false, false, 'rdn_widget_flickr', true ) ){
		wp_enqueue_script( 'flickr-feed',plugins_url( '/js/jflickrfeed.min.js' , __FILE__ ),array(),'', 'in_footer');
	}
} 
add_action('wp_enqueue_scripts', 'rdn_flickr_load', 20, 1);


function rdn_flickr_feed_start() {
	 if ( is_active_widget( false, false, 'rdn_widget_flickr', true ) ){

?>
	<script type="text/javascript">
	(function ($) {
	'use strict';
		$(window).on("load", function() { // makes sure the whole site is loaded
			// script popup image
			$('.flickr-popup-img').magnificPopup({
				type: 'image',
				gallery: {
					enabled: true
				}
			});
		});
		//script for flickr feed
		$('.flickr-feed').jflickrfeed({
			limit: <?php if  ( get_option('rdn_flickr_img') != '') { echo get_option('rdn_flickr_img');} else { echo "8";} ?>,
			qstrings: {
				id: '<?php if  ( get_option('rdn_flickr_id') != '') { echo get_option('rdn_flickr_id');} else { echo "52617155@N08";} ?>'
			},
			itemTemplate: '<li>' + '<a href="{{image_b}}" class="flickr-popup-img"><img src="{{image_q}}" alt="{{title}}" /></a>' + '</li>'
		});
	})(jQuery);
	</script>
<?php } 

}
//script for portfolio ajax
add_action( 'wp_footer', 'rdn_flickr_feed_start',102 );


//widget

class rdn_widget_flickr extends WP_Widget {

// constructor
public function __construct() {
        $widget_ops = array(
			'classname' => 'rdn_widget_flickr', 
			'description' => __('Display flickr feed.'),
		);
        parent::__construct('rdn_widget_flickr', __('Flickr Widget'), $widget_ops);
    }

// widget form creation

function form($instance) {

// Check values
if( $instance) {
	 $title = $instance['title'];
} else {
	 $title = '';
}

?>
<p>
		<label for="<?php echo $this->get_field_id('title'); ?>"><?php esc_html_e('Title:', 'cholot_plugin'); ?></label>
		<input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo $title; ?>" />
		</p>
<p>
You can set the flickr id & images to show in Flickr Feed Setting (left menu).
</p>


<?php
}

function update($new_instance, $old_instance) {
$instance = $old_instance;
$instance['title'] = ( ! empty( $new_instance['title'] ) ) ? $new_instance['title']: '';
// Fields

return $instance;

}

// display widget
function widget($args, $instance) {
extract( $args );
// Widget options
$title = $instance['title'];


echo $before_widget; 
if ( ! empty( $title ) )
echo $args['before_title'] . $title . $args['after_title'];?>

<ul id="flickr" class="flickr-feed clearfix"></ul>
   
<?php 
echo $after_widget;
}
}


// register widget 
function register_rdn_widget_flickr() {
	register_widget( 'rdn_widget_flickr' );
}
add_action( 'widgets_init', 'register_rdn_widget_flickr' );

