function initializePinchZoom() {
    // Récupérer l'élément cible
    const mapElement = document.getElementById('map');

    // Initialiser PinchZoom sur l'élément
    new PinchZoom(mapElement, {
        draggableUnzoomed: true,    // Permet de glisser même si non zoomé
        minZoom: 0.5,               // Zoom minimum
        maxZoom: 10,                // Zoom maximum
    });
}

// Attacher la fonction à window pour un accès global
window.initializePinchZoom = initializePinchZoom;