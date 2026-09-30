// Gère la sauvegarde et la restauration de la position de défilement pour un conteneur spécifique.
// noinspection JSUnusedGlobalSymbols
export function initializeScrollPositionManager() {
    const scrollContainer = document.querySelector('.scrollable-container');
    const tabSwitcherButton = document.getElementById('bloc-tab');
    const listIcon = document.querySelector('.fa-list-ul');

    // Restaure la position de défilement
    restoreScrollPosition(scrollContainer);

    // Écoute les changements de position de défilement pour sauvegarder la position
    scrollContainer.addEventListener('scroll', () => {
        const isBloc = tabSwitcherButton?.classList.contains('selected') || false; // True → dans l'onglet bloc
        const isList = listIcon.classList.contains('d-none'); // True → dans l'onglet list
        isList && isBloc && sessionStorage.setItem('scrollBlocPosition', scrollContainer.scrollTop.toString());
        isList && !isBloc && sessionStorage.setItem('scrollVoiePosition', scrollContainer.scrollTop.toString());
    });
}