import os, subprocess
from flask import Flask, send_from_directory, jsonify, request
from lib.constants import WALLPAPER_DIR
from lib.thumbnails import get_thumbnail
from lib import widget_manager
try:
    from Cocoa import NSScreen
except Exception:
    NSScreen = None


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


# --- Widget endpoints ---
@app.route("/api/widgets/config")
def widgets_config():
    """Get widget configuration (positions, enabled status, aspect ratios)."""
    config = widget_manager.get_widget_config()
    return jsonify({"widgets": config})


@app.route("/api/widgets/discover")
def widgets_discover():
    """Get list of available widgets (freshly discovered from filesystem)."""
    # Force fresh discovery on every call
    widgets = widget_manager.discover_widgets()
    return jsonify({"widgets": {k: {
        "id": v["id"],
        "aspect_ratio": v.get("aspect_ratio", 2.0)
    } for k, v in widgets.items()}})


@app.route("/api/widgets/config", methods=["POST"])
def update_widgets_config():
    """Update widget configuration."""
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Invalid payload"}), 400
    
    # Save configuration
    widget_manager.save_widget_config(data)
    
    # Reload daemon to apply changes
    if wallpaper_daemon:
        wallpaper_daemon.reload()
    
    return jsonify({"success": True})


@app.route("/widget_center/")
def widget_center():
    """Widget Center management page."""
    return send_from_directory(os.path.join(app.static_folder, "widget_center"), "index.html")


@app.route("/widgets/<widget_id>/frame")
def widget_frame(widget_id):
    """
    Serve an isolated widget frame (HTML with inline CSS/JS).
    Each widget gets its own execution context.
    """
    available = widget_manager.discover_widgets()
    if widget_id not in available:
        return "Widget not found", 404
    
    widget = available[widget_id]
    
    # Read widget files
    html_content = ""
    css_content = ""
    js_content = ""
    
    try:
        with open(widget["html"], "r") as f:
            html_content = f.read()
    except Exception as e:
        return f"Failed to load widget HTML: {e}", 500
    
    if widget["css"]:
        try:
            with open(widget["css"], "r") as f:
                css_content = f.read()
        except Exception:
            pass
    
    if widget["js"]:
        try:
            with open(widget["js"], "r") as f:
                js_content = f.read()
        except Exception:
            pass
    
    # Build isolated HTML frame
    frame_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
        * {{
            box-sizing: border-box;
        }}
        html, body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        #widget-root {{
            width: 100%;
            height: 100%;
            flex: 1;
            display: flex;
            flex-direction: column;
            container-type: size;
        }}
    </style>
    <style>
{css_content}
    </style>
</head>
<body>
    <div id="widget-root">
{html_content}
    </div>
    <script>
{js_content}
    </script>
</body>
</html>"""
    
    response = app.make_response(frame_html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


# --- API endpoints ---
@app.route("/api/wallpaper")
def wallpaper():
    global current_wallpaper
    if not current_wallpaper:
        return "No wallpaper selected", 404
    return send_from_directory(WALLPAPER_DIR, current_wallpaper)


@app.route('/api/screen')
def api_screen():
    """Return main screen dimensions in points."""
    # Return both the full screen frame and the visibleFrame (excludes menu bar/dock)
    if NSScreen is None:
        return jsonify({
            "frame": {"width": 1920, "height": 1080, "x": 0, "y": 0},
            "visible": {"width": 1920, "height": 1080, "x": 0, "y": 0}
        })
    try:
        screen = NSScreen.mainScreen()
        frame = screen.frame()
        visible = screen.visibleFrame()
        return jsonify({
            "frame": {
                "width": int(frame.size.width),
                "height": int(frame.size.height),
                "x": int(frame.origin.x),
                "y": int(frame.origin.y)
            },
            "visible": {
                "width": int(visible.size.width),
                "height": int(visible.size.height),
                "x": int(visible.origin.x),
                "y": int(visible.origin.y)
            }
        })
    except Exception:
        return jsonify({
            "frame": {"width": 1920, "height": 1080, "x": 0, "y": 0},
            "visible": {"width": 1920, "height": 1080, "x": 0, "y": 0}
        })


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


@app.route("/api/open_widgets_folder", methods=["POST"])
def open_widgets_folder():
    # Opens Finder at the widgets directory in Application Support (macOS)
    from lib.constants import WIDGETS_DIR
    try:
        subprocess.run(["open", WIDGETS_DIR])
        return {"success": True}
    except Exception:
        return {"success": False}, 500


@app.route("/api/wallpaper_thumbnails/<filename>")
def wallpaper_thumbnail(filename):
    if filename not in get_wallpapers():
        return "Wallpaper not found", 404
    
    thumb_path = get_thumbnail(filename)
    return send_from_directory(os.path.dirname(thumb_path), os.path.basename(thumb_path))
