function checkServerStatus() {
    fetch('http://10.0.0.124:3000/checkServerStatus')
        .then(response => {
            if (!response.ok) {
                throw new Error('Server is unreachable');
            }
            return response.json();
        })
        .then(data => {
            const status = data.status || 'Stopped';
            setStatus(status);
        })
        .catch(error => {
            console.error('Failed to check server status:', error);
            setStatus('Stopped');
        });
}


function setStatus(status) {
    const statusElement = document.getElementById('status1');
    statusElement.innerHTML = `
        <div class="flex items-center">
            <div class="p-1 rounded inline-block mr-2 ${status === 'Running' ? 'bg-green-700' : 'bg-red-700'}">${status}</div>
        </div>
    `;
}

// Check server status initially
checkServerStatus();

// Check server status every 5 seconds
setInterval(checkServerStatus, 5000);
