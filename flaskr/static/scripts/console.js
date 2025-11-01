const consoleBox = document.getElementById("console");
const input = document.getElementById("consoleInput");

logMessage("Debug console startet");

function logMessage(text, type = "info") {
    const line = document.createElement("div");
    line.classList.add("console-line", type);
    line.textContent = text;
    consoleBox.appendChild(line);
    consoleBox.scrollTop = consoleBox.scrollHeight; // auto-scroll
}
