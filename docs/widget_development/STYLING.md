# Widget Styling Guide

Advanced CSS techniques and patterns for creating responsive, accessible widgets.

## Container Queries Deep Dive

Container queries are the foundation of responsive widgets. They allow styles to respond to the container size rather than viewport size.

### Basic Container Query

```css
/* Define a container */
.widget {
  container-type: inline-size;
}

/* Styles respond to container width */
@container (max-width: 200px) {
  .title {
    font-size: 12px;
  }
}

@container (min-width: 200px) {
  .title {
    font-size: 16px;
  }
}
```

### Container Query Units

The most powerful feature is container-relative units:

| Unit | Meaning | Example |
|------|---------|---------|
| `cqw` | 1% of container width | `font-size: 4cqw` = 4% of width |
| `cqh` | 1% of container height | `height: 50cqh` = 50% of height |
| `cqi` | 1% of container inline size | Usually same as cqw |
| `cqb` | 1% of container block size | Usually same as cqh |
| `cqmin` | Min of cqw/cqh | `width: 100cqmin` = smaller dimension |
| `cqmax` | Max of cqw/cqh | `width: 100cqmax` = larger dimension |

### Container Query Comparison

```css
/* BAD - Fixed pixel sizes don't scale */
.widget-bad {
  font-size: 16px;
  padding: 20px;
  border-radius: 8px;
  /* Works only at one size */
}

/* GOOD - Container-relative sizes scale perfectly */
.widget-good {
  container-type: inline-size;
  font-size: 4cqw;
  padding: 5cqw;
  border-radius: 2cqw;
  /* Scales beautifully at any size */
}
```

### Practical Container Query Example

```css
.widget {
  container-type: inline-size;
  display: flex;
  flex-direction: column;
  gap: 3cqw;
}

/* Very small - stack vertically */
@container (max-width: 150px) {
  .header {
    font-size: 3cqw;
    margin-bottom: 2cqw;
  }
  
  .value {
    font-size: 5cqw;
  }
}

/* Medium - balanced layout */
@container (min-width: 150px) and (max-width: 300px) {
  .header {
    font-size: 4cqw;
  }
  
  .value {
    font-size: 6cqw;
  }
}

/* Large - spacious layout */
@container (min-width: 300px) {
  .header {
    font-size: 5cqw;
  }
  
  .value {
    font-size: 8cqw;
  }
  
  /* Can add side-by-side layouts */
  .widget {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
```

## Responsive Layout Patterns

### 1. Adaptive Text Size

Automatically adjust text size based on widget size:

```css
.widget {
  container-type: inline-size;
  font-size: 1rem; /* Fallback */
}

.title {
  font-size: 4cqw;
  font-weight: 600;
}

.value {
  font-size: 6cqw;
  font-weight: 700;
  margin-top: 2cqw;
}

.label {
  font-size: 2.5cqw;
  opacity: 0.7;
  text-transform: uppercase;
  letter-spacing: 1px;
}
```

### 2. Adaptive Layout Direction

Change from vertical to horizontal based on space:

```css
.widget {
  container-type: inline-size;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 3cqw;
}

/* Switch to row layout when space allows */
@container (min-width: 300px) {
  .content {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

/* Three column layout at larger sizes */
@container (min-width: 600px) {
  .content {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 5cqw;
  }
}
```

### 3. Adaptive Spacing

Adjust padding and margins for comfortable viewing:

```css
.widget {
  container-type: inline-size;
}

.widget-content {
  padding: 4cqw;
}

@container (max-width: 150px) {
  .widget-content {
    padding: 3cqw;
    gap: 2cqw;
  }
}

@container (min-width: 400px) {
  .widget-content {
    padding: 5cqw;
    gap: 4cqw;
  }
}
```

### 4. Multi-Column Grid

Responsive grid layout:

```css
.widget {
  container-type: inline-size;
}

.items {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2cqw;
}

/* Two columns at medium size */
@container (min-width: 300px) {
  .items {
    grid-template-columns: 1fr 1fr;
  }
}

/* Three columns at larger size */
@container (min-width: 500px) {
  .items {
    grid-template-columns: 1fr 1fr 1fr;
  }
}
```

## Dark Mode Support

### 1. CSS Variables for Theming

```css
.widget {
  /* Define color variables */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #000000;
  --text-secondary: #666666;
  --accent: #0066ff;
  --border: #e0e0e0;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  .widget {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2a2a2a;
    --text-primary: #ffffff;
    --text-secondary: #aaaaaa;
    --accent: #00d4ff;
    --border: #404040;
  }
}

/* Use variables consistently */
.widget {
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.title {
  color: var(--text-primary);
}

.label {
  color: var(--text-secondary);
}

.button {
  background: var(--accent);
  color: var(--bg-primary);
}
```

### 2. Testing Dark Mode

In Widget Center's config panel, toggle dark/light mode to test. Your widget should remain readable in both:

```css
/* Light mode - good contrast */
.widget {
  background: white;
  color: black;
}

/* Dark mode - still readable */
@media (prefers-color-scheme: dark) {
  .widget {
    background: #1a1a1a;
    color: #ffffff;
  }
}
```

