// === Fonction pour initialiser l'état de la page et gérer les événements ===
// noinspection JSUnusedGlobalSymbols
export function initializeSessionState() {

    // Sauvegarde de la date de la séance à chaque modification
    const dateInput = document.querySelector('input[name="date_seance"]');
    const today = new Date().toISOString().split("T")[0];

    // Empêcher la saisie d'une date future
    dateInput.addEventListener("change", function () {
        if (dateInput.value > today) {
            dateInput.value = today; // Remet la valeur à aujourd’hui
        }
        saveState();
    });

    // Sauvegarde des montées et des tops à chaque modification
    document.querySelectorAll('input[name^="nb_"]').forEach(input => {
        input.addEventListener('input', saveState);
    });

   // Sauvegarde de l'état des icônes flash à chaque modification
   document.querySelectorAll('.flash-icon').forEach(flashIcon => {
        flashIcon.addEventListener('click', saveState);
    });

    // Initialiser l'état de la page avec les valeurs sauvegardées
    restoreState();
}

// === Fonction de sauvegarde de l'état dans sessionStorage ===
function saveState() {
    const dateSeanceInput = document.querySelector('input[name="date_seance"]');
    const routeItems = document.querySelectorAll('.route-item');

    // Sauvegarde la date de la séance
    sessionStorage.setItem('date_seance', dateSeanceInput.value);

    // Sauvegarde des informations de chaque voie
    routeItems.forEach(routeItem => {
        const routeId = routeItem.dataset.routeId;

        // Sauvegarde le nombre de montées et de réussites [MOULINETTE]
        const nbTry = routeItem.querySelector(`input[name="nb_try_${routeId}"]`).value;
        const nbTop = routeItem.querySelector(`input[name="nb_top_${routeId}"]`).value;

        sessionStorage.setItem(`nb_try_${routeId}`, nbTry);
        sessionStorage.setItem(`nb_top_${routeId}`, nbTop);

        // Sauvegarde le nombre de montées et de tops en tête [TÊTE]
        const nbTryLeadInput = routeItem.querySelector(`input[name="nb_try_${routeId}_lead"]`);
        const nbTopLeadInput = routeItem.querySelector(`input[name="nb_top_${routeId}_lead"]`);

        if (nbTryLeadInput) {
            sessionStorage.setItem(`nb_try_${routeId}_lead`, nbTryLeadInput.value);
        }

        if (nbTopLeadInput) {
            sessionStorage.setItem(`nb_top_${routeId}_lead`, nbTopLeadInput.value);
        }

        // Sauvegarde l'état des icônes flash
        const flashIcon = routeItem.querySelector(`.flash-icon`);
        const flashIconLead = routeItem.querySelector('.flash-icon[data-flash-type="lead"]');

        if (flashIcon) {
            sessionStorage.setItem(`flash_${routeId}`, flashIcon.classList.contains('active') ? 'true' : 'false');
        }
        if (flashIconLead) {
            sessionStorage.setItem(`flash_${routeId}_lead`, flashIconLead.classList.contains('active') ? 'true' : 'false');
        }
    });
}

// === Fonction de restauration de l'état à partir de sessionStorage ===
function restoreState() {
    const dateSeanceInput = document.querySelector('input[name="date_seance"]');
    const routeItems = document.querySelectorAll('.route-item');

    // Restaure la date de la séance
    const savedDateSeance = sessionStorage.getItem('date_seance');
    if (savedDateSeance) dateSeanceInput.value = savedDateSeance;

    // Restaure les informations pour chaque voie
    routeItems.forEach(routeItem => {
        const routeId = routeItem.dataset.routeId;

        // Restaure le nombre de montées et de réussites (moulinette)
        const savedNbTry = sessionStorage.getItem(`nb_try_${routeId}`);
        const savedNbTop = sessionStorage.getItem(`nb_top_${routeId}`);

        if (savedNbTry) routeItem.querySelector(`input[name="nb_try_${routeId}"]`).value = savedNbTry;
        if (savedNbTop) routeItem.querySelector(`input[name="nb_top_${routeId}"]`).value = savedNbTop;

        // Restaure le nombre de montées et de réussites en tête
        const savedNbTryLead = sessionStorage.getItem(`nb_try_${routeId}_lead`);
        const savedNbTopLead = sessionStorage.getItem(`nb_top_${routeId}_lead`);

        if (savedNbTryLead) routeItem.querySelector(`input[name="nb_try_${routeId}_lead"]`).value = savedNbTryLead;
        if (savedNbTopLead) routeItem.querySelector(`input[name="nb_top_${routeId}_lead"]`).value = savedNbTopLead;

        // Restaure l'état des icônes flash
        const flashIcon = routeItem.querySelector(`.flash-icon`);
        const flashIconLead = routeItem.querySelector('.flash-icon[data-flash-type="lead"]');

        if (flashIcon) {
            const savedFlash = sessionStorage.getItem(`flash_${routeId}`);
            flashIcon.classList.toggle('active', savedFlash === 'true');
            routeItem.querySelector(`input[name="flash_${routeId}"]`).value = savedFlash;
        }
        if (flashIconLead) {
            const savedFlashLead = sessionStorage.getItem(`flash_${routeId}_lead`);
            flashIconLead.classList.toggle('active', savedFlashLead === 'true');
            routeItem.querySelector(`input[name="flash_${routeId}_lead"]`).value = savedFlashLead;
        }
    });
}