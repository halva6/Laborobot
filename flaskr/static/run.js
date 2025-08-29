function getWorkspaceContents() {
    const workspace = document.getElementById("workspaceInner");

    // rekursiv einen Block auslesen
    function parseBlock(block) {
        // Variablen / Inline-Slots erfassen
        const variables = Array.from(block.querySelectorAll(".block-variable, .inline-slot > .block-variable"))
            .map(v => ({
                id: v.id || null,
                text: v.innerText.trim(),
                type: v.className
            }));

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

    fetch('/laborobot',
        {
            method: 'POST',
            headers:
            {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contents)
        });
}