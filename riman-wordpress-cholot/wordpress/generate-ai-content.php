<?php
/**
 * AI-Powered WordPress Content Generator for RIMAN GmbH
 * Generates a complete website prototype with relevant content
 */

require_once 'wp-load.php';

class AIContentGenerator {
    private $company = 'RIMAN GmbH';
    private $industry = 'Schadstoffsanierung, Rückbaumanagement, Altlastensanierung, Mediation';
    private $services = [
        'schadstoff' => [
            'title' => 'Schadstoff-Management',
            'short' => 'Professionelle Schadstoffanalyse und -sanierung',
            'keywords' => ['Asbest', 'PCB', 'PAK', 'Schwermetalle', 'Schadstoffkataster', 'Probenahme']
        ],
        'rueckbau' => [
            'title' => 'Rückbaumanagement',
            'short' => 'Nachhaltige Rückbau- und Recyclingkonzepte',
            'keywords' => ['Abbruch', 'Entkernung', 'Recycling', 'Entsorgung', 'Rückbauplanung', 'Verwertung']
        ],
        'altlasten' => [
            'title' => 'Altlastensanierung',
            'short' => 'Bodensanierung und Grundwasserschutz',
            'keywords' => ['Bodensanierung', 'Grundwasser', 'Dekontamination', 'Monitoring', 'Sanierungsplanung']
        ],
        'mediation' => [
            'title' => 'Mediation',
            'short' => 'Konfliktlösung im Bauwesen',
            'keywords' => ['Konfliktmanagement', 'Streitschlichtung', 'Moderation', 'Baumediation', 'Verhandlung']
        ]
    ];

    public function generateContent() {
        $xml = $this->createXMLHeader();
        
        // Generate Pages
        $pages = [
            // Homepage
            [
                'title' => 'Startseite',
                'content' => $this->generateHomepageContent(),
                'template' => 'elementor_header_footer',
                'menu_order' => 0
            ],
            // About
            [
                'title' => 'Über uns',
                'content' => $this->generateAboutContent(),
                'template' => 'elementor_header_footer',
                'menu_order' => 1
            ],
            // Services
            [
                'title' => 'Leistungen',
                'content' => $this->generateServicesOverview(),
                'template' => 'elementor_header_footer',
                'menu_order' => 2
            ],
            // Individual service pages
            [
                'title' => 'Schadstoff-Management',
                'content' => $this->generateServiceContent('schadstoff'),
                'template' => 'elementor_header_footer',
                'parent' => 'Leistungen',
                'menu_order' => 3
            ],
            [
                'title' => 'Rückbaumanagement',
                'content' => $this->generateServiceContent('rueckbau'),
                'template' => 'elementor_header_footer',
                'parent' => 'Leistungen',
                'menu_order' => 4
            ],
            [
                'title' => 'Altlastensanierung',
                'content' => $this->generateServiceContent('altlasten'),
                'template' => 'elementor_header_footer',
                'parent' => 'Leistungen',
                'menu_order' => 5
            ],
            [
                'title' => 'Mediation',
                'content' => $this->generateServiceContent('mediation'),
                'template' => 'elementor_header_footer',
                'parent' => 'Leistungen',
                'menu_order' => 6
            ],
            // Projects/References
            [
                'title' => 'Referenzen',
                'content' => $this->generateProjectsContent(),
                'template' => 'elementor_header_footer',
                'menu_order' => 7
            ],
            // Team
            [
                'title' => 'Team',
                'content' => $this->generateTeamContent(),
                'template' => 'elementor_header_footer',
                'menu_order' => 8
            ],
            // Contact
            [
                'title' => 'Kontakt',
                'content' => $this->generateContactContent(),
                'template' => 'elementor_header_footer',
                'menu_order' => 9
            ],
            // Legal pages
            [
                'title' => 'Impressum',
                'content' => $this->generateImpressum(),
                'template' => 'default',
                'menu_order' => 10
            ],
            [
                'title' => 'Datenschutz',
                'content' => $this->generateDatenschutz(),
                'template' => 'default',
                'menu_order' => 11
            ]
        ];

        // Generate Blog Posts
        $posts = [
            [
                'title' => 'Neue EU-Richtlinien für Schadstoffsanierung 2024',
                'content' => $this->generateBlogPost('eu-richtlinien'),
                'category' => 'Rechtliches'
            ],
            [
                'title' => 'Nachhaltige Rückbaukonzepte: Kreislaufwirtschaft im Fokus',
                'content' => $this->generateBlogPost('nachhaltigkeit'),
                'category' => 'Nachhaltigkeit'
            ],
            [
                'title' => 'Asbestsanierung: Sicherheit hat oberste Priorität',
                'content' => $this->generateBlogPost('asbest'),
                'category' => 'Schadstoffsanierung'
            ],
            [
                'title' => 'BIM im Rückbaumanagement: Digitale Revolution',
                'content' => $this->generateBlogPost('bim'),
                'category' => 'Digitalisierung'
            ],
            [
                'title' => 'Erfolgreiche Mediation im Großprojekt München',
                'content' => $this->generateBlogPost('mediation-erfolg'),
                'category' => 'Projekte'
            ]
        ];

        $xml .= $this->generatePagesXML($pages);
        $xml .= $this->generatePostsXML($posts);
        $xml .= $this->createXMLFooter();
        
        return $xml;
    }

