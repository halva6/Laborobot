window.addEventListener('beforeunload', function (event) {
  // The following line is necessary to display the confirmation message
  event.preventDefault();
  // The default message is no longer displayed in modern browsers
  event.returnValue = 'Do you really want to leave the page?';
});

function getWorkspaceContents() {
  const workspace = document.getElementById("workspaceInner");

  // Variable map from the palette
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

  const variable_names = [];

  // Helper: generate a new unique variable name
  function getNewVariableName() {
    let variable_name = "var" + Date.now();
    while (variable_names.includes(variable_name)) {
      variable_name = "var" + Date.now() + Math.floor(Math.random() * Date.now());
    }
    variable_names.push(variable_name);
    return variable_name;
  }

  // Recursive parser for a block
  function parseBlock(block) {
    const childrenContainer = block.querySelector(":scope > .children");

    // Special case: position block (.block-pos)
    if (block.classList.contains("block-pos")) {
      const label = block.querySelector(".label")?.innerText.trim() || "";

      const inputs = Array.from(block.querySelectorAll("input")).map(input => {
        const name = input.previousSibling?.textContent?.replace(":", "").trim() || "";
        const newName = getNewVariableName();
        return {
          id: "block-get-" + newName + "-pos-" + Date.now(),
          axis: name, // X, Y, Z
          text: newName,
          type: "block-variable",
          value: input.value || ""
        };
      });

      return {
        id: block.id,
        type: block.className,
        text: label,
        variables: inputs,
        children: []
      };
    }

    // Collect variables inside the block (excluding its own children)
    const variables = Array.from(block.querySelectorAll(".block-variable, input"))
      .filter(v => !(childrenContainer && childrenContainer.contains(v)))
      .map(v => {
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

    // Block text (excluding children content)
    const labelElements = Array.from(block.querySelectorAll(".label"));

    var labelEls = Array.from(block.querySelectorAll(".label"));
    var labelEl = undefined;

    for (var i = 0; i < labelEls.length; i++) {
      if (!childrenContainer || !childrenContainer.contains(labelEls[i])) {
        labelEl = labelEls[i];
        break;
      }
    }

    var text = "";
    if (labelEl) {
      text = labelEl.innerText.trim();

      var specialChild = labelEl.querySelector(".operation-selection");
      if (specialChild) {
        text += " " + specialChild.innerText.trim();
      }
    }
    //const text = labelEl ? labelEl.innerText.trim() : "";

    // Parse children inside a .children container
    let children = childrenContainer
      ? Array.from(childrenContainer.children).map(parseBlock)
      : [];

    // Special case: slot with a position block inside
    const posSlot = block.querySelector(":scope .slot[data-accept='pos']");
    if (posSlot) {
      const posBlock = posSlot.querySelector(".block-pos");
      if (posBlock) {
        children.push(parseBlock(posBlock));
      }
    }

    return {
      id: block.id,
      type: block.className,
      text,
      variables,
      children
    };
  }

  // Collect top-level blocks, including .block-pos
  const topLevelBlocks = Array.from(workspace.children)
    .filter(block =>
      block.classList.contains("block-move") ||
      block.classList.contains("block-controll") ||
      block.classList.contains("block-event") ||
      block.classList.contains("block-variable") ||
      block.classList.contains("block-calc") ||
      block.classList.contains("block-time") ||
      block.classList.contains("block-debug") ||
      block.classList.contains("block-pos")
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