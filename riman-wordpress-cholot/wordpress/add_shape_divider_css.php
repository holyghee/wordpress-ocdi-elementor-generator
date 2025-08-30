<?php
/**
 * Fügt Shape Divider CSS und korrigiert Page Settings
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🎨 Füge Shape Divider CSS hinzu...\n\n";

// Korrigiere Page Settings
$page_settings = [];
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_page_settings'");
$settings_json = json_encode($page_settings);
$stmt->bind_param('s', $settings_json);
$stmt->execute();
echo "✅ Page Settings korrigiert\n";

// Erstelle Custom CSS Datei für Shape Dividers
$custom_css = '
/* Elementor Shape Dividers */
.elementor-shape {
    overflow: hidden;
    position: absolute;
    left: 0;
    width: 100%;
    line-height: 0;
    direction: ltr;
    z-index: 1;
}

.elementor-shape-bottom {
    bottom: -1px;
}

.elementor-shape-top {
    top: -1px;
}

.elementor-shape svg {
    display: block;
    width: calc(100% + 1.3px);
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    height: auto;
}

.elementor-shape-bottom svg {
    transform: translateX(-50%) rotateX(180deg);
}

.elementor-shape[data-negative="true"].elementor-shape-bottom svg {
    transform: translateX(-50%) rotate(180deg);
}

.elementor-shape .elementor-shape-fill {
    fill: #FAFAFA;
}

/* Service Card Specific Styles */
.elementor-inner-section[data-settings*="shape_divider_bottom"] {
    position: relative;
}

/* Curve Shape für Service Cards */
.elementor-shape-bottom[data-shape="curve"] svg {
    height: 50px;
}

/* Negative Curve */
.elementor-shape[data-negative="true"] .elementor-shape-fill {
    fill: #fafafa;
}

/* Service Card Image Container */
.elementor-widget-image {
    position: relative;
    overflow: hidden;
}

/* Pseudo-Element für Curve Effect wenn Shape Divider nicht funktioniert */
.elementor-inner-section[data-id] .elementor-widget-image::after {
    content: "";
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 50px;
    background: #fafafa;
    border-radius: 50% 50% 0 0 / 100% 100% 0 0;
    z-index: 1;
}

/* Icon Styles für Cholot TextIcon */
.elementor-widget-cholot-texticon .cholot-icon {
    width: 72px;
    height: 72px;
    line-height: 72px;
    background: #b68c2f;
    color: #ffffff;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: -27px auto 15px;
    border: 7px solid #fafafa;
    font-size: 20px;
}

/* Card Border und Shadow */
.elementor-column[data-settings*="border_width"] {
    border-style: solid;
    border-color: #ededed;
    background: #fafafa;
    box-shadow: 0 4px 5px 0 rgba(196,196,196,0.26);
    margin: 15px;
    overflow: hidden;
}

.elementor-column[data-settings*="border_width"]:hover {
    box-shadow: none;
}
';

// Speichere CSS in wp_options für global CSS
$result = $mysqli->query("SELECT option_value FROM wp_options WHERE option_name = 'elementor_custom_css'");
if ($result->num_rows > 0) {
    $mysqli->query("UPDATE wp_options SET option_value = '" . $mysqli->real_escape_string($custom_css) . "' WHERE option_name = 'elementor_custom_css'");
} else {
    $mysqli->query("INSERT INTO wp_options (option_name, option_value, autoload) VALUES ('elementor_custom_css', '" . $mysqli->real_escape_string($custom_css) . "', 'yes')");
}

echo "✅ Global Custom CSS hinzugefügt\n";

// Füge CSS auch direkt in wp_head ein über Theme Functions
$functions_file = 'wp-content/themes/cholot/functions.php';
$functions_content = file_get_contents($functions_file);

// Prüfe ob Hook bereits existiert
if (strpos($functions_content, 'cholot_shape_divider_styles') === false) {
    $hook_code = "
/* Shape Divider Styles */
add_action('wp_head', 'cholot_shape_divider_styles');
function cholot_shape_divider_styles() {
    ?>
    <style>
    $custom_css
    </style>
    <?php
}
";
    file_put_contents($functions_file, $functions_content . $hook_code);
    echo "✅ CSS Hook zu functions.php hinzugefügt\n";
}

// Füge Shape Divider HTML zu den Service Cards hinzu
echo "\n🔄 Füge Shape Divider HTML zu Service Cards...\n";

// Hole aktuelle Elementor Daten
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

// Funktion zum Hinzufügen der Shape HTML wenn Settings vorhanden
function ensure_shape_settings(&$element) {
    // Für Inner Sections mit shape_divider_bottom Setting
    if (isset($element['elType']) && $element['elType'] === 'section' && 
        isset($element['isInner']) && $element['isInner'] === true &&
        isset($element['settings']['shape_divider_bottom'])) {
        
        // Stelle sicher dass alle nötigen Settings da sind
        if (!isset($element['settings']['shape_divider_bottom_color'])) {
            $element['settings']['shape_divider_bottom_color'] = '#fafafa';
        }
        if (!isset($element['settings']['shape_divider_bottom_width'])) {
            $element['settings']['shape_divider_bottom_width'] = ['unit' => '%', 'size' => 100];
        }
        if (!isset($element['settings']['shape_divider_bottom_height'])) {
            $element['settings']['shape_divider_bottom_height'] = ['unit' => 'px', 'size' => 50];
        }
        
        echo "  ✓ Shape Divider Settings für Section gefunden\n";
    }
    
    // Rekursiv für Unterelemente
    if (isset($element['elements']) && is_array($element['elements'])) {
        foreach ($element['elements'] as &$child) {
            ensure_shape_settings($child);
        }
    }
}

// Verarbeite alle Sections
foreach ($elementor_data as &$section) {
    ensure_shape_settings($section);
}

// Speichere aktualisierte Daten
$updated_data = json_encode($elementor_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

echo "\n✅ Elementor Daten aktualisiert\n";

// Clear Cache
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_site_transient_%'");

echo "✅ Cache geleert\n";

$mysqli->close();

echo "\n🎨 Shape Divider CSS und Fallback-Styles hinzugefügt!\n";
echo "   ✅ Global CSS für Shape Dividers\n";
echo "   ✅ Fallback Pseudo-Elements für Curve Effect\n";
echo "   ✅ Cholot TextIcon Styles\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";