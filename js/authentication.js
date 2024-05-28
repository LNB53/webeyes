    // Function to check if user is authenticated
function isAuthenticated() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        return false;
    }

    try {
        // Decode the token payload to check expiration (optional)
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp;
        const currentTime = Math.floor(Date.now() / 1000);

        if (currentTime > exp) {
            localStorage.removeItem('accessToken'); // Remove expired token
            return false;
        }

        return true;
    } catch (error) {
        console.error('Error decoding token:', error);
        return false;
    }
}

// Function to redirect to login page if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

// Check authentication on page load
window.onload = requireAuth; 