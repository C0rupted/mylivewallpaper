build:
	nuitka --standalone --macos-create-app-bundle \
	--include-data-dir=scripts=scripts \
	--include-data-dir=static=static \
	--macos-app-name="MyLiveWallpaper" \
	--macos-signed-app-name="com.c0rupted.mylivewallpaper" \
	--macos-app-icon=static/mylivewallpaper.icns \
	--macos-app-version="1.0" \
	--macos-app-mode=ui-element \
	mylivewallpaper.py


clean:
	rm -rf mylivewallpaper.app mylivewallpaper.build mylivewallpaper.dist