### 3. Adaptive Opacity

Some designs use opacity to adapt to background:

```css
.overlay {
  /* Lighter in dark mode */
  background: rgba(255, 255, 255, 0.1);
}

@media (prefers-color-scheme: light) {
  .overlay {
    background: rgba(0, 0, 0, 0.1);
  }
}
```

## Animation Techniques

### 1. Smooth Transitions

```css
.value {
  transition: all 0.3s ease;
}

.value:hover {
  color: #00ff88;
  transform: scale(1.05);
}
```

### 2. Continuous Animations

```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.indicator {
  animation: pulse 1.5s ease-in-out infinite;
}
```

### 3. Loading Animation

```css
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading {
  animation: spin 1s linear infinite;
}
```

### 4. Slide In Animation

```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.widget-content {
  animation: slideIn 0.5s ease-out;
}
```

### 5. Shimmer Loading Effect

```css
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.loading-bar {
  background: linear-gradient(
    90deg,
    #e0e0e0 25%,
    #f0f0f0 50%,
    #e0e0e0 75%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}
```

## Advanced Styling Patterns

### 1. Glassmorphism Effect

Modern frosted glass appearance:

```css
.widget {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4cqw;
}

@media (prefers-color-scheme: dark) {
  .widget {
    background: rgba(30, 30, 30, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}
```

### 2. Gradient Backgrounds

```css
.widget {
  background: linear-gradient(
    135deg,
    #667eea 0%,
    #764ba2 100%
  );
}

/* Animated gradient */
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.widget-animated {
  background: linear-gradient(
    -45deg,
    #667eea,
    #764ba2,
    #f093fb,
    #4facfe
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}
```

### 3. Shadow Effects

```css
/* Subtle shadow */
.widget {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Deep shadow */
.widget-elevated {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* Glow effect */
.widget-glow {
  box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}

/* Inner shadow */
.widget-inset {
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

### 4. Border Treatments

```css
/* Thin border */
.widget {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Gradient border */
.widget-gradient-border {
  border: 2px solid;
  border-image: linear-gradient(
    135deg,
    #667eea,
    #764ba2
  ) 1;
}

/* Rounded borders */
.widget {
  border-radius: 3cqw;
}

/* Only top and bottom */
.widget-partial {
  border-radius: 3cqw 3cqw 0 0;
}
```

## Accessibility in CSS

### 1. Focus Indicators

```css
button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* For keyboard navigation */
:focus-visible {
  outline: 2px dashed var(--accent);
}
```

### 2. Color Contrast

Ensure text is readable:

```css
/* Good - 7:1 contrast ratio */
.widget {
  color: #000000;
  background: #ffffff;
}

/* Also good in dark mode */
@media (prefers-color-scheme: dark) {
  .widget {
    color: #ffffff;
    background: #1a1a1a;
  }
}
```

### 3. Reduced Motion Support

Respect user preferences for animations:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

/* Or selectively reduce */
@media (prefers-reduced-motion: reduce) {
  .widget {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 4. Text Sizing

```css
/* Allow user to zoom */
.widget {
  font-size: 4cqw;
  line-height: 1.5;
  letter-spacing: 0.5px;
}

/* Don't use user-select: none on text */
.text {
  user-select: text; /* Allow selection */
}

/* OK for decorative elements */
.icon {
  user-select: none;
}
```

## Performance Tips

### 1. Avoid Layout Thrashing

```css
/* Bad - triggers reflow */
.item {
  width: 100%;
  margin: calc(100% - 20px);
}

/* Good - simple math */
.item {
  width: 100%;
  margin: auto;
  max-width: calc(100cqw - 2cqw);
}
```

### 2. Use transform for Animations

```css
/* Bad - triggers layout recalculation */
.animated {
  animation: moveDown 1s;
}

@keyframes moveDown {
  from { top: 0; }
  to { top: 100px; }
}

/* Good - only triggers composite */
.animated {
  animation: moveDown 1s;
}

@keyframes moveDown {
  from { transform: translateY(0); }
  to { transform: translateY(100px); }
}
```

### 3. Use will-change Sparingly

```css
/* Only for elements that will animate */
.to-animate {
  will-change: transform;
}

.to-animate:hover {
  transform: scale(1.1);
}
```

## Common Styling Mistakes

| Problem | Bad Example | Good Solution |
|---------|------------|---|
| Fixed pixel sizes | `font-size: 16px` | `font-size: 4cqw` |
| Viewport units | `width: 100vw` | `width: 100%` or `100cqw` |
| Hardcoded colors | `color: #000` (breaks in dark) | Use CSS variables with media query |
| Too many keyframes | 10+ different animations | Reuse and combine animations |
| No transitions | Instant changes | `transition: 0.3s ease` |
| Fixed container | `max-width: 500px` | No limits, responsive |
| No dark mode | Only light theme | Add `@media (prefers-color-scheme)` |
| Complex selectors | `.widget > div > p.text` | Simpler, more direct selectors |

---

Next: See [Code Examples](./EXAMPLES.md) for complete working widget implementations.
