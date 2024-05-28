function logout() {
    localStorage.removeItem('accestoken');
    // Redirect to the login page
    window.location.href = "login.html";
}