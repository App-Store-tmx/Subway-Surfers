#!/data/data/com.termux/files/usr/bin/bash
# uninstall.sh

echo "Removing Termux Runner..."

APP_DIR="$HOME/.local/opt/termux-runner"
BIN_DIR="$PREFIX/bin"
APP_MENU_DIR="$HOME/.local/share/applications"

# Remove core files
rm -rf "$APP_DIR"
rm -f "$BIN_DIR/termux-runner"
rm -f "$APP_MENU_DIR/termux-runner.desktop"

# Refresh desktop DB
update-desktop-database "$APP_MENU_DIR"

echo "Uninstallation complete."