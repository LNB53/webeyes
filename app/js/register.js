document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password.length < 6) {
        alert("Password should be at least 6 characters long.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // http://10.0.0.124:8080
    const response = await fetch('http://10.0.0.124:8080/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mail: email, password: password })
    });

    if (response.ok) {
        alert("User registered successfully!");
        document.getElementById('registerForm').reset(); // Reset the form after successful registration
        window.location.href = "login.html"; // Redirect to login page
    } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
    }
});