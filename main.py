import threading, rumps

from wallpaper_daemon import WallpaperDaemon
from lib.web_window import WebWindowManager
from lib.system_wallpaper import SpaceObserver, set_macos_wallpaper
from lib.thumbnails import get_thumbnail
from lib.settings_manager import SettingsManager

import web_server



def run_flask():
    web_server.app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)


class MyLiveWallpaper(rumps.App):
    def __init__(self):
        super(MyLiveWallpaper, self).__init__(
            "MyLiveWallpaper",
            icon="mylivewallpaper.icns"
        )

        # Initialize settings manager
        settings_manager = SettingsManager()
        web_server.settings_manager = settings_manager

        # Start Flask in background
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # --- Initialize SpaceObserver ---
        def wallpaper_callback():
            """Called on space change or wake."""
            if self.space_observer.current_wallpaper_path:
                set_macos_wallpaper(self.space_observer.current_wallpaper_path)

        self.space_observer = SpaceObserver.alloc().initWithCallback_(wallpaper_callback)
        self.space_observer.install_space_observers()

        # Make observer available to Flask server
        web_server.space_observer = self.space_observer

        # Create wallpaper daemon
        self.daemon = WallpaperDaemon()
        self.daemon.create_window()
        web_server.wallpaper_daemon = self.daemon

        self.windows = WebWindowManager()

        # Initialize wallpaper with saved settings
        web_server.initialize_wallpaper()

        self.menu = [
            rumps.MenuItem("Refresh Wallpaper", self.refresh_wallpaper),
            rumps.MenuItem("Open Wallpaper Library", self.open_library),
            rumps.MenuItem("Widget Center", self.open_widget_center),
        ]

        # --- Set initial wallpaper if any ---
        if web_server.current_wallpaper:
            wallpaper_path = get_thumbnail(web_server.current_wallpaper)
            self.space_observer.current_wallpaper_path = wallpaper_path
            self.space_observer.reapply_wallpaper()

    def refresh_wallpaper(self, _):
        self.daemon.reload()
    

    def open_library(self, _):
        self.windows.open_window("http://localhost:8000/wallpaper_selector/", "Wallpaper Library")

    def open_widget_center(self, _):
        self.windows.open_window("http://localhost:8000/widget_center/", "Widget Center", width=1200, height=800)

    def quit_app(self, _):
        rumps.quit_application()


if __name__ == "__main__":
    MyLiveWallpaper().run()
