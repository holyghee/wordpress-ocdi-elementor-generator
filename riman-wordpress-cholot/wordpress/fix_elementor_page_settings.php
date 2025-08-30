<?php
/**
 * Repariert die Elementor Page Settings für Page 3000
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🔧 Repariere Elementor Page Settings...\n\n";

// Lösche korrupte Page Settings
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_page_settings'");
echo "✅ Alte Page Settings gelöscht\n";

// Lösche korrupte Page Assets
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_page_assets'");
echo "✅ Page Assets zurückgesetzt\n";

// Setze minimale valide Elementor Metadaten
$mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = 3000 AND meta_key = '_elementor_version'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor' WHERE post_id = 3000 AND meta_key = '_elementor_edit_mode'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = 'default' WHERE post_id = 3000 AND meta_key = '_elementor_template_type'");

echo "✅ Elementor Metadaten korrigiert\n";

// Lösche CSS Cache
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_inline_svg'");

echo "✅ CSS Cache gelöscht\n";

$mysqli->close();

echo "\n✅ Page Settings repariert!\n";
echo "Die Seite sollte jetzt wieder laden.\n";