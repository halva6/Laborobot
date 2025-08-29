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

  let block;

  if (fromPalette) {
    // Neue Kopie aus der Palette
    block = element.cloneNode(true);
    block.id = id + "-" + Date.now(); // eindeutige ID
    block.dataset.palette = "false"; // nicht mehr Palette
    block.setAttribute("draggable", "true");
  } else {
    // Bestehendes Block im Workspace → verschieben
    block = element;
  }

  // An Drop-Position einfügen
  const afterElement = getDragAfterElement(droppable, e.clientY);
  if (afterElement == null) {
    droppable.appendChild(block);
  } else {
    droppable.insertBefore(block, afterElement);
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
  if (!fromPalette && element && element.parentNode === droppable) {
    element.remove();
  }

  garbage.style.background = "transparent";

  logMessage("Deleted block", "warn")
});

// Workspace leeren Button
clearBtn.addEventListener("click", () => {
  droppable.innerHTML = "";
  logMessage("Everything cleared", "warn");
});

