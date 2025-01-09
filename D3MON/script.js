async function sendQuery(query) {
    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = 'Loading...';

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        const data = await response.json();
        responseDiv.innerHTML = data.message;
    } catch (error) {
        responseDiv.innerHTML = 'Error: ' + error;
    }
}
