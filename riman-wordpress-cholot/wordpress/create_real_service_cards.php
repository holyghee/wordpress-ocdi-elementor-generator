<?php
// Echte Service Cards mit Bildern und curved bottom wie im Cholot Theme

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Service Cards Section mit Bildern und curved shape wie Original
$real_service_cards = [
    "id" => "service_real_" . uniqid(),
    "elType" => "section",
    "settings" => [
        "structure" => "20",
        "content_width" => ["unit" => "px", "size" => 1140],
        "gap" => "extended",
        "padding" => ["unit" => "px", "top" => 80, "bottom" => 80]
    ],
    "elements" => [
        // Service Card 1 - Asbestsanierung
        [
            "id" => "card_col_1_" . uniqid(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "background_color" => "#ffffff",
                "animation" => "fadeInUp",
                "border_border" => "solid",
                "border_width" => ["unit" => "px", "top" => 1, "right" => 1, "bottom" => 1, "left" => 1],
                "border_color" => "#e5e5e5",
                "border_radius" => ["unit" => "px", "top" => 10, "right" => 10, "bottom" => 10, "left" => 10],
                "box_shadow_box_shadow_type" => "yes",
                "box_shadow_box_shadow" => [
                    "horizontal" => 0,
                    "vertical" => 10,
                    "blur" => 30,
                    "spread" => 0,
                    "color" => "rgba(0,0,0,0.1)"
                ]
            ],
            "elements" => [
                // Inner Section for Image with Shape
                [
                    "id" => "inner_sec_1_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 0, "bottom" => 0, "left" => 0, "right" => 0],
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#ffffff",
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50]
                    ],
                    "elements" => [
                        [
                            "id" => "img_inner_col_1_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "img_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg"
                                        ],
                                        "image_size" => "full",
                                        "width" => ["unit" => "%", "size" => 100]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Content Section
                [
                    "id" => "content_sec_1_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "padding" => ["unit" => "px", "top" => 40, "bottom" => 40, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "content_col_1_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "icon_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "icon",
                                    "settings" => [
                                        "selected_icon" => ["value" => "fas fa-shield-alt", "library" => "fa-solid"],
                                        "size" => ["unit" => "px", "size" => 40],
                                        "primary_color" => "#b68c2f",
                                        "align" => "center"
                                    ]
                                ],
                                [
                                    "id" => "subtitle_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "heading",
                                    "settings" => [
                                        "title" => "ZERTIFIZIERT",
                                        "header_size" => "h6",
                                        "align" => "center",
                                        "title_color" => "#b68c2f"
                                    ]
                                ],
                                [
                                    "id" => "title_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "heading",
                                    "settings" => [
                                        "title" => "Asbestsanierung",
                                        "header_size" => "h3",
                                        "align" => "center",
                                        "title_color" => "#1f1f1f"
                                    ]
                                ],
                                [
                                    "id" => "text_1_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "text-editor",
                                    "settings" => [
                                        "editor" => "<p style='text-align: center;'>Sichere und fachgerechte Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.</p>",
                                        "text_color" => "#666666"
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
            "id" => "card_col_2_" . uniqid(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "background_color" => "#ffffff",
                "animation" => "fadeInUp",
                "animation_delay" => 200,
                "border_border" => "solid",
                "border_width" => ["unit" => "px", "top" => 1, "right" => 1, "bottom" => 1, "left" => 1],
                "border_color" => "#e5e5e5",
                "border_radius" => ["unit" => "px", "top" => 10, "right" => 10, "bottom" => 10, "left" => 10],
                "box_shadow_box_shadow_type" => "yes",
                "box_shadow_box_shadow" => [
                    "horizontal" => 0,
                    "vertical" => 10,
                    "blur" => 30,
                    "spread" => 0,
                    "color" => "rgba(0,0,0,0.1)"
                ]
            ],
            "elements" => [
                // Inner Section for Image with Shape
                [
                    "id" => "inner_sec_2_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 0, "bottom" => 0, "left" => 0, "right" => 0],
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#ffffff",
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50]
                    ],
                    "elements" => [
                        [
                            "id" => "img_inner_col_2_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "img_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/pcb-sanierung-fachgerechte-entsorgung.jpg"
                                        ],
                                        "image_size" => "full",
                                        "width" => ["unit" => "%", "size" => 100]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ],
                // Content Section
                [
                    "id" => "content_sec_2_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "padding" => ["unit" => "px", "top" => 40, "bottom" => 40, "left" => 30, "right" => 30]
                    ],
                    "elements" => [
                        [
                            "id" => "content_col_2_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "icon_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "icon",
                                    "settings" => [
                                        "selected_icon" => ["value" => "fas fa-industry", "library" => "fa-solid"],
                                        "size" => ["unit" => "px", "size" => 40],
                                        "primary_color" => "#b68c2f",
                                        "align" => "center"
                                    ]
                                ],
                                [
                                    "id" => "subtitle_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "heading",
                                    "settings" => [
                                        "title" => "FACHGERECHT",
                                        "header_size" => "h6",
                                        "align" => "center",
                                        "title_color" => "#b68c2f"
                                    ]
                                ],
                                [
                                    "id" => "title_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "heading",
                                    "settings" => [
                                        "title" => "PCB-Sanierung",
                                        "header_size" => "h3",
                                        "align" => "center",
                                        "title_color" => "#1f1f1f"
                                    ]
                                ],
                                [
                                    "id" => "text_2_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "text-editor",
                                    "settings" => [
                                        "editor" => "<p style='text-align: center;'>Professionelle Beseitigung von PCB-belasteten Materialien nach aktuellen Richtlinien.</p>",
                                        "text_color" => "#666666"
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
            "id" => "card_col_3_" . uniqid(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_background" => "classic",
                "background_color" => "#ffffff",
                "animation" => "fadeInUp",
                "animation_delay" => 400,
                "border_border" => "solid",
                "border_width" => ["unit" => "px", "top" => 1, "right" => 1, "bottom" => 1, "left" => 1],
                "border_color" => "#e5e5e5",
                "border_radius" => ["unit" => "px", "top" => 10, "right" => 10, "bottom" => 10, "left" => 10],
                "box_shadow_box_shadow_type" => "yes",
                "box_shadow_box_shadow" => [
                    "horizontal" => 0,
                    "vertical" => 10,
                    "blur" => 30,
                    "spread" => 0,
                    "color" => "rgba(0,0,0,0.1)"
                ]
            ],
            "elements" => [
                // Inner Section for Image with Shape
                [
                    "id" => "inner_sec_3_" . uniqid(),
                    "elType" => "section",
                    "isInner" => true,
                    "settings" => [
                        "structure" => "10",
                        "gap" => "no",
                        "padding" => ["unit" => "px", "top" => 0, "bottom" => 0, "left" => 0, "right" => 0],
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_color" => "#ffffff",
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50]
                    ],
                    "elements" => [
                        [
                            "id" => "img_inner_col_3_" . uniqid(),
                            "elType" => "column",
                            "settings" => ["_column_size" => 100],
                            "elements" => [
                                [
                                    "id" => "img_3_" . uniqid(),
                                    "elType" => "widget",
                                    "widgetType" => "image",
                                    "settings" => [
                                        "image" => [
                                            "url" => "http://localhost:8081/wp-content/uploads/2025/08/schimmelsanierung-praevention-nachhaltig.jpg"
                                        ],
                                        "image_size" => "full",
                                        "width" => ["unit" => "%", "size" => 100]
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

// Füge die neuen Service Cards nach dem Hero Slider ein (Position 1)
array_splice($elementor_data, 1, 0, [$real_service_cards]);

// Speichere zurück
$updated_data = json_encode($elementor_data);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

echo "✅ Echte Service Cards mit Bildern und curved bottom eingefügt!\n";

$mysqli->close();