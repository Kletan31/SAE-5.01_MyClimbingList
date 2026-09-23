function relaisLogic(isBloc, scrollContainer) {
    const circles = document.querySelectorAll("#voie circle, #bloc circle");

    // Ajout des événements de clic sur chaque relais
    circles.forEach((circle) => {
        circle.parentElement.addEventListener("click", () => {
            // Désactive tous les relais
            resetCircles(circles);

            // Met à jour les lignes du tableau et active le relais sélectionné
            activateElementAndUpdateRows(circle.parentElement.id);

            // Stocker l'ID du relais cliqué
            const storageKey = circle.parentElement.id[0] === "S" ? 'active-secteur' : 'active-relais';
            sessionStorage.setItem(storageKey, circle.parentElement.id);

            // Ramener le tableau à la position initiale
            scrollContainer.scrollTop = 0;
        });
    });

    // Initialisation des ouvertures affichées dans le tableau
    if (circles.length > 0) {
        isBloc && activateElementAndUpdateRows(sessionStorage.getItem("active-secteur"));
        !isBloc && activateElementAndUpdateRows(sessionStorage.getItem("active-relais"));
    }
}

// Attacher la fonction à window pour un accès global
window.relaisLogic = relaisLogic;