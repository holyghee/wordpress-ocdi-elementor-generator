<?php
require_once 'wp-config.php';

// Fix Elementor data format issue
$post_id = 1000;

// Get the current elementor data
$elementor_data = get_post_meta($post_id, '_elementor_data', true);
echo "Current _elementor_data type: " . gettype($elementor_data) . "\n";
echo "Current _elementor_data length: " . strlen($elementor_data) . "\n";

// Check if it's properly formatted JSON
$decoded = json_decode($elementor_data, true);
if ($decoded === null && json_last_error() !== JSON_ERROR_NONE) {
    echo "JSON decode error: " . json_last_error_msg() . "\n";
    
    // Try to fix HTML entities
    $fixed_data = html_entity_decode($elementor_data);
    $decoded = json_decode($fixed_data, true);
    
    if ($decoded === null && json_last_error() !== JSON_ERROR_NONE) {
        echo "Still JSON error after HTML decode: " . json_last_error_msg() . "\n";
        
        // Create a minimal valid Elementor structure
        $minimal_structure = [
            [
                "id" => "riman_hero",
                "settings" => [
                    "content_width" => "boxed"
                ],
                "elements" => [
                    [
                        "id" => "riman_column",
                        "settings" => [
                            "_column_size" => "100"
                        ],
                        "elements" => [
                            [
                                "id" => "riman_heading",
                                "settings" => [
                                    "title" => "RIMAN GmbH - Sanierungsexperten",
                                    "size" => "large",
                                    "header_size" => "h1"
                                ],
                                "elements" => [],
                                "widgetType" => "heading",
                                "elType" => "widget"
                            ]
                        ],
                        "isInner" => false,
                        "elType" => "column"
                    ]
                ],
                "isInner" => false,
                "elType" => "section"
            ]
        ];
        
        echo "Creating minimal Elementor structure...\n";
        update_post_meta($post_id, '_elementor_data', wp_json_encode($minimal_structure));
        
    } else {
        echo "Fixed JSON with HTML decode, updating...\n";
        update_post_meta($post_id, '_elementor_data', wp_json_encode($decoded));
    }
} else {
    echo "JSON is valid, but checking structure...\n";
    echo "Structure: " . json_encode($decoded, JSON_PRETTY_PRINT) . "\n";
}

// Also check and fix other Elementor meta
$edit_mode = get_post_meta($post_id, '_elementor_edit_mode', true);
if (empty($edit_mode)) {
    update_post_meta($post_id, '_elementor_edit_mode', 'builder');
}

$version = get_post_meta($post_id, '_elementor_version', true);
if (empty($version)) {
    update_post_meta($post_id, '_elementor_version', '3.23.0');
}

$template_type = get_post_meta($post_id, '_elementor_template_type', true);
if (empty($template_type)) {
    update_post_meta($post_id, '_elementor_template_type', 'wp-page');
}

echo "Fixed Elementor meta data for post $post_id\n";
?>