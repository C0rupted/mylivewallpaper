# Widget Best Practices

Guidelines and patterns for creating high-quality, maintainable widgets.

## Performance Optimization

### 1. Minimize Reflows and Repaints

**Bad:**
```javascript
// Updates DOM in a loop - causes reflow for each update
for (let i = 0; i < 1000; i++) {
  document.getElementById('item-' + i).style.color = 'red';
}
```

**Good:**
```javascript
// Update styles in one operation
const items = document.querySelectorAll('[id^="item-"]');
items.forEach(item => {
  item.style.color = 'red';
});

// Or use CSS class
document.getElementById('container').classList.add('active');
```

### 2. Use Efficient Update Frequencies

**Bad:**
```javascript
// Updates every frame - excessive for most use cases
setInterval(update, 16); // 60 FPS
```

**Good:**
```javascript
// Update at appropriate intervals
setInterval(update, 1000);  // For time display
setInterval(update, 60000); // For weather (every minute)
setInterval(update, 5000);  // For live updates
```

### 3. Cancel Unused Intervals

**Bad:**
```javascript
setInterval(update, 1000);
// Widget may be removed but interval keeps running
```

**Good:**
```javascript
const intervalId = setInterval(update, 1000);

// Store reference to cleanup later
window.addEventListener('beforeunload', () => {
  clearInterval(intervalId);
});
```

### 4. Avoid Memory Leaks

**Bad:**
```javascript
// Creates new listeners every update
function update() {
  const btn = document.getElementById('button');
  btn.addEventListener('click', handleClick); // Adds listener each time!
}
setInterval(update, 1000);
```

**Good:**
```javascript
(function() {
  const btn = document.getElementById('button');
  btn.addEventListener('click', handleClick);
  
  function update() {
    // Just update content
  }
  setInterval(update, 1000);
})();
```

## Code Quality

### 1. Use Descriptive Names

```javascript
// Bad
const d = new Date();
const v = d.getHours();

// Good
const now = new Date();
const hours = now.getHours();
```

### 2. Add Comments for Complex Logic

```javascript
// Calculate and display sunrise time based on latitude
function calculateSunrise(lat, lng) {
  // Julian date for the given location
  const J2000 = (jd - 2451545) / 36525;
  // ... complex calculations
}
```

### 3. Validate Input Data

```javascript
// Fetch data from API
fetch(url)
  .then(res => res.json())
  .then(data => {
    // Validate before using
    if (data && data.value !== undefined) {
      updateDisplay(data.value);
    } else {
      console.warn('Invalid data format');
    }
  });
```

### 4. Handle Errors Gracefully

```javascript
try {
  const data = JSON.parse(apiResponse);
  updateWidget(data);
} catch (error) {
  console.error('Failed to parse data:', error);
  displayErrorMessage('Unable to load data');
}
```

## Responsive Design

### 1. Use Container Queries

```css
/* Adapt to widget size */
@container (max-width: 150px) {
  .title { font-size: 3cqw; }
}

@container (min-width: 300px) {
  .title { font-size: 5cqw; }
}
```

### 2. Flexible Layouts

```css
/* Bad - fixed sizes */
.widget-content {
  width: 300px;
  height: 200px;
}

/* Good - flexible */
.widget-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
```

### 3. Scalable Text

```css
/* Bad - doesn't scale */
.text {
  font-size: 16px;
}

/* Good - scales with widget */
.text {
  font-size: 3cqw; /* 3% of container width */
}
```

## Accessibility

### 1. Semantic HTML

```html
<!-- Bad -->
<div class="button" onclick="doSomething()">Click me</div>

<!-- Good -->
<button onclick="doSomething()">Click me</button>
```

### 2. ARIA Labels

```html
<!-- Add labels for screen readers -->
<button aria-label="Refresh widget">🔄</button>

<div id="status" aria-live="polite" aria-atomic="true">
  Loading...
</div>
```

### 3. Color Contrast

```css
/* Ensure readable contrast */
.text {
  color: #ffffff;           /* White text */
  background: #000000;      /* Black background */
  /* Good contrast ratio */
}

/* Support dark/light mode */
@media (prefers-color-scheme: dark) {
  .widget { background: #1a1a1a; color: #ffffff; }
}

@media (prefers-color-scheme: light) {
  .widget { background: #ffffff; color: #000000; }
}
```

