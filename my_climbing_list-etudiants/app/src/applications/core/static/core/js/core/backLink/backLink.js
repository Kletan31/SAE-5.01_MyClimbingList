// backLink.js — version i18n (sans stripLang car les chemins sont déjà enregistrés sans le code langue)

document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("back-container-js");
    const link = document.getElementById("back-link");
    const label = document.getElementById("back-label");

    if (!container || !link || !label) return;

    // --- Détection de la langue ---
    const langPrefix = window.location.pathname.split("/")[1] || "fr";

    // --- Dictionnaire de traduction ---
    const TRANSLATIONS = {
        fr: {
            default: "Retour",
            labels: {
                "core/home/": "Accueil",
                "core/list/?force_list=1": "Liste",
                "core/list/": "Liste",
                "core/guidebook/": "Topo",
                "core/projects/": "Projets",
                "core/logbook/": "Carnet",
                "core/graph/": "Statistiques",
                "core/profile/": "Profil",
                "core/settings/": "Paramètres",
                "core/feedback/": "Contact",
                "core/confirm_session/": "Séance",
                "core/details/": "Détails",
                "core/properties/": "Propriétés",
                "contest/": "Retour",
            },
        },
        en: {
            default: "Back",
            labels: {
                "core/home/": "Home",
                "core/list/?force_list=1": "List",
                "core/list/": "List",
                "core/guidebook/": "Guidebook",
                "core/projects/": "Projects",
                "core/logbook/": "Logbook",
                "core/graph/": "Stats",
                "core/profile/": "Profile",
                "core/settings/": "Settings",
                "core/feedback/": "Feedback",
                "core/confirm_session/": "Session",
                "core/details/": "Details",
                "core/properties/": "Properties",
                "contest/": "Back",
            },
        },
        es: {
            default: "Volver",
            labels: {
                "core/home/": "Inicio",
                "core/list/?force_list=1": "Lista",
                "core/list/": "Lista",
                "core/guidebook/": "Guía",
                "core/projects/": "Proyectos",
                "core/logbook/": "Registro",
                "core/graph/": "Estadísticas",
                "core/profile/": "Perfil",
                "core/settings/": "Configuración",
                "core/feedback/": "Contacto",
                "core/confirm_session/": "Sesión",
                "core/details/": "Detalles",
                "core/properties/": "Propiedades",
                "contest/": "Volver",
            },
        },
        pt: {
            default: "Voltar",
            labels: {
                "core/home/": "Início",
                "core/list/?force_list=1": "Lista",
                "core/list/": "Lista",
                "core/guidebook/": "Guia",
                "core/projects/": "Projetos",
                "core/logbook/": "Diário",
                "core/graph/": "Estatísticas",
                "core/profile/": "Perfil",
                "core/settings/": "Configurações",
                "core/feedback/": "Contato",
                "core/confirm_session/": "Sessão",
                "core/details/": "Detalhes",
                "core/properties/": "Propriedades",
                "contest/": "Voltar",
            },
        },
    };

    const T = TRANSLATIONS[langPrefix] || TRANSLATIONS.fr;

    // --- Récupération du chemin courant ---
    const currentPath = window.location.pathname.slice(4); // ex: "core/settings/"

    // --- Cas particuliers : settings / feedback / logbook → retour vers profile ---
    const profilePages = [
        "core/settings/",
        "core/feedback/",
        "core/logbook/",
        "core/training/",
    ];

    let backPath;
    if (profilePages.some(prefix => currentPath.startsWith(prefix))) {
        const params = new URLSearchParams(window.location.search);
        const bloc = params.get("bloc");

        backPath = bloc !== null
            ? `core/profile/?bloc=${bloc}`
            : "core/profile/";
    } else if (currentPath === "core/profile/") {
        backPath = localStorage.getItem("last_path_profile");
    } else {
        backPath = localStorage.getItem("last_path");
    }

    if (!backPath) return;

    // --- Détermination du label à afficher ---
    let backLabel = T.default;
    for (const path in T.labels) {
        if (backPath.startsWith(path)) {
            backLabel = T.labels[path];
            break;
        }
    }

    // --- Mise à jour du lien et du texte ---
    link.href = `/${langPrefix}/${backPath}`;
    label.textContent = backLabel;
    container.classList.remove("d-none");
});