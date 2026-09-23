document.addEventListener('DOMContentLoaded', () => {
    const isAndroid = /android/i.test(navigator.userAgent);
    const isInStandaloneMode = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;

    const popup = document.getElementById('installPopup');
    const dismissButton = document.getElementById('popup-install-dismiss');
    const dismissTimestamp = localStorage.getItem('install-popup-dismissed-at');
    const now = Date.now();
    const twentyFourHours = 24 * 60 * 60 * 1000;

    const shouldShowPopup = !dismissTimestamp || now - parseInt(dismissTimestamp, 10) > twentyFourHours;

    if (isAndroid && !isInStandaloneMode && popup && shouldShowPopup) {
        const modal = new bootstrap.Modal(popup);
        modal.show();

        if (dismissButton) {
            dismissButton.addEventListener('click', () => {
                // On enlève le focus du bouton avant de cacher la popup
                document.activeElement.blur();

                localStorage.setItem('install-popup-dismissed-at', Date.now().toString());
                modal.hide();
            });
        }
    }
});