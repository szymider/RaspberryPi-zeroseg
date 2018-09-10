import ZeroSeg.led as led
import threading
import buttons
import clock

device = led.sevensegment()
brightness = 3
device.brightness(brightness)

"""
* Available modes:
* #1 clock
* #2 display text
"""

mode = 1

clock_event = threading.Event()
temperature_event = threading.Event()

buttonScript.initialize(device, brightness)
timeScript.clock(device)
