// Attacher la constante à window pour un accès global
let flashMode = false;
window.flashMode = flashMode;

// Attacher la fonction à window pour un accès global
function toggleFlashMode() {
    const flashIcons = document.querySelectorAll('.fa-circle-bolt');

    flashIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            flashMode = !flashMode; // Inverser l'état actuel
            const newColor = flashMode ? '#ffb512' : '#212529';

            // Appliquer la couleur à tous les icônes
            flashIcons.forEach(icon => {
                icon.style.color = newColor;
            });

            // Mettre à jour le graphique
            displayGraph(flashMode);
        });
    });
}
window.toggleFlashMode = toggleFlashMode;