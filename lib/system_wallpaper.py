from Cocoa import NSScreen, NSWorkspace
from Foundation import NSObject, NSURL
from objc import super as objc_super


def set_macos_wallpaper(image_path: str):
    ws = NSWorkspace.sharedWorkspace()
    url = NSURL.fileURLWithPath_(image_path)

    for screen in NSScreen.screens():
        try:
            ws.setDesktopImageURL_forScreen_options_error_(
                url,
                screen,
                {},
                None
            )
        except Exception as e:
            print("Failed to set wallpaper:", e)




class SpaceObserver(NSObject):
    def initWithCallback_(self, callback):
        # Call the Objective-C superclass init
        self = objc_super(SpaceObserver, self).init()
        if self is None:
            return None
        
        self.current_wallpaper_path = None
        self.callback = callback
        return self

    def spaceChanged_(self, notification):
        self.callback()

    def wake_(self, notification):
        self.callback()
    

    def reapply_wallpaper(self):
        if not self.current_wallpaper_path:
            return

        set_macos_wallpaper(self.current_wallpaper_path)


    def install_space_observers(self):
        ws = NSWorkspace.sharedWorkspace()
        nc = ws.notificationCenter()

        self.space_observer = SpaceObserver.alloc().initWithCallback_(
            self.reapply_wallpaper
        )

        nc.addObserver_selector_name_object_(
            self.space_observer,
            "spaceChanged:",
            "NSWorkspaceActiveSpaceDidChangeNotification",
            None
        )

        nc.addObserver_selector_name_object_(
            self.space_observer,
            "wake:",
            "NSWorkspaceDidWakeNotification",
            None
        )




