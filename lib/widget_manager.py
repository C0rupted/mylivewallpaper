"""
Widget manager: handles widget discovery, configuration, and isolation.
Each widget is a folder inside web/widgets/ with widget.html, widget.css, widget.js
"""

import json
import os
from lib.constants import APP_SUPPORT_DIR, WIDGETS_DIR, WIDGETS_CONFIG_FILE, DEFAULT_WIDGET_CONFIG


def load_widget_config():
    """Load widget configuration from disk."""
    if not os.path.exists(WIDGETS_CONFIG_FILE):
        save_widget_config(DEFAULT_WIDGET_CONFIG)
        return DEFAULT_WIDGET_CONFIG
    try:
        with open(WIDGETS_CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        save_widget_config(DEFAULT_WIDGET_CONFIG)
        return DEFAULT_WIDGET_CONFIG


def save_widget_config(config):
    """Save widget configuration to disk."""
    os.makedirs(APP_SUPPORT_DIR, exist_ok=True)
    with open(WIDGETS_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    return config


def discover_widgets():
    """
    Discover available widgets by looking for widget folders.
    Returns a dict mapping widget_id -> widget_metadata
    """
    widgets = {}
    # widgets are stored in WIDGETS_DIR (App Support). If missing, return empty dict
    if not os.path.isdir(WIDGETS_DIR):
        return widgets
    
    for folder in os.listdir(WIDGETS_DIR):
        widget_path = os.path.join(WIDGETS_DIR, folder)
        if not os.path.isdir(widget_path):
            continue
        
        # Check for required files
        html_file = os.path.join(widget_path, "widget.html")
        css_file = os.path.join(widget_path, "widget.css")
        js_file = os.path.join(widget_path, "widget.js")
        
        if os.path.exists(html_file):
            # Load aspect ratio and other metadata from widget.html comment
            metadata = {
                "id": folder,
                "path": widget_path,
                "html": html_file,
                "css": css_file if os.path.exists(css_file) else None,
                "js": js_file if os.path.exists(js_file) else None,
                "aspect_ratio": 2.0,  # default 2:1, can be overridden per widget
            }
            
            # Try to read aspect ratio from widget.html
            try:
                with open(html_file, "r") as f:
                    content = f.read()
                    # Look for <!-- aspect-ratio: X:X --> or <!-- aspect-ratio: flex --> comment
                    import re
                    match = re.search(r'<!--\s*aspect-ratio:\s*([\w:]+)\s*-->', content)
                    if match:
                        ratio_str = match.group(1)
                        if ratio_str == "flex":
                            metadata["aspect_ratio"] = "flex"
                        else:
                            # Parse "W:H" format to numeric ratio (W / H)
                            parts = ratio_str.split(":")
                            if len(parts) == 2:
                                try:
                                    w, h = float(parts[0]), float(parts[1])
                                    metadata["aspect_ratio"] = w / h if h != 0 else 1.0
                                except ValueError:
                                    metadata["aspect_ratio"] = 1.0
            except Exception:
                pass
            
            widgets[folder] = metadata
    
    return widgets


def get_widget_config():
    """Get current widget configuration with available widgets."""
    config = load_widget_config()
    available = discover_widgets()
    
    # Filter config to only include available widgets
    valid_config = [w for w in config if w["id"] in available]
    
    # Enhance config with widget metadata
    result = []
    for w in valid_config:
        widget_meta = available[w["id"]]
        w["aspect_ratio"] = widget_meta.get("aspect_ratio", 2.0)
        # Calculate width from height and aspect ratio (unless it's "flex" or width is already set)
        if w["aspect_ratio"] != "flex" and "width" not in w:
            w["width"] = int(w["height"] * w["aspect_ratio"])
        result.append(w)
    
    return result
