function hideEmptyRelais(isBloc) {
    // Sélection des lignes selon la table
    const blocRows = document.querySelectorAll(".bloc-table tr");
    const voieRows = document.querySelectorAll(".voie-table tr");
    // Créer un Set pour stocker les identifiants uniques
    const uniqueIds = new Set();
    
    // Fonction générique pour traiter les lignes et former les identifiants à partir des numéros
    function processRows(rows, prefix) {
        rows.forEach(row => {
            const relaisValue = row.querySelector("td.toggle-column").textContent.trim();
            uniqueIds.add(prefix + relaisValue);
        });
    }

    // Traiter les deux groupes de lignes
    processRows(blocRows, "S");
    processRows(voieRows, "R");

    // Sélectionne les zones bloc et voie
    const zones = document.querySelectorAll("#bloc, #voie");

    // Parcourir chaque zone pour supprimer les relais / secteurs vides
    zones.forEach(zone => {
        const relaisElements = zone.querySelectorAll(":scope > *");
        relaisElements.forEach(relais => {
            // Vérifier si l'élément doit être supprimé
            if (!uniqueIds.has(relais.id)) {
                relais.remove();
                return; // Terminer ici pour éviter d'exécuter la suite inutilement
            }
            // Ajouter la classe "d-none" en fonction de la discipline sélectionnée (bloc/voie)
            const shouldHide = (!isBloc && relais.id[0] === "S") || (isBloc && relais.id[0] === "R");
            if (shouldHide) {
                relais.classList.add("d-none");
            }
        });
    });

    // Initialiser active-secteur dans sessionStorage
    const firstSecteurId = document.querySelector("#bloc g")?.id;
    firstSecteurId && sessionStorage.setItem("active-secteur", firstSecteurId);
    // Initialiser active-relais dans sessionStorage
    const firstRelaisId = document.querySelector("#voie g")?.id;
    firstRelaisId && sessionStorage.setItem("active-relais", firstRelaisId);
}

// Attacher la fonction à window pour un accès global
window.hideEmptyRelais = hideEmptyRelais;