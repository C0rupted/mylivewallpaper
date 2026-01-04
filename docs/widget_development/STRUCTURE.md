# Widget File Structure

Detailed explanation of each file in a widget and its role.

## Directory Layout

```
~/Library/Application Support/MyLiveWallpaper/widgets/mywidget/
├── widget.html    # DOM structure and metadata
├── widget.css     # Styling and layout
└── widget.js      # Interactivity and updates
```

## widget.html

The HTML file defines the widget's DOM structure and declares metadata.

### Basic Structure

```html
<!-- aspect-ratio: 2:1 -->
<div class="my-widget">
  <div class="widget-header">
    <h1>Widget Title</h1>
  </div>
  <div class="widget-content">
    <p>Content goes here</p>
  </div>
</div>
```

### Metadata Comment

**Required**: The first comment must declare the aspect ratio:

```html
<!-- aspect-ratio: WIDTH:HEIGHT -->
```

**Valid format examples:**

| Format | Result | Use Case |
|--------|--------|----------|
| `2:1` | Width is 2x height | Wide widgets (clocks, calendars) |
| `1:1` | Square | Balanced widgets |
| `16:9` | Widescreen | Media-heavy widgets |
| `flex` | User-defined | Flexible widgets |

**Examples:**

```html
<!-- aspect-ratio: 2:1 -->  <!-- Clock: 200px wide, 100px tall -->
<!-- aspect-ratio: 1:1 -->  <!-- Square widget -->
<!-- aspect-ratio: 4:3 -->  <!-- Landscape -->
<!-- aspect-ratio: flex --> <!-- User adjusts both width and height -->
```

### Element Requirements

1. **Root Container**: Use a div with a class name for styling:
   ```html
   <div class="my-widget">
     <!-- widget content -->
   </div>
   ```

2. **Unique IDs**: Use IDs for elements you'll update with JavaScript:
   ```html
   <div id="current-time">00:00:00</div>
   <div id="date">Loading...</div>
   ```

3. **Semantic HTML**: Use semantic elements when appropriate:
   ```html
   <header>Widget Title</header>
   <main>Main content</main>
   <footer>Footer info</footer>
   ```

### Full Example

```html
<!-- aspect-ratio: 2:1 -->
<div class="status-widget">
  <div class="status-header">
    <h2>System Status</h2>
  </div>
  
  <div class="status-content">
    <div class="status-item">
      <span class="label">CPU</span>
      <span class="value" id="cpu-value">--</span>
    </div>
    <div class="status-item">
      <span class="label">Memory</span>
      <span class="value" id="mem-value">--</span>
    </div>
    <div class="status-item">
      <span class="label">Battery</span>
      <span class="value" id="bat-value">--</span>
    </div>
  </div>
</div>
```

## widget.css

The CSS file defines all styling and layout for the widget.

### Style Isolation

CSS is automatically scoped to the widget's iframe, so:
- No style conflicts with other widgets
- No need for namespacing or BEM conventions (though good practice)
- Global styles from web server don't apply

### Container-Relative Units

Use `cqw` (container query width) units for responsive sizing:

```css
.widget-title {
  font-size: 4cqw;  /* 4% of widget width */
  padding: 2cqw;    /* 2% of widget width */
}
```

**Unit Reference:**

| Unit | Meaning |
|------|---------|
| `cqw` | 1% of widget width |
| `cqh` | 1% of widget height |
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `px` | Fixed pixels (use sparingly) |
| `em` | Relative to font size |
| `%` | Relative to parent |

### Recommended Base Styles

```css
.my-widget {
  /* Full size - required */
  width: 100%;
  height: 100%;
  
  /* Layout */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
  /* Appearance */
  background: rgba(26, 26, 26, 0.8);
  border-radius: 12px;
  padding: 5cqw;
  gap: 3cqw;
  
  /* Typography */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
  color: white;
  
  /* Styling */
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  
  /* Ensure content is visible */
  overflow: hidden;
}
```

### Responsive Container Queries

Use container queries to adjust styling based on widget size:

```css
@container (max-width: 150px) {
  .title {
    font-size: 3cqw;
  }
  .content {
    font-size: 2cqw;
  }
}

@container (min-width: 150px) {
  .title {
    font-size: 5cqw;
  }
  .content {
    font-size: 3cqw;
  }
}
```

### Full Example

