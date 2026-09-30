/**
 * Stocke les données de la séance dans sessionStorage afin d'accéder au template confirm_session en conformité.
 */
// noinspection JSUnusedGlobalSymbols
export function FetchSessionData() {
    // Récupérer la date de la séance depuis une balise <meta>
    const sessionDate = document.querySelector('input[name="date_seance"]').value;

    // Initialiser une liste pour stocker l'ordre des routes
    let routesOrder = [];

    // Parcourir toutes les balises <meta> correspondant aux routes
    document.querySelectorAll('meta[name^="route-"]').forEach(meta => {
        // Extraire l'ID de la route à partir du nom de la balise
        const routeId = meta.name.split('-')[1];

        // Ajouter l'ID de la route à routesOrder
        routesOrder.push(routeId);

        // Parser les données JSON contenues dans la balise <meta>
        const routeData = JSON.parse(meta.content);

        // Stocker chaque donnée de la route dans sessionStorage
        sessionStorage.setItem(`nb_try_${routeId}`, routeData.nb_try);
        sessionStorage.setItem(`nb_top_${routeId}`, routeData.nb_top);
        sessionStorage.setItem(`flash_${routeId}`, routeData.flash);
        sessionStorage.setItem(`flash_available_${routeId}`, routeData.flash_available);

        // Vérifier et stocker uniquement si les données "lead" existent
        if ('nb_try_lead' in routeData) {
            sessionStorage.setItem(`nb_try_${routeId}_lead`, routeData.nb_try_lead);
            sessionStorage.setItem(`nb_top_${routeId}_lead`, routeData.nb_top_lead);
            sessionStorage.setItem(`flash_${routeId}_lead`, routeData.flash_lead);
        }
    });

    // Stocker l'ordre des routes dans sessionStorage sous forme de chaîne
    sessionStorage.setItem('routesOrder', routesOrder.join(','));

    // Stocker l'ordre des routes dans une balise meta sous forme de chaîne
    document.querySelector('input[name="routes_order"]').value = routesOrder.join(',');

    // Stocker la date de la séance dans sessionStorage
    sessionStorage.setItem('date_seance', sessionDate);
}