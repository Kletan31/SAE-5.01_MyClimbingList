// Fonction désactiver tous les relais
function resetCircles(circles) {
    circles.forEach(circle => {
        circle.setAttribute('r', '10');
        circle.classList.remove('active');
    });
}

// Attacher la fonction à window pour un accès global
window.resetCircles = resetCircles;