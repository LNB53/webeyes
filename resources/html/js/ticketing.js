document.getElementById('ticketing').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    const webhookURL = 'https://discord.com/api/webhooks/1244546643546734646/4tnrRTmlqXPOwXlIO7J9xV4C7QFhYnm1XVNTtXGS2QAi6l7EiPKJKhi63LlR1YP1PbZK';

    const timestamp = Date.now();
    const randomNum = Math.floor(Math.random() * 9);
    const ticketID = `WE-${timestamp}-${randomNum}`;

    const ticketform = {
        content: `-----\n**Ticket ID:** ${ticketID}\n**New Ticket Created by**: ${email}\n**Subject**: ${subject}\n**Message**: ${message}`
    };

    document.getElementById('ticketing').reset();
    fetch(webhookURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(ticketform)
    })
    .then(response => {
        if (response.ok) {
            alert('Ticket submitted successfully!');
        } else {
            alert('Error submitting ticket.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting ticket.');
    });
});
