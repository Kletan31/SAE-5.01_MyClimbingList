function showTemporaryMessage(row, message) {
    let messageElement = row.querySelector(".row-action-message");

    if (!messageElement) {
        messageElement = document.createElement("span");
        messageElement.className = "row-action-message";
        row.querySelector(".actions").appendChild(messageElement);
    }

    messageElement.textContent = message;

    setTimeout(() => {
        messageElement.textContent = "";
    }, 2500);
}

function updatePaymentState(form, row, data) {
    const paymentCell = row.querySelector("[data-payment-cell]");
    const button = form.querySelector("button");

    paymentCell.innerHTML = "";

    const status = document.createElement("span");
    status.textContent = data.payment_label;
    status.className = data.is_payment_validated
        ? "payment-valid"
        : "payment-pending";

    paymentCell.appendChild(status);

    form.action = data.next_action_url;
    button.textContent = data.next_action_label;
}

function initializeStaffRowActionForms() {
    const forms = document.querySelectorAll(".staff-row-action-form");

    forms.forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const row = form.closest("[data-team-row]");
            const button = form.querySelector("button");
            const formData = new FormData(form);

            button.disabled = true;

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                if (!response.ok) {
                    form.submit();
                    return;
                }

                const data = await response.json();

                if (data.action === "payment_toggle") {
                    updatePaymentState(form, row, data);
                }

                if (data.action === "delete") {
                    row.remove();
                }

                if (data.action === "resend_link") {
                    showTemporaryMessage(row, data.message);
                }
            } catch (error) {
                form.submit();
            } finally {
                button.disabled = false;
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", initializeStaffRowActionForms);