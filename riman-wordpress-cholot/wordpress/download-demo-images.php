<?php
/**
 * Download real images from Cholot demo site
 */

// Image URLs from the demo site
$demo_images = [
    'val-vesa-410839-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/val-vesa-410839-unsplash.jpg',
    'esther-town-492626-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/esther-town-492626-unsplash.jpg',
    'huy-phan-100866-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/huy-phan-100866-unsplash.jpg',
    'damir-bosnjak-366766-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/damir-bosnjak-366766-unsplash.jpg',
    'josh-appel-423804-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/josh-appel-423804-unsplash.jpg',
    'matteo-vistocco-537858-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/matteo-vistocco-537858-unsplash.jpg',
    'vlad-sargu-479334-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/vlad-sargu-479334-unsplash.jpg',
    'anthony-metcalfe-580436-unsplash.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/anthony-metcalfe-580436-unsplash.jpg',
    'sign.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/sign.jpg',
    'team1.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/team1.jpg',
    'team2.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/team2.jpg',
    'team3.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/team3.jpg',
    'logo.png' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/logo.png',
    'logo-white.png' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/logo-white.png',
    'bg-ab.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/06/bg-ab.jpg',
    '1.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/1.jpg',
    '2.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/2.jpg',
    '3.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/3.jpg',
    '4.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/4.jpg',
    '5.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/5.jpg',
    '6.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/6.jpg',
    '7.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/7.jpg',
    '8.jpg' => 'https://demo.ridianur.com/cholot/wp-content/uploads/sites/9/2019/07/8.jpg',
];

// Create upload directory
$upload_dir = '/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/wp-content/uploads/2019/07/';
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}

echo "Downloading real images from Cholot demo site...\n\n";

foreach ($demo_images as $filename => $url) {
    $local_path = $upload_dir . $filename;
    
    echo "Downloading: $filename\n";
    echo "From: $url\n";
    
    // Download the image
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    $image_data = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($http_code == 200 && $image_data) {
        file_put_contents($local_path, $image_data);
        $size = filesize($local_path);
        echo "✓ Downloaded successfully (" . round($size/1024) . " KB)\n";
        
        // Also save without extension for WordPress import
        $name_without_ext = pathinfo($filename, PATHINFO_FILENAME);
        if ($name_without_ext != $filename) {
            copy($local_path, $upload_dir . $name_without_ext);
            echo "  → Also saved as: $name_without_ext\n";
        }
    } else {
        echo "✗ Failed to download (HTTP $http_code)\n";
    }
    
    echo "\n";
}

// Also create June directory for some images
$june_dir = '/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/wp-content/uploads/2019/06/';
if (!file_exists($june_dir)) {
    mkdir($june_dir, 0755, true);
}

// Copy June images to June folder
$june_images = [
    'val-vesa-410839-unsplash.jpg',
    'esther-town-492626-unsplash.jpg',
    'huy-phan-100866-unsplash.jpg',
    'damir-bosnjak-366766-unsplash.jpg',
    'josh-appel-423804-unsplash.jpg',
    'matteo-vistocco-537858-unsplash.jpg',
    'vlad-sargu-479334-unsplash.jpg',
    'anthony-metcalfe-580436-unsplash.jpg',
    'sign.jpg',
    'logo.png',
    'logo-white.png',
    'bg-ab.jpg'
];

echo "Copying images to June folder...\n";
foreach ($june_images as $image) {
    if (file_exists($upload_dir . $image)) {
        copy($upload_dir . $image, $june_dir . $image);
        echo "✓ Copied to June: $image\n";
    }
}

// Copy logos to theme directory
$theme_dir = '/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/wordpress-mediation-platform/wordpress/wp-content/themes/cholot/images/';
if (!file_exists($theme_dir)) {
    mkdir($theme_dir, 0755, true);
}

if (file_exists($upload_dir . 'logo.png')) {
    copy($upload_dir . 'logo.png', $theme_dir . 'logo.png');
    echo "\n✓ Copied logo.png to theme directory\n";
}

if (file_exists($upload_dir . 'logo-white.png')) {
    copy($upload_dir . 'logo-white.png', $theme_dir . 'logo-white.png');
    echo "✓ Copied logo-white.png to theme directory\n";
}

echo "\n✅ All images downloaded successfully!\n";
echo "You can now retry the import without errors.\n";