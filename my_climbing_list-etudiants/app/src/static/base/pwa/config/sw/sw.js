// sw.js — compatible i18n (gère /fr/, /en/, etc. dans les chemins)
let LOG = false;
const CACHE_VERSION = '';

importScripts(
    `/static/base/pwa/config/sw/swConst.js?v=${CACHE_VERSION}`,
    `/static/base/pwa/config/sw/swUtils.js?v=${CACHE_VERSION}`,
    `/static/base/pwa/config/sw/swInit.js?v=${CACHE_VERSION}`,
    `/static/base/pwa/config/sw/swFetchLogout.js?v=${CACHE_VERSION}`,
    `/static/base/pwa/config/sw/swNetworkFirst.js?v=${CACHE_VERSION}`,
    `/static/base/pwa/config/sw/swCacheFirst.js?v=${CACHE_VERSION}`,
);

// Installation du Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(install());
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
    event.waitUntil(activate());
});

// Réception de messages depuis l’app
self.addEventListener('message', (event) => {
    const data = event.data;
    if (!data || !data.action) return;

    const actions = {
        CLEAR_PROJECTS_CACHE: clearProjectsCache,
        CLEAR_HOME_CACHE: clearHomeCache,
        CLEAR_CONTESTS_CACHE: clearContestCache,
        CLEAR_SETTINGS_CACHE: clearSettingsCache,
        CLEAR_TRAINING_CACHE: clearTrainingCache,
        CLEAR_SALLE_LIST_CACHE: clearSalleListCache,
        CLEAR_MAIN_CACHE: clearMainCache,
    };

    const actionFn = actions[data.action];
    if (actionFn) event.waitUntil(actionFn());
});

// Gestion des requêtes réseau
self.addEventListener('fetch', (event) => {
    const requestUrl = new URL(event.request.url);

    // Supprimer le code langue (/fr/, /en/, etc.)
    const path = stripLang(requestUrl.pathname)

    // Gestion spécifique : déconnexion
    if (path === 'auth/logout/') {
        event.respondWith(handleLogout(event));
        return;
    }

    // Toutes les requêtes POST passent en "network first"
    if (event.request.method === 'POST') {
        event.respondWith(networkFirst(event));
        return;
    }

    // Ignorer les ressources statiques et les back-offices
    if (
        requestUrl.pathname.startsWith('/static/') ||
        path.startsWith('staff/') ||
        path.startsWith('direction/') ||
        path.startsWith('public_contests/') ||
        path.startsWith('auth/') ||
        path.startsWith('event/') ||
        path.startsWith('route_event/')
    ) {
        return;
    }

    // Pour le reste : stratégie "cache first"
    event.respondWith(cacheFirst(event));
});