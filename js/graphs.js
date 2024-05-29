document.addEventListener("DOMContentLoaded", function() {
    const apiEndpoint = 'http://10.0.0.50/api/v0/devices/10.0.0.20/graphs/';
    const apiToken = '7ac7e07e586ff6aae659c5c516ca1343';

    // Function to fetch graph data
    async function fetchGraphData() {
        try {
            const response = await fetch(apiEndpoint, {
                headers: {
                    'X-Auth-Token': apiToken
                }
            });
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }

    // Function to display graphs
    async function displayGraphs() {
        const graphData = await fetchGraphData();
        if (!graphData) return;

        const systemUptimeGraph = graphData.graphs.find(graph => graph.name === 'device_uptime');
        const processorUsageGraph = graphData.graphs.find(graph => graph.name === 'device_ucd_cpu');

        if (systemUptimeGraph) {
            const systemUptimeUrl = `${apiEndpoint}${systemUptimeGraph.name}?auth_token=${apiToken}`;
            document.getElementById('systemUptimeGraph').src = systemUptimeUrl;
        }

        if (processorUsageGraph) {
            const processorUsageUrl = `${apiEndpoint}${processorUsageGraph.name}?auth_token=${apiToken}`;
            document.getElementById('processorUsageGraph').src = processorUsageUrl;
        }
    }

    // Display the graphs when the page loads
    displayGraphs();
});
