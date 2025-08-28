<?php
/**
 * Manual WordPress Import Script
 * Imports XML data without WP-CLI
 */

// Set WordPress context
define('SHORTINIT', false);
require_once(__DIR__ . '/wp-config.php');
require_once(ABSPATH . 'wp-admin/includes/import.php');

if (!class_exists('WP_Import')) {
    die('WordPress Importer plugin is not installed. Please install it first.');
}

// Get XML file path from command line
$xml_file = isset($argv[1]) ? $argv[1] : 'generated/cholot-original-fixed.xml';

if (!file_exists($xml_file)) {
    die("XML file not found: $xml_file\n");
}

echo "🚀 Starting WordPress Import\n";
echo "📁 File: $xml_file\n";
echo "📊 Size: " . number_format(filesize($xml_file)) . " bytes\n\n";

// Create importer instance
$importer = new WP_Import();

// Set import options
$importer->fetch_attachments = true;  // Import media files
$importer->allow_create_users = true; // Allow creating users

// Capture output
ob_start();

try {
    // Import the file
    $importer->import($xml_file);
    $import_output = ob_get_clean();
    
    echo "✅ Import completed successfully!\n\n";
    echo "📋 Import Output:\n";
    echo "==================\n";
    echo $import_output;
    
    // Get some statistics
    $posts = wp_count_posts();
    $pages = wp_count_posts('page');
    $attachments = wp_count_posts('attachment');
    
    echo "\n📊 Import Statistics:\n";
    echo "==================\n";
    echo "Posts: " . $posts->publish . "\n";
    echo "Pages: " . $pages->publish . "\n";
    echo "Attachments: " . $attachments->inherit . "\n";
    
    echo "\n🎉 All done! Check your WordPress site.\n";
    
} catch (Exception $e) {
    ob_end_clean();
    echo "❌ Import failed: " . $e->getMessage() . "\n";
    exit(1);
}
?>