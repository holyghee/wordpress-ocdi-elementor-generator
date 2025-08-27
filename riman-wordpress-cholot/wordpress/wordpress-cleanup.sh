#!/bin/bash

# WordPress Cleanup Script - Safe Version
# Preserves WordPress core structure while cleaning content

echo "🧹 WordPress Safe Cleanup Script"
echo "================================"
echo "This script will clean WordPress content while preserving structure"
echo ""

# Configuration
DB_NAME="wordpress_cholot_test"
DB_USER="wp_user"
DB_PASS="wp_password123"
WP_PATH="/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress"

# Function to run MySQL commands
run_mysql() {
    mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$1" 2>/dev/null
}

# 1. Clean database content (preserve structure)
echo "📊 Cleaning database content..."
run_mysql "
-- Preserve WordPress structure, only clean content
SET FOREIGN_KEY_CHECKS = 0;

-- Delete all posts except default sample page
DELETE FROM wp_posts WHERE ID > 2;
DELETE FROM wp_postmeta WHERE post_id > 2;

-- Clean comments
TRUNCATE TABLE wp_comments;
TRUNCATE TABLE wp_commentmeta;

-- Clean term relationships but keep default category
DELETE FROM wp_term_relationships WHERE object_id > 2;
DELETE FROM wp_term_taxonomy WHERE term_id > 1;
DELETE FROM wp_terms WHERE term_id > 1;

-- Clean transients and cache
DELETE FROM wp_options WHERE option_name LIKE '_transient_%';
DELETE FROM wp_options WHERE option_name LIKE '_site_transient_%';

-- Clean Elementor cache but keep settings
DELETE FROM wp_options WHERE option_name LIKE '_elementor_css_%';
DELETE FROM wp_options WHERE option_name = 'elementor_global_css';
DELETE FROM wp_options WHERE option_name LIKE 'elementor_screenshots_%';

-- Clean import remnants
DELETE FROM wp_options WHERE option_name LIKE 'ocdi_%';
DELETE FROM wp_options WHERE option_name LIKE '_wxr_%';

-- Reset auto increment
ALTER TABLE wp_posts AUTO_INCREMENT = 100;
ALTER TABLE wp_postmeta AUTO_INCREMENT = 100;
ALTER TABLE wp_comments AUTO_INCREMENT = 1;
ALTER TABLE wp_commentmeta AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;
"

echo "✅ Database cleaned"

# 2. Clean uploads directory (preserve structure)
echo "📁 Cleaning uploads directory..."
if [ -d "$WP_PATH/wp-content/uploads" ]; then
    # Remove year directories but keep uploads folder
    find "$WP_PATH/wp-content/uploads" -type d -name "20*" -exec rm -rf {} + 2>/dev/null
    # Remove Elementor uploads
    rm -rf "$WP_PATH/wp-content/uploads/elementor" 2>/dev/null
    echo "✅ Uploads cleaned"
else
    echo "⚠️  Uploads directory not found"
fi

# 3. Clean cache directories
echo "🗑️  Cleaning cache..."
rm -rf "$WP_PATH/wp-content/cache/"* 2>/dev/null
rm -rf "$WP_PATH/wp-content/et-cache/"* 2>/dev/null
rm -f "$WP_PATH/wp-content/debug.log" 2>/dev/null
echo "✅ Cache cleaned"

# 4. Fix Elementor warnings
echo "🔧 Fixing Elementor warnings..."
run_mysql "
-- Create minimal post to prevent null warnings
INSERT IGNORE INTO wp_posts (ID, post_author, post_date, post_date_gmt, post_content, post_title, post_status, post_type)
VALUES (1, 1, NOW(), NOW(), '', 'Home', 'publish', 'page')
ON DUPLICATE KEY UPDATE post_status = 'publish';

-- Set homepage
UPDATE wp_options SET option_value = '1' WHERE option_name = 'show_on_front';
UPDATE wp_options SET option_value = '1' WHERE option_name = 'page_on_front';
"
echo "✅ Elementor warnings fixed"

# 5. Verify cleanup
echo ""
echo "📊 Cleanup Summary:"
echo "-------------------"

POST_COUNT=$(run_mysql "SELECT COUNT(*) FROM wp_posts;" | tail -1)
ATTACHMENT_COUNT=$(run_mysql "SELECT COUNT(*) FROM wp_posts WHERE post_type='attachment';" | tail -1)
COMMENT_COUNT=$(run_mysql "SELECT COUNT(*) FROM wp_comments;" | tail -1)

echo "Posts remaining: $POST_COUNT"
echo "Attachments: $ATTACHMENT_COUNT"
echo "Comments: $COMMENT_COUNT"

echo ""
echo "✅ WordPress cleanup complete!"
echo "🎯 Ready for fresh import"
echo ""
echo "Note: The site structure is preserved. You can now import content safely."