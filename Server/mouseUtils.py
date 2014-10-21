from AppKit import NSEvent
import Quartz

pressID = [None, Quartz.kCGEventLeftMouseDown,
           Quartz.kCGEventRightMouseDown, Quartz.kCGEventOtherMouseDown]

releaseID = [None, Quartz.kCGEventLeftMouseUp,
             Quartz.kCGEventRightMouseUp, Quartz.kCGEventOtherMouseUp]

def press(x, y, button=1):
	event = Quartz.CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
	Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def release(x, y, button=1):
	event = Quartz.CGEventCreateMouseEvent(None, releaseID[button], (x, y), button - 1)
	Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def click(button):
	x, y = position()
	press(x, y, button)
	release(x, y, button)

def position():
    loc = NSEvent.mouseLocation()
    return loc.x, Quartz.CGDisplayPixelsHigh(0) - loc.y

def move(x, y):
    moveEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, moveEvent)