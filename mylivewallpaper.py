from flask import Flask, send_from_directory, jsonify, abort
from moviepy import VideoFileClip

import subprocess, threading, shutil, rumps, os


app = Flask(__name__, static_folder="static", static_url_path="/static")


# Directories

APP_SUPPORT_DIR = os.path.expanduser("~/Library/Application Support/MyLiveWallpaper")
WALLPAPER_DIR = os.path.join(APP_SUPPORT_DIR, "wallpapers")
CACHE_DIR = "/tmp/mylivewallpaper_cache"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


os.makedirs(APP_SUPPORT_DIR, exist_ok=True)
# Ensure wallpaper directory exists and has at least one sample wallpaper
if not os.path.isdir(WALLPAPER_DIR):
    os.makedirs(WALLPAPER_DIR, exist_ok=True)
    shutil.copy(os.path.join(CURRENT_DIR, "static", "sample_wallpaper.mp4"), os.path.join(WALLPAPER_DIR, "Ocean.mp4"))

os.makedirs(CACHE_DIR, exist_ok=True)



# Helper function for setting wallpaper
def set_wallpaper(name):
    file_path = os.path.join(CACHE_DIR, f"{name}.jpg")

    print(f"Setting desktop wallpaper to {file_path}")
    applescript_commands = [f"""tell application "System Events" to set picture of every desktop to "{file_path}" """,
                            f"""tell application "Finder" to set desktop picture to POSIX file "{file_path}" """]
    for command in applescript_commands:
        os.system(f"osascript -e '{command}'")
    os.system("killall SystemUIServer > /dev/null")  # Refresh menu bar



def run_script(script: str, script_type: str = "applescript"):

    command = "osascript" if script_type == "applescript" else "sh"
    extension = ".applescript" if script_type == "applescript" else ".sh"

    path = os.path.join(CURRENT_DIR, "scripts", (script+extension))

    try:
        result = subprocess.run(
            [command, path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")



@app.route("/api/menubarheight")
def get_menubar_height():
    return run_script("getMenuBarHeight")

@app.route("/api/openwallpaperfolder")
def open_wallpaper_folder():
    os.system(f"open '{WALLPAPER_DIR}'")
    return ""



@app.route("/api/wallpapers")
def list_wallpapers():
    wallpapers = []

    for filename in os.listdir(WALLPAPER_DIR):
        if filename.lower().endswith((".mp4", ".mov", ".webm")):
            name = os.path.splitext(filename)[0]
            wallpapers.append({
                "name": name,
                "thumbnail": f"/api/thumb/{name}",
                "video": f"/api/video/{name}"
            })
    wallpapers.sort(key=lambda x: x["name"].lower())
    return jsonify(wallpapers)



@app.route("/api/video/<name>")
def get_video(name):
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-'))
    file_path = os.path.join(WALLPAPER_DIR, f"{safe_name}.mp4")
    if not os.path.exists(file_path):
        abort(404)

    set_wallpaper(name)

    return send_from_directory(WALLPAPER_DIR, f"{safe_name}.mp4")



@app.route("/api/thumb/<name>")
def get_thumb(name):
    thumb_path = os.path.join(CACHE_DIR, f"{name}.jpg")
    video_path = os.path.join(WALLPAPER_DIR, f"{name}.mp4")

    if not os.path.exists(video_path):
        abort(404)

    # Generate thumbnail if missing
    if not os.path.exists(thumb_path):
        try:
            with VideoFileClip(video_path) as clip:
                frame = clip.get_frame(0.0)  # first frame
                from PIL import Image
                image = Image.fromarray(frame)
                image.save(thumb_path, "JPEG")
        except Exception as e:
            print(f"Failed to make thumbnail for {name}: {e}")
            abort(500)

    return send_from_directory(CACHE_DIR, f"{name}.jpg")



class MyLiveWallpaper(rumps.App):
    def __init__(self):
        super(MyLiveWallpaper, self).__init__("MyLiveWallpaper", icon="static/mylivewallpaper.icns")
        

if __name__ == "__main__":
    # Run Flask in a background thread
    server_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False),
        daemon=True
    )
    server_thread.start()

    # Run the menu bar app in the main thread
    MyLiveWallpaper().run()

    
    
