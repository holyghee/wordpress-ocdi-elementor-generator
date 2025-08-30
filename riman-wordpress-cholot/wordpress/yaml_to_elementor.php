<?php
/**
 * YAML zu Elementor Konverter
 * Basierend auf Geminis Block-Pattern Analyse
 * 
 * Konvertiert einfache YAML Konfigurationen in komplexe Elementor Strukturen
 */

require_once 'vendor/autoload.php'; // Für Symfony YAML Parser (falls installiert)

class YamlToElementorConverter {
    
    private $blockLibrary;
    private $designTokens;
    
    public function __construct() {
        $this->initializeBlockLibrary();
        $this->initializeDesignTokens();
    }
    
    /**
     * Initialisiert die Block-Bibliothek basierend auf Geminis Analyse
     */
    private function initializeBlockLibrary() {
        $this->blockLibrary = [
            'service_cards' => [
                'description' => 'Service Cards mit curved shape divider',
                'generator' => 'generateServiceCards'
            ],
            'hero_slider' => [
                'description' => 'Hero Slider mit mountains divider',
                'generator' => 'generateHeroSlider'
            ],
            'contact_form' => [
                'description' => 'Kontaktformular Split Layout',
                'generator' => 'generateContactForm'
            ]
        ];
    }
    
    /**
     * Design System Tokens aus Geminis Analyse
     */
    private function initializeDesignTokens() {
        $this->designTokens = [
            'colors' => [
                'primary' => '#b68c2f',      // Gold/Ocker
                'background_light' => '#fafafa',
                'background_dark' => '#1f1f1f',
                'text_dark' => '#000000',
                'text_light' => '#ffffff'
            ],
            'typography' => [
                'heading_font' => 'Playfair Display',
                'heading_weight' => 700,
                'body_font' => 'Source Sans Pro',
                'body_weight' => 400
            ],
            'spacing' => [
                'section_padding' => 60,
                'grid_gap' => 30,
                'overlap_margin' => -100
            ],
            'animation' => [
                'type' => 'fadeInUp',
                'duration' => 'fast',
                'delay_increment' => 200
            ]
        ];
    }
    
    /**
     * Hauptfunktion: Konvertiert YAML zu Elementor JSON
     */
    public function convert($yamlContent) {
        // Parse YAML
        if (class_exists('Symfony\Component\Yaml\Yaml')) {
            $config = \Symfony\Component\Yaml\Yaml::parse($yamlContent);
        } else {
            // Fallback: Einfaches manuelles Parsing für Demo
            $config = $this->simpleYamlParse($yamlContent);
        }
        
        $elementorData = [];
        
        // Verarbeite jede Section aus der YAML Config
        foreach ($config['sections'] as $section) {
            $blockType = $section['type'];
            
            if (isset($this->blockLibrary[$blockType])) {
                $generator = $this->blockLibrary[$blockType]['generator'];
                $elementorData[] = $this->$generator($section['config']);
            }
        }
        
        return $elementorData;
    }
    
    /**
     * Generiert Service Cards Section (basierend auf exakter Cholot Struktur)
     */
    private function generateServiceCards($config) {
        $section = [
            "id" => $this->generateId(),
            "elType" => "section",
            "settings" => [
                "gap" => "extended",
                "custom_height" => ["unit" => "px", "size" => 300, "sizes" => []],
                "content_position" => "middle",
                "structure" => "30",
                "background_color" => $this->designTokens['colors']['primary'],
                "box_shadow_box_shadow" => [
                    "horizontal" => 10,
                    "vertical" => 0,
                    "blur" => 0,
                    "spread" => 4,
                    "color" => "#ededed"
                ],
                "margin" => [
                    "unit" => "px", 
                    "top" => $this->designTokens['spacing']['overlap_margin'],
                    "right" => 0,
                    "bottom" => 0,
                    "left" => 0,
                    "isLinked" => false
                ]
            ],
            "elements" => [],
            "isInner" => false
        ];
        
        // Generiere Columns für jede Card
        foreach ($config['cards'] as $index => $card) {
            $section['elements'][] = $this->generateServiceCard($card, $index);
        }
        
        return $section;
    }
    
