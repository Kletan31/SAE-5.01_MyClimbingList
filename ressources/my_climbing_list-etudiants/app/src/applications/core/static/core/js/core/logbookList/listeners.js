/**
 * Initialise la logique des volets.
 */
// noinspection JSUnusedGlobalSymbols
function initializeRowContainerListeners() {
    const scrollableContainer = document.querySelector('.scrollable-container');
    if (!scrollableContainer) { return }

    const listContainers = document.querySelectorAll('.list-container');

    listContainers.forEach(listContainer => {
        const mainRow = listContainer.querySelectorAll('.main-row');
        const lastMainRow = mainRow[mainRow.length - 1];

        const dropdownHeight = calculateDropdownHeight();

        mainRow.forEach(rowContainer => {
            const details = rowContainer.nextElementSibling;

            rowContainer.addEventListener('click', () => {
                // Cas particulier du dernier volet
                if (rowContainer === lastMainRow) {
                    toggleDropdown(details, listContainer, dropdownHeight, scrollableContainer)
                }
                // Fermeture du volet
                else if (details.classList.contains('open')) {
                    details.classList.remove('open');
                }
                // Ouverture du volet
                else {
                    details.classList.add('open');
                }
            });
        });
    })

    // Ajustement des bordures
    initializeTogglerScrollableClass();

    // Mise à jour à chaque redimensionnement
    window.addEventListener("resize", initializeTogglerScrollableClass);
}

/**
 * Gestion manuelle de l'ouverture du dernier volet. Le comportement natif est disgracieux. (Ouverture en-dehors de la
 * zone visible, nécessitant une action de défilement non-intuitive du client)
 */
function toggleDropdown(details, listContainer, dropdownHeight, scrollableContainer) {
    // Fermeture du volet
    if (details.classList.contains('open')) {
        details.classList.remove('open');
    }
    // Ouverture du volet
    else {
        // Ajuste la hauteur du conteneur pour permettre le defilement avec `smoothScrollTo`
        const originalHeight = listContainer.offsetHeight;
        const newHeight = originalHeight + dropdownHeight;
        listContainer.style.height = `${newHeight}px`;
        // Ouvre le volet
        details.classList.add('open');
        // Animation (transition: height .3s ease;)
        smoothScrollTo(scrollableContainer, 300);
        // Rendre la main au navigateur sur la hauteur
        listContainer.style.height = `auto`;
    }
}

/**
 * Ne pas afficher la dernière bordure basse dans le cas où le défilement est possible, pour des raisons d'élégance.
 */
function initializeTogglerScrollableClass() {
    const scrollableContainer = document.querySelector(".scrollable-container");
    const listContainer = document.querySelector(".list-container:not(.d-none)");

    // Vérifie que les deux éléments existent avant de poursuivre
    if (!scrollableContainer || !listContainer) {
        return;
    }

    if (scrollableContainer.scrollHeight > scrollableContainer.clientHeight) {
        // Conteneur scrollable : suppression de la bordure inférieure
        listContainer.classList.add("scrollable");
    } else {
        // Conteneur non-scrollable : ajout de la bordure inférieure
        listContainer.classList.remove("scrollable");
    }
}

// Attacher les fonctions à window pour un accès global
window.initializeRowContainerListeners = initializeRowContainerListeners;
window.initializeTogglerScrollableClass = initializeTogglerScrollableClass;