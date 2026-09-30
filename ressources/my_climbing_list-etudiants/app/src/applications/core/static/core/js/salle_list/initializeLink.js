document.addEventListener('DOMContentLoaded', () => {
    // Ajouter un gestionnaire à toutes les icônes avec la classe .fa-circle-info
    document.querySelectorAll('.fa-chart-simple').forEach(icon => {
        icon.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation(); // ← empêche le <a> de capter l'événement

            // Récupérer l'identifiant de la salle depuis l'attribut data-salle-id
            const salleId = icon.getAttribute('data-salle-id');

            preloadView();

            // Recharger la page après un délai très court pour laisser le spinner s'afficher
            requestAnimationFrame(() => {
                setTimeout(() => {
                    // Rediriger vers l'URL correspondante
                    window.location.href = `/core/properties/${salleId}/`;
                }, 50); // ajustable si besoin
            });
        });
    });
});