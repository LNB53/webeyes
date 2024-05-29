document.getElementById('password-change-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Get the current and new passwords from input fields
    const currentPassword = document.getElementById('login-password').value;
    const newPassword = document.getElementById('new-password').value;

    // Retrieve JWT token from local storage
    const accessToken = localStorage.getItem('accessToken');

    try {
        // Send a request to change the password
        const response = await fetch('http://127.0.0.1:8080/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}` // Include the JWT token in the Authorization header
            },
            body: JSON.stringify({
                old_password: currentPassword,
                new_password: newPassword
            })
        });

        if (response.ok) {
            const responseData = await response.json();
            alert(responseData.message); // Display success message
            // Redirect the user to the home page or any other appropriate page
            window.location.href = "index.html";
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error: Could not connect to the server. Please try again later.');
    }
});
