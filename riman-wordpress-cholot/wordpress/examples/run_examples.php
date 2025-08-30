<?php
/**
 * YAML Processor Examples Demonstration
 * 
 * This script demonstrates how to process the three example YAML files
 * and shows the flexibility of our YAML-to-WordPress pipeline.
 */

// Simple YAML parser for demonstration purposes
function parse_yaml_simple($filename) {
    if (!extension_loaded('yaml')) {
        die("YAML extension not loaded. Install with: pecl install yaml\n");
    }
    return yaml_parse_file($filename);
}

class ExampleDemonstrator {
    private $examples_dir;
    
    public function __construct() {
        $this->examples_dir = __DIR__;
    }
    
    /**
     * Run all example demonstrations
     */
    public function runAllExamples() {
        echo "=== YAML Processor Examples Demonstration ===\n\n";
        
        // Simple Example
        $this->runExample('simple_example', 'Minimal Single-Page Website');
        
        // Service Company Example
        $this->runExample('service_company', 'Professional Service Company');
        
        // Restaurant Example
        $this->runExample('restaurant_example', 'Restaurant & Dining Experience');
        
        echo "\n=== Demonstration Complete ===\n";
        echo "All examples processed successfully!\n";
        echo "Check the generated output to see how the same YAML processor\n";
        echo "creates completely different website types.\n\n";
    }
    
    /**
     * Process a single example
     */
    private function runExample($filename, $description) {
        echo "--- Processing: {$description} ---\n";
        
        $yaml_file = "{$this->examples_dir}/{$filename}.yaml";
        $output_dir = "{$this->examples_dir}/output/{$filename}";
        
        // Check if YAML file exists
        if (!file_exists($yaml_file)) {
            echo "ERROR: {$yaml_file} not found!\n\n";
            return;
        }
        
        // Create output directory
        if (!is_dir($output_dir)) {
            mkdir($output_dir, 0755, true);
        }
        
        try {
            // Process the YAML file
            echo "📁 Loading: {$filename}.yaml\n";
            $config = parse_yaml_simple($yaml_file);
            
            echo "✅ YAML parsed successfully\n";
            echo "📊 Site Name: {$config['site_name']}\n";
            echo "📝 Description: {$config['site_description']}\n";
            
            // Count sections
            $sections = isset($config['sections']) ? $config['sections'] : [];
            $section_count = count($sections);
            echo "📑 Sections: {$section_count}\n";
            
            // Show section types
            $section_types = [];
            foreach ($sections as $section) {
                $section_types[] = $section['type'];
            }
            echo "🏗️  Section Types: " . implode(', ', array_unique($section_types)) . "\n";
            
            // Generate files
            echo "🔄 Generating WordPress files...\n";
            $this->generateExampleFiles($config, $output_dir, $filename);
            
            echo "✅ Files generated in: {$output_dir}\n";
            echo "🌐 Commands to process:\n";
            echo "   php yaml_processor.php {$yaml_file}\n";
            echo "   # or\n";
            echo "   ./process_yaml.sh {$yaml_file}\n\n";
            
        } catch (Exception $e) {
            echo "❌ ERROR: " . $e->getMessage() . "\n\n";
        }
    }
    
    /**
     * Generate example output files to show what would be created
     */
    private function generateExampleFiles($config, $output_dir, $filename) {
        // Generate index.php
        $this->generateIndexFile($config, $output_dir);
        
        // Generate style.css
        $this->generateStyleFile($config, $output_dir);
        
        // Generate functions.php
        $this->generateFunctionsFile($config, $output_dir);
        
        // Generate README with instructions
        $this->generateReadmeFile($config, $output_dir, $filename);
        
        // Show file structure
        echo "📋 Generated files:\n";
        $files = scandir($output_dir);
        foreach ($files as $file) {
            if ($file !== '.' && $file !== '..') {
                echo "   - {$file}\n";
            }
        }
    }
    
