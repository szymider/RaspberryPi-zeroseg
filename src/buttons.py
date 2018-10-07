import ZeroSeg.led as led
import RPi.GPIO as GPIO
from itertools import cycle
import time
import threading
import clock


def initialize(dev, btn_event):
    global device, button_event
    device = dev
    button_event = btn_event


# button which controls brightness
def button_1_listener(source):
    device.brightness(next(brightness))


# button which controls current mode
def button_2_listener(source):
    button_event.set()


BUTTON_1 = 17
BUTTON_2 = 26

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
GPIO.setup(BUTTON_1, GPIO.IN)
GPIO.setup(BUTTON_2, GPIO.IN)

GPIO.add_event_detect(BUTTON_1, GPIO.RISING, callback=button_1_listener, bouncetime=200)
GPIO.add_event_detect(BUTTON_2, GPIO.RISING, callback=button_2_listener, bouncetime=200)

brightness_list  = [5, 7, 1, 3]
brightness       = cycle(brightness_list)
device           = None
button_event     = None

