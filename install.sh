#!/data/data/com.termux/files/usr/bin/bash
# install.sh

echo "Installing Termux Runner..."

# 1. Install dependencies
pkg update -y
pkg install -y python python-tkinter python-pillow xdg-utils desktop-file-utils

# Install CustomTkinter
pip install customtkinter pillow

# 2. Setup strict Termux paths
APP_DIR="$HOME/.local/opt/termux-runner"
BIN_DIR="$PREFIX/bin"
APP_MENU_DIR="$HOME/.local/share/applications"

mkdir -p "$APP_DIR"
mkdir -p "$APP_MENU_DIR"

# 3. Move files to directories
cp app.py "$APP_DIR/"
cp launch.sh "$APP_DIR/"
cp uninstall.sh "$APP_DIR/"
cp app.desktop "$APP_MENU_DIR/termux-runner.desktop"
cp readme.md "$APP_DIR/"

# 4. Generate Icon and Screenshot dynamically (Using Python Pillow)
echo "Generating local assets..."
python -c "
from PIL import Image, ImageDraw
# Create Icon
icon = Image.new('RGB', (256, 256), color='#1f538d')
d = ImageDraw.Draw(icon)
d.text((50, 100), 'RUNNER', fill='white')
icon.save('$APP_DIR/icon.png')

# Create Screenshot
screen = Image.new('RGB', (400, 600), color='#1e1e1e')
d2 = ImageDraw.Draw(screen)
d2.rectangle([160, 430, 190, 480], fill='#1f538d') # Player
d2.rectangle([60, 100, 90, 150], fill='#c93434')   # Obstacle
screen.save('$APP_DIR/screenshot.png')
"

# 5. Set Permissions
chmod +x "$APP_DIR/launch.sh"
chmod +x "$APP_DIR/uninstall.sh"

# Create a global command wrapper
cat << 'EOF' > "$BIN_DIR/termux-runner"
#!/data/data/com.termux/files/usr/bin/bash
/data/data/com.termux/files/home/.local/opt/termux-runner/launch.sh
EOF
chmod +x "$BIN_DIR/termux-runner"

# 6. Update Desktop Database for XFCE4
update-desktop-database "$APP_MENU_DIR"

echo "Installation complete! You can find the game in your XFCE4 Application menu under 'Games', or run 'termux-runner' in the terminal."