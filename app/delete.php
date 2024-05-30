<?php
// Function to execute the necessary commands via SSH
function executeDockerCommand() {
    try {
        // SSH credentials for the remote server
        $ssh_host = '10.0.0.40';
        $ssh_user = 'user';  // Remote server user
        $docker_compose_file = '/home/user/app/docker-compose.yaml'; // Path to the docker-compose.yaml file
        $docker_compose_down_command = "cd /home/user/app && docker compose down";
        $remove_command = "cd /home/user/app && sudo rm -f docker-compose.yaml";

        // SSH command to execute docker-compose down
        $command = "ssh -o StrictHostKeyChecking=no -i /var/www/.ssh/id_rsa $ssh_user@$ssh_host \"$docker_compose_down_command\" 2>&1";

        // Execute docker-compose down
        $output = shell_exec($command);

        // Log the output for debugging purposes
        file_put_contents('/var/www/ssh_debug.log', $output, FILE_APPEND);

        // Check if there's any output on stderr
        if (strpos($output, 'sudo: ') !== false) {
            throw new Exception('Failed to execute SSH command');
        }

        // SSH command to remove docker-compose.yaml
        $command = "ssh -o StrictHostKeyChecking=no -i /var/www/.ssh/id_rsa $ssh_user@$ssh_host \"$remove_command\" 2>&1";

        // Execute the remove command
        $output = shell_exec($command);

        // Log the output for debugging purposes
        file_put_contents('/var/www/ssh_debug.log', $output, FILE_APPEND);

        // Check if there's any output on stderr
        if (strpos($output, 'sudo: ') !== false) {
            throw new Exception('Failed to execute SSH command');
        }

        // Return success message
        return 'Successfully executed Docker commands';
    } catch (Exception $e) {
        // Handle the exception
        file_put_contents('/var/www/ssh_debug.log', 'Error: ' . $e->getMessage(), FILE_APPEND);
        return 'Error: ' . $e->getMessage();
    }
}

// Call the executeDockerCommand function
$result = executeDockerCommand();

// Output the result
echo $result;
?>
