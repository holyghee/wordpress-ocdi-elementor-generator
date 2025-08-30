<?php
/**
 * Direct Elementor Import - Umgeht XML und fügt Daten direkt ein
 */

require_once 'wp-load.php';

echo "🚀 Direct Elementor Import für RIMAN GmbH\n";
echo "=========================================\n\n";

// Hero Slider Block
$hero_slider = [
    'id' => uniqid(),
    'elType' => 'section',
    'settings' => [
        'layout' => 'full_width',
        'gap' => 'no'
    ],
    'elements' => [
        [
            'id' => uniqid(),
            'elType' => 'column',
            'settings' => ['_column_size' => 100],
            'elements' => [
                [
                    'id' => uniqid(),
                    'elType' => 'widget',
                    'widgetType' => 'rdn-slider',
                    'settings' => [
                        'slider_list' => [
                            [
                                '_id' => uniqid(),
                                'title' => '25+ Jahre Erfahrung in Sanierung & Umweltschutz',
                                'subtitle' => 'Seit 1998 Ihr zuverlässiger Partner',
                                'text' => 'Professionelle Lösungen für Asbest-, PCB- und Schadstoffsanierung.',
                                'btn_text' => 'Unsere Leistungen',
                                'btn_link' => ['url' => '#services'],
                                'image' => [
                                    'url' => 'http://localhost:8081/wp-content/uploads/2025/08/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg',
                                    'id' => ''
                                ]
                            ],
                            [
                                '_id' => uniqid(),
                                'title' => 'Zertifizierte Asbestsanierung nach TRGS 519',
                                'subtitle' => 'Höchste Sicherheitsstandards',
                                'text' => 'Als zertifizierter Fachbetrieb führen wir Asbestsanierungen sicher und gesetzeskonform durch.',
                                'btn_text' => 'Mehr erfahren',
                                'btn_link' => ['url' => '#asbest'],
                                'image' => [
                                    'url' => 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg',
                                    'id' => ''
                                ]
                            ]
                        ],
                        'slides_to_show' => 1,
                        'autoplay' => 'yes',
                        'pause_on_hover' => 'yes',
                        'pause_on_interaction' => 'yes',
                        'autoplay_speed' => 5000,
                        'infinite' => 'yes',
                        'effect' => 'slide',
                        'speed' => 500,
                        'direction' => 'ltr'
                    ]
                ]
            ]
        ]
    ]
];

// Service Cards Section
$service_cards = [
    'id' => uniqid(),
    'elType' => 'section',
    'settings' => [
        'padding' => [
            'unit' => 'px',
            'top' => '80',
            'right' => '0',
            'bottom' => '80',
            'left' => '0'
        ]
    ],
    'elements' => [
        [
            'id' => uniqid(),
            'elType' => 'column',
            'settings' => ['_column_size' => 100],
            'elements' => [
                [
                    'id' => uniqid(),
                    'elType' => 'widget',
                    'widgetType' => 'heading',
                    'settings' => [
                        'title' => 'Unsere Kernkompetenzen',
                        'header_size' => 'h2',
                        'align' => 'center'
                    ]
                ],
                [
                    'id' => uniqid(),
                    'elType' => 'widget',
                    'widgetType' => 'heading',
                    'settings' => [
                        'title' => 'Umfassende Sanierungslösungen',
                        'header_size' => 'h4',
                        'align' => 'center'
                    ]
                ]
            ]
        ]
    ]
];

// Service Cards Row
$services_row = [
    'id' => uniqid(),
    'elType' => 'section',
    'settings' => [],
    'elements' => []
];

$services = [
    ['title' => 'Asbestsanierung', 'icon' => 'fa fa-shield', 'text' => 'Sichere und fachgerechte Entfernung von Asbest nach TRGS 519'],
    ['title' => 'PCB-Sanierung', 'icon' => 'fa fa-flask', 'text' => 'Professionelle Beseitigung von PCB-belasteten Materialien'],
    ['title' => 'Schimmelsanierung', 'icon' => 'fa fa-bacteria', 'text' => 'Nachhaltige Schimmelbeseitigung und Prävention'],
    ['title' => 'Brandschaden', 'icon' => 'fa fa-fire', 'text' => 'Schnelle Hilfe bei Brand- und Wasserschäden']
];

foreach ($services as $service) {
    $services_row['elements'][] = [
        'id' => uniqid(),
        'elType' => 'column',
        'settings' => ['_column_size' => 25],
        'elements' => [
            [
                'id' => uniqid(),
                'elType' => 'widget',
                'widgetType' => 'cholot-texticon',
                'settings' => [
                    'title' => $service['title'],
                    'text' => $service['text'],
                    'selected_icon' => ['value' => $service['icon']],
                    'icon_color' => '#333399',
                    'title_color' => '#333333',
                    'description_color' => '#666666'
                ]
            ]
        ]
    ];
}

// Kombiniere alle Sections
$elementor_data = [
    $hero_slider,
    $service_cards,
    $services_row
];

// Erstelle oder update Homepage
$homepage_id = 2000;
$page = get_post($homepage_id);

if (!$page) {
    // Erstelle neue Seite
    $homepage_id = wp_insert_post([
        'post_title' => 'RIMAN GmbH - Startseite',
        'post_content' => '',
        'post_status' => 'publish',
        'post_type' => 'page',
        'post_name' => 'riman-startseite'
    ]);
    echo "✅ Neue Seite erstellt (ID: $homepage_id)\n";
} else {
    echo "✅ Verwende existierende Seite (ID: $homepage_id)\n";
}

// Speichere Elementor Data
$json_data = wp_json_encode($elementor_data);
update_post_meta($homepage_id, '_elementor_data', $json_data);
update_post_meta($homepage_id, '_elementor_edit_mode', 'builder');
update_post_meta($homepage_id, '_elementor_version', '3.17.0');
update_post_meta($homepage_id, '_wp_page_template', 'elementor_canvas');

// Elementor CSS regenerieren
if (class_exists('\Elementor\Plugin')) {
    $css_file = \Elementor\Core\Files\CSS\Post::create($homepage_id);
    $css_file->update();
    echo "✅ Elementor CSS regeneriert\n";
    
    // Clear Cache
    \Elementor\Plugin::instance()->files_manager->clear_cache();
    echo "✅ Cache geleert\n";
}

echo "\n✅ Import abgeschlossen!\n";
echo "👉 Öffne: http://localhost:8081/?page_id=$homepage_id\n";
?>