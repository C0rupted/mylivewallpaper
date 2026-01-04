"""Wallpaper daemon: manages the desktop wallpaper window with widgets."""

from Cocoa import (
    NSApplication,
    NSWindow,
    NSWindowStyleMaskBorderless,
    NSBackingStoreBuffered,
    NSColor,
    NSScreen,
    NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSWindowCollectionBehaviorStationary,
    NSEvent,
    NSEventMaskLeftMouseDown,
)
from Quartz import (
    CGWindowLevelForKey,
    kCGDesktopWindowLevelKey
)
from WebKit import WKWebView, WKWebViewConfiguration
from Foundation import NSURL, NSURLRequest


class WallpaperDaemon:
    """Manages a borderless window positioned at desktop level for displaying widgets."""
    
    def create_window(self):
        """Create the wallpaper window and load the widget page."""
        screen = NSScreen.mainScreen()
        frame = screen.frame()

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame,
            NSWindowStyleMaskBorderless,
            NSBackingStoreBuffered,
            False
        )

        self.window.setLevel_(CGWindowLevelForKey(kCGDesktopWindowLevelKey))
        self.window.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces |
            NSWindowCollectionBehaviorStationary
        )

        self.window.setIgnoresMouseEvents_(False)
        self.window.setAcceptsMouseMovedEvents_(True)

        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())

        self.webview = WKWebView.alloc().initWithFrame_configuration_(
            frame, WKWebViewConfiguration.alloc().init()
        )
        self.webview.setValue_forKey_(False, "drawsBackground")
        self.webview.setOpaque_(False)

        self.webview.loadRequest_(
            NSURLRequest.requestWithURL_(NSURL.URLWithString_("http://localhost:8000/"))
        )

        self.window.setContentView_(self.webview)
        self.window.makeKeyAndOrderFront_(None)

        self._install_mouse_hook()

    def _install_mouse_hook(self):
        """Install a mouse event monitor for debugging click positions."""
        def handler(event):
            pos = event.locationInWindow()
            print(f"Left mouse click at: {pos.x}, {pos.y}")
            return event  # let it propagate
        NSEvent.addLocalMonitorForEventsMatchingMask_handler_(
            NSEventMaskLeftMouseDown,
            handler
        )

    def reload(self):
        """Reload the wallpaper content."""
        if self.webview:
            self.webview.reload()
            print("Wallpaper daemon reloaded!")
