function sendViewportDimensions() {
    const viewportHeight = window.innerHeight; // Obtenir la hauteur actuelle du viewport
    const viewportWidth = window.innerWidth;   // Obtenir la largeur actuelle du viewport

    const previousHeight = localStorage.getItem('viewportHeight'); // Récupérer la hauteur précédente
    const previousWidth = localStorage.getItem('viewportWidth');   // Récupérer la largeur précédente

    // Vérifier si la hauteur ou la largeur a changé
    if (viewportHeight !== parseInt(previousHeight, 10) || viewportWidth !== parseInt(previousWidth, 10)) {
        // Stocker les nouvelles dimensions dans localStorage
        localStorage.setItem('viewportHeight', viewportHeight.toString());
        localStorage.setItem('viewportWidth', viewportWidth.toString());

        // Envoyer les nouvelles dimensions au serveur
        fetch('/set-viewport-dimensions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Inclure le CSRF token
            },
            body: JSON.stringify({ vh: viewportHeight, vw: viewportWidth }) // Envoyer hauteur et largeur
        })
        .then(response => {
            if (!response.ok) {
                // Journaliser une erreur si la réponse n'est pas correcte
                console.error(`Erreur serveur : ${response.status} - ${response.statusText}`);
                return response.text().then(errorMessage => {
                    console.error(`Détails : ${errorMessage}`);
                });
            } else {
                if (LOG) console.log("Dimensions du viewport mises à jour avec succès !");
            }
        })
        .catch(error => {
            // Journaliser une erreur réseau
            console.error("Erreur réseau lors de l'envoi des dimensions du viewport :", error);
        });
    }
}

// Initialisation : exécuter la fonction au premier chargement
sendViewportDimensions();

// Surveiller les changements de taille de l'écran
window.addEventListener('resize', sendViewportDimensions);