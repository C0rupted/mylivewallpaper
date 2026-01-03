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
    offsetY: 0
};

async function init() {
    try {
        // Load current config
        const res = await fetch(API + "widgets/config");
        if (!res.ok) throw new Error("Failed to load widget config");
        
        const data = await res.json();
        widgets = JSON.parse(JSON.stringify(data.widgets)); // Deep copy
        originalConfig = JSON.parse(JSON.stringify(data.widgets));
        
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
            const rect = preview.getBoundingClientRect();
            draggingState.isActive = true;
            draggingState.widgetIdx = idx;
            draggingState.offsetX = e.clientX - rect.left;
            draggingState.offsetY = e.clientY - rect.top;
            preview.classList.add('dragging');
        });
        
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
            }
            draggingState.isActive = false;
            draggingState.widgetIdx = null;
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