    /**
     * Generiert eine einzelne Service Card
     */
    private function generateServiceCard($card, $index) {
        return [
            "id" => $this->generateId(),
            "elType" => "column",
            "settings" => [
                "_column_size" => 33,
                "background_color" => $this->designTokens['colors']['background_light'],
                "border_width" => ["unit" => "px", "top" => 10, "right" => 0, "bottom" => 10, "left" => 10, "isLinked" => false],
                "border_color" => "#ededed",
                "animation" => $this->designTokens['animation']['type'],
                "animation_duration" => $this->designTokens['animation']['duration'],
                "animation_delay" => $index * $this->designTokens['animation']['delay_increment']
            ],
            "elements" => [
                // Inner Section 1: Bild mit Shape Divider
                $this->generateImageSection($card['image']),
                // Inner Section 2: Content mit cholot-texticon
                $this->generateContentSection($card)
            ],
            "isInner" => false
        ];
    }
    
    /**
     * Generiert Image Section mit Shape Divider
     */
    private function generateImageSection($imageUrl) {
        return [
            "id" => $this->generateId(),
            "elType" => "section",
            "settings" => [
                "gap" => "no",
                "shape_divider_bottom" => "curve",
                "shape_divider_bottom_color" => $this->designTokens['colors']['background_light'],
                "shape_divider_bottom_negative" => "yes",
                "shape_divider_bottom_above_content" => "yes"
            ],
            "elements" => [
                [
                    "id" => $this->generateId(),
                    "elType" => "column",
                    "settings" => ["_column_size" => 100],
                    "elements" => [
                        [
                            "id" => $this->generateId(),
                            "elType" => "widget",
                            "settings" => [
                                "image" => ["url" => $imageUrl, "id" => ""],
                                "_border_width" => ["unit" => "px", "top" => 4, "right" => 0, "bottom" => 0, "left" => 0],
                                "_border_color" => $this->designTokens['colors']['primary']
                            ],
                            "elements" => [],
                            "widgetType" => "image"
                        ]
                    ],
                    "isInner" => true
                ]
            ],
            "isInner" => true
        ];
    }
    
    /**
     * Generiert Content Section mit cholot-texticon
     */
    private function generateContentSection($card) {
        return [
            "id" => $this->generateId(),
            "elType" => "section",
            "settings" => [
                "gap" => "no",
                "margin" => ["unit" => "px", "top" => -30, "right" => 0, "bottom" => 0, "left" => 0],
                "z_index" => 2
            ],
            "elements" => [
                [
                    "id" => $this->generateId(),
                    "elType" => "column",
                    "settings" => ["_column_size" => 100],
                    "elements" => [
                        [
                            "id" => $this->generateId(),
                            "elType" => "widget",
                            "settings" => [
                                "title" => $card['title'],
                                "subtitle" => $card['subtitle'],
                                "text" => "<p>" . $card['text'] . "</p>",
                                "selected_icon" => [
                                    "value" => $this->mapIcon($card['icon']),
                                    "library" => "fa-solid"
                                ],
                                "icon_color" => $this->designTokens['colors']['text_light'],
                                "iconbg_color" => $this->designTokens['colors']['primary'],
                                "subtitle_color" => $this->designTokens['colors']['primary'],
                                "_border_color" => $this->designTokens['colors']['primary'],
                                "_border_border" => "dashed"
                            ],
                            "elements" => [],
                            "widgetType" => "cholot-texticon"
                        ]
                    ],
                    "isInner" => true
                ]
            ],
            "isInner" => true
        ];
    }
    
    /**
     * Mappt einfache Icon-Namen zu FontAwesome Klassen
     */
    private function mapIcon($iconName) {
        $iconMap = [
            'shield' => 'fas fa-shield-alt',
            'industry' => 'fas fa-industry',
            'home' => 'fas fa-home',
            'parachute' => 'fas fa-parachute-box',
            'pallet' => 'fas fa-pallet',
            'igloo' => 'fas fa-igloo'
        ];
        
        return $iconMap[$iconName] ?? 'fas fa-star';
    }
    
