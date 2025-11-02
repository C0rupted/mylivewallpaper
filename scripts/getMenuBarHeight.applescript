use framework "AppKit"
use framework "Foundation"
use scripting additions

on getMenuHeight()
	set theScreen to current application's NSScreen's mainScreen()
	set {{x1, y1}, {w1, h1}} to theScreen's frame()
	set {{x2, y2}, {w2, h2}} to theScreen's visibleFrame()
	return (h1 - h2 - y2 - 1) as integer
end getMenuHeight

return getMenuHeight()
