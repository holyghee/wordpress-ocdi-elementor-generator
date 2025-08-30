<?php
/**
 * Richtet Contact Form 7 korrekt ein
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "📧 Richte Contact Form 7 korrekt ein...\n\n";

$form_id = 3020;

// Formular HTML Content
$form_content = '<div class="cholot-contact-form">
<div class="row">
<div class="col-md-6">
[text* your-name placeholder "Ihr Name *"]
</div>
<div class="col-md-6">
[email* your-email placeholder "Ihre E-Mail *"]
</div>
</div>
<div class="row">
<div class="col-md-12">
[text your-subject placeholder "Betreff"]
</div>
</div>
<div class="row">
<div class="col-md-12">
[textarea your-message placeholder "Ihre Nachricht"]
</div>
</div>
<div class="row">
<div class="col-md-12">
[submit "Nachricht senden"]
</div>
</div>
</div>';

// Update Post Content
$stmt = $mysqli->prepare("UPDATE wp_posts SET post_content = ? WHERE ID = ?");
$stmt->bind_param('si', $form_content, $form_id);
$stmt->execute();

echo "✅ Formular HTML aktualisiert\n";

// Mail Settings
$mail = array(
    'active' => true,
    'subject' => '[your-subject]',
    'sender' => '[your-name] <wordpress@localhost>',
    'recipient' => get_option('admin_email', 'admin@localhost'),
    'body' => "Von: [your-name] <[your-email]>\nBetreff: [your-subject]\n\nNachricht:\n[your-message]\n\n-- \nDiese E-Mail wurde von einem Kontaktformular auf RIMAN GmbH (http://localhost:8081) gesendet.",
    'additional_headers' => 'Reply-To: [your-email]',
    'attachments' => '',
    'use_html' => false,
    'exclude_blank' => false
);

$mail_2 = array(
    'active' => false,
    'subject' => '',
    'sender' => '',
    'recipient' => '',
    'body' => '',
    'additional_headers' => '',
    'attachments' => '',
    'use_html' => false,
    'exclude_blank' => false
);

// Messages auf Deutsch
$messages = array(
    'mail_sent_ok' => 'Vielen Dank für Ihre Nachricht. Sie wurde erfolgreich versendet.',
    'mail_sent_ng' => 'Beim Versenden Ihrer Nachricht ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.',
    'validation_error' => 'Ein oder mehrere Felder sind fehlerhaft. Bitte prüfen Sie Ihre Eingaben.',
    'spam' => 'Beim Versenden Ihrer Nachricht ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.',
    'accept_terms' => 'Sie müssen die Bedingungen akzeptieren.',
    'invalid_required' => 'Bitte füllen Sie dieses Feld aus.',
    'invalid_too_long' => 'Die Eingabe ist zu lang.',
    'invalid_too_short' => 'Die Eingabe ist zu kurz.',
    'upload_failed' => 'Beim Hochladen der Datei ist ein Fehler aufgetreten.',
    'upload_file_type_invalid' => 'Dieser Dateityp ist nicht erlaubt.',
    'upload_file_too_large' => 'Die Datei ist zu groß.',
    'upload_failed_php_error' => 'Beim Hochladen der Datei ist ein Fehler aufgetreten.',
    'invalid_date' => 'Das Datumsformat ist ungültig.',
    'date_too_early' => 'Das Datum liegt zu früh.',
    'date_too_late' => 'Das Datum liegt zu spät.',
    'invalid_number' => 'Das Zahlenformat ist ungültig.',
    'number_too_small' => 'Die Zahl ist zu klein.',
    'number_too_large' => 'Die Zahl ist zu groß.',
    'quiz_answer_not_correct' => 'Die Antwort ist nicht korrekt.',
    'invalid_email' => 'Die E-Mail-Adresse ist ungültig.',
    'invalid_url' => 'Die URL ist ungültig.',
    'invalid_tel' => 'Die Telefonnummer ist ungültig.'
);

// Additional Settings
$additional_settings = '';

// Properties Array
$properties = array(
    'form' => $form_content,
    'mail' => $mail,
    'mail_2' => $mail_2,
    'messages' => $messages,
    'additional_settings' => $additional_settings
);

// Speichere als serialisiertes Postmeta
$serialized = serialize($properties);

// Lösche alte Meta
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $form_id");

// Füge neue Meta hinzu
$stmt = $mysqli->prepare("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (?, '_form', ?)");
$stmt->bind_param('is', $form_id, $form_content);
$stmt->execute();

$stmt = $mysqli->prepare("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (?, '_mail', ?)");
$mail_serialized = serialize($mail);
$stmt->bind_param('is', $form_id, $mail_serialized);
$stmt->execute();

$stmt = $mysqli->prepare("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (?, '_mail_2', ?)");
$mail_2_serialized = serialize($mail_2);
$stmt->bind_param('is', $form_id, $mail_2_serialized);
$stmt->execute();

$stmt = $mysqli->prepare("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (?, '_messages', ?)");
$messages_serialized = serialize($messages);
$stmt->bind_param('is', $form_id, $messages_serialized);
$stmt->execute();

$stmt = $mysqli->prepare("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (?, '_additional_settings', ?)");
$stmt->bind_param('is', $form_id, $additional_settings);
$stmt->execute();

// Locale
$mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($form_id, '_locale', 'de_DE')");

// Config Validator  
$config_errors = array();
$mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($form_id, '_config_errors', '" . serialize($config_errors) . "')");

echo "✅ Contact Form 7 Metadaten gesetzt\n";

// Stelle sicher dass CSS geladen wird
$custom_css = '
/* Contact Form 7 Styles für dunklen Hintergrund */
.wpcf7 {
    background: transparent !important;
}

