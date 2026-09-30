// Fonction pour convertir une chaîne en tableau
function stringToArray(str) {
    return str ? str.split(',') : [];
}

// Attacher la fonction à window pour un accès global
window.stringToArray = stringToArray;