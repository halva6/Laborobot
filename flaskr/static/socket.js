var socket = io();

socket.on('update', function (msg) {
    logMessage(msg.data, "info")
});