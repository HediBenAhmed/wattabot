from time import sleep
from typing import List
from drivers.Ultrasonic import USONIC
from drivers.Servo import USONIC_SERVO
from services.Object import Object, geObjectByDistance
from services.Service import Service

MAX_DISTANCE = 10000


class UltrasonicService(Service):

    def getDistance(self):
        min = MAX_DISTANCE
        for i in range(0, 10):
            d = USONIC.getDistance()
            min = d if d < min else min
            sleep(0.01)

        return min

    def move(self, step):
        USONIC_SERVO.move(step / 100)

    def setPosition(self, x):
        USONIC_SERVO.setValue(x)

    def isMax(self):
        return USONIC_SERVO.getValue() >= USONIC_SERVO.maxValue

    def isMin(self):
        return USONIC_SERVO.getValue() <= USONIC_SERVO.minValue

    def scanObjectDistance(self):
        self.setPosition(USONIC_SERVO.minValue)
        objects: List[Object] = []
        while not self.isMax():
            self.move(step=4)
            distance = self.getDistance()
            position = USONIC_SERVO.getValue()

            existingObject = geObjectByDistance(objects, distance)
            if existingObject is not None:
                existingObject.addPosition(position)
            else:
                objects.append(Object(position, distance))

        objects.sort(key=lambda o: o.distance, reverse=False)

        return objects


USONIC_SERVICE = UltrasonicService("USONIC_SERVICE")
