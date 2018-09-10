import ZeroSeg.led as led
from datetime import datetime
import time
import threading


def initialize(dev, event):
    global clock_event, device
    clock_event = event
    device = dev


def sleeper(seconds):
    time.sleep(seconds)
    timeout_event.set()


def display_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    # Set hours
    device.letter(0, 4, int(hour / 10))  # Tens
    device.letter(0, 3, hour % 10, True)  # Ones
    # Set minutes
    device.letter(0, 2, int(minute / 10))  # Tens
    device.letter(0, 1, minute % 10)  # Ones

    sleep_time = 60 - second
    sleeper_thread = threading.Thread(target=sleeper, name="sleeper", args=(sleep_time,))
    sleeper_thread.start()


def clock():
    display_time()
    while clock_event.is_set():
        if timeout_event.is_set():
            time.sleep(3)
            timeout_event.clear()
            display_time()
        time.sleep(1)
    print("clock is over")


device = None
clock_event = None
timeout_event = threading.Event()
