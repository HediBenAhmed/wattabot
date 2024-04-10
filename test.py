import time
from drivers.LED import LED, smile
from drivers.Servo import SERVO_CAMERA_H
from drivers.Ultrasonic import Ultrasonic
from drivers.Connectors import GPIO_TRIGGER, GPIO_ECHO
from gpiozero import DistanceSensor
from time import sleep

ultrasonic = Ultrasonic()
print(ultrasonic.getDistance())
from services.CameraService import CameraService

c = CameraService()
c.start()
