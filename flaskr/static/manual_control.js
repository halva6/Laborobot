function setupButton(id, axis, direction) {
    let holdInterval;
    let holdTimeout;
    const button = document.getElementById(id);

    function startHold() {
        // Press and hold after 500 ms → start the retry
        holdTimeout = setTimeout(() => {
            holdInterval = setInterval(() => {
                send(direction * 5, axis);
            }, 500);
        }, 500);
    }

    function endHold(isTouch = false) {
        if (holdTimeout) {
            clearTimeout(holdTimeout);
            send(direction, axis);
        }

        if (holdInterval) {
            clearInterval(holdInterval);
            holdInterval = null;
        }

        if (isTouch) button.blur();
    }

    // Mouse control
    button.addEventListener("mousedown", startHold);
    button.addEventListener("mouseup", () => endHold());
    button.addEventListener("mouseleave", () => endHold());

    // Touch control (for mobile phone/tablet)
    button.addEventListener("touchstart", (e) => {
        e.preventDefault();
        startHold();
    });
    button.addEventListener("touchend", (e) => {
        e.preventDefault();
        endHold(true);
    });
}

setupButton("x-forward", "x", 1);
setupButton("x-backward", "x", -1);
setupButton("y-forward", "y", 1);
setupButton("y-backward", "y", -1);
setupButton("z-up", "z", 1);
setupButton("z-down", "z", -1);

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