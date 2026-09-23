// noinspection JSUnusedGlobalSymbols
export function initializeGenderOrder() {
    // Sélectionner le conteneur
    const container = document.getElementById('gender-input');

    if (container) {
        const selectedElement = container.querySelector('.selected');
        if (selectedElement) {
            container.prepend(selectedElement);
        }
    }
}