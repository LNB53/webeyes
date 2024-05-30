const express = require('express');
const fetch = require('node-fetch');
const app = express();

const serverUrl = 'http://10.0.0.40:8081'; // Replace with the URL of your server

app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', 'http://10.0.0.124');
    res.setHeader('Access-Control-Allow-Methods', 'GET');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

app.get('/checkServerStatus', async (req, res) => {
    try {
        const response = await fetch(serverUrl);
        const status = response.ok ? 'Running' : 'Stopped';
        res.json({ status });
    } catch (error) {
        res.status(500).json({ error: 'Failed to check server status' });
    }
});

const PORT = 3000; // Port for the proxy server
app.listen(PORT, () => {
    console.log(`Proxy server listening on port ${PORT}`);
});
