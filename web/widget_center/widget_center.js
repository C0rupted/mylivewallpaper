// Widget Center - Manage widgets, positions, and settings
const API = "http://localhost:8000/api/";

let widgets = [];
let originalConfig = [];
let screenWidth = 1920;
let screenHeight = 1080;
let draggingState = {
    isActive: false,
    widgetIdx: null,
    offsetX: 0,
    offsetY: 0,
    isResizing: false
};

async function init() {
    try {
        // First, discover available widgets from filesystem
        const discoverRes = await fetch(API + "widgets/discover");
        let availableWidgets = {};
        if (discoverRes.ok) {
            const discoverData = await discoverRes.json();
            availableWidgets = discoverData.widgets || {};
        }

        // Load current config
        const res = await fetch(API + "widgets/config");
        if (!res.ok) throw new Error("Failed to load widget config");
        
        const data = await res.json();
        
        // Merge discovered widgets with config: add new widgets that exist on filesystem but not in config
        let configWidgets = data.widgets || [];
        for (const [widgetId, widgetMeta] of Object.entries(availableWidgets)) {
            if (!configWidgets.find(w => w.id === widgetId)) {
                // New widget discovered, add to config
                configWidgets.push({
                    id: widgetId,
                    enabled: false,
                    x: 100,
                    y: 100,
                    height: 100,
                    aspect_ratio: widgetMeta.aspect_ratio || 2.0
                });
            }
        }
        
        widgets = JSON.parse(JSON.stringify(configWidgets)); // Deep copy
        originalConfig = JSON.parse(JSON.stringify(configWidgets));
        
            // Try to get actual screen dimensions from the backend (both full frame and visibleFrame)
            try {
                const screenRes = await fetch(API + 'screen');
                if (screenRes.ok) {
                    const s = await screenRes.json();
                    // s now contains { frame: {width,height,x,y}, visible: {width,height,x,y} }
                    if (s.frame && s.frame.width && s.frame.height) {
                        screenWidth = s.frame.width;
                        screenHeight = s.frame.height;
                        // keep visible for debugging/adjustments if needed
                        window.__screen_debug = { frame: s.frame, visible: s.visible };
                        console.log('Screen frame:', s.frame, 'Visible frame:', s.visible);
                    }
                }
            } catch (e) {
                console.warn('Could not fetch screen dimensions, falling back to defaults');
            }
        
        renderWidgetList();
        renderCanvas();
        attachEventListeners();
        setupBackgroundWallpaper();
    } catch (e) {
        console.error("Initialization error:", e);
        alert("Failed to load widget configuration");
    }
}

function setupBackgroundWallpaper() {
    const canvas = document.getElementById('widgets-canvas');
    // Set background to the current wallpaper
    canvas.style.backgroundImage = 'url(' + API + 'wallpaper)';
    canvas.style.backgroundSize = 'cover';
    canvas.style.backgroundPosition = 'center';
}

function renderWidgetList() {
    const list = document.getElementById('widget-list');
    list.innerHTML = '';
    
    widgets.forEach((w, idx) => {
        const item = document.createElement('div');
        item.className = 'widget-item' + (w.enabled ? ' enabled' : '');
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = w.enabled;
        checkbox.addEventListener('change', (e) => {
            widgets[idx].enabled = e.target.checked;
            item.classList.toggle('enabled', e.target.checked);
            renderCanvas();
        });
        
        const label = document.createElement('div');
        label.className = 'widget-item-name';
        label.textContent = w.id.charAt(0).toUpperCase() + w.id.slice(1);
        
        item.appendChild(checkbox);
        item.appendChild(label);
        list.appendChild(item);
    });
}

function renderCanvas() {
    const canvas = document.getElementById('widgets-canvas');
    canvas.innerHTML = '';
    
    const container = document.getElementById('canvas-container');
    const canvasRect = canvas.getBoundingClientRect();
    // use both canvas width/height for accurate scaling (preserve aspect ratio)
    const scaleX = (canvasRect.width || container.offsetWidth) / screenWidth;
    const scaleY = (canvasRect.height || container.offsetHeight) / screenHeight;
    const scale = Math.min(scaleX, scaleY);
    
    widgets.forEach((w, idx) => {
        if (!w.enabled) return;
        
        const preview = document.createElement('div');
        preview.className = 'widget-preview';
        // compute scaled positions and sizes based on canvas rect
        const left = Math.round((w.x || 0) * scale);
        const top = Math.round((w.y || 0) * scale);
        const width = Math.max(20, Math.round((w.width || 100) * scale));
        const height = Math.max(20, Math.round((w.height || 50) * scale));
        preview.style.left = left + 'px';
        preview.style.top = top + 'px';
        preview.style.width = width + 'px';
        preview.style.height = height + 'px';
        preview.dataset.widgetIdx = idx;
        preview.textContent = w.id;
        
        // Drag functionality: compute offsets using boundingClientRect for precision
        preview.addEventListener('mousedown', (e) => {
            // Check if clicking resize handle
            if (e.target.classList.contains('widget-resize-handle')) {
                const rect = preview.getBoundingClientRect();
                draggingState.isActive = true;
                draggingState.isResizing = true;
                draggingState.widgetIdx = idx;
                draggingState.offsetX = e.clientX;
                draggingState.offsetY = e.clientY;
                preview.classList.add('resizing');
                return;
            }
            
            const rect = preview.getBoundingClientRect();
            draggingState.isActive = true;
            draggingState.isResizing = false;
            draggingState.widgetIdx = idx;
            draggingState.offsetX = e.clientX - rect.left;
            draggingState.offsetY = e.clientY - rect.top;
            preview.classList.add('dragging');
        });
        
        // Add resize handle
        const resizeHandle = document.createElement('div');
        resizeHandle.className = 'widget-resize-handle';
        preview.appendChild(resizeHandle);
        
        canvas.appendChild(preview);
    });
    
    // Reattach global drag handlers
    attachDragHandlers();
}

