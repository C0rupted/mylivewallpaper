# Widget Code Examples

Complete, working examples of different widget types. Copy these as templates for your own widgets.

## 1. Clock Widget - Real-Time Updates

A simple digital clock that updates every second.

**Folder:** `examples/widgets/clock/`

### widget.html
```html
<!-- aspect-ratio: 2:1 -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Clock Widget</title>
  <link rel="stylesheet" href="widget.css">
</head>
<body>
  <div class="widget">
    <div class="time-display">
      <div class="time" id="time">00:00</div>
      <div class="period" id="period">AM</div>
    </div>
    <div class="date" id="date">Monday, January 1</div>
  </div>
  <script src="widget.js"></script>
</body>
</html>
```

### widget.css
```css
:root {
  --primary: #00ffd1;
  --secondary: #8b9dc3;
  --bg: rgba(26, 26, 26, 0.8);
  --border: rgba(255, 255, 255, 0.08);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: transparent;
}

.widget {
  container-type: inline-size;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 1cqw;
  backdrop-filter: blur(8px);
  padding: 3cqw;
  gap: 2cqw;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.time-display {
  display: flex;
  align-items: baseline;
  gap: 2cqw;
}

.time {
  font-size: 8cqw;
  font-weight: 700;
  color: var(--primary);
  font-family: 'Monaco', monospace;
  letter-spacing: 1px;
}

.period {
  font-size: 3cqw;
  color: var(--secondary);
  font-weight: 600;
}

.date {
  font-size: 2.5cqw;
  color: var(--secondary);
  text-transform: capitalize;
  letter-spacing: 0.5px;
}

@media (prefers-color-scheme: light) {
  :root {
    --primary: #0066ff;
    --secondary: #666666;
    --bg: rgba(255, 255, 255, 0.8);
    --border: rgba(0, 0, 0, 0.1);
  }
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
  }
}
```

### widget.js
```javascript
(function() {
  // DOM elements
  const timeEl = document.getElementById('time');
  const periodEl = document.getElementById('period');
  const dateEl = document.getElementById('date');
  
  // Format time with leading zeros
  function formatTime(num) {
    return String(num).padStart(2, '0');
  }
  
  // Update display
  function updateClock() {
    const now = new Date();
    
    // Get hours, minutes, seconds
    let hours = now.getHours();
    const minutes = now.getMinutes();
    const isPM = hours >= 12;
    
    // Convert to 12-hour format
    if (hours > 12) hours -= 12;
    if (hours === 0) hours = 12;
    
    // Update time display
    timeEl.textContent = formatTime(hours) + ':' + formatTime(minutes);
    periodEl.textContent = isPM ? 'PM' : 'AM';
    
    // Update date display
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    dateEl.textContent = now.toLocaleDateString('en-US', options);
  }
  
  // Initial update
  updateClock();
  
  // Update every second
  setInterval(updateClock, 1000);
})();
```

## 2. System Monitor - Real-Time Stats

Display system CPU, memory, and battery information.

**Note:** This would require backend API support. Here's the widget structure:

### widget.html
```html
<!-- aspect-ratio: 2:1 -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>System Monitor</title>
  <link rel="stylesheet" href="widget.css">
</head>
<body>
  <div class="widget">
    <div class="stat">
      <div class="label">CPU</div>
      <div class="value" id="cpu">--</div>
      <div class="bar">
        <div class="fill" id="cpu-fill" style="width: 0%"></div>
      </div>
    </div>
    <div class="stat">
      <div class="label">Memory</div>
      <div class="value" id="memory">--</div>
      <div class="bar">
        <div class="fill" id="memory-fill" style="width: 0%"></div>
      </div>
    </div>
    <div class="stat">
      <div class="label">Battery</div>
      <div class="value" id="battery">--</div>
      <div class="bar">
        <div class="fill" id="battery-fill" style="width: 0%"></div>
      </div>
    </div>
  </div>
  <script src="widget.js"></script>
</body>
</html>
```

### widget.css
```css
:root {
  --primary: #00d4ff;
  --secondary: #8b9dc3;
  --bg: rgba(26, 26, 26, 0.85);
  --border: rgba(255, 255, 255, 0.08);
  --success: #00ff88;
  --warning: #ffaa00;
  --danger: #ff4444;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: transparent;
}

.widget {
  container-type: inline-size;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 1cqw;
  backdrop-filter: blur(8px);
  padding: 3cqw;
  font-family: 'Segoe UI', sans-serif;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 1cqw;
}

.label {
  font-size: 2cqw;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.value {
  font-size: 5cqw;
  color: var(--primary);
  font-weight: 700;
  font-family: 'Monaco', monospace;
}

.bar {
  width: 100%;
  height: 2cqw;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1cqw;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--success));
  transition: width 0.3s ease;
  border-radius: 1cqw;
}

/* Color fill based on value */
.stat.high .fill {
  background: linear-gradient(90deg, var(--warning), var(--danger));
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: rgba(255, 255, 255, 0.85);
    --border: rgba(0, 0, 0, 0.1);
    --primary: #0066ff;
    --secondary: #666666;
  }
}
```

