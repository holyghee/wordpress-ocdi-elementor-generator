<?php
// Connect to WordPress database
$mysqli = new mysqli('localhost', 'wp_user', 'wp_password123', 'wordpress_cholot_test');

if ($mysqli->connect_error) {
    die('Connection failed: ' . $mysqli->connect_error);
}

// Get current active plugins
$result = $mysqli->query("SELECT option_value FROM wp_options WHERE option_name = 'active_plugins'");
$row = $result->fetch_assoc();
$active_plugins = unserialize($row['option_value']);

// Add our plugin if not already active
$plugin_path = 'cholot-form-styles/cholot-form-styles.php';
if (!in_array($plugin_path, $active_plugins)) {
    $active_plugins[] = $plugin_path;
    $serialized = serialize($active_plugins);
    
    $stmt = $mysqli->prepare("UPDATE wp_options SET option_value = ? WHERE option_name = 'active_plugins'");
    $stmt->bind_param('s', $serialized);
    $stmt->execute();
    
    echo "Plugin activated successfully!\n";
} else {
    echo "Plugin is already active.\n";
}

$mysqli->close();