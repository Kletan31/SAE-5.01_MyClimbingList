// noinspection JSUnusedGlobalSymbols
export function sendPostRequest() {
    // Sélectionne le formulaire et l'élément déclencheur
    const form = document.getElementById("details-form");
    const editLink = document.getElementById("editLink");

    // Soumet le formulaire
    editLink.addEventListener("click", function () {
        preloadView(); // Affiche le spinner d’abord

        requestAnimationFrame(() => {
            setTimeout(() => {
                form.submit();
            }, 50); // Attente minimale pour que le DOM rende le spinner
        });
    });
}