const garbage = document.getElementById("garbage");
const clearBtn = document.getElementById("delete");
const droppable = document.getElementById("workspaceInner");

// dragstart: ID + info whether from pallet
document.addEventListener("dragstart", (e) => {
    if (e.target.matches(".block-move, .block-measure, .block-controll, .block-event, .block-variable, .block-pos, .block-calc, .block-time, .block-debug")) {
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

        // if this block can tolerate children --> install containers
        if (block.classList.contains("block-controll")) {
            const childContainer = document.createElement("div");
            childContainer.classList.add("children");
            block.appendChild(childContainer);
        }
    } else {
        block = element;
    }

    // --- check if drop in slot ---
    const targetSlot = e.target.closest(".slot");
    if (targetSlot) {
        const acceptedTypes = targetSlot.dataset.accept.split(" ");
        const blockType = [...block.classList].find(c => c.startsWith("block-"));

        if (acceptedTypes.includes(blockType.replace("block-", ""))) {
            // If there is already something in it --> take it out
            if (targetSlot.firstElementChild) {
                const oldBlock = targetSlot.firstElementChild;
                targetSlot.removeChild(oldBlock);
                oldBlock.dataset.palette = "false";
                oldBlock.setAttribute("draggable", "true");
                // back to the workspace (attach to the top or paste by mouse position)
                droppable.appendChild(oldBlock);
            }

            // append block
            targetSlot.appendChild(block);
            return;
        } else {
            logMessage("Block type not allowed for this slot", "warn");
            return;
        }
    }


    // --- check if we drop over a block with.children ---
    const targetBlock = e.target.closest(".block-controll"); // only control blocks are allowed to have children
    if (targetBlock && targetBlock.querySelector(".children")) {
        const childContainer = targetBlock.querySelector(".children");
        childContainer.appendChild(block);
    } else {
        // insert normally in the workspace (linear)
        const afterElement = getDragAfterElement(droppable, e.clientY);
        if (afterElement == null) {
            droppable.appendChild(block);
        } else {
            droppable.insertBefore(block, afterElement);
        }
    }
});

// sorting helper function
function getDragAfterElement(container, y) {
    const elements = [...container.querySelectorAll(".block-move, .block-measure, .block-controll, .block-event, .block-variable, .block-pos, .block-calc, .block-time, .block-debug:not([data-palette='true'])")];
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
    garbage.style.background = "#e660605e"; // visual effect
});
garbage.addEventListener("dragleave", () => {
    garbage.style.background = "transparent";
});
garbage.addEventListener("drop", (e) => {
    e.preventDefault();
    const id = e.dataTransfer.getData("text/plain");
    const fromPalette = e.dataTransfer.getData("from-palette") === "true";
    const element = document.getElementById(id);

    // delete workspace items only (no palette!)
    if (!fromPalette && element && droppable.contains(element)) {
        element.remove();
    }

    garbage.style.background = "transparent";

    logMessage("Deleted block", "info")
});

// workspace blank button
clearBtn.addEventListener("click", () => {
    const confirmDelete = confirm("Do you really want to delete everything?");
    if (confirmDelete) {
        droppable.innerHTML = "";
        logMessage("Everything cleared", "info");
    } else {
        logMessage("Deletion aborted", "warn");
    }
});

