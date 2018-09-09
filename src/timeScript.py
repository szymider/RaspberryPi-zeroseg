import ZeroSeg.led as led
import time
import threading
from datetime import datetime


def sleeper(seconds):
    print("Sleep for {}".format(seconds))
    time.sleep(seconds)
    print("Wake up")
    timeout_event.set()


def display_time(device):
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


def clock(device):
    display_time(device)
    while True:  # TODO: clock_event
        timeout_event.wait()
        timeout_event.clear()
        display_time(device)


timeout_event = threading.Event()
