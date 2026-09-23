// noinspection JSUnusedGlobalSymbols
export function initializeLogbookFilter() {
    const flashIcon = document.getElementById("flash-icon");
    const leadIcon = document.getElementById("lead-icon");
    const rows = document.querySelectorAll(".main-row");
    const message = document.getElementById("no-matching-routes");
    const routeCount = document.getElementById("routeCount");

    if (!routeCount) return;

    const singularLabel = routeCount.dataset.labelSingular;
    const pluralLabel = routeCount.dataset.labelPlural;

    function isSelected(icon) {
        return icon && icon.classList.contains("selected");
    }

    function updateCount(visibleCount) {
        const label = visibleCount === 1 ? singularLabel : pluralLabel;
        routeCount.textContent = `${visibleCount} ${label}`;
    }

    function updateFilter() {
        const flashOn = isSelected(flashIcon);
        const leadOn = isSelected(leadIcon);
        let visibleCount = 0;

        rows.forEach(mainRow => {
            const flashed = mainRow.dataset.flashed === "true";
            const leaded = mainRow.dataset.leaded === "true";
            const detailsRow = mainRow.nextElementSibling;

            let visible = true;

            if (flashOn && leadOn) {
                visible = flashed && leaded;
            } else if (flashOn) {
                visible = flashed;
            } else if (leadOn) {
                visible = leaded;
            }

            mainRow.style.display = visible ? "" : "none";
            if (detailsRow && detailsRow.classList.contains("details-row")) {
                detailsRow.style.display = visible ? "" : "none";
            }

            if (visible) visibleCount++;
        });

        if (message) {
            message.style.display = visibleCount === 0 ? "block" : "none";
        }

        updateCount(visibleCount);
    }

    function toggleIcon(icon) {
        if (!icon) return;
        icon.classList.toggle("selected");
        updateFilter();
    }

    if (flashIcon) flashIcon.addEventListener("click", () => toggleIcon(flashIcon));
    if (leadIcon) leadIcon.addEventListener("click", () => toggleIcon(leadIcon));

    updateFilter(); // initialisation
}