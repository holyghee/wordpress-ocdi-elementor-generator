<?php
/**
 * CHOLOT OCDI IMPORT SYSTEM
 * 
 * Direkter WordPress XML Import via OCDI Plugin
 * Erstellt von SWARM CHOLOT TESTER für automatisierten Import-Test
 * 
 * Usage: php test-ocdi-import.php [xml-file]
 * 
 * Author: Claude Code Assistant (OCDI TEST SUITE BUILDER)
 * Date: 2025-08-28
 * Memory Namespace: swarm-cholot-tester-1756407314892
 */

// WordPress Environment Setup
define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Command Line Arguments
$xml_file = $argv[1] ?? 'cholot-final.xml';

echo "🚀 CHOLOT OCDI IMPORT SYSTEM\n";
echo "============================\n";
echo "Target Site: " . get_site_url() . "\n";
echo "XML File: " . $xml_file . "\n";
echo "Timestamp: " . date('Y-m-d H:i:s') . "\n";
echo "============================\n\n";

// Validate XML File
if ( ! file_exists( $xml_file ) ) {
    echo "❌ ERROR: XML file not found: $xml_file\n";
    echo "\nAvailable XML files:\n";
    
    $xml_files = glob( '*.xml' );
    foreach ( $xml_files as $file ) {
        echo "  - $file\n";
    }
    
    exit( 1 );
}

echo "📄 XML File validated: " . filesize( $xml_file ) . " bytes\n";

// Check OCDI Plugin Availability
$ocdi_plugin_file = WP_PLUGIN_DIR . '/one-click-demo-import/one-click-demo-import.php';
$ocdi_main_class = WP_PLUGIN_DIR . '/one-click-demo-import/inc/class-ocdi-main.php';

if ( ! file_exists( $ocdi_plugin_file ) ) {
    echo "❌ ERROR: One Click Demo Import plugin not found!\n";
    echo "Expected location: $ocdi_plugin_file\n";
    echo "\nPlease install OCDI plugin:\n";
    echo "1. Download from: https://wordpress.org/plugins/one-click-demo-import/\n";
    echo "2. Extract to: wp-content/plugins/one-click-demo-import/\n";
    echo "3. Activate in WordPress admin\n";
    exit( 1 );
}

echo "✅ OCDI Plugin found\n";

// Load OCDI Plugin Components
if ( ! class_exists( 'OCDI\\Importer' ) ) {
    require_once $ocdi_plugin_file;
    
    // Include necessary OCDI classes
    $ocdi_includes = array(
        '/inc/class-ocdi-importer.php',
        '/inc/class-ocdi-logger.php',
        '/inc/class-ocdi-helpers.php'
    );
    
    foreach ( $ocdi_includes as $include_file ) {
        $full_path = WP_PLUGIN_DIR . '/one-click-demo-import' . $include_file;
        if ( file_exists( $full_path ) ) {
            require_once $full_path;
            echo "📦 Loaded: " . basename( $include_file ) . "\n";
        }
    }
}

// XML Structure Analysis
echo "\n🔍 XML ANALYSIS\n";
echo "================\n";

$xml_analysis = analyze_xml_structure( $xml_file );
echo "📊 XML Items: " . $xml_analysis['total_items'] . "\n";
echo "📄 Pages: " . $xml_analysis['pages'] . "\n";
echo "📝 Posts: " . $xml_analysis['posts'] . "\n";
echo "🖼️  Media: " . $xml_analysis['media'] . "\n";
echo "🎨 Elementor Pages: " . $xml_analysis['elementor_pages'] . "\n";

// Pre-Import Backup
echo "\n💾 PRE-IMPORT BACKUP\n";
echo "====================\n";

$backup_data = create_backup_snapshot();
echo "✅ Current state backed up:\n";
echo "  - Pages: " . $backup_data['pages'] . "\n";
echo "  - Posts: " . $backup_data['posts'] . "\n";
echo "  - Media: " . $backup_data['media'] . "\n";

// OCDI Import Process
echo "\n📥 STARTING OCDI IMPORT\n";
echo "=======================\n";

$import_start_time = microtime( true );

try {
    // Create OCDI Logger
    $logger = new \OCDI\Logger();
    
    // Import Configuration
    $import_options = array(
        'fetch_attachments' => true,  // Import media files
        'default_author' => 1,        // Default author ID
        'update_author' => false,     // Don't update existing authors
    );
    
    echo "⚙️  Import Options:\n";
    foreach ( $import_options as $option => $value ) {
        echo "   $option: " . ( $value ? 'true' : 'false' ) . "\n";
    }
    
    // Create OCDI Importer Instance
    $importer = new \OCDI\Importer( $import_options, $logger );
    
    echo "\n🚀 Starting content import...\n";
    
    // Import Content
    $import_result = $importer->import_content( $xml_file );
    
    $import_end_time = microtime( true );
    $import_duration = round( $import_end_time - $import_start_time, 2 );
    
    echo "\n✅ IMPORT COMPLETED in {$import_duration} seconds!\n";
    
} catch ( Exception $e ) {
    echo "\n❌ IMPORT FAILED!\n";
    echo "Error: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . ":" . $e->getLine() . "\n";
    
    // Attempt Fallback Import
    echo "\n🔄 Attempting fallback import...\n";
    $fallback_result = fallback_wordpress_import( $xml_file );
    
    if ( ! $fallback_result ) {
        exit( 1 );
    }
}