    private function generateHomepageContent() {
        return '<!-- wp:cholot-plugin/rdn-slider -->
<div class="slider home-slider">
    <div class="slider-box">
        <h1>RIMAN GmbH - Ihr Partner für nachhaltiges Bauen</h1>
        <p>Schadstoffsanierung | Rückbaumanagement | Altlastensanierung | Mediation</p>
    </div>
</div>
<!-- /wp:cholot-plugin/rdn-slider -->

<!-- wp:heading {"level":2} -->
<h2>Kompetenz in Sanierung und Rückbau</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Die RIMAN GmbH ist Ihr zuverlässiger Partner für alle Aspekte der Schadstoffsanierung, des Rückbaumanagements und der Altlastensanierung. Mit über 20 Jahren Erfahrung bieten wir ganzheitliche Lösungen für komplexe Bauvorhaben.</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>🏗️ Rückbaumanagement</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Nachhaltige Konzepte für Rückbau und Recycling. Wir maximieren die Wiederverwertung und minimieren Entsorgungskosten.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>⚠️ Schadstoffsanierung</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Professionelle Analyse und Sanierung von Schadstoffen wie Asbest, PCB und PAK nach neuesten Standards.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>🌍 Altlastensanierung</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Bodensanierung und Grundwasserschutz mit modernsten Verfahren für eine saubere Umwelt.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->';
    }

    private function generateAboutContent() {
        return '<!-- wp:heading -->
<h1>Über RIMAN GmbH</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Seit über zwei Jahrzehnten steht RIMAN GmbH für Kompetenz, Zuverlässigkeit und Innovation im Bereich der Schadstoffsanierung und des Rückbaumanagements.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Unsere Geschichte</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Gegründet im Jahr 2003, hat sich RIMAN GmbH von einem regionalen Spezialisten zu einem bundesweit agierenden Unternehmen entwickelt. Unser Fokus liegt auf der nachhaltigen Sanierung von Gebäuden und Grundstücken unter Berücksichtigung ökologischer und ökonomischer Aspekte.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Unsere Mission</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Nachhaltige Lösungen für komplexe Sanierungsaufgaben</li>
<li>Schutz von Mensch und Umwelt durch fachgerechte Schadstoffbeseitigung</li>
<li>Förderung der Kreislaufwirtschaft durch innovative Recyclingkonzepte</li>
<li>Transparente Kommunikation und partnerschaftliche Zusammenarbeit</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2>Zertifizierungen & Qualifikationen</h2>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<h3>ISO 9001:2015</h3>
<p>Qualitätsmanagement</p>
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<h3>ISO 14001:2015</h3>
<p>Umweltmanagement</p>
</div>
<!-- /wp:column -->
<!-- wp:column -->
<div class="wp-block-column">
<h3>SCC**</h3>
<p>Arbeitssicherheit</p>
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->';
    }

