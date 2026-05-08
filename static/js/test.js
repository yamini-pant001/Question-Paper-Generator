// Test page JavaScript: timer, answered progress, empty-check, and confirmation.
const testForm = document.querySelector("[data-test-form]");
const timerElement = document.querySelector("#timer");
const progressBar = document.querySelector("#progress-bar");
const answeredCount = document.querySelector("#answered-count");
const submitButton = document.querySelector("[data-submit-button]");

function updateProgress() {
    // Count unique answered question names because each MCQ has four radio inputs.
    const total = Number(testForm.dataset.total);
    const checkedInputs = testForm.querySelectorAll("input[type='radio']:checked");
    const answered = new Set(Array.from(checkedInputs).map((input) => input.name)).size;
    const percentage = total ? (answered / total) * 100 : 0;

    answeredCount.textContent = answered;
    progressBar.style.width = `${percentage}%`;
}

function startTimer() {
    // The timer is intentionally client-side only, so the backend remains easy to explain.
    let remainingSeconds = Number(timerElement.dataset.minutes) * 60;

    const intervalId = setInterval(() => {
        const minutes = Math.floor(remainingSeconds / 60);
        const seconds = remainingSeconds % 60;
        timerElement.textContent = `${minutes}:${String(seconds).padStart(2, "0")}`;

        if (remainingSeconds <= 0) {
            clearInterval(intervalId);
            testForm.requestSubmit();
        }
        remainingSeconds -= 1;
    }, 1000);
}

if (testForm) {
    testForm.addEventListener("change", updateProgress);
    testForm.addEventListener("submit", (event) => {
        updateProgress();
        const total = Number(testForm.dataset.total);
        const answered = Number(answeredCount.textContent);

        if (answered < total) {
            event.preventDefault();
            alert("Please answer every question before submitting.");
            return;
        }

        const confirmed = confirm("Submit your test now?");
        if (!confirmed) {
            event.preventDefault();
            return;
        }

        submitButton.textContent = "Checking answers...";
        submitButton.disabled = true;
    });

    updateProgress();
    startTimer();
}
