<?php
/**
 * Activate WordPress Importer Plugin
 */

// Set WordPress context
define('SHORTINIT', false);
require_once(__DIR__ . '/wp-config.php');
require_once(ABSPATH . 'wp-admin/includes/plugin.php');

// Activate the importer plugin
$plugin = 'wordpress-importer/wordpress-importer.php';

if (!is_plugin_active($plugin)) {
    activate_plugin($plugin);
    echo "✅ WordPress Importer activated!\n";
} else {
    echo "ℹ️  WordPress Importer is already active.\n";
}

// Verify that the WP_Import class is available
if (class_exists('WP_Import')) {
    echo "✅ WP_Import class is available.\n";
} else {
    echo "❌ WP_Import class is not available.\n";
}
?>