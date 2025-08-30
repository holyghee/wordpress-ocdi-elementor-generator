<?php
require_once 'wp-config.php';

$post_id = 1000;

echo "=== Complete Elementor Fix ===\n";

// Delete all Elementor cache
echo "Clearing Elementor cache...\n";
delete_transient('elementor_remote_info_api_data_' . ELEMENTOR_VERSION);
delete_transient('elementor_activation_redirect');

// Clear post meta cache
wp_cache_delete($post_id, 'post_meta');

// Fix page settings issue
$page_settings = get_post_meta($post_id, '_elementor_page_settings', true);
echo "Current page settings type: " . gettype($page_settings) . "\n";

if (!is_array($page_settings)) {
    // If it's a string "[]", convert to empty array
    if ($page_settings === '[]' || $page_settings === '') {
        $page_settings = [];
    } else {
        // Try to decode JSON
        $decoded_settings = json_decode($page_settings, true);
        if ($decoded_settings !== null) {
            $page_settings = $decoded_settings;
        } else {
            $page_settings = [];
        }
    }
    update_post_meta($post_id, '_elementor_page_settings', $page_settings);
    echo "Fixed page settings\n";
}

// Create completely new, valid Elementor data
$new_elementor_data = [
    [
        "id" => "hero_section",
        "elType" => "section",
        "isInner" => false,
        "settings" => [
            "content_width" => "boxed",
            "gap" => "default"
        ],
        "elements" => [
            [
                "id" => "hero_column",
                "elType" => "column",
                "isInner" => false,
                "settings" => [
                    "_column_size" => 100,
                    "_inline_size" => null
                ],
                "elements" => [
                    [
                        "id" => "hero_heading",
                        "elType" => "widget",
                        "isInner" => false,
                        "widgetType" => "heading",
                        "settings" => [
                            "title" => "RIMAN GmbH - Sanierungsexperten",
                            "size" => "large",
                            "header_size" => "h1",
                            "align" => "center"
                        ]
                    ],
                    [
                        "id" => "hero_text",
                        "elType" => "widget",
                        "isInner" => false,
                        "widgetType" => "text-editor",
                        "settings" => [
                            "editor" => "Professionelle Sanierungslösungen für Ihr Zuhause"
                        ]
                    ]
                ]
            ]
        ]
    ]
];

echo "Creating new Elementor data...\n";
update_post_meta($post_id, '_elementor_data', $new_elementor_data);

// Ensure all required meta fields
update_post_meta($post_id, '_elementor_edit_mode', 'builder');
update_post_meta($post_id, '_elementor_template_type', 'wp-page');
update_post_meta($post_id, '_elementor_version', '3.23.0');

// Clear CSS cache
delete_post_meta($post_id, '_elementor_css');

// Try to regenerate CSS if Elementor is loaded
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::$instance->files_manager->clear_cache();
}

echo "Fixed all Elementor data for post $post_id\n";
echo "Try refreshing the page now.\n";
?>