# Widget Development Guide

Everything you need to know about creating custom widgets for MyLiveWallpaper.

## Quick Start

The fastest way to create a widget:

1. Create a folder in `~/Library/Application Support/MyLiveWallpaper/widgets/mywidget/`
2. Add three files: `widget.html`, `widget.css`, `widget.js`
3. Restart MyLiveWallpaper
4. Open Widget Center and enable your widget

## What is a Widget?

A widget is a small, self-contained web application displayed on your desktop. Each widget:
- Runs in its own isolated iframe
- Has a predefined size with configurable position
- Can update in real-time
- Is completely independent of other widgets

## Core Concepts

### Widget Lifecycle

```
1. Discovery   → Widget folder found by widget_manager.py
2. Loading     → Flask endpoint serves widget in iframe
3. Rendering   → Styles applied, JavaScript initializes
4. Updates     → Widget updates content in real-time
5. Positioning → User adjusts size/position in Widget Center
```

### Aspect Ratios

Widgets declare their aspect ratio to maintain proper proportions:

```html
<!-- aspect-ratio: 2:1 -->   (width 2x height)
<!-- aspect-ratio: 1:1 -->   (square)
<!-- aspect-ratio: flex -->  (user-defined)
```

The Widget Center uses this to:
- Calculate initial dimensions
- Maintain proper proportions when resizing
- Preserve user preferences

## Widget File Structure

See [Widget Structure](./STRUCTURE.md) for detailed explanation of each file type.

## Creation Process

### Step 1: Create Widget Folder

```bash
# Navigate to widgets directory
cd ~/Library/Application Support/MyLiveWallpaper/widgets/

# Create widget folder (use lowercase, no spaces)
mkdir mywidget
cd mywidget
```

### Step 2: Create widget.html

```html
<!-- widget.html -->
<!-- aspect-ratio: 2:1 -->
<div class="my-widget">
  <div id="content">Hello, Desktop!</div>
</div>
```

### Step 3: Create widget.css

```css
/* widget.css */
.my-widget {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI';
  color: white;
  padding: 5cqw;
}
```

### Step 4: Create widget.js

```javascript
// widget.js
document.addEventListener('DOMContentLoaded', function() {
  const content = document.getElementById('content');
  content.textContent = new Date().toLocaleTimeString();
  
  // Update every second
  setInterval(function() {
    content.textContent = new Date().toLocaleTimeString();
  }, 1000);
});
```

### Step 5: Test Widget

1. Restart MyLiveWallpaper
2. Open Widget Center (menu bar → Widget Center)
3. Your widget should appear in the "Available Widgets" list
4. Check the checkbox to enable it
5. Adjust position and size as needed
6. Click "Save Changes"

## How Widgets are Loaded

Understanding the loading process helps you create better widgets:

### 1. Discovery Phase
When MyLiveWallpaper starts, `widget_manager.py` scans the widgets directory:

```python
def discover_widgets():
    """Look for folders with widget.html, widget.css, widget.js files"""
    for folder in os.listdir(WIDGETS_DIR):
        if os.path.exists(os.path.join(folder, "widget.html")):
            # Extract aspect ratio from HTML comment
            # <!-- aspect-ratio: 2:1 -->
            metadata = extract_metadata(widget_html)
            widgets[folder_name] = metadata
```

### 2. Configuration Phase
Widget configuration is loaded from `~/Library/Application Support/MyLiveWallpaper/widget_config.json`:

```json
{
  "widgets": [
    {
      "id": "mywidget",
      "enabled": true,
      "x": 100,
      "y": 100,
      "height": 150,
      "width": 300,
      "aspect_ratio": 2.0
    }
  ]
}
```

### 3. Flask Serving
When the wallpaper daemon loads, `web_server.py` serves widgets:

```python
@app.route("/widgets/<widget_id>/frame")
def widget_frame(widget_id):
    """Returns isolated HTML page for widget"""
    # Read widget.html, widget.css, widget.js
    # Combine into single HTML page
    # Return with proper CSS and JS isolation
```

