from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO, emit

from compiler.robot import Robot
from compiler.loader import Loader
from compiler.context import Context

from compiler.Blocks.block import *
from compiler.server_error import *

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
            robot: Robot = Robot()
            loader: Loader = Loader("flaskr/compiler/from_server.json", socket_io)
            context: Context = Context(loader.get_blocks(), robot)

            for block in loader.get_blocks():
                block.execute(context, robot)
        except Exception as e:
            ErrorManager.report(e)

    return render_template("index.html")

if __name__ == "__main__":
    socket_io.run(app, host='0.0.0.0',)
