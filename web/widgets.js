// Widget loader: fetches config and renders widgets as isolated iframes
const API_URL = "http://localhost:8000/api/";
const WIDGET_FRAME_URL = "http://localhost:8000/widgets";

async function loadWidgetConfig() {
    try {
        const res = await fetch(API_URL + "widgets/config");
        if (!res.ok) return [];
        const data = await res.json();
        return data.widgets || [];
    } catch (e) {
        console.error("Failed to load widget config:", e);
        return [];
    }
}

function renderWidget(widget) {
    // Create widget container
    const container = document.createElement('div');
    container.className = 'widget-container';
    container.style.position = 'absolute';
    container.style.left = widget.x + 'px';
    container.style.top = widget.y + 'px';
    container.style.width = widget.width + 'px';
    container.style.height = widget.height + 'px';
    container.dataset.widgetId = widget.id;
    
    // Create iframe for isolated widget
    const iframe = document.createElement('iframe');
    iframe.src = `${WIDGET_FRAME_URL}/${widget.id}/frame`;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    iframe.style.borderRadius = '12px';
    iframe.style.backgroundColor = 'transparent';
    iframe.sandbox.add('allow-same-origin');
    iframe.sandbox.add('allow-scripts');
    
    container.appendChild(iframe);
    return container;
}

async function initWidgets() {
    const root = document.getElementById('widgets-root');
    if (!root) {
        console.warn('widgets-root not found');
        return;
    }
    
    const widgets = await loadWidgetConfig();
    
    widgets.forEach(widget => {
        if (!widget.enabled) return;
        const container = renderWidget(widget);
        root.appendChild(container);
    });
}

// Initialize on page load
window.addEventListener('load', () => {
    initWidgets().catch(console.error);
});
