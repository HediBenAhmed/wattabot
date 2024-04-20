from drivers.Device import Device
import time

from gpiozero import Servo as GpServo
from gpiozero.pins.pigpio import PiGPIOFactory

from services.Configurations import connectorConfig


class Servo(Device):
    def __init__(self, servoPin: int):
        self.servo = GpServo(
            servoPin,
            min_pulse_width=0 / 1000,
            max_pulse_width=3 / 1000,
            pin_factory=PiGPIOFactory(),
        )

        self.servo.mid()
        self.currentAngle = 0
        time.sleep(1)

    def goToAngle(self, angle: float):
        delay = abs(abs(self.currentAngle) - abs(angle)) * 0.005
        newValue = angle / 90
        if newValue > 1 or newValue < -1:
            return

        self.servo.value = newValue
        time.sleep(delay)
        self.currentAngle = angle

    def move(self, direction: float):
        if direction == 0:
            return

        self.goToAngle(self.currentAngle + direction)


CAMERA_SERVO_H = Servo(connectorConfig("CAMERA_SERVO_H"))
CAMERA_SERVO_V = Servo(connectorConfig("CAMERA_SERVO_V"))
