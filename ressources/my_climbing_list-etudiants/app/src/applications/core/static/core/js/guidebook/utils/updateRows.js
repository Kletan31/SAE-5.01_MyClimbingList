function activateElementAndUpdateRows(elementId) {
    const rows = document.querySelectorAll("tr");
    const element = document.getElementById(elementId);

    // Activer le relais cliqué
    const circle = element.querySelector("circle");
    circle.setAttribute('r', '12');
    circle.classList.add('active');

    // Affichage des ouvertures associé au relais/secteur sélectionné
    rows.forEach(row => {
        const relaisValue = row.querySelector("td.toggle-column").id;
        row.classList.toggle("d-none", relaisValue !== elementId);
    });
}

// Attacher la fonction à window pour un accès global
window.activateElementAndUpdateRows = activateElementAndUpdateRows;