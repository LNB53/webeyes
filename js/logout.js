function logout() {
    localStorage.removeItem('user');
    // Redirect to the login page or any other appropriate page
    window.location.href = "login.html";
}