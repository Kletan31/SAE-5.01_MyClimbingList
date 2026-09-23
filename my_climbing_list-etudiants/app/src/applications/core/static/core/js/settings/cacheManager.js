// noinspection JSUnusedGlobalSymbols
export function setupSettingsCacheClearButton() {
    const saveButton = document.querySelector('#settings-save-button button');
    if (!saveButton) return;

    saveButton.addEventListener('click', () => {
        clearProjectsFromCache();
    });
}

function clearProjectsFromCache() {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
        navigator.serviceWorker.controller.postMessage({ action: 'CLEAR_SETTINGS_CACHE' });
    }
}