    private function generateServiceContent($serviceKey) {
        $service = $this->services[$serviceKey];
        $keywords = implode(', ', $service['keywords']);
        
        $content = "<!-- wp:heading -->
<h1>{$service['title']}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>{$service['short']}</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading {\"level\":2} -->
<h2>Unsere Leistungen im {$service['title']}</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>";

        foreach ($service['keywords'] as $keyword) {
            $content .= "\n<li>$keyword - Professionelle Durchführung und Dokumentation</li>";
        }

        $content .= "</ul>
<!-- /wp:list -->

<!-- wp:heading {\"level\":2} -->
<h2>Warum RIMAN GmbH?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Mit unserer langjährigen Erfahrung im Bereich {$service['title']} bieten wir Ihnen:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>✓ Zertifizierte Fachkräfte mit umfassender Expertise</li>
<li>✓ Modernste Technik und Verfahren</li>
<li>✓ Vollständige Dokumentation aller Arbeitsschritte</li>
<li>✓ Einhaltung aller gesetzlichen Vorgaben</li>
<li>✓ Transparente Kostenkalkulation</li>
</ul>
<!-- /wp:list -->";

        return $content;
    }

    private function generateServicesOverview() {
        return '<!-- wp:heading -->
<h1>Unsere Leistungen</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>RIMAN GmbH bietet Ihnen ein umfassendes Spektrum an Dienstleistungen rund um Sanierung, Rückbau und Umweltschutz.</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Schadstoff-Management</h3>
<!-- /wp:heading -->
<!-- wp:list -->
<ul>
<li>Asbestsanierung</li>
<li>PCB-Sanierung</li>
<li>PAK-Sanierung</li>
<li>Schadstoffkataster</li>
</ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Rückbaumanagement</h3>
<!-- /wp:heading -->
<!-- wp:list -->
<ul>
<li>Rückbauplanung</li>
<li>Entkernung</li>
<li>Abbrucharbeiten</li>
<li>Recyclingkonzepte</li>
</ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Altlastensanierung</h3>
<!-- /wp:heading -->
<!-- wp:list -->
<ul>
<li>Bodensanierung</li>
<li>Grundwassersanierung</li>
<li>Dekontamination</li>
<li>Monitoring</li>
</ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Mediation</h3>
<!-- /wp:heading -->
<!-- wp:list -->
<ul>
<li>Baumediation</li>
<li>Konfliktmanagement</li>
<li>Moderation</li>
<li>Streitschlichtung</li>
</ul>
<!-- /wp:list -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->';
    }

    private function generateProjectsContent() {
        return '<!-- wp:heading -->
<h1>Unsere Referenzen</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Erfolgreiche Projekte sprechen für sich. Hier eine Auswahl unserer abgeschlossenen Sanierungsprojekte.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Industriesanierung München</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Projekt:</strong> Komplettsanierung einer ehemaligen Industrieanlage<br>
<strong>Leistungen:</strong> Asbestentfernung, PCB-Sanierung, Rückbau, Bodensanierung<br>
<strong>Zeitraum:</strong> 2023-2024<br>
<strong>Besonderheit:</strong> Sanierung bei laufendem Betrieb der Nachbargebäude</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":2} -->
<h2>Wohnquartier Berlin</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Projekt:</strong> Schadstoffsanierung vor Modernisierung<br>
<strong>Leistungen:</strong> Schadstoffkataster, Asbestsanierung, Entsorgungsmanagement<br>
<strong>Zeitraum:</strong> 2023<br>
<strong>Besonderheit:</strong> Bewohner konnten während der Sanierung in den Wohnungen bleiben</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:heading {"level":2} -->
<h2>Krankenhausumbau Hamburg</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Projekt:</strong> Entkernung und Schadstoffsanierung<br>
<strong>Leistungen:</strong> Komplettentkernung, Schadstoffentsorgung, Mediation<br>
<strong>Zeitraum:</strong> 2022-2023<br>
<strong>Besonderheit:</strong> Einhaltung höchster Hygienestandards</p>
<!-- /wp:paragraph -->';
    }

    private function generateTeamContent() {
        return '<!-- wp:heading -->
<h1>Unser Team</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Kompetente Fachkräfte sind das Fundament unseres Erfolgs. Lernen Sie unser Team kennen.</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Dr. Michael Riman</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Geschäftsführer</strong><br>
Diplom-Ingenieur mit über 25 Jahren Erfahrung in der Schadstoffsanierung</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Sabine Weber</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Leiterin Projektmanagement</strong><br>
Master in Umwelttechnik, zertifizierte Projektmanagerin</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:heading {"level":3} -->
<h3>Thomas Müller</h3>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Leiter Technik</strong><br>
Sachverständiger für Schadstoffe in Gebäuden</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->

<!-- wp:heading {"level":2} -->
<h2>Unser Versprechen</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Unser Team aus über 50 Spezialisten steht für:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li>Kontinuierliche Weiterbildung und Zertifizierungen</li>
<li>Höchste Standards in Arbeitssicherheit und Umweltschutz</li>
<li>Innovative Lösungsansätze für komplexe Aufgaben</li>
<li>Partnerschaftliche Zusammenarbeit auf Augenhöhe</li>
</ul>
<!-- /wp:list -->';
    }

    private function generateContactContent() {
        return '<!-- wp:heading -->
<h1>Kontakt</h1>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column {"width":"60%"} -->
<div class="wp-block-column" style="flex-basis:60%">
<!-- wp:heading {"level":2} -->
<h2>Kontaktieren Sie uns</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Wir freuen uns auf Ihre Anfrage und beraten Sie gerne zu Ihrem Projekt.</p>
<!-- /wp:paragraph -->

<!-- wp:contact-form-7/contact-form-selector -->
<div class="wp-block-contact-form-7-contact-form-selector">
[contact-form-7 id="1" title="Kontaktformular"]
</div>
<!-- /wp:contact-form-7/contact-form-selector -->
</div>
<!-- /wp:column -->

<!-- wp:column {"width":"40%"} -->
<div class="wp-block-column" style="flex-basis:40%">
<!-- wp:heading {"level":2} -->
<h2>RIMAN GmbH</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Adresse:</strong><br>
Musterstraße 123<br>
80333 München<br>
Deutschland</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Telefon:</strong> +49 89 123456-0<br>
<strong>Fax:</strong> +49 89 123456-99<br>
<strong>E-Mail:</strong> info@riman-gmbh.de</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Öffnungszeiten</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Montag - Freitag: 8:00 - 17:00 Uhr<br>
24h-Notfallhotline: +49 89 123456-111</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->';
    }

    private function generateBlogPost($type) {
        $posts = [
            'eu-richtlinien' => "Die Europäische Union hat neue Richtlinien für die Schadstoffsanierung verabschiedet, die ab 2024 in Kraft treten. Diese Änderungen betreffen insbesondere die Grenzwerte für Asbest und PCB sowie die Dokumentationspflichten bei Sanierungsprojekten.\n\n<strong>Wichtige Änderungen im Überblick:</strong>\n- Verschärfte Grenzwerte für Asbestfasern\n- Erweiterte Meldepflichten\n- Neue Anforderungen an die Qualifikation von Sanierungsfachkräften\n\nRIMAN GmbH ist bereits heute auf die neuen Standards vorbereitet und unterstützt Sie bei der gesetzeskonformen Umsetzung Ihrer Projekte.",
            
            'nachhaltigkeit' => "Nachhaltigkeit im Rückbau bedeutet mehr als nur Recycling. Es geht um ganzheitliche Konzepte, die von der Planung bis zur Verwertung alle Aspekte der Kreislaufwirtschaft berücksichtigen.\n\n<strong>Unsere Ansätze:</strong>\n- Selective Demolition für maximale Materialrückgewinnung\n- BIM-basierte Rückbauplanung\n- Partnerschaften mit zertifizierten Recyclingunternehmen\n- CO2-Bilanzierung aller Rückbauprojekte\n\nDurch innovative Verfahren erreichen wir Recyclingquoten von über 95% und tragen aktiv zum Klimaschutz bei.",
            
            'asbest' => "Asbest gehört zu den gefährlichsten Schadstoffen in Gebäuden. Die fachgerechte Sanierung erfordert höchste Sorgfalt und Expertise.\n\n<strong>Unser Vorgehen:</strong>\n- Umfassende Bestandsaufnahme und Gefährdungsbeurteilung\n- Erstellung eines detaillierten Sanierungskonzepts\n- Einrichtung von Schwarzbereichen mit Unterdruckhaltung\n- Kontinuierliche Luftmessungen während der Arbeiten\n- Ordnungsgemäße Entsorgung und Dokumentation\n\nMit modernster Technik und geschultem Personal gewährleisten wir maximale Sicherheit für alle Beteiligten.",
            
            'bim' => "Building Information Modeling (BIM) revolutioniert auch das Rückbaumanagement. Digitale Zwillinge ermöglichen präzise Planung und Dokumentation.\n\n<strong>Vorteile von BIM im Rückbau:</strong>\n- Exakte Massenermittlung für Entsorgung und Recycling\n- Visualisierung von Rückbauphasen\n- Kollisionsprüfung bei Teilrückbauten\n- Digitale Schadstoffkartierung\n- Nahtlose Dokumentation für Behörden\n\nRIMAN GmbH setzt BIM erfolgreich in Großprojekten ein und optimiert damit Zeit- und Kostenpläne.",
            
            'mediation-erfolg' => "Bei einem Großbauprojekt in München konnte durch professionelle Mediation ein langwieriger Rechtsstreit vermieden werden.\n\n<strong>Die Ausgangssituation:</strong>\n- Konflikt zwischen Bauherr und Nachbarn wegen Lärmbelästigung\n- Drohende Bauverzögerung durch Klagen\n- Verhärtete Fronten nach gescheiterten Gesprächen\n\n<strong>Unser Mediationsansatz:</strong>\n- Strukturierte Gesprächsführung mit allen Parteien\n- Entwicklung eines Lärmschutzkonzepts\n- Vereinbarung von Kompensationsmaßnahmen\n- Win-Win-Lösung für alle Beteiligten\n\nDas Projekt konnte termingerecht fortgesetzt werden, und die Nachbarschaftsbeziehungen wurden nachhaltig verbessert."
        ];
        
        return "<!-- wp:paragraph -->\n<p>" . str_replace("\n\n", "</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:paragraph -->\n<p>", $posts[$type]) . "</p>\n<!-- /wp:paragraph -->";
    }

    private function generateImpressum() {
        return '<!-- wp:heading -->
<h1>Impressum</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>RIMAN GmbH</strong><br>
Musterstraße 123<br>
80333 München<br>
Deutschland</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Vertreten durch:</strong><br>
Dr. Michael Riman (Geschäftsführer)</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Kontakt:</strong><br>
Telefon: +49 89 123456-0<br>
Fax: +49 89 123456-99<br>
E-Mail: info@riman-gmbh.de</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Registereintrag:</strong><br>
Handelsregister: HRB 123456<br>
Registergericht: Amtsgericht München</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Umsatzsteuer-ID:</strong><br>
Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: DE123456789</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Berufsbezeichnung und berufsrechtliche Regelungen:</strong><br>
Berufsbezeichnung: Ingenieur<br>
Zuständige Kammer: Bayerische Ingenieurekammer-Bau<br>
Verliehen in: Deutschland</p>
<!-- /wp:paragraph -->';
    }

    private function generateDatenschutz() {
        return '<!-- wp:heading -->
<h1>Datenschutzerklärung</h1>
<!-- /wp:heading -->

<!-- wp:heading {"level":2} -->
<h2>1. Datenschutz auf einen Blick</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>2. Allgemeine Hinweise und Pflichtinformationen</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Verantwortliche Stelle:</strong><br>
RIMAN GmbH<br>
Musterstraße 123<br>
80333 München<br>
E-Mail: datenschutz@riman-gmbh.de</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>3. Datenerfassung auf dieser Website</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Die Kontaktdaten können Sie dem Impressum dieser Website entnehmen.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Cookies</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Diese Website verwendet Cookies. Cookies sind kleine Textdateien, die auf Ihrem Rechner gespeichert werden. Sie richten keinen Schaden an.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Server-Log-Dateien</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Der Provider der Seiten erhebt und speichert automatisch Informationen in so genannten Server-Log-Dateien, die Ihr Browser automatisch an uns übermittelt.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>4. Ihre Rechte</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Auskunft über Ihre gespeicherten Daten</li>
<li>Berichtigung unrichtiger Daten</li>
<li>Löschung Ihrer Daten</li>
<li>Einschränkung der Datenverarbeitung</li>
<li>Widerspruch gegen die Datenverarbeitung</li>
<li>Datenübertragbarkeit</li>
</ul>
<!-- /wp:list -->';
    }

    private function createXMLHeader() {
        $date = date('Y-m-d H:i');
        return '<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>RIMAN GmbH Website</title>
    <link>http://localhost:8080</link>
    <description>AI-Generated Content for RIMAN GmbH</description>
    <pubDate>' . $date . '</pubDate>
    <language>de-DE</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>http://localhost:8080</wp:base_site_url>
    <wp:base_blog_url>http://localhost:8080</wp:base_blog_url>
    
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[admin]]></wp:author_login>
        <wp:author_email><![CDATA[admin@riman-gmbh.de]]></wp:author_email>
        <wp:author_display_name><![CDATA[RIMAN Admin]]></wp:author_display_name>
    </wp:author>

    <wp:category>
        <wp:term_id>1</wp:term_id>
        <wp:category_nicename><![CDATA[rechtliches]]></wp:category_nicename>
        <wp:category_parent></wp:category_parent>
        <wp:cat_name><![CDATA[Rechtliches]]></wp:cat_name>
    </wp:category>
    <wp:category>
        <wp:term_id>2</wp:term_id>
        <wp:category_nicename><![CDATA[nachhaltigkeit]]></wp:category_nicename>
        <wp:category_parent></wp:category_parent>
        <wp:cat_name><![CDATA[Nachhaltigkeit]]></wp:cat_name>
    </wp:category>
    <wp:category>
        <wp:term_id>3</wp:term_id>
        <wp:category_nicename><![CDATA[schadstoffsanierung]]></wp:category_nicename>
        <wp:category_parent></wp:category_parent>
        <wp:cat_name><![CDATA[Schadstoffsanierung]]></wp:cat_name>
    </wp:category>
    <wp:category>
        <wp:term_id>4</wp:term_id>
        <wp:category_nicename><![CDATA[digitalisierung]]></wp:category_nicename>
        <wp:category_parent></wp:category_parent>
        <wp:cat_name><![CDATA[Digitalisierung]]></wp:cat_name>
    </wp:category>
    <wp:category>
        <wp:term_id>5</wp:term_id>
        <wp:category_nicename><![CDATA[projekte]]></wp:category_nicename>
        <wp:category_parent></wp:category_parent>
        <wp:cat_name><![CDATA[Projekte]]></wp:cat_name>
    </wp:category>';
    }

    private function generatePagesXML($pages) {
        $xml = '';
        $id = 100;
        
        foreach ($pages as $page) {
            $slug = strtolower(str_replace([' ', 'ä', 'ö', 'ü', 'ß'], ['_', 'ae', 'oe', 'ue', 'ss'], $page['title']));
            $xml .= '
    <item>
        <title>' . $page['title'] . '</title>
        <link>http://localhost:8080/' . $slug . '/</link>
        <pubDate>' . date('D, d M Y H:i:s +0000') . '</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">http://localhost:8080/?page_id=' . $id . '</guid>
        <content:encoded><![CDATA[' . $page['content'] . ']]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>' . $id . '</wp:post_id>
        <wp:post_date><![CDATA[' . date('Y-m-d H:i:s') . ']]></wp:post_date>
        <wp:post_date_gmt><![CDATA[' . date('Y-m-d H:i:s') . ']]></wp:post_date_gmt>
        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[' . $slug . ']]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>' . $page['menu_order'] . '</wp:menu_order>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>';
        
            if (isset($page['template']) && $page['template'] !== 'default') {
                $xml .= '
        <wp:postmeta>
            <wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
            <wp:meta_value><![CDATA[' . $page['template'] . ']]></wp:meta_value>
        </wp:postmeta>';
            }
            
            $xml .= '
    </item>';
            $id++;
        }
        
        return $xml;
    }

