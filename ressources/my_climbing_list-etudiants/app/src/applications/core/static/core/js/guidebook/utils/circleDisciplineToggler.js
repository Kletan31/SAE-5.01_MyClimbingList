// Fonction pour basculer la visibilité des relais/secteurs d'une discipline à l'autre
function toggleDiscipline(circles) {
    circles.forEach(circle => {
        circle.parentElement.classList.toggle('d-none');
    });
}

// Attacher la fonction à window pour un accès global
window.toggleDiscipline = toggleDiscipline;