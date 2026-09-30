function initTooltips() {
    // Initialiser tous les tooltips Bootstrap
    const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Attacher la fonction à window pour un accès global
window.initTooltips = initTooltips;