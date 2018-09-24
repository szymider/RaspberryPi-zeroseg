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


def display_temperature():
    global temperature
    get_temperature()

    # clear temperature display
    for i in range(5, 9):
        device.letter(0, i, ' ')

    if not (temperature is None):
        index = 8

        if temperature < 0:
            index = 7
            device.letter(0, 8, '-')

        if abs(temperature)/10 > 0:
            device.letter(0, index, int(abs(temperature) / 10))    # Tens
            index -= 1

        device.letter(0, index, int(abs(temperature) % 10))  # Ones
        device.letter(0, index-1, "*")
    else:
        device.letter(0, 8, '-')

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


temperature   = None
device        = None
mode_1_event  = None
timeout_event = threading.Event()
