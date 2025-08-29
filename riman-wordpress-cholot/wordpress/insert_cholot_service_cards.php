<?php
// Füge Cholot-Style Service Cards in RIMAN Seite ein

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Service Cards im Cholot-Stil mit Icons
$service_cards_section = [
    "id" => "service_" . uniqid(),
    "elType" => "section",
    "settings" => [
        "background_background" => "classic",
        "background_color" => "#ffffff",
        "padding" => ["unit" => "px", "top" => 80, "bottom" => 80]
    ],
    "elements" => [
        [
            "id" => "col1_" . uniqid(),
            "elType" => "column",
            "settings" => ["_column_size" => 25],
            "elements" => [
                [
                    "id" => "card1_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "cholot-texticon",
                    "settings" => [
                        "title" => "Asbestsanierung",
                        "subtitle" => "ZERTIFIZIERT",
                        "text" => "Sichere und fachgerechte Entfernung von Asbest nach TRGS 519",
                        "selected_icon" => ["value" => "fas fa-shield-alt", "library" => "fa-solid"],
                        "icon_color" => "#b68c2f"
                    ]
                ]
            ]
        ],
        [
            "id" => "col2_" . uniqid(),
            "elType" => "column", 
            "settings" => ["_column_size" => 25],
            "elements" => [
                [
                    "id" => "card2_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "cholot-texticon",
                    "settings" => [
                        "title" => "PCB-Sanierung",
                        "subtitle" => "FACHGERECHT",
                        "text" => "Professionelle Beseitigung von PCB-belasteten Materialien",
                        "selected_icon" => ["value" => "fas fa-industry", "library" => "fa-solid"],
                        "icon_color" => "#b68c2f"
                    ]
                ]
            ]
        ],
        [
            "id" => "col3_" . uniqid(),
            "elType" => "column",
            "settings" => ["_column_size" => 25],
            "elements" => [
                [
                    "id" => "card3_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "cholot-texticon",
                    "settings" => [
                        "title" => "Schimmelsanierung",
                        "subtitle" => "NACHHALTIG",
                        "text" => "Nachhaltige Schimmelbeseitigung und Prävention",
                        "selected_icon" => ["value" => "fas fa-home", "library" => "fa-solid"],
                        "icon_color" => "#b68c2f"
                    ]
                ]
            ]
        ],
        [
            "id" => "col4_" . uniqid(),
            "elType" => "column",
            "settings" => ["_column_size" => 25],
            "elements" => [
                [
                    "id" => "card4_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "cholot-texticon",
                    "settings" => [
                        "title" => "Brandschaden",
                        "subtitle" => "24/7 NOTDIENST",
                        "text" => "Schnelle Hilfe bei Brand- und Wasserschäden",
                        "selected_icon" => ["value" => "fas fa-fire-extinguisher", "library" => "fa-solid"],
                        "icon_color" => "#b68c2f"
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

// Füge Service Cards nach dem Hero Slider ein (Position 2)
array_splice($elementor_data, 2, 0, [$service_cards_section]);

// Speichere zurück
$updated_data = json_encode($elementor_data);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

echo "✅ Cholot Service Cards eingefügt!\n";

$mysqli->close();