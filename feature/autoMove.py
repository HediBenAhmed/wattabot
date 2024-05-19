from time import sleep
from services.MotorsService import MotorsService
from services.UltrasonicService import UltrasonicService

LIMIT = 10

MOTORS_SERVICE: MotorsService = MotorsService.getInsance()
USONIC_SERVICE: UltrasonicService = UltrasonicService.getInsance()


def moveTo(direction: float):

    if direction == 0:
        return

    if direction == 1:
        MOTORS_SERVICE.left()
    elif direction == -1:
        MOTORS_SERVICE.right()

    sleep(1.0)
    MOTORS_SERVICE.stop()


def move():
    moving = False
    previousDistance = 0
    while True:
        distance = USONIC_SERVICE.getDistance()
        print(distance)
        if distance > LIMIT and moving == False:
            moving = True
            MOTORS_SERVICE.forward()

        if distance <= LIMIT or distance == previousDistance:
            break

        previousDistance = distance
    MOTORS_SERVICE.stop()


if __name__ == "__main__":

    while True:
        position, distance = USONIC_SERVICE.findClearDirection()
        print(position, distance)

        moveTo(position)

        move()
