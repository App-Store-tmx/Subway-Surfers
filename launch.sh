#!/data/data/com.termux/files/usr/bin/bash
# launch.sh

# Termux home pathing
APP_DIR="$HOME/.local/opt/termux-runner"

# Ensure X11 display is exported if running from a non-X terminal but targeting XFCE4
export DISPLAY=:0

# Launch the game
cd "$APP_DIR" || exit 1
python app.py