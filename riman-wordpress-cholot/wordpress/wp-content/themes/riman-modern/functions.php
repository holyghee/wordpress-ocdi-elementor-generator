<?php
/**
 * RIMAN Modern Theme Functions
 */

// Theme Setup
function riman_theme_setup() {
    // Add theme support
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('automatic-feed-links');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ));
    
    // Block editor support
    add_theme_support('wp-block-styles');
    add_theme_support('align-wide');
    add_theme_support('editor-styles');
    add_editor_style('style-editor.css');
    add_theme_support('responsive-embeds');
    
    // Register navigation menu
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'riman-modern'),
        'footer' => __('Footer Menu', 'riman-modern'),
    ));
    
    // Add custom image sizes
    add_image_size('service-thumbnail', 400, 300, true);
    add_image_size('hero-banner', 1920, 1080, true);
}
add_action('after_setup_theme', 'riman_theme_setup');

// Enqueue Scripts and Styles
function riman_enqueue_assets() {
    // Styles
    wp_enqueue_style('riman-style', get_stylesheet_uri(), array(), '1.0.0');
    wp_enqueue_style('riman-blocks', get_template_directory_uri() . '/style-blocks.css', array(), '1.0.0');
    
    // Scripts
    wp_enqueue_script('riman-script', get_template_directory_uri() . '/assets/js/main.js', array('jquery'), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'riman_enqueue_assets');

// Default Menu Fallback
function riman_default_menu() {
    $pages = array(
        'Startseite' => home_url('/'),
        'Rückbau' => home_url('/rueckbaumanagement'),
        'Sanierung' => home_url('/altlastensanierung'),
        'Mediation' => home_url('/mediation'),
        'Über uns' => home_url('/ueber-uns'),
        'Kontakt' => home_url('/kontakt')
    );
    
    echo '<ul id="primary-menu">';
    foreach ($pages as $title => $url) {
        $current = (home_url($_SERVER['REQUEST_URI']) == $url) ? ' class="current-menu-item"' : '';
        echo '<li' . $current . '><a href="' . esc_url($url) . '">' . esc_html($title) . '</a></li>';
    }
    echo '</ul>';
}

// Customizer Settings
function riman_customize_register($wp_customize) {
    // Hero Section
    $wp_customize->add_section('hero_section', array(
        'title' => __('Hero Section', 'riman-modern'),
        'priority' => 30,
    ));
    
    // Hero Title
    $wp_customize->add_setting('hero_title', array(
        'default' => 'RIMAN GmbH - Rückbaumanagement & Altlastensanierung',
        'sanitize_callback' => 'sanitize_text_field',
    ));
    
    $wp_customize->add_control('hero_title', array(
        'label' => __('Hero Title', 'riman-modern'),
        'section' => 'hero_section',
        'type' => 'text',
    ));
    
    // Hero Subtitle
    $wp_customize->add_setting('hero_subtitle', array(
        'default' => 'RIMAN GmbH - Ihr Partner für nachhaltiges Rückbaumanagement und Altlastensanierung',
        'sanitize_callback' => 'sanitize_text_field',
    ));
    
    $wp_customize->add_control('hero_subtitle', array(
        'label' => __('Hero Subtitle', 'riman-modern'),
        'section' => 'hero_section',
        'type' => 'textarea',
    ));
    
    // Hero Background Image
    $wp_customize->add_setting('hero_background_image', array(
        'default' => '',
        'sanitize_callback' => 'esc_url_raw',
    ));
    
    $wp_customize->add_control(new WP_Customize_Image_Control($wp_customize, 'hero_background_image', array(
        'label' => __('Hero Background Image', 'riman-modern'),
        'section' => 'hero_section',
        'settings' => 'hero_background_image',
    )));
}
add_action('customize_register', 'riman_customize_register');

// Create default pages on theme activation
function riman_create_default_pages() {
    $pages = array(
        'Rückbaumanagement' => 'rueckbaumanagement',
        'Altlastensanierung' => 'altlastensanierung',
        'Mediation' => 'mediation',
        'Über uns' => 'ueber-uns',
        'Kontakt' => 'kontakt',
        'Impressum' => 'impressum',
        'Datenschutz' => 'datenschutz',
        'AGB' => 'agb',
        'Referenzen' => 'referenzen',
        'Infothek' => 'infothek',
        'Mitgliederbereich' => 'mitgliederbereich',
        'Schadstoff-Management' => 'schadstoff-management'
    );
    
    foreach ($pages as $title => $slug) {
        if (!get_page_by_path($slug)) {
            wp_insert_post(array(
                'post_title' => $title,
                'post_name' => $slug,
                'post_status' => 'publish',
                'post_type' => 'page',
                'post_content' => 'Inhalt für ' . $title . ' wird hier eingefügt.'
            ));
        }
    }
}
add_action('after_switch_theme', 'riman_create_default_pages');

// Add body classes
function riman_body_classes($classes) {
    if (is_front_page()) {
        $classes[] = 'home-page';
    }
    return $classes;
}
add_filter('body_class', 'riman_body_classes');

// Register Block Patterns
function riman_register_block_patterns() {
    register_block_pattern_category(
        'riman',
        array('label' => __('RIMAN', 'riman-modern'))
    );
    
    // Hero Section Pattern
    register_block_pattern(
        'riman/hero-section',
        array(
            'title' => __('Hero Section', 'riman-modern'),
            'description' => _x('A hero section with background image and call to action buttons', 'Block pattern description', 'riman-modern'),
            'categories' => array('riman', 'featured'),
            'content' => '
                <!-- wp:group {"align":"full","className":"hero-section-video","layout":{"type":"constrained"}} -->
                <div class="wp-block-group alignfull hero-section-video">
                    <!-- wp:html -->
                    <video class="hero-video-background" autoplay muted loop playsinline>
                        <source src="' . get_template_directory_uri() . '/assets/videos/hero-background.mp4" type="video/mp4">
                    </video>
                    <div class="hero-video-overlay"></div>
                    <!-- /wp:html -->
                    
                    <!-- wp:group {"className":"hero-video-content","layout":{"type":"constrained"}} -->
                    <div class="wp-block-group hero-video-content">
                        <!-- wp:heading {"textAlign":"center","level":1,"className":"hero-title"} -->
                        <h1 class="has-text-align-center hero-title">RIMAN GmbH - Rückbaumanagement &amp; Altlastensanierung</h1>
                        <!-- /wp:heading -->
                        
                        <!-- wp:paragraph {"align":"center","className":"hero-subtitle"} -->
                        <p class="has-text-align-center hero-subtitle">RIMAN GmbH - Ihr Partner für nachhaltiges Rückbaumanagement und Altlastensanierung</p>
                        <!-- /wp:paragraph -->
                    
                    <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
                    <div class="wp-block-buttons">
                        <!-- wp:button {"backgroundColor":"primary","className":"is-style-fill"} -->
                        <div class="wp-block-button is-style-fill"><a class="wp-block-button__link has-primary-background-color has-background wp-element-button" href="/kontakt">Jetzt Beratung anfragen</a></div>
                        <!-- /wp:button -->
                        
                        <!-- wp:button {"className":"is-style-outline","style":{"color":{"text":"#ffffff"},"border":{"color":"#ffffff"}}} -->
                        <div class="wp-block-button is-style-outline"><a class="wp-block-button__link has-text-color has-border-color wp-element-button" style="border-color:#ffffff;color:#ffffff" href="#leistungen">Unsere Leistungen</a></div>
                        <!-- /wp:button -->
                    </div>
                    <!-- /wp:buttons -->
                    </div>
                    <!-- /wp:group -->
                </div>
                <!-- /wp:group -->
            ',
        )
    );
    
    // Services Section Pattern
    register_block_pattern(
        'riman/services-section',
        array(
            'title' => __('Services Section', 'riman-modern'),
            'description' => _x('A services section with three columns', 'Block pattern description', 'riman-modern'),
            'categories' => array('riman', 'featured'),
            'content' => '
                <!-- wp:group {"align":"full","backgroundColor":"base","className":"services-section","layout":{"type":"constrained"}} -->
                <div class="wp-block-group alignfull services-section has-base-background-color has-background">
                    <!-- wp:heading {"textAlign":"center","style":{"spacing":{"margin":{"bottom":"60px"}}}} -->
                    <h2 class="has-text-align-center" style="margin-bottom:60px">Our Services</h2>
                    <!-- /wp:heading -->
                    
                    <!-- wp:columns {"align":"wide"} -->
                    <div class="wp-block-columns alignwide">
                        <!-- wp:column -->
                        <div class="wp-block-column">
                            <!-- wp:group {"className":"service-card","layout":{"type":"constrained"}} -->
                            <div class="wp-block-group service-card">
                                <!-- wp:image {"sizeSlug":"large"} -->
                                <figure class="wp-block-image size-large"><img src="' . get_template_directory_uri() . '/assets/images/rueckbau.png" alt="Rückbaumanagement"/></figure>
                                <!-- /wp:image -->
                                
                                <!-- wp:heading {"level":3} -->
                                <h3>Rückbaumanagement</h3>
                                <!-- /wp:heading -->
                                
                                <!-- wp:paragraph -->
                                <p>Professionelle Planung und Durchführung von Rückbauarbeiten mit Fokus auf Nachhaltigkeit und Ressourcenschonung.</p>
                                <!-- /wp:paragraph -->
                            </div>
                            <!-- /wp:group -->
                        </div>
                        <!-- /wp:column -->
                        
                        <!-- wp:column -->
                        <div class="wp-block-column">
                            <!-- wp:group {"className":"service-card","layout":{"type":"constrained"}} -->
                            <div class="wp-block-group service-card">
                                <!-- wp:html -->
                                <div class="service-card-media">
                                    <video autoplay muted loop playsinline>
                                        <source src="' . get_template_directory_uri() . '/assets/videos/sanierung.mp4" type="video/mp4">
                                    </video>
                                </div>
                                <!-- /wp:html -->
                                
                                <!-- wp:heading {"level":3} -->
                                <h3>Altlastensanierung</h3>
                                <!-- /wp:heading -->
                                
                                <!-- wp:paragraph -->
                                <p>Fachgerechte Sanierung kontaminierter Flächen und Gebäude nach modernsten Standards.</p>
                                <!-- /wp:paragraph -->
                            </div>
                            <!-- /wp:group -->
                        </div>
                        <!-- /wp:column -->
                        
                        <!-- wp:column -->
                        <div class="wp-block-column">
                            <!-- wp:group {"className":"service-card","layout":{"type":"constrained"}} -->
                            <div class="wp-block-group service-card">
                                <!-- wp:image {"sizeSlug":"large"} -->
                                <figure class="wp-block-image size-large"><img src="' . get_template_directory_uri() . '/assets/images/schadstoff.png" alt="Schadstoff-Management"/></figure>
                                <!-- /wp:image -->
                                
                                <!-- wp:heading {"level":3} -->
                                <h3>Schadstoff-Management</h3>
                                <!-- /wp:heading -->
                                
                                <!-- wp:paragraph -->
                                <p>Identifikation, Bewertung und sichere Entsorgung von Schadstoffen und Gefahrstoffen.</p>
                                <!-- /wp:paragraph -->
                            </div>
                            <!-- /wp:group -->
                        </div>
                        <!-- /wp:column -->
                    </div>
                    <!-- /wp:columns -->
                </div>
                <!-- /wp:group -->
            ',
        )
    );
}
add_action('init', 'riman_register_block_patterns');

// Register additional user-friendly block patterns
function riman_register_media_patterns() {
    // Hero with Media Upload Pattern
    register_block_pattern(
        'riman/hero-media-upload',
        array(
            'title' => __('Hero mit Media Upload', 'riman-modern'),
            'description' => _x('Hero-Bereich mit Video/Bild-Upload über Media Library', 'Block pattern description', 'riman-modern'),
            'categories' => array('riman', 'featured'),
            'content' => '
                <!-- wp:cover {"dimRatio":50,"minHeight":100,"minHeightUnit":"vh","contentPosition":"center center","align":"full","className":"hero-cover-section"} -->
                <div class="wp-block-cover alignfull hero-cover-section" style="min-height:100vh">
                    <span aria-hidden="true" class="wp-block-cover__background has-background-dim"></span>
                    <div class="wp-block-cover__inner-container">
                        <!-- wp:heading {"textAlign":"center","level":1,"style":{"typography":{"fontSize":"48px","fontWeight":"300"}}} -->
                        <h1 class="has-text-align-center" style="font-size:48px;font-weight:300">RIMAN GmbH - Rückbaumanagement & Altlastensanierung</h1>
                        <!-- /wp:heading -->
                        
                        <!-- wp:paragraph {"align":"center","style":{"typography":{"fontSize":"20px"}}} -->
                        <p class="has-text-align-center" style="font-size:20px">RIMAN GmbH - Ihr Partner für nachhaltiges Rückbaumanagement und Altlastensanierung</p>
                        <!-- /wp:paragraph -->
                        
                        <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
                        <div class="wp-block-buttons">
                            <!-- wp:button {"backgroundColor":"primary"} -->
                            <div class="wp-block-button"><a class="wp-block-button__link has-primary-background-color has-background wp-element-button" href="/kontakt">Jetzt Beratung anfragen</a></div>
                            <!-- /wp:button -->
                            
                            <!-- wp:button {"className":"is-style-outline"} -->
                            <div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="#leistungen">Unsere Leistungen</a></div>
                            <!-- /wp:button -->
                        </div>
                        <!-- /wp:buttons -->
                    </div>
                </div>
                <!-- /wp:cover -->
            ',
        )
    );
    
    // Three Column Services with Media
    register_block_pattern(
        'riman/services-three-column-media',
        array(
            'title' => __('3-Spalten Services mit Media', 'riman-modern'),
            'description' => _x('Drei Service-Spalten mit Media Upload', 'Block pattern description', 'riman-modern'),
            'categories' => array('riman'),
            'content' => '
                <!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"100px","bottom":"100px"}}},"backgroundColor":"base","className":"services-section-media"} -->
                <div class="wp-block-group alignfull services-section-media has-base-background-color has-background" style="padding-top:100px;padding-bottom:100px">
                    <!-- wp:heading {"textAlign":"center","style":{"spacing":{"margin":{"bottom":"60px"}}}} -->
                    <h2 class="has-text-align-center" style="margin-bottom:60px">Our Services</h2>
                    <!-- /wp:heading -->
                    
                    <!-- wp:columns {"align":"wide"} -->
                    <div class="wp-block-columns alignwide">
                        <!-- wp:column -->
                        <div class="wp-block-column">
                            <!-- wp:group {"className":"service-card-media-upload"} -->
                            <div class="wp-block-group service-card-media-upload">
                                <!-- wp:image {"sizeSlug":"large","className":"service-image"} -->
                                <figure class="wp-block-image size-large service-image"><img src="' . get_template_directory_uri() . '/assets/images/rueckbau.png" alt=""/></figure>
                                <!-- /wp:image -->
                                
                                <!-- wp:heading {"level":3,"style":{"spacing":{"margin":{"top":"20px"}}}} -->
                                <h3 style="margin-top:20px">Rückbaumanagement</h3>
                                <!-- /wp:heading -->
                                
                                <!-- wp:paragraph -->
                                <p>Professionelle Planung und Durchführung von Rückbauarbeiten.</p>
                                <!-- /wp:paragraph -->
                            </div>
                            <!-- /wp:group -->
                        </div>
                        <!-- /wp:column -->
                        
                        <!-- wp:column -->
                        <div class="wp-block-column">
                            <!-- wp:group {"className":"service-card-media-upload"} -->
                            <div class="wp-block-group service-card-media-upload">
                                <!-- wp:video {"id":0} -->
                                <figure class="wp-block-video"></figure>
                                <!-- /wp:video -->
                                
                                <!-- wp:heading {"level":3,"style":{"spacing":{"margin":{"top":"20px"}}}} -->
                                <h3 style="margin-top:20px">Altlastensanierung</h3>
                                <!-- /wp:heading -->
                                
                                <!-- wp:paragraph -->
                                <p>Fachgerechte Sanierung kontaminierter Flächen und Gebäude.</p>
                                <!-- /wp:paragraph -->
                            </div>
                            <!-- /wp:group -->
                        </div>
                        <!-- /wp:column -->
                        
                        <!-- wp:column -->
                        <div class="wp-block-column">
                            <!-- wp:group {"className":"service-card-media-upload"} -->
                            <div class="wp-block-group service-card-media-upload">
                                <!-- wp:image {"sizeSlug":"large","className":"service-image"} -->
                                <figure class="wp-block-image size-large service-image"><img src="' . get_template_directory_uri() . '/assets/images/schadstoff.png" alt=""/></figure>
                                <!-- /wp:image -->
                                
                                <!-- wp:heading {"level":3,"style":{"spacing":{"margin":{"top":"20px"}}}} -->
                                <h3 style="margin-top:20px">Schadstoff-Management</h3>
                                <!-- /wp:heading -->
                                
                                <!-- wp:paragraph -->
                                <p>Identifikation, Bewertung und sichere Entsorgung von Schadstoffen.</p>
                                <!-- /wp:paragraph -->
                            </div>
                            <!-- /wp:group -->
                        </div>
                        <!-- /wp:column -->
                    </div>
                    <!-- /wp:columns -->
                </div>
                <!-- /wp:group -->
            ',
        )
    );
}
add_action('init', 'riman_register_media_patterns');