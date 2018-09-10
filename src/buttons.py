import ZeroSeg.led as led
import time
import threading
import RPi.GPIO as GPIO
import clock

BUTTON_1 = 17
BUTTON_2 = 26

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
GPIO.setup(BUTTON_1, GPIO.IN)
GPIO.setup(BUTTON_2, GPIO.IN)


def initialize(dev, bright):
    global device, brightness
    device = dev
    brightness = bright


# button which controls brightness
def button_1_listener(source):
    global brightness
    brightness += 2
    if brightness > 7:
        brightness = 1
    device.brightness(brightness)
    print("Button 1 pressed")


# button which control current display mode
def button_2_listener(source):
    print("Button 2 pressed")


GPIO.add_event_detect(BUTTON_1, GPIO.RISING, callback=button_1_listener, bouncetime=200)
GPIO.add_event_detect(BUTTON_2, GPIO.RISING, callback=button_2_listener, bouncetime=200)

device = None
brightness = None

