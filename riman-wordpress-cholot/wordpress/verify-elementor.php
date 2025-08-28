<?php
/**
 * Verify Elementor Data Import
 * 
 * Umfassende Elementor Daten-Verifizierung nach OCDI Import
 * Teil der CHOLOT TEST SUITE
 * 
 * Usage: php verify-elementor.php [--detailed] [--page-id=123]
 * 
 * Author: Claude Code Assistant (OCDI TEST SUITE BUILDER)
 * Date: 2025-08-28
 */

define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Parse command line arguments
$detailed = in_array( '--detailed', $argv );
$specific_page = null;

foreach ( $argv as $arg ) {
    if ( strpos( $arg, '--page-id=' ) === 0 ) {
        $specific_page = intval( substr( $arg, 10 ) );
        break;
    }
}

echo "🎨 ELEMENTOR VERIFICATION UTILITY\n";
echo "=================================\n";
echo "Site: " . get_site_url() . "\n";
echo "Mode: " . ( $detailed ? 'Detailed Analysis' : 'Standard Check' ) . "\n";

if ( $specific_page ) {
    echo "Target: Page ID " . $specific_page . "\n";
}

echo "Timestamp: " . date('Y-m-d H:i:s') . "\n";
echo "=================================\n\n";

// Check if Elementor is active
if ( ! is_plugin_active( 'elementor/elementor.php' ) ) {
    echo "⚠️  WARNING: Elementor plugin is not active!\n";
    echo "Please activate Elementor plugin for proper functionality.\n\n";
}

// Get Elementor version
if ( defined( 'ELEMENTOR_VERSION' ) ) {
    echo "✅ Elementor Version: " . ELEMENTOR_VERSION . "\n\n";
} else {
    echo "⚠️  Elementor version not detected\n\n";
}

// Main verification function
if ( $specific_page ) {
    verify_single_page( $specific_page, $detailed );
} else {
    verify_all_elementor_pages( $detailed );
}

