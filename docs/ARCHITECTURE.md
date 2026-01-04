# Architecture Overview

MyLiveWallpaper is built with a layered architecture combining native macOS components with a web-based frontend.

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              Main Application (rumps Menu Bar App)           │
│               Manages: Daemon, Server, Observer              │
└──────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────────┐  ┌────▼──────────┐  ┌──▼────────────┐
│ Wallpaper Daemon │  │ Flask Server  │  │ SpaceObserver │
│                  │  │               │  │               │
│ - WebKit Window  │  │ - REST API    │  │ - Monitors    │
│ - Desktop Level  │  │ - Wallpaper   │  │   space       │
│ - Widget Display │  │   selector UI │  │   changes     │
│                  │  │ - Widget      │  │ - Wake events │
│                  │  │   center UI   │  │ - Auto-reapply│
└─────────┬────────┘  └────┬──────────┘  └───────────────┘
          │                │
          └────────┬───────┘
                   │
            ┌──────▼──────────┐
            │ Widget System   │
            │                 │
            │ Runs in Daemon  │
            │ Controlled by   │
            │ Flask Server    │
            │                 │
            │ - Real-time     │
            │   updates       │
            │ - Event         │
            │   handling      │
            │ - Widget frames │
            └─────────────────┘
```

## Core Components

### 1. **Main Application (main.py)**
The entry point that initializes and manages all systems:
- Starts Flask web server in background thread
- Creates WallpaperDaemon for desktop rendering
- Initializes SpaceObserver for macOS events
- Manages menu bar interface with rumps
- Orchestrates communication between components

### 2. **Wallpaper Daemon (wallpaper_daemon.py)**
Manages the desktop-level window for displaying widgets:
- Creates a borderless, transparent WebKit window
- Positions window at desktop level (behind all other windows)
- Loads widgets from Flask server
- Receives updates from Flask server when configuration changes

### 3. **Flask Web Server (web_server.py)**
Web-based backend controlling the widget system:
- Serves HTML/CSS/JavaScript frontend
- Provides REST API endpoints for widget and wallpaper management
- Controls the Wallpaper Daemon (refreshes on config updates)
- Handles wallpaper thumbnail generation
- Returns isolated widget frames via iframes
- Manages the Widget System running in the Daemon

### 4. **Widget Manager (lib/widget_manager.py)**
Handles widget discovery and configuration:
- Scans `~/Library/Application Support/MyLiveWallpaper/widgets/` for widget folders
- Reads widget metadata from HTML comments (aspect ratios, etc.)
- Manages widget configuration (positions, enabled status, dimensions)
- Persists configuration to JSON file

### 5. **Space Observer (lib/system_wallpaper.py)**
Monitors macOS system events independently:
- `SpaceObserver` - Monitors workspace changes and wake events
- Listens for space changes across multiple monitors
- Detects system wake from sleep
- Automatically reapplies wallpaper to maintain visibility
- Operates independently from other components

### 6. **Web Window Manager (lib/web_window.py)**
Creates and manages auxiliary web windows:
- Wallpaper Library window (for selecting wallpapers)
- Widget Center window (for configuring widgets)
- Reuses hidden windows when possible for efficiency

### 7. **Settings Manager (lib/settings_manager.py)**
Handles persistent settings storage:
- Loads settings from `~/Library/Application Support/MyLiveWallpaper/settings.json`
- Saves selected wallpaper to `selected_background` key
- Provides fallback to first wallpaper if saved selection doesn't exist
- Methods: `get()`, `set()`, `get_selected_background()`, `set_selected_background()`
- Gracefully handles missing or corrupted JSON files

## Data Flow

### Application Startup
1. `main.py` launches → rumps menu bar app
2. SettingsManager initializes and loads `settings.json`
3. Flask server starts in background thread
4. SpaceObserver registers for macOS notifications
5. WallpaperDaemon creates borderless window
6. `initialize_wallpaper()` restores saved wallpaper or uses first available
7. WebKit view loads `http://localhost:8000/` with current wallpaper

### Widget Loading
1. User opens Widget Center
2. Flask `/widget_center/` endpoint serves HTML interface
3. JavaScript requests `/api/widgets/config` to get widget configuration
4. User enables/disables widgets and adjusts positions
5. Clicking "Save" POSTs to `/api/widgets/config`
6. Widget manager updates configuration file
7. WallpaperDaemon reloads to apply changes

### Wallpaper Selection
1. User opens Wallpaper Library
2. Flask `/wallpaper_selector/` endpoint serves interface
3. JavaScript fetches `/api/wallpapers` list
4. User clicks wallpaper thumbnail
5. POST to `/api/select_wallpaper` triggers:
   - Saves wallpaper choice to `settings.json` via SettingsManager
   - Generates thumbnail if needed (moviepy + Pillow)
   - Sets macOS desktop background
   - SpaceObserver stores path for auto-reapply
   - WallpaperDaemon reloads widget display

### Space Change / Wake Event
1. SpaceObserver detects system event
2. Calls stored callback function
3. Reapplies current wallpaper via `set_macos_wallpaper()`
4. Ensures widgets stay visible across workspace changes

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.7+ | Core logic, system integration |
| **Framework** | Flask | REST API and web interface |
| **Menu Bar** | rumps | macOS menu bar app |
| **Desktop** | WebKit (WKWebView) | Widget rendering |
| **macOS** | Cocoa, Quartz | Native system integration |
| **Frontend** | HTML5, CSS3, JavaScript | User interfaces |
| **Image Processing** | moviepy, Pillow | Thumbnail generation |

## Directory Structure

```
mylivewallpaper/
├── main.py                 # Application entry point
├── wallpaper_daemon.py     # Desktop window manager
├── web_server.py          # Flask backend
├── lib/
│   ├── constants.py       # Configuration and paths
│   ├── system_wallpaper.py # macOS integration
│   ├── widget_manager.py  # Widget discovery/config
│   ├── web_window.py      # Auxiliary windows
│   └── thumbnails.py      # Image processing
├── web/                   # Frontend files
│   ├── index.html         # Main widget page
│   ├── main.js            # Wallpaper loader
│   ├── widgets.js         # Widget frame loader
│   ├── style.css
│   ├── wallpaper_selector/    # Wallpaper UI
│   └── widget_center/         # Widget config UI
├── examples/
│   ├── widgets/           # Example widget templates
│   └── wallpapers/        # Example wallpaper videos
└── docs/                  # This documentation
```

## Key Design Decisions

### 1. Web-Based UI
Using HTML/CSS/JavaScript allows for rich, responsive interfaces without native development complexity. Flask provides a lightweight web server that's cross-platform compatible.

### 2. Widget Isolation via iframes
Each widget runs in its own iframe to prevent style/script conflicts. This allows widgets to be truly independent and safe.

### 3. Borderless Transparent Window
The wallpaper daemon uses a borderless window positioned at the desktop level, allowing the actual desktop background to show through while widgets overlay on top.

### 4. Configuration Persistence
Widget configurations are stored in JSON, making them easy to backup, transfer, and edit manually if needed.

### 5. Automatic Wallpaper Reapply
SpaceObserver ensures wallpapers persist across workspace changes and wake events, maintaining a consistent experience.

---

See [Widget Development](./widget_development/README.md) for details on creating custom widgets.
