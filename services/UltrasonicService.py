from drivers.Ultrasonic import USONIC
from drivers.Servo import USONIC_SERVO
from services.Service import Service


class UltrasonicService(Service):
    def __init__(self):
        super().__init__("USONIC_SERVICE")

    def getDistance(self):
        return USONIC.getDistance()

    def move(self, step):
        USONIC_SERVO.move(step)


USONIC_SERVICE = UltrasonicService()
