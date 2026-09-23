// Restaure la position de défilement depuis sessionStorage
function restoreScrollPosition(scrollContainer) {
    const isBloc = document.getElementById('bloc-tab')?.classList.contains('selected') || false;
    if (isBloc) {
        scrollContainer.scrollTop = +sessionStorage.getItem('scrollBlocPosition') || 0;
    } else {
        scrollContainer.scrollTop = +sessionStorage.getItem('scrollVoiePosition') || 0;
    }
}

// Attacher la fonction à window pour un accès global
window.restoreScrollPosition = restoreScrollPosition;