<?php
/**
 * Kompletter Import mit allen Sections
 */

require_once 'wp-load.php';

echo "🚀 Kompletter RIMAN Import mit allen Sections\n";
echo "==============================================\n\n";

// Helper function to clean and prepare JSON
function prepare_json_structure($structure, $replacements = []) {
    // Convert to JSON string for replacement
    $json = json_encode($structure, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    
    // Replace all placeholders
    foreach ($replacements as $key => $value) {
        // Replace both {{KEY}} and {KEY} formats
        $json = str_replace('{{' . $key . '}}', $value, $json);
        $json = str_replace('{' . $key . '}', $value, $json);
    }
    
    // Also clean any remaining placeholders
    $json = preg_replace('/\{\{[A-Z_0-9]+\}\}/', '', $json);
    
    // Decode back
    $structure = json_decode($json, true);
    
    // Regenerate IDs
    return regenerate_all_ids($structure);
}

function regenerate_all_ids($element) {
    if (!is_array($element)) return $element;
    
    if (isset($element['id'])) {
        $element['id'] = substr(md5(uniqid() . mt_rand()), 0, 7);
    }
    if (isset($element['_id'])) {
        $element['_id'] = substr(md5(uniqid() . mt_rand()), 0, 7);
    }
    
    foreach ($element as $key => $value) {
        if (is_array($value)) {
            $element[$key] = regenerate_all_ids($value);
        }
    }
    
    return $element;
}

// Load template from file
function load_block_template($filename) {
    $path = __DIR__ . '/block_library/' . $filename;
    if (!file_exists($path)) {
        echo "❌ Template not found: $filename\n";
        return null;
    }
    
    $content = file_get_contents($path);
    $data = json_decode($content, true);
    
    if (!$data || !isset($data['structure'])) {
        echo "❌ Invalid template: $filename\n";
        return null;
    }
    
    return $data['structure'];
}

// Start building the page
$page_sections = [];

// 1. HERO SLIDER
echo "📦 Loading Hero Slider...\n";
$hero_template = load_block_template('hero-slider_9.json');
if ($hero_template) {
    $hero = prepare_json_structure($hero_template, [
        'SLIDE_0_TITLE' => '25+ Jahre Erfahrung in Sanierung &amp; Umweltschutz',
        'SLIDE_0_SUBTITLE' => 'Seit 1998 Ihr zuverlässiger Partner',
        'SLIDE_0_TEXT' => 'Professionelle Lösungen für Asbest-, PCB- und Schadstoffsanierung. Wir stehen für Sicherheit, Qualität und Nachhaltigkeit.',
        'SLIDE_0_BUTTON' => 'Unsere Leistungen',
        'SLIDE_0_LINK' => '#services',
        'SLIDE_0_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg',
        
        'SLIDE_1_TITLE' => 'Zertifizierte Asbestsanierung nach TRGS 519',
        'SLIDE_1_SUBTITLE' => 'Höchste Sicherheitsstandards',
        'SLIDE_1_TEXT' => 'Als zertifizierter Fachbetrieb führen wir Asbestsanierungen sicher und gesetzeskonform durch.',
        'SLIDE_1_BUTTON' => 'Mehr erfahren',
        'SLIDE_1_LINK' => '/asbestsanierung',
        'SLIDE_1_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg',
        
        'SLIDE_2_TITLE' => 'Komplettservice aus einer Hand',
        'SLIDE_2_SUBTITLE' => 'Von der Analyse bis zur Entsorgung',
        'SLIDE_2_TEXT' => 'Wir begleiten Sie durch den gesamten Sanierungsprozess mit höchster Kompetenz.',
        'SLIDE_2_BUTTON' => 'Kontakt',
        'SLIDE_2_LINK' => '/kontakt',
        'SLIDE_2_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/schadstoffsanierung-industrieanlage-riman-gmbh.jpg'
    ]);
    $page_sections[] = $hero;
    echo "✅ Hero Slider loaded\n";
}

// 2. SERVICE CARDS - Use the correct template
echo "📦 Loading Service Cards...\n";
$service_template = load_block_template('service-cards_2.json');
if ($service_template) {
    // Important: Replace ALL service placeholders
    $services = prepare_json_structure($service_template, [
        'TITLE' => 'Unsere Kernkompetenzen',
        'SUBTITLE' => 'Umfassende Sanierungslösungen',
        
        // Service 1
        'SERVICE_0_TITLE' => 'Asbestsanierung',
        'SERVICE_0_TEXT' => 'Sichere und fachgerechte Entfernung von Asbest nach TRGS 519',
        'SERVICE_0_ICON' => 'fas fa-shield-alt',
        'SERVICE_0_SUBTITLE' => 'ZERTIFIZIERT',
        'SERVICE_TITLE' => 'Asbestsanierung', // Fallback
        'SERVICE_TEXT' => 'Sichere und fachgerechte Entfernung von Asbest nach TRGS 519',
        
        // Service 2
        'SERVICE_1_TITLE' => 'PCB-Sanierung',
        'SERVICE_1_TEXT' => 'Professionelle Beseitigung von PCB-belasteten Materialien',
        'SERVICE_1_ICON' => 'fas fa-flask',
        'SERVICE_1_SUBTITLE' => 'FACHGERECHT',
        
        // Service 3
        'SERVICE_2_TITLE' => 'Schimmelsanierung',
        'SERVICE_2_TEXT' => 'Nachhaltige Schimmelbeseitigung und Prävention',
        'SERVICE_2_ICON' => 'fas fa-bacteria',
        'SERVICE_2_SUBTITLE' => 'NACHHALTIG',
        
        // Service 4
        'SERVICE_3_TITLE' => 'Brandschaden',
        'SERVICE_3_TEXT' => 'Schnelle Hilfe bei Brand- und Wasserschäden',
        'SERVICE_3_ICON' => 'fas fa-fire',
        'SERVICE_3_SUBTITLE' => '24/7 NOTDIENST',
        
        // Service 5
        'SERVICE_4_TITLE' => 'Schadstoffanalyse',
        'SERVICE_4_TEXT' => 'Umfassende Untersuchung und Bewertung',
        'SERVICE_4_ICON' => 'fas fa-microscope',
        'SERVICE_4_SUBTITLE' => 'PRÄZISE',
        
        // Service 6
        'SERVICE_5_TITLE' => 'Entsorgung',
        'SERVICE_5_TEXT' => 'Fachgerechte Entsorgung nach Vorschrift',
        'SERVICE_5_ICON' => 'fas fa-recycle',
        'SERVICE_5_SUBTITLE' => 'UMWELTGERECHT'
    ]);
    $page_sections[] = $services;
    echo "✅ Service Cards loaded\n";
}

// 3. TITLE SECTION
echo "📦 Loading Title Section...\n";
$title_template = load_block_template('title-section_1.json');
if ($title_template) {
    $title = prepare_json_structure($title_template, [
        'TITLE' => 'Warum RIMAN GmbH?',
        'SUBTITLE' => 'Ihr Partner für sichere Sanierung seit 1998'
    ]);
    $page_sections[] = $title;
    echo "✅ Title Section loaded\n";
}

// 4. SECOND SERVICE CARDS (Benefits)
echo "📦 Loading Benefits Section...\n";
$benefits_template = load_block_template('service-cards_6.json');
if ($benefits_template) {
    $benefits = prepare_json_structure($benefits_template, [
        'TITLE' => 'Ihre Vorteile',
        'SUBTITLE' => 'Das macht uns aus',
        
        'SERVICE_0_TITLE' => '25+ Jahre Erfahrung',
        'SERVICE_0_TEXT' => 'Über 2.000 erfolgreich abgeschlossene Projekte',
        'SERVICE_0_ICON' => 'fas fa-award',
        
        'SERVICE_1_TITLE' => 'Zertifizierte Experten',
        'SERVICE_1_TEXT' => 'TRGS 519, ISO 9001 und weitere Qualifikationen',
        'SERVICE_1_ICON' => 'fas fa-certificate',
        
        'SERVICE_2_TITLE' => 'Komplettservice',
        'SERVICE_2_TEXT' => 'Von der Analyse bis zur Entsorgung - alles aus einer Hand',
        'SERVICE_2_ICON' => 'fas fa-check-circle',
        
        'SERVICE_3_TITLE' => '24/7 Notdienst',
        'SERVICE_3_TEXT' => 'Im Notfall sind wir rund um die Uhr für Sie da',
        'SERVICE_3_ICON' => 'fas fa-phone-volume'
    ]);
    $page_sections[] = $benefits;
    echo "✅ Benefits Section loaded\n";
}

// 5. TEAM SECTION
echo "📦 Loading Team Section...\n";
$team_template = load_block_template('team-section_12.json');
if ($team_template) {
    $team = prepare_json_structure($team_template, [
        'TITLE' => 'Unser Expertenteam',
        'SUBTITLE' => 'Kompetenz und Erfahrung',
        
        'MEMBER_0_NAME' => 'Dipl.-Ing. Jürgen Fischer',
        'MEMBER_0_POSITION' => 'Geschäftsführer &amp; Gründer',
        'MEMBER_0_BIO' => '25+ Jahre Erfahrung im Bereich Umwelt- und Sicherheitsmanagement',
        'MEMBER_0_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/dr-michael-riman-geschaeftsfuehrer.jpg',
        
        'MEMBER_1_NAME' => 'Dr. Sarah Weber',
        'MEMBER_1_POSITION' => 'Leiterin Schadstoffanalytik',
        'MEMBER_1_BIO' => 'Expertin für Asbest- und PCB-Analytik',
        'MEMBER_1_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/sabine-weber-projektleitung.jpg',
        
        'MEMBER_2_NAME' => 'Thomas Klein',
        'MEMBER_2_POSITION' => 'Projektleiter Sanierung',
        'MEMBER_2_BIO' => 'Spezialist für Großprojekte',
        'MEMBER_2_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/thomas-mueller-technische-leitung.jpg'
    ]);
    $page_sections[] = $team;
    echo "✅ Team Section loaded\n";
}

// 6. TESTIMONIALS
echo "📦 Loading Testimonials...\n";
$testimonials_template = load_block_template('testimonials_5.json');
if ($testimonials_template) {
    $testimonials = prepare_json_structure($testimonials_template, [
        'TITLE' => 'Das sagen unsere Kunden',
        'SUBTITLE' => 'Über 2.000 zufriedene Kunden',
        
        'TESTIMONIAL_0_TEXT' => 'RIMAN hat unsere Asbestsanierung professionell und termingerecht durchgeführt.',
        'TESTIMONIAL_0_AUTHOR' => 'Klaus Müller',
        'TESTIMONIAL_0_POSITION' => 'Bauherr, Heidelberg',
        
        'TESTIMONIAL_1_TEXT' => 'Kompetente Beratung und saubere Ausführung bei der PCB-Sanierung.',
        'TESTIMONIAL_1_AUTHOR' => 'Dr. Schmidt GmbH',
        'TESTIMONIAL_1_POSITION' => 'Mannheim',
        
        'TESTIMONIAL_2_TEXT' => 'Schnelle Reaktion beim Brandschaden, sehr empfehlenswert!',
        'TESTIMONIAL_2_AUTHOR' => 'Familie Weber',
        'TESTIMONIAL_2_POSITION' => 'Ludwigshafen'
    ]);
    $page_sections[] = $testimonials;
    echo "✅ Testimonials loaded\n";
}

// 7. CONTACT FORM
echo "📦 Loading Contact Form...\n";
$contact_template = load_block_template('contact-form_7.json');
if ($contact_template) {
    $contact = prepare_json_structure($contact_template, [
        'TITLE' => 'Kostenlose Erstberatung',
        'SUBTITLE' => 'Wir beraten Sie gerne unverbindlich'
    ]);
    $page_sections[] = $contact;
    echo "✅ Contact Form loaded\n";
}

// SAVE TO DATABASE
echo "\n💾 Saving to database...\n";

// Create new page
$page_id = wp_insert_post([
    'post_title' => 'RIMAN GmbH - Komplett',
    'post_content' => '',
    'post_status' => 'publish',
    'post_type' => 'page',
    'post_name' => 'riman-komplett-' . time()
]);

echo "✅ Created page ID: $page_id\n";

// Save Elementor data
$elementor_json = json_encode($page_sections, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

// Validate JSON
$test = json_decode($elementor_json, true);
if (json_last_error() === JSON_ERROR_NONE && !empty($test)) {
    update_post_meta($page_id, '_elementor_data', $elementor_json);
    update_post_meta($page_id, '_elementor_edit_mode', 'builder');
    update_post_meta($page_id, '_elementor_version', '3.17.0');
    update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');
    
    echo "✅ Elementor data saved (" . strlen($elementor_json) . " bytes)\n";
    echo "✅ " . count($page_sections) . " sections saved\n";
} else {
    echo "❌ JSON validation failed!\n";
}

// Generate CSS
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::instance()->files_manager->clear_cache();
    $css_file = \Elementor\Core\Files\CSS\Post::create($page_id);
    $css_file->update();
    echo "✅ CSS generated\n";
}

echo "\n🎉 IMPORT COMPLETE!\n";
echo "👉 Open: http://localhost:8081/?page_id=$page_id\n";
?>