    private function generatePostsXML($posts) {
        $xml = '';
        $id = 200;
        
        foreach ($posts as $post) {
            $slug = strtolower(str_replace([' ', 'ä', 'ö', 'ü', 'ß', ':'], ['_', 'ae', 'oe', 'ue', 'ss', ''], $post['title']));
            $category = strtolower($post['category']);
            
            $xml .= '
    <item>
        <title>' . $post['title'] . '</title>
        <link>http://localhost:8080/' . $slug . '/</link>
        <pubDate>' . date('D, d M Y H:i:s +0000', strtotime('-' . rand(1, 30) . ' days')) . '</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">http://localhost:8080/?p=' . $id . '</guid>
        <content:encoded><![CDATA[' . $post['content'] . ']]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>' . $id . '</wp:post_id>
        <wp:post_date><![CDATA[' . date('Y-m-d H:i:s', strtotime('-' . rand(1, 30) . ' days')) . ']]></wp:post_date>
        <wp:post_date_gmt><![CDATA[' . date('Y-m-d H:i:s', strtotime('-' . rand(1, 30) . ' days')) . ']]></wp:post_date_gmt>
        <wp:comment_status><![CDATA[open]]></wp:comment_status>
        <wp:ping_status><![CDATA[open]]></wp:ping_status>
        <wp:post_name><![CDATA[' . $slug . ']]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[post]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        <category domain="category" nicename="' . $category . '"><![CDATA[' . $post['category'] . ']]></category>
    </item>';
            $id++;
        }
        
        return $xml;
    }

    private function createXMLFooter() {
        return '
</channel>
</rss>';
    }
}

// Generate the content
$generator = new AIContentGenerator();
$xml_content = $generator->generateContent();

// Save to file
$filename = 'riman-ai-content-' . date('Y-m-d-His') . '.xml';
file_put_contents($filename, $xml_content);

echo "✅ AI-Generated content XML created successfully!\n";
echo "📄 File: $filename\n";
echo "📊 Size: " . round(filesize($filename) / 1024, 2) . " KB\n\n";
echo "To import this content:\n";
echo "1. Go to WordPress Admin → Tools → Import\n";
echo "2. Select 'WordPress' importer\n";
echo "3. Upload the file: $filename\n";
echo "4. Assign authors and import\n\n";
echo "The XML contains:\n";
echo "- 13 Pages (Homepage, Services, About, Contact, etc.)\n";
echo "- 5 Blog Posts (Industry-relevant content)\n";
echo "- Categories for blog organization\n";
echo "- SEO-friendly URLs\n";
echo "- Structured content with Gutenberg blocks\n";