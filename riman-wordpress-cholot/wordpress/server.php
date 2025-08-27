<?php
// Router script for PHP built-in server
// Handles WordPress properly and prevents freezing

$uri = urldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));

// Set max execution time for each request
set_time_limit(30);

// Increase memory limit
ini_set('memory_limit', '512M');

// Handle static files
if ($uri !== '/' && file_exists(__DIR__ . $uri)) {
    // Serve static files directly
    return false;
}

// Handle WordPress
$_SERVER['SCRIPT_NAME'] = '/index.php';
$_SERVER['SCRIPT_FILENAME'] = __DIR__ . '/index.php';
require_once __DIR__ . '/index.php';