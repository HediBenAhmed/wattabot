from time import sleep
from feature.Feature import Feature
from services.JobService import startJobInLoop, stopJobInLoop
from services.MotorsService import MotorsService
from services.UltrasonicService import UltrasonicService

LIMIT = 10


class AutoMove(Feature):

    def start(self):

        def job():
            print("goooo")
            position, distance = UltrasonicService.getInsance().findClearDirection()
            print(position, distance)

            self.setDirection(position)

            self.move()

        thread, threadName = startJobInLoop(job=job, jobName="autoMove")

        if threadName is not None:
            self.threadName = threadName

    def stop(self):
        if self.threadName is not None:
            stopJobInLoop(self.threadName)

    def execute(self, action: str):
        if action == "START":
            self.start()
        elif action == "STOP":
            self.stop()

        return "autoMove {}".format(action)

    def setDirection(self, direction: float):

        if direction == 0:
            return

        if direction == 1:
            MotorsService.getInsance().left()
        elif direction == -1:
            MotorsService.getInsance().right()

        sleep(1.0)
        MotorsService.getInsance().stop()

    def move(self):
        moving = False
        previousDistance = 0
        while True:
            distance = UltrasonicService.getInsance().getDistance()
            print(distance)
            if distance > LIMIT and moving == False:
                moving = True
                MotorsService.getInsance().forward()

            if distance <= LIMIT or distance == previousDistance:
                break

            previousDistance = distance
        MotorsService.getInsance().stop()
