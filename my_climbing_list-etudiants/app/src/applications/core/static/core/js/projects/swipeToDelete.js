// noinspection JSUnusedGlobalSymbols
export function swipeToDelete() {
    const swipeContainers = document.querySelectorAll(".swipe-container");

    swipeContainers.forEach(container => {
        const content = container.querySelector(".swipe-content");
        let startX = 0;
        let currentX = 0;
        let isSwiping = false;

        content.addEventListener("touchstart", function (e) {
            startX = e.touches[0].clientX;
            currentX = startX;
            isSwiping = true;
        });

        content.addEventListener("touchmove", function (e) {
            if (!isSwiping) return;
            currentX = e.touches[0].clientX;
            const deltaX = startX - currentX;
            if (deltaX > 0) {
                content.style.transform = `translateX(${-deltaX}px)`;
            }
        });

        content.addEventListener("touchend", function () {
            isSwiping = false;
            const deltaX = startX - currentX;

            if (deltaX > 80) {
                animateSwipeOut(container, content);
                updateProjectCount();
                updateProjectInDatabase(container.dataset.ouvertureId);
                clearProjectsFromCache();
            } else {
                // Retour à l'état initial
                content.style.transform = "translateX(0)";
            }
        });
    });
}


// Animation
function animateSwipeOut(container, content) {
    content.style.transform = "translateX(-100%)";

    container.style.height = `${container.offsetHeight}px`;
    void container.offsetHeight;
    container.style.height = "0px";

    setTimeout(() => {
        container.remove();
    }, 400);
}


// Mise à jour du compteur
function updateProjectCount() {
    const counters = document.querySelectorAll(".menu p");
    counters.forEach(p => {
        if (!p.classList.contains("d-none")) {
            const text = p.textContent;
            const isVoie = p.id === "voieCount";

            const match = text.match(/(\d+)/);
            let count = match ? parseInt(match[1], 10) - 1 : 0;

            if (count === 0) {
                p.textContent = isVoie ? "Aucune voie en projet" : "Aucun bloc en projet";
            } else {
                const type = isVoie ? "voie" : "bloc";
                const plural = count > 1 ? "s" : "";
                p.textContent = `${count} ${type}${plural} en projet`;
            }
        }
    });
}


// Mise à jour de la base de données
function updateProjectInDatabase(ouvertureId) {
    // Récupère le code langue depuis l'URL
    const langCode = window.location.pathname.split("/")[1];
    const fetchUrl = `/${langCode}/core/projects/refresh/`;

    fetch(fetchUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken'),
        },
        body: JSON.stringify({ ouverture_id: ouvertureId })
    })
    .then(response => {
        if (!response.ok) {
            console.error("Échec de la mise à jour du projet.");
        }
    })
    .catch(error => {
        console.error("Erreur réseau :", error);
    });
}


// Mise à jour du cache [SW]
function clearProjectsFromCache() {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
        navigator.serviceWorker.controller.postMessage({ action: 'CLEAR_PROJECTS_CACHE' });
    }
}