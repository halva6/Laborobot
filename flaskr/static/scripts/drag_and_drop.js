const garbage = document.getElementById("garbage");
const clearBtn = document.getElementById("delete");
const droppable = document.getElementById("workspaceInner");

let dropIndicator = document.createElement("div");
dropIndicator.classList.add("drop-indicator");
document.body.appendChild(dropIndicator);

// dragstart: ID + info whether from pallet
document.addEventListener("dragstart", (e) => {
    if (e.target.matches(".block-move, .block-measure, .block-control, .block-event, .block-variable, .block-pos, .block-calc, .block-time, .block-debug")) {
        e.dataTransfer.setData("text/plain", e.target.id);
        e.dataTransfer.setData("from-palette", e.target.dataset.palette === "true");
    }
});

droppable.addEventListener("dragover", (e) => {
    e.preventDefault();

    // --- Check if we're dragging over a children container ---
    const targetChildren = e.target.closest(".children");
    const targetBlock = e.target.closest(".block-control");
    let container = droppable; // default workspace container

    // If we're hovering over a block that can have children
    if (targetChildren) {
        container = targetChildren;
    } else if (targetBlock && targetBlock.querySelector(".children")) {
        // if we're over a control block but not directly inside its .children,
        // show indicator at the top of its children area
        container = targetBlock.querySelector(".children");
    }

    // Get all valid blocks inside this container
    const afterElement = getDragAfterElement(container, e.clientY);
    const rect = container.getBoundingClientRect();

    // --- Determine proper indentation (for nested children) ---
    const isNested = container.classList.contains("children");
    const indent = isNested ? 20 : 0;

    // --- Compute indicator position ---
    if (afterElement) {
        const box = afterElement.getBoundingClientRect();
        dropIndicator.style.display = "block";
        dropIndicator.style.top = box.top + window.scrollY + "px";
        dropIndicator.style.left = box.left + indent + "px";
        dropIndicator.style.width = (box.width - indent * 2) + "px";
    } else {
        // Case: empty children container or dropping at end
        dropIndicator.style.display = "block";
        dropIndicator.style.top = rect.bottom + window.scrollY - 2 + "px";
        dropIndicator.style.left = rect.left + indent + "px";
        dropIndicator.style.width = (rect.width - indent * 2) + "px";
    }
});

function getDragAfterElement(container, y) {
    const elements = [...container.querySelectorAll(
        ":scope > .block-move, :scope > .block-measure, :scope > .block-control, :scope > .block-event, :scope > .block-variable, :scope > .block-pos, :scope > .block-calc, :scope > .block-time, :scope > .block-debug"
    )];

    return elements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}



droppable.addEventListener("dragleave", () => {
    // hide indicators when leaving
    dropIndicator.style.display = "none";
});

droppable.addEventListener("drop", (e) => {
    e.preventDefault();
    dropIndicator.style.display = "none";

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
        if (block.classList.contains("block-control")) {
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
            if (targetSlot.firstElementChild) {
                const oldBlock = targetSlot.firstElementChild;
                targetSlot.removeChild(oldBlock);
                oldBlock.dataset.palette = "false";
                oldBlock.setAttribute("draggable", "true");
                droppable.appendChild(oldBlock);
            }
            targetSlot.appendChild(block);
            return;
        } else {
            logMessage("Block type not allowed for this slot", "warn");
            return;
        }
    }

    // --- check if we drop over a block with.children ---
    const targetBlock = e.target.closest(".block-control");
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
    const elements = [...container.querySelectorAll(".block-move, .block-measure, .block-control, .block-event, .block-variable, .block-pos, .block-calc, .block-time, .block-debug:not([data-palette='true'])")];
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
