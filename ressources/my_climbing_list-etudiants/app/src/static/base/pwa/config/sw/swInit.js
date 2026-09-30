// # Logique d'installation
async function install() {
    try {
        // Supprime les anciens caches
        await deleteOldCaches();

        // Mise en cache des ressources minimales
        const cache = await caches.open(OFFLINE_CACHE);
        if (LOG) console.log("Mise en cache des ressources minimales :", OFFLINE_RESOURCES);
        await cache.addAll(OFFLINE_RESOURCES);

        // Force l'activation immédiate du nouveau SW
        await self.skipWaiting();
        if (LOG) console.log("Service Worker installé avec succès.");
    } catch (err) {
        console.error("Erreur pendant l'installation du Service Worker :", err);
    }
}

// # Logique d'activation
async function activate() {
    try {
        // Prend immédiatement le contrôle
        await self.clients.claim();
        if (LOG) console.log("Service Worker activé avec succès.");
    } catch (err) {
        console.error("Erreur pendant l'activation du Service Worker :", err);
    }
}