<?php
/**
 * Trigger Elementor CSS und HTML Regeneration
 */

// WordPress Bootstrap
define('WP_USE_THEMES', false);
require('wp-load.php');

// Prüfe ob Elementor aktiv ist
if (!did_action('elementor/loaded')) {
    die('Elementor ist nicht aktiv!');
}

echo "🔄 Triggere Elementor Regeneration für Page 3000...\n\n";

// Hole Elementor Instance
$elementor = \Elementor\Plugin::instance();

// Clear Cache
$elementor->files_manager->clear_cache();

// Regeneriere CSS für Page 3000
$post_id = 3000;

// Lösche alten CSS Cache
delete_post_meta($post_id, '_elementor_css');
delete_post_meta($post_id, '_elementor_css_time');

// Triggere CSS Generation
$css_file = new \Elementor\Core\Files\CSS\Post($post_id);
$css_file->update();

echo "✅ CSS regeneriert!\n";

// Flush Elementor Cache
\Elementor\Plugin::$instance->files_manager->clear_cache();

// Clear WordPress Cache
wp_cache_flush();

echo "✅ Cache geleert!\n";

// Regeneriere die Seite
$document = $elementor->documents->get($post_id);
if ($document) {
    // Lade die Elementor Daten
    $data = $document->get_elements_data();
    
    // Speichere sie wieder (triggert Regeneration)
    $document->save(['elements' => $data]);
    
    echo "✅ Elementor Dokument neu gespeichert!\n";
}

echo "\n✅ Regeneration abgeschlossen!\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";