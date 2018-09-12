import time
import threading
import requests
import json


def initialize(dev, event):
    global device, mode_1_event
    device = dev
    mode_1_event = event


def sleeper(seconds):
    time.sleep(seconds)
    timeout_event.set()


def get_temperature():
    global temperature
    response = requests.get('http://api.openweathermap.org/data/2.5/'
                            'weather?id=3081368&units=metric&appid=97b270e75c4525b3d0e79a2d1b635a2e')
    if response.status_code == requests.codes.ok:
        json_object = response.json()
        temperature = json_object['main']['temp']
    else:
        temperature = None
        print("Temperature empty")


# TODO: how to display minus temperature
def display_temperature():
    global temperature
    get_temperature()

    if not (temperature is None):
        if temperature/10 > 0:
            device.letter(0, 8, int(temperature / 10))  # Tens
        device.letter(0, 7, temperature % 10)           # Ones
        device.letter(0, 6, "*")
    else:
        device.letter(0, 7, '-')

    sleep_time = 1800
    sleeper_thread = threading.Thread(target=sleeper, name="sleeper", args=(sleep_time,))
    sleeper_thread.start()


def run():
    display_temperature()
    while mode_1_event.is_set():
        if timeout_event.is_set():
            timeout_event.clear()
            display_temperature()
        time.sleep(1)


temperature = None
device = None
mode_1_event = None
timeout_event = threading.Event()
