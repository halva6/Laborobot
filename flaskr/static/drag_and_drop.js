const garbage = document.getElementById("garbage");
const clearBtn = document.getElementById("delete");
const droppable = document.getElementById("workspaceInner");

// Dragstart: ID + Info ob aus Palette
document.addEventListener("dragstart", (e) => {
    if (e.target.matches(".block-move, .block-controll, .block-event, .block-variable, .block-debug")) {
        e.dataTransfer.setData("text/plain", e.target.id);
        e.dataTransfer.setData("from-palette", e.target.dataset.palette === "true");
    }
});

droppable.addEventListener("dragover", (e) => {
    e.preventDefault();
});

droppable.addEventListener("drop", (e) => {
    e.preventDefault();

    const id = e.dataTransfer.getData("text/plain");
    const fromPalette = e.dataTransfer.getData("from-palette") === "true";
    const element = document.getElementById(id);
    if (!element) return;

    let block;
    if (fromPalette) {
        block = element.cloneNode(true);
        block.id = id + "-" + Date.now();
        block.dataset.palette = "false";
        block.setAttribute("draggable", "true");

        // falls dieser Block Kinder verträgt → Container einbauen
        if (block.classList.contains("block-controll")) {
            const childContainer = document.createElement("div");
            childContainer.classList.add("children");
            block.appendChild(childContainer);
        }
    } else {
        block = element;
    }

    // --- NEU: prüfen ob Drop in Slot ---
    const targetSlot = e.target.closest(".slot");
    if (targetSlot) {
        const acceptedTypes = targetSlot.dataset.accept.split(" ");
        const blockType = [...block.classList].find(c => c.startsWith("block-"));

        if (acceptedTypes.includes(blockType.replace("block-", ""))) {
            // Falls schon was drinliegt → rausnehmen
            if (targetSlot.firstElementChild) {
                const oldBlock = targetSlot.firstElementChild;
                targetSlot.removeChild(oldBlock);
                oldBlock.dataset.palette = "false";
                oldBlock.setAttribute("draggable", "true");
                // zurück ins Workspace (oben anhängen oder nach Mausposition einfügen)
                droppable.appendChild(oldBlock);
            }

            // Neues einsetzen
            targetSlot.appendChild(block);
            return;
        } else {
            logMessage("Block type not allowed for this slot", "warn");
            return;
        }
    }


    // --- prüfen, ob wir über einem Block mit .children droppen ---
    const targetBlock = e.target.closest(".block-controll"); // nur Control-Blöcke dürfen Kinder haben
    if (targetBlock && targetBlock.querySelector(".children")) {
        const childContainer = targetBlock.querySelector(".children");
        childContainer.appendChild(block);
    } else {
        // normal im Workspace einfügen (linear)
        const afterElement = getDragAfterElement(droppable, e.clientY);
        if (afterElement == null) {
            droppable.appendChild(block);
        } else {
            droppable.insertBefore(block, afterElement);
        }
    }
});

// Hilfsfunktion für Sortierung
function getDragAfterElement(container, y) {
    const elements = [...container.querySelectorAll(".block-move, .block-controll, .block-event, .block-variable, .block-debug:not([data-palette='true'])")];
    return elements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

//trash
garbage.addEventListener("dragover", (e) => {
    e.preventDefault();
    garbage.style.background = "#ffcccc"; // visueller Effekt
});
garbage.addEventListener("dragleave", () => {
    garbage.style.background = "transparent";
});
garbage.addEventListener("drop", (e) => {
    e.preventDefault();
    const id = e.dataTransfer.getData("text/plain");
    const fromPalette = e.dataTransfer.getData("from-palette") === "true";
    const element = document.getElementById(id);

    // Nur Workspace-Elemente löschen (keine Palette!)
    if (!fromPalette && element && droppable.contains(element)) {
        element.remove();
    }

    garbage.style.background = "transparent";

    logMessage("Deleted block", "info")
});

// Workspace leeren Button
clearBtn.addEventListener("click", () => {
    droppable.innerHTML = "";
    logMessage("Everything cleared", "info");
});

