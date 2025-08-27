<?php class cholot_about extends WP_Widget
{

	// Defines the widget name
	public function __construct()
	{
		parent::__construct(false, $name = __('About Us Widget', 'cholot_plugin'));
	}

	// Creates the widget in the WP admin area
	function form($instance)
	{

		// values
		if ($instance) {
			$title = $instance['title'];
			$subtitle = $instance['subtitle'];
			$textarea = $instance['textarea'];
			$image_uri = esc_url($instance['image_uri']);
			$twitter = esc_url($instance['twitter']);
			$facebook = esc_url($instance['facebook']);
			$google = esc_url($instance['google']);
			$instagram = esc_url($instance['instagram']);
			$pinterest = esc_url($instance['pinterest']);
			$youtube = esc_url($instance['youtube']);
		} else {
			$subtitle = '';
			$title = '';
			$textarea = '';
			$image_uri = '';
			$twitter = '';
			$facebook = '';
			$google = '';
			$instagram = '';
			$pinterest = '';
			$youtube = '';
		}
		?>

<p>
    <label for="<?php echo $this->get_field_id('title'); ?>"><?php esc_html_e('Title:', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>"
        name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo $title; ?>" />
</p>
<p>
    <label
        for="<?php echo $this->get_field_id('subtitle'); ?>"><?php esc_html_e('Subtitle (text below title):', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('subtitle'); ?>"
        name="<?php echo $this->get_field_name('subtitle'); ?>" type="text" value="<?php echo $subtitle; ?>" />
</p>
<p>
    <label
        for="<?php echo $this->get_field_id('image_uri'); ?>"><?php esc_html_e('About Us Image:', 'cholot_plugin'); ?></label><br />

    <?php if ($image_uri) { ?>
    <img class="about_img" src="<?php echo $image_uri; ?>" style="max-width:100%;" />
    <?php } ?>
    <input type="text" class="widefat about_img_url" name="<?php echo $this->get_field_name('image_uri'); ?>"
        id="<?php echo $this->get_field_id('image_uri'); ?>" value="<?php echo $image_uri; ?>"> <br />Recommended size
    600x600px
</p>
<p>
    <input type="button" value="<?php esc_html_e('Upload Image', 'cholot_plugin'); ?>" class="button about_btn_upload"
        id="about_button" />
</p><br />

<p>
    <label
        for="<?php echo $this->get_field_id('textarea'); ?>"><?php esc_html_e('Textarea:', 'cholot_plugin'); ?></label>
    <textarea class="widefat" style="min-height: 150px;" id="<?php echo $this->get_field_id('textarea'); ?>"
        name="<?php echo $this->get_field_name('textarea'); ?>"><?php echo $textarea; ?></textarea>
</p>





<p>
    <label
        for="<?php echo $this->get_field_id('social'); ?>"><?php esc_html_e('Social Media:', 'cholot_plugin'); ?></label><br />
</p>

<p>
    <label
        for="<?php echo $this->get_field_id('facebook'); ?>"><?php esc_html_e('Facebook', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('facebook'); ?>"
        name="<?php echo $this->get_field_name('facebook'); ?>" type="text"
        value="<?php echo esc_attr($facebook); ?>" />
</p>

<p>
    <label for="<?php echo $this->get_field_id('twitter'); ?>"><?php esc_html_e('Twitter', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('twitter'); ?>"
        name="<?php echo $this->get_field_name('twitter'); ?>" type="text" value="<?php echo esc_attr($twitter); ?>" />
</p>

<p>
    <label for="<?php echo $this->get_field_id('google'); ?>"><?php esc_html_e('Google', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('google'); ?>"
        name="<?php echo $this->get_field_name('google'); ?>" type="text" value="<?php echo esc_attr($google); ?>" />
</p>

<p>
    <label
        for="<?php echo $this->get_field_id('instagram'); ?>"><?php esc_html_e('Instagram', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('instagram'); ?>"
        name="<?php echo $this->get_field_name('instagram'); ?>" type="text"
        value="<?php echo esc_attr($instagram); ?>" />
</p>

<p>
    <label
        for="<?php echo $this->get_field_id('pinterest'); ?>"><?php esc_html_e('Pinterest', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('pinterest'); ?>"
        name="<?php echo $this->get_field_name('pinterest'); ?>" type="text"
        value="<?php echo esc_attr($pinterest); ?>" />
</p>

<p>
    <label for="<?php echo $this->get_field_id('youtube'); ?>"><?php esc_html_e('Youtube', 'cholot_plugin'); ?></label>
    <input class="widefat" id="<?php echo $this->get_field_id('youtube'); ?>"
        name="<?php echo $this->get_field_name('youtube'); ?>" type="text" value="<?php echo esc_attr($youtube); ?>" />
</p>

<?php
	} // end admin area form

	// Widget Update
	function update($new_instance, $old_instance)
	{
		$instance = $old_instance;
		// Fields
		$instance['title'] = (!empty($new_instance['title'])) ? $new_instance['title'] : '';
		$instance['subtitle'] = (!empty($new_instance['subtitle'])) ? $new_instance['subtitle'] : '';
		$instance['textarea'] = (!empty($new_instance['textarea'])) ? wp_kses_post($new_instance['textarea']) : '';
		$instance['image_uri'] = (!empty($new_instance['image_uri'])) ? strip_tags($new_instance['image_uri']) : '';
		$instance['twitter'] = (!empty($new_instance['twitter'])) ? strip_tags($new_instance['twitter']) : '';
		$instance['facebook'] = (!empty($new_instance['facebook'])) ? strip_tags($new_instance['facebook']) : '';
		$instance['google'] = (!empty($new_instance['google'])) ? strip_tags($new_instance['google']) : '';
		$instance['instagram'] = (!empty($new_instance['instagram'])) ? strip_tags($new_instance['instagram']) : '';
		$instance['pinterest'] = (!empty($new_instance['pinterest'])) ? strip_tags($new_instance['pinterest']) : '';
		$instance['youtube'] = (!empty($new_instance['youtube'])) ? strip_tags($new_instance['youtube']) : '';
		$instance['vimeo'] = (!empty($new_instance['vimeo'])) ? strip_tags($new_instance['vimeo']) : '';
		return $instance;
	}

	// Output the content on frontend
	function widget($args, $instance)
	{
		extract($args);

		// Widget options
		$title = isset($instance['title']) ? $instance['title'] : '';
		$subtitle =  isset($instance['subtitle']) ? $instance['subtitle'] : '';
		$textarea =  isset($instance['textarea']) ? $instance['textarea'] : '';
		$image_uri = isset($instance['image_uri']) ? $instance['image_uri'] : '';
		$twitter =  isset($instance['twitter']) ? $instance['twitter'] : '';
		$facebook =  isset($instance['facebook']) ? $instance['facebook'] : '';
		$google =   isset($instance['google']) ? $instance['google'] : '';
		$instagram =  isset($instance['instagram']) ? $instance['instagram'] : '';
		$pinterest = isset($instance['pinterest']) ? $instance['pinterest'] : '';
		$youtube = isset($instance['youtube']) ? $instance['youtube'] : '';
		$vimeo = isset($instance['vimeo']) ? $instance['vimeo'] : '';

		echo $before_widget;
		// Display the widget
		echo '<div class="widget-about-us clearfix">';

		echo '<div class="abtw-box" style="background-image:url(' . $image_uri . ');background-position: center;background-size: cover;"><div class="border-ab"></div><div class="slider-mask"></div>';



		// if title is exist
		if ($title) { ?>
<div class="bordering-widget">



    <h3><?php echo wp_kses_post($title); ?></h3>
    <p class="wdg-about-subtitle"><?php echo esc_attr($subtitle); ?></p>
</div>
<?php }

		echo '</div><div class="ab-bordering">';

		// if textarea is exist
		if ($textarea) {

			echo wp_kses_post($textarea);
		}

		// Social Media Group


		if ($twitter or $facebook or $google or $instagram or $pinterest or $youtube) {
			echo '<ul class="abtw-soc">';

			// if Facebook is exist
			if ($facebook) { ?>
<li><a href="<?php echo $facebook; ?>" target="_blank"><i class="fa fa-facebook"></i></a></li>
<?php
			}

			// if Twitter is exist
			if ($twitter) { ?>
<li><a href="<?php echo $twitter; ?>" target="_blank"><i class="fa fa-twitter"></i></a></li>
<?php
			}



			// if Google+ is exist
			if ($google) { ?>
<li><a href="<?php echo $google; ?>" target="_blank"><i class="fa fa-google-plus"></i></a></li>
<?php
			}

			// if Instagram is exist
			if ($instagram) { ?>
<li><a href="<?php echo $instagram; ?>" target="_blank"><i class="fa fa-instagram"></i></a></li>
<?php
			}

			// if pinterest is exist
			if ($pinterest) { ?>
<li><a href="<?php echo $pinterest; ?>" target="_blank"><i class="fa fa-pinterest"></i></a></li>
<?php
			}

			// if Youtube is exist
			if ($youtube) { ?>
<li><a href="<?php echo $youtube; ?>" target="_blank"><i class="fa fa-youtube"></i></a></li>
<?php
			}
			// if Vimeo is exist
			if ($vimeo) { ?>
<li><a href="<?php echo $vimeo; ?>" target="_blank"><i class="fa fa-vimeo-square"></i></a></li>
<?php
			}

			echo '</ul>';
		} // end social check


		echo '</div></div>';
		echo $after_widget;
	} // end frontend output
} // end class

// Register widget

function register_about_us()
{
	register_widget('cholot_about');
}
add_action('widgets_init', 'register_about_us');

// Load scripts in admin area
if (!function_exists('cholot_about_scripts')) :
	function cholot_about_scripts()
	{

		wp_enqueue_media();
		// Media upload script
		wp_enqueue_script('cholot_about_upload', plugin_dir_url(__FILE__) . 'js/about-me.js');
	}
	add_action('admin_enqueue_scripts', 'cholot_about_scripts');
endif; // end cholot_about_scripts