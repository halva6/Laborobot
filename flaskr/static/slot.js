(function () {
    // Hilfsfunktionen zum Erzeugen/Zurückverwandeln
    function createInputFromSlot(slot) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'slot-input';
        input.value = slot.dataset.value || '';
        if (slot.dataset.accept) input.dataset.accept = slot.dataset.accept;
        input.setAttribute('draggable', 'false'); // nicht draggable
        return input;
    }

    function createSlotFromInput(input) {
        const slot = document.createElement('span'); // span für Inline-Kontext
        slot.className = 'slot';

        slot.innerHTML = `<span class="slot" data-accept="variable number">`;
        return slot;
    }

    // Delegierte Listener (funktioniert auch wenn Slots dynamisch erzeugt werden)
    document.addEventListener("dblclick", e => {
        const slot = e.target.closest(".slot");
        if (!slot) return;
        if (slot.querySelector(".slot-input")) return;
        const input = createInputFromSlot(slot);
        slot.replaceWith(input);
        input.focus();
        input.select();
    });

    document.addEventListener("contextmenu", e => {
        const input = e.target.closest(".slot-input");
        if (!input) return;
        e.preventDefault();
        const slot = createSlotFromInput(input);
        input.replaceWith(slot);
    });

    // Enter/Escape-Tasten: bestätigen oder abbrechen
    document.addEventListener('keydown', function (e) {
        if (!input) return;
        if (e.key === 'Enter') {
            // bestätigen
            const slot = createSlotFromInput(input);
            input.replaceWith(slot);
        } else if (e.key === 'Escape') {
            // abbrechen (hier behandeln wir gleich wie bestätigen, du kannst andere Logik einsetzen)
            const slot = createSlotFromInput(input);
            input.replaceWith(slot);
        }
    });

})();