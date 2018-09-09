import ZeroSeg.led as led
import buttonScript
import timeScript

device = led.sevensegment()
brightness = 3
device.brightness(brightness)
mode = 1  #clock

buttonScript.initialize(device, brightness)
timeScript.clock(device)
