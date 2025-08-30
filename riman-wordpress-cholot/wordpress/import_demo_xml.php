<?php
/**
 * Importiert die demo-data-fixed.xml über WordPress Importer
 */

// WordPress Bootstrap
define('WP_USE_THEMES', false);
require('wp-load.php');

echo "📥 Importiere demo-data-fixed.xml...\n\n";

// Prüfe ob WordPress Importer aktiv ist
if (!class_exists('WP_Import')) {
    $importer_file = WP_PLUGIN_DIR . '/wordpress-importer/wordpress-importer.php';
    if (file_exists($importer_file)) {
        require_once $importer_file;
    } else {
        die("❌ WordPress Importer Plugin nicht gefunden!\n");
    }
}

// XML Datei
$xml_file = 'demo-data-fixed.xml';
if (!file_exists($xml_file)) {
    die("❌ demo-data-fixed.xml nicht gefunden!\n");
}

echo "✅ XML Datei gefunden: $xml_file\n";

// Erstelle Importer Instanz
$importer = new WP_Import();
$importer->fetch_attachments = false; // Keine Bilder importieren

// Import Options
$importer->import_start($xml_file);

echo "🔄 Starte Import...\n";

// Parse die Datei
$importer->get_authors_from_import($importer->posts);

// Map Authors (Admin User)
$importer->author_mapping[1] = 1; // Map to admin

// Prozessiere Posts
foreach ($importer->posts as $post) {
    if ($post['post_type'] == 'page' && strpos($post['post_title'], 'Home') !== false) {
        echo "   → Importiere Seite: {$post['post_title']}\n";
        
        // Hole Elementor Data aus den Metadaten
        foreach ($post['postmeta'] as $meta) {
            if ($meta['key'] == '_elementor_data') {
                $elementor_data = $meta['value'];
                
                // Zähle Widgets
                $texticon_count = substr_count($elementor_data, '"widgetType":"cholot-texticon"');
                $shape_count = substr_count($elementor_data, '"shape_divider_bottom":"curve"');
                
                echo "      ✓ $texticon_count cholot-texticon Widgets\n";
                echo "      ✓ $shape_count Shape Dividers\n";
                
                // Importiere in unsere Test DB
                $mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');
                
                // Update Page 3000 mit diesen Daten
                $stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
                $stmt->bind_param('s', $elementor_data);
                
                if ($stmt->execute()) {
                    echo "      ✅ Elementor Data importiert in Page 3000\n";
                }
                
                // Setze auch die anderen Metadaten
                $mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = 3000 AND meta_key = '_elementor_version'");
                $mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor' WHERE post_id = 3000 AND meta_key = '_elementor_edit_mode'");
                
                $mysqli->close();
                break;
            }
        }
    }
}

echo "\n✅ Import abgeschlossen!\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";