// noinspection JSUnusedGlobalSymbols
export function initVoiesSelection() {
    // === Initialisation des données ===
    const routesOrder = sessionStorage.getItem('routesOrder') || '';
    let selectedRoutes = stringToArray(routesOrder);

    // Champs du formulaire
    const form = document.getElementById('guidebook-form');
    const routesOrderField = document.getElementById('routesOrder');
    const addButton = document.querySelector('#add-button-container button');

    // Mettre à jour la valeur initiale du champ de formulaire
    routesOrderField.value = selectedRoutes.join(',');

    // === Fonctions Utilitaires ===

    /**
     * Supprime les données associées à une voie dans le sessionStorage.
     * @param {string} routeId - Identifiant de la voie.
     */
    function removeRouteData(routeId) {
        sessionStorage.removeItem(`nb_try_${routeId}`);
        sessionStorage.removeItem(`nb_top_${routeId}`);
        sessionStorage.removeItem(`flash_${routeId}`);
    }

    /**
     * Met à jour la liste des voies sélectionnées dans le champ et le sessionStorage.
     */
    function updateRoutesOrder() {
        routesOrderField.value = selectedRoutes.join(','); // Formulaire
        sessionStorage.setItem('routesOrder', selectedRoutes.join(',')); // SessionStorage
        updateButtonState();
    }

    /**
     * Met à jour l'état du bouton en fonction des sélections.
     */
    function updateButtonState() {
        const hasSelection = selectedRoutes.length > 0;

        if (hasSelection) {
            addButton.classList.remove('d-none');
            addButton.addEventListener('click', submitForm);
        } else {
            addButton.classList.add('d-none');
            addButton.removeEventListener('click', submitForm);
        }
    }

    // Fonction référencer pour soumettre le formulaire (nécessaire pour utiliser removeEventListener)
    function submitForm() {
        preloadView(); // Affiche le spinner d’abord

        requestAnimationFrame(() => {
            setTimeout(() => {
                form.submit();
            }, 50); // Attente minimale pour que le DOM rende le spinner
        });
    }

    /**
     * Gère la sélection/désélection d'une ligne.
     * @param {HTMLElement} row - Ligne de tableau cliquée.
     */
    function handleRowSelection(row) {
        const routeId = row.dataset.id;
        const isSelected = selectedRoutes.includes(routeId);

        if (isSelected) {
            // Désélectionner la ligne
            row.classList.remove('selected-row');
            removeRouteData(routeId);
            selectedRoutes = selectedRoutes.filter(id => id !== routeId);
        } else {
            // Sélectionner la ligne
            row.classList.add('selected-row');
            selectedRoutes.push(routeId);
        }

        updateRoutesOrder();
    }

    // === Initialisation de l'affichage ===

    // Marquer les lignes déjà sélectionnées
    selectedRoutes.forEach(routeId => {
        const tableRow = document.querySelector(`.selectable-row[data-id="${routeId}"]`);
        if (tableRow) {
            tableRow.classList.add('selected-row');
        }
    });

    updateButtonState(); // Met à jour l'état initial du bouton

    // === Ajout des écouteurs d'événements ===

    document.querySelectorAll('.selectable-row').forEach(row => {
        row.addEventListener('click', () => handleRowSelection(row));
    });
}