// installGuideRedirection.js — compatible i18n (utilise slice(4) pour ignorer le code langue)
document.addEventListener('DOMContentLoaded', function () {
    const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
    const isInStandaloneMode = ('standalone' in window.navigator && window.navigator.standalone);
    const currentPath = window.location.pathname;

    // Supprime le préfixe de langue (/fr/, /en/, etc.)
    const stripLang = (path) => path.slice(4);
    const cleanPath = stripLang(currentPath);

    const exemptedPrefixes = [
        "install-guide",
        "password_reset",
        "reset"
    ];

    const isExempted = exemptedPrefixes.some(prefix => cleanPath.startsWith(prefix));

    if (isIOS && !isInStandaloneMode && !isExempted) {
        const langPrefix = currentPath.split('/')[1] || 'fr';
        window.location.href = `/${langPrefix}/install-guide/`;
    }
});