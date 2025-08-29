<?php
// WordPress XML Importer ohne WP-CLI
define('WP_USE_THEMES', false);
require_once(__DIR__ . '/wp-load.php');
require_once(ABSPATH . 'wp-admin/includes/import.php');

if (!class_exists('WP_Import')) {
    $class_wp_import = ABSPATH . 'wp-content/plugins/wordpress-importer/wordpress-importer.php';
    if (file_exists($class_wp_import)) {
        require_once $class_wp_import;
    } else {
        die("WordPress Importer plugin not found. Please install it first.\n");
    }
}

$xml_file = __DIR__ . '/dynamic-elementor-output.xml';

if (!file_exists($xml_file)) {
    die("XML file not found: $xml_file\n");
}

$wp_import = new WP_Import();
$wp_import->fetch_attachments = false;
$wp_import->import($xml_file);

echo "Import completed!\n";