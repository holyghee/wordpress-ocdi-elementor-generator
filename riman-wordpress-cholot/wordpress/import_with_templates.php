<?php
/**
 * Import mit Original Block Templates aus Library
 */

require_once 'wp-load.php';

echo "🚀 Import mit Original Templates\n";
echo "================================\n\n";

// Funktion zum Laden eines Block Templates
function load_block_template($filename) {
    $path = __DIR__ . '/block_library/' . $filename;
    if (!file_exists($path)) {
        echo "❌ Template nicht gefunden: $filename\n";
        return null;
    }
    
    $json = file_get_contents($path);
    $data = json_decode($json, true);
    
    if (!$data || !isset($data['structure'])) {
        echo "❌ Ungültige Template-Struktur: $filename\n";
        return null;
    }
    
    return $data['structure'];
}

// Funktion zum Ersetzen von Platzhaltern
function replace_placeholders($data, $replacements) {
    $json = json_encode($data);
    
    foreach ($replacements as $key => $value) {
        $json = str_replace('{{' . $key . '}}', $value, $json);
    }
    
    return json_decode($json, true);
}

// Funktion zum Generieren eindeutiger IDs
function regenerate_ids($element) {
    if (is_array($element)) {
        if (isset($element['id'])) {
            $element['id'] = substr(md5(uniqid()), 0, 7);
        }
        if (isset($element['_id'])) {
            $element['_id'] = substr(md5(uniqid()), 0, 7);
        }
        
        foreach ($element as $key => $value) {
            $element[$key] = regenerate_ids($value);
        }
    }
    
    return $element;
}

// 1. Hero Slider laden
echo "📦 Lade Hero Slider Template...\n";
$hero_slider = load_block_template('hero-slider_9.json');

if ($hero_slider) {
    // Ersetze Platzhalter für Hero Slider
    $hero_replacements = [
        'SLIDE_0_TITLE' => '25+ Jahre Erfahrung in Sanierung & Umweltschutz',
        'SLIDE_0_SUBTITLE' => 'Seit 1998 Ihr zuverlässiger Partner',
        'SLIDE_0_TEXT' => 'Professionelle Lösungen für Asbest-, PCB- und Schadstoffsanierung. Wir stehen für Sicherheit, Qualität und Nachhaltigkeit.',
        'SLIDE_0_BUTTON' => 'Unsere Leistungen',
        'SLIDE_0_LINK' => '#services',
        'SLIDE_0_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg',
        
        'SLIDE_1_TITLE' => 'Zertifizierte Asbestsanierung nach TRGS 519',
        'SLIDE_1_SUBTITLE' => 'Höchste Sicherheitsstandards',
        'SLIDE_1_TEXT' => 'Als zertifizierter Fachbetrieb führen wir Asbestsanierungen sicher und gesetzeskonform durch.',
        'SLIDE_1_BUTTON' => 'Mehr erfahren',
        'SLIDE_1_LINK' => '#asbest',
        'SLIDE_1_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg',
        
        'SLIDE_2_TITLE' => 'Komplettservice aus einer Hand',
        'SLIDE_2_SUBTITLE' => 'Von Analyse bis Entsorgung',
        'SLIDE_2_TEXT' => 'Wir begleiten Sie durch den gesamten Sanierungsprozess - kompetent, zuverlässig und transparent.',
        'SLIDE_2_BUTTON' => 'Kontakt aufnehmen',
        'SLIDE_2_LINK' => '#kontakt',
        'SLIDE_2_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/schadstoffsanierung-industrieanlage-riman-gmbh.jpg'
    ];
    
    $hero_slider = replace_placeholders($hero_slider, $hero_replacements);
    $hero_slider = regenerate_ids($hero_slider);
    echo "✅ Hero Slider vorbereitet\n";
}

// 2. Service Cards laden (verwende die beste Version)
echo "📦 Lade Service Cards Template...\n";
$service_cards = load_block_template('service-cards_2.json');

