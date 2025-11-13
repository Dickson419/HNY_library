#!/bin/bash
set -e

# ===============================
# Raspberry Pi Library App Setup
# ===============================

echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Installing Python3, venv, pip, git..."
sudo apt install -y python3 python3-venv python3-pip git

# Detect username and home folder
USER_NAME=$(whoami)
HOME_DIR=$(eval echo "~$USER_NAME")

echo "📦 Setting up environment for $USER_NAME in $HOME_DIR"

# Go to project folder (the folder where this script lives)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/HNY_library" || exit

echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

if [ -f ../requirements.txt ]; then
    echo "📚 Installing dependencies..."
    pip install -r ../requirements.txt
else
    echo "⚠️ No requirements.txt found, installing default packages..."
    pip install flask pillow qrcode schedule
fi

deactivate

# Create logs folder
mkdir -p logs
sudo chown "$USER_NAME":"$USER_NAME" logs

# --- Create systemd service ---
SERVICE_FILE="/etc/systemd/system/library_app.service"
echo "🛠️ Creating systemd service file at $SERVICE_FILE..."

sudo tee $SERVICE_FILE > /dev/null <<EOL
[Unit]
Description=Library Flask App
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$SCRIPT_DIR/HNY_library
Environment="PATH=$SCRIPT_DIR/HNY_library/venv/bin"
ExecStart=$SCRIPT_DIR/HNY_library/venv/bin/python $SCRIPT_DIR/HNY_library/library_app.py
Restart=always
RestartSec=10
StandardOutput=append:$SCRIPT_DIR/HNY_library/logs/app.log
StandardError=append:$SCRIPT_DIR/HNY_library/logs/app.log

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable library_app.service
sudo systemctl restart library_app.service

echo "✅ Setup complete!"
echo "Flask app is running and will auto-start on boot."
echo "View logs: tail -f $SCRIPT_DIR/HNY_library/logs/app.log"