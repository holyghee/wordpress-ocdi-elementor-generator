<?php
/**
 * Triggert Elementor CSS Generation durch Frontend-Aufruf
 */

echo "🔄 Triggere Elementor CSS Generation...\n\n";

// Lösche CSS Cache
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

// Lösche alten CSS Cache
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_css'");
$mysqli->query("DELETE FROM wp_postmeta WHERE post_id = 3000 AND meta_key = '_elementor_inline_svg'");
$mysqli->query("UPDATE wp_postmeta SET meta_value = '0' WHERE post_id = 3000 AND meta_key = '_elementor_css_time'");

echo "✅ CSS Cache gelöscht\n";

// Setze korrekte Elementor Version
$mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = 3000 AND meta_key = '_elementor_version'");

$mysqli->close();

// Rufe die Seite auf um CSS Generation zu triggern
$url = "http://localhost:8081/?page_id=3000";

echo "📡 Rufe Frontend auf: $url\n";

// Verwende cURL um die Seite aufzurufen
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 30);
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 Elementor CSS Generator');

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code == 200) {
    echo "✅ Seite erfolgreich aufgerufen (HTTP $http_code)\n";
    
    // Prüfe ob Shape Divider HTML generiert wurde
    if (strpos($response, 'elementor-shape') !== false) {
        echo "✅ Shape Divider HTML gefunden!\n";
        
        // Zähle Shape Dividers
        $count = substr_count($response, 'elementor-shape-bottom');
        echo "   → $count Shape Dividers im HTML\n";
    } else {
        echo "⚠️ Keine Shape Divider HTML gefunden\n";
        
        // Prüfe ob überhaupt Elementor aktiv ist
        if (strpos($response, 'elementor-section') !== false) {
            echo "   → Elementor ist aktiv\n";
        } else {
            echo "   ❌ Elementor scheint nicht aktiv zu sein\n";
        }
    }
    
    // Prüfe ob CSS generiert wurde
    if (strpos($response, 'elementor-post-3000.css') !== false) {
        echo "✅ Elementor CSS wird geladen\n";
    } else {
        echo "⚠️ Elementor CSS wird nicht geladen\n";
    }
    
} else {
    echo "❌ Fehler beim Seitenaufruf (HTTP $http_code)\n";
}

echo "\n🌐 Öffne im Browser: $url\n";
echo "💡 Hard Refresh mit Strg+F5!\n";