/**
 * Réinitialise sessionStorage à son état d'origine si le client décide de revenir en arrière.
 * Autrement dit, ne pas prendre en compte les intéractions avec le topo dans le cas d'un retour arrière.
 */
// noinspection JSUnusedGlobalSymbols
export function manageSessionStorage() {
    // Sauvegarde initiale de sessionStorage
    let sessionStorageBackup = {};
    backupSessionStorage(sessionStorageBackup);

    // Ajouter un écouteur sur le lien pour restaurer sessionStorage avant la redirection
    const backLink = document.getElementById('backLink');
    if (backLink) {
        backLink.addEventListener('click', (event) => {
            event.preventDefault(); // Empêche la redirection immédiate
            restoreSessionStorage(sessionStorageBackup); // Restaure sessionStorage
            window.location.href = backLink.href; // Redirige vers la page
        });
    }
}

function backupSessionStorage(sessionStorageBackup) {
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        sessionStorageBackup[key] = sessionStorage.getItem(key);
    }
}

function restoreSessionStorage(sessionStorageBackup) {
    sessionStorage.clear(); // Vide sessionStorage avant de restaurer
    for (const key in sessionStorageBackup) {
        sessionStorage.setItem(key, sessionStorageBackup[key]);
    }
}