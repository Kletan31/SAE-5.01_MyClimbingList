// refreshGraph.js — version compatible i18n + data-key
// noinspection JSUnusedGlobalSymbols
export function displayGraph() {

    /**
     * Met à jour le graphique avec les données reçues
     */
    function updateGraph(graphData) {
        const graphContainer = document.getElementById('graph');
        Plotly.newPlot(
            graphContainer,
            JSON.parse(graphData.graph).data,
            JSON.parse(graphData.graph).layout,
            {
                displayModeBar: false,
                staticPlot: true,
                responsive: true,
            }
        );
    }

    /**
     * Met à jour les informations de moulinette et tête
     */
    function updateTotals(totalMoulinette, totalTete) {
        const moulinetteTotalElement = document.querySelector('#data-container .total span');
        const teteTotalElement = document.querySelector('#data-container .total-lead span');

        if (moulinetteTotalElement) {
            const width = `calc(0.5rem + 0.9 * ${totalMoulinette.toString().length}rem)`;
            moulinetteTotalElement.textContent = totalMoulinette;
            moulinetteTotalElement.style.width = width;
        }

        if (teteTotalElement) {
            const width = `calc(0.5rem + 0.9 * ${totalTete.toString().length}rem)`;
            teteTotalElement.textContent = totalTete;
            teteTotalElement.style.width = width;
        }
    }

    /**
     * Met à jour les statistiques des profils (basé sur data-key)
     */
    function updateProfiles(profilsStats) {
        profilsStats.forEach(profil => {
            const profilElements = document.querySelectorAll('#profilRow .style-profil');
            const profilElement = Array.from(profilElements).find(
                el => el.dataset.key === profil.profil
            );

            if (profilElement && profilElement.nextElementSibling) {
                profilElement.nextElementSibling.innerHTML =
                    `${profil.percentage}% <span style="vertical-align:.05rem;">|</span> ${profil.total}`;
            }
        });
    }

    /**
     * Met à jour les statistiques des styles (basé sur data-key)
     */
    function updateStyles(stylesStats) {
        stylesStats.forEach(style => {
            const styleElements = document.querySelectorAll('#style-data-container .style-profil');
            const styleElement = Array.from(styleElements).find(
                el => el.dataset.key === style.style
            );

            if (styleElement && styleElement.nextElementSibling) {
                styleElement.nextElementSibling.innerHTML =
                    `${style.percentage}% <span style="vertical-align:.05rem;">|</span> ${style.total}`;
            }
        });
    }

    /**
     * Met à jour le nombre total d'ouvertures
     */
    function updateTotalOuvertures(totalOuvertures) {
        const totalOuvertureElement = document.getElementById('totalOuverture');
        if (totalOuvertureElement) {
            totalOuvertureElement.textContent = `${totalOuvertures} ouvertures disponibles`;
        }
    }

    /**
     * Rafraîchit le graphique en envoyant une requête au serveur (compatible i18n)
     */
    async function refreshGraph() {
        const langPrefix = window.location.pathname.split('/')[1] || 'fr';
        const baseUrl = `/${langPrefix}/core/properties/refresh/`;

        const salleId = window.location.pathname.split('/')
            .filter(segment => segment !== '')
            .pop();

        const selectedTypeElement = document.querySelector('.menu-item.selected');
        const type = selectedTypeElement && selectedTypeElement.dataset.category === "bloc";

        const selectedStyles = Array.from(
            document.querySelectorAll('#style-data-container .selected')
        ).map(el => el.dataset.key);

        const selectedProfiles = Array.from(
            document.querySelectorAll('#profil-data-container .selected')
        ).map(el => el.dataset.key);

        const requestData = {
            salle_id: salleId,
            type: type,
            styles: selectedStyles,
            profiles: selectedProfiles,
        };

        try {
            const response = await fetch(baseUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(requestData),
            });

            const data = await csrfErrorChecker(response);
            if (!data) {
                window.location.href = `/${langPrefix}/core/offline/`;
                return;
            }

            updateGraph(data);
            updateTotals(data.total_moulinette, data.total_tete);
            updateProfiles(data.profils_stats);
            updateStyles(data.styles_stats);
            updateTotalOuvertures(data.total_ouvertures);
        } catch (error) {
            console.error("Erreur lors du rafraîchissement du graphique :", error);
            window.location.href = `/${langPrefix}/core/offline/`;
        }
    }

    /**
     * Initialise les écouteurs sur les boutons pour rafraîchir le graphique
     */
    function initializeListeners() {
        const buttons = document.querySelectorAll('.menu-item, .style-profil-container');
        buttons.forEach(button => {
            button.addEventListener('click', refreshGraph);
        });
    }

    // Initialisation
    initializeListeners();
    void refreshGraph();
}