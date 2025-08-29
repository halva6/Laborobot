var variable_names = ["X", "Y", "Z", "x", "y", "z"]

function addVariable() {
    var v_name = prompt("Name the variable");
    if (v_name.length <= 20) {
        if (is_name_valid(variable_names, v_name)) {
            if (!v_name == "") {
                document.getElementById("variable-container").innerHTML += '<div class="inline-container"><div class="block-variable" id="block-get-' + v_name + '-pos" draggable="true" data-palette="true"><span class="label">' + v_name + '</span></div><p>=</p><span class="param"contenteditable>0</span></div> </br>';
                variable_names.push(v_name)
                logMessage("Successfully created a variable", "info");
            } else {
                logMessage("failed to created a variable", "error");
            }
        } else {
            logMessage("failed to created a variable - variable exists already", "error");
        }
    } else {
        logMessage("failed to created a variable - variable name is to long max 20 chars", "error");
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