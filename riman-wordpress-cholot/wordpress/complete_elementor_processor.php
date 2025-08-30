<?php
/**
 * Kompletter Elementor Processor
 * Versteht und repliziert die Cholot Theme Struktur korrekt
 */

class CompleteElementorProcessor {
    
    private $mysqli;
    private $img_server = "http://localhost:3456";
    
    public function __construct() {
        $this->mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');
        if ($this->mysqli->connect_error) {
            die('Connection failed: ' . $this->mysqli->connect_error);
        }
    }
    
    /**
     * Generiert komplette Seite aus Config Array
     */
    public function generateFromConfig($config) {
        echo "📋 Verarbeite Config...\n";
        
        foreach ($config['pages'] as $page) {
            $sections = [];
            
            foreach ($page['sections'] as $section_config) {
                if ($section_config['type'] == 'service_cards') {
                    $section = $this->generateServiceCardsSection($section_config['cards']);
                    $sections[] = $section;
                }
            }
            
            // Importiere in WordPress
            $this->importToWordPress($sections, 3000);
        }
    }
    
    /**
     * Generiert Service Cards Section mit korrekter Struktur
     */
    private function generateServiceCardsSection($cards) {
        $section = [
            "id" => $this->generateId(),
            "elType" => "section",
            "settings" => [
                "gap" => "extended",
                "custom_height" => ["unit" => "px", "size" => 300, "sizes" => []],
                "content_position" => "middle",
                "structure" => "30",
                "background_color" => "#b68c2f",
                "box_shadow_box_shadow" => [
                    "horizontal" => 10,
                    "vertical" => 0,
                    "blur" => 0,
                    "spread" => 4,
                    "color" => "#ededed"
                ],
                "margin" => ["unit" => "px", "top" => -100, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false]
            ],
            "elements" => [],
            "isInner" => false  // Wichtig: Outer Section
        ];
        
        foreach ($cards as $index => $card) {
            $column = $this->generateServiceCard($card, $index);
            $section['elements'][] = $column;
        }
        
        return $section;
    }
    
