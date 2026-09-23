// Attacher la constante à window pour un accès global
const graphData = {};
window.graphData = graphData;

// Attacher la fonction à window pour un accès global
function loadGraphData() {
    const ids = [
        'progression-voie-graph-data',
        'progression-bloc-graph-data',
        'ascension-voie-graph-data',
        'ascension-bloc-graph-data',
        'ascension-voie-flash-graph-data',
        'ascension-bloc-flash-graph-data',
        'profil-voie-graph-data',
        'profil-bloc-graph-data',
        'style-voie-graph-data',
        'style-bloc-graph-data'
    ];

    ids.forEach(id => {
        const element = document.getElementById(id);
        if (element && element.textContent.trim()) {  // Vérifie si l'élément existe et s'il contient du texte non vide
            graphData[id] = JSON.parse(element.textContent);
        }
    });
}
window.loadGraphData = loadGraphData;