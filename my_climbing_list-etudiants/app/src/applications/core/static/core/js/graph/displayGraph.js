function displayGraph() {
    // Déterminer les paramètres sélectionnés par l'utilisateur
    const activeGraph = document.querySelector('.menu-bar-graph .selected').dataset.category;
    const activeType = document.querySelector('.menu-bar .selected').dataset.category;
    const isFlashMode = flashMode && activeGraph === 'ascension';
    const suffix = isFlashMode ? '-flash' : '';

    // Déterminer les IDs de conteneurs actifs
    const containerId = `${activeGraph}-${activeType}${suffix}`;
    const graphId = `${activeGraph}-${activeType}${suffix}-graph`;
    const dataKey = `${activeGraph}-${activeType}${suffix}-graph-data`;

    // Masquer tous les conteneurs
    const allContainers = document.querySelectorAll('.chart-container > div');
    allContainers.forEach(container => container.style.display = 'none');

    // Afficher le conteneur actif
    const activeContainer = document.getElementById(containerId);
    if (activeContainer) activeContainer.style.display = 'flex';

    // Charger les données du graphique actif depuis graphData
    const activeData = graphData[dataKey];
    if (activeData) {
        const plotContainer = document.getElementById(graphId);
        Plotly.newPlot(plotContainer, activeData.data, activeData.layout, {
            displayModeBar: false,        // Masquer la barre d'outils
            staticPlot: true,             // Désactive toutes les interactions (zoom, autoscale, etc.)
            responsive: true              // Permet au graphique de s'adapter dynamiquement
        });
    }
}

// Attacher la fonction à window pour un accès global
window.displayGraph = displayGraph;