"""This module provides the entry point for the entire program; everything comes together here."""

import os
import json
import threading
import markdown
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
from markupsafe import Markup

from flaskr.compiler.blocks.block import Block
from flaskr.compiler.loader import Loader
from flaskr.compiler.context import Context
from flaskr.measurement import GoDirectDataCollector
from flaskr.server_error import ErrorManager, ServerError, ExecutionStartedError, NoDeviceConnected
from flaskr.robot_movement.test_robot import TestRobot

# Try to import real Robot (works only on Raspberry Pi with GPIO)
try:
    from RPi import GPIO
    from flaskr.robot_movement.robot import Robot
    GPIO_AVAILABLE: bool = True
except Exception:
    GPIO_AVAILABLE: bool = False


class App:
    """
    Flask application, SocketIO, and robot execution logic.
    """

    def __init__(self) -> None:
        """Initializes the Flask app, SocketIO, robot, and application constants."""
        self.__app: Flask = Flask(__name__)
        self.__app.config["SECRET_KEY"] = "sec,msdfgnß04835,mnvkmliouzh32409ß854309##.ret!"
        self.__socket_io: SocketIO = SocketIO(self.__app, async_mode="threading")

        ErrorManager.init(self.__socket_io)

        self.__base_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.__position_path: str = os.path.join(self.__base_dir, "robot_movement", "position.json")

        # Robot initialization
        if GPIO_AVAILABLE:
            self.__robot: Robot = Robot(GPIO_AVAILABLE, self.__socket_io, self.__position_path)
        else:
            self.__robot: TestRobot = TestRobot(GPIO_AVAILABLE, self.__socket_io, self.__position_path)

        # Constants
        self.__axles: list[str] = ["x", "y", "z"]
        self.__calc_operators: list[dict] = [
            {"value":"{", "text":"+"}, {"value":"}", "text":"-"}, {"value":"[", "text":"*"},
            {"value":"/", "text":"/"}, {"value":"pow", "text":"^"}, {"value":"sqrt", "text":"√"},
            {"value":"mod", "text":"mod"}, {"value":"and", "text":"and"}, {"value":"or", "text":"or"},
            {"value":"xor", "text":"xor"}, {"value":"not", "text":"not"}, {"value":"<<", "text":"<<"},
            {"value":">>", "text":">>"}
        ]
        self.__if_operators: list[str] = ["==","<=",">=","<",">","!="]
        self.__clipboards: int = 3

        self.__is_running: bool = False
        self.__lock: threading.Lock = threading.Lock()

        # Register routes and socket events
        self.__register_routes()
        self.__register_socket_events()

    def __register_routes(self) -> None:
        """Registers all Flask routes."""

        @self.__app.route("/", methods=["GET", "POST"])
        def start() -> str:
            """Handles GET and POST requests to start block execution."""
            with self.__lock:
                if request.method == "POST":
                    try:
                        if not self.__is_running:
                            self.__is_running = True
                            command = request.get_json()

                            json_path: str = os.path.join(self.__base_dir, "compiler", "from_server.json")
                            with open(json_path, "w", encoding="utf-8") as file:
                                file.write(json.dumps(command))

                            thread = threading.Thread(target=self.__execute, args=(json_path,), daemon=True)
                            thread.start()
                        else:
                            raise ExecutionStartedError("The program already started")
                    except ServerError as e:
                        ErrorManager.report(e)

            return render_template(
                "index.html",
                axles=self.__axles,
                clipboards=self.__clipboards,
                calc_operators=self.__calc_operators,
                if_operators=self.__if_operators
            )

        @self.__app.route("/info-md/<page>")
        def info_md_page(page: str):
            """Loads various Markdown files safely."""
            pages: dict = {
                "general": "static/software_info/generel.md",
                "blocks": "static/software_info/blocks.md",
                "programming": "static/software_info/programming.md",
                "manual_control": "static/software_info/manual_control.md"
            }

            if page not in pages:
                return jsonify({"error": "invalid page"}), 404

            md_path: str = os.path.join(self.__base_dir, pages[page])
            if not os.path.exists(md_path):
                return jsonify({"error": "file not found"}), 404

            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            html_content: str = markdown.markdown(md_content, extensions=["fenced_code", "tables", "sane_lists", "nl2br"])
            return Markup(html_content)

    def __register_socket_events(self) -> None:
        """Registers SocketIO events."""

        @self.__socket_io.on("connect")
        def handle_connect():
            """Handles new client connections and sends the current robot coordinates."""
            print("[DEBUG] New client connected")
            self.__robot.inform_about_move()

    def __execute(self, json_path: str) -> None:
        """
        Executes the instructions from a JSON file.
        This is the first function executed by the thread system.

        Args:
            json_path (str): path of the JSON file containing the client's instructions
        """
        try:
            loader: Loader = Loader(json_path)

            is_measurement_block: bool = any(self.__check_measurement_block(block) for block in loader.blocks)
            go_direct_data_collector: GoDirectDataCollector = None

            if is_measurement_block:
                try:
                    go_direct_data_collector = GoDirectDataCollector()
                    go_direct_data_collector.start()
                except RuntimeError as e:
                    raise NoDeviceConnected(
                        "There is no GoDirect device - either connect one or remove the measurement block."
                    ) from e

            context: Context = Context(loader.blocks, loader.variables, self.__robot, go_direct_data_collector, self.__socket_io)
            print("[DEBUG] thread started")

            for block in loader.blocks:
                block.execute(context)

            if is_measurement_block:
                go_direct_data_collector.stop()

        except ServerError as e:
            ErrorManager.report(e)
        finally:
            with self.__lock:
                self.__is_running = False
                print("[DEBUG] thread finished")

    def __check_measurement_block(self, block: Block) -> bool:
        """
        Recursively checks if a block or its children is a measurement block.

        Args:
            block (Block): block to check

        Returns:
            bool: True if measurement block exists, False otherwise
        """
        if "measurement" in block.block_id:
            return True
        if block.has_children():
            return any(self.__check_measurement_block(child) for child in block.children)
        return False

    def run(self, host:str = "0.0.0.0", port:int = 5000, debug:bool = True) -> None:
        """Runs the Flask-SocketIO server."""
        self.__socket_io.run(self.__app, host=host, port=port, debug=debug)


if __name__ == "__main__":
    robot_app = App()
    robot_app.run()