function verify_all_elementor_pages( $detailed = false ) {
    echo "📄 SCANNING FOR ELEMENTOR PAGES\n";
    echo "================================\n";
    
    // Get all pages with Elementor data
    $elementor_pages = get_posts( array(
        'post_type' => 'page',
        'meta_key' => '_elementor_data',
        'numberposts' => -1,
        'post_status' => 'any'
    ) );
    
    echo "Found: " . count( $elementor_pages ) . " pages with Elementor data\n\n";
    
    if ( empty( $elementor_pages ) ) {
        echo "❌ NO ELEMENTOR PAGES FOUND!\n";
        echo "This could indicate:\n";
        echo "1. Import failed to include Elementor data\n";
        echo "2. XML file doesn't contain Elementor meta fields\n";
        echo "3. Pages were imported but Elementor data was corrupted\n\n";
        
        // Check if there are any pages at all
        $all_pages = get_pages();
        echo "Total pages in site: " . count( $all_pages ) . "\n";
        
        if ( count( $all_pages ) > 0 ) {
            echo "\n📋 AVAILABLE PAGES (checking for Elementor indicators):\n";
            echo "======================================================\n";
            
            foreach ( $all_pages as $page ) {
                echo "Page: " . $page->post_title . " (ID: " . $page->ID . ")\n";
                
                // Check various Elementor meta fields
                $elementor_indicators = array(
                    '_elementor_data' => get_post_meta( $page->ID, '_elementor_data', true ),
                    '_elementor_edit_mode' => get_post_meta( $page->ID, '_elementor_edit_mode', true ),
                    '_elementor_template_type' => get_post_meta( $page->ID, '_elementor_template_type', true ),
                    '_elementor_version' => get_post_meta( $page->ID, '_elementor_version', true )
                );
                
                $has_elementor = false;
                foreach ( $elementor_indicators as $key => $value ) {
                    if ( ! empty( $value ) ) {
                        echo "  ✅ $key: " . ( strlen( $value ) > 50 ? '[Large Data]' : $value ) . "\n";
                        $has_elementor = true;
                    }
                }
                
                if ( ! $has_elementor ) {
                    echo "  ❌ No Elementor data found\n";
                }
                
                echo "\n";
            }
        }
        
        return;
    }
    
    // Statistics
    $stats = array(
        'total_pages' => count( $elementor_pages ),
        'total_sections' => 0,
        'total_widgets' => 0,
        'total_columns' => 0,
        'pages_with_errors' => 0,
        'widget_types' => array(),
        'template_types' => array()
    );
    
    echo "📊 DETAILED ANALYSIS\n";
    echo "====================\n";
    
    foreach ( $elementor_pages as $page ) {
        echo "\n🔍 ANALYZING: " . $page->post_title . " (ID: " . $page->ID . ")\n";
        echo str_repeat( "-", 50 ) . "\n";
        
        $page_stats = verify_single_page( $page->ID, $detailed, false );
        
        // Aggregate statistics
        $stats['total_sections'] += $page_stats['sections'];
        $stats['total_widgets'] += $page_stats['widgets'];
        $stats['total_columns'] += $page_stats['columns'];
        
        if ( $page_stats['has_errors'] ) {
            $stats['pages_with_errors']++;
        }
        
        // Collect widget types
        foreach ( $page_stats['widget_types'] as $type ) {
            if ( ! isset( $stats['widget_types'][$type] ) ) {
                $stats['widget_types'][$type] = 0;
            }
            $stats['widget_types'][$type]++;
        }
        
        // Collect template types
        $template_type = get_post_meta( $page->ID, '_elementor_template_type', true );
        if ( $template_type ) {
            if ( ! isset( $stats['template_types'][$template_type] ) ) {
                $stats['template_types'][$template_type] = 0;
            }
            $stats['template_types'][$template_type]++;
        }
    }
    
    // Final Summary
    echo "\n🎯 FINAL SUMMARY\n";
    echo "================\n";
    echo "Total Elementor Pages: " . $stats['total_pages'] . "\n";
    echo "Total Sections: " . $stats['total_sections'] . "\n";
    echo "Total Columns: " . $stats['total_columns'] . "\n";
    echo "Total Widgets: " . $stats['total_widgets'] . "\n";
    echo "Pages with Errors: " . $stats['pages_with_errors'] . "\n";
    
    if ( $stats['total_pages'] > 0 ) {
        $success_rate = ( ( $stats['total_pages'] - $stats['pages_with_errors'] ) / $stats['total_pages'] ) * 100;
        echo "Success Rate: " . round( $success_rate, 1 ) . "%\n";
    }
    
    echo "\n📊 WIDGET TYPES FOUND:\n";
    echo "=======================\n";
    foreach ( $stats['widget_types'] as $type => $count ) {
        echo sprintf( "  %-20s: %d\n", $type, $count );
    }
    
    echo "\n📋 TEMPLATE TYPES:\n";
    echo "===================\n";
    foreach ( $stats['template_types'] as $type => $count ) {
        echo sprintf( "  %-20s: %d\n", $type, $count );
    }
    
    // Quality Assessment
    echo "\n✅ QUALITY ASSESSMENT\n";
    echo "======================\n";
    
    if ( $stats['total_sections'] == 0 ) {
        echo "❌ CRITICAL: No Elementor sections found - import likely failed\n";
    } elseif ( $stats['pages_with_errors'] == 0 ) {
        echo "🏆 EXCELLENT: All Elementor pages imported successfully\n";
    } elseif ( $stats['pages_with_errors'] < $stats['total_pages'] / 2 ) {
        echo "✅ GOOD: Most Elementor pages imported successfully\n";
    } else {
        echo "⚠️  POOR: Many Elementor pages have issues - review required\n";
    }
    
    echo "\n📋 RECOMMENDATIONS:\n";
    echo "====================\n";
    
    if ( $stats['pages_with_errors'] > 0 ) {
        echo "1. Review pages with errors for manual fixes\n";
        echo "2. Check XML source for Elementor data integrity\n";
        echo "3. Consider re-importing specific pages\n";
    }
    
    if ( empty( $stats['widget_types'] ) ) {
        echo "1. Verify Elementor widgets are properly registered\n";
        echo "2. Check theme compatibility with Elementor\n";
    }
    
    if ( $stats['total_widgets'] > 0 && $stats['total_sections'] > 0 ) {
        echo "✅ Elementor structure appears healthy\n";
    }
    
    echo "\n";
}

