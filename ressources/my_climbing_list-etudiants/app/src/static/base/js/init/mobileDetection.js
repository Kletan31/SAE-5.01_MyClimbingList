// mobileDetection.js — compatible i18n (utilise slice(4) pour ignorer le code langue)
document.addEventListener("DOMContentLoaded", function () {
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
        .test(navigator.userAgent);

    const currentPath = window.location.pathname;

    // Supprime le code langue du chemin (/fr/, /en/, etc.)
    const stripLang = (path) => path.slice(4);
    const cleanPath = stripLang(currentPath);

    // Autoriser les URLs liées à la réinitialisation de mot de passe
    const isPasswordResetFlow =
        cleanPath.startsWith("password_reset") || cleanPath.startsWith("reset/");

    // Si non mobile et pas dans le flux de réinitialisation → redirige vers la page desktop
    if (!isMobile && !isPasswordResetFlow) {
        window.location.href = "/";
    }
});