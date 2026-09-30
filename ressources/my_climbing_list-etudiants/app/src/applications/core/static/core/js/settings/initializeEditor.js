// noinspection JSUnusedGlobalSymbols
export function initializeEditableFields() {
    // Sélectionner toutes les icônes d'édition
    const editIcons = document.querySelectorAll('[id^="edit-"]');

    // Bouton de sauvegarde et messages
    const saveButton = document.getElementById('settings-save-button');
    const errorMessage = document.getElementById('error-msg');
    const confidentialityMessage = document.getElementById('confidentiality-msg');

    // Conteneur du champ "gender"
    const genderContainer = document.getElementById('gender-input');
    const hiddenGenderInput = document.getElementById('gender-value'); // Champ caché pour stocker la valeur du genre

    // Ajout des gestionnaires d'événements pour chaque champ
    editIcons.forEach((icon) => {
        const fieldName = icon.id.replace('edit-', '');
        const displayElement = document.getElementById(`${fieldName}-display`);
        const inputElement = document.getElementById(`${fieldName}-input`);
        const isGenderField = fieldName === 'gender';

        // Valeur initiale du champ
        const initialValue = isGenderField
            ? (genderContainer.querySelector('.selected')?.dataset.value)
            : inputElement.value;

        icon.addEventListener('click', () => toggleEditMode(icon, displayElement, inputElement, initialValue, isGenderField));

        // Détecter les modifications pour les champs autres que `gender`
        if (!isGenderField) {
            inputElement.addEventListener('input', checkForChanges);
        }
    });

    // Gestion des clics dans le conteneur "gender"
    genderContainer.addEventListener('click', (event) => {
        const clickedIcon = event.target;

        // Vérifier que l'élément cliqué est une icône
        if (clickedIcon.tagName === 'I') {
            updateGenderSelection(clickedIcon);
            checkForChanges();
        }
    });

    /**
     * Basculer entre le mode édition et le mode affichage.
     */
    function toggleEditMode(icon, displayElement, inputElement, initialValue, isGenderField) {
        const isEditing = !displayElement.classList.contains('d-none');

        if (isEditing) {
            // Passer en mode édition
            displayElement.classList.add('d-none');
            inputElement.classList.remove('d-none');
            icon.classList.replace('fa-pen', 'fa-pen-slash');
            inputElement.focus();
        } else {
            // Revenir en mode affichage
            displayElement.classList.remove('d-none');
            inputElement.classList.add('d-none');
            icon.classList.replace('fa-pen-slash', 'fa-pen');

            if (isGenderField) {
                resetGenderSelection(initialValue);
            } else {
                inputElement.value = initialValue;
            }
        }

        checkForChanges();
    }

    /**
     * Réinitialiser la sélection pour le champ `gender`.
     */
    function resetGenderSelection(initialValue) {
        const icons = genderContainer.querySelectorAll('i');
        icons.forEach(icon => icon.classList.remove('selected'));

        const initialIcon = genderContainer.querySelector(`[data-value="${initialValue}"]`);
        if (initialIcon) initialIcon.classList.add('selected');

        hiddenGenderInput.value = initialValue;
    }

    /**
     * Mettre à jour la sélection pour le champ `gender`.
     */
    function updateGenderSelection(clickedIcon) {
        const icons = genderContainer.querySelectorAll('i');
        icons.forEach(icon => icon.classList.remove('selected'));

        clickedIcon.classList.add('selected');

        hiddenGenderInput.value = clickedIcon.dataset.value;
    }

    /**
     * Vérifier si des modifications ont été apportées.
     */
    function checkForChanges() {
        let hasChanges = false;

        editIcons.forEach((icon) => {
            const fieldName = icon.id.replace('edit-', '');
            const inputElement = document.getElementById(`${fieldName}-input`);
            const displayElement = document.getElementById(`${fieldName}-display`);

            if (fieldName === 'gender') {
                const selectedValue = genderContainer.querySelector('.selected')?.dataset.value;
                const initialValue = displayElement.querySelector(':not(.d-none)')?.dataset.value;

                if (selectedValue !== initialValue) {
                    hasChanges = true;
                }
            } else if (inputElement && displayElement) {
                if (inputElement.value.trim() !== displayElement.textContent.trim()) {
                    hasChanges = true;
                }
            }
        });

        // Gérer l'affichage du bouton et des messages
        saveButton.classList.toggle('d-none', !hasChanges);
        confidentialityMessage.classList.toggle('d-none', hasChanges);
        errorMessage.classList.add('d-none');
    }
}
