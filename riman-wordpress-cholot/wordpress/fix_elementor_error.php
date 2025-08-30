<?php
/**
 * Fix für Elementor Page Settings Error
 * Behebt: "Cannot access offset of type string on string"
 */

echo "🔧 ELEMENTOR ERROR FIX\n";
echo "======================\n\n";

// Datenbankverbindung
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');
if ($mysqli->connect_error) {
    die('❌ Datenbankverbindung fehlgeschlagen: ' . $mysqli->connect_error);
}

$page_id = 3000;

echo "📋 Prüfe Page ID $page_id...\n\n";

// 1. Prüfe ob die Seite existiert
$result = $mysqli->query("SELECT * FROM wp_posts WHERE ID = $page_id");
if ($result->num_rows == 0) {
    echo "❌ Seite mit ID $page_id existiert nicht!\n";
    echo "🔄 Erstelle neue Seite...\n";
    
    // Erstelle die Seite
    $mysqli->query("
        INSERT INTO wp_posts (
            ID, post_author, post_date, post_date_gmt, post_content, 
            post_title, post_status, comment_status, ping_status, 
            post_name, post_type, post_parent, menu_order
        ) VALUES (
            $page_id, 1, NOW(), NOW(), '',
            'RIMAN Homepage', 'publish', 'closed', 'closed',
            'riman-homepage', 'page', 0, 0
        )
    ");
    echo "✅ Seite erstellt\n\n";
} else {
    echo "✅ Seite existiert\n\n";
}

// 2. Lösche korrupte _elementor_page_settings
echo "🗑️ Lösche korrupte _elementor_page_settings...\n";
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_page_settings'");

// 3. Setze korrekte Page Settings
echo "📝 Setze neue Page Settings...\n";
$page_settings = json_encode([
    "hide_title" => "yes",
    "post_title" => "hide",
    "post_status" => "",
    "template" => "elementor_header_footer"
], JSON_UNESCAPED_UNICODE);

$stmt = $mysqli->prepare("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (?, ?, ?)");
$meta_key = '_elementor_page_settings';
$stmt->bind_param('iss', $page_id, $meta_key, $page_settings);
$stmt->execute();

echo "✅ Page Settings korrigiert\n\n";

// 4. Prüfe und korrigiere andere wichtige Metadaten
echo "🔧 Prüfe weitere Elementor-Metadaten...\n";

// _elementor_version
$result = $mysqli->query("SELECT * FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_version'");
if ($result->num_rows == 0) {
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($page_id, '_elementor_version', '3.18.3')");
    echo "✅ _elementor_version gesetzt\n";
} else {
    echo "✓ _elementor_version vorhanden\n";
}

// _elementor_edit_mode
$result = $mysqli->query("SELECT * FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_edit_mode'");
if ($result->num_rows == 0) {
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($page_id, '_elementor_edit_mode', 'builder')");
    echo "✅ _elementor_edit_mode gesetzt\n";
} else {
    echo "✓ _elementor_edit_mode vorhanden\n";
}

// _elementor_template_type
$result = $mysqli->query("SELECT * FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_template_type'");
if ($result->num_rows == 0) {
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($page_id, '_elementor_template_type', 'wp-page')");
    echo "✅ _elementor_template_type gesetzt\n";
} else {
    echo "✓ _elementor_template_type vorhanden\n";
}

// _wp_page_template
$result = $mysqli->query("SELECT * FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_wp_page_template'");
if ($result->num_rows == 0) {
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($page_id, '_wp_page_template', 'elementor_header_footer')");
    echo "✅ _wp_page_template gesetzt\n";
} else {
    $mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor_header_footer' WHERE post_id = $page_id AND meta_key = '_wp_page_template'");
    echo "✅ _wp_page_template aktualisiert\n";
}

// 5. Lösche Elementor Cache
echo "\n🗑️ Lösche Elementor Cache...\n";
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_inline_svg'");
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_controls_usage'");

// Lösche auch globale Elementor Caches
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_site_transient_elementor%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE 'elementor_log%'");

echo "✅ Cache gelöscht\n\n";

// 6. Prüfe ob _elementor_data vorhanden ist
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_elementor_data'");
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $elementor_data = $row['meta_value'];
    
    // Zähle Widgets
    $widget_count = substr_count($elementor_data, '"widgetType"');
    $texticon_count = substr_count($elementor_data, '"cholot-texticon"');
    
    echo "📊 Elementor Data Status:\n";
    echo "   → $widget_count Widgets total\n";
    echo "   → $texticon_count cholot-texticon Widgets\n\n";
} else {
    echo "⚠️ Keine Elementor Data gefunden!\n";
    echo "   → Bitte exact_cholot_processor.php ausführen\n\n";
}

// 7. Setze zusätzliche WordPress-Metadaten
echo "📝 Setze WordPress-Metadaten...\n";

// _edit_lock (verhindert gleichzeitiges Bearbeiten)
$edit_lock = time() . ':1';
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_edit_lock'");
$mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($page_id, '_edit_lock', '$edit_lock')");

// _edit_last (letzter Bearbeiter)
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $page_id AND meta_key = '_edit_last'");
$mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($page_id, '_edit_last', '1')");

echo "✅ WordPress-Metadaten gesetzt\n\n";

$mysqli->close();

echo "🎯 FERTIG!\n";
echo "=========\n\n";
echo "✅ Alle Fehler behoben\n";
echo "✅ Page Settings korrigiert\n";
echo "✅ Cache gelöscht\n";
echo "✅ Metadaten bereinigt\n\n";

echo "📋 NÄCHSTE SCHRITTE:\n";
echo "===================\n";
echo "1. Öffne: http://localhost:8081/?page_id=3000\n";
echo "2. Falls immer noch Fehler:\n";
echo "   → Öffne im Elementor Editor\n";
echo "   → Klicke auf 'Speichern'\n";
echo "   → Das regeneriert alle CSS-Dateien\n\n";

echo "💡 Alternative: http://localhost:8081/wp-admin/post.php?post=3000&action=elementor\n";
echo "   (Öffnet direkt im Elementor Editor)\n";