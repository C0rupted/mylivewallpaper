# Building from Source

Complete guide to building MyLiveWallpaper from source code and creating a standalone macOS application bundle.

## Development Setup

### Prerequisites

- macOS 10.13 or later
- Python 3.7 or later
- Xcode Command Line Tools (for compiler)
- Git

### Install Development Tools

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Verify Python installation
python3 --version

# Verify git installation
git --version
```

## Clone and Setup

### 1. Clone Repository

```bash
git clone https://github.com/C0rupted/mylivewallpaper.git
cd mylivewallpaper
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** - Web framework for backend
- **moviepy** - Video processing for thumbnails
- **Pillow** - Image processing
- **rumps** - Menu bar application framework
- **PyObjC** - macOS Cocoa bindings
- **Nuitka** - Python-to-C compiler for building

## Running Development Version

```bash
# With virtual environment activated:
python3 main.py
```

The application will:
1. Start Flask server on `http://localhost:8000`
2. Create the wallpaper daemon window
3. Appear as an icon in the menu bar
4. Load example widgets and wallpapers

### Testing Widgets

During development, test your widgets by:
1. Placing widget folder in `examples/widgets/`
2. Restarting the application
3. Opening Widget Center from menu bar
4. Enabling your widget to see it on desktop

## Building Standalone Application

### Using Makefile

```bash
# Ensure virtual environment is active
source venv/bin/activate

# Run build
make build
```

The Makefile uses Nuitka to compile Python to C and create a macOS app bundle.

### Manual Build Command

If you prefer to build without the Makefile:

```bash
nuitka \
  --standalone \
  --macos-create-app-bundle \
  --macos-app-name="MyLiveWallpaper" \
  --macos-signed-app-name="com.c0rupted.mylivewallpaper" \
  --macos-app-icon=MyLiveWallpaper.icns \
  --macos-app-version="1.0" \
  --macos-app-mode=ui-element \
  --include-data-dir=web=web \
  --include-data-dir=examples=examples \
  --follow-imports \
  --output-filename=MyLiveWallpaper \
  main.py
```

### Build Parameters Explained

| Parameter | Purpose |
|-----------|---------|
| `--standalone` | Create self-contained app without external dependencies |
| `--macos-create-app-bundle` | Generate `.app` bundle format |
| `--macos-app-name` | Display name in Finder |
| `--macos-signed-app-name` | Bundle identifier (reverse domain notation) |
| `--macos-app-icon` | Icon file for application |
| `--macos-app-version` | Version number |
| `--macos-app-mode=ui-element` | Menu bar app mode |
| `--include-data-dir=web=web` | Include web directory in bundle |
| `--include-data-dir=examples=examples` | Include examples directory |
| `--follow-imports` | Recursively include all imports |

## Build Output

Successful build creates:

```
MyLiveWallpaper.app/
├── Contents/
│   ├── MacOS/
│   │   └── MyLiveWallpaper      # Executable
│   ├── Resources/
│   │   ├── web/                 # Frontend files
│   │   ├── examples/            # Example widgets
│   │   └── MyLiveWallpaper.icns # Icon
│   └── Info.plist              # Bundle metadata
```

## Troubleshooting Build Issues

### Nuitka Not Found

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall Nuitka
pip install --upgrade nuitka
```

### Missing Icon File

Ensure `MyLiveWallpaper.icns` exists in the project root:
- If missing, either provide your own icon or modify build command to remove `--macos-app-icon` parameter
- Use a tool like Image2Icon to convert PNG to ICNS format

### Build Takes Too Long

This is normal for the first build. Nuitka is compiling all Python code to C:
- First build: 5-15 minutes depending on machine
- Subsequent builds are faster

### "Icon doesn't exist" Error

Create a placeholder icon or convert existing:

```bash
# Using ImageMagick (if installed)
convert -size 512x512 xc:white -draw "circle 256,256 0,0" icon.png
iconutil -c icns -o MyLiveWallpaper.icns icon.png

# Or download from an icon source
# Then point build command to it
```

### Code Signature Issues

For local development, you can skip code signing:

```bash
# Add to build command
--macos-app-unsigned
```

## Development Workflow

### Making Changes

1. Edit code while running development version
2. Restart application to test changes
3. Check for errors in terminal output

### Testing Widgets

1. Create widget in `examples/widgets/MyWidget/`
2. Restart application
3. Widget appears in Widget Center
4. Enable and position in Widget Center

### Debugging

```bash
# Run with verbose output
python3 main.py

# Check Flask server logs in terminal
# JavaScript console logs appear in terminal

# For macOS-specific issues
# Check system logs: log show --info --debug
```


---

See [Architecture Overview](./ARCHITECTURE.md) for understanding the codebase structure.
