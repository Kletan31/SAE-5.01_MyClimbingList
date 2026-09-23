document.addEventListener("DOMContentLoaded", () => {
    const threshold = 100;
    const indicator = document.getElementById("pull-indicator");

    let startY = 0;
    let isPulling = false;
    let deltaY = 0;
    let isTriggered = false;
    let scrollableTarget = null;

    // === Détection du conteneur scrollable le plus proche ===
    function findScrollableAncestor(el) {
        while (el && el !== document.body) {
            const style = window.getComputedStyle(el);
            if (/(auto|scroll)/.test(style.overflowY) && el.scrollHeight > el.clientHeight) {
                return el;
            }
            el = el.parentElement;
        }
        return null;
    }

    // === Touch start ===
    function onTouchStart(e) {
        const target = e.target;
        scrollableTarget = findScrollableAncestor(target);
        const canStart =
            !scrollableTarget || scrollableTarget.scrollTop === 0;

        if (canStart) {
            startY = e.touches[0].clientY;
            isPulling = true;
            isTriggered = false;
            indicator.classList.add("active");
            indicator.style.top = "-50px";
        } else {
            isPulling = false;
        }
    }

    // === Touch move ===
    function onTouchMove(e) {
        if (!isPulling) return;
        deltaY = e.touches[0].clientY - startY;
        if (deltaY > 0) {
            e.preventDefault();
            const offset = Math.min(deltaY / 2, 120);
            indicator.style.top = `${offset - 50}px`;
            isTriggered = deltaY > threshold;
        }
    }

    // === Touch end ===
    function onTouchEnd() {
        indicator.style.top = "-50px";
        indicator.style.opacity = "0";
        indicator.classList.remove("active");

        if (isTriggered) {
            preloadView();
            triggerPullToRefresh();
        }

        isPulling = false;
        scrollableTarget = null;
    }

    // === Rafraîchissement ===
    function triggerPullToRefresh() {
        if (navigator.serviceWorker?.controller) {
            // Envoie les deux actions au Service Worker
            navigator.serviceWorker.controller.postMessage({ action: "CLEAR_CONTESTS_CACHE" });
            navigator.serviceWorker.controller.postMessage({ action: "CLEAR_PROJECTS_CACHE" });

            // Recharge après un petit délai (pour laisser le SW purger)
            setTimeout(() => window.location.reload(), 700);
        } else {
            console.warn("Service Worker non disponible.");
        }
    }

    // === Ajout global des écouteurs ===
    document.addEventListener("touchstart", onTouchStart, { passive: true });
    document.addEventListener("touchmove", onTouchMove, { passive: false });
    document.addEventListener("touchend", onTouchEnd);
});