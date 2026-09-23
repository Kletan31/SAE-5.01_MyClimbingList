// hideProfileLink.js — compatible i18n (utilise slice(4) pour ignorer le code langue)

document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("profile-container-js");
    if (!container) return;

    // Supprime le code langue (/fr/, /en/, etc.)
    const stripLang = (path) => path.slice(4);

    const currentPath = stripLang(window.location.pathname);

    // Pages sur lesquelles le lien profil ne doit pas apparaître
    const hideProfileLink = [
        "core/settings/",
        "core/feedback/",
        "core/profile/",
    ];

    // Affiche le lien profil si la page actuelle n’est pas dans la liste
    if (!hideProfileLink.includes(currentPath)) {
        container.classList.remove("d-none");
    }
});