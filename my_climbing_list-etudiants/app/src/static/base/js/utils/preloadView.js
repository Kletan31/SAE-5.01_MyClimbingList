function preloadView() {
    const loader = document.querySelector(".spinner-wrapper");
    if (!loader) return;

    // Masquer le contenu principal
    document.querySelector(".auth-form-container")?.classList.add("d-none");
    document.getElementById("template-container")?.classList.add("d-none");

    // Afficher le spinner avec animation CSS
    loader.classList.add("active");
    document.body.style.overflow = "hidden";
}

// Réinitialisation au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    const loader = document.querySelector(".spinner-wrapper");
    if (loader) loader.classList.remove("active");

    document.querySelector(".auth-form-container")?.classList.remove("d-none");
    document.getElementById("template-container")?.classList.remove("d-none");
    document.body.style.overflow = "auto";
});

// Réinitialisation si retour via bfcache
window.addEventListener("pageshow", () => {
    const loader = document.querySelector(".spinner-wrapper");
    if (loader) loader.classList.remove("active");

    document.querySelector(".auth-form-container")?.classList.remove("d-none");
    document.getElementById("template-container")?.classList.remove("d-none");
    document.body.style.overflow = "auto";
});