## Security

### 1. Sanitize User Input

```javascript
// Bad - allows XSS
document.getElementById('content').innerHTML = userInput;

// Good - safe
document.getElementById('content').textContent = userInput;
```

### 2. Validate API Responses

```javascript
// Always validate data from external sources
fetch(apiUrl)
  .then(res => res.json())
  .then(data => {
    // Check expected structure
    if (typeof data.value !== 'number') {
      throw new Error('Invalid data format');
    }
  });
```

### 3. Use HTTPS for APIs

```javascript
// Bad - insecure
fetch('http://api.example.com/data')

// Good - encrypted
fetch('https://api.example.com/data')
```

## Styling Best Practices

### 1. Consistent Spacing

```css
.widget {
  --spacing-xs: 1cqw;
  --spacing-sm: 2cqw;
  --spacing-md: 3cqw;
  --spacing-lg: 5cqw;
  
  padding: var(--spacing-md);
  gap: var(--spacing-md);
}
```

### 2. Consistent Colors

```css
.widget {
  --primary: #00ffd1;
  --background: rgba(26, 26, 26, 0.8);
  --border: rgba(255, 255, 255, 0.08);
  
  background: var(--background);
  color: var(--primary);
  border: 1px solid var(--border);
}
```

### 3. Animations for Polish

```css
/* Smooth transitions */
.value {
  transition: color 0.3s ease;
}

.value:hover {
  color: #00ffaa;
}

/* Subtle animations */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.loading {
  animation: pulse 1.5s infinite;
}
```

## Documentation

### 1. README in Widget Folder

```markdown
# My Widget

Brief description of what the widget does.

## Features
- Real-time updates
- Responsive design
- Dark mode support

## Configuration
- Update interval: 1 second
- Aspect ratio: 2:1

## Dependencies
None - pure JavaScript/CSS

## Author
Your Name (your@email.com)
```

### 2. Code Comments

```javascript
// Widget initialization
(function() {
  // Fetch DOM references
  const display = document.getElementById('display');
  
  // Update display with current time
  function update() {
    const now = new Date();
    display.textContent = now.toLocaleTimeString();
  }
  
  // Initial update
  update();
  
  // Update every second
  setInterval(update, 1000);
})();
```

## Testing

### 1. Test Different Sizes

Test your widget at various sizes in Widget Center:
- Small (100px width)
- Medium (200px width)
- Large (400px width)

### 2. Test Different Content

- Empty/no data
- Long text
- Large numbers
- Multiple items

### 3. Test Error Conditions

- Network timeout
- Invalid API response
- Missing elements
- Rapid updates

## Common Mistakes to Avoid

| Mistake | Impact | Solution |
|---------|--------|----------|
| Global variables | Conflicts with other widgets | Use IIFE scope |
| Hardcoded sizes | Breaks in different sizes | Use responsive units (cqw) |
| Memory leaks | Widget slows down desktop | Clean up intervals/listeners |
| No error handling | Widget breaks silently | Add try/catch and fallbacks |
| Too frequent updates | High CPU usage | Use appropriate intervals |
| Ignoring dark mode | Unreadable in dark wallpapers | Support both color schemes |
| Blocking operations | Freezes widget updates | Use async for long operations |
| CSS conflicts | Widget styling breaks | Scope styles to widget class |

## Performance Checklist

- [ ] Updates run at appropriate intervals (not too frequent)
- [ ] Intervals are cleaned up when not needed
- [ ] No DOM elements created/destroyed in loops
- [ ] No memory leaks (listeners removed on cleanup)
- [ ] Responsive units used (cqw, not px)
- [ ] Errors handled gracefully
- [ ] External APIs use timeout/error handling
- [ ] CSS is performant (no expensive selectors)
- [ ] Images/media are optimized
- [ ] JavaScript is minified for production

## Quality Checklist

- [ ] Code is readable and well-commented
- [ ] Descriptive variable/function names used
- [ ] HTML is semantic and valid
- [ ] CSS is organized and maintainable
- [ ] JavaScript follows IIFE pattern
- [ ] No console errors or warnings
- [ ] Works in dark and light modes
- [ ] Responsive at various sizes
- [ ] README included with description
- [ ] No unused code or imports

---

Next: See [Styling Guide](./STYLING.md) for CSS techniques and patterns.
