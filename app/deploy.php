<?php
$secret = '1668be5265021fba526217363816dbaff5a84a19';
$deployScript = '/var/www/webeyes/deploy.sh';
$logFile = '/var/www/deploy.log';

function logMessage($message) {
    global $logFile;
    file_put_contents($logFile, date('Y-m-d H:i:s') . " - " . $message . PHP_EOL, FILE_APPEND);
}

$payload = file_get_contents('php://input');
$signature = $_SERVER['HTTP_X_HUB_SIGNATURE_256'];

if (!$signature) {
    logMessage("No signature provided.");
    exit('No signature provided');
}

$hash = 'sha256=' . hash_hmac('sha256', $payload, $secret);
if (!hash_equals($hash, $signature)) {
    logMessage("Invalid signature.");
    exit('Invalid signature');
}

$data = json_decode($payload, true);

if (isset($data['ref']) && $data['ref'] === 'refs/heads/main') {
    logMessage("Branch matched. Executing deploy script.");
    $output = shell_exec($deployScript . ' 2>&1');
    logMessage("Deploy script output: " . $output);
} else {
    logMessage("Branch did not match or ref not set.");
}
