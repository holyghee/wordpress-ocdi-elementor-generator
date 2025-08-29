<?php
// Komplette Service Cards mit exakter Cholot Struktur
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Exakte Cholot Service Cards Struktur
$service_cards = [
    "id" => "388095a",
    "elType" => "section",
    "settings" => [
        "content_width" => ["unit" => "px", "size" => 1140, "sizes" => []],
        "gap" => "extended"
    ],
    "elements" => [
        // Card 1 - Asbestsanierung
        [
            "id" => "5019170",
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "_widget_size" => 33,
                "background_background" => "classic",
                "animation" => "fadeInUp"
            ],
            "elements" => [
                // Inner Section mit Bild und Shape
                [
                    "id" => "2a5e03d",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "background_background" => "classic",
                        "background_image" => [
                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg",
                            "id" => "",
                            "size" => ""
                        ],
                        "background_position" => "center center",
                        "background_repeat" => "no-repeat",
                        "background_size" => "cover",
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#FFFFFF",
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 150, "bottom" => 50, "left" => 0, "right" => 0]
                    ],
                    "elements" => [
                        [
                            "id" => "61e7066",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => []
                        ]
                    ]
                ],
                // Inner Section mit Text
                [
                    "id" => "db46a32",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "background_background" => "classic",
                        "background_color" => "#FFFFFF",
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 30, "bottom" => 40, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "17f1f3e",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "d9a9a92",
                                    "elType" => "widget",
                                    "widgetType" => "cholot-texticon",
                                    "settings" => [
                                        "title" => "Asbestsanierung",
                                        "subtitle" => "ZERTIFIZIERT",
                                        "text" => "Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.",
                                        "selected_icon" => [
                                            "value" => "fas fa-shield-alt",
                                            "library" => "fa-solid"
                                        ],
                                        "icon_color" => "#b68c2f",
                                        "subtitle_color" => "#b68c2f",
                                        "title_color" => "#1f1f1f",
                                        "text_color" => "#666666"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ],
        // Card 2 - PCB-Sanierung
        [
            "id" => "5e77a44",
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "_widget_size" => 33,
                "background_background" => "classic",
                "animation" => "fadeInUp",
                "animation_delay" => 200
            ],
            "elements" => [
                // Inner Section mit Bild und Shape
                [
                    "id" => "6e8e4f2",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "background_background" => "classic",
                        "background_image" => [
                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung-fachgerechte-entsorgung.jpg",
                            "id" => "",
                            "size" => ""
                        ],
                        "background_position" => "center center",
                        "background_repeat" => "no-repeat",
                        "background_size" => "cover",
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#FFFFFF",
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 150, "bottom" => 50, "left" => 0, "right" => 0]
                    ],
                    "elements" => [
                        [
                            "id" => "4a19762",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => []
                        ]
                    ]
                ],
                // Inner Section mit Text
                [
                    "id" => "95034f2",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "background_background" => "classic",
                        "background_color" => "#FFFFFF",
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 30, "bottom" => 40, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "a5bb23e",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "34e2b9e",
                                    "elType" => "widget",
                                    "widgetType" => "cholot-texticon",
                                    "settings" => [
                                        "title" => "PCB-Sanierung",
                                        "subtitle" => "FACHGERECHT",
                                        "text" => "Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.",
                                        "selected_icon" => [
                                            "value" => "fas fa-industry",
                                            "library" => "fa-solid"
                                        ],
                                        "icon_color" => "#b68c2f",
                                        "subtitle_color" => "#b68c2f",
                                        "title_color" => "#1f1f1f",
                                        "text_color" => "#666666"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ],
        // Card 3 - Schimmelsanierung
        [
            "id" => "64f5b4b",
            "elType" => "column",
            "settings" => [
                "_column_size" => 34,
                "_widget_size" => 34,
                "background_background" => "classic",
                "animation" => "fadeInUp",
                "animation_delay" => 400
            ],
            "elements" => [
                // Inner Section mit Bild und Shape
                [
                    "id" => "de41fcc",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "background_background" => "classic",
                        "background_image" => [
                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung-praevention-nachhaltig.jpg",
                            "id" => "",
                            "size" => ""
                        ],
                        "background_position" => "center center",
                        "background_repeat" => "no-repeat",
                        "background_size" => "cover",
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#FFFFFF",
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 150, "bottom" => 50, "left" => 0, "right" => 0]
                    ],
                    "elements" => [
                        [
                            "id" => "2f5df56",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => []
                        ]
                    ]
                ],
                // Inner Section mit Text
                [
                    "id" => "01aace0",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "background_background" => "classic",
                        "background_color" => "#FFFFFF",
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 30, "bottom" => 40, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "a74e9e9",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "7a878b9",
                                    "elType" => "widget",
                                    "widgetType" => "cholot-texticon",
                                    "settings" => [
                                        "title" => "Schimmelsanierung",
                                        "subtitle" => "NACHHALTIG",
                                        "text" => "Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.",
                                        "selected_icon" => [
                                            "value" => "fas fa-home",
                                            "library" => "fa-solid"
                                        ],
                                        "icon_color" => "#b68c2f",
                                        "subtitle_color" => "#b68c2f",
                                        "title_color" => "#1f1f1f",
                                        "text_color" => "#666666"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]
];

// Hole aktuelle Elementor Daten
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

// Ersetze die alten Service Cards (Position 1) mit den neuen
$new_data = [];
$new_data[] = $elementor_data[0]; // Hero Slider behalten
$new_data[] = $service_cards; // Neue Service Cards mit Shape Dividers

// Füge den Rest der Seite hinzu (ab Position 2)
for ($i = 2; $i < count($elementor_data); $i++) {
    if (isset($elementor_data[$i])) {
        $new_data[] = $elementor_data[$i];
    }
}

// Speichere zurück
$updated_data = json_encode($new_data);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

echo "✅ Service Cards mit Bildern und Curved Shapes komplett erneuert!\n";

$mysqli->close();