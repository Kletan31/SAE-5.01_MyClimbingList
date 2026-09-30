/** Fonction pour gérer la déconnexion :
    • Vide le cache (évite de se connecter avec les données de l'utilisateur précédent)
    • Gére la redirection qui suit la déconnexion
*/
async function handleLogout(event) {
    const response = await fetch(event.request);

    // Vider le cache avant de retourner la réponse
    await clearMainCache();
    return response;
}