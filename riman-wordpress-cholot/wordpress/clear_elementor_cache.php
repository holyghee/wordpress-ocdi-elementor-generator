<?php
// Clear Elementor Cache und regeneriere CSS
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// 1. Lösche Elementor CSS Cache für die Seite
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
echo "✅ Elementor CSS Cache gelöscht\n";

// 2. Setze Elementor Data als "dirty" damit es neu generiert wird
$mysqli->query("UPDATE wp_postmeta SET meta_value = UNIX_TIMESTAMP() WHERE post_id = 3000 AND meta_key = '_elementor_data_time'");
echo "✅ Elementor Data Time aktualisiert\n";

// 3. Lösche WordPress Transients die mit Elementor zu tun haben
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_timeout_elementor%'");
echo "✅ Elementor Transients gelöscht\n";

// 4. Lösche Page Cache
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_%3000%'");
echo "✅ Page Cache gelöscht\n";

// 5. Update Elementor global CSS version um Regenerierung zu erzwingen
$mysqli->query("UPDATE wp_options SET option_value = UNIX_TIMESTAMP() WHERE option_name = 'elementor_global_css_time'");
echo "✅ Global CSS Version aktualisiert\n";

// 6. Prüfe ob _elementor_page_settings existiert und setze es ggf. neu
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_page_settings'");
if (!$result->fetch_assoc()) {
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (3000, '_elementor_page_settings', 'a:0:{}')");
    echo "✅ Page Settings initialisiert\n";
}

// 7. Wichtig: Setze auch die Template-Type
$mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor_header_footer' WHERE post_id = 3000 AND meta_key = '_wp_page_template'");
echo "✅ Template Type gesetzt\n";

echo "\n🔄 Bitte die Seite mit Strg+F5 (Hard Refresh) neu laden!\n";

$mysqli->close();