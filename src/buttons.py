import ZeroSeg.led as led
import RPi.GPIO as GPIO
import time
import threading
import clock


def initialize(dev, btn_event):
    global device, button_event
    device = dev
    button_event = btn_event


# button which controls brightness
def button_1_listener(source):
    global brightness
    brightness += 2
    if brightness > 7:
        brightness = 1
    device.brightness(brightness)
    print("Button 1 pressed")


# button which controls current mode
def button_2_listener(source):
    print("Button 2 pressed")
    button_event.set()


BUTTON_1 = 17
BUTTON_2 = 26

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
GPIO.setup(BUTTON_1, GPIO.IN)
GPIO.setup(BUTTON_2, GPIO.IN)

GPIO.add_event_detect(BUTTON_1, GPIO.RISING, callback=button_1_listener, bouncetime=200)
GPIO.add_event_detect(BUTTON_2, GPIO.RISING, callback=button_2_listener, bouncetime=200)

brightness = 3
device = None
button_event = None

