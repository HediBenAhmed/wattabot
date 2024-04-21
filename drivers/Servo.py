from drivers.Device import Device
import time

from gpiozero import Servo as GpServo
from gpiozero.pins.pigpio import PiGPIOFactory

from services.Configurations import connectorConfig

SERVO_MAX_VALUE = 0.7
SERVO_MIN_VALUE = -0.7


class Servo(Device):
    def __init__(self, servoPin: int):
        self.servo = GpServo(
            servoPin,
            min_pulse_width=0 / 1000,
            max_pulse_width=3 / 1000,
            pin_factory=PiGPIOFactory(),
        )

    def setValue(self, value: float):
        if value > SERVO_MAX_VALUE:
            value = SERVO_MAX_VALUE
        elif value < SERVO_MIN_VALUE:
            value = SERVO_MIN_VALUE

        delay = abs(abs(self.servo.value) - abs(value)) * 2
        self.servo.value = value
        time.sleep(delay)

    def move(self, step: float):
        if step == 0:
            return

        self.setValue(self.servo.value + step)


CAMERA_SERVO_H = Servo(connectorConfig("CAMERA_SERVO_H"))
CAMERA_SERVO_V = Servo(connectorConfig("CAMERA_SERVO_V"))
