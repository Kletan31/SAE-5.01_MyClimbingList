document.addEventListener("DOMContentLoaded", () => {
    let autoScrollEnabled = true;
    let scrollAccumulator = 0;

    const scrollSpeed = 0.6;
    const intervalDelay = 16;
    const pauseAtBottom = 3000;

    const toggleButton = document.getElementById("toggle-scroll");
    const scrollingElement = document.scrollingElement || document.documentElement;

    if (!toggleButton) {
        return;
    }

    toggleButton.addEventListener("click", () => {
        autoScrollEnabled = !autoScrollEnabled;

        if (autoScrollEnabled) {
            toggleButton.textContent = "Pause défilement";
            toggleButton.classList.remove("paused");
        } else {
            toggleButton.textContent = "Reprendre défilement";
            toggleButton.classList.add("paused");
        }
    });

    function getMaxScroll() {
        return scrollingElement.scrollHeight - window.innerHeight;
    }

    function scrollPage() {
        if (!autoScrollEnabled) {
            return;
        }

        const maxScroll = getMaxScroll();

        if (maxScroll <= 0) {
            return;
        }

        if (scrollingElement.scrollTop >= maxScroll - 2) {
            autoScrollEnabled = false;

            setTimeout(() => {
                scrollingElement.scrollTop = 0;
                autoScrollEnabled = true;
            }, pauseAtBottom);

            return;
        }

        scrollAccumulator += scrollSpeed;

        if (scrollAccumulator >= 1) {
            const pixelsToScroll = Math.floor(scrollAccumulator);
            scrollingElement.scrollTop += pixelsToScroll;
            scrollAccumulator -= pixelsToScroll;
        }
    }

    setInterval(scrollPage, intervalDelay);
});