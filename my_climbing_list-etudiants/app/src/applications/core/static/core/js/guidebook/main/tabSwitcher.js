// noinspection JSUnusedGlobalSymbols
export function initializeTabSwitcher() {
    const elements = {
        // Menu
        menu: {
            voie: document.getElementById('voie-tab'),
            bloc: document.getElementById('bloc-tab'),
        },
        // Map
        map: {
            icon: {
                faMap: document.querySelector('.fa-map'),
                faList: document.querySelector('.fa-list-ul'),
            },
            plans: {
                voie: document.getElementById('voie-map-pinch-zoom-container'),
                bloc: document.getElementById('bloc-map-pinch-zoom-container'),
            }
        },
        // Fenêtre Tableau
        tableContainer: {
            tableWrapper: document.querySelector('.scrollable-container'),
            heads: {
                voie: document.getElementById('voie-head'),
                bloc: document.getElementById('bloc-head'),
            },
            tables: {
                voie: document.querySelector('.voie-table'),
                bloc: document.querySelector('.bloc-table'),
            },
            infos: {
                voie: document.querySelector('.voie-info'),
                bloc: document.querySelector('.bloc-info'),
            },
        },
        // Champ caché pour stocker l'état (bloc/voie)
        blocInput: document.getElementById('bloc-input'),
        // Albi
        isAlbi: document.querySelector(".top-bar p").textContent === "Albi",
    };

    function toggleElements(isBloc) {
        // Mise à jour des onglets actifs
        elements.menu.voie?.classList.toggle('selected', !isBloc);
        elements.menu.bloc?.classList.toggle('selected', isBloc);

        // Basculer l'affichage des différentes sections
        Object.keys(elements.tableContainer.heads).forEach(key => elements.tableContainer.heads[key]?.classList.toggle('d-none', key !== (isBloc ? 'bloc' : 'voie')));
        Object.keys(elements.tableContainer.tables).forEach(key => elements.tableContainer.tables[key]?.classList.toggle('d-none', key !== (isBloc ? 'bloc' : 'voie')));
        Object.keys(elements.map.plans).forEach(key => elements.map.plans[key]?.classList.toggle('d-none', key !== (isBloc ? 'bloc' : 'voie')));
        Object.keys(elements.tableContainer.infos).forEach(key => elements.tableContainer.infos[key]?.classList.toggle('d-none', key !== (isBloc ? 'bloc' : 'voie')));

        // Met à jour l'input caché
        elements.blocInput.value = isBloc;

        // Restore la position de défilement si le topo est en mode "liste"
        if (elements.map.icon.faList.classList.contains('d-none')) {
            restoreScrollPosition(elements.tableContainer.tableWrapper);
        }

        // Gestion des cercles matérialisant les relais / secteurs si le topo est en mode "map"
        if (elements.map.icon.faMap.classList.contains('d-none')) {
            const circles = document.querySelectorAll("#voie circle, #bloc circle");
            const activeId = isBloc ? sessionStorage.getItem("active-secteur") : sessionStorage.getItem("active-relais");
            // Affiche les relais / secteur de la discipline sélectionnée
            toggleDiscipline(circles);
            // Désactive tous les relais
            resetCircles(circles);
            // Activation du relais / secteur précédemment sélectionné
            activateElementAndUpdateRows(activeId);
        }

        // Gestion de l'étage d'Albi
        elements.isAlbi && document.getElementById("etage")?.classList.toggle("d-none", !isBloc);
    }

    // Ajout des événements aux onglets
    elements.menu.voie?.addEventListener('click', () => toggleElements(false));
    elements.menu.bloc?.addEventListener('click', () => toggleElements(true));
}