<?php
/**
 * Behebt alle Bilder - Hero Section und Service Cards
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🖼️  Behebe alle Bilder - Hero und Service Cards\n\n";

// Image-Server URL
$image_server = "http://localhost:3456";

// Hole aktuelle Elementor Data
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

echo "📝 Analysiere aktuelle Struktur...\n";

// 1. HERO SECTION FIXEN
if (isset($elementor_data[0]['elements'][0]['elements'][0]['widgetType']) && 
    $elementor_data[0]['elements'][0]['elements'][0]['widgetType'] == 'rdn-slider') {
    
    echo "✅ Hero Slider gefunden - aktualisiere Bilder...\n";
    
    // Aktualisiere Slider Items mit Image-Server Bildern
    $elementor_data[0]['elements'][0]['elements'][0]['settings']['slider_list'] = [
        [
            "_id" => uniqid(),
            "title" => "25+ Jahre Erfahrung in Sanierung & Umweltschutz",
            "subtitle" => "Seit 1998 Ihr zuverlässiger Partner",
            "text" => "Professionelle Lösungen für Asbest-, PCB- und Schadstoffsanierung. Wir stehen für Sicherheit, Qualität und Nachhaltigkeit.",
            "btn_text" => "Unsere Leistungen",
            "btn_link" => ["url" => "#services"],
            "image" => [
                "url" => $image_server . "/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg",
                "id" => ""
            ]
        ],
        [
            "_id" => uniqid(),
            "title" => "Zertifizierte Asbestsanierung nach TRGS 519",
            "subtitle" => "Höchste Sicherheitsstandards",
            "text" => "Als zertifizierter Fachbetrieb führen wir Asbestsanierungen sicher und gesetzeskonform durch.",
            "btn_text" => "Mehr erfahren",
            "btn_link" => ["url" => "#asbest"],
            "image" => [
                "url" => $image_server . "/asbestsanierung-schutzausruestung-fachpersonal.jpg",
                "id" => ""
            ]
        ]
    ];
    
    echo "   - Slide 1: Gebäuderückbau Bild\n";
    echo "   - Slide 2: Asbestsanierung Bild\n";
}

// 2. SERVICE CARDS SECTION KOMPLETT NEU
echo "\n📦 Erstelle neue Service Cards Section mit Bildern...\n";

$service_section = [
    "id" => "services_" . uniqid(),
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

// Service Cards Daten
$cards = [
    [
        'title' => 'Asbestsanierung',
        'subtitle' => 'ZERTIFIZIERT',
        'text' => 'Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.',
        'icon' => 'fas fa-shield-alt',
        'image' => $image_server . '/asbestsanierung-schutzausruestung-fachpersonal.jpg'
    ],
    [
        'title' => 'PCB-Sanierung', 
        'subtitle' => 'FACHGERECHT',
        'text' => 'Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.',
        'icon' => 'fas fa-industry',
        'image' => $image_server . '/schadstoffsanierung-industrieanlage-riman-gmbh.jpg'
    ],
    [
        'title' => 'Schimmelsanierung',
        'subtitle' => 'NACHHALTIG',
        'text' => 'Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.',
        'icon' => 'fas fa-home',
        'image' => $image_server . '/umweltingenieur-bodenproben-analyse-labor.jpg'
    ]
];

foreach ($cards as $index => $card) {
    $column = [
        "id" => uniqid(),
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
            "padding" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0]
        ],
        "elements" => [
            // Image Widget oben
            [
                "id" => uniqid(),
                "elType" => "widget",
                "widgetType" => "image",
                "settings" => [
                    "image" => [
                        "url" => $card['image'],
                        "id" => "",
                        "size" => "",
                        "alt" => $card['title']
                    ],
                    "image_size" => "full",
                    "width" => ["unit" => "%", "size" => 100],
                    "height" => ["unit" => "px", "size" => 250],
                    "object_fit" => "cover",
                    "_margin" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0],
                    "_padding" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 0, "left" => 0]
                ]
            ],
            // Curved Divider als Spacer mit negativem Margin
            [
                "id" => uniqid(),
                "elType" => "widget",
                "widgetType" => "spacer",
                "settings" => [
                    "space" => ["unit" => "px", "size" => 50],
                    "_margin" => ["unit" => "px", "top" => -50, "right" => 0, "bottom" => 0, "left" => 0],
                    "shape_divider_top" => "curve",
                    "shape_divider_top_color" => "#ffffff",
                    "shape_divider_top_height" => ["unit" => "px", "size" => 50]
                ]
            ],
            // Text Content
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
                    "icon_align" => "center",
                    "icon_color" => "#b68c2f",
                    "subtitle_color" => "#b68c2f",
                    "title_color" => "#1f1f1f",
                    "text_color" => "#666666",
                    "iconbg_color" => "rgba(182, 140, 47, 0.1)",
                    "_padding" => ["unit" => "px", "top" => 20, "right" => 30, "bottom" => 40, "left" => 30]
                ]
            ]
        ]
    ];
    
    $service_section['elements'][] = $column;
    echo "   ✅ Card: " . $card['title'] . "\n";
}

// 3. NEUE STRUKTUR ZUSAMMENBAUEN
$new_data = [];

// Hero Section behalten (mit aktualisierten Bildern)
if (isset($elementor_data[0])) {
    $new_data[] = $elementor_data[0];
    echo "\n✅ Hero Section mit neuen Bildern\n";
}

// Service Cards einfügen
$new_data[] = $service_section;
echo "✅ Service Cards Section eingefügt\n";

// Rest der Sections behalten (ab Index 2)
for ($i = 2; $i < count($elementor_data); $i++) {
    if (isset($elementor_data[$i])) {
        // Skip alte Service Card Sections
        $json = json_encode($elementor_data[$i]);
        if (strpos($json, 'service') === false || strpos($json, 'contact') !== false) {
            $new_data[] = $elementor_data[$i];
        }
    }
}

// Speichere zurück
$updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);

if ($stmt->execute()) {
    echo "\n✅ Elementor Data erfolgreich aktualisiert!\n";
} else {
    echo "\n❌ Fehler: " . $stmt->error . "\n";
}

// Cache löschen
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = UNIX_TIMESTAMP() WHERE post_id = 3000 AND meta_key = '_elementor_data_time'");

echo "\n🎨 Alle Bilder behoben!\n";
echo "   ✅ Hero Slider mit Bildern\n";
echo "   ✅ Service Cards mit Bildern\n";
echo "   ✅ Image-Server: $image_server\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "💡 Hard Refresh: Strg+F5\n";

// Prüfe Image-Server Status
$ch = curl_init($image_server);
curl_setopt($ch, CURLOPT_NOBODY, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 2);
curl_exec($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($code == 200) {
    echo "\n✅ Image-Server läuft auf $image_server\n";
} else {
    echo "\n⚠️  Image-Server nicht erreichbar!\n";
    echo "   Starte mit: python3 -m http.server 3456\n";
    echo "   Im Verzeichnis: /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/image-server\n";
}

$mysqli->close();