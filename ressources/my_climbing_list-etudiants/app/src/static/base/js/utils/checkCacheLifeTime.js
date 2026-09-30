// Logique pour assurer une mise à jour du cache
const CACHE_LIFETIME = 60 * 10 * 1000; // 10 minutes en millisecondes
const TIMESTAMP_KEY = "cache-timestamp";

function getCacheTimestamp() {
    return parseInt(localStorage.getItem(TIMESTAMP_KEY)) || null;
}

function setCacheTimestamp() {
    const now = Date.now();
    localStorage.setItem(TIMESTAMP_KEY, now.toString());
}

function updateCache() {
    const lastTimestamp = getCacheTimestamp();
    const now = Date.now();

    if (lastTimestamp && now - lastTimestamp > CACHE_LIFETIME) {
        if (LOG) console.log("Le cache a expiré. Réinitialisation du Service Worker...");
        setCacheTimestamp();
        return true;
    }
    return false;
}

// Attacher la fonction à window pour un accès global
window.updateCache = updateCache;