// Helper function: create an input element from a slot
function createInputFromSlot(slot) {
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'slot-input';
    input.value = slot.dataset.value || '';

    // Copy data-accept attribute if present
    if (slot.dataset.accept) {
        input.dataset.accept = slot.dataset.accept;
    }

    // Prevent dragging
    input.setAttribute('draggable', 'false');

    return input;
}

// Helper function: create a slot element from an input
function createSlotFromInput(input) {
    const slot = document.createElement('span'); // use span for inline context
    slot.className = 'slot';

    // Keep same data-accept attribute if present
    if (input.dataset.accept) {
        slot.dataset.accept = input.dataset.accept;
    }

    // Also store the input value as data-value and visible text
    slot.dataset.value = input.value;
    slot.textContent = input.value || ''; // display the input text

    return slot;
}

// Handle double-click: convert slot to input
document.addEventListener("dblclick", function (e) {
    const slot = e.target.closest(".slot");
    if (!slot) {
        return;
    }

    // Prevent converting already active input slots
    const slotString = slot.outerHTML;
    if (slot.querySelector(".slot-input") || !slotString.includes("number")) {
        return;
    }

    const input = createInputFromSlot(slot);
    slot.replaceWith(input);
    input.focus();
    input.select();
});

// Handle right-click: convert input back to slot
document.addEventListener("contextmenu", function (e) {
    const input = e.target.closest(".slot-input");
    if (!input) {
        return;
    }
    input.value = null;
    e.preventDefault();

    const slot = createSlotFromInput(input);
    input.replaceWith(slot);
});

// Handle Enter/Escape keys: confirm or cancel input
document.addEventListener("keydown", function (e) {
    const input = e.target.closest(".slot-input");
    if (!input) {
        return;
    }

    if (e.key === "Escape") {
        // On both Enter and Escape, revert input to slot
        input.value = null;
        const slot = createSlotFromInput(input);
        input.replaceWith(slot);
    }
});
