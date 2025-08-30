<?php
/**
 * Fügt das Kontaktformular zur Seite hinzu
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "📧 Füge Kontaktformular zur Seite hinzu...\n\n";

$form_id = 3020; // Das gerade erstellte Formular

// Hole aktuelle Elementor Data
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

// Contact Form Section
$contact_section = [
    "id" => "contact_" . uniqid(),
    "elType" => "section",
    "settings" => [
        "padding" => ["unit" => "px", "top" => 80, "bottom" => 80],
        "background_background" => "classic",
        "background_color" => "#1a1a1a",
        "content_width" => ["unit" => "px", "size" => 800]
    ],
    "elements" => [
        [
            "id" => "contact_col_" . uniqid(),
            "elType" => "column",
            "settings" => ["_column_size" => 100],
            "elements" => [
                [
                    "id" => "contact_heading_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "heading",
                    "settings" => [
                        "title" => "Kostenlose Erstberatung",
                        "header_size" => "h2",
                        "align" => "center",
                        "title_color" => "#ffffff"
                    ]
                ],
                [
                    "id" => "contact_subheading_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "heading",
                    "settings" => [
                        "title" => "Wir beraten Sie gerne unverbindlich",
                        "header_size" => "h4",
                        "align" => "center",
                        "title_color" => "#b68c2f"
                    ]
                ],
                [
                    "id" => "contact_form_" . uniqid(),
                    "elType" => "widget",
                    "widgetType" => "shortcode",
                    "settings" => [
                        "shortcode" => '[contact-form-7 id="' . $form_id . '" title="Kontaktformular"]'
                    ]
                ]
            ]
        ]
    ]
];

// Suche existierende Contact Section oder füge am Ende hinzu
$contact_found = false;
$new_data = [];

foreach ($elementor_data as $section) {
    $section_json = json_encode($section);
    
    // Behalte Hero und Service Cards
    if (isset($section['elements'][0]['elements'][0]['widgetType']) && 
        $section['elements'][0]['elements'][0]['widgetType'] == 'rdn-slider') {
        $new_data[] = $section;
        echo "✅ Hero Section beibehalten\n";
    }
    elseif (strpos($section_json, 'service') !== false && strpos($section_json, 'contact') === false) {
        $new_data[] = $section;
        echo "✅ Service Cards beibehalten\n";
    }
    // Ersetze alte Contact Section
    elseif (strpos($section_json, 'contact') !== false || strpos($section_json, 'Erstberatung') !== false) {
        if (!$contact_found) {
            $new_data[] = $contact_section;
            $contact_found = true;
            echo "✅ Kontaktformular Section ersetzt\n";
        }
    }
    else {
        $new_data[] = $section;
    }
}

// Falls nicht gefunden, füge am Ende hinzu
if (!$contact_found) {
    $new_data[] = $contact_section;
    echo "✅ Kontaktformular Section am Ende hinzugefügt\n";
}

// Speichere zurück
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

echo "\n📧 Kontaktformular hinzugefügt!\n";
echo "   - Form ID: $form_id\n";
echo "   - Shortcode: [contact-form-7 id=\"$form_id\"]\n";
echo "   - Schwarzer Hintergrund (#1a1a1a)\n";
echo "   - Position: Am Ende der Seite\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "   Scrolle nach unten zum Kontaktformular\n";

$mysqli->close();