if ($service_cards) {
    // Ersetze Platzhalter für Service Cards
    $service_replacements = [
        'TITLE' => 'Unsere Kernkompetenzen',
        'SUBTITLE' => 'Umfassende Sanierungslösungen aus einer Hand',
        
        'SERVICE_0_TITLE' => 'Asbestsanierung',
        'SERVICE_0_TEXT' => 'Sichere und fachgerechte Entfernung von Asbest nach TRGS 519. Zertifizierte Durchführung mit höchsten Sicherheitsstandards.',
        'SERVICE_0_ICON' => 'fas fa-shield-alt',
        'SERVICE_0_SUBTITLE' => 'ZERTIFIZIERT',
        
        'SERVICE_1_TITLE' => 'PCB-Sanierung',
        'SERVICE_1_TEXT' => 'Professionelle Beseitigung von PCB-belasteten Materialien. Umweltgerechte Entsorgung nach gesetzlichen Vorgaben.',
        'SERVICE_1_ICON' => 'fas fa-flask',
        'SERVICE_1_SUBTITLE' => 'FACHGERECHT',
        
        'SERVICE_2_TITLE' => 'Schimmelsanierung',
        'SERVICE_2_TEXT' => 'Nachhaltige Schimmelbeseitigung und Prävention. Ursachenanalyse und dauerhafte Lösungen.',
        'SERVICE_2_ICON' => 'fas fa-bacteria',
        'SERVICE_2_SUBTITLE' => 'NACHHALTIG',
        
        'SERVICE_3_TITLE' => 'Brandschaden',
        'SERVICE_3_TEXT' => 'Schnelle Hilfe bei Brand- und Wasserschäden. 24/7 Notdienst für Sofortmaßnahmen.',
        'SERVICE_3_ICON' => 'fas fa-fire',
        'SERVICE_3_SUBTITLE' => '24/7 NOTDIENST'
    ];
    
    $service_cards = replace_placeholders($service_cards, $service_replacements);
    $service_cards = regenerate_ids($service_cards);
    echo "✅ Service Cards vorbereitet\n";
}

// 3. Title Section laden
echo "📦 Lade Title Section Template...\n";
$title_section = load_block_template('title-section_1.json');

if ($title_section) {
    $title_replacements = [
        'TITLE' => 'Warum RIMAN GmbH?',
        'SUBTITLE' => 'Ihr Partner für sichere Sanierung seit 1998'
    ];
    
    $title_section = replace_placeholders($title_section, $title_replacements);
    $title_section = regenerate_ids($title_section);
    echo "✅ Title Section vorbereitet\n";
}

// 4. Team Section laden
echo "📦 Lade Team Section Template...\n";
$team_section = load_block_template('team-section_12.json');

if ($team_section) {
    $team_replacements = [
        'TITLE' => 'Unser Expertenteam',
        'SUBTITLE' => 'Kompetenz und Erfahrung für Ihre Sicherheit',
        
        'MEMBER_0_NAME' => 'Dipl.-Ing. Jürgen Fischer',
        'MEMBER_0_POSITION' => 'Geschäftsführer & Gründer',
        'MEMBER_0_BIO' => '25+ Jahre Erfahrung im Bereich Umwelt- und Sicherheitsmanagement',
        'MEMBER_0_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/dr-michael-riman-geschaeftsfuehrer.jpg',
        
        'MEMBER_1_NAME' => 'Dr. Sarah Weber',
        'MEMBER_1_POSITION' => 'Leiterin Schadstoffanalytik',
        'MEMBER_1_BIO' => 'Expertin für Asbest- und PCB-Analytik mit Laborleitung',
        'MEMBER_1_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/sabine-weber-projektleitung.jpg',
        
        'MEMBER_2_NAME' => 'Thomas Klein',
        'MEMBER_2_POSITION' => 'Projektleiter Sanierung',
        'MEMBER_2_BIO' => 'Spezialist für Großprojekte und komplexe Sanierungen',
        'MEMBER_2_IMAGE' => 'http://localhost:8081/wp-content/uploads/2025/08/thomas-mueller-technische-leitung.jpg'
    ];
    
    $team_section = replace_placeholders($team_section, $team_replacements);
    $team_section = regenerate_ids($team_section);
    echo "✅ Team Section vorbereitet\n";
}

// 5. Testimonials laden
echo "📦 Lade Testimonials Template...\n";
$testimonials = load_block_template('testimonials_5.json');

