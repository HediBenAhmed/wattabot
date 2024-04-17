from drivers.Device import Device
import time

from gpiozero import Servo as GpServo
from gpiozero.pins.pigpio import PiGPIOFactory


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
        self.moving = False
        time.sleep(1)

    def goToAngle(self, angle: float):
        delay = abs(abs(self.currentAngle) - abs(angle)) * 0.005
        newValue = angle / 90
        if newValue > 1 or newValue < -1:
            self.stop()
            return

        self.servo.value = newValue
        time.sleep(delay)
        self.currentAngle = angle

    def move(self, direction: float, speed: float = 500):
        self.moving = True
        while self.moving:
            self.goToAngle(self.currentAngle + direction)
            time.sleep(1 / speed)

    def stop(self):
        self.moving = False
