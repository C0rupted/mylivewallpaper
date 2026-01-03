import os, shutil

APP_SUPPORT_DIR = os.path.expanduser("~/Library/Application Support/MyLiveWallpaper")
WALLPAPER_DIR = os.path.join(APP_SUPPORT_DIR, "wallpapers")
CACHE_DIR = "/tmp/mylivewallpaper_cache"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))




# Ensure all directories exist
os.makedirs(APP_SUPPORT_DIR, exist_ok=True)

if not os.path.isdir(WALLPAPER_DIR):
    os.makedirs(WALLPAPER_DIR, exist_ok=True)
    shutil.copy(os.path.join(CURRENT_DIR, "static", "sample_wallpaper.mp4"), os.path.join(WALLPAPER_DIR, "Ocean.mp4"))

os.makedirs(CACHE_DIR, exist_ok=True)