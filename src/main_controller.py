import ZeroSeg.led as led
import threading
import buttons
import clock


def change_mode():
    global mode
    mode += 1
    if mode == 3:
        mode = 1


def run_clock():
    device.clear()
    clock_event.set()
    clock_thread = threading.Thread(target=clock.clock, name="clock")
    clock_thread.start()


"""
* Available modes:
* #1 clock
* #2 display text
"""


device = led.sevensegment()
device.brightness(3)

clock_event = threading.Event()
button_event = threading.Event()

buttons.initialize(device, button_event)
clock.initialize(device, clock_event)

# default mode
mode = 1
run_clock()

while True:
    button_event.wait()
    print("Button event triggered")
    change_mode()

    if mode == 1:
        print("Mode 1")
        run_clock()
    elif mode == 2:
        print("Mode 2")
        clock_event.clear()
        device.clear()
        device.show_message("HELLO")

    button_event.clear()
