// === Initialisation des champs nb_try et nb_try_lead avec vérification ===
/**
 * Le but de ce code est de s’assurer que la valeur d’un champ d’entrée nb_try_* (nombre de montées) ne soit jamais
 * inférieure à celle du champ correspondant nb_top_* (nombre de tops réussis). Si cela se produit, le champ nb_try_*
 * est automatiquement ajusté pour égaler nb_top_*.
 */
// noinspection JSUnusedGlobalSymbols
export function initializeTryValidation() {
    document.querySelectorAll('.route-item').forEach(routeItem => {
        const routeId = routeItem.dataset.routeId;

        // Récupération des champs d'entrée pour nb_try et nb_top
        const nbTryInput = routeItem.querySelector(`input[name='nb_try_${routeId}']`);
        const nbTopInput = routeItem.querySelector(`input[name='nb_top_${routeId}']`);

        // Ajout des événements 'input' pour valider les valeurs
        nbTryInput.addEventListener('input', () => validateInput(nbTryInput, nbTopInput, 'try'));
        nbTopInput.addEventListener('input', () => validateInput(nbTryInput, nbTopInput, 'top'));

        // Vérification et ajout de la logique pour 'lead' si applicable
        const nbTryLeadInput = routeItem.querySelector(`input[name='nb_try_${routeId}_lead']`);
        const nbTopLeadInput = routeItem.querySelector(`input[name='nb_top_${routeId}_lead']`);

        if (nbTryLeadInput && nbTopLeadInput) {
            nbTryLeadInput.addEventListener('input', () => validateInput(nbTryLeadInput, nbTopLeadInput, 'try'));
            nbTopLeadInput.addEventListener('input', () => validateInput(nbTryLeadInput, nbTopLeadInput, 'top'));
        }
    });
}

// Fonction utilitaire
function validateInput(nbTryInput, nbTopInput, inputType) {
    const nbTryValue = +nbTryInput.value || 0;
    const nbTopValue = +nbTopInput.value || 0;

    if (nbTryValue < nbTopValue) {
        if (inputType === 'try') {
            nbTopInput.value = nbTryValue;
        } else {
            nbTryInput.value = nbTopValue;
        }
    }
}