// noinspection JSUnusedGlobalSymbols
export function initializeSorting() {
    const headerConfigs = [
        { headId: "voie-head", tableClass: "voie-table" },
        { headId: "bloc-head", tableClass: "bloc-table" }
    ];

    headerConfigs.forEach(({ headId, tableClass }) => {
        const head = document.getElementById(headId);
        const tableContainer = document.querySelector(`.${tableClass}`);
        if (!head || !tableContainer) return;

        head.querySelectorAll('.title-column').forEach(header => {
            // Stocke le nom d’origine une fois
            if (!header.dataset.label) {
                header.dataset.label = header.textContent.trim();
            }

            header.addEventListener('click', () => {
                const headerText = header.dataset.label.toLowerCase();
                const isRelais = headerText.includes("relais") || headerText.includes("secteur");
                const isCotation = headerText.includes("cotation");

                if (!isRelais && !isCotation) return;

                const table = tableContainer.querySelector('table');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const columnIndex = Array.from(header.parentNode.children).indexOf(header);
                const isAsc = header.dataset.sortOrder !== 'asc';

                header.dataset.sortOrder = isAsc ? 'asc' : 'desc';

                // Réinitialise tous les en-têtes avec leur texte original
                head.querySelectorAll('.title-column').forEach(h => {
                    h.innerHTML = h.dataset.label;
                    h.removeAttribute('data-sort-order');
                });

                // Ajoute la flèche
                header.innerHTML = header.dataset.label + (isAsc ? ' ↑' : ' ↓');
                header.dataset.sortOrder = isAsc ? 'asc' : 'desc';

                rows.sort((a, b) => {
                    const aVal = a.children[columnIndex]?.textContent.trim();
                    const bVal = b.children[columnIndex]?.textContent.trim();
                    return compareAlphaNumeric(aVal, bVal, isAsc);
                });

                tbody.innerHTML = '';
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });
}

function compareAlphaNumeric(a, b, isAsc) {
    const result = a.localeCompare(b, 'fr', { numeric: true, sensitivity: 'base' });
    return isAsc ? result : -result;
}