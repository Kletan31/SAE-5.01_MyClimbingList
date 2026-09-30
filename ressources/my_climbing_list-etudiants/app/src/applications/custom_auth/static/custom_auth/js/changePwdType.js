// noinspection JSUnusedGlobalSymbols
export function initializeTogglePasswordFields() {
    // Trouver tous les éléments dont l'id commence par "toggle-password"
    const toggles = document.querySelectorAll('[id^="toggle-password"]');

    toggles.forEach(toggle => {
        // Trouver le champ de mot de passe correspondant
        const passwordFieldId = toggle.getAttribute('id').replace('toggle-', '');
        const passwordField = document.getElementById(passwordFieldId);

        if (passwordField) {
            toggle.addEventListener('click', function () {
                // Bascule entre type "password" et "text"
                const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordField.setAttribute('type', type);

                // Bascule entre les icônes fa-eye et fa-eye-slash
                this.classList.toggle('fa-eye');
                this.classList.toggle('fa-eye-slash');
            });
        }
    });
}