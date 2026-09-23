// Constantes globales pour le Service Worker
self.MAIN_CACHE = `main-cache-${CACHE_VERSION}`;
self.OFFLINE_CACHE = `offline-cache-${CACHE_VERSION}`;

self.OFFLINE_RESOURCES = [
    '/fr/offline/',
    '/en/offline/',
    '/es/offline/',
    '/pt/offline/',
    '/fr/auth/offline/',
    '/en/auth/offline/',
    '/es/auth/offline/',
    '/pt/auth/offline/',
    '/fr/core/offline/',
    '/en/core/offline/',
    '/es/core/offline/',
    '/pt/core/offline/',
];

self.FALLBACK_URL = '/offline/';
self.FALLBACK_AUTH_URL = '/auth/offline/';
self.FALLBACK_CORE_URL = '/core/offline/';