var socket = io();

// receives the sent data from the backend
socket.on('update', function (msg) {
    if (msg.error_code == 0) {
        logMessage(msg.data, "info")
    } else if (msg.error_code == 1) {
        logMessage(msg.data, "error")
    } else {
        logMessage(msg.data, "warn")
    }
});