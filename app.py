"""
franklins-dash — A clean, simple dashboard for Home Assistant
Serves a web UI that communicates directly with HA's WebSocket API.
"""

import json
import requests
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, jsonify, request

app = Flask(
    __name__,
    template_folder="web/templates",
    static_folder="web/static"
)


def load_json(path):
    """Load and return JSON file contents."""
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    """Save data to JSON file with pretty formatting."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    """Serve the main dashboard UI."""
    return render_template("index.html")


@app.route("/settings")
def settings_page():
    """Serve the settings page."""
    return render_template("settings.html")


@app.route("/wizard")
def wizard_page():
    """Serve the configuration wizard."""
    return render_template("wizard.html")


@app.route("/api/settings", methods=["GET"])
def get_settings():
    """Provide system settings to the frontend (reloads on each request)."""
    return jsonify(load_json("settings.json"))


@app.route("/api/settings", methods=["POST"])
def save_settings():
    """Save updated settings."""
    data = request.get_json()
    save_json("settings.json", data)
    return jsonify({"status": "ok"})


@app.route("/api/config", methods=["GET"])
def get_config():
    """Provide room/device config to the frontend (reloads on each request)."""
    return jsonify(load_json("config.json"))


@app.route("/api/config", methods=["POST"])
def save_config():
    """Save updated config."""
    data = request.get_json()
    save_json("config.json", data)
    return jsonify({"status": "ok"})


@app.route("/api/ha/entities")
def ha_entities():
    """Proxy: Fetch all entities from Home Assistant."""
    try:
        settings = load_json("settings.json")
        ha = settings["ha"]
        url = f"http://{ha['url']}:{ha['port']}/api/states"
        headers = {"Authorization": f"Bearer {ha['token']}"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        # Return simplified entity list
        entities = []
        for e in resp.json():
            entities.append({
                "entity_id": e["entity_id"],
                "state": e["state"],
                "friendly_name": e.get("attributes", {}).get("friendly_name", ""),
                "domain": e["entity_id"].split(".")[0]
            })
        entities.sort(key=lambda x: x["entity_id"])
        return jsonify(entities)
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route("/weather")
def weather_page():
    """Serve the weather station page."""
    return render_template("weather.html")


@app.route("/energy")
def energy_page():
    """Serve the energy monitoring page."""
    return render_template("energy.html")


@app.route("/api/ha/history")
def ha_history():
    """Proxy: Fetch history data from Home Assistant."""
    try:
        settings = load_json("settings.json")
        ha = settings["ha"]
        entity_ids = request.args.get("entity_ids", "")
        hours = request.args.get("hours", "24")

        end = datetime.now(timezone.utc)
        start = end - timedelta(hours=int(hours))

        # Format timestamps without timezone suffix for HA compatibility
        start_str = start.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%S")

        base_url = f"http://{ha['url']}:{ha['port']}/api/history/period/{start_str}"
        params = {
            "filter_entity_id": entity_ids,
            "end_time": end_str,
            "minimal_response": "",
            "no_attributes": ""
        }
        headers = {"Authorization": f"Bearer {ha['token']}"}
        print(f"[History] Fetching {hours}h for {len(entity_ids.split(','))} entities...")
        resp = requests.get(base_url, params=params, headers=headers, timeout=30)
        print(f"[History] HA response: {resp.status_code}")
        resp.raise_for_status()
        data = resp.json()
        print(f"[History] Got {len(data)} entity arrays")
        return jsonify(data)
    except Exception as ex:
        print(f"[History] Error: {ex}")
        return jsonify({"error": str(ex)}), 500


if __name__ == "__main__":
    settings = load_json("settings.json")
    config = load_json("config.json")
    print("=" * 50)
    print(f"  franklins-dash — {settings['building']}")
    print(f"  HA: {settings['ha']['url']}:{settings['ha']['port']}")
    print(f"  Rooms: {len(config['rooms'])}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)