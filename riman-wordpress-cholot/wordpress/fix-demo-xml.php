<?php
/**
 * Fix demo-data.xml to use local image paths
 */

$xml_file = '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data.xml';
$output_file = '/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/demo-data-fixed.xml';

// Read the XML file
$xml_content = file_get_contents($xml_file);

// Replace with actual demo URLs from the live site
$replacements = [
    // Replace the old URL with the actual demo URL
    'https://theme.winnertheme.com/cholot/' => 'https://demo.ridianur.com/cholot/',
    
    // Fix the upload path
    'wp-content/uploadz/' => 'wp-content/uploads/sites/9/',
    
    // Also check for any guid references
    '<guid isPermaLink="false">https://theme.winnertheme.com/cholot/wp-content/uploadz/' => '<guid isPermaLink="false">https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/',
    
    // Fix attachment URLs
    '<wp:attachment_url><![CDATA[https://theme.winnertheme.com/cholot/wp-content/uploadz/' => '<wp:attachment_url><![CDATA[https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/',
];

foreach ($replacements as $old => $new) {
    $xml_content = str_replace($old, $new, $xml_content);
}

// Save the fixed XML
file_put_contents($output_file, $xml_content);

echo "✓ XML file fixed and saved to: $output_file\n\n";

// Count how many URLs were replaced
preg_match_all('/<wp:attachment_url>.*?<\/wp:attachment_url>/', $xml_content, $matches);
echo "Found " . count($matches[0]) . " attachment URLs\n\n";

// Show sample of fixed URLs
echo "Sample fixed URLs:\n";
for ($i = 0; $i < min(5, count($matches[0])); $i++) {
    $url = strip_tags($matches[0][$i]);
    echo "  - $url\n";
}

echo "\n✅ You can now import the fixed XML file:\n";
echo "   demo-data-fixed.xml\n";