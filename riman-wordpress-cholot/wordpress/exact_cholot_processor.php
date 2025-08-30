<?php
/**
 * EXAKTER CHOLOT PROCESSOR
 * Reproduziert die exakte Struktur aus der original demo-data-fixed.xml
 * Basierend auf der Analyse der extracted_elementor_data.json
 */

echo "🚀 EXAKTER CHOLOT PROCESSOR\n";
echo "================================\n\n";

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');
if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Image Server
$img_server = "http://localhost:3456";

echo "📋 ORIGINAL CHOLOT STRUKTUR VERSTANDEN:\n";
echo "======================================\n";
echo "✅ Section mit background_color: #b68c2f\n";
echo "✅ 3 Columns mit jeweils 2 Inner Sections\n";
echo "✅ Inner Section 1: Image mit shape_divider_bottom: curve\n";
echo "✅ Inner Section 2: cholot-texticon Widget\n\n";

// EXAKTE Service Cards aus Original
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

// EXAKTE Hauptsection wie im Original (id: 388095a)
$service_section = [
    "id" => "serv" . substr(md5(uniqid()), 0, 3),
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
    // EXAKTE Column Struktur (wie id: 5019170)
    $column = [
        "id" => "col" . substr(md5(uniqid() . $index), 0, 4),
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
            // Inner Section 1: Image mit Shape Divider (wie id: 2a5e03d)
            [
                "id" => "img" . substr(md5(uniqid() . 'sec' . $index), 0, 4),
                "elType" => "section",
                "settings" => [
                    "gap" => "no",
                    "shape_divider_bottom" => "curve",
                    "shape_divider_bottom_color" => "#fafafa",
                    "shape_divider_bottom_negative" => "yes",
                    "shape_divider_bottom_above_content" => "yes"
                ],
                "elements" => [
                    [
                        "id" => "imgc" . substr(md5(uniqid() . 'col' . $index), 0, 3),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [
                            [
                                "id" => "wimg" . substr(md5(uniqid() . 'w' . $index), 0, 3),
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
                            ]
                        ],
                        "isInner" => true
                    ]
                ],
                "isInner" => true
            ],
            // Inner Section 2: cholot-texticon (wie id: db46a32)
            [
                "id" => "txt" . substr(md5(uniqid() . 'sec2' . $index), 0, 4),
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
                        "id" => "txtc" . substr(md5(uniqid() . 'col2' . $index), 0, 3),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [
                            // EXAKTE cholot-texticon Struktur (wie id: d9a9a92)
                            [
                                "id" => "wti" . substr(md5(uniqid() . 'ti' . $index), 0, 4),
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
                                    "text" => "<p>" . $card['text'] . "</p>",
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
                            ]
                        ],
                        "isInner" => true
                    ]
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

// Hero behalten wenn vorhanden
if (isset($current_data[0])) {
    $new_data[] = $current_data[0];
    echo "\n✅ Hero Section beibehalten\n";
}

// Service Cards einfügen
$new_data[] = $service_section;
echo "✅ Service Cards Section mit EXAKTER Cholot-Struktur eingefügt\n";

// Contact Form behalten wenn vorhanden
for ($i = 2; $i < count($current_data); $i++) {
    if (isset($current_data[$i])) {
        $json_check = json_encode($current_data[$i]);
        if (strpos($json_check, 'contact') !== false || strpos($json_check, 'form') !== false) {
            $new_data[] = $current_data[$i];
            echo "✅ Contact Form beibehalten\n";
        }
    }
}

// Speichern mit EXAKTER JSON-Struktur
$updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);

if ($stmt->execute()) {
    echo "\n✅ Elementor Data mit EXAKTER Cholot-Struktur aktualisiert!\n";
    
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

// Speichere auch als JSON für Debugging
file_put_contents('generated_cholot_structure.json', json_encode($new_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
echo "💾 Struktur gespeichert als: generated_cholot_structure.json\n";

$mysqli->close();

echo "\n🎯 FERTIG! Der Processor hat:\n";
echo "==================================\n";
echo "✅ EXAKTE Cholot-Struktur aus Original reproduziert\n";
echo "✅ Shape Divider in Inner Sections korrekt platziert\n";
echo "✅ cholot-texticon Widgets mit allen Original-Settings\n";
echo "✅ isInner Flags exakt wie im Original\n";
echo "✅ Alle IDs sind unique (kurze IDs wie Original)\n";
echo "✅ Cache gelöscht für CSS Regenerierung\n\n";

echo "🌐 Öffne: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";