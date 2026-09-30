// noinspection JSUnusedGlobalSymbols
export function enableToggleType() {
    // Initialisation des événements pour les éléments du menu
    const elements = document.querySelectorAll(".menu-item");

    elements.forEach(element => {
        element.addEventListener("click", function () {
            handleMenuSelection(elements, this);
            resetProfileSelection();
            toggleRowsBasedOnCategory(this.getAttribute("data-category"));
            updateAscensionContainer(this.getAttribute("data-category"));
        });
    });
}

// Gestion de la sélection du menu
function handleMenuSelection(elements, selectedElement) {
    elements.forEach(el => el.classList.remove("selected"));
    selectedElement.classList.add("selected");
}

// Réinitialisation de la sélection des profils
function resetProfileSelection() {
    const profilRow = document.getElementById('profilRow');
    profilRow.querySelectorAll(".selected").forEach(child => child.classList.remove("selected"));
}

// Basculer les lignes correspondantes en fonction de la catégorie
function toggleRowsBasedOnCategory(category) {
    const rows = document.querySelectorAll("#style-data-container .d-flex");
    const matchingClass = `w-${category === "voie" ? "75" : "100"}`;

    rows.forEach(row => {
        if (row.classList.contains(matchingClass)) {
            row.classList.remove("d-none"); // Afficher la ligne correspondante
        } else {
            row.classList.add("d-none"); // Masquer les autres lignes
        }
        // Toujours réinitialiser la classe "selected" des enfants
        row.querySelectorAll(".selected").forEach(child => child.classList.remove("selected"));
    });
}

// Mise à jour de l'affichage dans le conteneur d'ascension
function updateAscensionContainer(category) {
    const ascensionContainer = document.getElementById("data-container");
    const moulinette = ascensionContainer.querySelector(".total");
    const tete = ascensionContainer.querySelector(".total-lead");
    const moulinetteText = document.getElementById("moulinetteText");
    const blocText = document.getElementById("blocText");

    if (category === "bloc") {
        // Masquer la barre verticale et la tête, ajuster la moulinette
        tete.classList.add("d-none");
        moulinetteText.classList.add("d-none");
        blocText.classList.remove("d-none");
        moulinette.classList.remove("col-6");
    } else {
        // Afficher la barre verticale et la tête, restaurer la moulinette
        tete.classList.remove("d-none");
        moulinetteText.classList.remove("d-none");
        blocText.classList.add("d-none");
        moulinette.classList.add("col-6");
    }
}