"""
franklins-dash — A clean, simple dashboard for Home Assistant
Serves a web UI that communicates directly with HA's WebSocket API.
"""

import json
from flask import Flask, render_template, jsonify

app = Flask(
    __name__,
    template_folder="web/templates",
    static_folder="web/static"
)

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)


@app.route("/")
def index():
    """Serve the main dashboard UI."""
    return render_template("index.html")


@app.route("/api/config")
def get_config():
    """Provide configuration to the frontend."""
    return jsonify(config)


if __name__ == "__main__":
    print("=" * 50)
    print("  franklins-dash")
    print(f"  HA: {config['ha']['url']}:{config['ha']['port']}")
    print(f"  Rooms: {len(config['rooms'])}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
