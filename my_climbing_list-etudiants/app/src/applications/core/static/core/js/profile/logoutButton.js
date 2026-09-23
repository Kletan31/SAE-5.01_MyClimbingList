// Initialise la logique de déconnexion
// noinspection JSUnusedGlobalSymbols
export function initializeLogoutButton() {
    const logoutButton = document.getElementById('logout-button');
    const popupOverlay = document.getElementById('popup-overlay');
    const popupContainer = document.getElementById('popup-container');
    const cancelLogout = document.getElementById('cancel-logout');

    // Ajouter la classe "active" au clic sur le bouton logout
    logoutButton.addEventListener('click', () => popupOverlay.classList.add('active'));

    // Supprimer la classe "active" en cliquant sur le bouton cancel
    cancelLogout.addEventListener('click', () => popupOverlay.classList.remove('active'));

    // Supprimer la classe "active" en cliquant en dehors de la popup-container
    popupOverlay.addEventListener('click', (event) => {
        if (!popupContainer.contains(event.target)) {
            popupOverlay.classList.remove('active');
        }
    });
}