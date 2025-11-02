let given_names = ["X", "Y", "Z", "x", "y", "z","p1", "p2", "p3"];
const forbidden_chars = ["{", "}", "[", "/", "%", "&", "|", " ", "  ", "^", "~", "<<", ">>", "==", "<=", ">=", "<", ">", "=", ",", ";", "."]

function checkForbiddenChars(name) {
    for (let i = 0; i < forbidden_chars.length; i++) {
        if (name.includes(forbidden_chars[i])) {
            return false;
        }
    }
    return true;
}

function addVariable() {
    let v_name = prompt("Name the variable");
    if (v_name.length <= 20 && checkForbiddenChars(v_name)) {
        if (is_name_valid(given_names, v_name)) {
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
                given_names.push(v_name);
                logMessage("Successfully created a variable", "info");
            } else {
                logMessage("failed to create a variable", "error");
            }
        } else {
            logMessage("failed to create a variable - name exists already", "error");
        }
    } else {
        logMessage("failed to create a variable - too long or not allowed chars (" + forbidden_chars + ")", "error");
    }
}

function removeVariable(id) {
    const el = document.getElementById(id);
    if (el) el.remove();

    const varName = id.replace("inline-container-", "");
    const baseId = "block-get-" + varName + "-pos";

    const matches = document.querySelectorAll("[id^='" + baseId + "']");
    for (let i = 0; i < matches.length; i++) {
        let m = matches[i];
        m.remove();
    }



    const index = given_names.indexOf(varName);
    if (index > -1) {
        given_names.splice(index, 1);
    }
}

// --------------------- POSITIONS ---------------------

function addPos() {
    let p_name = prompt("Name the position");
    if (p_name.length <= 20 && checkForbiddenChars(p_name)) {
        if (is_name_valid(given_names, p_name)) {
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
                given_names.push(p_name);
                logMessage("Successfully created a position", "info");
            } else {
                logMessage("failed to create a position", "error");
            }
        } else {
            logMessage("failed to create a position - name exists already", "error");
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
    for (let i = 0; i < matches.length; i++) {
        let m = matches[i];
        m.remove();
    }


    const index = given_names.indexOf(posName);
    if (index > -1) {
        given_names.splice(index, 1);
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