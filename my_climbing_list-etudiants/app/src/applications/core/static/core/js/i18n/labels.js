// static/js/i18n/labels.js

export const LABEL_TRANSLATIONS = {
    fr: {
        dalle: "dalle",
        dièdre: "dièdre",
        dévers: "dévers",
        toit: "toit",
        vertical: "vertical",
        bloc: "bloc",
        conti: "conti",
        rési: "rési",
        classic: "classic",
        physic: "physic",
        technic: "technic",
        coordo: "coordo",
        tricky: "tricky",
        undefined: "non défini",
    },
    en: {
        dalle: "slab",
        dièdre: "dihedral",
        dévers: "overhang",
        toit: "roof",
        vertical: "vertical",
        bloc: "cruxy",
        conti: "stamina",
        rési: "p-endur",
        classic: "classic",
        physic: "physical",
        technic: "technical",
        coordo: "coordination",
        tricky: "tricky",
        undefined: "undefined",
    },
    es: {
        dalle: "placa",
        dièdre: "diedro",
        dévers: "desplome",
        toit: "techo",
        vertical: "vertical",
        bloc: "bloque",
        conti: "continuidad",
        rési: "resistencia",
        classic: "clásico",
        physic: "físico",
        technic: "técnico",
        coordo: "coordinación",
        tricky: "tricky",
        undefined: "no definido",
    },
    pt: {
        dalle: "placa",
        dièdre: "diedro",
        dévers: "desplome",
        toit: "teto",
        vertical: "vertical",
        bloc: "bloco",
        conti: "continuidade",
        rési: "resistência",
        classic: "clássico",
        physic: "físico",
        technic: "técnico",
        coordo: "coordenação",
        tricky: "tricky",
        undefined: "não definido",
    },
};


/**
 * Traduit un label métier (FR) pour affichage.
 * Ne modifie jamais la valeur brute (clé / CSS).
 */
function getCurrentLang() {
    return window.location.pathname.split('/')[1] || 'fr';
}

export function translateLabel(value) {
    const lang = getCurrentLang();
    const dict = LABEL_TRANSLATIONS[lang] || LABEL_TRANSLATIONS.fr;

    return dict[value] || dict.undefined || value;
}