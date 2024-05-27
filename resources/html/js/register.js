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

    // Function to hash the password
    async function hashPassword(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hash = await crypto.subtle.digest('SHA-512', data);
        return Array.from(new Uint8Array(hash)).map(byte => byte.toString(16).padStart(2, '0')).join('');
    }
    const hashedPassword = await hashPassword(password);

    const response = await fetch('http://localhost:8080/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mail: email, password: hashedPassword })
    });

    if (response.ok) {
        alert("User registered successfully!");
    } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
    }
});