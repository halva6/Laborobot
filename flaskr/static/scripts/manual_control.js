function setMoveButton(id, dir, axis) {
    document.getElementById(id).onclick = function () {
        send(() => moveJSON(dir, axis));
    };
}

setMoveButton("x-up", 1, "x");
setMoveButton("x-down", -1, "x");
setMoveButton("y-up", 1, "y");
setMoveButton("y-down", -1, "y");
setMoveButton("z-up", 1, "z");
setMoveButton("z-down", -1, "z");
setMoveButton("reset-manuel", 0, "r")

function moveJSON(value, axis) {
    if (axis == "x" || axis == "y" || axis == "z") {
        return [
            {
                "id": "block-steps-" + axis + "-1761750547079",
                "type": "block-move",
                "text": "Go  steps on the  axis " + axis,
                "variables": [
                    {
                        "id": "block-get-var01-pos-01",
                        "text": "var1761750550405",
                        "type": "block-variable",
                        "value": value.toString(),
                    }
                ],
                "children": []
            }
        ];
    } else {
        return [{ "id": "block-reset-pos-01", "type": "block-move", "text": "Reset position", "variables": [], "children": [] }]
    }
}

function send(getJSON) {
    const contents = getJSON();
    console.log(contents);

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