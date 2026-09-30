// === Utilitaire : retirer le préfixe langue (/fr/, /en/, etc.) ===
function stripLang(pathname) {
    return pathname.startsWith("/") ? pathname.slice(4) : pathname;
}

// === Suppression de tous les caches ===
async function deleteOldCaches() {
    try {
        const names = await caches.keys();
        await Promise.all(
            names.map(name => caches.delete(name))
        );
        if (LOG) console.log("[CACHE] Tous les caches ont été supprimés.");
    } catch (err) {
        console.error("[CACHE] Erreur deleteOldCaches :", err);
    }
}

// === Suppression du MAIN_CACHE ===
async function clearMainCache() {
    try {
        const names = await caches.keys();
        const toDelete = names.filter(name => name.startsWith("main-cache-"));
        await Promise.all(toDelete.map(name => caches.delete(name)));
        if (LOG) console.log("[CACHE] Tous les main-cache-* ont été supprimés.");
    } catch (err) {
        console.error("[CACHE] Erreur clearMainCache :", err);
    }
}

// === Suppression de /core/projects/ et /core/guidebook/ ===
async function clearProjectsCache() {
    try {
        const cache = await caches.open(MAIN_CACHE);
        const keys = await cache.keys();

        const toDelete = keys.filter(req => {
            const path = stripLang(new URL(req.url).pathname);
            return path.startsWith("core/projects/") || path.startsWith("core/guidebook/");
        });

        await Promise.all(toDelete.map(req => cache.delete(req)));
        if (LOG) console.log("[CACHE] /core/projects/ et /core/guidebook/* purgés.");
    } catch (err) {
        console.error("[CACHE] Erreur clearProjectsCache :", err);
    }
}

// === Suppression de /core/home/ ===
async function clearHomeCache() {
    try {
        const cache = await caches.open(MAIN_CACHE);
        const keys = await cache.keys();

        const toDelete = keys.filter(req =>
            stripLang(new URL(req.url).pathname).startsWith("core/home/")
        );

        await Promise.all(toDelete.map(req => cache.delete(req)));
        if (LOG) console.log("[CACHE] /core/home/* purgé.");
    } catch (err) {
        console.error("[CACHE] Erreur clearHomeCache :", err);
    }
}

// === Suppression de /contest/ ===
async function clearContestCache() {
    try {
        const cache = await caches.open(MAIN_CACHE);
        const keys = await cache.keys();

        const toDelete = keys.filter(req =>
            stripLang(new URL(req.url).pathname).startsWith("contest/")
        );

        await Promise.all(toDelete.map(req => cache.delete(req)));
        if (LOG) console.log("[CACHE] /contest/* purgé.");
    } catch (err) {
        console.error("[CACHE] Erreur clearContestCache :", err);
    }
}

// === Suppression de /core/settings/ ===
async function clearSettingsCache() {
    try {
        const cache = await caches.open(MAIN_CACHE);
        const keys = await cache.keys();

        const toDelete = keys.filter(req =>
            stripLang(new URL(req.url).pathname).startsWith("core/settings/")
        );

        await Promise.all(toDelete.map(req => cache.delete(req)));
        if (LOG) console.log("[CACHE] /core/settings/* purgé.");
    } catch (err) {
        console.error("[CACHE] Erreur clearSettingsCache :", err);
    }
}

// === Suppression de /core/training/ ===
async function clearTrainingCache() {
    try {
        const cache = await caches.open(MAIN_CACHE);
        const keys = await cache.keys();

        const toDelete = keys.filter(req =>
            stripLang(new URL(req.url).pathname).startsWith("core/training/")
        );

        await Promise.all(toDelete.map(req => cache.delete(req)));
        if (LOG) console.log("[CACHE] /core/training/* purgé.");
    } catch (err) {
        console.error("[CACHE] Erreur clearTrainingCache :", err);
    }
}

// === Suppression de /core/list/ ===
async function clearSalleListCache() {
    try {
        const cache = await caches.open(MAIN_CACHE);
        const keys = await cache.keys();

        const toDelete = keys.filter(req =>
            stripLang(new URL(req.url).pathname).startsWith("core/list/")
        );

        await Promise.all(toDelete.map(req => cache.delete(req)));
        if (LOG) console.log("[CACHE] /core/list/* purgé.");
    } catch (err) {
        console.error("[CACHE] Erreur clearSalleListCache :", err);
    }
}

// === Gestion du fallback hors-ligne ===
async function handleFallBack(request) {
    try {
        const url = new URL(request.url);
        const pathname = url.pathname;

        // Détection du code langue
        let langPrefix = "";
        const langMatch = pathname.match(/^\/(fr|en|pt)\//);
        if (langMatch) langPrefix = `/${langMatch[1]}`;

        // Supprime le code langue pour identifier le type de page
        const path = stripLang(pathname);

        // Sélection du bon fallback
        if (path.startsWith("core/") || path.startsWith("contest/")) {
            return Response.redirect(`${langPrefix}${self.FALLBACK_CORE_URL}`, 302);
        } else if (path.startsWith("auth/")) {
            return Response.redirect(`${langPrefix}${self.FALLBACK_AUTH_URL}`, 302);
        } else {
            return Response.redirect(`${langPrefix}${self.FALLBACK_URL}`, 302);
        }
    } catch (err) {
        console.error("[CACHE] Erreur handleFallBack :", err, request);
        return new Response("", { status: 500 });
    }
}