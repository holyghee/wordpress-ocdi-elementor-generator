<?php
// Service Cards mit Bildern und Shape Divider wie Original Cholot

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Service Cards Section mit Bildern und curved shape divider
$service_cards_with_images = [
    "id" => "service_img_" . uniqid(),
    "elType" => "section",
    "settings" => [
        "stretch_section" => "section-stretched",
        "gap" => "extended",
        "content_width" => ["unit" => "px", "size" => 1140]
    ],
    "elements" => [
        // Service Card 1 - Asbestsanierung
        [
            "id" => "col_img_1_" . uniqid(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "background_color" => "#ffffff",
                "animation" => "fadeInUp"
            ],
            "elements" => [
                // Image Section with Shape Divider
                [
                    "id" => "img_section_1_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#ffffff",
                        "padding" => ["unit" => "px", "top" => 0, "bottom" => 0, "left" => 0, "right" => 0]
                    ],
                    "elements" => [
                        [
                            "id" => "img_col_1_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "img_widget_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg",
                                            "id" => ""
                                        ],
                                        "image_size" => "large"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Text Section with Icon
                [
                    "id" => "text_section_1_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "background_background" => "classic",
                        "background_color" => "#ffffff",
                        "padding" => ["unit" => "px", "top" => 30, "bottom" => 30, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "text_col_1_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "icon_text_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "cholot-texticon",
                                    "settings" => [
                                        "title" => "Asbestsanierung",
                                        "subtitle" => "ZERTIFIZIERT",
                                        "text" => "Sichere Entfernung von Asbest nach TRGS 519",
                                        "selected_icon" => ["value" => "fas fa-shield-alt", "library" => "fa-solid"],
                                        "icon_color" => "#b68c2f",
                                        "icon_align" => "center"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ],
        // Service Card 2 - PCB-Sanierung
        [
            "id" => "col_img_2_" . uniqid(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "background_color" => "#ffffff",
                "animation" => "fadeInUp",
                "animation_delay" => 200
            ],
            "elements" => [
                // Image Section with Shape Divider
                [
                    "id" => "img_section_2_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#ffffff",
                        "padding" => ["unit" => "px", "top" => 0, "bottom" => 0, "left" => 0, "right" => 0]
                    ],
                    "elements" => [
                        [
                            "id" => "img_col_2_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "img_widget_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung-fachgerechte-entsorgung.jpg",
                                            "id" => ""
                                        ],
                                        "image_size" => "large"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Text Section with Icon
                [
                    "id" => "text_section_2_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "background_background" => "classic",
                        "background_color" => "#ffffff",
                        "padding" => ["unit" => "px", "top" => 30, "bottom" => 30, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "text_col_2_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "icon_text_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "cholot-texticon",
                                    "settings" => [
                                        "title" => "PCB-Sanierung",
                                        "subtitle" => "FACHGERECHT",
                                        "text" => "Professionelle Beseitigung von PCB-Materialien",
                                        "selected_icon" => ["value" => "fas fa-industry", "library" => "fa-solid"],
                                        "icon_color" => "#b68c2f",
                                        "icon_align" => "center"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ],
        // Service Card 3 - Schimmelsanierung
        [
            "id" => "col_img_3_" . uniqid(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "background_color" => "#ffffff",
                "animation" => "fadeInUp",
                "animation_delay" => 400
            ],
            "elements" => [
                // Image Section with Shape Divider
                [
                    "id" => "img_section_3_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#ffffff",
                        "padding" => ["unit" => "px", "top" => 0, "bottom" => 0, "left" => 0, "right" => 0]
                    ],
                    "elements" => [
                        [
                            "id" => "img_col_3_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "img_widget_3_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung-praevention-nachhaltig.jpg",
                                            "id" => ""
                                        ],
                                        "image_size" => "large"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Text Section with Icon
                [
                    "id" => "text_section_3_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "background_background" => "classic",
                        "background_color" => "#ffffff",
                        "padding" => ["unit" => "px", "top" => 30, "bottom" => 30, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "text_col_3_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "icon_text_3_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "cholot-texticon",
                                    "settings" => [
                                        "title" => "Schimmelsanierung",
                                        "subtitle" => "NACHHALTIG",
                                        "text" => "Nachhaltige Schimmelbeseitigung und Prävention",
                                        "selected_icon" => ["value" => "fas fa-home", "library" => "fa-solid"],
                                        "icon_color" => "#b68c2f",
                                        "icon_align" => "center"
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

// Ersetze die alte Service Cards Section (Position 2) mit der neuen
$elementor_data[2] = $service_cards_with_images;

// Speichere zurück
$updated_data = json_encode($elementor_data);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

echo "✅ Service Cards mit Bildern und Shape Divider eingefügt!\n";

$mysqli->close();