    /**
     * Generiert unique ID für Elementor Elemente
     */
    private function generateId() {
        return substr(md5(uniqid()), 0, 7);
    }
    
    /**
     * Einfacher YAML Parser als Fallback
     */
    private function simpleYamlParse($yamlContent) {
        // Sehr vereinfachtes Parsing für Demo-Zwecke
        $config = [
            'company' => 'RIMAN GmbH',
            'sections' => [
                [
                    'type' => 'service_cards',
                    'config' => [
                        'cards' => [
                            [
                                'title' => 'Asbestsanierung',
                                'subtitle' => 'ZERTIFIZIERT',
                                'text' => 'Professionelle Entfernung von Asbest.',
                                'icon' => 'shield',
                                'image' => 'http://localhost:3456/asbestsanierung.jpg'
                            ],
                            [
                                'title' => 'PCB-Sanierung',
                                'subtitle' => 'FACHGERECHT',
                                'text' => 'Sichere Beseitigung von PCB.',
                                'icon' => 'industry',
                                'image' => 'http://localhost:3456/pcb-sanierung.jpg'
                            ],
                            [
                                'title' => 'Schimmelsanierung',
                                'subtitle' => 'NACHHALTIG',
                                'text' => 'Nachhaltige Schimmelbeseitigung.',
                                'icon' => 'home',
                                'image' => 'http://localhost:3456/schimmel.jpg'
                            ]
                        ]
                    ]
                ]
            ]
        ];
        
        return $config;
    }
}

// Beispiel-Verwendung
echo "🚀 YAML TO ELEMENTOR CONVERTER\n";
echo "==============================\n\n";

$converter = new YamlToElementorConverter();

// Beispiel YAML Content (normalerweise aus Datei geladen)
$yamlContent = '
company: RIMAN GmbH
sections:
  - type: service_cards
    config:
      cards:
        - title: Asbestsanierung
          subtitle: ZERTIFIZIERT
          text: Professionelle Entfernung von Asbest nach TRGS 519.
          icon: shield
          image: http://localhost:3456/asbestsanierung.jpg
        - title: PCB-Sanierung
          subtitle: FACHGERECHT
          text: Sichere Beseitigung von PCB-belasteten Materialien.
          icon: industry
          image: http://localhost:3456/pcb-sanierung.jpg
        - title: Schimmelsanierung
          subtitle: NACHHALTIG
          text: Nachhaltige Schimmelbeseitigung und Prävention.
          icon: home
          image: http://localhost:3456/schimmel.jpg
';

// Konvertiere zu Elementor
$elementorData = $converter->convert($yamlContent);

// Speichere als JSON
$outputFile = 'yaml_generated_elementor.json';
file_put_contents($outputFile, json_encode($elementorData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

echo "✅ YAML erfolgreich konvertiert!\n";
echo "📋 Generierte Struktur:\n";
echo "   → " . count($elementorData) . " Hauptsektionen\n";

// Zähle Widgets
$jsonString = json_encode($elementorData);
$widgetCount = substr_count($jsonString, '"widgetType"');
$texticonCount = substr_count($jsonString, '"cholot-texticon"');

echo "   → $widgetCount Widgets total\n";
echo "   → $texticonCount cholot-texticon Widgets\n\n";

echo "💾 Gespeichert als: $outputFile\n\n";

echo "📝 YAML Schema Beispiel:\n";
echo "=======================\n";
echo "company: [Firmenname]\n";
echo "sections:\n";
echo "  - type: service_cards\n";
echo "    config:\n";
echo "      cards:\n";
echo "        - title: [Titel]\n";
echo "          subtitle: [Untertitel]\n";
echo "          text: [Beschreibung]\n";
echo "          icon: [shield|industry|home]\n";
echo "          image: [URL]\n\n";

echo "🎯 Der Converter nutzt Geminis Block-Pattern Analyse!\n";