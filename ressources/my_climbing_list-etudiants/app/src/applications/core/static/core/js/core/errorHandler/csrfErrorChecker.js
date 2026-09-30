async function csrfErrorChecker(response) {
    let data = {};

    // Supprimer tous les cookies en cas d'erreur CSRF
    if (response.status === 403) {
        deleteAllCookies();
        window.location.href = "/auth/logout/";
        return;
    }

    try {
        data = await response.json();
        return data;
    } catch {
        return null;
    }
}

// Attacher la fonction à window pour un accès global
window.csrfErrorChecker = csrfErrorChecker;