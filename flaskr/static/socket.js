let socket = io();

socket.on("execution_error", (data) => {
    logMessage("Execution Error:", "error");
    logMessage("Message: " + data.error, "error");
    logMessage("Block ID: " + data.block_id, "error");
    logMessage("Error Code: " + data.error_code, "error");
});

// receives the sent data from the backend
socket.on('update', function (msg) {
    logMessage(msg.data, "debug")
});

socket.on('coords', function (msg) {
    let data = msg.data.split(",");

    let spanX = document.getElementById("x-axis-label");
    let spanY = document.getElementById("y-axis-label");
    let spanZ = document.getElementById("z-axis-label");

    spanX.innerHTML = data[0];
    spanY.innerHTML = data[1];
    spanZ.innerHTML = data[2];
});