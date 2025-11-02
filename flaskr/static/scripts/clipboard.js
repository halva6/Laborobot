let copyButtons = document.querySelectorAll('.copy-btn');
copyButtons.forEach(function (c) {
    c.addEventListener("click", function (e) {
        let dataPos = c.getAttribute("data-pos");
        copyButton(dataPos);
    });
});

function extractInteger(str) {
    const match = str.match(/-?\d+/);
    return match ? parseInt(match[0], 10) : null;
}

function copyButton(position) {
    let X = document.getElementById("x-axis-label").innerHTML;
    let Y = document.getElementById("y-axis-label").innerHTML;
    let Z = document.getElementById("z-axis-label").innerHTML;

    document.getElementById("pos" + position + "-x").value = extractInteger(X);
    document.getElementById("pos" + position + "-y").value = extractInteger(Y);
    document.getElementById("pos" + position + "-z").value = extractInteger(Z);

    localStorage.setItem("pos" + position + "-x", extractInteger(X));
    localStorage.setItem("pos" + position + "-y", extractInteger(Y));
    localStorage.setItem("pos" + position + "-z", extractInteger(Z));
}


let setButtons = document.querySelectorAll('.set-btn');
setButtons.forEach(function (c) {
    c.addEventListener("click", function (e) {
        let dataPos = c.getAttribute("data-pos");
        setButton(dataPos);
    });
});

function setButton(position) {
    let valueX = localStorage.getItem("pos" + position + "-x");
    let valueY = localStorage.getItem("pos" + position + "-y");
    let valueZ = localStorage.getItem("pos" + position + "-z");

    send(() => setJSON(valueX, valueY, valueZ));
}

function setJSON(x, y, z) {
    return [
        {
            "id": "block-go-to-pos-1762097099398",
            "type": "block-move",
            "text": "Goto position:",
            "variables": [
                {
                    "id": "block-get-var01-pos-x",
                    "text": "var1761750550401",
                    "type": "block-variable",
                    "value": x.toString(),
                },
                {
                    "id": "block-get-var01-pos-y",
                    "text": "var1761750550402",
                    "type": "block-variable",
                    "value": y.toString(),
                },
                {
                    "id": "block-get-var01-pos-z",
                    "text": "var1761750550403",
                    "type": "block-variable",
                    "value": z.toString(),
                }
            ],
            "children": []
        }
    ];
}