<?php
/**
 * Direct Import Script für Cholot XML Test
 * Führt Import direkt über WordPress aus
 */

// WordPress laden
require_once('wp-load.php');

// Prüfe ob WordPress geladen ist
if (!defined('ABSPATH')) {
    die('WordPress konnte nicht geladen werden');
}

// Import-Funktion
function import_cholot_xml($xml_file, $label = 'Test') {
    echo "\n" . str_repeat('=', 60) . "\n";
    echo "📥 IMPORTING: $label\n";
    echo str_repeat('=', 60) . "\n";
    
    if (!file_exists($xml_file)) {
        echo "❌ Datei nicht gefunden: $xml_file\n";
        return false;
    }
    
    // WordPress Importer laden
    if (!class_exists('WP_Import')) {
        // Lade alle benötigten Dateien
        $importer_files = [
            WP_PLUGIN_DIR . '/wordpress-importer/wordpress-importer.php',
            WP_PLUGIN_DIR . '/wordpress-importer/parsers.php',
            WP_PLUGIN_DIR . '/wordpress-importer/compat.php'
        ];
        
        foreach($importer_files as $file) {
            if (file_exists($file)) {
                require_once $file;
            }
        }
        
        // Prüfe nochmals
        if (!class_exists('WP_Import')) {
            echo "❌ WordPress Importer konnte nicht geladen werden!\n";
            return false;
        }
    }
    
    // Import durchführen
    $wp_import = new WP_Import();
    
    // Optionen setzen
    $wp_import->fetch_attachments = false; // Keine Bilder herunterladen für schnelleren Test
    
    // Authors mapping
    $wp_import->authors = array();
    
    echo "📄 Importiere XML...\n";
    
    // Capture output
    ob_start();
    $wp_import->import($xml_file);
    $output = ob_get_clean();
    
    // Prüfe ob erfolgreich
    if (strpos($output, 'All done') !== false || strpos($output, 'Have fun') !== false) {
        echo "✅ Import erfolgreich!\n";
        
        // Zähle importierte Items
        $pages = get_pages();
        $posts = get_posts(['numberposts' => -1]);
        
        echo "\n📊 Importiert:\n";
        echo "   - Seiten: " . count($pages) . "\n";
        echo "   - Posts: " . count($posts) . "\n";
        
        // Prüfe Elementor-Daten
        $elementor_pages = 0;
        foreach($pages as $page) {
            $elementor_data = get_post_meta($page->ID, '_elementor_data', true);
            if (!empty($elementor_data)) {
                $elementor_pages++;
                echo "   ✅ {$page->post_title} - Hat Elementor-Daten\n";
            } else {
                echo "   ❌ {$page->post_title} - KEINE Elementor-Daten\n";
            }
        }
        
        echo "\n📊 Ergebnis: $elementor_pages/" . count($pages) . " Seiten mit Elementor\n";
        
        return true;
    } else {
        echo "❌ Import fehlgeschlagen!\n";
        echo "Output: " . substr($output, 0, 500) . "\n";
        return false;
    }
}

// Main Execution
echo "\n";
echo "🚀 CHOLOT XML IMPORT TEST\n";
echo str_repeat('=', 60) . "\n\n";

// 1. Bereinige WordPress zuerst
echo "🧹 Bereinige WordPress...\n";
// Lösche alle Posts und Pages (außer Sample)
$posts = get_posts(['numberposts' => -1, 'post_status' => 'any']);
foreach($posts as $post) {
    wp_delete_post($post->ID, true);
}
$pages = get_pages();
foreach($pages as $page) {
    if ($page->post_title != 'Sample Page') {
        wp_delete_post($page->ID, true);
    }
}
echo "✅ WordPress bereinigt\n\n";

// 2. Teste Original Cholot XML
$original_xml = '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml';

if (file_exists($original_xml)) {
    $success = import_cholot_xml($original_xml, 'ORIGINAL CHOLOT');
    
    if ($success) {
        echo "\n✅✅✅ ORIGINAL IMPORT ERFOLGREICH ✅✅✅\n";
        
        // Liste alle Seiten mit Links
        echo "\n📄 IMPORTIERTE SEITEN:\n";
        $pages = get_pages();
        foreach($pages as $page) {
            $url = get_permalink($page->ID);
            echo "   - {$page->post_title}: $url\n";
        }
        
        echo "\n🌐 Besuche http://localhost:8082 um die importierte Seite zu sehen!\n";
        
    } else {
        echo "\n❌ Original Import fehlgeschlagen\n";
    }
} else {
    echo "❌ Original XML nicht gefunden: $original_xml\n";
}

echo "\n" . str_repeat('=', 60) . "\n";
echo "Test abgeschlossen\n";
?>