function getCsrfToken() {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');

    if (!csrfInput) {
        return "";
    }

    return csrfInput.value;
}

function updateOrderCell(routeId, newOrder) {
    const row = document.querySelector(`[data-route-id="${routeId}"]`);

    if (!row) {
        return;
    }

    const orderCell = row.querySelector("[data-order-cell]");

    if (orderCell) {
        orderCell.textContent = newOrder;
    }
}

function flashUpdatedRow(row) {
    row.classList.add("route-updated");

    setTimeout(() => {
        row.classList.remove("route-updated");
    }, 500);
}

function moveRowInDom(direction, movedRouteId, swappedRouteId) {
    const movedRow = document.querySelector(`[data-route-id="${movedRouteId}"]`);
    const swappedRow = document.querySelector(`[data-route-id="${swappedRouteId}"]`);
    const tbody = document.querySelector("#route-order-body");

    if (!movedRow || !swappedRow || !tbody) {
        return;
    }

    if (direction === "up") {
        tbody.insertBefore(movedRow, swappedRow);
    }

    if (direction === "down") {
        tbody.insertBefore(swappedRow, movedRow);
    }

    flashUpdatedRow(movedRow);
}

async function handleRouteMoveClick(event) {
    const link = event.currentTarget;

    event.preventDefault();

    const row = link.closest("tr");

    if (row) {
        row.classList.add("route-moving");
    }

    try {
        const response = await fetch(link.href, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCsrfToken(),
            },
        });

        if (!response.ok) {
            window.location.href = link.href;
            return;
        }

        const data = await response.json();

        if (!data.moved) {
            return;
        }

        moveRowInDom(
            data.direction,
            data.moved_route_id,
            data.swapped_route_id
        );

        updateOrderCell(data.moved_route_id, data.moved_order);
        updateOrderCell(data.swapped_route_id, data.swapped_order);
    } catch (error) {
        window.location.href = link.href;
    } finally {
        if (row) {
            row.classList.remove("route-moving");
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const moveLinks = document.querySelectorAll("[data-route-move]");

    moveLinks.forEach((link) => {
        link.addEventListener("click", handleRouteMoveClick);
    });
});

async function handleZoneToggleSubmit(event) {
    const form = event.currentTarget;
    const button = form.querySelector("[data-zone-toggle-button]");

    event.preventDefault();

    if (button) {
        button.disabled = true;
    }

    try {
        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCsrfToken(),
            },
            body: new FormData(form),
        });

        if (!response.ok) {
            form.submit();
            return;
        }

        const data = await response.json();

        if (data.success && button) {
            button.textContent = data.label;
            button.classList.add("route-updated");

            setTimeout(() => {
                button.classList.remove("route-updated");
            }, 500);
        }
    } catch (error) {
        form.submit();
    } finally {
        if (button) {
            button.disabled = false;
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const zoneToggleForms = document.querySelectorAll("[data-zone-toggle-form]");

    zoneToggleForms.forEach((form) => {
        form.addEventListener("submit", handleZoneToggleSubmit);
    });
});

async function handleDeleteRouteSubmit(event) {
    const form = event.currentTarget;

    event.preventDefault();

    const confirmed = confirm("Supprimer ce bloc du topo ?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCsrfToken(),
            },
            body: new FormData(form),
        });

        if (!response.ok) {
            form.submit();
            return;
        }

        const data = await response.json();

        if (data.success) {
            const row = form.closest("tr");

            if (row) {
                row.style.transition = "opacity 0.2s ease";
                row.style.opacity = "0";

                setTimeout(() => {
                    row.remove();
                }, 200);
            }
        }
    } catch (error) {
        form.submit();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const deleteForms = document.querySelectorAll("[data-delete-route-form]");

    deleteForms.forEach((form) => {
        form.addEventListener("submit", handleDeleteRouteSubmit);
    });
});