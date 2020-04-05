import time
import threading
import requests
import json
import logging
import datetime


def initialize(dev, log):
    global device, logger
    device       = dev
    logger       = log


def get_data():
    global message
    try:
        response = requests.get('https://ptsv2.com/t/8q32v-1585414405/d/latest/json')
        if response.status_code == requests.codes.ok:
            json_object = response.json()
            timestamp = json_object['Timestamp'].split('.')
            body = json.loads(json_object['Body'])
            temperature = int(body['temperature'])
            humidity = int(body['humidity'])
            message = str(temperature) + '*C - ' + str(humidity)
            logger.info('Internal measurement: ' + message)
        else:
            message = "NOT OK"
            logger.error('Invalid response code from ptsv API: ' + str(response.status_code))
    except requests.exceptions.RequestException as exception:
        logger.error(exception)
        message = "ERROR"


def display_temperature():
    global message
    get_data()
    device.show_message(message)


device       = None
logger       = None
message      = None