function attachDragHandlers() {
    const canvas = document.getElementById('widgets-canvas');
    const container = document.getElementById('canvas-container');
    const canvasRect = canvas.getBoundingClientRect();
    const scaleX = (canvasRect.width || container.offsetWidth) / screenWidth;
    const scaleY = (canvasRect.height || container.offsetHeight) / screenHeight;
    const scale = Math.min(scaleX, scaleY);
    
    const handleMouseMove = (e) => {
        if (!draggingState.isActive || draggingState.widgetIdx === null) return;

        const preview = canvas.querySelector(`[data-widget-idx="${draggingState.widgetIdx}"]`);
        if (!preview) return;

        const canvasRect = canvas.getBoundingClientRect();

        if (draggingState.isResizing) {
            // Resize from bottom-right
            const deltaX = e.clientX - draggingState.offsetX;
            const deltaY = e.clientY - draggingState.offsetY;
            
            const widget = widgets[draggingState.widgetIdx];
            const aspectRatio = widget.aspect_ratio;
            
            let newWidth = Math.max(40, preview.offsetWidth + deltaX);
            let newHeight = Math.max(40, preview.offsetHeight + deltaY);
            
            // Apply aspect ratio constraint if not "flex"
            if (aspectRatio !== "flex" && aspectRatio > 0) {
                // Prefer width as primary; adjust height to match ratio
                newHeight = Math.round(newWidth / aspectRatio);
            }
            
            // Constrain to canvas bounds
            const maxWidth = canvasRect.width - preview.offsetLeft;
            const maxHeight = canvasRect.height - preview.offsetTop;
            
            newWidth = Math.min(newWidth, maxWidth);
            newHeight = Math.min(newHeight, maxHeight);
            
            preview.style.width = newWidth + 'px';
            preview.style.height = newHeight + 'px';
            
            // Store unscaled dimensions
            widgets[draggingState.widgetIdx].width = Math.round(newWidth / scale);
            widgets[draggingState.widgetIdx].height = Math.round(newHeight / scale);
            
            // Update stored offsets for next move
            draggingState.offsetX = e.clientX;
            draggingState.offsetY = e.clientY;
            return;
        }

        // Calculate desired top-left position relative to canvas using stored offsets
        let newX = e.clientX - canvasRect.left - draggingState.offsetX;
        let newY = e.clientY - canvasRect.top - draggingState.offsetY;

        // Ensure the widget's bottom-right remains inside the canvas by constraining
        const maxX = Math.max(0, canvasRect.width - preview.offsetWidth);
        const maxY = Math.max(0, canvasRect.height - preview.offsetHeight);

        newX = Math.max(0, Math.min(newX, maxX));
        newY = Math.max(0, Math.min(newY, maxY));

        preview.style.left = newX + 'px';
        preview.style.top = newY + 'px';

        // Store in original screen coordinates (unscaled)
        // Note: we assume widget.y is distance from the TOP of the screen.
        widgets[draggingState.widgetIdx].x = Math.round(newX / scale);
        widgets[draggingState.widgetIdx].y = Math.round(newY / scale);
    };
    
    const handleMouseUp = () => {
        if (draggingState.isActive) {
            const preview = canvas.querySelector(`[data-widget-idx="${draggingState.widgetIdx}"]`);
            if (preview) {
                preview.classList.remove('dragging');
                preview.classList.remove('resizing');
            }
            draggingState.isActive = false;
            draggingState.widgetIdx = null;
            draggingState.isResizing = false;
        }
    };
    
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
}

async function saveConfig() {
    try {
        const res = await fetch(API + "widgets/config", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(widgets)
        });
        
        if (!res.ok) throw new Error("Failed to save configuration");
        
        originalConfig = JSON.parse(JSON.stringify(widgets));
        alert("✓ Widget configuration saved successfully!");
    } catch (e) {
        console.error("Save error:", e);
        alert("Failed to save configuration: " + e.message);
    }
}

function resetConfig() {
    if (!confirm("Reset to last saved configuration?")) return;
    widgets = JSON.parse(JSON.stringify(originalConfig));
    renderWidgetList();
    renderCanvas();
}

function attachEventListeners() {
    const saveBtn = document.getElementById('save-btn');
    const resetBtn = document.getElementById('reset-btn');
    const openWidgetsBtn = document.getElementById('open-widgets-btn');
    
    if (saveBtn) saveBtn.addEventListener('click', saveConfig);
    if (resetBtn) resetBtn.addEventListener('click', resetConfig);
    if (openWidgetsBtn) {
        openWidgetsBtn.addEventListener('click', async () => {
            try {
                const res = await fetch(API + 'open_widgets_folder', { method: 'POST' });
                if (!res.ok) throw new Error('Failed to open folder');
            } catch (e) {
                console.error('Open widgets folder error', e);
                alert('Failed to open widgets folder');
            }
        });
    }
    
    // Add window resize listener to recalculate scale and re-render
    window.addEventListener('resize', () => {
        renderCanvas();
    });
}

window.addEventListener('load', init);
