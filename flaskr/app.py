from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from robot_movement.test_robot import TestRobot
from compiler.loader import Loader
from compiler.context import Context
from compiler.blocks.block import *
from server_error import *

# Try to import real Robot (works only on Raspberry Pi with GPIO)
try:
    import RPi.GPIO as GPIO
    from robot_movement.robot import Robot

    gpio_available: bool = True
except Exception:
    gpio_available: bool = False

import json

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "sec,msdfgnß04835,mnvkmliouzh32409ß854309##.ret!"
socket_io: SocketIO = SocketIO(app)

ErrorManager.init(socket_io)

# Create the Robot/TestRobot only once
if gpio_available:
    robot: Robot = Robot(gpio_available, socket_io)
else:
    robot: TestRobot = TestRobot(gpio_available, socket_io)


@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        command = request.get_json()

        with open("flaskr/compiler/from_server.json", "w") as file:
            file.write(json.dumps(command))

        try:
            loader: Loader = Loader("flaskr/compiler/from_server.json")
            context: Context = Context(
                loader.get_blocks(),
                loader.get_variables(),
                robot,  # reuse the same Robot/TestRobot instance
                socket_io,
            )

            for block in loader.get_blocks():
                block.execute(context)

        except Exception as e:
            ErrorManager.report(e)

    return render_template("index.html")


# Called when a new client connects
@socket_io.on("connect")
def handle_connect():
    print("[DEBUG] New client connected")
    robot.inform_about_move()


if __name__ == "__main__":
    socket_io.run(app, host="0.0.0.0", debug=True)


#TODO Joystick (Achsen mit knopfdruck)
#TODO Punktspeicherung mit Geschwindigkeitsfaktor
#TODO Exportieren und importieren von JSON im frontend um Programme zu speichern
#TODO Anleitung in die README.md schreiben
