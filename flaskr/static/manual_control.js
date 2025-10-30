document.getElementById("x-forward").onclick = () => send(1, "x");
document.getElementById("x-backward").onclick = () => send(-1, "x");
document.getElementById("y-forward").onclick = () => send(1, "y");
document.getElementById("y-backward").onclick = () => send(-1, "y");
document.getElementById("z-up").onclick = () => send(1, "z");
document.getElementById("z-down").onclick = () => send(-1, "z");

document.getElementById("reset-manuel").onclick = () => send(0, "r");


function moveJSON(value, axis) {
    if (axis == "x" || axis == "y" || axis == "z") {
        return [
            {
                "id": "block-steps-" + axis + "-1761750547079",
                "type": "block-move",
                "text": "Go  steps on the " + axis.toUpperCase() + " axis",
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


function send(value, axis) {
    const contents = moveJSON(value, axis);

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