// Créer un défilement fluide [ease]
function smoothScrollTo(element, duration){
    const target = element.scrollHeight - element.clientHeight;
    const start = element.scrollTop;
    const distance = target - start;

    let startTime = null;

    const ease = (t) => t * (2 - t); // Interpolation ease standard

    const step = (timestamp) => {
        if (!startTime) startTime = timestamp;
        const progress = (timestamp - startTime) / duration;
        const easedProgress = ease(Math.min(progress, 1));

        element.scrollTop = start + distance * easedProgress;

        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            element.scrollTop = target; // Assure la position finale
        }
    };

    window.requestAnimationFrame(step);
}

// Calcule la hauteur d'un dropdown
function calculateDropdownHeight(){
    const tempElement = document.createElement("div");
    tempElement.style.visibility = "hidden";
    tempElement.style.position = "absolute";
    tempElement.style.height = "var(--dropdown-height)";
    document.body.appendChild(tempElement);

    const dropdownHeight = tempElement.offsetHeight;
    document.body.removeChild(tempElement);

    return dropdownHeight;
}

// Attacher la fonction à window pour un accès global
window.smoothScrollTo = smoothScrollTo;
window.calculateDropdownHeight = calculateDropdownHeight;