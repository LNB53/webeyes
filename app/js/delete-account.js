document.getElementById('yeetus-deletus-btn').addEventListener('click', async function(event) {
    event.preventDefault();

    // Get user confirmation
    const confirmDelete = confirm("Are you sure you want to delete your account? This action cannot be undone.");

    if (confirmDelete) {
        // Retrieve JWT token from local storage
        const accessToken = localStorage.getItem('accessToken');
        
        // Decode the JWT to extract the user's email
        const email = parseJwt(accessToken).mail;

        try {
            // Send a request to delete the account
            const response = await fetch('http://10.0.0.124:8080/yeetus-deletus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}` // Include the JWT token in the Authorization header
                },
                body: JSON.stringify({mail: email})
            });

            if (response.ok) {
                const responseData = await response.json();
                alert(responseData.message); // Display success message
                // Redirect the user to the home page
                window.location.href = "index.html";
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error: Could not connect to the server. Please try again later.');
        }
    }
});

// Function to decode JWT token
function parseJwt(token) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
}
