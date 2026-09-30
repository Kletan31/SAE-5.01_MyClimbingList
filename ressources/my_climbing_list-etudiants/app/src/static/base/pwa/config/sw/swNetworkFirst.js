self.networkFirst = async function (event) {
    try {
        const requestUrl = new URL(event.request.url);
        const path = stripLang(requestUrl.pathname); // enlève le code de langue (/fr/, /en/, etc.)

        // Essaye toujours d’aller chercher la ressource sur le réseau
        const response = await fetch(event.request);

        // === Gestion spécifique des pages à rafraîchir ===
        if (path === "core/confirm_session/") {
            await clearMainCache();
            if (LOG) console.log("[CACHE] Cache principal vidé après confirmation de séance.");
        }

        if (/^core\/contest\/contest\/\d+\/inscription\/$/.test(path)) {
            await clearContestCache();
            if (LOG) console.log("[CACHE] Cache contest vidé après inscription.");
        }

        return response;

    } catch (error) {
        if (LOG) console.warn("[NETWORK] Erreur réseau :", error);
        return handleFallBack(event.request);
    }
};