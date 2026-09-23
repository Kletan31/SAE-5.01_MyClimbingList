// noinspection JSUnusedGlobalSymbols
export function updateHiddenInputFromSession() {
    const form = document.getElementById('confirmSessionForm');
    const saveButton = document.querySelector('#save-button-container button');
    const routesOrderInput = document.getElementById('routesOrder');

    saveButton.addEventListener('click', () => {

        // Met à jour la valeur de l'input caché avec les données de sessionStorage
        const sessionData = sessionStorage.getItem('routesOrder');
        routesOrderInput.value = sessionData || ''; // Assure une valeur par défaut

        // Soumet le formulaire
        preloadView(); // Affiche le spinner d’abord

        requestAnimationFrame(() => {
            setTimeout(() => {
                form.submit();
            }, 50); // Attente minimale pour que le DOM rende le spinner
        });
    });
}