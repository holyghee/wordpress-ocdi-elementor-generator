<?php
/**
 * Fix Elementor Data für importierte Seiten
 */

require_once 'wp-load.php';

echo "🔧 Fixing Elementor Data für RIMAN Seiten...\n\n";

// Liste der zu fixenden Seiten
$page_ids = [2000, 2001, 2002, 2003];

foreach ($page_ids as $page_id) {
    $page = get_post($page_id);
    if (!$page) {
        echo "❌ Page $page_id nicht gefunden\n";
        continue;
    }
    
    echo "📄 Bearbeite: {$page->post_title} (ID: $page_id)\n";
    
    // Hole aktuelles Elementor Data
    $elementor_data = get_post_meta($page_id, '_elementor_data', true);
    
    if (!$elementor_data) {
        echo "   ⚠️  Keine Elementor-Daten gefunden\n";
        continue;
    }
    
    // Versuche zu dekodieren
    $decoded = json_decode($elementor_data, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        echo "   ⚠️  JSON Error: " . json_last_error_msg() . "\n";
        
        // Versuche verschiedene Fixes
        // 1. Stripslashes
        $fixed_data = stripslashes($elementor_data);
        $decoded = json_decode($fixed_data, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            // 2. Remove BOM
            $fixed_data = preg_replace('/[\x00-\x1F\x80-\xFF]/', '', $elementor_data);
            $decoded = json_decode($fixed_data, true);
        }
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            echo "   ❌ Konnte JSON nicht reparieren\n";
            
            // Als letzter Versuch: Erstelle minimale Elementor-Struktur
            $decoded = [
                [
                    'id' => uniqid(),
                    'elType' => 'section',
                    'settings' => [],
                    'elements' => [
                        [
                            'id' => uniqid(),
                            'elType' => 'column',
                            'settings' => ['_column_size' => 100],
                            'elements' => [
                                [
                                    'id' => uniqid(),
                                    'elType' => 'widget',
                                    'widgetType' => 'heading',
                                    'settings' => [
                                        'title' => $page->post_title,
                                        'header_size' => 'h1',
                                        'align' => 'center'
                                    ]
                                ],
                                [
                                    'id' => uniqid(),
                                    'elType' => 'widget',
                                    'widgetType' => 'text-editor',
                                    'settings' => [
                                        'editor' => '<p>Diese Seite wird gerade aufgebaut. Bitte schauen Sie später wieder vorbei.</p>'
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ];
            echo "   ✅ Minimale Struktur erstellt\n";
        } else {
            echo "   ✅ JSON repariert\n";
        }
    } else {
        echo "   ✅ JSON ist valide\n";
    }
    
    // Speichere bereinigtes Data
    if ($decoded && is_array($decoded)) {
        $clean_json = wp_json_encode($decoded);
        update_post_meta($page_id, '_elementor_data', $clean_json);
        
        // Stelle sicher, dass Edit Mode gesetzt ist
        update_post_meta($page_id, '_elementor_edit_mode', 'builder');
        update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');
        
        // Regeneriere CSS
        if (class_exists('\Elementor\Plugin')) {
            $css_file = \Elementor\Core\Files\CSS\Post::create($page_id);
            $css_file->update();
            echo "   ✅ CSS regeneriert\n";
        }
    }
}

// Clear Cache
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::instance()->files_manager->clear_cache();
}
wp_cache_flush();

echo "\n✅ Fertig! Bitte Seiten neu laden.\n";
?>