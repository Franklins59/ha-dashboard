# franklins-dash

A clean, minimal dashboard for Home Assistant — designed for wall-mounted tablets.

![franklins](static/logo.png)

## What it does

Replaces the Lovelace UI with a simple, touch-friendly interface. HA runs headless as the backend; franklins-dash is the only thing your household sees.

```
[Tablet Browser] → [RPi: Flask] → [HA WebSocket API] → [Devices]
```

**Features:**
- Room-based layout with switches, dimmers, covers, and sensors
- Cover control with open/stop/close buttons and position slider
- Dimmer brightness control
- Real-time state updates via WebSocket
- Auto dark/light theme (switches at 07:00 / 20:00)
- Tablet landscape optimized
- Configuration via a single JSON file — no YAML, no Lovelace

## Setup

**Requirements:** Raspberry Pi (3B+ or newer), Python 3.11+, Home Assistant instance on the network.

```bash
# Clone
git clone https://github.com/Franklins59/franklins-dash.git
cd franklins-dash

# Configure
cp config.example.json config.json
# Edit config.json: set HA IP, token, rooms and devices

# Install & start (handles venv, systemd, port 80)
sudo bash setup.sh
```

Open `http://<pi-ip>` on your tablet.

### Home Assistant Token

In HA, go to your Profile (bottom left) → scroll to "Long-Lived Access Tokens" → create one. Copy it into `config.json`.

## Configuration

All configuration lives in `config.json`. No database, no YAML.

```json
{
  "ha": {
    "url": "192.168.1.20",
    "port": 8123,
    "token": "YOUR_TOKEN"
  },
  "rooms": [
    {
      "id": "living",
      "name": "Wohnzimmer",
      "icon": "🛋️",
      "devices": [
        { "entity_id": "switch.light_1", "name": "Decke", "type": "switch" },
        { "entity_id": "cover.shutter_1", "name": "Jalousie", "type": "cover" },
        { "entity_id": "sensor.temp_1", "name": "Temperatur", "type": "sensor", "unit": "°C" }
      ]
    }
  ]
}
```

### Device types

| Type | Controls | Notes |
|---|---|---|
| `switch` | Toggle on/off | For relays, plugs |
| `light` | Toggle + brightness slider | Slider appears when light is on |
| `cover` | Open / Stop / Close + position | For shutters, blinds |
| `sensor` | Display only | Shows value + unit |

## Security

`config.json` contains your HA token and is excluded from git via `.gitignore`. Never commit it to a public repository.

## License

MIT

---

*Part of the [franklins](https://franklins.forstec.ch) smart home toolkit.*
