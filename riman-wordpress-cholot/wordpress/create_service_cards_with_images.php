<?php
/**
 * Erstellt Service Cards mit Bildern im Cholot-Stil
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "📦 Erstelle Service Cards mit Bildern im Cholot-Stil\n\n";

// Service Cards Section mit Bildern und Curved Shape Dividers
$service_section = [
    "id" => "service_" . uniqid(),
    "elType" => "section",
    "settings" => [
        "content_width" => ["unit" => "px", "size" => 1140],
        "gap" => "extended",
        "padding" => ["unit" => "px", "top" => 80, "bottom" => 80],
        "background_background" => "classic",
        "background_color" => "#f8f8f8"
    ],
    "elements" => []
];

// Service Card Daten
$cards = [
    [
        'title' => 'Asbestsanierung',
        'subtitle' => 'ZERTIFIZIERT',
        'text' => 'Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.',
        'icon' => 'fas fa-shield-alt',
        'image' => 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg'
    ],
    [
        'title' => 'PCB-Sanierung',
        'subtitle' => 'FACHGERECHT',
        'text' => 'Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.',
        'icon' => 'fas fa-industry',
        'image' => 'http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung-fachgerechte-entsorgung.jpg'
    ],
    [
        'title' => 'Schimmelsanierung',
        'subtitle' => 'NACHHALTIG',
        'text' => 'Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.',
        'icon' => 'fas fa-home',
        'image' => 'http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung-praevention-nachhaltig.jpg'
    ]
];

// Erstelle 3 Service Cards
foreach ($cards as $index => $card_data) {
    $column = [
        "id" => "col_" . uniqid(),
        "elType" => "column",
        "settings" => [
            "_column_size" => 33,
            "background_background" => "classic",
            "background_color" => "#ffffff",
            "border_radius" => ["unit" => "px", "top" => 10, "right" => 10, "bottom" => 10, "left" => 10],
            "box_shadow_box_shadow_type" => "yes",
            "box_shadow_box_shadow" => [
                "horizontal" => 0,
                "vertical" => 10,
                "blur" => 30,
                "spread" => 0,
                "color" => "rgba(0,0,0,0.1)"
            ],
            "animation" => "fadeInUp",
            "animation_delay" => $index * 200,
            "margin" => ["unit" => "px", "top" => 0, "right" => 10, "bottom" => 0, "left" => 10]
        ],
        "elements" => [
            // Bild Section mit Curved Shape Divider
            [
                "id" => "img_sec_" . uniqid(),
                "elType" => "section",
                "isInner" => true,
                "settings" => [
                    "structure" => "10",
                    "gap" => "no",
                    "padding" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0],
                    "margin" => ["unit" => "px", "top" => -10, "right" => -10, "bottom" => 0, "left" => -10],
                    "background_background" => "classic",
                    "background_image" => [
                        "url" => $card_data['image'],
                        "id" => "",
                        "size" => "",
                        "alt" => $card_data['title']
                    ],
                    "background_position" => "center center",
                    "background_repeat" => "no-repeat",
                    "background_size" => "cover",
                    "min_height" => ["unit" => "px", "size" => 250],
                    "shape_divider_bottom" => "curve",
                    "shape_divider_bottom_negative" => "yes",
                    "shape_divider_bottom_color" => "#ffffff",
                    "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                    "shape_divider_bottom_flip" => "",
                    "shape_divider_bottom_above_content" => ""
                ],
                "elements" => [
                    [
                        "id" => "img_col_" . uniqid(),
                        "elType" => "column",
                        "settings" => ["_column_size" => 100],
                        "elements" => []
                    ]
                ]
            ],
            // Text Content Section
            [
                "id" => "text_sec_" . uniqid(),
                "elType" => "section",
                "isInner" => true,
                "settings" => [
                    "structure" => "10",
                    "gap" => "no",
                    "padding" => ["unit" => "px", "top" => 20, "right" => 30, "bottom" => 40, "left" => 30],
                    "margin" => ["unit" => "px", "top" => -20, "right" => 0, "bottom" => 0, "left" => 0]
                ],
                "elements" => [
                    [
                        "id" => "text_col_" . uniqid(),
                        "elType" => "column",
                        "settings" => ["_column_size" => 100],
                        "elements" => [
                            // Icon
                            [
                                "id" => "icon_" . uniqid(),
                                "elType" => "widget",
                                "widgetType" => "icon",
                                "settings" => [
                                    "selected_icon" => [
                                        "value" => $card_data['icon'],
                                        "library" => "fa-solid"
                                    ],
                                    "view" => "framed",
                                    "shape" => "circle",
                                    "size" => ["unit" => "px", "size" => 40],
                                    "align" => "center",
                                    "primary_color" => "#b68c2f",
                                    "secondary_color" => "rgba(182, 140, 47, 0.1)",
                                    "icon_space" => ["unit" => "px", "size" => 20]
                                ]
                            ],
                            // Subtitle
                            [
                                "id" => "subtitle_" . uniqid(),
                                "elType" => "widget",
                                "widgetType" => "heading",
                                "settings" => [
                                    "title" => $card_data['subtitle'],
                                    "header_size" => "h6",
                                    "align" => "center",
                                    "title_color" => "#b68c2f",
                                    "typography_typography" => "custom",
                                    "typography_font_family" => "Heebo",
                                    "typography_font_size" => ["unit" => "px", "size" => 12],
                                    "typography_font_weight" => "600",
                                    "typography_letter_spacing" => ["unit" => "px", "size" => 2]
                                ]
                            ],
                            // Title
                            [
                                "id" => "title_" . uniqid(),
                                "elType" => "widget",
                                "widgetType" => "heading",
                                "settings" => [
                                    "title" => $card_data['title'],
                                    "header_size" => "h3",
                                    "align" => "center",
                                    "title_color" => "#1f1f1f",
                                    "typography_typography" => "custom",
                                    "typography_font_family" => "Heebo",
                                    "typography_font_size" => ["unit" => "px", "size" => 24],
                                    "typography_font_weight" => "700"
                                ]
                            ],
                            // Description
                            [
                                "id" => "desc_" . uniqid(),
                                "elType" => "widget",
                                "widgetType" => "text-editor",
                                "settings" => [
                                    "editor" => "<p style='text-align: center;'>" . $card_data['text'] . "</p>",
                                    "text_color" => "#666666",
                                    "typography_typography" => "custom",
                                    "typography_font_family" => "Open Sans",
                                    "typography_font_size" => ["unit" => "px", "size" => 15],
                                    "typography_line_height" => ["unit" => "em", "size" => 1.6]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ];
    
    $service_section['elements'][] = $column;
}

// Hole aktuelle Elementor Data
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

echo "📝 Ersetze Service Cards Section...\n";

// Finde und ersetze die Service Cards Section
$new_data = [];
$service_replaced = false;

foreach ($elementor_data as $index => $section) {
    // Behalte Hero Section (erste Section mit rdn-slider)
    if ($index === 0 || (isset($section['elements'][0]['elements'][0]['widgetType']) && 
        $section['elements'][0]['elements'][0]['widgetType'] == 'rdn-slider')) {
        $new_data[] = $section;
        echo "✅ Hero Section beibehalten\n";
    }
    // Ersetze die zweite Section (Service Cards)
    elseif ($index === 1 && !$service_replaced) {
        $new_data[] = $service_section;
        $service_replaced = true;
        echo "✅ Service Cards mit Bildern ersetzt\n";
    }
    // Behalte andere Sections
    else {
        $new_data[] = $section;
    }
}

// Falls nicht ersetzt, füge nach Hero ein
if (!$service_replaced && count($new_data) > 0) {
    array_splice($new_data, 1, 0, [$service_section]);
    echo "✅ Service Cards nach Hero eingefügt\n";
}

// Speichere zurück
$updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);

if ($stmt->execute()) {
    echo "\n✅ Elementor Data erfolgreich aktualisiert!\n";
} else {
    echo "\n❌ Fehler beim Update: " . $stmt->error . "\n";
}

// Cache löschen
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = UNIX_TIMESTAMP() WHERE post_id = 3000 AND meta_key = '_elementor_data_time'");

echo "\n🎨 Service Cards mit Bildern im Cholot-Stil erstellt!\n";
echo "   - 3 Cards mit Hintergrundbildern\n";
echo "   - Curved Shape Dividers\n";
echo "   - Icons und Texte\n";
echo "   - Animationen\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Tipp: Hard Refresh mit Strg+F5\n";

$mysqli->close();