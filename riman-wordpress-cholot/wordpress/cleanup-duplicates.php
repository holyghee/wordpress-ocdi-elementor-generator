<?php
/**
 * Remove duplicate pages from the first import
 * Keep the newer ones (ID > 1500)
 */

require_once 'wp-load.php';

// List of duplicate page titles and their old IDs to delete
$duplicates_to_delete = [
    179,  // About (keep 1576)
    374,  // Assited living (keep 1581)
    289,  // Contact (keep 1578)
    6,    // Home (keep 1575)
    365,  // Independent living (keep 1579)
    251,  // Service (keep 1577)
    429,  // Blog (keep 1589)
    467,  // Page with custom header & custom footer (keep 1594)
    
    // Duplicate posts
    436,  // Aliquam lorem ante dapibus in tellus (keep 1599)
    425,  // Blandit vel luctus pulvinar hendrerit massa quis enim (keep 1588)
    426,  // Duis arcu tortor suscipit egetro etante (keep 1596)
    411,  // Every carry ready the quinoa mperdiet etiam (keep 1585)
    417,  // Interest humble brag air plant nec odio et ante (keep 1586)
    424,  // Purus quamut mollised aenean commodo (keep 1587)
    427,  // Ultricies mieu turpis hendrerit ultricies (keep 1597)
    428,  // Venenatis faucibus nullam quisenean (keep 1598)
];

echo "Cleaning up duplicate pages and posts...\n\n";

foreach ($duplicates_to_delete as $post_id) {
    $post = get_post($post_id);
    if ($post) {
        echo "Deleting: [{$post_id}] {$post->post_title}\n";
        wp_delete_post($post_id, true); // true = force delete (skip trash)
    }
}

// Also delete the test pages that are not needed
$test_pages = [
    2,   // Beispiel-Seite
    42,  // Test
    1,   // Hallo Welt!
];

echo "\nDeleting test pages...\n";
foreach ($test_pages as $post_id) {
    $post = get_post($post_id);
    if ($post) {
        echo "Deleting: [{$post_id}] {$post->post_title}\n";
        wp_delete_post($post_id, true);
    }
}

// Update the homepage setting to use the new Home page
update_option('show_on_front', 'page');
update_option('page_on_front', 1575); // New Home page ID
update_option('page_for_posts', 1589); // New Blog page ID

echo "\n✅ Cleanup complete!\n";
echo "Homepage set to: Home (ID: 1575)\n";
echo "Blog page set to: Blog (ID: 1589)\n";