import os, shutil

APP_SUPPORT_DIR = os.path.expanduser("~/Library/Application Support/MyLiveWallpaper")
WALLPAPER_DIR = os.path.join(APP_SUPPORT_DIR, "wallpapers")
CACHE_DIR = "/tmp/mylivewallpaper_cache"
WIDGETS_DIR = os.path.join(APP_SUPPORT_DIR, "widgets")

WIDGETS_CONFIG_FILE = os.path.join(APP_SUPPORT_DIR, "widget_config.json")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


# Default widget configuration (moved from widget_manager)
# By default include only the sample widget enabled
DEFAULT_WIDGET_CONFIG = [
    {"id": "clock", "enabled": True, "x": 100, "y": 100, "height": 100},
    {"id": "sample", "enabled": True, "x": 300, "y": 300, "height": 100},
]



# Ensure all directories exist
os.makedirs(APP_SUPPORT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(WIDGETS_DIR, exist_ok=True)

# Ensure widgets directory exists in App Support. If empty, populate from example widgets
# Project examples directory (contains starter widgets/backgrounds)
EXAMPLES_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "examples")
EXAMPLES_WIDGETS = os.path.join(EXAMPLES_DIR, "widgets")
EXAMPLES_WALLPAPERS = os.path.join(EXAMPLES_DIR, "wallpapers")

# Ensure wallpaper directory exists. If missing, copy example wallpapers there
if not os.path.isdir(WALLPAPER_DIR):
    shutil.copytree(EXAMPLES_WALLPAPERS, WALLPAPER_DIR)


# If widgets directory inside App Support is empty, copy example widgets there
if os.path.isdir(EXAMPLES_WIDGETS) and not os.listdir(WIDGETS_DIR):
    for name in os.listdir(EXAMPLES_WIDGETS):
        src = os.path.join(EXAMPLES_WIDGETS, name)
        dst = os.path.join(WIDGETS_DIR, name)
        if os.path.isdir(src) and not os.path.exists(dst):
            shutil.copytree(src, dst)
