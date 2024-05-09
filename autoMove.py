from time import sleep
from services.MotorsService import MOTORS_SERVICE
from services.UltrasonicService import USONIC_SERVICE

LIMIT = 10


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
