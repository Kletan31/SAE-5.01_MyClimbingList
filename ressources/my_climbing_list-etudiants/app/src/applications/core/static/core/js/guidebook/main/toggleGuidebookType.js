// noinspection JSUnusedGlobalSymbols
export function toggleGuidebookType() {
    // Récupération des éléments du DOM
    const elements = {
        mapGuidebook: document.getElementById('map-guidebook'),
        listGuidebook: document.getElementById('list-guidebook'),
        guidebookMapLink: document.getElementById('guidebook-type-link'),
        tabSwitcherButton: document.getElementById('bloc-tab'),
        mapIcon: document.querySelector('.fa-map'),
        listIcon: document.querySelector('.fa-list-ul'),
        scrollContainer: document.querySelector('.scrollable-container'),
        titleColumns: document.querySelectorAll('.title-column'),
        relaisColumns: document.querySelectorAll('.toggle-column'),
        tableRows: document.querySelectorAll('table tr'),
        tableDatas: document.querySelectorAll('table td'),
        mapInput: document.getElementById('map-input'),
    };
    
    // Flags d'initialisation
    let isMapInitialized = false;

    // Gestionnaire d'événement principal
    elements.guidebookMapLink.addEventListener('click', handleMapClick);

    async function handleMapClick() {
        const isBloc = elements.tabSwitcherButton?.classList.contains('selected') || false;
        const mapIsClicked = elements.listIcon.classList.contains('d-none'); // True → icône "map" cliqué
        await toggleDisplayStates(mapIsClicked, isBloc);
    }

    // Basculer les états d'affichage des éléments
    async function toggleDisplayStates(mapIsClicked, isBloc) {
        // Sous-pages
        elements.mapGuidebook.classList.toggle('d-none');
        elements.listGuidebook.classList.toggle('map-display');
        // Icônes
        elements.mapIcon.classList.toggle('d-none');
        elements.listIcon.classList.toggle('d-none');
        // Input
        elements.mapInput.value = mapIsClicked ? 'true' : 'false';
        // Initialisation conditionnelle du plan
        await checkForInitializingMap(isBloc)
        // Change le mode du tableau (liste / plan)
        changeTableMode(mapIsClicked);
        // Actualiser l'URL
        changeURL(mapIsClicked);
        // Afficher les ouvertures du relais sélectionné sur le plan
        mapIsClicked && displayActiveRelais(isBloc);
        // Restaurer la position de défilement dans le tableau (si l'icône "list" est cliqué)
        !mapIsClicked && restoreScrollPosition(elements.scrollContainer);

        // Partie spécifique à Albi
        elements.etageBlocAlbi?.classList.toggle("d-none", !isBloc);
    }

    // Check si le plan doit-être initialisé
    async function checkForInitializingMap(isBloc) {
        if (!isMapInitialized) {
            await initializeMap(isBloc);
            isMapInitialized = true;
        }
    }

    // Gérer la logique pour initialiser le plan
    async function initializeMap(isBloc) {
        await fetchSVG();                               // Charger le SVG
        initializePinchZoom();                          // Initialiser PinchZoom
        hideEmptyRelais(isBloc);                        // Masquer les relais vides
        relaisLogic(isBloc, elements.scrollContainer);  // Ajouter la logique des relais

        // Gestion du cas particulier : Albi
        if (document.querySelector("svg").id === "albi") {
            elements.etageBlocAlbi = document.getElementById("etage");
        }
    }

    function changeTableMode(mapIsClicked) {
        elements.relaisColumns.forEach(el => el.classList.toggle('d-none'));
        elements.tableRows.forEach(el => el.classList.toggle('d-none', mapIsClicked));
        elements.titleColumns.forEach(el => el.classList.toggle('map-display'));
        elements.tableDatas.forEach(el => el.classList.toggle('map-display'));
    }

    function changeURL(mapIsClicked) {
        const url = new URL(window.location.href);
        url.searchParams.set("map_display", mapIsClicked.toString());
        history.pushState(null, "", url.toString());
    }

    function displayActiveRelais(isBloc) {
        // Récupération du dernier relais/secteur sélectionné
        const elementId = isBloc ?
            sessionStorage.getItem("active-secteur"):
            sessionStorage.getItem("active-relais");

        // Met à jour les lignes du tableau et active le relais sélectionné
        activateElementAndUpdateRows(elementId);
    }

    // Affichage en mode plan dès le chargement si demandé
    if (elements.mapInput.value.toLowerCase() === 'true') {
        const isBloc = elements.tabSwitcherButton?.classList.contains('selected') || false;
        void checkForInitializingMap(isBloc);   // Initialise le plan et ignore le résultat de la fonction asynchrone
    }
}