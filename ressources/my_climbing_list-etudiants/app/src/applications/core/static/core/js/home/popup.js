document.addEventListener("DOMContentLoaded", function () {
    // On récupère l'élément DOM de la popup
    const modalElement = document.getElementById('updatePopup');

    // Si la popup n'existe pas dans le HTML, on arrête le script ici.
    if (!modalElement) return;

    // Affichage de la popup
    modalElement.style.display = 'block';  // Rendre visible la popup
    modalElement.classList.add('show');  // Appliquer l'animation d'opacité

    // Fonction utilitaire pour fermer la popup
    function closeModal() {
        modalElement.classList.remove('show');  // Enlève la classe qui gère l'opacité
        modalElement.style.display = 'none';  // Cache la modale
    }

    // On récupère le bouton de confirmation
    const confirmButton = document.getElementById('popup-confirm');

    // On envoie une requête POST au serveur après le clique sur le bouton de confirmation
    if (confirmButton) {
        confirmButton.addEventListener('click', function () {
            fetch('/mark_popup_seen/', {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
            }).finally(() => {
                // Vide le cache de la page principale
                if (navigator.serviceWorker && navigator.serviceWorker.controller) {
                    navigator.serviceWorker.controller.postMessage({ action: "CLEAR_HOME_CACHE" });
                }

                // Ferme la popup
                closeModal();
            });
        });
    }
});