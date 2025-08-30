var variable_names = ["X", "Y", "Z", "x", "y", "z"]

function addVariable() {
    var v_name = prompt("Name the variable");
    if (v_name.length <= 20 && !v_name.includes(" ")) {
        if (is_name_valid(variable_names, v_name)) {
            if (!v_name == "") {
                const container = document.getElementById("variable-container");

                // create inline-Container
                const inlineContainer = document.createElement("div");
                inlineContainer.className = "inline-container";
                inlineContainer.id = "inline-container-" + v_name;

                // Variable Block
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
                variable_names.push(v_name)
                logMessage("Successfully created a variable", "info");
            } else {
                logMessage("failed to created a variable", "error");
            }
        } else {
            logMessage("failed to created a variable - variable exists already", "error");
        }
    } else {
        logMessage("failed to created a variable - to long or not allowd chars", "error");
    }
}

function removeVariable(id) {
   const el = document.getElementById(id);
    if (el) el.remove();

    // determine the base ID --> e.g. from "inline-container-asd"
    const varName = id.replace("inline-container-", ""); 
    const baseId = "block-get-" + varName + "-pos";

    // find all elements whose id starts with baseId
    const matches = document.querySelectorAll("[id^='" + baseId + "']");
    matches.forEach(m => m.remove());

    // removes name from the list
    const id_slice = id.slice(17, id.length)
    const index = variable_names.indexOf(id_slice);
    console.log(id_slice)
    if (index > -1) { // only splice array when item is found
        variable_names.splice(index, 1); // 2nd parameter means remove one item only
    }
}

function is_name_valid(variable_names, name) {
    for (const variable_name of variable_names) {
        if (variable_name == name) {
            return false;
        }
    }
    return true;
}