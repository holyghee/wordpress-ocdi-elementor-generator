<?php
/**
 * Robuster Import mit korrekter JSON-Behandlung
 */

require_once 'wp-load.php';

echo "🚀 Robuster Template Import\n";
echo "============================\n\n";

// Helper: Lade und parse Template korrekt
function load_and_prepare_template($filename, $replacements = []) {
    $path = __DIR__ . '/block_library/' . $filename;
    
    if (!file_exists($path)) {
        echo "❌ File not found: $filename\n";
        return null;
    }
    
    // Lade Raw JSON
    $raw_json = file_get_contents($path);
    $template_data = json_decode($raw_json, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        echo "❌ JSON parse error in $filename: " . json_last_error_msg() . "\n";
        return null;
    }
    
    if (!isset($template_data['structure'])) {
        echo "❌ No structure in $filename\n";
        return null;
    }
    
    // Hole die Struktur
    $structure = $template_data['structure'];
    
    // Ersetze Platzhalter
    $json_str = json_encode($structure);
    foreach ($replacements as $key => $value) {
        $json_str = str_replace('{{' . $key . '}}', $value, $json_str);
    }
    
    // Parse zurück und regeneriere IDs
    $structure = json_decode($json_str, true);
    $structure = regenerate_element_ids($structure);
    
    return $structure;
}

// Helper: Regeneriere alle IDs
function regenerate_element_ids($element) {
    if (!is_array($element)) {
        return $element;
    }
    
    // Generiere neue ID wenn vorhanden
    if (isset($element['id'])) {
        $element['id'] = generate_unique_id();
    }
    if (isset($element['_id'])) {
        $element['_id'] = generate_unique_id();
    }
    
    // Rekursiv für alle Sub-Elemente
    foreach ($element as $key => $value) {
        if (is_array($value)) {
            $element[$key] = regenerate_element_ids($value);
        }
    }
    
    return $element;
}

// Helper: Generiere unique ID
function generate_unique_id() {
    return substr(md5(uniqid(mt_rand(), true)), 0, 7);
}

// HAUPT-IMPORT
echo "📦 Lade Templates...\n";

$elementor_sections = [];

// 1. Hero Slider
$hero = load_and_prepare_template('hero-slider_9.json', [
    'SLIDE_0_TITLE' => '25+ Jahre Erfahrung in Sanierung &amp; Umweltschutz',
    'SLIDE_0_SUBTITLE' => 'Seit 1998 Ihr zuverlässiger Partner',
    'SLIDE_0_TEXT' => 'Professionelle Lösungen für Asbest-, PCB- und Schadstoffsanierung.',
    'SLIDE_0_BUTTON' => 'Unsere Leistungen',
    'SLIDE_0_LINK' => '#services',
    'SLIDE_0_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg',
    
    'SLIDE_1_TITLE' => 'Zertifizierte Asbestsanierung',
    'SLIDE_1_SUBTITLE' => 'Nach TRGS 519',
    'SLIDE_1_TEXT' => 'Sicher und gesetzeskonform.',
    'SLIDE_1_BUTTON' => 'Mehr erfahren',
    'SLIDE_1_LINK' => '#asbest',
    'SLIDE_1_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg',
    
    'SLIDE_2_TITLE' => '',
    'SLIDE_2_SUBTITLE' => '',
    'SLIDE_2_TEXT' => '',
    'SLIDE_2_BUTTON' => '',
    'SLIDE_2_LINK' => '',
    'SLIDE_2_IMAGE' => ''
]);

if ($hero) {
    $elementor_sections[] = $hero;
    echo "✅ Hero Slider geladen\n";
}

// 2. Service Cards
$services = load_and_prepare_template('service-cards_2.json', [
    'TITLE' => 'Unsere Kernkompetenzen',
    'SUBTITLE' => 'Professionelle Sanierungslösungen',
    
    'SERVICE_0_TITLE' => 'Asbestsanierung',
    'SERVICE_0_TEXT' => 'Sichere Entfernung nach TRGS 519',
    'SERVICE_0_ICON' => 'fas fa-shield-alt',
    'SERVICE_0_SUBTITLE' => 'ZERTIFIZIERT',
    
    'SERVICE_1_TITLE' => 'PCB-Sanierung',
    'SERVICE_1_TEXT' => 'Fachgerechte Beseitigung',
    'SERVICE_1_ICON' => 'fas fa-flask',
    'SERVICE_1_SUBTITLE' => 'PROFESSIONELL',
    
    'SERVICE_2_TITLE' => 'Schimmelsanierung',
    'SERVICE_2_TEXT' => 'Nachhaltige Beseitigung',
    'SERVICE_2_ICON' => 'fas fa-bacteria',
    'SERVICE_2_SUBTITLE' => 'NACHHALTIG',
    
    'SERVICE_3_TITLE' => 'Brandschaden',
    'SERVICE_3_TEXT' => '24/7 Notdienst',
    'SERVICE_3_ICON' => 'fas fa-fire',
    'SERVICE_3_SUBTITLE' => 'SOFORT'
]);

if ($services) {
    $elementor_sections[] = $services;
    echo "✅ Service Cards geladen\n";
}

// 3. Title Section
$title = load_and_prepare_template('title-section_1.json', [
    'TITLE' => 'Warum RIMAN GmbH?',
    'SUBTITLE' => 'Ihr Partner seit 1998'
]);

if ($title) {
    $elementor_sections[] = $title;
    echo "✅ Title Section geladen\n";
}

// Prüfe ob wir Sections haben
if (empty($elementor_sections)) {
    die("\n❌ Keine Sections geladen! Abbruch.\n");
}

echo "\n📊 " . count($elementor_sections) . " Sections bereit\n";

// Erstelle/Update Page
$page_id = 2100; // Neue ID um Konflikte zu vermeiden
$existing = get_post($page_id);

if (!$existing) {
    $page_id = wp_insert_post([
        'post_title' => 'RIMAN GmbH Homepage',
        'post_content' => '',
        'post_status' => 'publish',
        'post_type' => 'page',
        'post_name' => 'riman-home-' . time()
    ]);
    echo "✅ Neue Seite erstellt: ID $page_id\n";
} else {
    echo "✅ Update existierende Seite: ID $page_id\n";
}

// WICHTIG: Speichere als sauberes JSON
$elementor_json = json_encode($elementor_sections, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

// Validiere JSON vor dem Speichern
$test_decode = json_decode($elementor_json, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    die("❌ JSON Validierung fehlgeschlagen: " . json_last_error_msg() . "\n");
}

echo "✅ JSON validiert (" . strlen($elementor_json) . " bytes)\n";

// Speichere Meta-Daten
update_post_meta($page_id, '_elementor_data', $elementor_json);
update_post_meta($page_id, '_elementor_edit_mode', 'builder');
update_post_meta($page_id, '_elementor_version', '3.17.0');
update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');

// Elementor CSS generieren
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::instance()->files_manager->clear_cache();
    
    $css_file = \Elementor\Core\Files\CSS\Post::create($page_id);
    $css_file->update();
    echo "✅ Elementor CSS generiert\n";
}

// Verification
$saved_data = get_post_meta($page_id, '_elementor_data', true);
$verify = json_decode($saved_data, true);
if ($verify && count($verify) > 0) {
    echo "\n✅ ERFOLG! Daten korrekt gespeichert\n";
    echo "   " . count($verify) . " Sections in Datenbank\n";
} else {
    echo "\n❌ FEHLER beim Speichern!\n";
}

echo "\n🎉 Import abgeschlossen!\n";
echo "👉 Öffne: http://localhost:8081/?page_id=$page_id\n";
?>