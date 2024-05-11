from time import sleep
from typing import List
from drivers.Ultrasonic import USONIC
from drivers.Servo import Servo
from services.Configurations import connectorConfig
from services.Object import Object, geObjectByDistance
from services.Service import Service

MAX_DISTANCE = 10000


class UltrasonicService(Service):

    def __init__(self):
        self.USONIC_SERVO = Servo(connectorConfig("USONIC_SERVO"))

    def getDistance(self, ndigits=0):
        min = MAX_DISTANCE
        for i in range(0, 10):
            d = USONIC.getDistance()
            min = d if d < min else min
            sleep(0.01)

        min = round(min, ndigits)
        return min

    def move(self, step):
        self.USONIC_SERVO.move(step / 100)

    def setPosition(self, x):
        self.USONIC_SERVO.setValue(x)

    def isMax(self):
        return self.USONIC_SERVO.getValue() >= self.USONIC_SERVO.maxValue

    def isMin(self):
        return self.USONIC_SERVO.getValue() <= self.USONIC_SERVO.minValue

    def scanObjectDistance(self):
        self.setPosition(self.USONIC_SERVO.minValue)
        objects: List[Object] = []
        while not self.isMax():
            self.move(step=4)
            distance = self.getDistance()
            position = self.USONIC_SERVO.getValue()

            existingObject = geObjectByDistance(objects, distance)
            if existingObject is not None:
                existingObject.addPosition(position)
            else:
                objects.append(Object(position, distance))

        objects.sort(key=lambda o: o.distance, reverse=False)

        return objects

    def findClearDirection(self):
        self.setPosition(0)
        forward = self.getDistance()

        self.setPosition(-1)
        right = self.getDistance()

        self.setPosition(1)
        left = self.getDistance()

        self.setPosition(0)

        diections = [(0, forward), (-1, right), (1, left)]

        return max(diections, key=lambda d: d[1])


USONIC_SERVICE = UltrasonicService()