function verify_single_page( $page_id, $detailed = false, $print_header = true ) {
    if ( $print_header ) {
        $page = get_post( $page_id );
        if ( ! $page ) {
            echo "❌ ERROR: Page with ID $page_id not found\n";
            return false;
        }
        
        echo "\n🔍 ANALYZING: " . $page->post_title . " (ID: " . $page_id . ")\n";
        echo str_repeat( "=", 50 ) . "\n";
    }
    
    $page_stats = array(
        'sections' => 0,
        'columns' => 0,
        'widgets' => 0,
        'has_errors' => false,
        'widget_types' => array(),
        'errors' => array()
    );
    
    // Check basic Elementor meta fields
    $elementor_data = get_post_meta( $page_id, '_elementor_data', true );
    $edit_mode = get_post_meta( $page_id, '_elementor_edit_mode', true );
    $template_type = get_post_meta( $page_id, '_elementor_template_type', true );
    $elementor_version = get_post_meta( $page_id, '_elementor_version', true );
    
    echo "📝 Basic Meta Fields:\n";
    echo "  Edit Mode: " . ( $edit_mode ?: 'not set' ) . "\n";
    echo "  Template Type: " . ( $template_type ?: 'not set' ) . "\n";
    echo "  Elementor Version: " . ( $elementor_version ?: 'not set' ) . "\n";
    echo "  Data Size: " . ( $elementor_data ? strlen( $elementor_data ) . ' chars' : 'no data' ) . "\n";
    
    if ( ! $elementor_data ) {
        echo "\n❌ CRITICAL: No Elementor data found!\n";
        $page_stats['has_errors'] = true;
        $page_stats['errors'][] = 'No _elementor_data meta field';
        return $page_stats;
    }
    
    // Parse Elementor data
    $data = json_decode( $elementor_data, true );
    
    if ( ! is_array( $data ) ) {
        echo "\n❌ ERROR: Elementor data is not valid JSON!\n";
        if ( $detailed ) {
            echo "Raw data preview: " . substr( $elementor_data, 0, 200 ) . "...\n";
        }
        $page_stats['has_errors'] = true;
        $page_stats['errors'][] = 'Invalid JSON in _elementor_data';
        return $page_stats;
    }
    
    if ( empty( $data ) ) {
        echo "\n⚠️  WARNING: Elementor data is empty array\n";
        $page_stats['has_errors'] = true;
        $page_stats['errors'][] = 'Empty _elementor_data array';
        return $page_stats;
    }
    
    echo "\n🎨 Elementor Structure:\n";
    echo "  Sections: " . count( $data ) . "\n";
    
    $page_stats['sections'] = count( $data );
    
    // Analyze each section
    foreach ( $data as $section_index => $section ) {
        if ( ! isset( $section['elType'] ) || $section['elType'] !== 'section' ) {
            continue;
        }
        
        if ( $detailed ) {
            echo "\n  📦 Section " . ( $section_index + 1 ) . ":\n";
            echo "    ID: " . ( $section['id'] ?? 'no-id' ) . "\n";
            echo "    Type: " . ( $section['elType'] ?? 'unknown' ) . "\n";
        }
        
        // Analyze columns in section
        if ( isset( $section['elements'] ) && is_array( $section['elements'] ) ) {
            $page_stats['columns'] += count( $section['elements'] );
            
            if ( $detailed ) {
                echo "    Columns: " . count( $section['elements'] ) . "\n";
            }
            
            // Analyze widgets in columns
            foreach ( $section['elements'] as $column_index => $column ) {
                if ( isset( $column['elements'] ) && is_array( $column['elements'] ) ) {
                    $page_stats['widgets'] += count( $column['elements'] );
                    
                    foreach ( $column['elements'] as $widget ) {
                        if ( isset( $widget['widgetType'] ) ) {
                            $page_stats['widget_types'][] = $widget['widgetType'];
                            
                            if ( $detailed ) {
                                echo "      🔧 " . $widget['widgetType'] . "\n";
                            }
                        } elseif ( isset( $widget['elType'] ) ) {
                            $page_stats['widget_types'][] = $widget['elType'];
                        }
                    }
                }
            }
        }
    }
    
    echo "  Columns: " . $page_stats['columns'] . "\n";
    echo "  Widgets: " . $page_stats['widgets'] . "\n";
    
    // Widget type summary for this page
    if ( ! empty( $page_stats['widget_types'] ) ) {
        $widget_counts = array_count_values( $page_stats['widget_types'] );
        echo "\n🔧 Widget Types on this page:\n";
        foreach ( $widget_counts as $type => $count ) {
            echo "  $type: $count\n";
        }
    }
    
    // Status assessment
    if ( $page_stats['sections'] > 0 && $page_stats['widgets'] > 0 ) {
        echo "\n✅ STATUS: Page structure looks healthy\n";
    } elseif ( $page_stats['sections'] > 0 ) {
        echo "\n⚠️  STATUS: Page has sections but no widgets\n";
        $page_stats['has_errors'] = true;
        $page_stats['errors'][] = 'Sections present but no widgets found';
    } else {
        echo "\n❌ STATUS: Page structure appears empty\n";
        $page_stats['has_errors'] = true;
        $page_stats['errors'][] = 'No sections or widgets found';
    }
    
    // Check page URL and preview
    $page_url = get_permalink( $page_id );
    echo "\n🔗 Page URL: " . $page_url . "\n";
    
    return $page_stats;
}

echo "\n🎉 ELEMENTOR VERIFICATION COMPLETED!\n";
echo "====================================\n";
echo "For detailed analysis of specific page:\n";
echo "  php verify-elementor.php --detailed --page-id=123\n";
echo "\nFor detailed analysis of all pages:\n";
echo "  php verify-elementor.php --detailed\n";
echo "\n";