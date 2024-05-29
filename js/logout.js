document.getElementById('logoutButton').addEventListener('click', function() {
    // Remove items from localStorage
    localStorage.clear();

    // Redirect to login page
    window.location.href = "login.html";
});
