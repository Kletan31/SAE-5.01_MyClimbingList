// noinspection JSUnusedGlobalSymbols
export function triggerDeleteProcess() {
    const triggerBtn = document.getElementById("trigger-account-delete");
    const popup = document.getElementById("delete-account-popup");
    const cancelBtn = document.getElementById("cancel-delete");

    triggerBtn.addEventListener("click", () => popup.classList.add('active'));
    cancelBtn.addEventListener("click", () => popup.classList.remove('active'));
}