// === Initialisation des icônes Flash ===
// noinspection JSUnusedGlobalSymbols
export function initializeIcons() {
    document.querySelectorAll('.route-item').forEach(routeItem => {
        const routeId = routeItem.dataset.routeId;

        // Attacher les écouteurs d'événements aux icônes flash (moulinette et tête) pour chaque route
        routeItem.querySelectorAll('.flash-icon').forEach(flashIcon => {
            const lead = flashIcon.getAttribute('data-flash-type') === 'lead';
            flashIcon.addEventListener('click', () => toggleFlashIcon(flashIcon, routeId, lead));
        });

        // Initialise les restrictions pour les champs nb_try et nb_top (moulinette) et pour nb_try_lead et nb_top_lead (tête)
        initializeInputValidation(routeItem, routeId);
    });
}

// Fonction pour attacher les écouteurs d'événements pour la validation des champs nb_try et nb_top
function initializeInputValidation(routeItem, routeId) {
    const nbTryInput = routeItem.querySelector(`input[name="nb_try_${routeId}"]`);
    const nbTopInput = routeItem.querySelector(`input[name="nb_top_${routeId}"]`);
    const nbTryLeadInput = routeItem.querySelector(`input[name="nb_try_${routeId}_lead"]`);
    const nbTopLeadInput = routeItem.querySelector(`input[name="nb_top_${routeId}_lead"]`);

    const validateHandler = () => {
        if (nbTryInput.dataset.flash === 'true' || nbTopInput.dataset.flash === 'true') {
            enforceMinimumValues(nbTryInput, nbTopInput);
        }
        if (nbTryLeadInput?.dataset.flash === 'true' || nbTopLeadInput?.dataset.flash === 'true') {
            enforceMinimumValues(nbTryLeadInput, nbTopLeadInput);
        }
    };

    [nbTryInput, nbTopInput, nbTryLeadInput, nbTopLeadInput].forEach(input => {
        if (input) input.addEventListener('input', validateHandler);
    });
}

// Fonction pour basculer l'état d'une icône flash (moulinette ou tête)
function toggleFlashIcon(icon, routeId, isLead) {
    const inputType = isLead ? 'lead' : '';
    const hiddenInput = document.getElementById(`flash_${routeId}${inputType ? '_' + inputType : ''}`);
    const nbTryInput = document.querySelector(`input[name="nb_try_${routeId}${inputType ? '_' + inputType : ''}"]`);
    const nbTopInput = document.querySelector(`input[name="nb_top_${routeId}${inputType ? '_' + inputType : ''}"]`);

    // Basculer l'état d'activation de l'icône
    const isActive = icon.classList.toggle('active');

    // Mettre à jour les inputs
    nbTryInput.dataset.flash = isActive ? 'true' : 'false';
    nbTopInput.dataset.flash = isActive ? 'true' : 'false';
    hiddenInput.value = isActive ? 'true' : 'false';

    // Vérifier que le nombre de montées ainsi que le nombre de tops est supérieur à 1 si l'ouverture est flashée
    if (isActive) {
        enforceMinimumValues(nbTryInput, nbTopInput);
    }
}

// Fonction de vérification pour les restrictions de valeurs minimales
function enforceMinimumValues(nbTryInput, nbTopInput) {
    if (nbTopInput && +nbTopInput.value < 1) nbTopInput.value = 1;
    if (nbTryInput && +nbTryInput.value < 1) nbTryInput.value = 1;
}