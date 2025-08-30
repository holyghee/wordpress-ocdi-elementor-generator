<?php
/**
 * Aktualisiert Elementor Data direkt aus der generierten XML
 */

$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Lade XML
$xml = simplexml_load_file('dynamic-elementor-output.xml');

// Registriere Namespaces
$xml->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');
$xml->registerXPathNamespace('content', 'http://purl.org/rss/1.0/modules/content/');

echo "📦 Aktualisiere Elementor Daten aus dynamic-elementor-output.xml\n\n";

// Verarbeite jedes Item
foreach ($xml->channel->item as $item) {
    $title = (string)$item->title;
    $post_id = null;
    $elementor_data = null;
    
    // Hole Post ID und Elementor Data
    foreach ($item->children('http://wordpress.org/export/1.2/')->postmeta as $postmeta) {
        $meta_key = (string)$postmeta->children('http://wordpress.org/export/1.2/')->meta_key;
        $meta_value = (string)$postmeta->children('http://wordpress.org/export/1.2/')->meta_value;
        
        if ($meta_key == '_elementor_data') {
            $elementor_data = $meta_value;
        }
    }
    
    $post_id = (string)$item->children('http://wordpress.org/export/1.2/')->post_id;
    
    if ($post_id && $elementor_data) {
        echo "📝 Aktualisiere: $title (ID: $post_id)\n";
        
        // Prüfe ob Post existiert
        $check = $mysqli->query("SELECT ID FROM wp_posts WHERE ID = $post_id");
        
        if ($check->num_rows > 0) {
            // Update Elementor Data
            $stmt = $mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = ? AND meta_key = '_elementor_data'");
            $stmt->bind_param('si', $elementor_data, $post_id);
            
            if ($stmt->execute()) {
                echo "   ✅ Elementor Data aktualisiert\n";
            } else {
                echo "   ❌ Fehler beim Update\n";
            }
            
            // Setze auch Template und Version
            $mysqli->query("UPDATE wp_postmeta SET meta_value = 'elementor_header_footer' WHERE post_id = $post_id AND meta_key = '_wp_page_template'");
            $mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = $post_id AND meta_key = '_elementor_version'");
            $mysqli->query("UPDATE wp_postmeta SET meta_value = 'builder' WHERE post_id = $post_id AND meta_key = '_elementor_edit_mode'");
            
        } else {
            echo "   ⚠️ Post existiert nicht, erstelle neu...\n";
            
            // Erstelle Post
            $post_name = strtolower(str_replace(' ', '-', $title));
            $insert_post = $mysqli->prepare("INSERT INTO wp_posts (ID, post_author, post_date, post_date_gmt, post_content, post_title, post_status, post_name, post_type, post_modified, post_modified_gmt) VALUES (?, 1, NOW(), NOW(), '', ?, 'publish', ?, 'page', NOW(), NOW())");
            $insert_post->bind_param('iss', $post_id, $title, $post_name);
            
            if ($insert_post->execute()) {
                echo "   ✅ Seite erstellt\n";
                
                // Füge Elementor Data hinzu
                $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($post_id, '_elementor_data', '" . $mysqli->real_escape_string($elementor_data) . "')");
                $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($post_id, '_wp_page_template', 'elementor_header_footer')");
                $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($post_id, '_elementor_version', '3.18.3')");
                $mysqli->query("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ($post_id, '_elementor_edit_mode', 'builder')");
            }
        }
    }
}

// Lösche Elementor Cache
$mysqli->query("DELETE FROM wp_options WHERE option_name LIKE '_transient_elementor%'");
$mysqli->query("DELETE FROM wp_postmeta WHERE meta_key = '_elementor_css'");

echo "\n✅ Alle Seiten aktualisiert!\n";
echo "\n🌐 URLs:\n";
echo "   - Startseite: http://localhost:8081/?page_id=3000\n";
echo "   - Asbestsanierung: http://localhost:8081/?page_id=3001\n";
echo "   - Über uns: http://localhost:8081/?page_id=3002\n";
echo "   - Kontakt: http://localhost:8081/?page_id=3003\n";

$mysqli->close();