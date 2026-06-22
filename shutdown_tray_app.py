import os
import pystray
from pystray import MenuItem as Item
from PIL import Image, ImageDraw


# ---------- SYSTEM ACTIONS ----------

def restart(icon, item):
    os.system("shutdown /r /t 0")

def restart_time(icon, item):
    os.system("shutdown /r /t 30")

def logout(icon, item):
    os.system("shutdown /l")

def shutdown(icon, item):
    os.system("shutdown /s /t 0")

def exit_app(icon, item):
    icon.stop()


# ---------- POWER ICON (perfect top gap + larger circle + extended line) ----------

def create_power_icon():
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    center = size // 2          # 128
    radius = 120                # larger circle for bold look
    thickness = 34              # thicker outline

    # Circle bounding box
    bbox = [center - radius, center - radius, center + radius, center + radius]

    # Arc with small top gap
    # 0° = right, 90° = bottom, 180° = left, 270° = top
    # Gap from 255° to 285° (tight around top)
    d.arc(
        bbox,
        start=285,     # right side of top
        end=255,       # left side of top
        fill="white",
        width=thickness
    )

    # Vertical line slightly outside the circle (for beauty)
    line_top_y = center - radius - 16     # shifted upward more
    line_bottom_y = center + 18           # reaches slightly below center

    d.line(
        [
            (center, line_top_y),
            (center, line_bottom_y)
        ],
        fill="white",
        width=thickness
    )

    # Smooth downscale to tray size
    return img.resize((64, 64), Image.LANCZOS)


# ---------- TRAY ICON APP ----------

def main():
    menu = pystray.Menu(
        Item("Restart", restart),
        Item("Restart (30s)", restart_time),
        Item("Log Out", logout),
        Item("Shut Down", shutdown),
        Item("Exit", exit_app)
    )

    icon = pystray.Icon(
        "ShutdownTray",
        create_power_icon(),
        "System Power Controls",
        menu
    )

    icon.run()


if __name__ == "__main__":
    main()
