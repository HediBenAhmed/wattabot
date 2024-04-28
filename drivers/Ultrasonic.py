import time
from drivers.Device import Device
from services.Configurations import connectorConfig
import RPi.GPIO as GPIO

GPIO_ECHO = connectorConfig("USONIC_ECHO")
GPIO_TRIGGER = connectorConfig("USONIC_TRIGGER")


class Ultrasonic(Device):
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

    def getDistance(self):
        # 10us is the trigger signal
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)  # 10us
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        while not GPIO.input(GPIO_ECHO):
            pass
        t1 = time.time()
        while GPIO.input(GPIO_ECHO):
            pass
        t2 = time.time()
        return ((t2 - t1) * 340 / 2) * 100


USONIC = Ultrasonic()