if ($testimonials) {
    $testimonial_replacements = [
        'TITLE' => 'Das sagen unsere Kunden',
        'SUBTITLE' => 'Über 2.000 zufriedene Kunden vertrauen uns',
        
        'TESTIMONIAL_0_TEXT' => 'RIMAN hat unsere Asbestsanierung professionell und termingerecht durchgeführt. Die Zusammenarbeit war vorbildlich!',
        'TESTIMONIAL_0_AUTHOR' => 'Klaus Müller',
        'TESTIMONIAL_0_POSITION' => 'Bauherr, Heidelberg',
        
        'TESTIMONIAL_1_TEXT' => 'Kompetente Beratung und saubere Ausführung. Bei der PCB-Sanierung unseres Bürogebäudes war RIMAN die richtige Wahl.',
        'TESTIMONIAL_1_AUTHOR' => 'Dr. Schmidt GmbH',
        'TESTIMONIAL_1_POSITION' => 'Geschäftsführung, Mannheim',
        
        'TESTIMONIAL_2_TEXT' => 'Schnelle Reaktion beim Brandschaden, professionelle Abwicklung mit der Versicherung. Sehr empfehlenswert!',
        'TESTIMONIAL_2_AUTHOR' => 'Familie Weber',
        'TESTIMONIAL_2_POSITION' => 'Privatkunde, Ludwigshafen'
    ];
    
    $testimonials = replace_placeholders($testimonials, $testimonial_replacements);
    $testimonials = regenerate_ids($testimonials);
    echo "✅ Testimonials vorbereitet\n";
}

// 6. Contact Form laden
echo "📦 Lade Contact Form Template...\n";
$contact_form = load_block_template('contact-form_7.json');

if ($contact_form) {
    $contact_replacements = [
        'TITLE' => 'Kostenlose Erstberatung',
        'SUBTITLE' => 'Wir beraten Sie gerne unverbindlich zu Ihrem Sanierungsprojekt'
    ];
    
    $contact_form = replace_placeholders($contact_form, $contact_replacements);
    $contact_form = regenerate_ids($contact_form);
    echo "✅ Contact Form vorbereitet\n";
}

// Kombiniere alle Sections
$elementor_data = [];

if ($hero_slider) $elementor_data[] = $hero_slider;
if ($service_cards) $elementor_data[] = $service_cards;
if ($title_section) $elementor_data[] = $title_section;
if ($team_section) $elementor_data[] = $team_section;
if ($testimonials) $elementor_data[] = $testimonials;
if ($contact_form) $elementor_data[] = $contact_form;

// Speichere in Seite
$page_id = 2000;
$page = get_post($page_id);

if (!$page) {
    $page_id = wp_insert_post([
        'post_title' => 'RIMAN GmbH - Sicher bauen, Gesund leben',
        'post_content' => '',
        'post_status' => 'publish',
        'post_type' => 'page',
        'post_name' => 'riman-homepage'
    ]);
    echo "\n✅ Neue Seite erstellt (ID: $page_id)\n";
} else {
    echo "\n✅ Update Seite (ID: $page_id)\n";
}

// Speichere Elementor Data
$json_data = wp_json_encode($elementor_data);
update_post_meta($page_id, '_elementor_data', $json_data);
update_post_meta($page_id, '_elementor_edit_mode', 'builder');
update_post_meta($page_id, '_elementor_version', '3.17.0');
update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');

// Elementor CSS regenerieren
if (class_exists('\Elementor\Plugin')) {
    $css_file = \Elementor\Core\Files\CSS\Post::create($page_id);
    $css_file->update();
    echo "✅ Elementor CSS regeneriert\n";
    
    \Elementor\Plugin::instance()->files_manager->clear_cache();
    echo "✅ Cache geleert\n";
}

// Statistik
echo "\n📊 Import-Statistik:\n";
echo "-------------------\n";
echo "✅ " . count($elementor_data) . " Sections importiert\n";

$widget_count = 0;
foreach ($elementor_data as $section) {
    if (isset($section['elements'])) {
        foreach ($section['elements'] as $column) {
            if (isset($column['elements'])) {
                $widget_count += count($column['elements']);
            }
        }
    }
}
echo "✅ $widget_count Widgets total\n";

echo "\n🎉 Import erfolgreich!\n";
echo "👉 Öffne: http://localhost:8081/?page_id=$page_id\n";
?>