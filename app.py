# /home/admin/Laborroboter/app.py
from flask import Flask, render_template, request, redirect, url_for, json
from web_function_manager import WebFunctionManager

app = Flask(__name__)
robot = WebFunctionManager()

@app.route("/")
def index():
    return render_template("index.html",
                           positions=robot.get_positions(),
                           saved_positions=robot.get_saved_positions())

@app.route("/move", methods=["POST"])
def move():
    axis = request.form["axis"]
    direction = request.form["direction"] == "true"
    robot.move(axis, direction)
    return redirect(url_for("index"))

@app.route("/save/<int:index>", methods=["POST"])
def save(index):
    robot.save_current_position(index)
    return redirect(url_for("index"))

@app.route("/goto/<int:index>", methods=["POST"])
def goto(index):
    success = robot.move_to_saved_position(index)
    if not success:
        return f"Position {index+1} ist leer.", 400
    return redirect(url_for("index"))

@app.route("/zero", methods=["POST"])
def zero():
    robot.set_axis_to_zero()
    return redirect(url_for("index"))

@app.route("/api/positions")
def api_positions():
    return jsonify({
        "current": robot.get_positions(),
        "saved": robot.get_saved_positions()
    })

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
