<?php
/**
 * Fügt die Shape Divider HTML Struktur korrekt in die Elementor Daten ein
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🔧 Korrigiere Shape Divider Struktur...\n\n";

// Hole aktuelle Daten
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

// Funktion zum Hinzufügen der Shape Divider HTML
function add_shape_divider_html(&$element) {
    if (isset($element['settings']) && 
        isset($element['settings']['shape_divider_bottom']) && 
        $element['settings']['shape_divider_bottom'] === 'curve') {
        
        // Füge HTML für Shape Divider hinzu
        if (!isset($element['settings']['__dynamic__'])) {
            $element['settings']['__dynamic__'] = [];
        }
        
        // Wichtig: Elementor braucht diese Settings für die HTML-Generierung
        $element['settings']['shape_divider_bottom'] = 'curve';
        $element['settings']['shape_divider_bottom_color'] = '#fafafa';
        $element['settings']['shape_divider_bottom_width'] = ['unit' => '%', 'size' => 100];
        $element['settings']['shape_divider_bottom_height'] = ['unit' => 'px', 'size' => 50];
        $element['settings']['shape_divider_bottom_negative'] = 'yes';
        $element['settings']['shape_divider_bottom_above_content'] = '';
        $element['settings']['shape_divider_bottom_flip'] = '';
    }
    
    // Rekursiv für alle Unterelemente
    if (isset($element['elements']) && is_array($element['elements'])) {
        foreach ($element['elements'] as &$child) {
            add_shape_divider_html($child);
        }
    }
}

// Verarbeite alle Sections
foreach ($elementor_data as &$section) {
    add_shape_divider_html($section);
}

// Speichern
$updated_data = json_encode($elementor_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);

if ($stmt->execute()) {
    echo "✅ Shape Divider Settings aktualisiert!\n";
} else {
    echo "❌ Fehler: " . $stmt->error . "\n";
}

// WICHTIG: Elementor CSS muss regeneriert werden
echo "\n🔄 Regeneriere Elementor CSS...\n";

// Lösche alte CSS
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");

// Lösche Elementor Cache
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_site_transient_elementor%'");

// Setze CSS Generation Time
$mysqli->query("UPDATE wp_postmeta SET meta_value = '0' WHERE post_id = 3000 AND meta_key = '_elementor_css_time'");

// Markiere als "needs regeneration"
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_controls_usage'");

// Aktiviere Shape Feature in Elementor
$features_result = $mysqli->query("SELECT option_value FROM wp_options WHERE option_name = 'elementor_experiment-e_shapes'");
if ($features_result->num_rows == 0) {
    $mysqli->query("INSERT INTO wp_options (option_name, option_value, autoload) VALUES ('elementor_experiment-e_shapes', 'active', 'yes')");
    echo "✅ Shape Feature aktiviert!\n";
} else {
    $mysqli->query("UPDATE wp_options SET option_value = 'active' WHERE option_name = 'elementor_experiment-e_shapes'");
    echo "✅ Shape Feature aktualisiert!\n";
}

// Füge Elementor Version hinzu für Compatibility
$mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = 3000 AND meta_key = '_elementor_version'");

echo "\n⚠️  WICHTIG: Die Seite muss jetzt im Elementor Editor geöffnet und gespeichert werden!\n";
echo "   Dies triggert die CSS-Regenerierung mit Shape Dividers.\n\n";
echo "Alternative: Öffne http://localhost:8081/wp-admin/post.php?post=3000&action=elementor\n";
echo "und klicke auf 'Update' um die CSS zu regenerieren.\n\n";

// Zusätzlich: Füge Custom CSS für Shape Dividers hinzu
$custom_css = '
/* Shape Divider Styles */
.elementor-shape {
    overflow: hidden;
    position: absolute;
    left: 0;
    width: 100%;
    line-height: 0;
    direction: ltr;
}
.elementor-shape-bottom {
    bottom: -1px;
}
.elementor-shape-bottom svg {
    transform: rotate(180deg);
}
.elementor-shape[data-negative="true"] svg {
    transform: rotate(180deg);
}
.elementor-shape svg {
    display: block;
    width: calc(100% + 1.3px);
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    height: auto;
}
.elementor-shape .elementor-shape-fill {
    fill: #FAFAFA;
}
';

// Füge Custom CSS zu Elementor hinzu
$custom_css_result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_page_settings'");
if ($custom_css_result && $row = $custom_css_result->fetch_assoc()) {
    $page_settings = json_decode($row['meta_value'], true);
    if (!is_array($page_settings)) {
        $page_settings = [];
    }
    $page_settings['custom_css'] = $custom_css;
    $updated_settings = json_encode($page_settings);
    $mysqli->query("UPDATE wp_postmeta SET meta_value = '$updated_settings' WHERE post_id = 3000 AND meta_key = '_elementor_page_settings'");
} else {
    $page_settings = ['custom_css' => $custom_css];
    $updated_settings = json_encode($page_settings);
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (3000, '_elementor_page_settings', '$updated_settings')");
}

echo "✅ Custom CSS für Shape Dividers hinzugefügt!\n";

$mysqli->close();

echo "\n🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";