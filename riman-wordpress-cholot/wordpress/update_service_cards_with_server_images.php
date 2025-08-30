<?php
/**
 * Aktualisiert Service Cards mit Bildern vom Image-Server
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🖼️  Aktualisiere Service Cards mit Image-Server Bildern\n\n";

// Bilder vom Image-Server (Port 3456)
$image_server_base = "http://localhost:3456";

// Service Cards mit Image-Server Bildern
$cards = [
    [
        'title' => 'Asbestsanierung',
        'subtitle' => 'ZERTIFIZIERT',
        'text' => 'Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.',
        'icon' => 'fas fa-shield-alt',
        'image' => $image_server_base . '/asbestsanierung-schutzausruestung-fachpersonal.jpg'
    ],
    [
        'title' => 'PCB-Sanierung',
        'subtitle' => 'FACHGERECHT',
        'text' => 'Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.',
        'icon' => 'fas fa-industry',
        'image' => $image_server_base . '/pcb-sanierung-fachgerechte-entsorgung.jpg'
    ],
    [
        'title' => 'Schimmelsanierung',
        'subtitle' => 'NACHHALTIG',
        'text' => 'Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.',
        'icon' => 'fas fa-home',
        'image' => $image_server_base . '/schimmelsanierung-praevention-nachhaltig.jpg'
    ]
];

// Prüfe ob der Image-Server läuft
$ch = curl_init($image_server_base);
curl_setopt($ch, CURLOPT_NOBODY, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
curl_exec($ch);
$responseCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($responseCode != 200) {
    echo "⚠️  Image-Server nicht erreichbar auf $image_server_base\n";
    echo "   Starte den Server mit: python3 -m http.server 3456 --directory /path/to/images\n\n";
}

// Service Cards Section mit Image-Server Bildern
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

// Erstelle 3 Service Cards
foreach ($cards as $index => $card_data) {
    echo "📦 Erstelle Card: " . $card_data['title'] . "\n";
    echo "   Bild: " . $card_data['image'] . "\n";
    
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
                        "size" => ""
                    ],
                    "background_position" => "center center",
                    "background_repeat" => "no-repeat",
                    "background_size" => "cover",
                    "min_height" => ["unit" => "px", "size" => 250],
                    "shape_divider_bottom" => "curve",
                    "shape_divider_bottom_negative" => "yes",
                    "shape_divider_bottom_color" => "#ffffff",
                    "shape_divider_bottom_height" => ["unit" => "px", "size" => 50]
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
            // Text Content Section mit cholot-texticon
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
                            [
                                "id" => "texticon_" . uniqid(),
                                "elType" => "widget",
                                "widgetType" => "cholot-texticon",
                                "settings" => [
                                    "title" => $card_data['title'],
                                    "subtitle" => $card_data['subtitle'],
                                    "text" => $card_data['text'],
                                    "selected_icon" => [
                                        "value" => $card_data['icon'],
                                        "library" => "fa-solid"
                                    ],
                                    "icon_align" => "center",
                                    "icon_color" => "#b68c2f",
                                    "subtitle_color" => "#b68c2f",
                                    "title_color" => "#1f1f1f",
                                    "text_color" => "#666666",
                                    "iconbg_color" => "rgba(182, 140, 47, 0.1)"
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

echo "\n📝 Ersetze Service Cards Section...\n";

// Neue Datenstruktur
$new_data = [];
$service_replaced = false;

foreach ($elementor_data as $index => $section) {
    // Behalte Hero Section
    if ($index === 0 || (isset($section['elements'][0]['elements'][0]['widgetType']) && 
        $section['elements'][0]['elements'][0]['widgetType'] == 'rdn-slider')) {
        $new_data[] = $section;
        echo "✅ Hero Section beibehalten\n";
    }
    // Ersetze Service Cards (normalerweise zweite Section)
    elseif ($index === 1 && !$service_replaced) {
        $new_data[] = $service_section;
        $service_replaced = true;
        echo "✅ Service Cards mit Image-Server Bildern ersetzt\n";
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
$updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
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

echo "\n🎨 Service Cards mit Image-Server Bildern erstellt!\n";
echo "   Image-Server: $image_server_base\n";
echo "   - 3 Cards mit Hintergrundbildern\n";
echo "   - Curved Shape Dividers\n";
echo "   - cholot-texticon Widgets\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";

// Starte Image-Server falls nicht läuft
if ($responseCode != 200) {
    echo "\n⚠️  Starte den Image-Server:\n";
    echo "   cd /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/image-server\n";
    echo "   python3 -m http.server 3456\n";
}

$mysqli->close();