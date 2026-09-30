async function checkServiceWorkerVersion() {
    const registrations = await navigator.serviceWorker.getRegistrations();
    const registration = registrations[0]; // On prend le premier élément

    // Vérifier qu'un Service Worker est enregistré avant de continuer
    if (!registration || !registration.active) return true;

    const scriptURL = registration.active.scriptURL;

    // Extraction de la version depuis l'URL
    const match = scriptURL.match(/[?]v=?(\d+)/);
    const swVersion = match ? match[1] : null;

    if (!swVersion) {
        if (LOG) console.log("Le service worker enregistré ne contient pas de version.");
        return true;
    }

    // Récupération de la version stockée dans localStorage
    const storedVersion = localStorage.getItem("swVersion");

    if (LOG) console.log(`Version SW actuelle : ${swVersion}`);
    if (LOG) console.log(`Version SW stockée : ${storedVersion}`);

    return storedVersion === swVersion;
}

// Attacher la fonction à window pour un accès global
window.checkServiceWorkerVersion = checkServiceWorkerVersion;