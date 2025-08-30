<?php
/**
 * Implementiert die exakte Cholot Service Card Struktur mit Shape Dividers
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🎨 Implementiere exakte Cholot Service Card Struktur...\n\n";

// Image Server
$img_server = "http://localhost:3456";

// Service Cards Section - Exakte Cholot Struktur
$service_section = [
    "id" => uniqid(),
    "elType" => "section",
    "settings" => [
        "structure" => "20", // Wichtig für Layout
        "content_width" => ["unit" => "px", "size" => 1140],
        "gap" => "extended",
        "padding" => ["unit" => "px", "top" => 80, "bottom" => 80],
        "background_background" => "classic",
        "background_color" => "#f8f8f8"
    ],
    "elements" => []
];

$cards = [
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

foreach ($cards as $index => $card) {
    // Hauptcolumn für jede Card
    $column = [
        "id" => uniqid(),
        "elType" => "column",
        "settings" => [
            "_column_size" => 33,
            "_inline_size" => 33,
            "background_background" => "classic",
            "background_color" => "#ffffff",
            "animation" => "fadeInUp",
            "animation_delay" => $index * 200,
            "border_border" => "solid",
            "border_width" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0],
            "border_radius" => ["unit" => "px", "top" => 10, "right" => 10, "bottom" => 10, "left" => 10],
            "box_shadow_box_shadow_type" => "yes",
            "box_shadow_box_shadow" => [
                "horizontal" => 0,
                "vertical" => 10,
                "blur" => 30,
                "spread" => 0,
                "color" => "rgba(0,0,0,0.1)"
            ],
            "padding" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0],
            "margin" => ["unit" => "px", "top" => 0, "right" => 10, "bottom" => 30, "left" => 10]
        ],
        "elements" => [
            // Inner Section für Bild mit Shape Divider (wie in der JSON)
            [
                "id" => uniqid(),
                "elType" => "section",
                "isInner" => true,
                "settings" => [
                    "structure" => "10",
                    "layout" => "boxed",
                    "gap" => "no",
                    "height" => "default",
                    "height_inner" => "default",
                    "padding" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0],
                    "margin" => ["unit" => "px", "top" => -10, "right" => -10, "bottom" => 0, "left" => -10],
                    "shape_divider_bottom" => "curve",
                    "shape_divider_bottom_color" => "#ffffff",
                    "shape_divider_bottom_width" => ["unit" => "%", "size" => 100],
                    "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                    "shape_divider_bottom_negative" => "yes",
                    "shape_divider_bottom_above_content" => "yes",
                    "shape_divider_bottom_flip" => "",
                    "background_background" => "classic",
                    "background_image" => [
                        "url" => $card['image'],
                        "id" => "",
                        "size" => "",
                        "alt" => $card['title'],
                        "source" => "library"
                    ],
                    "background_position" => "center center",
                    "background_repeat" => "no-repeat",
                    "background_size" => "cover",
                    "background_bg_width" => ["unit" => "%", "size" => 100],
                    "min_height" => ["unit" => "px", "size" => 250],
                    "border_radius" => ["unit" => "px", "top" => 10, "right" => 10, "bottom" => 0, "left" => 10]
                ],
                "elements" => [
                    [
                        "id" => uniqid(),
                        "elType" => "column",
                        "settings" => [
                            "_column_size" => 100,
                            "_inline_size" => null
                        ],
                        "elements" => [] // Leer für Bild-Hintergrund
                    ]
                ]
            ],
            // Inner Section für Content
            [
                "id" => uniqid(),
                "elType" => "section",
                "isInner" => true,
                "settings" => [
                    "structure" => "10",
                    "layout" => "boxed",
                    "gap" => "no",
                    "padding" => ["unit" => "px", "top" => 30, "right" => 30, "bottom" => 40, "left" => 30],
                    "margin" => ["unit" => "px", "top" => -30, "right" => 0, "bottom" => 0, "left" => 0],
                    "background_background" => "classic",
                    "background_color" => "#ffffff"
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
                                "widgetType" => "cholot-texticon",
                                "settings" => [
                                    "title" => $card['title'],
                                    "subtitle" => $card['subtitle'],
                                    "text" => $card['text'],
                                    "selected_icon" => [
                                        "value" => $card['icon'],
                                        "library" => "fa-solid"
                                    ],
                                    "icon_view" => "framed",
                                    "icon_shape" => "circle",
                                    "icon_align" => "center",
                                    "icon_color" => "#b68c2f",
                                    "iconbg_color" => "rgba(182, 140, 47, 0.1)",
                                    "icon_space" => ["unit" => "px", "size" => 15],
                                    "icon_size" => ["unit" => "px", "size" => 40],
                                    "icon_padding" => ["unit" => "px", "size" => 20],
                                    "icon_rotate" => ["unit" => "deg", "size" => 0],
                                    "icon_border_width" => ["unit" => "px", "size" => 0],
                                    "title_color" => "#1f1f1f",
                                    "title_typography_typography" => "custom",
                                    "title_typography_font_family" => "Heebo",
                                    "title_typography_font_size" => ["unit" => "px", "size" => 24],
                                    "title_typography_font_weight" => "700",
                                    "title_typography_line_height" => ["unit" => "px", "size" => 30],
                                    "subtitle_color" => "#b68c2f",
                                    "subtitle_typography_typography" => "custom",
                                    "subtitle_typography_font_family" => "Heebo",
                                    "subtitle_typography_font_size" => ["unit" => "px", "size" => 12],
                                    "subtitle_typography_font_weight" => "600",
                                    "subtitle_typography_text_transform" => "uppercase",
                                    "subtitle_typography_letter_spacing" => ["unit" => "px", "size" => 2],
                                    "text_color" => "#666666",
                                    "text_typography_typography" => "custom",
                                    "text_typography_font_family" => "Open Sans",
                                    "text_typography_font_size" => ["unit" => "px", "size" => 15],
                                    "text_typography_line_height" => ["unit" => "em", "size" => 1.6],
                                    "text_align" => "center"
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
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

echo "\n🎨 Service Cards mit exakter Cholot-Struktur implementiert!\n";
echo "   ✅ Inner Sections mit Shape Dividers\n";
echo "   ✅ Curved Bottom Masks auf Bildern\n";
echo "   ✅ Cholot-TextIcon Widgets\n";
echo "   ✅ Alle Styles und Animationen\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh mit Strg+F5!\n";

$mysqli->close();