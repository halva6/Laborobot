const consoleBox = document.getElementById("console");
const clearConsoleButton = document.getElementById("clear-console");

logMessage("Debug console startet");

function logMessage(text, type = "info") {
    const line = document.createElement("div");
    line.classList.add("console-line", type);
    line.textContent = text;
    consoleBox.insertBefore(line, clearConsoleButton);
    consoleBox.scrollTop = consoleBox.scrollHeight; // auto-scroll
}

clearConsoleButton.addEventListener("click", () => {
    document.querySelectorAll(".console-line").forEach(line => line.remove());
    logMessage("Console cleaned", "debug");
});

