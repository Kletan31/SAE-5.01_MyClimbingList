document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".scrollable-container");
    const spinner = document.getElementById("loader-spinner");
    const offlineNotice = document.getElementById("offline-notice");
    const bottomInfo = container.querySelector(".bottom-info");

    let isLoading = false;
    let allLoaded = false;

    const initialCount = container.querySelectorAll(".seance-row").length;
    let offset = initialCount;
    let totalLoaded = initialCount;
    const limit = 10;

    if (bottomInfo) bottomInfo.style.display = "none";

    async function loadMoreSessions() {
        if (isLoading || allLoaded) return;

        if (!navigator.onLine) {
            showOfflineNotice();
            return;
        }

        isLoading = true;
        spinner.style.display = "block";
        offlineNotice.style.display = "none";

        try {
            const response = await fetch(`/core/load_more_sessions/?offset=${offset}&limit=${limit}`);
            const html = await response.text();

            if (!html.trim()) {
                allLoaded = true;
                spinner.style.display = "none";
                showBottomInfo();
                return;
            }

            // Insertion directe du fragment HTML rendu par Django
            spinner.insertAdjacentHTML("beforebegin", html);

            // Comptage du nombre réel de séances ajoutées
            const count = (html.match(/<a\b/gi) || []).length;
            offset += limit;
            totalLoaded += count;

        } catch (err) {
            console.error("Erreur lors du chargement des séances :", err);
            showOfflineNotice();
        } finally {
            spinner.style.display = "none";
            isLoading = false;
        }
    }

    function showOfflineNotice() {
        offlineNotice.style.display = "block";
        setTimeout(() => {
            offlineNotice.style.display = "none";
        }, 3000);
    }

    function showBottomInfo() {
        if (!bottomInfo) return;
        bottomInfo.style.display = "block";
        const p = bottomInfo.querySelector("p");
        const plural = totalLoaded > 1 ? "séances enregistrées" : "séance enregistrée";
        p.textContent = `${totalLoaded} ${plural}`;
    }

    function handleScroll() {
        const nearBottom =
            container.scrollTop + container.clientHeight >= container.scrollHeight - 100;
        if (nearBottom && !isLoading && !allLoaded) {
            void loadMoreSessions();
        }
    }

    container.addEventListener("scroll", handleScroll);
});