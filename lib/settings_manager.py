import json
import os
from lib.constants import APP_SUPPORT_DIR


class SettingsManager:
    """Manages application settings persistence."""
    
    def __init__(self):
        self.settings_file = os.path.join(APP_SUPPORT_DIR, "settings.json")
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """Load settings from file or return defaults."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Error loading settings from {self.settings_file}, using defaults")
                return self._get_defaults()
        return self._get_defaults()
    
    def _get_defaults(self):
        """Return default settings."""
        return {
            "selected_background": None
        }
    
    def save(self):
        """Save current settings to file."""
        try:
            os.makedirs(APP_SUPPORT_DIR, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save."""
        self.settings[key] = value
        self.save()
    
    def get_selected_background(self):
        """Get the selected background wallpaper name."""
        return self.settings.get("selected_background")
    
    def set_selected_background(self, wallpaper_name):
        """Set the selected background wallpaper name."""
        self.set("selected_background", wallpaper_name)