// Post-Import Configuration
echo "\n🔧 POST-IMPORT SETUP\n";
echo "====================\n";

// 1. Set Homepage
$home_page = get_page_by_title( 'Home' );
if ( $home_page ) {
    update_option( 'page_on_front', $home_page->ID );
    update_option( 'show_on_front', 'page' );
    echo "🏠 Homepage set: " . $home_page->post_title . " (ID: " . $home_page->ID . ")\n";
} else {
    echo "⚠️  Home page not found - manual setup required\n";
}

// 2. Configure Menus
$menus = wp_get_nav_menus();
if ( ! empty( $menus ) ) {
    foreach ( $menus as $menu ) {
        // Assign first menu to primary location if not already assigned
        $locations = get_nav_menu_locations();
        if ( empty( $locations['primary'] ) && $menu->name === 'Main Menu' ) {
            $locations['primary'] = $menu->term_id;
            set_theme_mod( 'nav_menu_locations', $locations );
            echo "📋 Menu assigned: " . $menu->name . " → primary location\n";
        }
    }
}

// 3. Activate Elementor
if ( is_plugin_active( 'elementor/elementor.php' ) ) {
    echo "🎨 Elementor is active\n";
} else {
    echo "⚠️  Elementor plugin not active - Elementor pages may not display correctly\n";
}

// 4. Flush Rewrite Rules
flush_rewrite_rules();
echo "🔄 Permalink structure refreshed\n";

// Import Results Analysis
echo "\n📊 IMPORT RESULTS ANALYSIS\n";
echo "==========================\n";

$post_import_data = analyze_import_results();

echo "📈 Import Summary:\n";
echo "  Pages imported: " . ( $post_import_data['pages'] - $backup_data['pages'] ) . "\n";
echo "  Posts imported: " . ( $post_import_data['posts'] - $backup_data['posts'] ) . "\n";
echo "  Media imported: " . ( $post_import_data['media'] - $backup_data['media'] ) . "\n";

echo "\n📋 Current Content:\n";
echo "  Total Pages: " . $post_import_data['pages'] . "\n";
echo "  Total Posts: " . $post_import_data['posts'] . "\n";
echo "  Total Media: " . $post_import_data['media'] . "\n";

// Elementor Data Verification
echo "\n🎨 ELEMENTOR VERIFICATION\n";
echo "=========================\n";

$elementor_verification = verify_elementor_import();
echo "📄 Pages with Elementor data: " . $elementor_verification['elementor_pages'] . "\n";
echo "🔧 Total Elementor elements: " . $elementor_verification['total_elements'] . "\n";

if ( $elementor_verification['errors'] > 0 ) {
    echo "⚠️  Elementor import issues: " . $elementor_verification['errors'] . "\n";
}

// Quality Assessment
echo "\n✅ QUALITY ASSESSMENT\n";
echo "======================\n";

$quality_score = calculate_import_quality_score( $xml_analysis, $post_import_data, $elementor_verification );

echo "🎯 Import Quality Score: " . $quality_score . "/100\n";

if ( $quality_score >= 90 ) {
    echo "🏆 EXCELLENT: Import highly successful!\n";
} elseif ( $quality_score >= 75 ) {
    echo "✅ GOOD: Import successful with minor issues\n";
} elseif ( $quality_score >= 60 ) {
    echo "⚠️  FAIR: Import partially successful - review required\n";
} else {
    echo "❌ POOR: Import had significant issues - manual intervention needed\n";
}

// Generate Report
echo "\n📄 GENERATING REPORT\n";
echo "====================\n";

$report_data = array(
    'timestamp' => date( 'Y-m-d H:i:s' ),
    'xml_file' => $xml_file,
    'site_url' => get_site_url(),
    'import_duration' => $import_duration ?? 0,
    'xml_analysis' => $xml_analysis,
    'backup_data' => $backup_data,
    'post_import_data' => $post_import_data,
    'elementor_verification' => $elementor_verification,
    'quality_score' => $quality_score,
    'logger_messages' => $logger->get_logs() ?? array()
);

$report_file = 'cholot-import-report-' . date( 'Ymd-His' ) . '.json';
file_put_contents( $report_file, json_encode( $report_data, JSON_PRETTY_PRINT ) );

echo "📊 Report saved: $report_file\n";

echo "\n🎉 CHOLOT OCDI IMPORT COMPLETED!\n";
echo "================================\n";
echo "Next Steps:\n";
echo "1. Visit: " . get_site_url() . "\n";
echo "2. Check pages and content\n";
echo "3. Verify Elementor designs\n";
echo "4. Run visual comparison tests\n";
echo "\n";

