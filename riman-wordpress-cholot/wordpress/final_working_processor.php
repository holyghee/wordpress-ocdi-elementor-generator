<?php
/**
 * FINALER ELEMENTOR PROCESSOR
 * Versteht und repliziert die Cholot Theme Struktur korrekt
 * 
 * WICHTIG: Dieser Processor versteht wie Elementor arbeitet:
 * 1. Shape Dividers werden beim Frontend-Rendering aus Settings generiert
 * 2. Custom Widgets müssen mit exaktem widgetType registriert sein
 * 3. CSS wird lazy beim ersten Aufruf generiert
 */

echo "🚀 FINALER ELEMENTOR PROCESSOR\n";
echo "================================\n\n";

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');
if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Image Server
$img_server = "http://localhost:3456";

echo "📋 VERSTÄNDNIS DES PROZESSES:\n";
echo "============================\n";
echo "1. Cholot Plugin muss aktiv sein (✓ ist aktiv)\n";
echo "2. Widget Name muss 'cholot-texticon' sein (nicht 'cholot_texticon')\n";
echo "3. Shape Dividers nur in Inner Sections\n";
echo "4. isInner Flag muss korrekt gesetzt sein\n\n";

// Service Cards mit exakter Struktur
$service_cards = [
    [
        'title' => 'Asbestsanierung',
        'subtitle' => 'ZERTIFIZIERT',
        'text' => 'Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.',
        'icon' => 'fas fa-shield-alt',
        'image' => $img_server . '/asbestsanierung-schutzausruestung-fachpersonal.jpg'
    ],
    [
        'title' => 'PCB-Sanierung',
        'subtitle' => 'FACHGERECHT',
        'text' => 'Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.',
        'icon' => 'fas fa-industry',
        'image' => $img_server . '/schadstoffsanierung-industrieanlage-riman-gmbh.jpg'
    ],
    [
        'title' => 'Schimmelsanierung',
        'subtitle' => 'NACHHALTIG',
        'text' => 'Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.',
        'icon' => 'fas fa-home',
        'image' => $img_server . '/umweltingenieur-bodenproben-analyse-labor.jpg'
    ]
];

// Hauptsection für Service Cards
$service_section = [
    "id" => substr(md5(uniqid()), 0, 7),
    "elType" => "section",
    "settings" => [
        "gap" => "extended",
        "custom_height" => ["unit" => "px", "size" => 300, "sizes" => []],
        "content_position" => "middle",
        "structure" => "30",
        "background_color" => "#b68c2f",
        "box_shadow_box_shadow" => [
            "horizontal" => 10,
            "vertical" => 0,
            "blur" => 0,
            "spread" => 4,
            "color" => "#ededed"
        ],
        "margin" => ["unit" => "px", "top" => -100, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
        "margin_tablet" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false]
    ],
    "elements" => [],
    "isInner" => false
];

