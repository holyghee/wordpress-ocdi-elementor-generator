<?php

//KIRKI OPTIONS

Kirki::add_config('cholot_config', array(
    'capability' => 'edit_theme_options',
    'option_type' => 'theme_mod',
));

//Color schemes section
Kirki::add_section('cholot_color_customizer', array(
    'title' => esc_html__('Color Settings', 'cholot_plugin'),
    'description' => esc_html__('Most of the color scheme/settings below only affect on the element/page that not using the elementor page builder.', 'cholot_plugin'),
    'priority' => 21,
));

//Fields inside color schemes

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_colorschemes',
    'label' => esc_html__('Color schemes', 'cholot_plugin'),
    'description' => esc_html__('Pick your color scheme. ', 'cholot_plugin'),
    'section' => 'cholot_color_customizer',
    'choices' => [
        'alpha' => true,
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_color_link',
    'label' => esc_html__('Hyperlink Color', 'cholot_plugin'),
    'description' => esc_html__('Pick your color for hyperlink.', 'cholot_plugin'),
    'section' => 'cholot_color_customizer',
    'choices' => [
        'alpha' => true,
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_color_link_hover',
    'label' => esc_html__('Hyperlink color on hover state', 'cholot_plugin'),
    'description' => esc_html__('Pick your color for hover state in hyperlink.', 'cholot_plugin'),
    'section' => 'cholot_color_customizer',
    'choices' => [
        'alpha' => true,
    ],
]);

//Preloader section
Kirki::add_section('cholot_preloader_section', array(
    'title' => esc_html__('Preloader Settings', 'cholot_plugin'),
    'priority' => 22,
));

