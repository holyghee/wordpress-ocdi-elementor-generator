<?php
require_once 'wp-load.php';

// Regeneriere Elementor CSS für alle Seiten
if (class_exists('\Elementor\Plugin')) {
    $elementor = \Elementor\Plugin::instance();
    
    // Hole alle Elementor-Seiten
    $args = array(
        'post_type' => array('page', 'post'),
        'meta_key' => '_elementor_edit_mode',
        'meta_value' => 'builder',
        'posts_per_page' => -1
    );
    
    $posts = get_posts($args);
    
    echo "🎨 Regenerating Elementor CSS for " . count($posts) . " pages...\n\n";
    
    foreach ($posts as $post) {
        // Regeneriere CSS für jede Seite
        $css_file = \Elementor\Core\Files\CSS\Post::create($post->ID);
        $css_file->update();
        echo "✅ CSS regeneriert für: " . $post->post_title . " (ID: " . $post->ID . ")\n";
    }
    
    // Clear Cache
    $elementor->files_manager->clear_cache();
    echo "\n✅ Elementor Cache geleert\n";
    
    // Also clear WordPress cache
    wp_cache_flush();
    echo "✅ WordPress Cache geleert\n";
} else {
    echo "❌ Elementor Plugin nicht aktiv!\n";
}
?>