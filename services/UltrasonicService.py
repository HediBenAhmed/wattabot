import time
from drivers.Ultrasonic import USONIC
from drivers.Servo import USONIC_SERVO
from services.Service import Service


class UltrasonicService(Service):

    def getDistance(self):
        return USONIC.getDistance()

    def move(self, step):
        USONIC_SERVO.move(step)

    def consumeImg(self):
        while True:
            time.sleep(1 / 50)
            f = self.get("frame")
            print("consume", f)


USONIC_SERVICE = UltrasonicService("USONIC_SERVICE")
