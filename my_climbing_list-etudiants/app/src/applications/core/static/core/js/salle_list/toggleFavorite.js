document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('.favorite-toggle').forEach(el => {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const salleId = this.getAttribute('data-salle-id');
      const langCode = window.location.pathname.split("/")[1];  // ex: "fr" ou "en"
      const fetchUrl = `/${langCode}/core/favorite/toggle/`;

      fetch(fetchUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie('csrftoken'),
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ salle_id: salleId })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "set") {
          // Mettre l'étoile pleine sur l’élément courant et vider les autres
          document.querySelectorAll('.favorite-toggle i').forEach(i => {
            i.classList.remove('fa-solid', 'text-warning');
            i.classList.add('fa-regular', 'text-secondary');
          });
          const icon = this.querySelector('i');
          icon.classList.remove('fa-regular', 'text-secondary');
          icon.classList.add('fa-solid', 'text-warning');
        } else if (data.status === "unset") {
          const icon = this.querySelector('i');
          icon.classList.remove('fa-solid', 'text-warning');
          icon.classList.add('fa-regular', 'text-secondary');
        }
        navigator.serviceWorker.controller.postMessage({ action: 'CLEAR_SALLE_LIST_CACHE' });
      })
      .catch(err => console.error(err));
    });
  });
});