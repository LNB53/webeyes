// Add an event listener to the Delete Account button
document.getElementById('yeetus-deletus-btn').addEventListener('click', async function(event) {
    event.preventDefault();

    // Get user confirmation
    const confirmDelete = confirm("Are you sure you want to delete your account? This action cannot be undone.");

    if (confirmDelete) {
        // Get user credentials
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            // Send a request to delete the account
            const response = await fetch('http://127.0.0.1:8080/yeetus-deletus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({mail: email, password: password})
            });

            if (response.ok) {
                const responseData = await response.json();
                alert(responseData.message); // Display success message
                // Redirect the user to the login page or home page
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
