<?php
// Theme-Setup
function wp_blank_modern_setup() {
    // Theme-Unterstützung hinzufügen
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ));
    add_theme_support('custom-logo', array( // Standardwerte für Custom Logo hier direkt setzen
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ));
    add_theme_support('customize-selective-refresh-widgets');
    
    // Menüs registrieren
    register_nav_menus(array(
        'primary' => __('Hauptmenü', 'wp-blank-modern'),
    ));
}
add_action('after_setup_theme', 'wp_blank_modern_setup');

// Scripts und Styles laden
function wp_blank_modern_scripts() {
    wp_enqueue_style('wp-blank-modern-style', get_stylesheet_uri(), array(), '1.0');
    // Es wird kein separates navigation.js benötigt, da der JS-Code direkt im Footer ist
}
add_action('wp_enqueue_scripts', 'wp_blank_modern_scripts');

// Navigation für Mobile (JavaScript im Footer)
function wp_blank_modern_mobile_navigation_script() {
    ?>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const menuToggle = document.querySelector('.menu-toggle');
        const navigation = document.querySelector('.main-navigation');
        
        if (menuToggle && navigation) {
            menuToggle.addEventListener('click', function() {
                navigation.classList.toggle('toggled');
                // ARIA-Attribute aktualisieren
                let isExpanded = menuToggle.getAttribute('aria-expanded') === 'true' || false;
                menuToggle.setAttribute('aria-expanded', !isExpanded);
                navigation.classList.toggle('toggled');
            });
        }
    });
    </script>
    <?php
}
add_action('wp_footer', 'wp_blank_modern_mobile_navigation_script');

// Excerpt-Länge anpassen
function wp_blank_modern_excerpt_length($length) {
    return 30; // Anzahl der Wörter
}
add_filter('excerpt_length', 'wp_blank_modern_excerpt_length');

// Weiterlesen-Link für Excerpt anpassen
function wp_blank_modern_excerpt_more($more) {
    return '... <a class="read-more" href="' . get_permalink(get_the_ID()) . '">' . __('Weiterlesen', 'wp-blank-modern') . '</a>';
}
add_filter('excerpt_more', 'wp_blank_modern_excerpt_more');

// Fallback-Menü, falls kein Menü zugewiesen ist
// Diese Funktion wird in header.php verwendet, daher hier definieren, wenn sie dort aufgerufen wird.
// Es ist besser, sie hier zu haben, um functions.php sauber zu halten.
if (!function_exists('wp_blank_modern_fallback_menu')) {
    function wp_blank_modern_fallback_menu() {
        echo '<ul id="primary-menu" class="menu">';
        echo '<li><a href="' . esc_url(home_url('/')) . '">' . __('Startseite', 'wp-blank-modern') . '</a></li>';
        wp_list_pages(array(
            'title_li' => '',
            'depth'    => 1,
        ));
        echo '</ul>';
    }
}
?>
