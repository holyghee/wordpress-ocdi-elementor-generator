<?php
/**
 * Repariert das Kontaktformular
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "📧 Repariere Kontaktformular...\n\n";

// 1. Prüfe ob Contact Form 7 existiert
$result = $mysqli->query("SELECT ID, post_title, post_status FROM wp_posts WHERE post_type = 'wpcf7_contact_form'");

echo "📝 Vorhandene Kontaktformulare:\n";
$form_id = null;
while ($row = $result->fetch_assoc()) {
    echo "   - ID: " . $row['ID'] . " | " . $row['post_title'] . " | Status: " . $row['post_status'] . "\n";
    if ($row['post_status'] == 'publish') {
        $form_id = $row['ID'];
    }
}

// 2. Erstelle neues Formular falls keines existiert
if (!$form_id) {
    echo "\n⚠️  Kein aktives Kontaktformular gefunden. Erstelle neues...\n";
    
    // Erstelle Contact Form Post
    $form_title = 'Kontaktformular RIMAN';
    $form_content = '<label> Ihr Name (Pflichtfeld)
    [text* your-name] </label>

<label> Ihre E-Mail-Adresse (Pflichtfeld)
    [email* your-email] </label>

<label> Betreff
    [text your-subject] </label>

<label> Ihre Nachricht
    [textarea your-message] </label>

[submit "Senden"]';
    
    $insert = $mysqli->prepare("INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_status, post_name, post_type, post_modified, post_modified_gmt) VALUES (1, NOW(), NOW(), ?, ?, 'publish', 'kontaktformular-riman', 'wpcf7_contact_form', NOW(), NOW())");
    $insert->bind_param('ss', $form_content, $form_title);
    $insert->execute();
    $form_id = $mysqli->insert_id;
    
    echo "✅ Neues Formular erstellt (ID: $form_id)\n";
    
    // Füge Contact Form 7 Meta hinzu
    $mail_settings = [
        'active' => true,
        'subject' => 'RIMAN Kontaktanfrage von [your-name]',
        'sender' => '[your-name] <[your-email]>',
        'recipient' => 'info@riman-gmbh.de',
        'body' => "Von: [your-name] <[your-email]>\nBetreff: [your-subject]\n\nNachricht:\n[your-message]",
        'additional_headers' => 'Reply-To: [your-email]',
        'attachments' => '',
        'use_html' => false,
        'exclude_blank' => false
    ];
    
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($form_id, '_mail', '" . serialize($mail_settings) . "')");
    
    // Messages
    $messages = [
        'mail_sent_ok' => 'Vielen Dank für Ihre Nachricht. Sie wurde erfolgreich versendet.',
        'mail_sent_ng' => 'Beim Versenden Ihrer Nachricht ist ein Fehler aufgetreten. Bitte versuchen Sie es später noch einmal.',
        'validation_error' => 'Ein oder mehrere Felder enthalten fehlerhafte Angaben. Bitte prüfen Sie Ihre Eingaben.',
        'spam' => 'Beim Versenden Ihrer Nachricht ist ein Fehler aufgetreten. Bitte versuchen Sie es später noch einmal.',
        'accept_terms' => 'Sie müssen die Bedingungen akzeptieren, bevor Sie Ihre Nachricht versenden.',
        'invalid_required' => 'Bitte füllen Sie dieses Feld aus.',
        'invalid_too_long' => 'Diese Eingabe ist zu lang.',
        'invalid_too_short' => 'Diese Eingabe ist zu kurz.'
    ];
    
    $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($form_id, '_messages', '" . serialize($messages) . "')");
}

// 3. Aktualisiere Elementor Data mit korrektem Shortcode
echo "\n📝 Aktualisiere Elementor mit Kontaktformular (ID: $form_id)...\n";

$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

// Füge Contact Form Section hinzu oder aktualisiere
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

// Suche und ersetze oder füge Contact Section hinzu
$contact_found = false;
for ($i = 0; $i < count($elementor_data); $i++) {
    $section_json = json_encode($elementor_data[$i]);
    if (strpos($section_json, 'contact-form-7') !== false || 
        strpos($section_json, 'Kostenlose Erstberatung') !== false) {
        $elementor_data[$i] = $contact_section;
        $contact_found = true;
        echo "✅ Kontaktformular Section aktualisiert\n";
        break;
    }
}

// Falls nicht gefunden, füge am Ende hinzu
if (!$contact_found) {
    $elementor_data[] = $contact_section;
    echo "✅ Kontaktformular Section hinzugefügt\n";
}

// Speichere zurück
$updated_data = json_encode($elementor_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$stmt->bind_param('s', $updated_data);
$stmt->execute();

// 4. Stelle sicher dass Contact Form 7 Plugin aktiv ist
$active_plugins = $mysqli->query("SELECT option_value FROM wp_options WHERE option_name = 'active_plugins'");
$row = $active_plugins->fetch_assoc();
$plugins = unserialize($row['option_value']);

if (!in_array('contact-form-7/wp-contact-form-7.php', $plugins)) {
    echo "\n⚠️  Contact Form 7 Plugin nicht aktiv. Aktiviere...\n";
    $plugins[] = 'contact-form-7/wp-contact-form-7.php';
    $mysqli->query("UPDATE wp_options SET option_value = '" . serialize($plugins) . "' WHERE option_name = 'active_plugins'");
    echo "✅ Contact Form 7 aktiviert\n";
}

// Cache löschen
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");

echo "\n✅ Kontaktformular repariert!\n";
echo "   - Form ID: $form_id\n";
echo "   - Shortcode: [contact-form-7 id=\"$form_id\"]\n";
echo "   - Schwarzer Hintergrund\n";
echo "   - Deutsche Texte\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000#contact\n";

$mysqli->close();