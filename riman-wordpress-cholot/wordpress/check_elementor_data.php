<?php
// Überprüfe was in der Datenbank steht
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Hole Elementor Daten
$result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
$row = $result->fetch_assoc();
$elementor_data = json_decode($row['meta_value'], true);

echo "=== ELEMENTOR DATA STRUCTURE ===\n\n";
echo "Anzahl Hauptsektionen: " . count($elementor_data) . "\n\n";

foreach ($elementor_data as $index => $section) {
    echo "Section $index:\n";
    echo "- ID: " . ($section['id'] ?? 'N/A') . "\n";
    echo "- Type: " . ($section['elType'] ?? 'N/A') . "\n";
    
    if (isset($section['settings']['content_width'])) {
        echo "- Width: " . json_encode($section['settings']['content_width']) . "\n";
    }
    
    if (isset($section['elements']) && is_array($section['elements'])) {
        echo "- Columns: " . count($section['elements']) . "\n";
        
        foreach ($section['elements'] as $colIndex => $column) {
            if (isset($column['elType']) && $column['elType'] === 'column') {
                echo "  - Column $colIndex: ";
                echo "Size=" . ($column['settings']['_column_size'] ?? 'N/A') . ", ";
                echo "Elements=" . (isset($column['elements']) ? count($column['elements']) : 0) . "\n";
                
                // Zeige erste Widget-Info
                if (isset($column['elements'][0])) {
                    $firstElement = $column['elements'][0];
                    if (isset($firstElement['widgetType'])) {
                        echo "    First widget: " . $firstElement['widgetType'] . "\n";
                    } elseif (isset($firstElement['elType']) && $firstElement['elType'] === 'section') {
                        echo "    First element: Inner Section\n";
                        if (isset($firstElement['settings']['shape_divider_bottom'])) {
                            echo "    Has shape divider: " . $firstElement['settings']['shape_divider_bottom'] . "\n";
                        }
                        if (isset($firstElement['settings']['background_image'])) {
                            echo "    Has background image: YES\n";
                        }
                    }
                }
            }
        }
    }
    echo "\n";
}

// Prüfe auch Elementor Version
$result2 = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_version'");
if ($row2 = $result2->fetch_assoc()) {
    echo "Elementor Version: " . $row2['meta_value'] . "\n";
}

// Prüfe ob Elementor Edit Mode aktiv
$result3 = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_edit_mode'");
if ($row3 = $result3->fetch_assoc()) {
    echo "Elementor Edit Mode: " . $row3['meta_value'] . "\n";
}

$mysqli->close();