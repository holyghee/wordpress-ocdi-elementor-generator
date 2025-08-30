<?php
/**
 * Exportiere einzelne Elementor Blocks als JSON
 * Für modulare Wiederverwendung im Generator
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "📦 Exportiere individuelle Elementor Blocks...\n\n";

// Erstelle Verzeichnisstruktur
$export_dir = 'elementor_blocks';
$dirs = [
    $export_dir,
    $export_dir . '/hero',
    $export_dir . '/services',
    $export_dir . '/testimonials',
    $export_dir . '/contact',
    $export_dir . '/custom'
];

foreach ($dirs as $dir) {
    if (!file_exists($dir)) {
        mkdir($dir, 0755, true);
    }
}

// Hole die aktuelle Elementor Data von Seite 3000 (RIMAN)
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
if ($row = $result->fetch_assoc()) {
    $elementor_data = json_decode($row['meta_value'], true);
    
    if ($elementor_data && is_array($elementor_data)) {
        foreach ($elementor_data as $index => $section) {
            $section_type = identifySectionType($section);
            exportSection($section, $section_type, $index);
        }
    }
}

// Funktion um Section-Typ zu identifizieren
function identifySectionType($section) {
    $widgets = extractWidgets($section);
    
    if (in_array('rdn-slider', $widgets)) {
        return 'hero';
    } elseif (in_array('cholot-texticon', $widgets) && hasShapeDivider($section)) {
        return 'services';
    } elseif (in_array('testimonial-carousel', $widgets)) {
        return 'testimonials';
    } elseif (strpos(json_encode($section), 'contact-form-7') !== false) {
        return 'contact';
    } else {
        return 'custom';
    }
}

// Extrahiere alle Widgets aus einer Section
function extractWidgets($element) {
    $widgets = [];
    
    if (isset($element['widgetType'])) {
        $widgets[] = $element['widgetType'];
    }
    
    if (isset($element['elements'])) {
        foreach ($element['elements'] as $child) {
            $widgets = array_merge($widgets, extractWidgets($child));
        }
    }
    
    return $widgets;
}

// Prüfe ob Section einen Shape Divider hat
function hasShapeDivider($element) {
    $json = json_encode($element);
    return strpos($json, 'shape_divider_bottom') !== false || 
           strpos($json, 'shape_divider_top') !== false;
}

// Exportiere Section als JSON
function exportSection($section, $type, $index) {
    global $export_dir;
    
    // Bereinige IDs für Wiederverwendung
    $clean_section = cleanIds($section);
    
    // Erstelle Metadaten
    $metadata = [
        'type' => $type,
        'name' => generateSectionName($section, $type, $index),
        'description' => generateDescription($section, $type),
        'widgets' => extractWidgets($section),
        'has_shape_divider' => hasShapeDivider($section),
        'configurable_fields' => extractConfigurableFields($section)
    ];
    
    // Export-Struktur
    $export = [
        'metadata' => $metadata,
        'structure' => $clean_section
    ];
    
    // Dateiname
    $filename = $export_dir . '/' . $type . '/' . $metadata['name'] . '.json';
    
    // Speichere JSON
    file_put_contents($filename, json_encode($export, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo "✅ Exportiert: " . $filename . "\n";
}

// Bereinige IDs für Wiederverwendbarkeit
function cleanIds($element) {
    if (is_array($element)) {
        $clean = [];
        foreach ($element as $key => $value) {
            if ($key === 'id') {
                $clean[$key] = '{{ID}}';
            } elseif (is_array($value)) {
                $clean[$key] = cleanIds($value);
            } else {
                $clean[$key] = $value;
            }
        }
        return $clean;
    }
    return $element;
}

// Generiere Section Namen
function generateSectionName($section, $type, $index) {
    $name = $type . '_' . $index;
    
    // Spezifische Namen für bekannte Sections
    if ($type === 'services' && isset($section['elements'])) {
        $columns = count($section['elements']);
        $name = 'service_cards_' . $columns . '_columns';
    } elseif ($type === 'hero') {
        $name = 'hero_slider_main';
    } elseif ($type === 'testimonials') {
        $name = 'testimonial_carousel';
    } elseif ($type === 'contact') {
        $name = 'contact_form_section';
    }
    
    return $name;
}

// Generiere Beschreibung
function generateDescription($section, $type) {
    $desc = ucfirst($type) . ' section';
    
    if (hasShapeDivider($section)) {
        $desc .= ' with curved shape divider';
    }
    
    $widgets = extractWidgets($section);
    if (!empty($widgets)) {
        $desc .= ' containing: ' . implode(', ', array_unique($widgets));
    }
    
    return $desc;
}

// Extrahiere konfigurierbare Felder
function extractConfigurableFields($section) {
    $fields = [];
    
    // Suche nach Text-Inhalten
    $json = json_encode($section);
    
    if (strpos($json, '"title"') !== false) {
        $fields[] = 'title';
    }
    if (strpos($json, '"subtitle"') !== false) {
        $fields[] = 'subtitle';
    }
    if (strpos($json, '"text"') !== false || strpos($json, '"editor"') !== false) {
        $fields[] = 'content';
    }
    if (strpos($json, '"image"') !== false || strpos($json, 'background_image') !== false) {
        $fields[] = 'image';
    }
    if (strpos($json, '"selected_icon"') !== false) {
        $fields[] = 'icon';
    }
    if (strpos($json, '"button_text"') !== false) {
        $fields[] = 'button';
    }
    
    return array_unique($fields);
}

// Exportiere auch einzelne Service Cards
echo "\n📦 Exportiere einzelne Service Cards...\n";

// Hole Service Cards Section
foreach ($elementor_data as $section) {
    if (identifySectionType($section) === 'services' && isset($section['elements'])) {
        foreach ($section['elements'] as $card_index => $card) {
            if ($card['elType'] === 'column') {
                $card_name = 'service_card_' . ($card_index + 1);
                
                // Extrahiere Card-Daten
                $card_data = extractCardData($card);
                
                $export = [
                    'metadata' => [
                        'type' => 'service_card',
                        'name' => $card_name,
                        'title' => $card_data['title'] ?? '',
                        'subtitle' => $card_data['subtitle'] ?? '',
                        'icon' => $card_data['icon'] ?? '',
                        'has_image' => $card_data['has_image'] ?? false,
                        'has_shape_divider' => hasShapeDivider($card)
                    ],
                    'structure' => cleanIds($card)
                ];
                
                $filename = $export_dir . '/services/' . $card_name . '.json';
                file_put_contents($filename, json_encode($export, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
                echo "✅ Service Card exportiert: " . $filename . "\n";
            }
        }
    }
}

// Extrahiere Card-Daten
function extractCardData($card) {
    $data = [];
    $json = json_encode($card);
    
    // Suche nach cholot-texticon Widget
    if (preg_match('/"title":\s*"([^"]+)"/', $json, $matches)) {
        $data['title'] = $matches[1];
    }
    if (preg_match('/"subtitle":\s*"([^"]+)"/', $json, $matches)) {
        $data['subtitle'] = $matches[1];
    }
    if (preg_match('/"value":\s*"([^"]+)"/', $json, $matches)) {
        $data['icon'] = $matches[1];
    }
    
    $data['has_image'] = strpos($json, 'background_image') !== false;
    
    return $data;
}

echo "\n✅ Export abgeschlossen!\n";
echo "📁 Blocks gespeichert in: " . realpath($export_dir) . "\n";

$mysqli->close();