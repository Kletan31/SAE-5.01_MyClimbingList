document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("a[href]:not([target])").forEach(link => {
        if (link.dataset.preload === "false") return;

        link.addEventListener("click", function (e) {
            const href = link.getAttribute("href");

            // Ignorer les liens non navigables
            if (
                href.startsWith("javascript:") ||
                href.startsWith("#") ||
                link.hasAttribute("download") ||
                e.ctrlKey || e.metaKey || e.shiftKey || e.altKey
            ) return;

            e.preventDefault();
            preloadView();

            requestAnimationFrame(() => {
                setTimeout(() => {
                    window.location.href = link.href;
                }, 50);
            });
        });
    });
});