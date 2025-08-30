<?php
/**
 * Fix für Elementor Pro Installation Fehler
 * Behebt den TypeError in class-wp-plugins-list-table.php
 */

require_once('wp-load.php');

echo "🔧 Behebe Elementor Pro Installation Fehler...\n\n";

// 1. Bereinige recently_activated Option
$recently_activated = get_option('recently_activated', array());
echo "📊 Aktuelle recently_activated Einträge: " . count($recently_activated) . "\n";

// Bereinige ungültige Einträge
$cleaned = array();
foreach ($recently_activated as $key => $time) {
    // Stelle sicher, dass time ein Integer ist
    if (is_numeric($time)) {
        $cleaned[$key] = intval($time);
    } else {
        echo "⚠️  Entferne ungültigen Eintrag: $key => $time\n";
    }
}

// Speichere bereinigte Option
update_option('recently_activated', $cleaned);
echo "✅ recently_activated bereinigt\n\n";

// 2. Prüfe und repariere Plugin-Cache
delete_site_transient('update_plugins');
wp_clean_plugins_cache();
echo "✅ Plugin-Cache geleert\n\n";

// 3. Prüfe Elementor Installation
$active_plugins = get_option('active_plugins', array());
$elementor_found = false;
$elementor_pro_found = false;

foreach ($active_plugins as $plugin) {
    if (strpos($plugin, 'elementor/elementor.php') !== false) {
        $elementor_found = true;
        echo "✅ Elementor ist aktiv\n";
    }
    if (strpos($plugin, 'elementor-pro/elementor-pro.php') !== false) {
        $elementor_pro_found = true;
        echo "✅ Elementor Pro ist aktiv\n";
    }
}

if (!$elementor_found) {
    echo "⚠️  Elementor ist nicht aktiv\n";
}

// 4. Bereinige Elementor Transients
$wpdb = $GLOBALS['wpdb'];
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_elementor%'");
$wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_elementor%'");
echo "✅ Elementor Transients bereinigt\n\n";

// 5. Setze Elementor auf sichere Defaults
update_option('elementor_disable_typography_schemes', 'yes');
update_option('elementor_disable_color_schemes', 'yes');
update_option('elementor_load_fa4_shim', 'yes');
echo "✅ Elementor Einstellungen zurückgesetzt\n\n";

// 6. Prüfe wp-content/uploads Ordner
$upload_dir = wp_upload_dir();
if (!file_exists($upload_dir['basedir'])) {
    wp_mkdir_p($upload_dir['basedir']);
    echo "✅ Upload-Verzeichnis erstellt\n";
}

// 7. Erstelle Elementor Upload-Verzeichnisse
$elementor_upload_dir = $upload_dir['basedir'] . '/elementor';
if (!file_exists($elementor_upload_dir)) {
    wp_mkdir_p($elementor_upload_dir);
    wp_mkdir_p($elementor_upload_dir . '/css');
    wp_mkdir_p($elementor_upload_dir . '/fonts');
    echo "✅ Elementor Upload-Verzeichnisse erstellt\n";
}

echo "\n🎉 Reparatur abgeschlossen!\n";
echo "➡️  Bitte versuche jetzt erneut die Plugin-Seite zu laden:\n";
echo "   http://localhost:8081/wp-admin/plugins.php\n\n";

// Optional: Deaktiviere problematische Plugins temporär
$problematic_plugins = array();
foreach ($active_plugins as $key => $plugin) {
    if (strpos($plugin, 'elementor-pro') !== false && !file_exists(WP_PLUGIN_DIR . '/' . $plugin)) {
        echo "⚠️  Elementor Pro Plugin-Datei fehlt, deaktiviere...\n";
        unset($active_plugins[$key]);
        $problematic_plugins[] = $plugin;
    }
}

if (!empty($problematic_plugins)) {
    update_option('active_plugins', array_values($active_plugins));
    echo "✅ Problematische Plugins deaktiviert\n";
    echo "   Du kannst Elementor Pro neu installieren unter:\n";
    echo "   http://localhost:8081/wp-admin/plugin-install.php\n";
}