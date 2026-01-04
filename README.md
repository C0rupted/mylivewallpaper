<a id="readme-top"></a>

<div align="center">
  <h1>MyLiveWallpaper</h1>

  <p align="center">
    A macOS application for creating live, interactive desktop wallpapers with customizable widgets.
    <br />
    <br />
    <a href="#features"><strong>View Features »</strong></a>
    &middot;
    <a href="#getting-started">Getting Started</a>
    &middot;
    <a href="#usage">Usage</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

**MyLiveWallpaper** is a macOS application that transforms your desktop background into an interactive, dynamic wallpaper with customizable widgets. Unlike static wallpapers, MyLiveWallpaper displays live content such as time, date, weather, system status, or custom widgets directly on your desktop.

The application runs as a menu bar app and provides a modern web-based interface for managing wallpapers and widgets through a Flask backend and HTML/CSS/JavaScript frontend.

<p align="right">(<a href="#readme-top">⬆</a>)</p>

## Features

- **Live Desktop Widgets** - Display interactive widgets directly on your desktop
- **Widget Center** - Manage and customize widgets with an intuitive interface
- **Wallpaper Library** - Browse and select from custom wallpapers
- **Auto-Refresh** - Automatically reapply wallpaper when switching spaces or waking from sleep
- **Web-Based UI** - Modern, responsive interface built with HTML/CSS/JavaScript
- **Extensible** - Easy to add custom widgets
- **Menu Bar Control** - Quick access to features from the macOS menu bar

<p align="right">(<a href="#readme-top">⬆</a>)</p>

### Built With

[![Python][Python.org]][Python-url]
[![Flask][Flask.com]][Flask-url]
[![Cocoa][Cocoa.org]][Cocoa-url]
[![CSS][CSS.org]][CSS-url]
[![JavaScript][JavaScript.com]][JavaScript-url]
[![HTML5][HTML5.org]][HTML5-url]

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

For running the pre-built application:
* **macOS 10.13+** - This application requires modern macOS frameworks

For building from source:
* **Python 3.7+** - Download from [python.org](https://www.python.org/downloads/)
* **pip** - Python package manager (comes with Python)

### Installation

#### Option 1: Download Pre-Built Application (Recommended)

1. **Download the latest release**
   - Visit the [Releases page](https://github.com/C0rupted/mylivewallpaper/releases)
   - Download the latest `.app` file
   - Move it to your Applications folder

2. **Launch MyLiveWallpaper**
   - Open Applications folder or use Spotlight search
   - Double-click MyLiveWallpaper.app
   - The app will appear in your macOS menu bar

#### Option 2: Build from Source

For developers who want to modify or contribute to the project:

1. **Clone the repository**
   ```sh
   git clone https://github.com/C0rupted/mylivewallpaper.git
   cd mylivewallpaper
   ```

2. **Create a virtual environment (recommended)**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```sh
   python3 main.py
   ```

The application will start and appear in your macOS menu bar. You'll see a menu bar icon where you can access the Wallpaper Library and Widget Center.

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Basic Usage

1. **Launch the Application**
   - Open your Applications folder
   - Double-click MyLiveWallpaper.app
   - The app will appear as an icon in your macOS menu bar

2. **Access Features from Menu Bar**
   - Click the menu bar icon to see available options:
     - **Refresh Wallpaper** - Force refresh the current wallpaper
     - **Open Wallpaper Library** - Browse and select wallpapers
     - **Widget Center** - Manage and customize widgets
     - **Quit** - Exit the application

3. **Wallpaper Library**
   - Select from available wallpapers
   - The wallpaper will automatically apply to your desktop
   - The system will reapply it automatically when switching spaces or waking from sleep

4. **Widget Center**
   - View available widgets (Clock, Quote, Status, Sample, and custom widgets)
   - Customize widget settings
   - Widgets display in real-time on your desktop

### Architecture

The application consists of several key components:

- **main.py** - Entry point; creates the menu bar app and initializes all systems
- **wallpaper_daemon.py** - Manages the borderless window that displays widgets on the desktop
- **web_server.py** - Flask server providing the web interface
- **lib/system_wallpaper.py** - Handles macOS wallpaper system integration
- **lib/widget_manager.py** - Manages widget lifecycle and rendering
- **lib/web_window.py** - Creates and manages web-based windows for UI
- **web/** - Frontend files (HTML, CSS, JavaScript)
  - **wallpaper_selector/** - Wallpaper selection interface
  - **widget_center/** - Widget management interface

<p align="right">(<a href="#readme-top">⬆</a>)</p>



## Roadmap and Planned Features

- [ ] More built-in widgets (Weather, Calendar, News)
- [ ] Settings menu for app preferences and customization
- [ ] Add support for widgets to use scripts to access system info (securely)
- [ ] Custom theme system for app menus and accessible by widgets
- [ ] Improve overall performance and resource usage
- [ ] First-run wizard to guide new users through setup
- [ ] Improve documentation
- [ ] Better logging, error handling and developer tools

See [open issues](https://github.com/C0rupted/mylivewallpaper/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">⬆</a>)</p>



## Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed: `python3 --version`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that port 8000 is available (Flask server binds to this port)

### Wallpaper not applying
- Grant the application necessary permissions in macOS System Preferences
- Ensure you've selected a wallpaper from the Wallpaper Library
- Try clicking "Refresh Wallpaper" from the menu bar

### Widgets not displaying
- Verify the Flask server is running (check terminal output)
- Ensure your widget files are in the correct `examples/widgets/` directory
- Check browser console for JavaScript errors in the web interface

### Performance issues
- Close other resource-intensive applications
- Reduce the number of active widgets
- Ensure macOS is up to date

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- CONTACT -->
## Contact

For questions, feature requests, or bug reports, please open an issue on the GitHub repository.

Project Link: [https://github.com/C0rupted/mylivewallpaper](https://github.com/C0rupted/mylivewallpaper)

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This project uses the following open source libraries and frameworks:

* [Flask](https://flask.palletsprojects.com/) - Lightweight Python web framework
* [PyObjC](https://pyobjc.readthedocs.io/) - Python bindings for Cocoa
* [rumps](https://github.com/jaredks/rumps) - Menu bar app framework for macOS
* [moviepy](https://zulko.github.io/moviepy/) - Video and image processing
* [Pillow (PIL)](https://python-pillow.org/) - Image processing library
* [Nuitka](https://nuitka.net/) - Python compiler for building standalone .app bundle

<p align="right">(<a href="#readme-top">⬆</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[Python.org]: https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python
[Python-url]: https://www.python.org/
[Flask.com]: https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask
[Flask-url]: https://flask.palletsprojects.com/
[Cocoa.org]: https://img.shields.io/badge/Cocoa-macOS-gray?style=flat-square&logo=apple
[Cocoa-url]: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/OSX_Technology_Overview/CocoaApplicationLayer/CocoaApplicationLayer.html
[CSS.org]: https://img.shields.io/badge/CSS-Styling-blue?style=flat-square&logo=css3
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[JavaScript.com]: https://img.shields.io/badge/JavaScript-Scripting-yellow?style=flat-square&logo=javascript
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[HTML5.org]: https://img.shields.io/badge/HTML5-Frontend-red?style=flat-square&logo=html5
[HTML5-url]: https://html.spec.whatwg.org/
