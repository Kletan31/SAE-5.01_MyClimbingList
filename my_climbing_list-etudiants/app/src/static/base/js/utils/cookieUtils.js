// Fonction utilitaire getCookie pour la recherche d'un cookie par son nom et retourne sa valeur
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fonction utilitaire pour supprimer tous les cookies du client
function deleteAllCookies() {
    document.cookie.split(";").forEach((cookie) => {
        let name = cookie.split("=")[0].trim();
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
    });
}

// Attacher la fonction à window pour un accès global
window.getCookie = getCookie;
window.deleteAllCookies = deleteAllCookies;