// swCacheFirst.js — compatible i18n (MAIN + OFFLINE cache)
self.cacheFirst = async function (event) {
    const mainCache = await caches.open(MAIN_CACHE);
    const offlineCache = await caches.open(OFFLINE_CACHE);
    const requestUrl = new URL(event.request.url);
    const path = requestUrl.pathname;

    // ================================
    // Ne jamais mettre en cache /core/confirm_session/
    // ================================
    if (stripLang(path) === 'core/confirm_session/') {
        if (LOG) console.log(`[CACHE FIRST] Bypass du cache pour : ${path}`);
        try {
            return await fetch(event.request);
        } catch (error) {
            if (LOG) console.warn(`[CACHE FIRST] Échec réseau pour ${path}`, error);
            return handleFallBack(event.request); // Fallback hors ligne
        }
    }

    // ================================
    // Stratégie Cache First améliorée
    // ================================
    try {
        // Cherche d'abord dans le MAIN_CACHE
        let cachedResponse = await mainCache.match(event.request);

        // Si pas trouvé, cherche dans OFFLINE_CACHE
        if (!cachedResponse) {
            cachedResponse = await offlineCache.match(event.request);
            if (cachedResponse && LOG) {
                console.log(`[CACHE FIRST] Trouvé dans le cache OFFLINE : ${path}`);
            }
        } else if (LOG) {
            console.log(`[CACHE FIRST] Trouvé dans le cache MAIN : ${path}`);
        }

        // Si trouvé, on retourne la réponse
        if (cachedResponse) return cachedResponse;

        // Sinon, on tente le réseau
        const networkResponse = await fetch(event.request);
        if (networkResponse && networkResponse.status === 200) {
            await mainCache.put(event.request, networkResponse.clone());
            if (LOG) console.log(`[CACHE FIRST] Ajouté au MAIN cache : ${path}`);
        }
        return networkResponse;

    } catch (error) {
        if (LOG) console.warn(`[CACHE FIRST] Erreur réseau pour ${path}`, error);
        return handleFallBack(event.request);
    }
};