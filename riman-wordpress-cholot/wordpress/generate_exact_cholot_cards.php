<?php
/**
 * Generiert die exakte Cholot Service Card Struktur aus der demo-data-fixed.xml
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🎨 Generiere exakte Cholot Service Card Struktur...\n\n";

// Image Server
$img_server = "http://localhost:3456";

// Service Cards Section - Exakte Struktur aus demo-data-fixed.xml
$service_section = [
    "id" => uniqid(),
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
    "elements" => []
];

$cards = [
    [
        'title' => 'Asbestsanierung',
        'subtitle' => 'ZERTIFIZIERT',
        'text' => '<p>Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.</p>',
        'icon' => 'fas fa-shield-alt',
        'image' => $img_server . '/asbestsanierung-schutzausruestung-fachpersonal.jpg'
    ],
    [
        'title' => 'PCB-Sanierung',
        'subtitle' => 'FACHGERECHT',
        'text' => '<p>Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.</p>',
        'icon' => 'fas fa-industry',
        'image' => $img_server . '/schadstoffsanierung-industrieanlage-riman-gmbh.jpg'
    ],
    [
        'title' => 'Schimmelsanierung',
        'subtitle' => 'NACHHALTIG',
        'text' => '<p>Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.</p>',
        'icon' => 'fas fa-home',
        'image' => $img_server . '/umweltingenieur-bodenproben-analyse-labor.jpg'
    ]
];

foreach ($cards as $index => $card) {
    // Hauptcolumn für jede Card - Exakte Struktur aus XML
    $column = [
        "id" => uniqid(),
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
            // Inner Section 1: Bild mit Shape Divider (Exakt aus XML)
            [
                "id" => uniqid(),
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
                        "id" => uniqid(),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [
                            // Image Widget
                            [
                                "id" => uniqid(),
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
            // Inner Section 2: Content mit cholot-texticon
            [
                "id" => uniqid(),
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
                        "id" => uniqid(),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [
                            // Cholot TextIcon Widget
                            [
                                "id" => uniqid(),
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
                                    "text" => $card['text'],
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
    echo "✅ Card erstellt: " . $card['title'] . "\n";
}

// Hole aktuelle Daten
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

// Neue Struktur
$new_data = [];

// Hero behalten
if (isset($elementor_data[0])) {
    $new_data[] = $elementor_data[0];
    echo "\n✅ Hero Section beibehalten\n";
}

// Service Cards einfügen
$new_data[] = $service_section;
echo "✅ Service Cards mit exakter Cholot-Struktur eingefügt\n";

// Rest behalten (Contact Form etc.)
for ($i = 2; $i < count($elementor_data); $i++) {
    if (isset($elementor_data[$i])) {
        $json = json_encode($elementor_data[$i]);
        // Skip alte Service Cards
        if (strpos($json, 'service') === false || strpos($json, 'contact') !== false) {
            $new_data[] = $elementor_data[$i];
        }
    }
}

// Speichern
$updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);

if ($stmt->execute()) {
    echo "\n✅ Elementor Data aktualisiert!\n";
} else {
    echo "\n❌ Fehler: " . $stmt->error . "\n";
}

// Cache löschen
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = UNIX_TIMESTAMP() WHERE post_id = 3000 AND meta_key = '_elementor_data_time'");

// Elementor CSS regenerieren
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_controls_usage'");

echo "\n🎨 Service Cards mit exakter Cholot-Struktur aus demo-data-fixed.xml implementiert!\n";
echo "   ✅ Inner Sections mit shape_divider_bottom: curve\n";
echo "   ✅ shape_divider_bottom_negative: yes für Curved Mask\n";
echo "   ✅ Cholot-TextIcon Widgets mit allen Settings\n";
echo "   ✅ Exakte Border, Shadow und Animation Settings\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";

$mysqli->close();