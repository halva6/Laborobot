function getWorkspaceContents() {
    const workspace = document.getElementById("workspaceInner");

    // build a variable map from the palette
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

    // recursively read a block
    function parseBlock(block) {
        // variables + values from the map if applicable
        const variables = Array.from(block.querySelectorAll(".block-variable, .inline-slot > .block-variable"))
            .map(v => {
                const label = v.querySelector(".label") ? v.querySelector(".label").innerText.trim() : v.innerText.trim();
                const varData = variableMap[label] || {}; // values from the palette map
                return {
                    id: v.id || varData.id || null,
                    text: label,
                    type: v.className,
                    value: varData.value || null
                };
            });

        // children from the.children container
        const childrenContainer = block.querySelector(".children");
        const children = childrenContainer
            ? Array.from(childrenContainer.children).map(parseBlock)
            : [];

        return {
            id: block.id,
            type: block.className,
            text: block.querySelector(".label") ? block.querySelector(".label").innerText.trim() : "",
            variables: variables,
            children: children
        };
    }

    // collect all top-level blocks in the workspace
    const topLevelBlocks = Array.from(workspace.children)
        .filter(block => block.classList.contains("block-move") ||
            block.classList.contains("block-controll") ||
            block.classList.contains("block-event") ||
            block.classList.contains("block-variable") ||
            block.classList.contains("block-debug"))
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