### 4. iframe Loading
The main wallpaper page (`web/index.html`) loads widgets:

```html
<!-- Each enabled widget gets its own iframe -->
<iframe src="http://localhost:8000/widgets/mywidget/frame"></iframe>
```

### 5. Rendering
Browser renders iframe with:
- Widget HTML structure
- Widget CSS styling
- Widget JavaScript logic

## Best Practices

See [Best Practices](./BEST_PRACTICES.md) for detailed guidelines on:
- Code organization
- Performance optimization
- Memory management
- Accessibility
- Error handling

## Styling Guide

See [Styling Guide](./STYLING.md) for information on:
- Container queries (responsive sizing)
- CSS units (cqw, px, etc.)
- Dark mode support
- Backdrop effects
- Animations

## Code Examples

See [Code Examples](./EXAMPLES.md) for complete widget examples:
- Simple text widget
- Real-time clock
- System information display
- Weather widget (API example)
- Animation example

## Common Patterns

### Real-time Updates

```javascript
// Update content every second
setInterval(function() {
  document.getElementById('time').textContent = new Date().toLocaleTimeString();
}, 1000);
```

### Responsive to Container Size

```css
/* Use container queries to respond to widget size */
@container (max-width: 200px) {
  .text { font-size: 2cqw; }
}

@container (min-width: 200px) {
  .text { font-size: 4cqw; }
}
```

### Fetching External Data

```javascript
// Fetch data from API
fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => {
    document.getElementById('content').textContent = data.value;
  });
```

### Dark Mode Support

```css
/* Automatically responds to system appearance */
@media (prefers-color-scheme: dark) {
  .widget {
    background: rgba(0, 0, 0, 0.8);
    color: white;
  }
}

@media (prefers-color-scheme: light) {
  .widget {
    background: rgba(255, 255, 255, 0.9);
    color: black;
  }
}
```

## Debugging Widgets

### Check Console
Open Widget Center in web browser and look at console for errors:
- Right-click widget → Inspect Element
- Check for JavaScript errors

### Verify Files
Ensure all three files exist and have correct names:
```bash
ls ~/Library/Application Support/MyLiveWallpaper/widgets/mywidget/
# Should show: widget.html widget.css widget.js
```

### Test Markup
Validate your HTML structure:
```bash
# Open widget.html in a text editor and check syntax
```

### Check Metadata
Ensure aspect ratio comment is correct:
```html
<!-- aspect-ratio: WIDTH:HEIGHT -->
<!-- Examples: 2:1, 16:9, 1:1 -->
```

## Troubleshooting

### Widget doesn't appear

1. Restart MyLiveWallpaper
2. Verify folder is in correct location: `~/Library/Application Support/MyLiveWallpaper/widgets/mywidget/`
3. Check that `widget.html` exists
4. Open Widget Center - widget should appear in list
5. Enable widget and save

### Widget shows blank

1. Check browser console for JavaScript errors
2. Verify CSS doesn't hide content
3. Check that `widget.html` has visible content
4. Ensure JavaScript initializes correctly

### Widget content not updating

1. Verify `setInterval()` is called
2. Check that DOM selectors match element IDs
3. Look for JavaScript errors in console
4. Ensure `DOMContentLoaded` event listener fires

### Styling doesn't apply

1. Check CSS selectors match HTML elements
2. Verify CSS units are correct (cqw for responsive)
3. Check for CSS typos (spacing, colons, etc.)
4. Ensure `widget.css` is in correct location

## Widget Examples

MyLiveWallpaper includes several example widgets in `examples/widgets/`:

- **clock** - Real-time digital clock
- **quote** - Rotating inspirational quotes
- **status** - System information display
- **sample** - Minimal template

Study these examples to understand patterns and best practices.

---

**Ready to create?** Start with [Widget Structure](./STRUCTURE.md), then reference [Best Practices](./BEST_PRACTICES.md), [Styling Guide](./STYLING.md), and [Code Examples](./EXAMPLES.md) as needed.
