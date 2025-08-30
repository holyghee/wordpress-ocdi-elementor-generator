<?php
/**
 * Fix für Elementor Kit Fehler
 * Erstellt ein Default Kit wenn keines existiert
 */

require_once('wp-load.php');

echo "🔧 Behebe Elementor Kit Problem...\n\n";

// Hole aktuelles Kit ID
$kit_id = get_option('elementor_active_kit');
echo "📊 Aktuelle Kit ID: " . ($kit_id ?: 'Keine') . "\n";

if ($kit_id) {
    // Prüfe ob Kit Post existiert
    $kit_post = get_post($kit_id);
    if (!$kit_post) {
        echo "⚠️  Kit Post mit ID $kit_id existiert nicht!\n";
        $kit_id = null;
    } else {
        echo "✅ Kit Post existiert: " . $kit_post->post_title . "\n";
    }
}

// Wenn kein gültiges Kit existiert, erstelle ein neues
if (!$kit_id) {
    echo "\n📝 Erstelle neues Default Kit...\n";
    
    // Erstelle Kit Post
    $kit_id = wp_insert_post([
        'post_title' => 'Default Kit',
        'post_type' => 'elementor_library',
        'post_status' => 'publish',
        'meta_input' => [
            '_elementor_template_type' => 'kit',
            '_elementor_edit_mode' => 'builder'
        ]
    ]);
    
    if ($kit_id) {
        // Setze als aktives Kit
        update_option('elementor_active_kit', $kit_id);
        
        // Setze Default Kit Settings
        $kit_settings = [
            'system_colors' => [
                [
                    '_id' => 'primary',
                    'title' => 'Primary',
                    'color' => '#b68c2f'
                ],
                [
                    '_id' => 'secondary',
                    'title' => 'Secondary',
                    'color' => '#1a1a1a'
                ],
                [
                    '_id' => 'text',
                    'title' => 'Text',
                    'color' => '#666666'
                ],
                [
                    '_id' => 'accent',
                    'title' => 'Accent',
                    'color' => '#C8A882'
                ]
            ],
            'system_typography' => [
                [
                    '_id' => 'primary',
                    'title' => 'Primary',
                    'typography_typography' => 'custom',
                    'typography_font_family' => 'Poppins',
                    'typography_font_weight' => '600'
                ],
                [
                    '_id' => 'secondary',
                    'title' => 'Secondary',
                    'typography_typography' => 'custom',
                    'typography_font_family' => 'Open Sans',
                    'typography_font_weight' => '400'
                ]
            ],
            'container_width' => [
                'size' => 1140,
                'unit' => 'px'
            ],
            'space_between_widgets' => [
                'size' => 20,
                'unit' => 'px'
            ]
        ];
        
        update_post_meta($kit_id, '_elementor_page_settings', $kit_settings);
        update_post_meta($kit_id, '_elementor_data', '[]');
        update_post_meta($kit_id, '_elementor_version', '3.18.3');
        
        echo "✅ Neues Default Kit erstellt (ID: $kit_id)\n";
    } else {
        echo "❌ Fehler beim Erstellen des Kits\n";
    }
}

// Bereinige Elementor Cache
delete_option('_elementor_global_css');
delete_option('elementor_css_print_method');
delete_post_meta_by_key('_elementor_css');

// Lösche alle Elementor Transients
global $wpdb;
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_elementor%'");
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_site_transient_elementor%'");

echo "\n✅ Elementor Cache bereinigt\n";

// Prüfe und erstelle notwendige Elementor Optionen
$elementor_options = [
    'elementor_cpt_support' => ['post', 'page'],
    'elementor_disable_color_schemes' => 'yes',
    'elementor_disable_typography_schemes' => 'yes',
    'elementor_load_fa4_shim' => 'yes',
    'elementor_experiment-e_dom_optimization' => 'active',
    'elementor_experiment-e_optimized_assets_loading' => 'active',
    'elementor_experiment-additional_custom_breakpoints' => 'active'
];

foreach ($elementor_options as $option => $value) {
    update_option($option, $value);
}

echo "✅ Elementor Optionen gesetzt\n";

// Erstelle Elementor Upload-Verzeichnisse
$upload_dir = wp_upload_dir();
$elementor_dirs = [
    $upload_dir['basedir'] . '/elementor',
    $upload_dir['basedir'] . '/elementor/css',
    $upload_dir['basedir'] . '/elementor/fonts',
    $upload_dir['basedir'] . '/elementor/tmp'
];

foreach ($elementor_dirs as $dir) {
    if (!file_exists($dir)) {
        wp_mkdir_p($dir);
    }
}

echo "✅ Elementor Verzeichnisse erstellt\n";

echo "\n🎉 Elementor Kit Reparatur abgeschlossen!\n";
echo "➡️  Die Plugin-Seite sollte jetzt funktionieren:\n";
echo "   http://localhost:8081/wp-admin/plugins.php\n";

// Zeige finale Kit Info
$final_kit_id = get_option('elementor_active_kit');
$final_kit = get_post($final_kit_id);
if ($final_kit) {
    echo "\n📊 Aktives Kit:\n";
    echo "   - ID: " . $final_kit_id . "\n";
    echo "   - Titel: " . $final_kit->post_title . "\n";
    echo "   - Status: " . $final_kit->post_status . "\n";
}