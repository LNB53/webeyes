<?php
putenv('PYTHONPATH=/home/webserver/.local/lib/python3.10/site-packages');
// FTP server settings
$ftp_server = "10.0.0.204"; // FTP server IP address
$ftp_username = "ftpserver"; // FTP username
$ftp_password = "ITF"; // FTP password
$ftp_dir = "/home/ftpserver/userfiles"; // Directory on FTP server to upload files
// Check if file has been uploaded and appname is set
if ($_FILES["dropzone-file"]["error"] == UPLOAD_ERR_OK && isset($_POST["appname"])) {
    $appname = $_POST["appname"];
    
    // Validate appname
    if (!preg_match('/^[a-z0-9]+$/', $appname)) {
        die("Invalid application name. Only lowercase letters and numbers are allowed, with no spaces.");
    }

    // Connect to FTP server
    $conn_id = ftp_connect($ftp_server);
    if (!$conn_id) {
        die("Failed to connect to FTP server");
    }
    echo "Connected to FTP server successfully.\n"; // Debug statement

    // Login to FTP server
    $login = ftp_login($conn_id, $ftp_username, $ftp_password);
    if (!$login) {
        die("Failed to login to FTP server");
    }
    echo "Logged in to FTP server successfully.\n"; // Debug statement

    // Change directory to FTP upload directory
    if (!ftp_chdir($conn_id, $ftp_dir)) {
        die("Failed to change directory on FTP server");
    }
    echo "Changed directory on FTP server successfully.\n"; // Debug statement

    // Upload file to FTP server
    $file_tmp = $_FILES["dropzone-file"]["tmp_name"];
    $file_extension = pathinfo($_FILES["dropzone-file"]["name"], PATHINFO_EXTENSION);
    $file_name = $appname . '.' . $file_extension;

    if (!ftp_put($conn_id, $file_name, $file_tmp, FTP_BINARY)) {
        ftp_close($conn_id); // Close FTP connection
        die("Failed to upload file to FTP server");
    }
    echo "Uploaded file to FTP server successfully.\n"; // Debug statement
    
    // Close FTP connection
    ftp_close($conn_id);
    echo "Closed FTP connection.\n"; // Debug statement

    // Execute Python script
    $python_script = "py/upload.py";
    $command = "/usr/bin/python3 $python_script $file_name 2>&1";
    echo exec($command, $output, $return_var);
    
    // Print the value of return_var
    echo "Return value of Python script: $return_var\n";

    // Check if Python script executed successfully
    if ($return_var !== 0) {
        die("Error executing Python script");
    }

    // Execute check.sh script with a 20-second timeout
    $ssh_host = '10.0.0.40';
    $ssh_user = 'user';
    $check_script_command = "/home/user/check.sh";
    $timeout = 20; // 20 seconds timeout
    $ssh_command = "timeout $timeout ssh -o StrictHostKeyChecking=no -i /var/www/.ssh/id_rsa $ssh_user@$ssh_host \"$check_script_command\" 2>&1";

    // Execute SSH command and capture output
    $ssh_output = shell_exec($ssh_command);

    // Log the SSH command and its output for debugging purposes
    file_put_contents('/var/www/ssh_command.log', $ssh_command . PHP_EOL, FILE_APPEND);
    file_put_contents('/var/www/ssh_output.log', $ssh_output . PHP_EOL, FILE_APPEND);

    // Check if there's any output on stderr
    if (strpos($ssh_output, 'sudo: ') !== false) {
        die("Error executing check.sh script");
    }

    // Redirect back to the form with success parameter
    header("Location: dashboard.html?s=T");
    exit;
} else {
    // Handle file upload error
    die("File upload failed");
}
?>
