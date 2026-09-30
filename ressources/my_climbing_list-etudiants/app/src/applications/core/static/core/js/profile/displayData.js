// core/js/profile/displayData.js
import { translateLabel } from "../i18n/labels.js";

// noinspection JSUnusedGlobalSymbols
export function initializeStats() {
    // 1. Détecte la langue actuelle depuis l'URL
    const langPrefix = window.location.pathname.split('/')[1] || 'fr';

    // 2. Dictionnaire des traductions
    const TRANSLATIONS = {
        fr: {
            undefined: 'non défini',
        },
        en: {
            undefined: 'undefined',
        },
        es: {
            undefined: 'no definido',
        },
        pt: {
            undefined: 'não definido',
        },
    };

    // 3. Sélectionne la traduction selon la langue détectée
    const T = TRANSLATIONS[langPrefix] || TRANSLATIONS.fr;
    const fallback = T.undefined;

    // 4. Récupère les données du localStorage avec valeurs par défaut traduites
    const stats = {
        totalRoute: localStorage.getItem('totalRoute') || 0,
        totalRouteFlash: localStorage.getItem('totalRouteFlash') || 0,
        totalRouteLead: localStorage.getItem('totalRouteLead') || 0,
        totalRouteLeadFlash: localStorage.getItem('totalRouteLeadFlash') || 0,
        preferredRouteProfile: localStorage.getItem('preferredRouteProfile') || fallback,
        preferredRouteStyle: localStorage.getItem('preferredRouteStyle') || fallback,
        preferredRouteStyleColor: localStorage.getItem('preferredRouteStyleColor') || 'undefined',
        levelRoute: localStorage.getItem('levelRoute') || '-',
        levelRouteColor: localStorage.getItem('levelRouteColor') || '#333',
        totalRouteSessions: localStorage.getItem('totalRouteSessions') || fallback,

        totalBoulder: localStorage.getItem('totalBoulder') || 0,
        totalBoulderFlash: localStorage.getItem('totalBoulderFlash') || 0,
        preferredBoulderProfile: localStorage.getItem('preferredBoulderProfile') || fallback,
        preferredBoulderStyle: localStorage.getItem('preferredBoulderStyle') || fallback,
        preferredBoulderStyleColor: localStorage.getItem('preferredBoulderStyleColor') || 'undefined',
        levelBoulder: localStorage.getItem('levelBoulder') || fallback,
        levelBoulderColor: localStorage.getItem('levelBoulderColor') || fallback,
        totalBoulderSessions: localStorage.getItem('totalBoulderSessions') || fallback,
    };

    // 5. Injection des valeurs dans le DOM
    document.getElementById('totalRouteTopRope').textContent = stats.totalRoute;
    document.getElementById('totalRouteTopRopeFlash').textContent = stats.totalRouteFlash;
    document.getElementById('totalRouteLead').textContent = stats.totalRouteLead.toString();
    document.getElementById('totalRouteLeadFlash').textContent = stats.totalRouteLeadFlash.toString();
    document.getElementById('preferredRouteProfile').textContent = translateLabel(stats.preferredRouteProfile);
    document.getElementById('preferredRouteStyle').textContent = translateLabel(stats.preferredRouteStyle);
    document.getElementById('preferredRouteStyle').classList.add("style-" + stats.preferredRouteStyleColor);
    document.getElementById('levelRoute').textContent = stats.levelRoute;
    document.getElementById('levelRoute').style.borderColor = stats.levelRouteColor;
    document.getElementById('totalRouteSessions').textContent = stats.totalRouteSessions;

    document.getElementById('totalBoulder').textContent = stats.totalBoulder;
    document.getElementById('totalBoulderFlash').textContent = stats.totalBoulderFlash;
    document.getElementById('preferredBoulderProfile').textContent = translateLabel(stats.preferredBoulderProfile);
    document.getElementById('preferredBoulderStyle').textContent = translateLabel(stats.preferredBoulderStyle);
    document.getElementById('preferredBoulderStyle').classList.add("style-" + stats.preferredBoulderStyleColor);
    document.getElementById('levelBoulder').textContent = stats.levelBoulder;
    document.getElementById('levelBoulder').style.borderColor = stats.levelBoulderColor;
    document.getElementById('totalBoulderSessions').textContent = stats.totalBoulderSessions;
}