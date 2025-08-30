<?php
/**
 * YAML Processor Examples Demonstration (Simplified)
 * 
 * This script demonstrates the three example YAML files without requiring
 * the full YAML processor or extensions.
 */

class SimpleExampleDemonstrator {
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
        $this->showExample('simple_example', 'Minimal Single-Page Website');
        
        // Service Company Example
        $this->showExample('service_company', 'Professional Service Company');
        
        // Restaurant Example
        $this->showExample('restaurant_example', 'Restaurant & Dining Experience');
        
        echo "\n=== Demonstration Complete ===\n";
        echo "All examples are ready to be processed!\n\n";
        echo "🚀 To process these examples with the actual YAML processor:\n";
        echo "   php yaml_processor.php examples/simple_example.yaml\n";
        echo "   php yaml_processor.php examples/service_company.yaml\n";
        echo "   php yaml_processor.php examples/restaurant_example.yaml\n\n";
        
        echo "📁 Or use the convenience script:\n";
        echo "   ./examples/process_example.sh simple\n";
        echo "   ./examples/process_example.sh service\n";
        echo "   ./examples/process_example.sh restaurant\n\n";
    }
    
    /**
     * Analyze and show information about a single example
     */
    private function showExample($filename, $description) {
        echo "--- {$description} ---\n";
        
        $yaml_file = "{$this->examples_dir}/{$filename}.yaml";
        
        // Check if YAML file exists
        if (!file_exists($yaml_file)) {
            echo "ERROR: {$yaml_file} not found!\n\n";
            return;
        }
        
        echo "📁 File: {$filename}.yaml\n";
        echo "📏 Size: " . $this->formatBytes(filesize($yaml_file)) . "\n";
        
        // Read file content to analyze
        $content = file_get_contents($yaml_file);
        $lines = explode("\n", $content);
        echo "📄 Lines: " . count($lines) . "\n";
        
        // Extract basic information by parsing simple patterns
        $info = $this->extractBasicInfo($content);
        
        echo "✅ Configuration Analysis:\n";
        echo "   🏷️  Site Name: {$info['site_name']}\n";
        echo "   📝 Description: {$info['site_description']}\n";
        echo "   🎨 Primary Color: {$info['primary_color']}\n";
        echo "   🧩 Sections Found: {$info['sections_count']}\n";
        echo "   🔗 Navigation Items: {$info['nav_items']}\n";
        
        if (!empty($info['section_types'])) {
            echo "   🏗️  Section Types: " . implode(', ', $info['section_types']) . "\n";
        }
        
        if (!empty($info['special_features'])) {
            echo "   ⭐ Special Features: " . implode(', ', $info['special_features']) . "\n";
        }
        
        echo "\n";
        
        // Create sample output directory
        $output_dir = "{$this->examples_dir}/output/{$filename}";
        if (!is_dir($output_dir)) {
            mkdir($output_dir, 0755, true);
        }
        
        // Create a demonstration README
        $this->createDemoReadme($info, $output_dir, $filename);
        
        echo "📋 Demo files created in: examples/output/{$filename}/\n";
        echo "\n";
    }
    
    /**
     * Extract basic information from YAML content using simple text parsing
     */
    private function extractBasicInfo($content) {
        $info = [
            'site_name' => 'Unknown',
            'site_description' => 'No description',
            'primary_color' => 'Not specified',
            'sections_count' => 0,
            'nav_items' => 0,
            'section_types' => [],
            'special_features' => []
        ];
        
        // Extract site name
        if (preg_match('/site_name:\s*["\']?([^"\'\n]+)["\']?/', $content, $matches)) {
            $info['site_name'] = trim($matches[1]);
        }
        
        // Extract site description
        if (preg_match('/site_description:\s*["\']?([^"\'\n]+)["\']?/', $content, $matches)) {
            $info['site_description'] = trim($matches[1]);
        }
        
        // Extract primary color
        if (preg_match('/primary_color:\s*["\']?([^"\'\n]+)["\']?/', $content, $matches)) {
            $info['primary_color'] = trim($matches[1]);
        }
        
        // Count sections by looking for "- type:" patterns
        $info['sections_count'] = preg_match_all('/^\s*-\s*type:\s*["\']?([^"\'\n]+)["\']?/m', $content, $section_matches);
        if (!empty($section_matches[1])) {
            $info['section_types'] = array_unique($section_matches[1]);
        }
        
        // Count navigation items
        $nav_section = '';
        if (preg_match('/navigation:\s*\n((?:\s*-\s*.*\n?)*)/s', $content, $nav_matches)) {
            $nav_section = $nav_matches[1];
            $info['nav_items'] = substr_count($nav_section, '- name:');
        }
        
        // Detect special features
        $special_features = [];
        if (strpos($content, 'menu_categories:') !== false) {
            $special_features[] = 'Restaurant Menu';
        }
        if (strpos($content, 'services:') !== false) {
            $special_features[] = 'Service Cards';
        }
        if (strpos($content, 'team_members:') !== false) {
            $special_features[] = 'Team Profiles';
        }
        if (strpos($content, 'testimonials:') !== false) {
            $special_features[] = 'Testimonials';
        }
        if (strpos($content, 'pricing_plans:') !== false) {
            $special_features[] = 'Pricing Tables';
        }
        if (strpos($content, 'gallery:') !== false) {
            $special_features[] = 'Image Gallery';
        }
        if (strpos($content, 'reservations:') !== false) {
            $special_features[] = 'Reservations';
        }
        if (strpos($content, 'wine_list:') !== false) {
            $special_features[] = 'Wine List';
        }
        if (strpos($content, 'social_feeds:') !== false) {
            $special_features[] = 'Social Media';
        }
        
        $info['special_features'] = $special_features;
        
        return $info;
    }
    
    /**
     * Format bytes into human readable format
     */
    private function formatBytes($size, $precision = 2) {
        $units = ['B', 'KB', 'MB', 'GB'];
        for ($i = 0; $size > 1024 && $i < count($units) - 1; $i++) {
            $size /= 1024;
        }
        return round($size, $precision) . ' ' . $units[$i];
    }
    
    /**
     * Create a demonstration README file
     */
    private function createDemoReadme($info, $output_dir, $filename) {
        $content = "# {$info['site_name']} - Example Demonstration\n\n";
        $content .= "{$info['site_description']}\n\n";
        
        $content .= "## Configuration Overview\n\n";
        $content .= "This example demonstrates a **{$info['site_name']}** website with the following features:\n\n";
        $content .= "- **Sections:** {$info['sections_count']} different content sections\n";
        $content .= "- **Navigation:** {$info['nav_items']} menu items\n";
        $content .= "- **Theme:** Primary color is {$info['primary_color']}\n\n";
        
        if (!empty($info['section_types'])) {
            $content .= "### Section Types\n\n";
            foreach ($info['section_types'] as $type) {
                $content .= "- `{$type}` - " . $this->getSectionDescription($type) . "\n";
            }
            $content .= "\n";
        }
        
        if (!empty($info['special_features'])) {
            $content .= "### Special Features\n\n";
            foreach ($info['special_features'] as $feature) {
                $content .= "- ✅ {$feature}\n";
            }
            $content .= "\n";
        }
        
        $content .= "## How This Example Works\n\n";
        $content .= "1. **YAML Configuration**: The `{$filename}.yaml` file contains all the website configuration\n";
        $content .= "2. **Processing**: The YAML processor reads this file and generates WordPress files\n";
        $content .= "3. **Output**: Complete WordPress theme with all sections and features\n\n";
        
        $content .= "## Processing Commands\n\n";
        $content .= "```bash\n";
        $content .= "# Process this example\n";
        $content .= "php yaml_processor.php examples/{$filename}.yaml\n\n";
        $content .= "# Or use the convenience script\n";
        $content .= "./examples/process_example.sh " . str_replace('_example', '', $filename) . "\n";
        $content .= "```\n\n";
        
        $content .= "## What Gets Generated\n\n";
        $content .= "When processed, this YAML configuration will create:\n\n";
        $content .= "- **index.php** - Main theme template with all {$info['sections_count']} sections\n";
        $content .= "- **style.css** - Theme styles with {$info['primary_color']} color scheme\n";
        $content .= "- **functions.php** - WordPress theme functions and features\n";
        $content .= "- **Elementor templates** - Pre-configured page builder templates\n";
        $content .= "- **Custom post types** - If needed for specific features\n\n";
        
        $content .= "---\n";
        $content .= "*This is a demonstration file showing how the YAML processor analyzes configurations.*\n";
        $content .= "*Generated at: " . date('Y-m-d H:i:s') . "*\n";
        
        file_put_contents("{$output_dir}/DEMO_README.md", $content);
    }
    
    /**
     * Get description for section types
     */
    private function getSectionDescription($type) {
        $descriptions = [
            'hero' => 'Landing section with title, subtitle, and call-to-action buttons',
            'content' => 'Text content block with optional images',
            'services' => 'Grid of service cards with icons and descriptions',
            'team' => 'Team member profiles with photos and social links',
            'testimonials' => 'Customer reviews and testimonials',
            'pricing' => 'Pricing tables with feature comparisons',
            'gallery' => 'Image gallery with categories and lightbox',
            'contact' => 'Contact form and business information',
            'menu' => 'Restaurant menu with categories and pricing',
            'reservations' => 'Online reservation system',
            'events' => 'Special events and offers',
            'stats' => 'Statistics and achievements display',
            'cta' => 'Call-to-action section',
            'story' => 'About/story section with rich content',
            'reviews' => 'Customer reviews and ratings'
        ];
        
        return isset($descriptions[$type]) ? $descriptions[$type] : 'Custom content section';
    }
}

// Run the demonstration if this script is called directly
if (basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    $demonstrator = new SimpleExampleDemonstrator();
    $demonstrator->runAllExamples();
}
?>