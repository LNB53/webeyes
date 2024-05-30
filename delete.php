<?php
// Function to execute the rm command via SSH
function executeRmCommand($password) {
    try {
        // SSH credentials for the remote server
        $ssh_host = '10.0.0.40';
        $ssh_user = 'user';
        $remote_file = '/home/user/rm/file.zip'; // Path to the file to delete on the remote server

        // SSH command to execute the rm command with sudo and read the password from standard input
        $command = "echo \"$password\" | sudo -S ssh $ssh_user@$ssh_host 'rm -f $remote_file' 2>&1";

        // Execute the SSH command
        $output = shell_exec($command);

        // Check if the command was successful
        if ($output === null) {
            throw new Exception('Failed to execute SSH command');
        }

        // Return the output
        return $output;
    } catch (Exception $e) {
        // Handle the exception
        return 'Error: ' . $e->getMessage();
    }
}

// Call the executeRmCommand function with the password
$password = 'VMware123!';
$result = executeRmCommand($password);

// Output the result
echo $result;
?>
