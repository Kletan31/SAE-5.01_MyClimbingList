// noinspection JSUnusedGlobalSymbols
export function toggleMenuAndData() {
    const menuItems = document.querySelectorAll('.menu-item');
    const voieData = document.querySelector('.voie-data');
    const blocData = document.querySelector('.bloc-data');
    const feedbackLink = document.getElementById('feedback-link');
    const settingsLink = document.getElementById('settings-link');

    if (!menuItems || !voieData || !blocData) {
        console.warn("Menu items or data containers not found!");
        return;
    }

    // Détecte la langue à partir du chemin
    const langPrefix = window.location.pathname.split('/')[1] || 'fr';
    const basePath = `/${langPrefix}`;

    menuItems.forEach((item) => {
        item.addEventListener('click', () => {
            // Retire la sélection actuelle
            menuItems.forEach((el) => el.classList.remove('selected'));
            item.classList.add('selected');

            const key = item.dataset.key;

            if (key === 'voie') {
                voieData.classList.remove('d-none');
                blocData.classList.add('d-none');
                feedbackLink.href = `${basePath}/core/feedback/?bloc=false`;
                settingsLink.href = `${basePath}/core/settings/?bloc=false`;
            } else if (key === 'bloc') {
                blocData.classList.remove('d-none');
                voieData.classList.add('d-none');
                feedbackLink.href = `${basePath}/core/feedback/?bloc=true`;
                settingsLink.href = `${basePath}/core/settings/?bloc=true`;
            }
        });
    });
}