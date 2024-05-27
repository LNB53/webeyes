document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    document.getElementById('registerForm').reset();

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    const response = await fetch('http://localhost:8080/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mail: email, password: password })
    });

    if (response.ok) {
        alert("User registered successfully!");
    } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
    }
});