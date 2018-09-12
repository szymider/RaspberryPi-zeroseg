import ZeroSeg.led as led
import threading
import buttons
import clock
import temperature


def change_mode():
    global mode
    mode += 1
    if mode == 3:
        mode = 1


def run_clock():
    clock_thread = threading.Thread(target=clock.run, name="clock")
    clock_thread.start()


def run_temperature():
    temperature_thread = threading.Thread(target=temperature.run, name="temperature")
    temperature_thread.start()


device = led.sevensegment()
device.brightness(3)
device.clear()

mode_1_event = threading.Event()
button_event = threading.Event()

buttons.initialize(device, button_event)
clock.initialize(device, mode_1_event)
temperature.initialize(device, mode_1_event)

# default mode
mode = 1
mode_1_event.set()
run_clock()
run_temperature()

"""
* Available modes:
* #1 clock and temperature
* #2 display text
"""

while True:
    button_event.wait()
    print("Button event triggered")
    change_mode()

    if mode == 1:
        print("Mode 1")
        device.clear()
        mode_1_event.set()
        run_clock()
        run_temperature()
    elif mode == 2:
        print("Mode 2")
        mode_1_event.clear()
        device.clear()
        device.show_message("HELLO")

    button_event.clear()
