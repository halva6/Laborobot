var socket = io();

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