    /**
     * Generate a sample index.php file
     */
    private function generateIndexFile($config, $output_dir) {
        $content = "<?php\n";
        $content .= "/**\n";
        $content .= " * Theme: {$config['site_name']}\n";
        $content .= " * Generated from YAML configuration\n";
        $content .= " */\n\n";
        $content .= "get_header(); ?>\n\n";
        
        $sections = isset($config['sections']) ? $config['sections'] : [];
        foreach ($sections as $index => $section) {
            $content .= "<!-- Section: {$section['type']} -->\n";
            $content .= "<section id=\"{$section['id']}\" class=\"section-{$section['type']}\">\n";
            
            if (isset($section['title'])) {
                $content .= "    <h2>{$section['title']}</h2>\n";
            }
            
            if (isset($section['subtitle'])) {
                $content .= "    <p class=\"subtitle\">{$section['subtitle']}</p>\n";
            }
            
            // Add section-specific content based on type
            switch ($section['type']) {
                case 'hero':
                    $content .= "    <!-- Hero section with call-to-action -->\n";
                    break;
                case 'services':
                    $services = isset($section['services']) ? $section['services'] : [];
                    $services_count = count($services);
                    $content .= "    <!-- Services grid with {$services_count} services -->\n";
                    break;
                case 'menu':
                    $menu_categories = isset($section['menu_categories']) ? $section['menu_categories'] : [];
                    $categories_count = count($menu_categories);
                    $content .= "    <!-- Restaurant menu with {$categories_count} categories -->\n";
                    break;
                case 'contact':
                    $form_fields = isset($section['form_fields']) ? $section['form_fields'] : [];
                    $fields_count = count($form_fields);
                    $content .= "    <!-- Contact form with {$fields_count} fields -->\n";
                    break;
                default:
                    $content .= "    <!-- {$section['type']} content -->\n";
            }
            
            $content .= "</section>\n\n";
        }
        
        $content .= "<?php get_footer(); ?>\n";
        
        file_put_contents("{$output_dir}/index.php", $content);
    }
    
    /**
     * Generate a sample style.css file
     */
    private function generateStyleFile($config, $output_dir) {
        $theme = isset($config['theme']) ? $config['theme'] : [];
        
        $content = "/*\n";
        $content .= "Theme Name: {$config['site_name']}\n";
        $content .= "Description: {$config['site_description']}\n";
        $content .= "Generated from YAML configuration\n";
        $content .= "*/\n\n";
        
        $content .= ":root {\n";
        $primary_color = isset($theme['primary_color']) ? $theme['primary_color'] : '#3498db';
        $secondary_color = isset($theme['secondary_color']) ? $theme['secondary_color'] : '#2c3e50';
        $accent_color = isset($theme['accent_color']) ? $theme['accent_color'] : '#e74c3c';
        $font_family = isset($theme['font_family']) ? $theme['font_family'] : 'Arial, sans-serif';
        
        $content .= "  --primary-color: {$primary_color};\n";
        $content .= "  --secondary-color: {$secondary_color};\n";
        $content .= "  --accent-color: {$accent_color};\n";
        $content .= "  --font-family: {$font_family};\n";
        $content .= "}\n\n";
        
        $content .= "body {\n";
        $content .= "  font-family: var(--font-family);\n";
        $content .= "  color: var(--secondary-color);\n";
        $content .= "}\n\n";
        
        // Add section-specific styles based on what's in the config
        $sections = isset($config['sections']) ? $config['sections'] : [];
        foreach ($sections as $section) {
            $content .= ".section-{$section['type']} {\n";
            $content .= "  /* Styles for {$section['type']} section */\n";
            $content .= "  padding: 60px 0;\n";
            $content .= "}\n\n";
        }
        
        file_put_contents("{$output_dir}/style.css", $content);
    }
    
