// lastPage.js — compatible i18n (utilise slice(4) pour ignorer le code langue)

document.addEventListener("DOMContentLoaded", function () {
    const referrer = document.referrer;
    const currentPath = window.location.pathname;

    if (!referrer) return;

    const refURL = new URL(referrer);
    const refPath = refURL.pathname + refURL.search;

    // Supprime le code langue (/fr/, /en/, etc.)
    const stripLang = (path) => path.slice(4);

    // Nettoyage des chemins
    const cleanRefPath = stripLang(refPath);
    const cleanCurrentPath = stripLang(currentPath);

    const forceReturnToHomePaths = [
        "core/list/",
        "core/projects/",
        "core/graph/",
        "core/details/",
        "contest/"
    ];

    const profilePages = [
        "core/settings/",
        "core/feedback/",
        "core/logbook/",
        "core/training/",
    ];

    // Ne pas stocker si la page précédente est identique (on ignore les query params)
    if (cleanRefPath === cleanCurrentPath) return;

    // Cas particuliers pour la page profile
    // Si la page courante est une page secondaire du profil
    // (settings, feedback, logbook), on ne met pas à jour last_path
    if (profilePages.some(prefix => cleanCurrentPath.startsWith(prefix))) return;

    // Si la page précédente est une page secondaire du profil,
    // on ne met pas à jour last_path pour éviter un retour incohérent
    if (profilePages.some(prefix => cleanRefPath.startsWith(prefix))) return;
    if (cleanRefPath === "core/profile/") return;

    if (cleanCurrentPath === "core/home/") {
        localStorage.setItem("last_path", "");
        return;
    }

    if (forceReturnToHomePaths.includes(cleanCurrentPath)) {
        localStorage.setItem("last_path", "core/home/");
        return;
    }

    if (cleanCurrentPath === "core/guidebook/") {
        localStorage.setItem("last_path", "core/list/?force_list=1");
        return;
    }

    if (cleanCurrentPath === "core/profile/") {
        localStorage.setItem("last_path_profile", cleanRefPath);
        return;
    }

    // ===============================
    // === Cas spécifiques contest ===
    // ===============================

    // Page Alti Ligue (classement global)
    if (cleanCurrentPath.startsWith("contest/ranking/")) {
        localStorage.setItem("last_path", "contest/");
        return;
    }

    const salleRegex = /^contest\/salle\/(\d+)\/$/;
    const contestDetailRegex = /^contest\/contest\/(\d+)\/$/;
    const contestResultRegex = /^contest\/contest\/(\d+)\/resultats\/$/;
    const participantRegex = /^contest\/contest\/(\d+)\/participant\/(\d+)\/$/;
    const teamRegex = /^contest\/contest\/(\d+)\/team\/(\d+)\/$/;

    // Page salle → stocke le salle_id
    if (salleRegex.test(cleanCurrentPath)) {
        const match = cleanCurrentPath.match(salleRegex);
        localStorage.setItem("contest_salle_id", match[1]);
        localStorage.setItem("last_path", "contest/");
        return;
    }

    // Page contest → revient vers /contest/salle/{salle_id}/
    if (contestDetailRegex.test(cleanCurrentPath)) {
        const salleId = localStorage.getItem("contest_salle_id");
        if (salleId) {
            localStorage.setItem("last_path", `contest/salle/${salleId}/`);
        } else {
            localStorage.setItem("last_path", "contest/");
        }
        return;
    }

    // Page résultats → revient vers /contest/salle/{salle_id}/
    if (contestResultRegex.test(cleanCurrentPath)) {
        const salleId = localStorage.getItem("contest_salle_id");
        if (salleId) {
            localStorage.setItem("last_path", `contest/salle/${salleId}/`);
        } else {
            localStorage.setItem("last_path", "contest/");
        }
        return;
    }

    // Page participant → revient vers résultats avec le bon classement
    if (participantRegex.test(cleanCurrentPath)) {
        const match = cleanCurrentPath.match(participantRegex);

        const currentURL = new URL(window.location.href);
        const classement = currentURL.searchParams.get("classement");

        let backPath = `contest/contest/${match[1]}/resultats/`;
        if (classement) {
            backPath += `?classement=${classement}`;
        }

        localStorage.setItem("last_path", backPath);
        return;
    }

    // Page team → revient vers résultats avec le bon classement
    if (teamRegex.test(cleanCurrentPath)) {
        const match = cleanCurrentPath.match(teamRegex);

        const currentURL = new URL(window.location.href);
        const classement = currentURL.searchParams.get("classement");

        let backPath = `contest/contest/${match[1]}/resultats/`;
        if (classement) {
            backPath += `?classement=${classement}`;
        }

        localStorage.setItem("last_path", backPath);
        return;
    }

    // Fallback général
    localStorage.setItem("last_path", cleanRefPath);
});