```css
/* Status Widget CSS */
.status-widget {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, rgba(15, 20, 25, 0.7), rgba(25, 30, 40, 0.8));
  border-radius: 12px;
  padding: 5cqw;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  gap: 3cqw;
}

.status-header {
  text-align: center;
}

.status-header h2 {
  margin: 0;
  font-size: 4cqw;
  font-weight: 600;
  color: #00ffd1;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 1.5cqw;
  flex: 1;
  justify-content: space-around;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2cqw;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.label {
  font-size: 2.5cqw;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.value {
  font-size: 3cqw;
  color: #00ffd1;
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
}

/* Responsive adjustments */
@container (max-width: 200px) {
  .status-header h2 {
    font-size: 3cqw;
  }
  .label {
    font-size: 1.8cqw;
  }
  .value {
    font-size: 2.2cqw;
  }
}
```

## widget.js

The JavaScript file handles interactivity, updates, and real-time content.

### Initialization Pattern

```javascript
// Wrap in IIFE to avoid global scope pollution
(function() {
  // Get DOM references
  const titleEl = document.getElementById('title');
  const contentEl = document.getElementById('content');
  
  // Define update function
  function update() {
    // Update DOM elements
    contentEl.textContent = new Date().toLocaleTimeString();
  }
  
  // Initial update
  update();
  
  // Schedule updates
  setInterval(update, 1000);
})();
```

**Why IIFE (Immediately Invoked Function Expression)?**
- Avoids polluting global scope
- Variables don't interfere with other widgets
- Cleaner, more modular code

### Common Patterns

#### 1. Real-time Updates

```javascript
(function() {
  const timeEl = document.getElementById('time');
  
  function updateTime() {
    const now = new Date();
    timeEl.textContent = now.toLocaleTimeString();
  }
  
  updateTime();
  setInterval(updateTime, 1000);
})();
```

#### 2. Event Listeners

```javascript
(function() {
  const button = document.getElementById('my-button');
  
  button.addEventListener('click', function() {
    // Handle click
    document.getElementById('message').textContent = 'Clicked!';
  });
  
  // Cleanup if widget is removed
  window.addEventListener('beforeunload', function() {
    button.removeEventListener('click', null);
  });
})();
```

#### 3. Fetching External Data

```javascript
(function() {
  const contentEl = document.getElementById('content');
  
  async function fetchData() {
    try {
      const response = await fetch('https://api.example.com/data');
      const data = await response.json();
      contentEl.textContent = data.value;
    } catch (error) {
      console.error('Failed to fetch data:', error);
      contentEl.textContent = 'Error loading data';
    }
  }
  
  fetchData();
  setInterval(fetchData, 60000); // Update every minute
})();
```

#### 4. DOM Content Ready

```javascript
(function() {
  // Wait for DOM to be ready before accessing elements
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  function init() {
    // Safe to access DOM elements now
    document.getElementById('content').textContent = 'Ready!';
  }
})();
```

### Full Example

```javascript
// Clock Widget JavaScript
(function() {
  const hhmmEl = document.getElementById('clock-hhmm');
  const secsEl = document.getElementById('clock-secs');
  const dateEl = document.getElementById('clock-date');
  
  if (!hhmmEl || !dateEl) return; // Safety check
  
  function update() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    
    hhmmEl.textContent = `${hours}:${mins}`;
    secsEl.textContent = `:${secs}`;
    
    const dateStr = now.toLocaleDateString(undefined, {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
    dateEl.textContent = dateStr;
  }
  
  // Initial update
  update();
  
  // Update every second
  setInterval(update, 1000);
})();
```

### Error Handling

```javascript
(function() {
  try {
    const el = document.getElementById('content');
    if (!el) {
      console.warn('Content element not found');
      return;
    }
    
    el.textContent = 'Loaded successfully';
  } catch (error) {
    console.error('Widget error:', error);
  }
})();
```

## Naming Conventions

Use clear, descriptive names:

**Good:**
```html
<div id="clock-display"></div>
<span class="status-label">CPU</span>
```

**Avoid:**
```html
<div id="d1"></div>          <!-- Too vague -->
<span class="sl">CPU</span>  <!-- Non-obvious abbreviation -->
```

## Loading Lifecycle

Understand when each file is processed:

1. **HTML Load** → Browser parses structure, creates DOM
2. **CSS Load** → Browser applies styles
3. **JS Load** → Browser executes JavaScript
4. **DOMContentLoaded** → JavaScript can access DOM safely
5. **Ready** → Widget is fully initialized and visible

---

Next: See [Styling Guide](./STYLING.md) for advanced CSS techniques.
