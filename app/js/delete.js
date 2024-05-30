$(document).ready(function() {
    // When the removeButton is clicked
    $('#removeButton').on('click', function() {
        // Display confirmation dialog
        if (confirm("Are you sure you want to delete?")) {
            // If user confirms, send an AJAX request to execute the PHP script
            $.ajax({
                url: '../delete.php', // URL of your PHP script
                type: 'POST',
                success: function(response) {
                    // Handle success response
                    console.log('Application stopped successfully:', response);
                    alert('Application stopped successfully!');
                },
                error: function(xhr, status, error) {
                    // Handle error response
                    console.error('Error executing script:', error);
                    alert('Error executing script!');
                }
            });
        } else {
            // If user cancels, do nothing
            console.log('Deletion cancelled by user.');
        }
    });
});