### widget.js
```javascript
(function() {
  const cpuEl = document.getElementById('cpu');
  const memoryEl = document.getElementById('memory');
  const batteryEl = document.getElementById('battery');
  
  const cpuFill = document.getElementById('cpu-fill');
  const memoryFill = document.getElementById('memory-fill');
  const batteryFill = document.getElementById('battery-fill');
  
  function updateStats() {
    // Simulate random values (in real widget, fetch from API)
    const cpu = Math.floor(Math.random() * 100);
    const memory = Math.floor(Math.random() * 100);
    const battery = Math.floor(Math.random() * 100);
    
    // Update displays
    cpuEl.textContent = cpu + '%';
    memoryEl.textContent = memory + '%';
    batteryEl.textContent = battery + '%';
    
    // Update fills
    cpuFill.style.width = cpu + '%';
    memoryFill.style.width = memory + '%';
    batteryFill.style.width = battery + '%';
  }
  
  updateStats();
  setInterval(updateStats, 2000);
})();
```

## 3. Quote Widget - Display Rotating Quotes

Show random quotes that change daily.

### widget.html
```html
<!-- aspect-ratio: 3:2 -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Quote Widget</title>
  <link rel="stylesheet" href="widget.css">
</head>
<body>
  <div class="widget">
    <div class="quote-container">
      <p class="quote" id="quote">Loading...</p>
      <p class="author" id="author">-- Author</p>
    </div>
    <button class="refresh-btn" id="refresh" aria-label="Next quote">↻</button>
  </div>
  <script src="widget.js"></script>
</body>
</html>
```

### widget.css
```css
:root {
  --primary: #00ffd1;
  --secondary: #8b9dc3;
  --bg: rgba(26, 26, 26, 0.8);
  --border: rgba(255, 255, 255, 0.08);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: transparent;
}

.widget {
  container-type: inline-size;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 1cqw;
  backdrop-filter: blur(8px);
  padding: 4cqw;
  gap: 3cqw;
  font-family: 'Georgia', serif;
}

.quote-container {
  display: flex;
  flex-direction: column;
  gap: 1.5cqw;
  text-align: center;
  flex: 1;
  justify-content: center;
}

.quote {
  font-size: 3cqw;
  color: var(--primary);
  line-height: 1.4;
  font-style: italic;
}

.author {
  font-size: 2cqw;
  color: var(--secondary);
  font-style: normal;
}

.refresh-btn {
  width: 6cqw;
  height: 6cqw;
  border-radius: 50%;
  background: var(--primary);
  color: var(--bg);
  border: none;
  font-size: 3cqw;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.refresh-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(0, 255, 209, 0.3);
}

.refresh-btn:active {
  transform: scale(0.95);
}

@media (prefers-color-scheme: light) {
  :root {
    --primary: #0066ff;
    --secondary: #666666;
    --bg: rgba(255, 255, 255, 0.8);
    --border: rgba(0, 0, 0, 0.1);
  }
  
  .refresh-btn {
    color: var(--bg);
  }
}
```

### widget.js
```javascript
(function() {
  const quotes = [
    { text: 'The only way to do great work is to love what you do.', author: 'Steve Jobs' },
    { text: 'Innovation distinguishes between a leader and a follower.', author: 'Steve Jobs' },
    { text: 'Life is what happens when you\'re busy making other plans.', author: 'John Lennon' },
    { text: 'The future belongs to those who believe in the beauty of their dreams.', author: 'Eleanor Roosevelt' },
    { text: 'It is during our darkest moments that we must focus to see the light.', author: 'Aristotle' },
  ];
  
  const quoteEl = document.getElementById('quote');
  const authorEl = document.getElementById('author');
  const refreshBtn = document.getElementById('refresh');
  
  function getRandomQuote() {
    return quotes[Math.floor(Math.random() * quotes.length)];
  }
  
  function displayQuote() {
    const quote = getRandomQuote();
    quoteEl.textContent = '"' + quote.text + '"';
    authorEl.textContent = '— ' + quote.author;
  }
  
  refreshBtn.addEventListener('click', displayQuote);
  
  // Display random quote on load
  displayQuote();
})();
```

## 4. Todo List - Interactive Widget

Simple todo list that persists via localStorage.

