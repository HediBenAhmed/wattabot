from drivers.Device import Device
from drivers.Connectors import servoPin1, servoPin2, servoPin3
import time

from gpiozero import Servo as GpServo
from gpiozero.pins.pigpio import PiGPIOFactory


class Servo(Device):
    def __init__(self, servoPin: int):
        self.servo = GpServo(
            servoPin,
            min_pulse_width=0.5 / 1000,
            max_pulse_width=2.5 / 1000,
            pin_factory=PiGPIOFactory(),
        )

        self.servo.mid()
        self.currentAngle = 0
        time.sleep(1)

    def goToAngle(self, angle: float):
        delay = abs(abs(self.currentAngle) - abs(angle)) * 0.005
        print("go to ", angle, angle / 90, delay, "s")
        self.servo.value = angle / 90
        time.sleep(delay)
        self.currentAngle = angle


SERVO_CAMERA_H = Servo(servoPin3)
SERVO_CAMERA_V = Servo(servoPin2)
SERVO_ULTRASONIC = Servo(servoPin1)
