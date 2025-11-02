function setMoveButton(id, dir, axis) {
    document.getElementById(id).onclick = function () {
        send(dir, axis);
    };
}

setMoveButton("x-forward", 1, "x");
setMoveButton("x-backward", -1, "x");
setMoveButton("y-forward", 1, "y");
setMoveButton("y-backward", -1, "y");
setMoveButton("z-up", 1, "z");
setMoveButton("z-down", -1, "z");
setMoveButton("reset-manuel", 0, "r")

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

let saveButtons = document.querySelectorAll('.save-btn');
for (let i = 0; i < saveButtons.length; i++) {
    saveButtons[i].addEventListener('click', function () {
        let posNum = this.dataset.pos;
        console.log('Save current position to slot ' + posNum);
        // TODO: Implement logic to read and store current XYZ
    });
}

// Handle "Set" buttons for positions
let setButtons = document.querySelectorAll('.set-btn');
for (let j = 0; j < setButtons.length; j++) {
    setButtons[j].addEventListener('click', function () {
        let posNum = this.dataset.pos;
        console.log('Set current position to slot ' + posNum);
        // TODO: Implement logic to move to stored XYZ
    });
}

// Handle manual edit of position inputs
let positionInputs = document.querySelectorAll('.pos-input');
for (let k = 0; k < positionInputs.length; k++) {
    positionInputs[k].addEventListener('input', function () {
        let id = this.id;
        console.log('Edited ' + id + ': ' + this.value);
        // TODO: Implement logic to handle manual position edits
    });
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