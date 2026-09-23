// Initialise la logique du changement de langue
// noinspection JSUnusedGlobalSymbols
export function initializeLanguageButton() {
    const languageButton = document.getElementById('language-button');
    const popupOverlay = document.getElementById('language-popup-overlay');
    const popupContainer = document.getElementById('language-popup-container');

    if (!languageButton || !popupOverlay || !popupContainer) return;

    // Affiche la popup au clic sur le bouton "langue"
    languageButton.addEventListener('click', () => popupOverlay.classList.add('active'));

    // Ferme la popup si on clique en dehors du conteneur
    popupOverlay.addEventListener('click', (event) => {
        if (!popupContainer.contains(event.target)) {
            popupOverlay.classList.remove('active');
        }
    });
}