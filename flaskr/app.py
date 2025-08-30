from flask import Flask
from flask import render_template
from flask import request

from compiler.robot import Robot
from compiler.loader import Loader
from compiler.context import Context

import json

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def start():
    if request.method == "POST":
        command = request.get_json()

        with open("flaskr/compiler/from_server.json","w") as file:
            file.write(json.dumps(command))

        robot = Robot()
        loader = Loader("flaskr/compiler/from_server.json")
        context = Context(loader.get_blocks(), robot)

        for block in loader.get_blocks():
            block._execute(context, robot)

        print(f"command: {command} + type of command {type(command)}")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
