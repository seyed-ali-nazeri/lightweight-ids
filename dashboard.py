from flask import Flask, render_template
import json, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENT_FILE = os.path.join(BASE_DIR, "data", "events.json")

@app.route("/")
def index():
    events = []

    try:
        if os.path.exists(EVENT_FILE):
            with open(EVENT_FILE, "r") as f:
                events = json.load(f)
    except Exception as e:
        return f"<h1>Dashboard Error</h1><pre>{e}</pre>"

    stats = {
        "CRITICAL": sum(1 for e in events if e.get("level")=="CRITICAL"),
        "WARNING": sum(1 for e in events if e.get("level")=="WARNING"),
        "INFO": sum(1 for e in events if e.get("level")=="INFO"),
    }

    return render_template("index.html", events=events[::-1], stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
