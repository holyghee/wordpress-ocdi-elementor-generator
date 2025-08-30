<?php
/**
 * Elementor Processor - Versteht wie Elementor CSS aus JSON generiert
 * Analysiert und repliziert die Cholot Theme Struktur
 */

class ElementorProcessor {
    
    private $mysqli;
    private $elementor_version = '3.18.3';
    
    public function __construct($db_config) {
        $this->mysqli = new mysqli(
            $db_config['host'],
            $db_config['user'],
            $db_config['password'],
            $db_config['database']
        );
        
        if ($this->mysqli->connect_error) {
            die('Connection failed: ' . $this->mysqli->connect_error);
        }
    }
    
    /**
     * Analysiert die Original Cholot Struktur aus Port 8080
     */
    public function analyzeOriginalStructure($source_db, $post_id) {
        // Wechsle zur Original DB
        $this->mysqli->select_db($source_db);
        
        // Hole Elementor Data
        $result = $this->mysqli->query("
            SELECT meta_value 
            FROM wp_postmeta 
            WHERE post_id = $post_id AND meta_key = '_elementor_data'
        ");
        
        if ($row = $result->fetch_assoc()) {
            $elementor_data = json_decode($row['meta_value'], true);
            
            // Analysiere Shape Dividers
            $shape_dividers = $this->extractShapeDividers($elementor_data);
            
            // Analysiere CSS Generation Trigger
            $css_triggers = $this->analyzeCssTriggers($elementor_data);
            
            return [
                'data' => $elementor_data,
                'shape_dividers' => $shape_dividers,
                'css_triggers' => $css_triggers
            ];
        }
        
        return null;
    }
    
    /**
     * Extrahiert alle Shape Divider Konfigurationen
     */
    private function extractShapeDividers($elements, $path = '') {
        $shape_dividers = [];
        
        foreach ($elements as $i => $element) {
            $current_path = $path . "[$i]";
            
            if (isset($element['settings'])) {
                $settings = $element['settings'];
                
                // Prüfe auf Shape Divider Settings
                foreach (['top', 'bottom'] as $position) {
                    $key = "shape_divider_$position";
                    if (isset($settings[$key])) {
                        $divider_info = [
                            'path' => $current_path,
                            'position' => $position,
                            'type' => $settings[$key],
                            'color' => $settings["{$key}_color"] ?? null,
                            'width' => $settings["{$key}_width"] ?? null,
                            'height' => $settings["{$key}_height"] ?? null,
                            'negative' => $settings["{$key}_negative"] ?? null,
                            'flip' => $settings["{$key}_flip"] ?? null,
                            'above_content' => $settings["{$key}_above_content"] ?? null,
                            'element_type' => $element['elType'] ?? null,
                            'is_inner' => $element['isInner'] ?? false
                        ];
                        $shape_dividers[] = $divider_info;
                        
                        echo "   🔍 Shape Divider gefunden: {$divider_info['type']} ($position)\n";
                        echo "      - Element: {$divider_info['element_type']}\n";
                        echo "      - Inner: " . ($divider_info['is_inner'] ? 'Ja' : 'Nein') . "\n";
                        echo "      - Negative: {$divider_info['negative']}\n";
                        echo "      - Color: {$divider_info['color']}\n\n";
                    }
                }
            }
            
            // Rekursiv
            if (isset($element['elements']) && is_array($element['elements'])) {
                $child_dividers = $this->extractShapeDividers(
                    $element['elements'],
                    $current_path . '.elements'
                );
                $shape_dividers = array_merge($shape_dividers, $child_dividers);
            }
        }
        
        return $shape_dividers;
    }
    
    /**
     * Analysiert was CSS Generation triggert
     */
    private function analyzeCssTriggers($elements) {
        $triggers = [];
        
        // Settings die CSS Generation triggern
        $css_trigger_settings = [
            'shape_divider_top',
            'shape_divider_bottom',
            'background_background',
            'border_border',
            'box_shadow_box_shadow_type',
            'animation'
        ];
        
        $this->findTriggers($elements, $css_trigger_settings, $triggers);
        
        return $triggers;
    }
    
    private function findTriggers($elements, $trigger_settings, &$triggers) {
        foreach ($elements as $element) {
            if (isset($element['settings'])) {
                foreach ($trigger_settings as $trigger) {
                    if (isset($element['settings'][$trigger])) {
                        $triggers[] = [
                            'setting' => $trigger,
                            'value' => $element['settings'][$trigger],
                            'element_type' => $element['elType'] ?? 'unknown'
                        ];
                    }
                }
            }
            
            if (isset($element['elements'])) {
                $this->findTriggers($element['elements'], $trigger_settings, $triggers);
            }
        }
    }
    
    /**
     * Versteht und dokumentiert die Elementor CSS Generation
     */
    public function understandCssGeneration() {
        echo "\n📚 ELEMENTOR CSS GENERATION VERSTEHEN:\n";
        echo "=====================================\n\n";
        
        echo "1. SHAPE DIVIDERS:\n";
        echo "   - Werden NICHT in der Datenbank gespeichert\n";
        echo "   - Werden beim Frontend-Rendering generiert\n";
        echo "   - Benötigen diese Settings in der JSON:\n";
        echo "     • shape_divider_[position]: 'curve' (oder anderer Typ)\n";
        echo "     • shape_divider_[position]_color: '#fafafa'\n";
        echo "     • shape_divider_[position]_negative: 'yes' (für Inversion)\n";
        echo "     • shape_divider_[position]_above_content: 'yes'\n\n";
        
        echo "2. CSS GENERATION TRIGGER:\n";
        echo "   - _elementor_css wird gelöscht → Regenerierung\n";
        echo "   - _elementor_version muss gesetzt sein\n";
        echo "   - Frontend-Aufruf triggert CSS Generation\n\n";
        
        echo "3. CHOLOT THEME WIDGETS:\n";
        echo "   - cholot-texticon benötigt Theme-Aktivierung\n";
        echo "   - Widget CSS kommt vom Theme, nicht Elementor\n";
        echo "   - Theme muss die Widget-Klassen bereitstellen\n\n";
        
        echo "4. KRITISCHE PUNKTE:\n";
        echo "   ⚠️  isInner muss für Inner Sections true sein\n";
        echo "   ⚠️  Widget Type muss exact match sein (z.B. 'cholot-texticon')\n";
        echo "   ⚠️  Shape Dividers nur bei Sections, nicht Columns\n";
        echo "   ⚠️  CSS wird LAZY generiert beim ersten Aufruf\n\n";
    }
}

// HAUPTPROGRAMM
echo "🔬 ELEMENTOR PROCESSOR - ANALYSE\n";
echo "=================================\n\n";

$db_config = [
    'host' => 'localhost',
    'user' => 'wp_user',
    'password' => 'wp_password123',
    'database' => 'wordpress_cholot_test'
];

$processor = new ElementorProcessor($db_config);

// 1. Analysiere Original Cholot (Port 8080)
echo "📊 Analysiere Original Cholot Theme (Port 8080)...\n\n";
$original = $processor->analyzeOriginalStructure('wordpress_mediation', 45);

if ($original) {
    echo "\n✅ Analyse abgeschlossen:\n";
    echo "   - " . count($original['shape_dividers']) . " Shape Dividers gefunden\n";
    echo "   - " . count($original['css_triggers']) . " CSS Trigger gefunden\n\n";
    
    // Speichere Analyse
    file_put_contents(
        'cholot_structure_analysis.json',
        json_encode($original, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
    );
    echo "💾 Analyse gespeichert: cholot_structure_analysis.json\n";
}

// 2. Verstehe CSS Generation
$processor->understandCssGeneration();

// 3. Zeige wie es richtig gemacht wird
echo "✅ LÖSUNG:\n";
echo "=========\n\n";
echo "Der Prozessor muss:\n";
echo "1. Die exakte JSON Struktur aus der Original XML/Demo verwenden\n";
echo "2. Shape Divider Settings korrekt in Inner Sections platzieren\n";
echo "3. CSS Cache löschen nach Import\n";
echo "4. Frontend aufrufen um CSS Generation zu triggern\n\n";

echo "🎯 Nächster Schritt:\n";
echo "   php import_with_understanding.php\n";
echo "   → Importiert mit korrektem Verständnis der Elementor Mechanik\n";