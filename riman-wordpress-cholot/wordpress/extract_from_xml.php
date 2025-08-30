<?php
/**
 * Extrahiert Elementor Data direkt aus demo-data-fixed.xml
 */

echo "📋 Extrahiere Elementor Data aus demo-data-fixed.xml...\n\n";

$xml_file = 'demo-data-fixed.xml';
if (!file_exists($xml_file)) {
    die("❌ demo-data-fixed.xml nicht gefunden!\n");
}

// Parse XML
$xml = simplexml_load_file($xml_file);

// Registriere Namespaces
$xml->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');
$xml->registerXPathNamespace('content', 'http://purl.org/rss/1.0/modules/content/');

// Suche nach der Home Page
$items = $xml->xpath('//item');

$found_home = false;
foreach ($items as $item) {
    $title = (string)$item->title;
    
    // Suche nach Home Page oder Page mit Elementor Data
    if (strpos($title, 'Home') !== false || $title == '') {
        echo "Prüfe Seite: '$title'\n";
        
        // Hole Postmeta
        $postmetas = $item->xpath('wp:postmeta');
        
        foreach ($postmetas as $postmeta) {
            $meta_key = (string)$postmeta->xpath('wp:meta_key')[0];
            
            if ($meta_key == '_elementor_data') {
                $meta_value = (string)$postmeta->xpath('wp:meta_value')[0];
                
                // Parse CDATA
                $meta_value = trim($meta_value);
                
                // Zähle Widgets
                $texticon_count = substr_count($meta_value, '"widgetType":"cholot-texticon"');
                $shape_count = substr_count($meta_value, '"shape_divider_bottom":"curve"');
                
                if ($texticon_count > 0 || $shape_count > 0) {
                    echo "\n✅ Gefunden! Home Page mit Service Cards:\n";
                    echo "   - $texticon_count cholot-texticon Widgets\n";
                    echo "   - $shape_count Shape Dividers\n";
                    
                    // Speichere in Datei
                    file_put_contents('extracted_elementor_data.json', $meta_value);
                    echo "\n💾 Gespeichert als: extracted_elementor_data.json\n";
                    
                    // Importiere in WordPress
                    $mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');
                    
                    // Hole aktuelle Daten um Hero zu behalten
                    $result = $mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_data'");
                    $row = $result->fetch_assoc();
                    $current_data = json_decode($row['meta_value'], true);
                    
                    // Parse die neuen Daten
                    $new_data = json_decode($meta_value, true);
                    
                    // Kombiniere: Hero von aktuell + Rest von XML
                    $combined_data = [];
                    
                    // Hero behalten (wenn vorhanden)
                    if (isset($current_data[0]) && isset($current_data[0]['elType']) && 
                        isset($current_data[0]['settings']) && 
                        (isset($current_data[0]['settings']['shape_divider_bottom']) || 
                         strpos(json_encode($current_data[0]), 'rdn-slider') !== false)) {
                        $combined_data[] = $current_data[0];
                        echo "\n✅ Hero Section beibehalten\n";
                    }
                    
                    // Füge Service Cards und Rest aus XML hinzu
                    foreach ($new_data as $section) {
                        // Skip Hero wenn es eine ist
                        if (isset($section['elType']) && $section['elType'] == 'section') {
                            $section_json = json_encode($section);
                            // Füge alle Sections außer Hero hinzu
                            if (strpos($section_json, 'rdn-slider') === false) {
                                $combined_data[] = $section;
                            }
                        }
                    }
                    
                    // Speichere kombinierte Daten
                    $final_data = json_encode($combined_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
                    
                    $stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = 3000 AND meta_key = '_elementor_data'");
                    $stmt->bind_param('s', $final_data);
                    
                    if ($stmt->execute()) {
                        echo "✅ Elementor Data importiert in Page 3000\n";
                        
                        // Zähle finale Widgets
                        $final_texticon = substr_count($final_data, '"widgetType":"cholot-texticon"');
                        $final_shape = substr_count($final_data, '"shape_divider_bottom":"curve"');
                        
                        echo "   - $final_texticon cholot-texticon Widgets in DB\n";
                        echo "   - $final_shape Shape Dividers in DB\n";
                    }
                    
                    // Setze Metadaten
                    $mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = 3000 AND meta_key = '_elementor_version'");
                    $mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor' WHERE post_id = 3000 AND meta_key = '_elementor_edit_mode'");
                    $mysqli->query("UPDATE wp_postmeta SET meta_value = 'default' WHERE post_id = 3000 AND meta_key = '_elementor_template_type'");
                    
                    // Clear Cache
                    $mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
                    $mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
                    
                    $mysqli->close();
                    
                    $found_home = true;
                    break;
                }
            }
        }
        
        if ($found_home) break;
    }
}

if (!$found_home) {
    echo "❌ Keine Home Page mit Service Cards gefunden!\n";
} else {
    echo "\n🌐 URL: http://localhost:8081/?page_id=3000\n";
    echo "💡 Hard Refresh mit Strg+F5!\n";
    echo "\n📝 Die Original XML Struktur wurde importiert.\n";
    echo "   Wenn es jetzt funktioniert, lag es an der exakten Struktur.\n";
}