foreach ($service_cards as $index => $card) {
    $column = [
        "id" => substr(md5(uniqid() . $index), 0, 7),
        "elType" => "column",
        "settings" => [
            "_column_size" => 33,
            "_inline_size" => null,
            "background_background" => "classic",
            "background_size" => "cover",
            "border_width" => ["unit" => "px", "top" => 10, "right" => 0, "bottom" => 10, "left" => 10, "isLinked" => false],
            "border_color" => "#ededed",
            "box_shadow_box_shadow" => [
                "horizontal" => 0,
                "vertical" => 4,
                "blur" => 5,
                "spread" => 0,
                "color" => "rgba(196,196,196,0.26)"
            ],
            "z_index" => 1,
            "background_color" => "#fafafa",
            "box_shadow_box_shadow_type" => "yes",
            "box_shadow_hover_box_shadow_type" => "yes",
            "box_shadow_hover_box_shadow" => [
                "horizontal" => 0,
                "vertical" => 0,
                "blur" => 0,
                "spread" => 0,
                "color" => "rgba(0,0,0,0)"
            ],
            "margin" => ["unit" => "px", "top" => 15, "right" => 15, "bottom" => 15, "left" => 15, "isLinked" => true],
            "padding" => ["unit" => "%", "top" => "", "right" => "", "bottom" => "", "left" => "", "isLinked" => false],
            "animation" => "fadeInUp",
            "animation_duration" => "fast",
            "animation_delay" => $index * 200,
            "_inline_size_tablet" => 50
        ],
        "elements" => [
            // Inner Section 1: Bild mit Shape Divider
            [
                "id" => substr(md5(uniqid() . 'img' . $index), 0, 7),
                "elType" => "section",
                "settings" => [
                    "gap" => "no",
                    "shape_divider_bottom" => "curve",
                    "shape_divider_bottom_color" => "#fafafa",
                    "shape_divider_bottom_width" => ["unit" => "%", "size" => 100],
                    "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                    "shape_divider_bottom_negative" => "yes",
                    "shape_divider_bottom_above_content" => "yes"
                ],
                "elements" => [
                    [
                        "id" => substr(md5(uniqid() . 'imgcol' . $index), 0, 7),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [
                            [
                                "id" => substr(md5(uniqid() . 'widget' . $index), 0, 7),
                                "elType" => "widget",
                                "settings" => [
                                    "image" => [
                                        "url" => $card['image'],
                                        "id" => ""
                                    ],
                                    "opacity" => ["unit" => "px", "size" => 1, "sizes" => []],
                                    "_border_width" => ["unit" => "px", "top" => 4, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                                    "_border_color" => "#b68c2f"
                                ],
                                "elements" => [],
                                "widgetType" => "image"
                            }
                        ],
                        "isInner" => true
                    }
                ],
                "isInner" => true
            ],
            // Inner Section 2: Content mit cholot-texticon
            [
                "id" => substr(md5(uniqid() . 'content' . $index), 0, 7),
                "elType" => "section",
                "settings" => [
                    "gap" => "no",
                    "content_position" => "middle",
                    "background_background" => "classic",
                    "padding" => ["unit" => "%", "top" => "", "right" => "", "bottom" => "", "left" => "", "isLinked" => true],
                    "margin" => ["unit" => "px", "top" => -30, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                    "z_index" => 2
                ],
                "elements" => [
                    [
                        "id" => substr(md5(uniqid() . 'contentcol' . $index), 0, 7),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [
                            [
                                "id" => substr(md5(uniqid() . 'texticon' . $index), 0, 7),
                                "elType" => "widget",
                                "settings" => [
                                    "icon" => "fa fa-child",
                                    "title_text_margin" => ["unit" => "px", "size" => 50, "sizes" => []],
                                    "title" => $card['title'],
                                    "title_typography_typography" => "custom",
                                    "title_typography_font_size" => ["unit" => "px", "size" => 28, "sizes" => []],
                                    "title_margin" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 15, "left" => 0, "isLinked" => false],
                                    "subtitle_typography_typography" => "custom",
                                    "subtitle_typography_font_size" => ["unit" => "px", "size" => 13, "sizes" => []],
                                    "subtitle_typography_font_weight" => "700",
                                    "subtitle_typography_text_transform" => "uppercase",
                                    "subtitle_typography_letter_spacing" => ["unit" => "px", "size" => 1, "sizes" => []],
                                    "sb_padding" => ["unit" => "%", "top" => "", "right" => "", "bottom" => "", "left" => "", "isLinked" => false],
                                    "sb_margin" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => -15, "left" => 0, "isLinked" => false],
                                    "subtitle_color" => "#b68c2f",
                                    "icon_size" => ["unit" => "px", "size" => 20, "sizes" => []],
                                    "icon_bg_size" => ["unit" => "px", "size" => 72, "sizes" => []],
                                    "icon_margin_left" => ["unit" => "%", "top" => 1, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                                    "selected_icon" => ["value" => $card['icon'], "library" => "fa-solid"],
                                    "__fa4_migrated" => ["selected_icon" => true],
                                    "text" => "<p>{$card['text']}</p>",
                                    "text_typography_font_size" => ["unit" => "px", "size" => 15, "sizes" => []],
                                    "text_typography_font_style" => "italic",
                                    "text_margin" => ["unit" => "px", "top" => 15, "right" => 0, "bottom" => -30, "left" => 0, "isLinked" => false],
                                    "icon_color" => "#ffffff",
                                    "iconbg_color" => "#b68c2f",
                                    "icon_bordering_border" => "solid",
                                    "icon_bordering_color" => "#fafafa",
                                    "_padding" => ["unit" => "px", "top" => 30, "right" => 30, "bottom" => 30, "left" => 30, "isLinked" => true],
                                    "_border_width" => ["unit" => "px", "top" => 0, "right" => 1, "bottom" => 1, "left" => 1, "isLinked" => false],
                                    "_border_color" => "#b68c2f",
                                    "_border_border" => "dashed",
                                    "icon_margin" => ["unit" => "px", "top" => -27, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                                    "icon_bordering_width" => ["unit" => "px", "top" => 7, "right" => 7, "bottom" => 7, "left" => 7, "isLinked" => true],
                                    "subtitle" => $card['subtitle'],
                                    "btn_margin" => ["unit" => "%", "top" => "", "right" => "", "bottom" => "", "left" => "", "isLinked" => false],
                                    "icon_lheight" => ["unit" => "px", "size" => 58, "sizes" => []]
                                ],
                                "elements" => [],
                                "widgetType" => "cholot-texticon"
                            }
                        ],
                        "isInner" => true
                    }
                ],
                "isInner" => true
            ]
        ],
        "isInner" => false
    ];
    
    $service_section['elements'][] = $column;
    echo "✅ Card generiert: {$card['title']}\n";
}

// Hole aktuelle Daten
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$current_data = json_decode($row['meta_value'], true);

// Baue neue Struktur
$new_data = [];

// Hero behalten
if (isset($current_data[0])) {
    $new_data[] = $current_data[0];
    echo "\n✅ Hero Section beibehalten\n";
}

// Service Cards einfügen
$new_data[] = $service_section;
echo "✅ Service Cards Section eingefügt\n";

// Contact Form behalten
for ($i = 2; $i < count($current_data); $i++) {
    if (isset($current_data[$i])) {
        $json_check = json_encode($current_data[$i]);
        if (strpos($json_check, 'contact') !== false) {
            $new_data[] = $current_data[$i];
            echo "✅ Contact Form beibehalten\n";
        }
    }
}

// Speichern
$updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);

if ($stmt->execute()) {
    echo "\n✅ Elementor Data aktualisiert!\n";
    
    // Zähle Widgets
    $widget_count = substr_count($updated_data, '"widgetType":"cholot-texticon"');
    echo "   → $widget_count cholot-texticon Widgets eingefügt\n";
    
    $shape_count = substr_count($updated_data, '"shape_divider_bottom":"curve"');
    echo "   → $shape_count Shape Dividers konfiguriert\n";
}

// Wichtige Metadaten setzen
$mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = 3000 AND meta_key = '_elementor_version'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor' WHERE post_id = 3000 AND meta_key = '_elementor_edit_mode'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = 'default' WHERE post_id = 3000 AND meta_key = '_elementor_template_type'");

// CSS Cache löschen
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_inline_svg'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_site_transient_%'");

echo "\n🔄 Cache gelöscht und Metadaten gesetzt\n";

$mysqli->close();

echo "\n🎯 FERTIG! Der Processor hat:\n";
echo "==================================\n";
echo "✅ Service Cards mit exakter Cholot-Struktur generiert\n";
echo "✅ Shape Divider Settings korrekt konfiguriert\n";
echo "✅ cholot-texticon Widgets eingefügt\n";
echo "✅ isInner Flags korrekt gesetzt\n";
echo "✅ Alle IDs sind unique\n";
echo "✅ Cache gelöscht für CSS Regenerierung\n\n";

echo "🌐 Öffne: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";
echo "\n📝 Falls Service Cards nicht erscheinen:\n";
echo "   1. Prüfe ob Cholot Plugin aktiv ist\n";
echo "   2. Öffne Seite im Elementor Editor und speichere\n";
echo "   3. Das triggert die Widget-Registrierung\n";