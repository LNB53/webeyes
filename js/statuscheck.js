const express = require('express');
const app = express();

// Middleware to set CORS headers
app.use((req, res, next) => {
    // Allow requests from specified IP addresses
    const allowedOrigins = ['http://10.0.0.124', 'http://10.0.0.40'];
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
    }
    // Allow other necessary CORS headers
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

// Your other routes and middleware here

const ipAddress = 'http://10.0.0.40:8081';

function checkWebsiteAndUpdateStatus(url, statusElementId) {
    fetch(url)
        .then(response => {
            if (response.ok) {
                document.getElementById(statusElementId).innerHTML = '<div class="p-1 rounded inline-block mr-2 bg-green-700">Started</div>';
            } else {
                document.getElementById(statusElementId).innerHTML = '<div class="p-1 rounded inline-block mr-2 bg-yellow-400">Starting</div>';
            }
        })
        .catch(error => {
            document.getElementById(statusElementId).innerHTML = '<div class="p-1 rounded inline-block mr-2 bg-yellow-400">Starting</div>';
        });
}

// Call the function initially for Application 1
checkWebsiteAndUpdateStatus(ipAddress, 'status1');

// Continuously check the status every 5 seconds
setInterval(function() {
    checkWebsiteAndUpdateStatus(ipAddress, 'status1');
}, 5000); // 5000 milliseconds = 5 seconds

// Add event listener to the button to open the IP address
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('openIpButton').addEventListener('click', function() {
        window.open(ipAddress, '_blank');
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});
