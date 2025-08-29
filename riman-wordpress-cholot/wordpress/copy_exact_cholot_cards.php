<?php
// Exakte Kopie der Cholot Service Cards Struktur von Port 8080

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Exakte Cholot Service Cards Section
$cholot_service_cards = [
    "id" => "388095a",
    "elType" => "section",
    "settings" => [
        "content_width" => ["unit" => "px", "size" => 1140],
        "gap" => "extended"
    ],
    "elements" => [
        // Column 1
        [
            "id" => "5019170",
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "animation" => "fadeInUp"
            ],
            "elements" => [
                // Image Section with Shape Divider
                [
                    "id" => "2a5e03d",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "gap" => "no"
                    ],
                    "elements" => [
                        [
                            "id" => "61e7066",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "10fcc6d",
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg",
                                            "id" => ""
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Text Icon Section
                [
                    "id" => "db46a32",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "background_background" => "classic",
                        "gap" => "no"
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
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ],
        // Column 2
        [
            "id" => "5e77a44",
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "animation" => "fadeInUp",
                "animation_delay" => 200
            ],
            "elements" => [
                // Image Section with Shape Divider
                [
                    "id" => "6e8e4f2",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "background_background" => "classic",
                        "gap" => "no"
                    ],
                    "elements" => [
                        [
                            "id" => "4a19762",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "6e967c2",
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung-fachgerechte-entsorgung.jpg",
                                            "id" => ""
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Text Icon Section
                [
                    "id" => "95034f2",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "background_background" => "classic",
                        "gap" => "no"
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
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ],
        // Column 3
        [
            "id" => "64f5b4b",
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "animation" => "fadeInUp",
                "animation_delay" => 400
            ],
            "elements" => [
                // Image Section with Shape Divider
                [
                    "id" => "de41fcc",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "gap" => "no"
                    ],
                    "elements" => [
                        [
                            "id" => "2f5df56",
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "efbac09",
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung-praevention-nachhaltig.jpg",
                                            "id" => ""
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Text Icon Section
                [
                    "id" => "01aace0",
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "background_background" => "classic",
                        "gap" => "no"
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
                                        ]
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

// Lösche alte Service Cards und füge neue ein
// Behalte nur den Hero Slider (Position 0) und füge die neuen Service Cards danach ein
$new_data = [];
$new_data[] = $elementor_data[0]; // Hero Slider
$new_data[] = $cholot_service_cards; // Neue Service Cards

// Füge den Rest der Seite hinzu
for ($i = 3; $i < count($elementor_data); $i++) {
    if (isset($elementor_data[$i])) {
        $new_data[] = $elementor_data[$i];
    }
}

// Speichere zurück
$updated_data = json_encode($new_data);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

echo "✅ Exakte Cholot Service Cards kopiert!\n";

$mysqli->close();