### widget.html
```html
<!-- aspect-ratio: 1:1 -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Todo Widget</title>
  <link rel="stylesheet" href="widget.css">
</head>
<body>
  <div class="widget">
    <h2 class="title">Today's Tasks</h2>
    <div class="todo-list" id="todoList"></div>
    <div class="input-area">
      <input type="text" id="todoInput" placeholder="Add a task..." aria-label="Add new task">
      <button id="addBtn" aria-label="Add task">+</button>
    </div>
  </div>
  <script src="widget.js"></script>
</body>
</html>
```

### widget.css
```css
:root {
  --primary: #00ffd1;
  --secondary: #8b9dc3;
  --bg: rgba(26, 26, 26, 0.8);
  --border: rgba(255, 255, 255, 0.08);
  --success: #00ff88;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: transparent;
}

.widget {
  container-type: inline-size;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 1cqw;
  backdrop-filter: blur(8px);
  padding: 3cqw;
  gap: 2cqw;
  font-family: 'Segoe UI', sans-serif;
}

.title {
  font-size: 4cqw;
  color: var(--primary);
  margin-bottom: 1cqw;
}

.todo-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5cqw;
  padding-right: 1cqw;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 1.5cqw;
  padding: 1.5cqw;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1cqw;
  cursor: pointer;
  transition: all 0.2s ease;
}

.todo-item:hover {
  background: rgba(0, 255, 209, 0.1);
}

.todo-item.done {
  opacity: 0.6;
}

.todo-item.done .text {
  text-decoration: line-through;
  color: var(--secondary);
}

.checkbox {
  width: 2cqw;
  height: 2cqw;
  border: 1px solid var(--primary);
  border-radius: 0.5cqw;
  flex-shrink: 0;
}

.todo-item.done .checkbox {
  background: var(--success);
  border-color: var(--success);
}

.text {
  font-size: 2cqw;
  color: var(--primary);
  flex: 1;
}

.input-area {
  display: flex;
  gap: 1cqw;
}

input {
  flex: 1;
  padding: 1.5cqw;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  border-radius: 0.8cqw;
  color: var(--primary);
  font-size: 2cqw;
  outline: none;
  transition: border 0.2s;
}

input:focus {
  border-color: var(--primary);
}

input::placeholder {
  color: var(--secondary);
}

button {
  width: 5cqw;
  padding: 1.5cqw;
  background: var(--primary);
  color: var(--bg);
  border: none;
  border-radius: 0.8cqw;
  font-size: 2.5cqw;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: bold;
}

button:hover {
  transform: scale(1.05);
}

button:active {
  transform: scale(0.95);
}

@media (prefers-color-scheme: light) {
  :root {
    --primary: #0066ff;
    --secondary: #666666;
    --bg: rgba(255, 255, 255, 0.8);
    --border: rgba(0, 0, 0, 0.1);
  }
}
```

### widget.js
```javascript
(function() {
  const todoList = document.getElementById('todoList');
  const todoInput = document.getElementById('todoInput');
  const addBtn = document.getElementById('addBtn');
  
  // Load todos from localStorage
  const todos = JSON.parse(localStorage.getItem('todos')) || [];
  
  function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
  }
  
  function renderTodos() {
    todoList.innerHTML = '';
    todos.forEach((todo, index) => {
      const item = document.createElement('div');
      item.className = 'todo-item' + (todo.done ? ' done' : '');
      item.innerHTML = '<div class="checkbox"></div><div class="text">' + todo.text + '</div>';
      item.addEventListener('click', () => {
        todos[index].done = !todos[index].done;
        saveTodos();
        renderTodos();
      });
      todoList.appendChild(item);
    });
  }
  
  function addTodo() {
    const text = todoInput.value.trim();
    if (text) {
      todos.push({ text: text, done: false });
      saveTodos();
      renderTodos();
      todoInput.value = '';
    }
  }
  
  addBtn.addEventListener('click', addTodo);
  todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
  });
  
  // Initial render
  renderTodos();
})();
```

## Creating Your Own Widget

Use these examples as templates:

1. **Choose a template** - Pick the example structure that matches your widget type
2. **Copy the files** - Create a new folder in `examples/widgets/`
3. **Modify HTML** - Update the aspect ratio and structure
4. **Customize CSS** - Adjust colors, sizing, and responsive breakpoints
5. **Add functionality** - Update the JavaScript with your logic
6. **Test** - Use Widget Center to position and test your widget

## Tips for Successful Widgets

- Start simple - build from the Clock or Quote examples
- Use container-relative units (cqw) for responsiveness
- Support dark mode with `@media (prefers-color-scheme)`
- Handle errors gracefully
- Clean up intervals and listeners
- Add comments to complex code
- Test at multiple sizes

---

For more details, see:
- [Structure Guide](./STRUCTURE.md) - File format details
- [Best Practices](./BEST_PRACTICES.md) - Performance and quality guidelines
- [Styling Guide](./STYLING.md) - Advanced CSS techniques
