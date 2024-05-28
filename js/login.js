document.getElementById('loginform').addEventListener('submit', async function (event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://10.0.0.124:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mail: email,
                password: password
            })
        });

        if (response.ok) {
            const responseData = await response.json();
            const accessToken = responseData.access_token;
            // Store token in localStorage
            localStorage.setItem('accessToken', accessToken);
            window.location.href = "dashboard.html"; // Redirect to dashboard
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    }
});
