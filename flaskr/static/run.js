function getWorkspaceContents() {
    const workspaceBlocks = document.querySelectorAll("#workspaceInner > div");
    const contents = Array.from(workspaceBlocks).map(block => {
        return {
            id: block.id,
            type: block.className,
            text: block.innerText.trim()
        };
    });

    return contents;
}


function run() {
    console.log(getWorkspaceContents());
}