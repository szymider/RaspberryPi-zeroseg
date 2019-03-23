import time
import threading
import requests
import json
import logging
import datetime


def initialize(dev, event, log):
    global device, mode_1_event, logger
    device       = dev
    logger       = log
    mode_1_event = event


def get_temperature():
    global temperature_new
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/'
                                'weather?id=3081368&units=metric&appid=97b270e75c4525b3d0e79a2d1b635a2e')
        if response.status_code == requests.codes.ok:
            json_object = response.json()
            temperature_new = int(json_object['main']['temp'])
        else:
            temperature_new = None
            logger.error('Invalid response code from openweathermap API')
    except requests.exceptions.RequestException as exception:
        logger.error(exception)
        temperature_new = None


def display_temperature():
    global temperature_current, temperature_new, counter
    get_temperature()
    if not (temperature_new is None):
        logger.info('New temperature: %s' % temperature_new)
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
            device.letter(0, index-1, '*')
    else:
        device.letter(0, 8, '-')
        for i in range(5, 8):
            device.letter(0, i, ' ')


def run():
    global temperature_current, counter, timeout
    temperature_current = None

    while mode_1_event.is_set():
        if counter >= timeout:
            display_temperature()
            counter = 0
        counter += 1
        time.sleep(1)
    counter = timeout


temperature_current = None
temperature_new     = None
device              = None
mode_1_event        = None
logger              = None
timeout             = 900
counter             = timeout