    /**
     * Generate a sample functions.php file
     */
    private function generateFunctionsFile($config, $output_dir) {
        $content = "<?php\n";
        $content .= "/**\n";
        $content .= " * Theme Functions for {$config['site_name']}\n";
        $content .= " * Generated from YAML configuration\n";
        $content .= " */\n\n";
        
        $content .= "// Enqueue styles and scripts\n";
        $content .= "function theme_enqueue_scripts() {\n";
        $content .= "    wp_enqueue_style('theme-style', get_stylesheet_uri());\n";
        $content .= "    wp_enqueue_script('theme-script', get_template_directory_uri() . '/js/main.js', array('jquery'), '1.0.0', true);\n";
        $content .= "}\n";
        $content .= "add_action('wp_enqueue_scripts', 'theme_enqueue_scripts');\n\n";
        
        // Add navigation menu support if navigation is defined
        if (isset($config['navigation'])) {
            $content .= "// Register navigation menus\n";
            $content .= "function register_theme_menus() {\n";
            $content .= "    register_nav_menus(array(\n";
            $content .= "        'primary' => 'Primary Menu'\n";
            $content .= "    ));\n";
            $content .= "}\n";
            $content .= "add_action('init', 'register_theme_menus');\n\n";
        }
        
        // Add theme support features
        $content .= "// Theme support\n";
        $content .= "function theme_setup() {\n";
        $content .= "    add_theme_support('title-tag');\n";
        $content .= "    add_theme_support('post-thumbnails');\n";
        $content .= "    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption'));\n";
        $content .= "}\n";
        $content .= "add_action('after_setup_theme', 'theme_setup');\n";
        
        file_put_contents("{$output_dir}/functions.php", $content);
    }
    
    /**
     * Generate README with instructions
     */
    private function generateReadmeFile($config, $output_dir, $filename) {
        $content = "# {$config['site_name']}\n\n";
        $content .= "{$config['site_description']}\n\n";
        $content .= "## Generated from YAML Configuration\n\n";
        $content .= "This WordPress theme was automatically generated from the `{$filename}.yaml` configuration file.\n\n";
        
        $content .= "### Configuration Summary\n\n";
        $content .= "- **Site Name:** {$config['site_name']}\n";
        $sections = isset($config['sections']) ? $config['sections'] : [];
        $navigation = isset($config['navigation']) ? $config['navigation'] : [];
        $theme = isset($config['theme']) ? $config['theme'] : [];
        $primary_color = isset($theme['primary_color']) ? $theme['primary_color'] : 'Not set';
        
        $content .= "- **Sections:** " . count($sections) . "\n";
        $content .= "- **Navigation Items:** " . count($navigation) . "\n";
        $content .= "- **Primary Color:** {$primary_color}\n\n";
        
        $content .= "### Section Types\n\n";
        foreach ($sections as $section) {
            $section_title = isset($section['title']) ? $section['title'] : 'No title';
            $content .= "- **{$section['type']}**: {$section_title}\n";
            if (isset($section['id'])) {
                $content .= "  - ID: `{$section['id']}`\n";
            }
        }
        
        $content .= "\n### How to Use\n\n";
        $content .= "1. Copy the generated files to your WordPress theme directory\n";
        $content .= "2. Activate the theme in WordPress admin\n";
        $content .= "3. Customize further using WordPress Customizer\n\n";
        
        $content .= "### Processing Commands\n\n";
        $content .= "To regenerate this theme:\n\n";
        $content .= "```bash\n";
        $content .= "# Using the YAML processor directly\n";
        $content .= "php yaml_processor.php {$filename}.yaml\n\n";
        $content .= "# Using the convenience script\n";
        $content .= "./process_yaml.sh {$filename}.yaml\n\n";
        $content .= "# Or using the examples script\n";
        $content .= "php examples/run_examples.php\n";
        $content .= "```\n\n";
        
        $content .= "---\n";
        $content .= "*Generated by YAML Processor at " . date('Y-m-d H:i:s') . "*\n";
        
        file_put_contents("{$output_dir}/README.md", $content);
    }
}

// Run the demonstration if this script is called directly
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    $demonstrator = new ExampleDemonstrator();
    $demonstrator->runAllExamples();
}
?>