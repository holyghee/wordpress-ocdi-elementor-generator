<?php
/**
 * Analysiert die Original Cholot Theme Elementor-Struktur von Port 8080
 */

// Verbinde zur Original Cholot DB (Port 8080)
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_mediation_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

echo "🔍 Analysiere Original Cholot Theme Elementor-Struktur (Port 8080)...\n\n";

// Hole die Homepage Elementor Data
$query = "SELECT p.ID, p.post_title, pm.meta_value 
          FROM wp_posts p 
          INNER JOIN wp_postmeta pm ON p.ID = pm.post_id 
          WHERE pm.meta_key = '_elementor_data' 
          AND p.post_type = 'page'
          AND p.post_title LIKE '%Home%'
          LIMIT 1";

$result = $mysqli->query($query);

if ($row = $result->fetch_assoc()) {
    $elementor_data = json_decode($row['meta_value'], true);
    
    echo "📄 Analysiere Seite: " . $row['post_title'] . " (ID: " . $row['ID'] . ")\n\n";
    
    // Analysiere jede Section
    foreach ($elementor_data as $index => $section) {
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
        echo "SECTION $index:\n";
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
        
        // Section Settings
        if (isset($section['settings'])) {
            echo "Settings:\n";
            foreach ($section['settings'] as $key => $value) {
                if (strpos($key, 'shape_divider') !== false) {
                    echo "  🎨 $key: " . json_encode($value) . "\n";
                }
            }
        }
        
        // Suche nach Service Cards
        if (isset($section['elements'])) {
            foreach ($section['elements'] as $colIndex => $column) {
                if ($column['elType'] == 'column') {
                    echo "\n  Column $colIndex (Size: " . ($column['settings']['_column_size'] ?? 'auto') . "):\n";
                    
                    // Analysiere Inner Sections
                    if (isset($column['elements'])) {
                        foreach ($column['elements'] as $elemIndex => $element) {
                            if (isset($element['elType']) && $element['elType'] == 'section' && isset($element['isInner'])) {
                                echo "    📦 Inner Section $elemIndex:\n";
                                
                                // Shape Divider Settings
                                if (isset($element['settings'])) {
                                    $has_shape = false;
                                    foreach ($element['settings'] as $key => $value) {
                                        if (strpos($key, 'shape_divider') !== false) {
                                            echo "      → $key: " . json_encode($value) . "\n";
                                            $has_shape = true;
                                        }
                                        if ($key == 'background_image') {
                                            echo "      → Has Background Image\n";
                                        }
                                    }
                                    if ($has_shape) {
                                        echo "      ✅ HAS SHAPE DIVIDER!\n";
                                    }
                                }
                                
                                // Widgets in Inner Section
                                if (isset($element['elements'])) {
                                    foreach ($element['elements'] as $innerCol) {
                                        if (isset($innerCol['elements'])) {
                                            foreach ($innerCol['elements'] as $widget) {
                                                if (isset($widget['widgetType'])) {
                                                    echo "      Widget: " . $widget['widgetType'] . "\n";
                                                }
                                            }
                                        }
                                    }
                                }
                            } elseif (isset($element['widgetType'])) {
                                echo "    Widget: " . $element['widgetType'] . "\n";
                            }
                        }
                    }
                }
            }
        }
        echo "\n";
    }
    
    // Speichere die Original-Struktur als Referenz
    file_put_contents('original_cholot_structure.json', json_encode($elementor_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    echo "✅ Original-Struktur gespeichert als: original_cholot_structure.json\n";
    
} else {
    echo "❌ Keine Homepage gefunden\n";
}

$mysqli->close();