import ZeroSeg.led as led
from itertools import cycle
import threading
import buttons
import clock
import temperature


def run_clock():
    clock_thread = threading.Thread(target=clock.run, name="clock")
    clock_thread.start()


def run_temperature():
    temperature_thread = threading.Thread(target=temperature.run, name="temperature")
    temperature_thread.start()


def start_clock_and_temperature():
    device.clear()
    mode_1_event.set()
    run_clock()
    run_temperature()


def start_upcoming_event():
    mode_1_event.clear()
    device.clear()
    device.show_message("HELLO")


device = led.sevensegment()
device.brightness(3)
device.clear()

mode_1_event = threading.Event()
button_event = threading.Event()

buttons.initialize(device, button_event)
clock.initialize(device, mode_1_event)
temperature.initialize(device, mode_1_event)

mode_list  = [1, 2]
mode_cycle = cycle(mode_list)

modes = {
    1: start_clock_and_temperature,
    2: start_upcoming_event
}

# default mode is 1
current_mode = next(mode_cycle)
start_clock_and_temperature()

"""
* Available modes:
* #1 clock and temperature
* #2 upcoming events
"""

while True:
    button_event.wait()

    current_mode = next(mode_cycle)
    modes[current_mode]()

    button_event.clear()