    /**
     * Generiert einzelne Service Card mit Shape Divider
     */
    private function generateServiceCard($card, $index) {
        return [
            "id" => $this->generateId(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "_inline_size" => null,
                "background_background" => "classic",
                "background_size" => "cover",
                "border_width" => ["unit" => "px", "top" => 10, "right" => 0, "bottom" => 10, "left" => 10, "isLinked" => false],
                "border_color" => "#ededed",
                "box_shadow_box_shadow" => [
                    "horizontal" => 0,
                    "vertical" => 4,
                    "blur" => 5,
                    "spread" => 0,
                    "color" => "rgba(196,196,196,0.26)"
                ],
                "z_index" => 1,
                "background_color" => "#fafafa",
                "box_shadow_box_shadow_type" => "yes",
                "margin" => ["unit" => "px", "top" => 15, "right" => 15, "bottom" => 15, "left" => 15, "isLinked" => true],
                "animation" => "fadeInUp",
                "animation_duration" => "fast",
                "animation_delay" => $index * 200
            ],
            "elements" => [
                // Inner Section 1: Bild mit Shape Divider
                [
                    "id" => $this->generateId(),
                    "elType" => "section",
                    "settings" => [
                        "gap" => "no",
                        // KRITISCH: Diese Settings generieren den Shape Divider
                        "shape_divider_bottom" => "curve",
                        "shape_divider_bottom_color" => "#fafafa",
                        "shape_divider_bottom_width" => ["unit" => "%", "size" => 100],
                        "shape_divider_bottom_height" => ["unit" => "px", "size" => 50],
                        "shape_divider_bottom_negative" => "yes",
                        "shape_divider_bottom_above_content" => "yes"
                    ],
                    "elements" => [
                        [
                            "id" => $this->generateId(),
                            "elType" => "column",
                            "settings" => [
                                "_column_size" => 100,
                                "_inline_size" => null
                            ],
                            "elements" => [
                                [
                                    "id" => $this->generateId(),
                                    "elType" => "widget",
                                    "settings" => [
                                        "image" => [
                                            "url" => $card['image'],
                                            "id" => ""
                                        ],
                                        "opacity" => ["unit" => "px", "size" => 1, "sizes" => []],
                                        "_border_width" => ["unit" => "px", "top" => 4, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                                        "_border_color" => "#b68c2f"
                                    ],
                                    "elements" => [],
                                    "widgetType" => "image"
                                ]
                            ],
                            "isInner" => true
                        ]
                    ],
                    "isInner" => true  // KRITISCH: Muss true sein für Inner Section
                ],
                // Inner Section 2: Content
                [
                    "id" => $this->generateId(),
                    "elType" => "section",
                    "settings" => [
                        "gap" => "no",
                        "content_position" => "middle",
                        "background_background" => "classic",
                        "margin" => ["unit" => "px", "top" => -30, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                        "z_index" => 2
                    ],
                    "elements" => [
                        [
                            "id" => $this->generateId(),
                            "elType" => "column",
                            "settings" => [
                                "_column_size" => 100,
                                "_inline_size" => null
                            ],
                            "elements" => [
                                [
                                    "id" => $this->generateId(),
                                    "elType" => "widget",
                                    "settings" => [
                                        "title" => $card['title'],
                                        "subtitle" => $card['subtitle'],
                                        "text" => "<p>{$card['description']}</p>",
                                        "selected_icon" => [
                                            "value" => $card['icon'],
                                            "library" => "fa-solid"
                                        ],
                                        "__fa4_migrated" => ["selected_icon" => true],
                                        "title_typography_typography" => "custom",
                                        "title_typography_font_size" => ["unit" => "px", "size" => 28, "sizes" => []],
                                        "title_margin" => ["unit" => "px", "top" => 0, "right" => 0, "bottom" => 15, "left" => 0, "isLinked" => false],
                                        "subtitle_typography_typography" => "custom",
                                        "subtitle_typography_font_size" => ["unit" => "px", "size" => 13, "sizes" => []],
                                        "subtitle_typography_font_weight" => "700",
                                        "subtitle_typography_text_transform" => "uppercase",
                                        "subtitle_typography_letter_spacing" => ["unit" => "px", "size" => 1, "sizes" => []],
                                        "subtitle_color" => "#b68c2f",
                                        "text_typography_font_size" => ["unit" => "px", "size" => 15, "sizes" => []],
                                        "text_typography_font_style" => "italic",
                                        "icon_size" => ["unit" => "px", "size" => 20, "sizes" => []],
                                        "icon_bg_size" => ["unit" => "px", "size" => 72, "sizes" => []],
                                        "icon_color" => "#ffffff",
                                        "iconbg_color" => "#b68c2f",
                                        "icon_margin" => ["unit" => "px", "top" => -27, "right" => 0, "bottom" => 0, "left" => 0, "isLinked" => false],
                                        "_padding" => ["unit" => "px", "top" => 30, "right" => 30, "bottom" => 30, "left" => 30, "isLinked" => true]
                                    ],
                                    "elements" => [],
                                    "widgetType" => "cholot-texticon"
                                ]
                            ],
                            "isInner" => true
                        ]
                    ],
                    "isInner" => true  // KRITISCH: Muss true sein für Inner Section
                ]
            ],
            "isInner" => false
        ];
    }
    
    /**
     * Importiert in WordPress mit korrekten Settings
     */
    private function importToWordPress($sections, $post_id) {
        echo "\n📥 Importiere in WordPress...\n";
        
        // Hole aktuelle Daten (Hero behalten)
        $result = $this->mysqli->query("SELECT meta_value FROM wp_postmeta WHERE post_id = $post_id AND meta_key = '_elementor_data'");
        $row = $result->fetch_assoc();
        $current_data = json_decode($row['meta_value'], true);
        
        $new_data = [];
        
        // Hero behalten
        if (isset($current_data[0])) {
            $new_data[] = $current_data[0];
            echo "   ✅ Hero Section beibehalten\n";
        }
        
        // Neue Sections einfügen
        foreach ($sections as $section) {
            $new_data[] = $section;
            echo "   ✅ Service Cards Section eingefügt\n";
        }
        
        // Contact Form behalten
        for ($i = 2; $i < count($current_data); $i++) {
            if (isset($current_data[$i])) {
                $json = json_encode($current_data[$i]);
                if (strpos($json, 'contact') !== false) {
                    $new_data[] = $current_data[$i];
                    echo "   ✅ Contact Form beibehalten\n";
                }
            }
        }
        
        // Speichere mit korrekten JSON Settings
        $updated_data = json_encode($new_data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        
        $stmt = $this->mysqli->prepare("UPDATE wp_postmeta SET meta_value = ? WHERE post_id = ? AND meta_key = '_elementor_data'");
        $stmt->bind_param('si', $updated_data, $post_id);
        $stmt->execute();
        
        // Setze Elementor Version
        $this->mysqli->query("UPDATE wp_postmeta SET meta_value = '3.18.3' WHERE post_id = $post_id AND meta_key = '_elementor_version'");
        
        // Lösche CSS Cache
        $this->mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $post_id AND meta_key = '_elementor_css'");
        $this->mysqli->query("DELETE FROM wp_postmeta WHERE post_id = $post_id AND meta_key = '_elementor_inline_svg'");
        
        echo "\n✅ Import abgeschlossen!\n";
    }
    
    private function generateId() {
        return substr(md5(uniqid()), 0, 7);
    }
}

// HAUPTPROGRAMM
echo "🚀 KOMPLETTER ELEMENTOR PROCESSOR\n";
echo "==================================\n\n";

$processor = new CompleteElementorProcessor();

// Erstelle Test YAML
$yaml_content = "
pages:
  - title: RIMAN GmbH
    sections:
      - type: service_cards
        cards:
          - title: Asbestsanierung
            subtitle: ZERTIFIZIERT
            description: Professionelle Entfernung von Asbest nach TRGS 519 mit höchsten Sicherheitsstandards.
            icon: fas fa-shield-alt
            image: http://localhost:3456/asbestsanierung-schutzausruestung-fachpersonal.jpg
          - title: PCB-Sanierung
            subtitle: FACHGERECHT
            description: Sichere Beseitigung von PCB-belasteten Materialien nach aktuellen Vorschriften.
            icon: fas fa-industry
            image: http://localhost:3456/schadstoffsanierung-industrieanlage-riman-gmbh.jpg
          - title: Schimmelsanierung
            subtitle: NACHHALTIG
            description: Nachhaltige Schimmelbeseitigung und Prävention für gesundes Wohnen.
            icon: fas fa-home
            image: http://localhost:3456/umweltingenieur-bodenproben-analyse-labor.jpg
";

file_put_contents('riman_complete.yaml', $yaml_content);
echo "✅ YAML Config erstellt\n";

// Generiere und importiere
$processor->generateFromYaml('riman_complete.yaml');

echo "\n🎯 VERSTÄNDNIS DES PROZESSES:\n";
echo "============================\n";
echo "1. ✅ Shape Divider Settings in Inner Sections\n";
echo "2. ✅ isInner Flag korrekt gesetzt\n";
echo "3. ✅ Widget Types exact match (cholot-texticon)\n";
echo "4. ✅ CSS Cache gelöscht für Regenerierung\n";
echo "5. ✅ Elementor Version gesetzt\n\n";

echo "🌐 Öffne: http://localhost:8081/?page_id=3000\n";
echo "   → Shape Dividers werden beim Frontend-Rendering generiert\n";
echo "   → CSS wird lazy beim ersten Aufruf generiert\n";
echo "💡 Hard Refresh mit Strg+F5!\n";