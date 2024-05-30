<?php
// Function to execute the rm command via SSH
function executeRmCommand() {
    try {
        // SSH credentials for the remote server
        $ssh_host = '10.0.0.40';
        $ssh_user = 'user';  // Remote server user
        $remote_file = '/home/user/rm/file.zip'; // Path to the file to delete on the remote server

        // SSH command to execute the rm command with sudo
        $command = "ssh -o StrictHostKeyChecking=no -i /var/www/.ssh/id_rsa $ssh_user@$ssh_host 'sudo rm -f $remote_file' 2>&1";

        // Execute the SSH command
        $output = shell_exec($command);

        // Log the output for debugging purposes
        file_put_contents('/var/www/ssh_debug.log', $output, FILE_APPEND);

        // Check if there's any output on stderr
        if (strpos($output, 'sudo: ') !== false) {
            throw new Exception('Failed to execute SSH command');
        }

        // Return the output
        return $output;
    } catch (Exception $e) {
        // Handle the exception
        file_put_contents('/var/www/ssh_debug.log', 'Error: ' . $e->getMessage(), FILE_APPEND);
        return 'Error: ' . $e->getMessage();
    }
}

// Call the executeRmCommand function
$result = executeRmCommand();

// Output the result
echo $result;
?>
