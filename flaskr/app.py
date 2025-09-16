from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO, emit

from robot_movement.test_robot import TestRobot
from compiler.loader import Loader
from compiler.context import Context

from compiler.blocks.block import *
from server_error import *

#TODO Testing if it works with the management of imports on the Raspberry Pi
try: 
    import RPi.GPIO as GPIO
    from robot_movement.robot import Robot
    gpio_avialable:bool = True
except Exception:
    gpio_avialable:bool = False


import json

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = 'sec,msdfgnß04835,mnvkmliouzh32409ß854309##.ret!'
socket_io:SocketIO = SocketIO(app)

ErrorManager.init(socket_io)

@app.route("/", methods = ["GET", "POST"])
def start():
    if request.method == "POST":
        command = request.get_json()

        with open("flaskr/compiler/from_server.json","w") as file:
            file.write(json.dumps(command))

        try:
            loader: Loader = Loader("flaskr/compiler/from_server.json", socket_io)
            if gpio_avialable:
                context: Context = Context(loader.get_blocks(), loader.get_variables(), Robot(gpio_avialable))

            else:
                context: Context = Context(loader.get_blocks(), loader.get_variables(), TestRobot(gpio_avialable))



            for block in loader.get_blocks():
                block.execute(context)
        except Exception as e:
            ErrorManager.report(e)

    return render_template("index.html")

if __name__ == "__main__":
    socket_io.run(app, host='0.0.0.0',debug=True)
