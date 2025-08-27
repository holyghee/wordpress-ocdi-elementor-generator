<?php
/**
 * WordPress Safe Cleanup Script - PHP Version
 * Can be run from WordPress admin or command line
 * 
 * Usage: php wordpress-cleanup.php
 * Or place in wp-content/mu-plugins for admin access
 */

// Check if WordPress is loaded
if (!defined('ABSPATH')) {
    // Load WordPress if running standalone
    require_once(__DIR__ . '/wp-load.php');
}

class WordPressCleanup {
    
    private $preserved_options = [
        'siteurl',
        'home',
        'blogname',
        'blogdescription',
        'users_can_register',
        'admin_email',
        'timezone_string',
        'date_format',
        'time_format',
        'start_of_week',
        'default_role',
        'WPLANG',
        'stylesheet',
        'template',
        'active_plugins',
        'elementor_version',
        'elementor_pro_version'
    ];
    
    public function __construct() {
        // Increase limits for cleanup
        @set_time_limit(300);
        @ini_set('memory_limit', '256M');
    }
    
    /**
     * Main cleanup function
     */
    public function cleanup() {
        echo "🧹 Starting WordPress Safe Cleanup...\n";
        
        $this->cleanDatabase();
        $this->cleanUploads();
        $this->cleanCache();
        $this->fixElementor();
        $this->showSummary();
        
        echo "✅ Cleanup complete!\n";
    }
    
    /**
     * Clean database content
     */
    private function cleanDatabase() {
        global $wpdb;
        
        echo "📊 Cleaning database...\n";
        
        // Disable foreign key checks
        $wpdb->query("SET FOREIGN_KEY_CHECKS = 0");
        
        // Clean posts (keep ID 1 and 2 for structure)
        $wpdb->query("DELETE FROM {$wpdb->posts} WHERE ID > 2");
        $wpdb->query("DELETE FROM {$wpdb->postmeta} WHERE post_id > 2");
        
        // Clean comments
        $wpdb->query("TRUNCATE TABLE {$wpdb->comments}");
        $wpdb->query("TRUNCATE TABLE {$wpdb->commentmeta}");
        
        // Clean terms (keep default category)
        $wpdb->query("DELETE FROM {$wpdb->term_relationships} WHERE object_id > 2");
        $wpdb->query("DELETE FROM {$wpdb->term_taxonomy} WHERE term_id > 1");
        $wpdb->query("DELETE FROM {$wpdb->terms} WHERE term_id > 1");
        
        // Clean transients
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_%'");
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_site_transient_%'");
        
        // Clean Elementor cache
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_elementor_css_%'");
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name = 'elementor_global_css'");
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE 'elementor_screenshots_%'");
        
        // Clean import remnants
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE 'ocdi_%'");
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_wxr_%'");
        
        // Reset auto increment
        $wpdb->query("ALTER TABLE {$wpdb->posts} AUTO_INCREMENT = 100");
        $wpdb->query("ALTER TABLE {$wpdb->postmeta} AUTO_INCREMENT = 100");
        
        // Re-enable foreign key checks
        $wpdb->query("SET FOREIGN_KEY_CHECKS = 1");
        
        echo "✅ Database cleaned\n";
    }
    
    /**
     * Clean uploads directory
     */
    private function cleanUploads() {
        echo "📁 Cleaning uploads...\n";
        
        $upload_dir = wp_upload_dir();
        $base_dir = $upload_dir['basedir'];
        
        // Remove year directories
        $year_dirs = glob($base_dir . '/20*', GLOB_ONLYDIR);
        foreach ($year_dirs as $dir) {
            $this->deleteDirectory($dir);
        }
        
        // Remove Elementor uploads
        if (is_dir($base_dir . '/elementor')) {
            $this->deleteDirectory($base_dir . '/elementor');
        }
        
        echo "✅ Uploads cleaned\n";
    }
    
    /**
     * Clean cache directories
     */
    private function cleanCache() {
        echo "🗑️  Cleaning cache...\n";
        
        $cache_dirs = [
            WP_CONTENT_DIR . '/cache',
            WP_CONTENT_DIR . '/et-cache',
            WP_CONTENT_DIR . '/uploads/elementor/css',
            WP_CONTENT_DIR . '/uploads/elementor/thumbs'
        ];
        
        foreach ($cache_dirs as $dir) {
            if (is_dir($dir)) {
                $this->deleteDirectory($dir);
            }
        }
        
        // Remove debug log
        if (file_exists(WP_CONTENT_DIR . '/debug.log')) {
            @unlink(WP_CONTENT_DIR . '/debug.log');
        }
        
        echo "✅ Cache cleaned\n";
    }
    
    /**
     * Fix Elementor warnings
     */
    private function fixElementor() {
        global $wpdb;
        
        echo "🔧 Fixing Elementor...\n";
        
        // Create a minimal page to prevent null warnings
        $page_exists = $wpdb->get_var("SELECT ID FROM {$wpdb->posts} WHERE ID = 1");
        
        if (!$page_exists) {
            $wpdb->insert(
                $wpdb->posts,
                [
                    'ID' => 1,
                    'post_author' => 1,
                    'post_date' => current_time('mysql'),
                    'post_date_gmt' => current_time('mysql', 1),
                    'post_content' => '',
                    'post_title' => 'Home',
                    'post_status' => 'publish',
                    'post_type' => 'page'
                ]
            );
        }
        
        // Set as homepage
        update_option('show_on_front', 'page');
        update_option('page_on_front', 1);
        
        // Clear Elementor cache
        if (class_exists('\Elementor\Plugin')) {
            \Elementor\Plugin::$instance->files_manager->clear_cache();
        }
        
        echo "✅ Elementor fixed\n";
    }
    
    /**
     * Show cleanup summary
     */
    private function showSummary() {
        global $wpdb;
        
        echo "\n📊 Cleanup Summary:\n";
        echo "-------------------\n";
        
        $posts = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts}");
        $attachments = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'attachment'");
        $comments = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->comments}");
        $terms = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->terms}");
        
        echo "Posts remaining: $posts\n";
        echo "Attachments: $attachments\n";
        echo "Comments: $comments\n";
        echo "Terms: $terms\n";
    }
    
    /**
     * Helper: Delete directory recursively
     */
    private function deleteDirectory($dir) {
        if (!is_dir($dir)) {
            return;
        }
        
        $files = array_diff(scandir($dir), ['.', '..']);
        
        foreach ($files as $file) {
            $path = $dir . '/' . $file;
            is_dir($path) ? $this->deleteDirectory($path) : unlink($path);
        }
        
        return rmdir($dir);
    }
}

// Run cleanup if executed directly
if (php_sapi_name() === 'cli' || (!defined('DOING_AJAX') && !defined('DOING_CRON'))) {
    $cleanup = new WordPressCleanup();
    $cleanup->cleanup();
}