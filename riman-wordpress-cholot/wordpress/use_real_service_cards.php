<?php
/**
 * Verwendet die echten Service Card Templates aus elementor_blocks
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "📦 Verwende echte Service Card Templates\n\n";

// Lade Service Card Template
$template_file = 'elementor_blocks/services/service_cards_image_1.json';
$template_data = json_decode(file_get_contents($template_file), true);

echo "✅ Template geladen: $template_file\n";

// Extrahiere die Service Card Struktur
$service_card_structure = $template_data['content'][0];

// Generiere Service Cards Section mit 3 Cards
$service_section = [
    "id" => uniqid(),
    "elType" => "section",
    "settings" => [
        "content_width" => ["unit" => "px", "size" => 1140],
        "gap" => "extended",
        "padding" => ["unit" => "px", "top" => 80, "bottom" => 80]
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

// Erstelle 3 Service Cards basierend auf dem Template
foreach ($cards as $index => $card_data) {
    // Kopiere Template Struktur
    $card = json_decode(json_encode($service_card_structure), true);
    
    // Generiere neue IDs
    $card['id'] = uniqid();
    
    // Wickle in Column für 3-Spalten Layout
    $column = [
        "id" => uniqid(),
        "elType" => "column",
        "settings" => [
            "_column_size" => 33,
            "animation" => "fadeInUp",
            "animation_delay" => $index * 200
        ],
        "elements" => []
    ];
    
    // Update Bild
    if (isset($card['elements'][0]['elements'][0]['settings']['image'])) {
        $card['elements'][0]['elements'][0]['settings']['image']['url'] = $card_data['image'];
    }
    
    // Füge Text-Content hinzu (als zweite Inner Section)
    $text_section = [
        "id" => uniqid(),
        "elType" => "section",
        "isInner" => true,
        "settings" => [
            "gap" => "no",
            "background_background" => "classic",
            "background_color" => "#ffffff",
            "padding" => ["unit" => "px", "top" => 30, "bottom" => 40, "left" => 30, "right" => 30]
        ],
        "elements" => [
            [
                "id" => uniqid(),
                "elType" => "column",
                "settings" => ["_column_size" => 100],
                "elements" => [
                    [
                        "id" => uniqid(),
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
                            "icon_color" => "#b68c2f",
                            "subtitle_color" => "#b68c2f",
                            "title_color" => "#1f1f1f",
                            "text_color" => "#666666",
                            "icon_align" => "center"
                        ]
                    ]
                ]
            ]
        ]
    ];
    
    // Kombiniere Image Section mit Text Section
    $column['elements'] = [$card, $text_section];
    
    // Füge zur Service Section hinzu
    $service_section['elements'][] = $column;
}

// Hole aktuelle Elementor Data
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

echo "\n📝 Aktuelle Sections: " . count($elementor_data) . "\n";

// Ersetze die Service Cards Section (normalerweise Position 1 oder 2)
$new_data = [];
$service_cards_replaced = false;

foreach ($elementor_data as $section) {
    // Behalte Hero Section
    if (isset($section['elements'][0]['elements'][0]['widgetType']) && 
        $section['elements'][0]['elements'][0]['widgetType'] == 'rdn-slider') {
        $new_data[] = $section;
        echo "✅ Hero Slider beibehalten\n";
    }
    // Ersetze Service Cards
    elseif (!$service_cards_replaced && 
            (strpos(json_encode($section), 'cholot-texticon') !== false ||
             strpos(json_encode($section), 'service') !== false)) {
        $new_data[] = $service_section;
        $service_cards_replaced = true;
        echo "✅ Service Cards mit echten Templates ersetzt\n";
    }
    // Behalte andere Sections
    else {
        $new_data[] = $section;
    }
}

// Falls keine Service Cards ersetzt wurden, füge sie nach Hero ein
if (!$service_cards_replaced && count($new_data) > 0) {
    array_splice($new_data, 1, 0, [$service_section]);
    echo "✅ Service Cards nach Hero eingefügt\n";
}

// Speichere zurück
$updated_data = json_encode($new_data);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

// Cache löschen
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");

echo "\n✅ Service Cards mit echten Templates aktualisiert!\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";

$mysqli->close();