document.getElementById('loginform').addEventListener('submit', async function (event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8080/login', {
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
            const userData = await response.json();
            // Store user data in browser
            localStorage.setItem('user', JSON.stringify(userData.user.mail));
            window.location.href = "dashboard.html"; // Redirect to dashboard
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});
