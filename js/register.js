document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }
    
    // Function to hash the password using CryptoJS
    function hashPassword(password) {
        return CryptoJS.SHA512(password).toString(CryptoJS.enc.Hex);
    }
    
    const hashedPassword = hashPassword(password);
    
    try {
        const response = await fetch('http://10.0.0.124:8080/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mail: email, password: hashedPassword })
        });
        
        if (response.ok) {
            alert("User registered successfully!");
            document.getElementById('registerForm').reset(); // Reset the form after successful registration
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred during registration. Please try again.');
    }
});
