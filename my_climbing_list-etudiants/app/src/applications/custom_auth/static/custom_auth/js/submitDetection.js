// noinspection JSUnusedGlobalSymbols
export function initializeAuthFormSubmission() {
    const forms = document.querySelectorAll(".auth-form-container form");

    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Empêche la soumission immédiate (évite les conflits)
            preloadView(); // Affiche le spinner d’abord

            requestAnimationFrame(() => {
                setTimeout(() => {
                    form.submit();
                }, 50); // Attente minimale pour que le DOM rende le spinner
            });
        });
    });
}