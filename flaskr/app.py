"""This module provides the entry point for the entire program; everything comes together here."""

import os
import json
import markdown
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
from markupsafe import Markup

from flaskr.robot_movement.test_robot import TestRobot
from flaskr.compiler.loader import Loader
from flaskr.compiler.context import Context
from flaskr.server_error import ErrorManager, ServerError

# Try to import real Robot (works only on Raspberry Pi with GPIO)
try:
    import RPi.GPIO as GPIO
    from flaskr.robot_movement.robot import Robot

    gpio_available: bool = True
except Exception:
    gpio_available: bool = False

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "sec,msdfgnß04835,mnvkmliouzh32409ß854309##.ret!"
socket_io: SocketIO = SocketIO(app)

ErrorManager.init(socket_io)

# Create the Robot/TestRobot only once
base_dir = os.path.dirname(os.path.abspath(__file__))
position_path = os.path.join(base_dir, "robot_movement", "position.json")
if gpio_available:
    robot: Robot = Robot(gpio_available, socket_io, position_path)
else:
    robot: TestRobot = TestRobot(gpio_available, socket_io, position_path)


@app.route("/", methods=["GET", "POST"])
def start():
    """
    handles get and post requests to start block execution
    for post requests it saves the received json command, loads blocks and executes them
    returns:
        str: rendered html template
    """
    if request.method == "POST":
        command = request.get_json()

        json_path = os.path.join(base_dir, "compiler", "from_server.json")

        with open(json_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(command))

        try:
            loader: Loader = Loader(json_path)
            context: Context = Context(
                loader.blocks,
                loader.variables,
                robot,  # reuse the same Robot/TestRobot instance
                socket_io,
            )

            for block in loader.blocks:
                block.execute(context)

        except ServerError as e:
            ErrorManager.report(e)

    return render_template("index.html")

@app.route('/info-md/<page>')
def info_md_page(page):
    """Lädt verschiedene Markdown-Dateien sicher."""
    # Whitelisting
    pages = {
        "general": "static/software_info/generel.md",
        "blocks": "static/software_info/blocks.md",
        "programming": "static/software_info/programming.md"
    }

    if page not in pages:
        return jsonify({"error": "invalid page"}), 404

    md_path = os.path.join(os.path.dirname(__file__), pages[page])
    if not os.path.exists(md_path):
        return jsonify({"error": "file not found"}), 404

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables"])
    return Markup(html_content)

# Called when a new client connects
@socket_io.on("connect")
def handle_connect():
    """
    handles new client connections and sends the current robot coordinates
    """
    print("[DEBUG] New client connected")
    robot.inform_about_move()

if __name__ == "__main__":
    socket_io.run(app, host="0.0.0.0", port=5000, debug=True)


#TODO Punktspeicherung mit Geschwindigkeitsfaktor
#TODO Exportieren und importieren von JSON im frontend um Programme zu speichern
#TODO Anleitung in die README.md schreiben
