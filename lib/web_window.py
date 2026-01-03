from Cocoa import (
    NSWindow,
    NSScreen,
    NSColor,
    NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable,
    NSWindowStyleMaskResizable,
    NSBackingStoreBuffered,
    NSObject,
)
from WebKit import WKWebView, WKWebViewConfiguration
from Foundation import NSURL, NSURLRequest


class WindowDelegate(NSObject):
    """Delegate to intercept window closing and hide the window instead of destroying."""
    def initWithOwner_(self, owner):
        self = super().init()
        if self is None:
            return None
        self.owner = owner
        return self

    def windowWillClose_(self, notification):
        """Hide the window instead of destroying it."""
        window = notification.object()
        window.orderOut_(None)
        # Optionally free heavy content (WebView) if memory is a concern:
        # self.owner.webview.removeFromSuperview()
        # self.owner.webview = None


class WebWindow:
    """Represents a single reusable web window."""
    def __init__(self):
        self.window = None
        self.webview = None
        self.delegate = None

    def create_window(self, url: str, title: str = "WebWindow", width=900, height=600, reload_on_open=True):
        """Create or show the window with the given URL."""
        if self.window is not None:
            # Window already exists → show it
            self.window.makeKeyAndOrderFront_(None)
            if reload_on_open and self.webview:
                self.webview.loadRequest_(
                    NSURLRequest.requestWithURL_(NSURL.URLWithString_(url))
                )
            return

        # First-time creation
        screen = NSScreen.mainScreen()
        screen_frame = screen.frame()

        x = (screen_frame.size.width - width) / 2
        y = (screen_frame.size.height - height) / 2
        frame = ((x, y), (width, height))

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame,
            NSWindowStyleMaskTitled
            | NSWindowStyleMaskClosable
            | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False,
        )

        self.window.setTitle_(title)
        self.window.setBackgroundColor_(NSColor.blackColor())
        self.window.setReleasedWhenClosed_(False)  # Keep object alive

        # Attach delegate to hide on close
        self.delegate = WindowDelegate.alloc().initWithOwner_(self)
        self.window.setDelegate_(self.delegate)

        # Create WebView
        self.webview = WKWebView.alloc().initWithFrame_configuration_(
            frame, WKWebViewConfiguration.alloc().init()
        )
        self.webview.loadRequest_(
            NSURLRequest.requestWithURL_(NSURL.URLWithString_(url))
        )

        self.window.setContentView_(self.webview)
        self.window.makeKeyAndOrderFront_(None)

    def reload(self):
        """Reload the webview if it exists."""
        if self.webview:
            self.webview.reload()


class WebWindowManager:
    """Manages multiple WebWindow instances, reusing hidden windows when possible."""
    def __init__(self):
        self.windows = []

    def open_window(self, url: str, title: str = "WebWindow", width=900, height=600):
        """
        Open a window.
        Reuse an existing hidden window if available, otherwise create a new one.
        """
        # Try to find a hidden window to reuse
        for w in self.windows:
            if w.window is not None and not w.window.isVisible():
                # Reuse this window
                w.create_window(url, title, width, height)
                return w

        # No reusable window → create new
        w = WebWindow()
        w.create_window(url, title, width, height)
        self.windows.append(w)
        return w

    def close_all(self):
        """Hide all windows."""
        for w in self.windows:
            if w.window is not None and w.window.isVisible():
                w.window.orderOut_(None)

    def reload_all(self):
        """Reload all active webviews."""
        for w in self.windows:
            w.reload()
