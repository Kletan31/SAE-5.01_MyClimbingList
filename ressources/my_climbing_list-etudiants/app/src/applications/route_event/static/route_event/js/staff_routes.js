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