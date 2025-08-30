<?php
/**
 * Final Working Import - Direkte Elementor-Strukturen ohne JSON-Probleme
 */

require_once 'wp-load.php';

echo "🚀 Final Working Import für RIMAN GmbH\n";
echo "======================================\n\n";

// Erstelle neue Seite
$page_id = wp_insert_post([
    'post_title' => 'RIMAN GmbH - Finale Version',
    'post_content' => '',
    'post_status' => 'publish',
    'post_type' => 'page',
    'post_name' => 'riman-final-' . time()
]);

echo "✅ Neue Seite erstellt: ID $page_id\n\n";

// Erstelle Elementor-Struktur direkt als PHP-Array
$elementor_data = [
    // HERO SLIDER SECTION
    [
        'id' => uniqid(),
        'elType' => 'section',
        'settings' => [
            'layout' => 'full_width',
            'gap' => 'no',
            'background_background' => 'classic',
            'background_color' => 'rgba(0,0,0,0.3)'
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
                        'widgetType' => 'slides',
                        'settings' => [
                            'slides' => [
                                [
                                    '_id' => uniqid(),
                                    'heading' => '25+ Jahre Erfahrung',
                                    'description' => 'Professionelle Sanierung seit 1998',
                                    'button_text' => 'Mehr erfahren',
                                    'button_link' => ['url' => '#services'],
                                    'background_color' => '#333399',
                                    'background_image' => [
                                        'url' => 'http://localhost:8081/wp-content/uploads/2025/08/systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg'
                                    ]
                                ],
                                [
                                    '_id' => uniqid(),
                                    'heading' => 'Zertifizierte Asbestsanierung',
                                    'description' => 'Nach TRGS 519 - Höchste Sicherheitsstandards',
                                    'button_text' => 'Kontakt',
                                    'button_link' => ['url' => '#contact'],
                                    'background_color' => '#FF0000',
                                    'background_image' => [
                                        'url' => 'http://localhost:8081/wp-content/uploads/2025/08/asbestsanierung-schutzausruestung-fachpersonal.jpg'
                                    ]
                                ]
                            ],
                            'transition' => 'slide',
                            'transition_speed' => 500,
                            'autoplay' => 'yes',
                            'autoplay_speed' => 5000,
                            'pause_on_hover' => 'yes',
                            'pause_on_interaction' => 'yes',
                            'infinite' => 'yes'
                        ]
                    ]
                ]
            ]
        ]
    ],
    
    // TITLE SECTION
    [
        'id' => uniqid(),
        'elType' => 'section',
        'settings' => [
            'padding' => [
                'unit' => 'px',
                'top' => '80',
                'right' => '0',
                'bottom' => '40',
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
                            'align' => 'center',
                            'title_color' => '#333399'
                        ]
                    ],
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'text-editor',
                        'settings' => [
                            'editor' => '<p style="text-align: center;">Umfassende Sanierungslösungen aus einer Hand</p>'
                        ]
                    ]
                ]
            ]
        ]
    ],
    
    // SERVICE CARDS SECTION
    [
        'id' => uniqid(),
        'elType' => 'section',
        'settings' => [
            'structure' => '25',
            'padding' => [
                'unit' => 'px',
                'top' => '40',
                'right' => '0',
                'bottom' => '80',
                'left' => '0'
            ]
        ],
        'elements' => [
            // Service 1: Asbestsanierung
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 25],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'icon-box',
                        'settings' => [
                            'selected_icon' => [
                                'value' => 'fas fa-shield-alt',
                                'library' => 'fa-solid'
                            ],
                            'title_text' => 'Asbestsanierung',
                            'description_text' => 'Sichere und fachgerechte Entfernung von Asbest nach TRGS 519',
                            'position' => 'top',
                            'title_size' => 'h4',
                            'primary_color' => '#333399',
                            'icon_size' => ['size' => 60, 'unit' => 'px']
                        ]
                    ]
                ]
            ],
            // Service 2: PCB-Sanierung
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 25],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'icon-box',
                        'settings' => [
                            'selected_icon' => [
                                'value' => 'fas fa-flask',
                                'library' => 'fa-solid'
                            ],
                            'title_text' => 'PCB-Sanierung',
                            'description_text' => 'Professionelle Beseitigung von PCB-belasteten Materialien',
                            'position' => 'top',
                            'title_size' => 'h4',
                            'primary_color' => '#333399',
                            'icon_size' => ['size' => 60, 'unit' => 'px']
                        ]
                    ]
                ]
            ],
            // Service 3: Schimmelsanierung
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 25],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'icon-box',
                        'settings' => [
                            'selected_icon' => [
                                'value' => 'fas fa-bacteria',
                                'library' => 'fa-solid'
                            ],
                            'title_text' => 'Schimmelsanierung',
                            'description_text' => 'Nachhaltige Schimmelbeseitigung und Prävention',
                            'position' => 'top',
                            'title_size' => 'h4',
                            'primary_color' => '#333399',
                            'icon_size' => ['size' => 60, 'unit' => 'px']
                        ]
                    ]
                ]
            ],
            // Service 4: Brandschaden
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 25],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'icon-box',
                        'settings' => [
                            'selected_icon' => [
                                'value' => 'fas fa-fire',
                                'library' => 'fa-solid'
                            ],
                            'title_text' => 'Brandschaden',
                            'description_text' => 'Schnelle Hilfe bei Brand- und Wasserschäden - 24/7 Notdienst',
                            'position' => 'top',
                            'title_size' => 'h4',
                            'primary_color' => '#FF0000',
                            'icon_size' => ['size' => 60, 'unit' => 'px']
                        ]
                    ]
                ]
            ]
        ]
    ],
    
    // WARUM RIMAN SECTION
    [
        'id' => uniqid(),
        'elType' => 'section',
        'settings' => [
            'background_background' => 'classic',
            'background_color' => '#f7f7f7',
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
                            'title' => 'Warum RIMAN GmbH?',
                            'header_size' => 'h2',
                            'align' => 'center',
                            'title_color' => '#333399'
                        ]
                    ],
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'text-editor',
                        'settings' => [
                            'editor' => '<p style="text-align: center; font-size: 18px;">Seit 1998 Ihr zuverlässiger Partner für sichere Sanierung</p>'
                        ]
                    ]
                ]
            ]
        ]
    ],
    
    // VORTEILE SECTION
    [
        'id' => uniqid(),
        'elType' => 'section',
        'settings' => [
            'structure' => '33',
            'padding' => [
                'unit' => 'px',
                'top' => '40',
                'right' => '0',
                'bottom' => '80',
                'left' => '0'
            ]
        ],
        'elements' => [
            // Vorteil 1
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 33],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'counter',
                        'settings' => [
                            'starting_number' => 0,
                            'ending_number' => 25,
                            'suffix' => '+ Jahre',
                            'title' => 'Erfahrung',
                            'number_color' => '#333399',
                            'title_color' => '#333333'
                        ]
                    ]
                ]
            ],
            // Vorteil 2
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 33],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'counter',
                        'settings' => [
                            'starting_number' => 0,
                            'ending_number' => 2000,
                            'suffix' => '+',
                            'title' => 'Projekte',
                            'number_color' => '#333399',
                            'title_color' => '#333333'
                        ]
                    ]
                ]
            ],
            // Vorteil 3
            [
                'id' => uniqid(),
                'elType' => 'column',
                'settings' => ['_column_size' => 33],
                'elements' => [
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'counter',
                        'settings' => [
                            'starting_number' => 0,
                            'ending_number' => 100,
                            'suffix' => '%',
                            'title' => 'Zufriedenheit',
                            'number_color' => '#FF0000',
                            'title_color' => '#333333'
                        ]
                    ]
                ]
            ]
        ]
    ],
    
    // CONTACT CTA SECTION
    [
        'id' => uniqid(),
        'elType' => 'section',
        'settings' => [
            'background_background' => 'classic',
            'background_color' => '#333399',
            'padding' => [
                'unit' => 'px',
                'top' => '60',
                'right' => '0',
                'bottom' => '60',
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
                            'title' => 'Kostenlose Erstberatung',
                            'header_size' => 'h2',
                            'align' => 'center',
                            'title_color' => '#ffffff'
                        ]
                    ],
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'text-editor',
                        'settings' => [
                            'editor' => '<p style="text-align: center; color: #ffffff;">Wir beraten Sie gerne unverbindlich zu Ihrem Sanierungsprojekt</p>'
                        ]
                    ],
                    [
                        'id' => uniqid(),
                        'elType' => 'widget',
                        'widgetType' => 'button',
                        'settings' => [
                            'text' => 'Jetzt Kontakt aufnehmen',
                            'link' => ['url' => '/kontakt'],
                            'align' => 'center',
                            'button_type' => 'success',
                            'size' => 'lg',
                            'button_text_color' => '#333399',
                            'background_color' => '#ffffff'
                        ]
                    ]
                ]
            ]
        ]
    ]
];

// Konvertiere zu JSON und speichere
$json_data = wp_json_encode($elementor_data);

// Speichere Meta-Daten
update_post_meta($page_id, '_elementor_data', $json_data);
update_post_meta($page_id, '_elementor_edit_mode', 'builder');
update_post_meta($page_id, '_elementor_version', '3.17.0');
update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');

echo "✅ Elementor-Daten gespeichert\n";

// Generiere CSS
if (class_exists('\Elementor\Plugin')) {
    \Elementor\Plugin::instance()->files_manager->clear_cache();
    $css_file = \Elementor\Core\Files\CSS\Post::create($page_id);
    $css_file->update();
    echo "✅ CSS generiert\n";
}

// Verifizierung
$saved = get_post_meta($page_id, '_elementor_data', true);
$test = json_decode($saved, true);
if ($test && count($test) > 0) {
    echo "\n✅ ERFOLG! " . count($test) . " Sections korrekt gespeichert\n";
} else {
    echo "\n❌ Fehler beim Speichern\n";
}

echo "\n🎉 Import abgeschlossen!\n";
echo "👉 Öffne: http://localhost:8081/?page_id=$page_id\n";
?>