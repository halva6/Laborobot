from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def start():
    if request.method == "POST":
        command = request.get_json()
        print(f"command: {command}")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
