// noinspection JSUnusedGlobalSymbols
export function initializeCharts() {
    // == Récupérer les données du graphique ==
    const chartContainer = document.getElementById("ascension-graph");
    const chartData = JSON.parse(document.getElementById("ascension-graph-data").textContent);

    // == Initialiser le graphique ==
    Plotly.newPlot(chartContainer, chartData.data, chartData.layout, {
        displayModeBar: false,        // Masquer la barre d'outils
        staticPlot: true,             // Désactive toutes les interactions (zoom, autoscale, etc.)
        responsive: true              // Permet au graphique de s'adapter dynamiquement
    });
}