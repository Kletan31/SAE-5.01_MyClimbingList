// === Initialisation des boutons d'incrémentation et de décrémentation ===
// noinspection JSUnusedGlobalSymbols
export function initializeIncrementDecrementButtons() {
    document.querySelectorAll('.increment-button, .decrement-button').forEach((button) => {
        button.addEventListener('click', () => {
            const isIncrement = button.classList.contains('increment-button');
            const input = isIncrement ? button.previousElementSibling : button.nextElementSibling;
            const currentValue = +input.value || 0;
            const newValue = isIncrement ? currentValue + 1 : currentValue - 1;

            // Les valeurs saisies doivent être positives
            if (newValue >= 0) {
                input.value = newValue;
                input.dispatchEvent(new Event('input')); // Déclenche manuellement l'événement input
            }
        });
    });
}