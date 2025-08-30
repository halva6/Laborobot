window.addEventListener('beforeunload', function (event) {
  // The following line is necessary to display the confirmation message
  event.preventDefault();
  // The default message is no longer displayed in modern browsers
  event.returnValue = 'Do you really want to leave the page?';
});

function getWorkspaceContents() {
  const workspace = document.getElementById("workspaceInner");

  // 1) Variable-Map aus der Palette
  const variableMap = {};
  document.querySelectorAll("#variable-container .inline-container").forEach(container => {
    const varBlock = container.querySelector(".block-variable");
    const label = varBlock.querySelector(".label")?.innerText.trim() || "";
    const value = container.querySelector(".param")?.innerText.trim() || null;

    variableMap[label] = {
      id: varBlock.id,
      type: varBlock.className,
      value: value
    };
  });

  // 2) Rekursiv einen Block lesen
  function parseBlock(block) {
    // eigener children-Container (direktes Kind)
    const childrenContainer = block.querySelector(":scope > .children");

    // --- Variablen dieses Blocks (ohne eigene Children) ---
    const variables = Array.from(block.querySelectorAll(".block-variable"))
      // nur die Variablen behalten, die NICHT im *eigenen* children-Container liegen
      .filter(v => !(childrenContainer && childrenContainer.contains(v)))
      .map(v => {
        const label = v.querySelector(".label")
          ? v.querySelector(".label").innerText.trim()
          : v.innerText.trim();

        const varData = variableMap[label] || {};
        return {
          id: v.id || varData.id || null,
          text: label,
          type: v.className,
          value: varData.value ?? null
        };
      });

    // --- Block-Text (Label), ebenfalls ohne Inhalte aus dem eigenen children-Container ---
    const labelEl = Array.from(block.querySelectorAll(".label"))
      .find(el => !(childrenContainer && childrenContainer.contains(el)));
    const text = labelEl ? labelEl.innerText.trim() : "";

    // --- Kinder parsen ---
    const children = childrenContainer
      ? Array.from(childrenContainer.children).map(parseBlock)
      : [];

    return {
      id: block.id,
      type: block.className,
      text,
      variables,
      children
    };
  }

  // 3) Top-Level Blöcke einsammeln
  const topLevelBlocks = Array.from(workspace.children)
    .filter(block =>
      block.classList.contains("block-move") ||
      block.classList.contains("block-controll") ||
      block.classList.contains("block-event") ||
      block.classList.contains("block-variable") ||
      block.classList.contains("block-debug")
    )
    .map(parseBlock);

  return topLevelBlocks;
}

//send it to the server
function run() {
  const contents = getWorkspaceContents();
  console.log(JSON.stringify(contents, null, 2));

  fetch('/',
    {
      method: 'POST',
      headers:
      {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contents)
    });
}