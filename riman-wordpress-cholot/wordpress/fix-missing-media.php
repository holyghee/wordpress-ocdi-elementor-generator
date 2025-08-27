<?php
/**
 * Fix Missing Media for Cholot Demo Import
 * Creates placeholder images for missing media files
 */

// Set up WordPress environment
$_SERVER['HTTP_HOST'] = 'localhost:8080';
$_SERVER['REQUEST_URI'] = '/';
$_SERVER['SERVER_NAME'] = 'localhost';

require_once('wp-load.php');

// List of missing images from the error log
$missing_images = [
    'esther-town-492626-unsplash' => 'Hero Background',
    'huy-phan-100866-unsplash' => 'Service Image 1',
    'damir-bosnjak-366766-unsplash' => 'Service Image 2', 
    'josh-appel-423804-unsplash' => 'Portfolio Image 1',
    'matteo-vistocco-537858-unsplash' => 'About Us Background',
    'val-vesa-410839-unsplash' => 'Team Member 1',
    'vlad-sargu-479334-unsplash' => 'Gallery Image',
    'anthony-metcalfe-580436-unsplash' => 'Contact Background',
    'sign' => 'Sign Image',
    '1' => 'Gallery 1',
    '2' => 'Gallery 2', 
    '3' => 'Gallery 3',
    '4' => 'Gallery 4',
    '5' => 'Gallery 5',
    '6' => 'Gallery 6',
    '7' => 'Gallery 7',
    '8' => 'Gallery 8',
    'team1' => 'Team Member 1',
    'team2' => 'Team Member 2',
    'team3' => 'Team Member 3',
    'logo' => 'Logo',
    'logo-white' => 'Logo White',
    'cropped-matteo-vistocco-537858-unsplash.jpg' => 'Cropped Header',
    'bg-ab' => 'About Background'
];

// Create uploads directory structure
$upload_dir = wp_upload_dir();
$base_dir = $upload_dir['basedir'];
$base_url = $upload_dir['baseurl'];

echo "Fixing missing media files...\n\n";

// Create placeholder images
foreach ($missing_images as $filename => $description) {
    // Determine file extension
    $ext = 'jpg';
    if (strpos($filename, '.') === false) {
        $filename .= '.jpg';
    } else {
        $parts = explode('.', $filename);
        $ext = end($parts);
    }
    
    $filepath = $base_dir . '/2019/07/' . $filename;
    
    // Create directory if it doesn't exist
    $dir = dirname($filepath);
    if (!file_exists($dir)) {
        wp_mkdir_p($dir);
    }
    
    // Create placeholder image
    $width = 1920;
    $height = 1080;
    
    // Special sizes for different types
    if (strpos($filename, 'logo') !== false) {
        $width = 300;
        $height = 100;
    } elseif (strpos($filename, 'team') !== false || strpos($filename, 'val-vesa') !== false) {
        $width = 400;
        $height = 400;
    } elseif (is_numeric(str_replace('.jpg', '', $filename))) {
        $width = 800;
        $height = 600;
    }
    
    // Create image
    $image = imagecreatetruecolor($width, $height);
    
    // Set colors
    $bg_color = imagecolorallocate($image, 200, 168, 130); // RIMAN golden color
    $text_color = imagecolorallocate($image, 255, 255, 255);
    $border_color = imagecolorallocate($image, 160, 137, 104);
    
    // Fill background
    imagefill($image, 0, 0, $bg_color);
    
    // Add border
    imagerectangle($image, 0, 0, $width-1, $height-1, $border_color);
    imagerectangle($image, 1, 1, $width-2, $height-2, $border_color);
    
    // Add text
    $font_size = 5; // Built-in font size
    $text = strtoupper($description);
    $text_width = imagefontwidth($font_size) * strlen($text);
    $text_height = imagefontheight($font_size);
    $x = ($width - $text_width) / 2;
    $y = ($height - $text_height) / 2;
    
    imagestring($image, $font_size, $x, $y, $text, $text_color);
    
    // Add filename below
    $filename_text = basename($filename, '.' . $ext);
    $filename_width = imagefontwidth(3) * strlen($filename_text);
    $x2 = ($width - $filename_width) / 2;
    $y2 = $y + $text_height + 10;
    imagestring($image, 3, $x2, $y2, $filename_text, $text_color);
    
    // Save image
    if ($ext == 'jpg' || $ext == 'jpeg') {
        imagejpeg($image, $filepath, 85);
    } else {
        imagepng($image, $filepath);
    }
    
    imagedestroy($image);
    
    echo "✓ Created: $filepath\n";
    
    // Add to WordPress Media Library
    $file_url = $base_url . '/2019/07/' . $filename;
    
    // Check if already exists in database
    global $wpdb;
    $existing = $wpdb->get_var($wpdb->prepare(
        "SELECT ID FROM $wpdb->posts WHERE post_type = 'attachment' AND post_title = %s",
        str_replace(['.jpg', '.png', '-', '_'], ' ', basename($filename, '.' . $ext))
    ));
    
    if (!$existing) {
        $attachment = array(
            'guid' => $file_url,
            'post_mime_type' => ($ext == 'png') ? 'image/png' : 'image/jpeg',
            'post_title' => str_replace(['.jpg', '.png', '-', '_'], ' ', basename($filename, '.' . $ext)),
            'post_content' => '',
            'post_status' => 'inherit'
        );
        
        $attach_id = wp_insert_attachment($attachment, $filepath);
        
        if (!is_wp_error($attach_id)) {
            require_once(ABSPATH . 'wp-admin/includes/image.php');
            $attach_data = wp_generate_attachment_metadata($attach_id, $filepath);
            wp_update_attachment_metadata($attach_id, $attach_data);
            echo "  → Added to Media Library (ID: $attach_id)\n";
        }
    } else {
        echo "  → Already in Media Library\n";
    }
    
    echo "\n";
}

echo "\n✅ All missing media files have been created!\n";
echo "\nYou can now retry the import process.\n";

// Also create copies in theme directory if needed
$theme_dir = get_template_directory() . '/images/';
if (!file_exists($theme_dir)) {
    wp_mkdir_p($theme_dir);
}

// Copy logo files to theme
$logo_files = ['logo.jpg', 'logo-white.jpg'];
foreach ($logo_files as $logo) {
    $source = $base_dir . '/2019/07/' . $logo;
    $dest = $theme_dir . str_replace('.jpg', '.png', $logo);
    
    if (file_exists($source)) {
        // Convert to PNG for logos
        $image = imagecreatefromjpeg($source);
        imagepng($image, $dest);
        imagedestroy($image);
        echo "✓ Copied logo to theme: $dest\n";
    }
}

echo "\nDone!\n";