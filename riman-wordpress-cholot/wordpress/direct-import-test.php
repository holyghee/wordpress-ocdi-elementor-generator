<?php
// WordPress Bootstrap
define( 'WP_USE_THEMES', false );
require( 'wp-load.php' );

// Parse the XML file directly
$file = 'riman-xl-site-no-images.xml';

if ( ! file_exists( $file ) ) {
    die( "Error: XML file not found: $file\n" );
}

echo "🚀 Parsing $file\n";

// Load and parse XML
$xml = simplexml_load_file( $file );

// Register namespaces
$xml->registerXPathNamespace('wp', 'http://wordpress.org/export/1.2/');
$xml->registerXPathNamespace('content', 'http://purl.org/rss/1.0/modules/content/');
$xml->registerXPathNamespace('excerpt', 'http://wordpress.org/export/1.2/excerpt/');
$xml->registerXPathNamespace('dc', 'http://purl.org/dc/elements/1.1/');

// First, import the nav_menu terms
$terms = $xml->xpath('//wp:term[wp:term_taxonomy="nav_menu"]');
echo "\n📋 Found " . count($terms) . " menu term(s) to import\n";

foreach ($terms as $term) {
    $term_id = (string) $term->children('wp', true)->term_id;
    $term_slug = (string) $term->children('wp', true)->term_slug;
    $term_name = (string) $term->children('wp', true)->term_name;
    
    echo "  Creating menu: $term_name (slug: $term_slug)\n";
    
    // Check if menu already exists
    $existing = get_term_by('slug', $term_slug, 'nav_menu');
    
    if (!$existing) {
        // Create the menu
        $menu_id = wp_create_nav_menu($term_name);
        
        if (is_wp_error($menu_id)) {
            echo "    ❌ Failed to create menu: " . $menu_id->get_error_message() . "\n";
        } else {
            echo "    ✅ Menu created with ID: $menu_id\n";
            
            // Update the slug if needed
            $created_menu = get_term($menu_id, 'nav_menu');
            if ($created_menu && $created_menu->slug !== $term_slug) {
                wp_update_term($menu_id, 'nav_menu', array('slug' => $term_slug));
                echo "    ✅ Menu slug updated to: $term_slug\n";
            }
        }
    } else {
        echo "    ℹ️ Menu already exists with ID: " . $existing->term_id . "\n";
        $menu_id = $existing->term_id;
    }
}

// Import pages first
$pages = $xml->xpath('//item[wp:post_type="page"]');
echo "\n📄 Found " . count($pages) . " page(s) to import\n";

$page_mapping = array();
foreach ($pages as $page) {
    $post_id = (string) $page->children('wp', true)->post_id;
    $title = (string) $page->title;
    $slug = (string) $page->children('wp', true)->post_name;
    $content = (string) $page->children('content', true)->encoded;
    
    // Check if page exists
    $existing_page = get_page_by_path($slug);
    
    if (!$existing_page) {
        $new_id = wp_insert_post(array(
            'post_title' => $title,
            'post_name' => $slug,
            'post_content' => $content,
            'post_status' => 'publish',
            'post_type' => 'page',
        ));
        
        if (!is_wp_error($new_id)) {
            $page_mapping[$post_id] = $new_id;
            echo "  ✅ Created: $title (ID: $new_id)\n";
        }
    } else {
        $page_mapping[$post_id] = $existing_page->ID;
        echo "  ℹ️ Exists: $title (ID: " . $existing_page->ID . ")\n";
    }
}

// Now import menu items
$menu_items = $xml->xpath('//item[wp:post_type="nav_menu_item"]');
echo "\n🔗 Found " . count($menu_items) . " menu item(s) to import\n";

$menu_item_mapping = array();
foreach ($menu_items as $item) {
    $old_id = (string) $item->children('wp', true)->post_id;
    $title = (string) $item->title;
    $menu_order = (int) $item->children('wp', true)->menu_order;
    
    // Get the menu this item belongs to
    $menu_category = $item->xpath('category[@domain="nav_menu"]');
    $menu_slug = $menu_category ? (string) $menu_category[0]['nicename'] : 'default-menu';
    
    // Get menu ID
    $menu = get_term_by('slug', $menu_slug, 'nav_menu');
    if (!$menu) {
        echo "  ❌ Menu not found for item: $title\n";
        continue;
    }
    
    // Get meta data
    $metas = array();
    foreach ($item->children('wp', true)->postmeta as $meta) {
        $key = (string) $meta->children('wp', true)->meta_key;
        $value = (string) $meta->children('wp', true)->meta_value;
        $metas[$key] = $value;
    }
    
    // Map object_id for pages
    if (isset($metas['_menu_item_object_id']) && isset($page_mapping[$metas['_menu_item_object_id']])) {
        $metas['_menu_item_object_id'] = $page_mapping[$metas['_menu_item_object_id']];
    }
    
    // Map parent menu item
    $parent = 0;
    if (isset($metas['_menu_item_menu_item_parent']) && $metas['_menu_item_menu_item_parent'] != '0') {
        $old_parent = $metas['_menu_item_menu_item_parent'];
        if (isset($menu_item_mapping[$old_parent])) {
            $parent = $menu_item_mapping[$old_parent];
        }
    }
    
    // Create menu item
    $menu_item_data = array(
        'menu-item-title' => $title,
        'menu-item-type' => $metas['_menu_item_type'] ?? 'custom',
        'menu-item-object' => $metas['_menu_item_object'] ?? 'custom',
        'menu-item-object-id' => $metas['_menu_item_object_id'] ?? 0,
        'menu-item-url' => $metas['_menu_item_url'] ?? '#',
        'menu-item-parent-id' => $parent,
        'menu-item-position' => $menu_order,
        'menu-item-status' => 'publish',
    );
    
    $new_item_id = wp_update_nav_menu_item($menu->term_id, 0, $menu_item_data);
    
    if (!is_wp_error($new_item_id)) {
        $menu_item_mapping[$old_id] = $new_item_id;
        echo "  ✅ Added to menu: $title (ID: $new_item_id)\n";
    } else {
        echo "  ❌ Failed: $title - " . $new_item_id->get_error_message() . "\n";
    }
}

// Final check
echo "\n--- Final Results ---\n\n";

$menus = wp_get_nav_menus();
echo "📋 Navigation Menus: " . count($menus) . "\n";

foreach ($menus as $menu) {
    echo "\n✓ " . $menu->name . " (ID: " . $menu->term_id . ", Slug: " . $menu->slug . ")\n";
    
    $menu_items = wp_get_nav_menu_items($menu->term_id);
    echo "  Items: " . count($menu_items) . "\n";
    
    if ($menu_items) {
        // Sort by menu order
        usort($menu_items, function($a, $b) {
            return $a->menu_order - $b->menu_order;
        });
        
        foreach ($menu_items as $item) {
            $indent = $item->menu_item_parent ? "    ↳ " : "    - ";
            echo $indent . $item->title . " (" . $item->type . ")\n";
        }
    }
}