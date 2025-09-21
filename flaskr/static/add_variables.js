var variable_names = ["X", "Y", "Z", "x", "y", "z"];
var pos_names = ["p1", "p2", "p3"];

function addVariable() {
    var v_name = prompt("Name the variable");
    if (v_name.length <= 20 && !v_name.includes(" ")) {
        if (is_name_valid(variable_names, v_name)) {
            if (!v_name == "") {
                const container = document.getElementById("variable-container");

                const inlineContainer = document.createElement("div");
                inlineContainer.className = "inline-container";
                inlineContainer.id = "inline-container-" + v_name;

                inlineContainer.innerHTML = `
        <div class="block-variable" id="block-get-${v_name}-pos" draggable="true" data-palette="true">
            <span class="label">${v_name}</span>
        </div>
        <p>=</p>
        <span class="param" contenteditable>0</span>
    `;

                // Remove-Button
                const btn = document.createElement("button");
                btn.className = "remove-variable";
                btn.innerText = "🗑";
                btn.onclick = function () {
                    removeVariable(inlineContainer.id);
                };

                inlineContainer.appendChild(btn);
                container.appendChild(inlineContainer);
                variable_names.push(v_name);
                logMessage("Successfully created a variable", "info");
            } else {
                logMessage("failed to create a variable", "error");
            }
        } else {
            logMessage("failed to create a variable - variable exists already", "error");
        }
    } else {
        logMessage("failed to create a variable - too long or not allowed chars", "error");
    }
}

function removeVariable(id) {
    const el = document.getElementById(id);
    if (el) el.remove();

    const varName = id.replace("inline-container-", "");
    const baseId = "block-get-" + varName + "-pos";

    const matches = document.querySelectorAll("[id^='" + baseId + "']");
    matches.forEach(m => m.remove());

    const index = variable_names.indexOf(varName);
    if (index > -1) {
        variable_names.splice(index, 1);
    }
}

// --------------------- POSITIONS ---------------------

function addPos() {
    var p_name = prompt("Name the position");
    if (p_name.length <= 20 && !p_name.includes(" ")) {
        if (is_name_valid(pos_names, p_name)) {
            if (p_name !== "") {
                const container = document.getElementById("position-container");

                const inlineContainer = document.createElement("div");
                inlineContainer.className = "inline-container";
                inlineContainer.id = "inline-container-" + p_name;

                inlineContainer.innerHTML = `
                    <div class="block-pos" id="block-get-${p_name}-pos" draggable="true" data-palette="true">
                        <span class="label">${p_name}: <br></span>
                        X: <span class="slot" data-accept="variable number"></span><br>
                        Y: <span class="slot" data-accept="variable number"></span><br>
                        Z: <span class="slot" data-accept="variable number"></span><br>
                    </div> </br>
                `;

                const btn = document.createElement("button");
                btn.className = "remove-pos";
                btn.innerText = "🗑";
                btn.onclick = function () {
                    removePos(inlineContainer.id);
                };

                inlineContainer.appendChild(btn);
                container.appendChild(inlineContainer);
                pos_names.push(p_name);
                logMessage("Successfully created a position", "info");
            } else {
                logMessage("failed to create a position", "error");
            }
        } else {
            logMessage("failed to create a position - position exists already", "error");
        }
    } else {
        logMessage("failed to create a position - too long or not allowed chars", "error");
    }
}

function removePos(id) {
    const el = document.getElementById(id);
    if (el) el.remove();

    const posName = id.replace("inline-container-", "");
    const baseId = "block-get-" + posName + "-pos";

    const matches = document.querySelectorAll("[id^='" + baseId + "']");
    matches.forEach(m => m.remove());

    const index = pos_names.indexOf(posName);
    if (index > -1) {
        pos_names.splice(index, 1);
    }
}

// ---------------------

function is_name_valid(list, name) {
    for (const item of list) {
        if (item === name) {
            return false;
        }
    }
    return true;
}