// noinspection JSUnusedGlobalSymbols
export function toggleMenuSelection(menuClass, selectedClass) {
    const menuItems = document.querySelectorAll(menuClass);
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove(selectedClass));
            item.classList.add(selectedClass);
            displayGraph();
        });
    });
}