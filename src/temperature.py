import time
import threading
import requests
import json
import logging


def initialize(dev, event):
    global device, mode_1_event
    device = dev
    mode_1_event = event


def sleeper(seconds):
    time.sleep(seconds)
    timeout_event.set()


def get_temperature():
    global temperature_new
    response = requests.get('http://api.openweathermap.org/data/2.5/'
                            'weather?id=3081368&units=metric&appid=97b270e75c4525b3d0e79a2d1b635a2e')
    if response.status_code == requests.codes.ok:
        json_object = response.json()
        temperature_new = int(json_object['main']['temp'])
    else:
        temperature_new = None
        logger.error('Connection error')


def display_temperature():
    global temperature_current, temperature_new
    get_temperature()
    if not (temperature_new is None):
        logger.info('New temp: ' + str(temperature_current))
        if temperature_new != temperature_current:
            temperature_current = temperature_new

            # clear temperature display
            for i in range(5, 9):
                device.letter(0, i, ' ')

            index = 8
            if temperature_current < 0:
                index = 7
                device.letter(0, 8, '-')

            if abs(temperature_current)/10 > 0:
                device.letter(0, index, int(abs(temperature_current) / 10))    # Tens
                index -= 1

            device.letter(0, index, int(abs(temperature_current) % 10))  # Ones
            device.letter(0, index-1, "*")
    else:
        device.letter(0, 8, '-')
        for i in range(5, 8):
            device.letter(0, i, ' ')

    sleep_time = 900
    sleeper_thread = threading.Thread(target=sleeper, name="sleeper", args=(sleep_time,))
    sleeper_thread.start()


def run():
    display_temperature()
    while mode_1_event.is_set():
        if timeout_event.is_set():
            timeout_event.clear()
            display_temperature()
        time.sleep(1)


logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/home/pi/ZeroSeg/apo/logs/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

temperature_current = 99
temperature_new     = None
device              = None
mode_1_event        = None
timeout_event       = threading.Event()
