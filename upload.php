<?php
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
        die("Failed to upload file to FTP server");
    }
    echo "Uploaded file to FTP server successfully.\n"; // Debug statement

    // Close FTP connection
    ftp_close($conn_id);
    echo "Closed FTP connection.\n"; // Debug statement

    // Redirect back to the form with success message
    header("Location: dashboard.html");
    exit;
} else {
    // Handle file upload error
    die("File upload failed");
}
?>
