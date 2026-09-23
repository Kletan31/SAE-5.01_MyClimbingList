// noinspection JSUnusedGlobalSymbols
export function enableToggleButton(selector) {
    // Sélectionner tous les éléments correspondant au sélecteur
    const elements = document.querySelectorAll(selector);

    // Ajouter un événement de clic à chaque élément
    elements.forEach(element => {
        element.addEventListener("click", function () {
            // Si l'élément est déjà sélectionné, retirer la classe et terminer
            if (this.classList.contains("selected")) {
                this.classList.remove("selected");
                return;
            }

            // Ajouter la classe "selected" à l'élément cliqué
            this.classList.add("selected");
        });
    });
}