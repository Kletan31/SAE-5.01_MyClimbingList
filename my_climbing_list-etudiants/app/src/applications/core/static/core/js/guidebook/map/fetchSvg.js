async function fetchSVG() {
    try {
        // Récupérer la variable salle_id
        const salleId = document.querySelector('meta[name="salle_id"]').content;

        // Charger et parse le SVG
        const svgUrl = `/static/core/media/map/${salleId}.svg`;
        const svgElement = await loadAndParseSVG(svgUrl);

        // Ajouter le SVG dans le conteneur approprié
        const mapContainer = document.getElementById('map');
        mapContainer.appendChild(svgElement);

    } catch (error) {
        console.error('Erreur lors du chargement du SVG :', error);
    }
}

/**
 * Charge et parse le fichier SVG.
 */
async function loadAndParseSVG(svgUrl) {
    const response = await fetch(svgUrl);
    const svgText = await response.text();

    const parser = new DOMParser();
    const svgDocument = parser.parseFromString(svgText, "image/svg+xml");
    return svgDocument.documentElement;
}

// Attacher la fonction à window pour un accès global
window.fetchSVG = fetchSVG;