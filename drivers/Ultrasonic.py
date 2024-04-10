import time
from drivers.Device import Device
from drivers.Connectors import GPIO_TRIGGER, GPIO_ECHO
import RPi.GPIO as GPIO


class Ultrasonic(Device):
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

    def reads(self):
        ret, frame = self.cap.read()

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
