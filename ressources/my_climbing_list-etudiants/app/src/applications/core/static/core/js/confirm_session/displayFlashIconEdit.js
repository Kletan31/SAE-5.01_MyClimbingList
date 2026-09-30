/**
 * Supprime les icônes flash de la page lorsque le client ne peut pas modifier ce champ.
 */
// noinspection JSUnusedGlobalSymbols
export function displayFlashIconEdit() {
    document.querySelectorAll('.route-item').forEach(routeItem => {
        // Récupérer l'état de 'flash_available' dans sessionStorage
        const routeId = routeItem.dataset.routeId;
        const flashAvailableKey = `flash_available_${routeId}`;
        const flashAvailable = sessionStorage.getItem(flashAvailableKey);

        if (flashAvailable === 'false') {
            // Supprimer les containers flash associés
            removeFlashContainers(routeItem);
        }

        if (flashAvailable === null) {
            let pastTry = 0;
            const pastTryElements = routeItem.querySelectorAll('.past-try');

            pastTryElements.forEach(element => {
                const firstSpan = element.querySelector('span');
                const value = +firstSpan.textContent;
                pastTry += value;
            });

            if (pastTry !== 0) {
                // Supprimer les containers flash associés
                removeFlashContainers(routeItem);
            }
        }
    });
}

// Fonction utilitaire pour supprimer les containers flash associés à un élément routeItem
function removeFlashContainers(routeItem) {
    const flashContainers = routeItem.querySelectorAll('.flashContainer');
    flashContainers.forEach(flashContainer => {
        flashContainer.remove();
    });
}