.wpcf7 input[type="text"],
.wpcf7 input[type="email"],
.wpcf7 textarea {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: #fff !important;
    padding: 12px 20px !important;
    width: 100% !important;
    margin-bottom: 20px !important;
    border-radius: 3px !important;
}

.wpcf7 input[type="text"]::placeholder,
.wpcf7 input[type="email"]::placeholder,
.wpcf7 textarea::placeholder {
    color: rgba(255,255,255,0.5) !important;
}

.wpcf7 input[type="submit"] {
    background: #b68c2f !important;
    color: #fff !important;
    border: 2px solid #b68c2f !important;
    padding: 12px 40px !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    border-radius: 3px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.wpcf7 input[type="submit"]:hover {
    background: transparent !important;
    color: #b68c2f !important;
}

.wpcf7-response-output {
    color: #fff !important;
    border-color: #b68c2f !important;
    margin: 20px 0 !important;
}

.wpcf7-not-valid-tip {
    color: #ff6b6b !important;
}

.wpcf7-validation-errors {
    border-color: #ff6b6b !important;
    color: #ff6b6b !important;
}

.wpcf7 form.sent .wpcf7-response-output {
    border-color: #46b450 !important;
    color: #46b450 !important;
}
';

// Füge Custom CSS zu Elementor hinzu
$mysqli->query("UPDATE wp_options SET option_value = CONCAT(option_value, '$custom_css') WHERE option_name = 'elementor_custom_css' LIMIT 1");

echo "✅ Custom CSS für dunklen Hintergrund hinzugefügt\n";

// Cache löschen
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_%cf7%'");
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_wpcf7%'");

echo "\n📧 Contact Form 7 komplett eingerichtet!\n";
echo "   - Form ID: $form_id\n";
echo "   - Deutsche Texte\n";
echo "   - Styling für dunklen Hintergrund\n";
echo "   - Placeholder-Texte\n\n";
echo "🌐 URL: http://localhost:8081/?page_id=3000\n";
echo "   Scrolle zum Kontaktformular\n";

$mysqli->close();