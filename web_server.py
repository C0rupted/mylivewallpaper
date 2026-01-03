import os, subprocess
from flask import Flask, send_from_directory, jsonify, request
from lib.constants import WALLPAPER_DIR
from lib.thumbnails import get_thumbnail


app = Flask(__name__, static_folder="web", static_url_path="/web")
wallpaper_daemon = None
space_observer = None

# Currently selected wallpaper
current_wallpaper = None


def get_wallpapers():
    wallpapers = []
    for f in os.listdir(WALLPAPER_DIR):
        if f.lower().endswith((".mp4", ".mov", ".webm")):
            wallpapers.append(f)
    wallpapers.sort()
    return wallpapers

# Set default selection
if get_wallpapers():
    current_wallpaper = get_wallpapers()[0]


# --- Main page ---
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# --- Wallpaper selector page ---
@app.route("/wallpaper_selector/")
def wallpaper_selector_page():
    return send_from_directory(os.path.join(app.static_folder, "wallpaper_selector"), "index.html")



# --- API endpoints ---
@app.route("/api/wallpaper")
def wallpaper():
    global current_wallpaper
    if not current_wallpaper:
        return "No wallpaper selected", 404
    return send_from_directory(WALLPAPER_DIR, current_wallpaper)


@app.route("/api/wallpapers")
def list_wallpapers():
    wallpapers = get_wallpapers()
    return jsonify({"wallpapers": wallpapers, "selected": current_wallpaper})


@app.route("/api/select_wallpaper", methods=["POST"])
def select_wallpaper():
    global current_wallpaper
    data = request.json
    name = data.get("name")
    if name not in get_wallpapers():
        return "Wallpaper not found", 404

    current_wallpaper = name
    wallpaper_image_path = get_thumbnail(current_wallpaper)

    if space_observer:
        space_observer.current_wallpaper_path = wallpaper_image_path
        space_observer.reapply_wallpaper()

    if wallpaper_daemon:
        wallpaper_daemon.reload()

    print(f"Wallpaper selected: {name}")
    return jsonify({"selected": current_wallpaper})


@app.route("/api/open_wallpaper_folder", methods=["POST"])
def open_wallpaper_folder():
    # Opens Finder at the wallpaper directory (macOS)
    subprocess.run(["open", WALLPAPER_DIR])
    return {"success": True}


@app.route("/api/wallpaper_thumbnails/<filename>")
def wallpaper_thumbnail(filename):
    if filename not in get_wallpapers():
        return "Wallpaper not found", 404
    
    thumb_path = get_thumbnail(filename)
    return send_from_directory(os.path.dirname(thumb_path), os.path.basename(thumb_path))



