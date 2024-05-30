// delete.js

$(document).ready(function() {
    // When the removeButton is clicked
    $('#removeButton').on('click', function() {
        // Send an AJAX request to execute the PHP script
        $.ajax({
            url: '../delete.php', // URL of your PHP script
            type: 'POST',
            success: function(response) {
                // Handle success response
                console.log('Script executed successfully:', response);
                alert('Script executed successfully!');
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error('Error executing script:', error);
                alert('Error executing script!');
            }
        });
    });
});
