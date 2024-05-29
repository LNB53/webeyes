document.addEventListener("DOMContentLoaded", function() {
    // Function to decode JWT token
    function decodeJwtToken(token) {
        const payloadBase64 = token.split('.')[1];
        const payload = JSON.parse(atob(payloadBase64));
        return payload;
    }

    // Get the JWT token from localStorage
    const token = localStorage.getItem("accessToken");

    if (token) {
        try {
            // Decode the JWT token
            const decodedToken = decodeJwtToken(token);

            // Get the email from the decoded token
            const userEmail = decodedToken.mail;

            // Replace the placeholder email with the actual email
            const emailPlaceholder = document.getElementById("email-placeholder");
            if (emailPlaceholder) {
                emailPlaceholder.innerText = userEmail;
            }
        } catch (error) {
            console.error("Error decoding JWT token:", error);
        }
    } else {
        console.error("JWT token not found in localStorage");
    }
});