window.addEventListener('beforeunload', function (event) {
  // The following line is necessary to display the confirmation message
  event.preventDefault();
  // The default message is no longer displayed in modern browsers
  event.returnValue = 'Do you really want to leave the page?';
});

function getWorkspaceContents() {
  const workspace = document.getElementById("workspaceInner");

  // variable map from the palette
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

  // Hilfsfunktion: neuen Variablennamen finden
  function getNewVariableName() {
    var variable_name = "var" + Date.now();
    while (!is_name_valid(variable_names, variable_name)) {
      variable_name = "var" + Date.now() + Math.floor(Math.random()*Date.now());
    }

    variable_names.push(variable_name)
    return variable_name; // fallback falls alle Namen belegt
  }

  // recursively read a block
  function parseBlock(block) {
    // own children container (direct child)
    const childrenContainer = block.querySelector(":scope > .children");

    // Variablen in diesem Block (ohne die eigenen Children)
    const variables = Array.from(block.querySelectorAll(".block-variable, input"))
      // keep only those that are NOT in the own children container
      .filter(v => !(childrenContainer && childrenContainer.contains(v)))
      .map(v => {
        // Fall 1: normale Variable (wie bisher)
        if (v.classList.contains("block-variable")) {
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
        }

        // Fall 2: Input-Feld -> neue Variable anlegen
        if (v.tagName.toLowerCase() === "input") {
          const newName = getNewVariableName();
          return {
            id: "block-get-" + newName + "-pos-" + Date.now(),
            text: newName,
            type: "block-variable",
            value: v.value || null
          };
        }
      });

    // Block text (label), auch ohne eigenen Children-Inhalt
    const labelEl = Array.from(block.querySelectorAll(".label"))
      .find(el => !(childrenContainer && childrenContainer.contains(el)));
    const text = labelEl ? labelEl.innerText.trim() : "";

    // parse children
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

  // top-Level Blöcke einsammeln
  const topLevelBlocks = Array.from(workspace.children)
    .filter(block =>
      block.classList.contains("block-move") ||
      block.classList.contains("block-controll") ||
      block.classList.contains("block-event") ||
      block.classList.contains("block-variable") ||
      block.classList.contains("block-time") ||
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