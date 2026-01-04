build:
	@echo "Building MyLiveWallpaper..."
	nuitka \
	--standalone \
	--macos-create-app-bundle \
	--macos-app-name="MyLiveWallpaper" \
	--macos-signed-app-name="com.c0rupted.mylivewallpaper" \
	--macos-app-icon=MyLiveWallpaper.icns \
	--macos-app-version="1.0" \
	--macos-app-mode=ui-element \
	--include-data-dir=web=web \
	--include-data-dir=examples=examples \
	--follow-imports \
	--output-filename=MyLiveWallpaper \
	main.py
	@echo "Build complete!"


clean:
	rm -rf main.app main.build main.dist
	@echo "Cleaned build artifacts."

