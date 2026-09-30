document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener("click", (event) => {

        const button = event.target.closest(".hold-button");

        if (!button) {
            return;
        }

        const container = button.closest(".hold-counter");

        const input = container.querySelector(
            ".participant-score-input"
        );

        let value = parseInt(input.value || 0, 10);

        if (button.dataset.action === "increase") {
            value += 1;
        }

        if (button.dataset.action === "decrease") {
            value = Math.max(0, value - 1);
        }

        input.value = value;
    });
});