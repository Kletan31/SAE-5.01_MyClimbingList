// noinspection JSUnusedGlobalSymbols
export function toggleMenu() {
    const voieBtn = document.querySelector('.menu-item:nth-child(1)');
    const blocBtn = document.querySelector('.menu-item:nth-child(2)');
    const voieCount = document.getElementById('voieCount');
    const blocCount = document.getElementById('blocCount');
    const voieContainer = document.getElementById('projetsVoie');
    const blocContainer = document.getElementById('projetsBloc');

    voieBtn.addEventListener('click', () => {
        voieBtn.classList.add('selected');
        blocBtn.classList.remove('selected');
        voieCount?.classList.remove('d-none');
        blocCount?.classList.add('d-none');
        voieContainer?.classList.remove('d-none');
        blocContainer?.classList.add('d-none');
        initializeTogglerScrollableClass();  // Vérifier les bordures
    });

    blocBtn.addEventListener('click', () => {
        blocBtn.classList.add('selected');
        voieBtn.classList.remove('selected');
        blocCount?.classList.remove('d-none');
        voieCount?.classList.add('d-none');
        blocContainer?.classList.remove('d-none');
        voieContainer?.classList.add('d-none');
        initializeTogglerScrollableClass();  // Vérifier les bordures
    });
}
