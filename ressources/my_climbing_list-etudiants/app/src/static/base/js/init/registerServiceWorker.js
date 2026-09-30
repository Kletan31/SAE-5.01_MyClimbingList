const SW_VERSION = ''; // Version injectée dynamiquement par Django

// Vérifier si le navigateur supporte le service-worker
if ('serviceWorker' in navigator) {
    (async () => {
        try {
            // Vérifier si un Service Worker est déjà installé
            const initialRegistration = await navigator.serviceWorker.getRegistration();

            if (!initialRegistration) {
                if (LOG) console.log("Initialisation du Service Worker");
                // Si aucun Service Worker n'est enregistré, enregistrer sans version
                await navigator.serviceWorker.register('/sw-placeholder.js', { updateViaCache: 'all' });
            }

            const storedVersion = localStorage.getItem("swVersion");

            // Vérifie la version du Service Worker avec localStorage
            if (!storedVersion || storedVersion !== SW_VERSION) {
                if (LOG) console.log("Nouvelle version détectée");
                await registerServiceWorker();
                localStorage.setItem("swVersion", SW_VERSION); // Synchroniser la version avec localStorage
            }

            // Vérifie la version du Service Worker avec l'attribut scriptURL
            else if (!await checkServiceWorkerVersion()) {
                const registrations = await navigator.serviceWorker.getRegistrations();
                const registration = registrations[0]; // On prend le premier élément
                await registration.unregister(); // Supprimer le Service Worker obsolète
                await registerServiceWorker();
            }

            // Maintient le cache du Service Worker à jour
            else if (updateCache()) {
                if (LOG) console.log("Réinitialisation du cache");
                navigator.serviceWorker.controller.postMessage({ action: "CLEAR_MAIN_CACHE" });
            }

            else {
                if (LOG) console.log("Service Worker à jour.");
            }
        } catch (error) {
            console.error('Erreur lors de la mise à jour du Service Worker:', error);
        }
    })();
}

// Fonction asynchrone pour enregistrer le Service Worker
async function registerServiceWorker() {
    try {
        // Enregistrer ensuite avec une version pour forcer la mise à jour et bloquer les requêtes réseau [Safari]
        const newRegistration = await navigator.serviceWorker.register(
            `/service-worker.js?v=${SW_VERSION}`,
            { updateViaCache: 'all' }
        );

        if (LOG) console.log("Service Worker enregistré avec le scope :", newRegistration.scope);
    } catch (error) {
        console.error("Erreur lors de l'enregistrement du Service Worker :", error);
    }
}