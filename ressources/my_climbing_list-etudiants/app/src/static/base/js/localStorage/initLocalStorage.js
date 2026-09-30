// === GESTION LOCAL STORAGE ===

// Initialiser une clé dans localStorage si elle n'existe pas déjà
function initLocalStorageKey(key, defaultValue) {
    if (!localStorage.getItem(key)) {
        localStorage.setItem(key, defaultValue);
    }
}

// Mettre à jour une clé spécifique dans localStorage
function updateLocalStorageKey(key, value) {
    localStorage.setItem(key, value);
}

// Synchroniser une clé avec les données présentes sur la page
function syncLocalStorageKeyWithPage(key, elementId) {
    const element = document.getElementById(elementId);

    if (element) {
        let pageValue = element.dataset.value; // Récupérer la valeur de l'attribut data-value

        const storedValue = localStorage.getItem(key);

        // Si la valeur de la page est différente de celle stockée, mettre à jour
        if (pageValue && pageValue !== storedValue) {
            updateLocalStorageKey(key, pageValue);
        }
    }
}

// Initialiser toutes les données dans localStorage et les synchroniser avec la page
function initAndSyncLocalStorageData() {
    // Liste des clés et leurs identifiants correspondants dans le DOM
    const localStorageMapping = [
        // home
        { key: 'totalRouteSessions', id: 'localStorageTotalRouteSessions' },
        { key: 'totalBoulderSessions', id: 'localStorageTotalBoulderSessions' },

        // progression
        { key: 'levelRoute', id: 'localStorageLevelRoute' },
        { key: 'levelRouteColor', id: 'localStorageLevelRouteColor' },
        { key: 'levelBoulder', id: 'localStorageLevelBoulder' },
        { key: 'levelBoulderColor', id: 'localStorageLevelBoulderColor' },

        // ascension-voie
        { key: 'totalRoute', id: 'localStorageTotalRoute' },
        { key: 'totalRouteFlash', id: 'localStorageTotalRouteFlash' },
        { key: 'totalRouteLead', id: 'localStorageTotalRouteLead' },
        { key: 'totalRouteLeadFlash', id: 'localStorageTotalRouteLeadFlash' },

        // ascension-bloc
        { key: 'totalBoulder', id: 'localStorageTotalBoulders' },
        { key: 'totalBoulderFlash', id: 'localStorageTotalBoulderFlash' },

        // profil
        { key: 'preferredRouteProfile', id: 'localStoragePreferredRouteProfile' },
        { key: 'preferredBoulderProfile', id: 'localStoragePreferredBoulderProfile' },

        // style
        { key: 'preferredRouteStyle', id: 'localStoragePreferredRouteStyle' },
        { key: 'preferredRouteStyleColor', id: 'localStoragePreferredRouteStyleColor' },
        { key: 'preferredBoulderStyle', id: 'localStoragePreferredBoulderStyle' },
        { key: 'preferredBoulderStyleColor', id: 'localStoragePreferredBoulderStyleColor' },
    ];

    // Initialiser toutes les clés avec leurs valeurs par défaut
    localStorageMapping.forEach(({ key }) => {
        let defaultValue;

        // Définir des valeurs par défaut spécifiques pour certaines clés
        if (['levelRouteColor', 'levelBoulderColor'].includes(key)) {
            defaultValue = "#000"; // Noir pour les couleurs
        } else if (['preferredRouteStyleColor', 'preferredBoulderStyleColor'].includes(key)) {
            defaultValue = "undefined"; // class de base
        } else if (['levelRoute', 'levelBoulder'].includes(key)) {
            defaultValue = "-"; // class de base
        } else if (['preferredRouteProfile', 'preferredBoulderProfile', 'preferredRouteStyle', 'preferredBoulderStyle'].includes(key)) {
            defaultValue = ""; // "" pour les champs textuels
        } else {
            defaultValue = 0; // 0 pour les champs numériques
        }

        initLocalStorageKey(key, defaultValue);
    });

    // Synchroniser chaque clé avec son élément correspondant dans la page
    localStorageMapping.forEach(({ key, id }) => syncLocalStorageKeyWithPage(key, id));
}

// Appeler l'initialisation et la synchronisation au chargement
document.addEventListener('DOMContentLoaded', initAndSyncLocalStorageData);
