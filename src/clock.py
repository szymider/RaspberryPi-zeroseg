import ZeroSeg.led as led
from datetime import datetime
import time
import threading


def initialize(dev, event):
    global mode_1_event, device
    mode_1_event = event
    device = dev


def display_time():
    now    = datetime.now()
    hour   = now.hour
    minute = now.minute
    second = now.second

    # Set hours
    device.letter(0, 4, int(hour / 10))  # Tens
    device.letter(0, 3, hour % 10, True)  # Ones
    # Set minutes
    device.letter(0, 2, int(minute / 10))  # Tens
    device.letter(0, 1, minute % 10)  # Ones

    global timeout
    timeout = 60 - second


def run():
    global counter, timeout

    while mode_1_event.is_set():
        if counter >= timeout:
            display_time()
            counter = 0
        counter += 1
        time.sleep(1)
    counter = timeout


device        = None
mode_1_event  = None
timeout       = 60
counter       = timeout