//Preloader fields
Kirki::add_field('cholot_config', [
    'type' => 'select',
    'settings' => 'cholot_preloader_show',
    'label' => esc_html__('Choose Preloader setting', 'cholot_plugin'),
    'section' => 'cholot_preloader_section',
    'default' => 'hide',
    'priority' => 1,
    'multiple' => 1,
    'choices' => [
        'home' => esc_html__('Show only in homepage', 'cholot_plugin'),
        'all' => esc_html__('Show in all pages', 'cholot_plugin'),
        'hide' => esc_html__('Hide in all pages', 'cholot_plugin'),
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_bg_preloader',
    'label' => esc_html__('Preloader Background Color', 'cholot_plugin'),
    'description' => esc_html__('Choose your background color for preloader.', 'cholot_plugin'),
    'section' => 'cholot_preloader_section',
    'choices' => [
        'alpha' => true,
    ],
]);



//field in site identity

//Site branding/logo white text
Kirki::add_field('cholot_config', [
    'type' => 'image',
    'settings' => 'cholot_logo_image_white',
    'label' => esc_html__('Logo for Header White Text', 'cholot_plugin'),
    'description' => wp_kses_post('Upload your logo only for white text (standard) header here. <br/>Recommended size 240x80px', 'cholot_plugin'),
    'section' => 'title_tagline',
    'default' => '',
]);

//Site branding/logo black text
Kirki::add_field('cholot_config', [
    'type' => 'image',
    'settings' => 'cholot_logo_image',
    'label' => esc_html__('Logo for Header Black Text', 'cholot_plugin'),
    'description' => wp_kses_post('Upload your logo only for black text (standard) header here. <br/>Recommended size 240x80px', 'cholot_plugin'),
    'section' => 'title_tagline',
    'default' => '',
]);

//Social icon in header section
Kirki::add_section('cholot_customizer_header', array(
    'title' => esc_html__('Social Icon in Header', 'cholot_plugin'),
    'description' => esc_html__('Settings for the social icon in header area (standard header).', 'cholot_plugin'),
    'priority' => 23,
));

//field in social icon
Kirki::add_field('cholot_config', [
    'type' => 'text',
    'settings' => 'fb_social_head',
    'label' => esc_html__('Facebook link', 'cholot_plugin'),
    'section' => 'cholot_customizer_header',
    'description' => esc_html__('Insert your Facebook link here', 'cholot_plugin'),
    'priority' => 12,
]);
Kirki::add_field('cholot_config', [
    'type' => 'text',
    'settings' => 'lkd_social_head',
    'label' => esc_html__('Linkedin link', 'cholot_plugin'),
    'section' => 'cholot_customizer_header',
    'description' => esc_html__('Insert your Linkedin link here', 'cholot_plugin'),
    'priority' => 12,
]);
Kirki::add_field('cholot_config', [
    'type' => 'text',
    'settings' => 'tw_social_head',
    'label' => esc_html__('Twitter link', 'cholot_plugin'),
    'section' => 'cholot_customizer_header',
    'description' => esc_html__('Insert your Twitter Plus link here', 'cholot_plugin'),
    'priority' => 12,
]);
//repeater
Kirki::add_field('cholot_config', [
    'type' => 'repeater',
    'label' => esc_html__('Other Social Icon', 'cholot_plugin'),
    'description' => esc_html__('Insert the social icon.', 'cholot_plugin'),
    'section' => 'cholot_customizer_header',
    'default' => [
        [
            'link_text' => '',
            'link_url' => '',
        ],
    ],
    'priority' => 13,
    'row_label' => [
        'type' => 'text',
        'value' => esc_html__('Custom Social Icon. ', 'cholot_plugin'),
    ],
    'button_label' => esc_html__('New social icon', 'cholot_plugin'),
    'settings' => 'social_icon',
    'fields' => [
        'link_text' => [
            'type' => 'text',
            'label' => esc_html__('Social Icon', 'cholot_plugin'),
            'description' => wp_kses_post('Input your social icon here. See the list  <a href="https://fontawesome.com/v4.7.0/icons/" target="_blank">here.</a> <br>eg. <b>fa-github</b>', 'cholot_plugin'),
            'default' => '',
        ],
        'link_url' => [
            'type' => 'text',
            'label' => esc_html__('Social Icon link', 'cholot_plugin'),
            'description' => esc_html__('Insert the custom social icon link here.', 'cholot_plugin'),
            'default' => '',
        ],
    ],
]);





//BLOG PAGE SECTION
Kirki::add_section('cholot_cst_blog_page', array(
    'title' => esc_html__('Blog Settings', 'cholot_plugin'),
    'description' => esc_html__('Settings for blog page.', 'cholot_plugin'),
    'priority' => 23,
));

Kirki::add_field('cholot_config', [
    'type' => 'slider',
    'settings' => 'cholot_blog_slider_delay',
    'label' => esc_html__('Blog Slider Delay', 'cholot_plugin'),
    'description' => esc_html__('Insert the slider delay for slider in blog sidebar,blog wide and single blog post here. The default value 8000', 'cholot_plugin'),
    'section' => 'cholot_cst_blog_page',
    'default' => 8000,
    'choices' => [
        'min' => 0,
        'max' => 20000,
        'step' => 100,
    ],
]);

Kirki::add_field('cholot_config', [
    'type'        => 'select',
    'settings' => 'cholot_related_image',
    'label' => esc_html__('Featured Image in Related Posts', 'cholot_plugin'),
    'section' => 'cholot_cst_blog_page',
    'default' => 'hide',
    'priority' => 1,
    'multiple' => 1,
    'description' => wp_kses_post('Hide/show the featured images in related posts. The default value is hide.', 'cholot_plugin'),
    'choices'     => [
        'hide' => esc_html__('Hide', 'kirki'),
        'show' => esc_html__('Show', 'kirki'),
    ],
]);


Kirki::add_field('cholot_config', [
    'type' => 'background',
    'settings' => 'cholot_bg_blogs',
    'label' => esc_html__('Breadcrumb background image', 'cholot_plugin'),
    'description' => esc_html__('Upload your footer image for breadcumb here.', 'cholot_plugin'),
    'section' => 'cholot_cst_blog_page',
    'default'     => [
        'background-color'      => 'rgba(20,20,20,.8)',
        'background-image'      => '',
        'background-repeat'     => 'repeat',
        'background-position'   => 'center center',
        'background-size'       => 'cover',
        'background-attachment' => 'scroll',
    ],
    'output'      => [
        [
            'element' => '.box-crumb',
        ],
    ],
]);



//HEADER SECTION
Kirki::add_section('cholot_header_cst_settings', array(
    'title' => esc_html__('Header Settings', 'cholot_plugin'),
    'priority' => 25,
));

//CUSTOM HEADER FIELD
Kirki::add_field('cholot_config', [
    'type' => 'select',
    'settings' => 'custom_header_setting_value',
    'label' => esc_html__('Header Setting(global)', 'cholot_plugin'),
    'description' => wp_kses_post('<p>Choose Header type for all pages but you still can set different/overwrite header type for specific page in page/post settings. </p><p><b>Standard Header</b> is Black text with white background header in relative position.</p>', 'cholot_plugin'),
    'section' => 'cholot_header_cst_settings',
    'default' => 'standard',
    'priority' => 10,
    'multiple' => 1,
    'choices' => [
        'standard' => esc_html__('Standard Header', 'cholot_plugin'),
        'custom' => esc_html__('Custom Header', 'cholot_plugin'),
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'select',
    'settings' => 'cholot_select_header',
    'label' => esc_html__('Select the custom header', 'cholot_plugin'),
    'section' => 'cholot_header_cst_settings',
    'multiple' => 1,
    'placeholder' => esc_attr__('Select the header', 'kirki'),
    'choices' => Kirki_Helper::get_posts(array('post_type' => 'header')),

    //conditional/only appear in value
    'required' => array(
        array(
            'setting' => 'custom_header_setting_value',
            'value' => 'custom',
            'operator' => '==',
        ),
    ),

]);

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_all_header_bg_color',
    'label' => esc_html__('Sticky Menu Background color (for menu with black background & All Sticky Custom Menu)', 'cholot_plugin'),
    'description' => esc_html__('Pick your background color for sticky menu in white text header. Default color is #1f1f1f', 'cholot_plugin'),
    'section' => 'cholot_header_cst_settings',
    'default' => '#1f1f1f',
    'choices' => [
        'alpha' => true,
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_white_header_bg_color',
    'label' => esc_html__('Sticky Menu Background color (for menu with white background)', 'cholot_plugin'),
    'description' => esc_html__('Pick your background color for sticky menu in white text header. Default color is #ffffff', 'cholot_plugin'),
    'section' => 'cholot_header_cst_settings',
    'default' => '#ffffff',
    'choices' => [
        'alpha' => true,
    ],
]);

//FOOTER SECTION
Kirki::add_section('cholot_footer_cst_settings', array(
    'title' => esc_html__('Footer Settings', 'cholot_plugin'),
    'priority' => 26,
));

//CUSTOM FOOTER FIELD
Kirki::add_field('cholot_config', [
    'type' => 'select',
    'settings' => 'custom_footer_setting_value',
    'label' => esc_html__('Footer Setting(global)', 'cholot_plugin'),
    'description' => wp_kses_post('<p>Choose Footer type for all pages but you still can set different/overwrite footer type for specific page in page/post settings. </p><p><b>Standard Header</b> is Black text with white background header in relative position.</p>', 'cholot_plugin'),
    'section' => 'cholot_footer_cst_settings',
    'default' => 'standard',
    'priority' => 10,
    'multiple' => 1,
    'choices' => [
        'standard' => esc_html__('Standard Footer', 'cholot_plugin'),
        'custom' => esc_html__('Custom Footer', 'cholot_plugin'),
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'select',
    'settings' => 'cholot_select_footer',
    'label' => esc_html__('Select the custom footer', 'cholot_plugin'),
    'section' => 'cholot_footer_cst_settings',
    'placeholder' => esc_attr__('Select the footer', 'kirki'),
    'multiple' => 1,
    'choices' => Kirki_Helper::get_posts(array('post_type' => 'footer')),

    //conditional/only appear in value
    'required' => array(
        array(
            'setting' => 'custom_footer_setting_value',
            'value' => 'custom',
            'operator' => '==',
        ),
    ),

]);

Kirki::add_field('cholot_config', [
    'type' => 'color',
    'settings' => 'cholot_default_footer_bg_color',
    'label' => esc_html__('Standard Footer Background color', 'cholot_plugin'),
    'description' => esc_html__('Pick your background color for standard footer. Default color is black #000000', 'cholot_plugin'),
    'section' => 'cholot_footer_cst_settings',
    'default' => '#000000',
    'choices' => [
        'alpha' => true,
    ],
    //conditional/only appear in value
    'required' => array(
        array(
            'setting' => 'custom_footer_setting_value',
            'value' => 'standard',
            'operator' => '==',
        ),
    ),
]);

Kirki::add_field('cholot_config', [
    'type' => 'image',
    'settings' => 'cholot_footer_logo',
    'label' => esc_html__('Standard Footer Image', 'cholot_plugin'),
    'description' => esc_html__('Upload your footer image for standard footer here. Recommended size 240x120px', 'cholot_plugin'),
    'section' => 'cholot_footer_cst_settings',
    'default' => '',
    //conditional/only appear in value
    'required' => array(
        array(
            'setting' => 'custom_footer_setting_value',
            'value' => 'standard',
            'operator' => '==',
        ),
    ),
]);

Kirki::add_field('cholot_config', [
    'type' => 'editor',
    'settings' => 'cholot_footer_text',
    'label' => esc_html__('Standard Footer Text', 'kirki'),
    'description' => esc_html__('Input standard footer text here.', 'kirki'),
    'section' => 'cholot_footer_cst_settings',
    //conditional/only appear in value
    'required' => array(
        array(
            'setting' => 'custom_footer_setting_value',
            'value' => 'standard',
            'operator' => '==',
        ),
    ),
]);

//Social icon in footer section
Kirki::add_section('cholot_customizer_footer_icon', array(
    'title' => esc_html__('Social Icon in Footer', 'cholot_plugin'),
    'description' => esc_html__('Settings for the social icon in footer area (standard footer).', 'cholot_plugin'),
    'priority' => 27,
));

//field in social icon
Kirki::add_field('cholot_config', [
    'type' => 'text',
    'settings' => 'fb_social_foot',
    'label' => esc_html__('Facebook link', 'cholot_plugin'),
    'section' => 'cholot_customizer_footer_icon',
    'description' => esc_html__('Insert your Facebook link here', 'cholot_plugin'),
    'priority' => 12,
]);
Kirki::add_field('cholot_config', [
    'type' => 'text',
    'settings' => 'lkd_social_foot',
    'label' => esc_html__('Linkedin link', 'cholot_plugin'),
    'section' => 'cholot_customizer_footer_icon',
    'description' => esc_html__('Insert your Linkedin link here', 'cholot_plugin'),
    'priority' => 12,
]);
Kirki::add_field('cholot_config', [
    'type' => 'text',
    'settings' => 'tw_social_foot',
    'label' => esc_html__('Twitter link', 'cholot_plugin'),
    'section' => 'cholot_customizer_footer_icon',
    'description' => esc_html__('Insert your Google Plus link here', 'cholot_plugin'),
    'priority' => 12,
]);
//repeater
Kirki::add_field('cholot_config', [
    'type' => 'repeater',
    'label' => esc_html__('Other Social Icon', 'cholot_plugin'),
    'description' => esc_html__('Insert the social icon.', 'cholot_plugin'),
    'section' => 'cholot_customizer_footer_icon',
    'priority' => 13,
    'row_label' => [
        'type' => 'text',
        'value' => esc_html__('Custom Social Icon. ', 'cholot_plugin'),
    ],
    'button_label' => esc_html__('New social icon', 'cholot_plugin'),
    'default' => [
        [
            'link_text_foot' => '',
            'link_url_foot' => '',
        ],
    ],
    'settings' => 'social_icon_footer',
    'fields' => [
        'link_text_foot' => [
            'type' => 'text',
            'label' => esc_html__('Social Icon', 'cholot_plugin'),
            'description' => wp_kses_post('Input your social icon here. See the list  <a href="https://fontawesome.com/v4.7.0/icons/" target="_blank">here.</a> <br>eg. <b>fa-github</b>', 'cholot_plugin'),
            'default' => '',
        ],
        'link_url_foot' => [
            'type' => 'text',
            'label' => esc_html__('Social Icon link', 'cholot_plugin'),
            'description' => esc_html__('Insert the custom social icon link here.', 'cholot_plugin'),
            'default' => '',
        ],
    ],
]);

//TYPOGRAPHY SECTION
Kirki::add_section('cholot_cst_typography', array(
    'title' => esc_html__('Typography Settings', 'cholot_plugin'),
    'description' => wp_kses_post('<p>Some text/font only can be changed by elementor or custom css.</p> <p>You can use <b>px,em,rem</b> for Font Size/Line Height/Letter Spacing value.</p> <p>Example value: <b>15em</b></p>', 'kirki'),
    'priority' => 28,
));

//TYPOGRAPHY FIELD
Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_one',
    'label' => esc_html__('H1 Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'h1',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_two',
    'label' => esc_html__('H2 Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'h2',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_three',
    'label' => esc_html__('H3 Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'h3',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_four',
    'label' => esc_html__('H4 Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'h4',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_five',
    'label' => esc_html__('H5 Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'h5',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_five',
    'label' => esc_html__('H6 Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'h6',
        ],
    ],
]);


Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_five',
    'label' => esc_html__('Blog Title Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => '.blog-title,h1.blog-title',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_heading_five',
    'label' => esc_html__('Blog Title Font in Breadcrumb ', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Playfair Display',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => '.box-crumb .blog-title,.box-crumb  h1.blog-title',
        ],
    ],
]);

Kirki::add_field('cholot_config', [
    'type' => 'typography',
    'settings' => 'cholot_paragraph_font',
    'label' => esc_html__('Paragraph Font', 'cholot_plugin'),
    'section' => 'cholot_cst_typography',
    'default' => [
        'font-family' => 'Source Sans Pro',
        'variant' => '',
        'font-size' => '',
        'line-height' => '',
        'letter-spacing' => '',
        'color' => '',
    ],
    'transport' => 'auto',
    'output' => [
        [
            'element' => 'body',
        ],
    ],
]);