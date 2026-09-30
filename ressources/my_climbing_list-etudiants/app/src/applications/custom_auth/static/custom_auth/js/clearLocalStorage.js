// noinspection JSUnusedGlobalSymbols
export function clearLocalStorage() {
    localStorage.clear();
    if (LOG) console.log('LocalStorage effacé.');
}