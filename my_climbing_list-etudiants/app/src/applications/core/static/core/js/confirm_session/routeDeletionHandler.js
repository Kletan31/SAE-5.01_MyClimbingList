// === Initialisation des boutons de suppression pour les ouvertures ===
// noinspection JSUnusedGlobalSymbols
export function initializeDeleteButtons() {
    document.querySelectorAll('.delete-button').forEach((button) => {
        button.addEventListener('click', () => {
            const routeId = button.value;
            deleteRoute(routeId);
        });
    });
}

// Fonction pour gérer la suppression d'une ouverture sélectionnée
function deleteRoute(routeId) {
    // Supprime l'élément de la page
    const routeItem = document.querySelector(`.route-item[data-route-id="${routeId}"]`);
    if (routeItem) routeItem.remove();

    // Met à jour la liste des ouvertures dans sessionStorage
    const routesOrder = sessionStorage.getItem('routesOrder');
    let selectedRoutes = stringToArray(routesOrder);
    selectedRoutes = selectedRoutes.filter(id => id !== routeId);
    sessionStorage.setItem('routesOrder', selectedRoutes.join(','));

    // Supprime les données spécifiques de l'ouverture supprimée de sessionStorage (inclut les champs 'lead' si présents)
    const storedKeys = [
        `nb_try_${routeId}`,
        `nb_top_${routeId}`,
        `flash_${routeId}`,
        `nb_try_${routeId}_lead`,
        `nb_top_${routeId}_lead`,
        `flash_${routeId}_lead`
    ];

    // Supprimer chaque clé stockée dans sessionStorage pour cette ouverture
    storedKeys.forEach(key => sessionStorage.removeItem(key));
}