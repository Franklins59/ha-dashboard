#!/bin/bash
# franklins-dash setup: venv, autostart, port 80 redirect
# Usage: sudo bash setup.sh

set -e

DASH_USER=$(logname)
DASH_DIR="/home/$DASH_USER/franklins-dash"

echo "=== franklins-dash setup ==="
echo "User: $DASH_USER"
echo "Dir:  $DASH_DIR"
echo ""

# 1. Python venv
echo "[1/4] Setting up Python venv..."
sudo -u "$DASH_USER" python3 -m venv "$DASH_DIR/venv"
sudo -u "$DASH_USER" "$DASH_DIR/venv/bin/pip" install -r "$DASH_DIR/requirements.txt"

# 2. Systemd service
echo "[2/4] Installing systemd service..."
sed "s|YOUR_USER|$DASH_USER|g" "$DASH_DIR/franklins-dash.service" > /etc/systemd/system/franklins-dash.service
systemctl daemon-reload
systemctl enable franklins-dash
systemctl start franklins-dash

# 3. Port 80 redirect
echo "[3/4] Setting up port 80 redirect..."
apt install -y iptables iptables-persistent
iptables -t nat -C PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000 2>/dev/null || \
  iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000
netfilter-persistent save

# 4. Verify
echo "[4/4] Verifying..."
sleep 2
systemctl status franklins-dash --no-pager

echo ""
echo "=== Done ==="
echo "Dashboard: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Don't forget to create config.json from config.example.json!"
