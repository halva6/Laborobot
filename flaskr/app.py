"""This module provides the entry point for the entire program; everything comes together here."""

import os
import json
import threading
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
socket_io: SocketIO = SocketIO(app, async_mode="threading")

ErrorManager.init(socket_io)

# Create the Robot/TestRobot only once
base_dir = os.path.dirname(os.path.abspath(__file__))
position_path = os.path.join(base_dir, "robot_movement", "position.json")
if gpio_available:
    robot: Robot = Robot(gpio_available, socket_io, position_path)
else:
    robot: TestRobot = TestRobot(gpio_available, socket_io, position_path)


axles:list = ["x","y","z"]
calc_operators:list[dict] = [{"value":"{", "text":"+"},
                            {"value":"}", "text":"-"},
                            {"value":"[", "text":"*"},
                            {"value":"/", "text":"/"},
                            {"value":"pow", "text":"^"},
                            {"value":"sqrt", "text":"√"},
                            {"value":"mod", "text":"mod"},
                            {"value":"and", "text":"and"},
                            {"value":"or", "text":"or"},
                            {"value":"xor", "text":"xor"},
                            {"value":"not", "text":"not"},
                            {"value":"<<", "text":"<<"},
                            {"value":">>", "text":">>"},]

if_operators:list[dict] = ["==","<=",">=","<",">","!="]
clipboards:int = 3

is_running:bool = False
lock:threading.Lock = threading.Lock()

def execute(json_path:str, socket_io_p:SocketIO) -> None:
    """
    executes the instructions
    this is the first function executed by the thread system
    args:
        json_path (str): path of the json-file, this file contains the client's instructions on what the robot should do
    """
    try:
        loader: Loader = Loader(json_path)
        context: Context = Context(
            loader.blocks,
            loader.variables,
            robot,  # reuse the same Robot/TestRobot instance
            socket_io_p)
        print("[DEBUG] thread started")


        for block in loader.blocks:
            block.execute(context)

    except ServerError as e:
        ErrorManager.report(e)
    finally:
        with lock:
            global is_running
            is_running = False
            print("[DEBUG] thread finished")

@app.route("/", methods=["GET", "POST"])
def start():
    """
    handles get and post requests to start block execution
    for post requests it saves the received json command, loads blocks and executes them
    returns:
        str: rendered html template
    """
    global is_running
    with lock:
        if request.method == "POST" and not is_running:
            is_running = True
            command = request.get_json()

            json_path:str = os.path.join(base_dir, "compiler", "from_server.json")

            with open(json_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(command))
            
            thread = threading.Thread(target=execute, args=(json_path, socket_io,), daemon=True)
            thread.start()

    return render_template("index.html", axles = axles, clipboards=clipboards, calc_operators=calc_operators, if_operators=if_operators)

@app.route('/info-md/<page>')
def info_md_page(page:str):
    """loads various Markdown files safely"""
    # Whitelisting
    pages:dict = {
        "general": "static/software_info/generel.md",
        "blocks": "static/software_info/blocks.md",
        "programming": "static/software_info/programming.md",
        "manual_control": "static/software_info/manual_control.md"
    }

    if page not in pages:
        return jsonify({"error": "invalid page"}), 404

    md_path:str = os.path.join(os.path.dirname(__file__), pages[page])
    if not os.path.exists(md_path):
        return jsonify({"error": "file not found"}), 404

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content:str = markdown.markdown(md_content, extensions=["fenced_code", "tables", "sane_lists", "nl2br"])
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


#TODO Exportieren und importieren von JSON im frontend um Programme zu speichern
#TODO Anleitung in die README.md schreiben