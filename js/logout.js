function logout() {
    localStorage.removeItem('accesToken');
    // Redirect to the login page
    window.location.href = "login.html";
}