// Helper Functions
function analyze_xml_structure( $xml_file ) {
    $data = array(
        'total_items' => 0,
        'pages' => 0,
        'posts' => 0,
        'media' => 0,
        'elementor_pages' => 0
    );
    
    try {
        $xml = simplexml_load_file( $xml_file );
        $items = $xml->xpath( '//item' );
        
        $data['total_items'] = count( $items );
        
        foreach ( $items as $item ) {
            $post_type = (string) $item->children( 'wp', true )->post_type;
            
            switch ( $post_type ) {
                case 'page':
                    $data['pages']++;
                    
                    // Check for Elementor data
                    $postmetas = $item->xpath( './/wp:postmeta[wp:meta_key="_elementor_data"]' );
                    if ( ! empty( $postmetas ) ) {
                        $data['elementor_pages']++;
                    }
                    break;
                    
                case 'post':
                    $data['posts']++;
                    break;
                    
                case 'attachment':
                    $data['media']++;
                    break;
            }
        }
        
    } catch ( Exception $e ) {
        error_log( "XML analysis error: " . $e->getMessage() );
    }
    
    return $data;
}

function create_backup_snapshot() {
    return array(
        'pages' => wp_count_posts( 'page' )->publish,
        'posts' => wp_count_posts( 'post' )->publish,
        'media' => wp_count_posts( 'attachment' )->inherit
    );
}

function analyze_import_results() {
    return array(
        'pages' => wp_count_posts( 'page' )->publish,
        'posts' => wp_count_posts( 'post' )->publish,
        'media' => wp_count_posts( 'attachment' )->inherit
    );
}

function verify_elementor_import() {
    $verification = array(
        'elementor_pages' => 0,
        'total_elements' => 0,
        'errors' => 0
    );
    
    // Get pages with Elementor data
    $elementor_pages = get_posts( array(
        'post_type' => 'page',
        'meta_key' => '_elementor_data',
        'numberposts' => -1,
    ) );
    
    $verification['elementor_pages'] = count( $elementor_pages );
    
    foreach ( $elementor_pages as $page ) {
        $elementor_data = get_post_meta( $page->ID, '_elementor_data', true );
        
        if ( $elementor_data ) {
            $data = json_decode( $elementor_data, true );
            
            if ( is_array( $data ) ) {
                foreach ( $data as $section ) {
                    $verification['total_elements']++;
                    
                    if ( isset( $section['elements'] ) ) {
                        foreach ( $section['elements'] as $column ) {
                            if ( isset( $column['elements'] ) ) {
                                $verification['total_elements'] += count( $column['elements'] );
                            }
                        }
                    }
                }
            } else {
                $verification['errors']++;
            }
        } else {
            $verification['errors']++;
        }
    }
    
    return $verification;
}

function calculate_import_quality_score( $xml_analysis, $post_import_data, $elementor_verification ) {
    $score = 0;
    
    // Base import success (40 points)
    if ( $post_import_data['pages'] > 0 ) $score += 20;
    if ( $post_import_data['posts'] >= 0 ) $score += 10;
    if ( $post_import_data['media'] >= 0 ) $score += 10;
    
    // Elementor import success (40 points)
    if ( $elementor_verification['elementor_pages'] > 0 ) {
        $score += 20;
        
        if ( $elementor_verification['total_elements'] > 0 ) {
            $score += 15;
        }
        
        // Penalty for errors
        if ( $elementor_verification['errors'] == 0 ) {
            $score += 5;
        }
    }
    
    // Homepage setup (20 points)
    $home_page = get_page_by_title( 'Home' );
    if ( $home_page ) {
        $score += 10;
        
        if ( get_option( 'page_on_front' ) == $home_page->ID ) {
            $score += 10;
        }
    }
    
    return min( $score, 100 );
}

function fallback_wordpress_import( $xml_file ) {
    echo "🔄 Using WordPress native importer...\n";
    
    try {
        if ( ! defined( 'WP_LOAD_IMPORTERS' ) ) {
            define( 'WP_LOAD_IMPORTERS', true );
        }
        
        require_once ABSPATH . 'wp-admin/includes/import.php';
        
        if ( file_exists( ABSPATH . 'wp-admin/includes/class-wp-importer.php' ) ) {
            require_once ABSPATH . 'wp-admin/includes/class-wp-importer.php';
        }
        
        if ( file_exists( ABSPATH . 'wp-admin/includes/class-wp-import.php' ) ) {
            require_once ABSPATH . 'wp-admin/includes/class-wp-import.php';
        }
        
        if ( class_exists( 'WP_Import' ) ) {
            $importer = new WP_Import();
            $importer->fetch_attachments = false;
            $importer->import( $xml_file );
            
            echo "✅ Fallback import completed\n";
            return true;
        } else {
            echo "❌ WordPress importer class not available\n";
            return false;
        }
        
    } catch ( Exception $e ) {
        echo "❌ Fallback import failed: " . $e->getMessage() . "\n";
        return false;
    }
}