<?php 

// create custom plugin settings menu
add_action('admin_menu', 'rdn_flickr_menu');

function rdn_flickr_menu() {

	//create new top-level menu
	add_menu_page('Flickr Feed Setting', 'Flickr Feed Setting', 'administrator', __FILE__, 'rdn_flickr_page',plugins_url('/flickr.png', __FILE__));

	//call register settings function
	add_action( 'admin_init', 'register_rdn_flickr_feed' );
}


function register_rdn_flickr_feed() {
	//register our settings
	register_setting( 'rdn-flickr-feed-setting-group', 'rdn_flickr_id' );
	register_setting( 'rdn-flickr-feed-setting-group', 'rdn_flickr_img');
}

function plugin_options_validate($input) {
$newinput['text_string'] = trim($input['text_string']);
if(!preg_match('/^[a-z0-9]{32}$/i', $newinput['text_string'])) {
$newinput['text_string'] = '';
}
return $newinput;
}
function rdn_flickr_page() {
?>
<div class="wrap">
<h2>Flickr Feed Setting</h2>

<form method="post" action="options.php">
    <?php settings_fields( 'rdn-flickr-feed-setting-group' ); ?>
    <?php do_settings_sections( 'rdn-flickr-feed-setting-group' ); ?>
    <table class="form-table">
        <tr valign="top">
        <th scope="row">1. Flickr ID<br/> <small>eg: 52617155@N08</small></th>
        <td><input type="text" name="rdn_flickr_id" value="<?php echo get_option('rdn_flickr_id'); ?>" /></td>
        </tr>
         
        <tr valign="top">
        <th scope="row">2. Show Flickr Image.<br/> <small>(default value 8)</small></th>
        <td><input type="text" name="rdn_flickr_img" value="<?php echo get_option('rdn_flickr_img'); ?>" /></td>
        </tr>
        
        
    </table>
    
    <?php submit_button(); ?>

</form>
		<h4>Explanation:</h4>
		<ul>
        	<li><p>You can check your Flickr ID <a href="http://idgettr.com/" target="_blank">here</a></p></li> 
        	<li><p>You can decide how many images will be displayed. Default value is 8 </p></li>
            <li><p>After you finish set it up, you can use it in widget page.</p></li>
        </ul>
</div>
<?php } 



