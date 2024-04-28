from drivers.Motor import MOTOR_L1, MOTOR_L2, MOTOR_R1, MOTOR_R2
import threading

from services.Command import Command
from services.Service import Service


class MotorsService(Service):
    def __init__(self):
        super().__init__("MOTORS_SERVICE")

    def forward(self):
        l1 = threading.Thread(target=MOTOR_L1.goForward)
        l2 = threading.Thread(target=MOTOR_L2.goForward)
        r1 = threading.Thread(target=MOTOR_R1.goForward)
        r2 = threading.Thread(target=MOTOR_R2.goForward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def backward(self):
        l1 = threading.Thread(target=MOTOR_L1.goBackward)
        l2 = threading.Thread(target=MOTOR_L2.goBackward)
        r1 = threading.Thread(target=MOTOR_R1.goBackward)
        r2 = threading.Thread(target=MOTOR_R2.goBackward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def right(self):
        l1 = threading.Thread(target=MOTOR_L1.goForward)
        l2 = threading.Thread(target=MOTOR_L2.goForward)
        r1 = threading.Thread(target=MOTOR_R1.goBackward)
        r2 = threading.Thread(target=MOTOR_R2.goBackward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def left(self):
        l1 = threading.Thread(target=MOTOR_L1.goBackward)
        l2 = threading.Thread(target=MOTOR_L2.goBackward)
        r1 = threading.Thread(target=MOTOR_R1.goForward)
        r2 = threading.Thread(target=MOTOR_R2.goForward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def stop(self):
        l1 = threading.Thread(target=MOTOR_L1.stop)
        l2 = threading.Thread(target=MOTOR_L2.stop)
        r1 = threading.Thread(target=MOTOR_R1.stop)
        r2 = threading.Thread(target=MOTOR_R2.stop)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def executeCommand(self, command: Command):
        if command.command == "forward":
            self.forward()
        elif command.command == "backward":
            self.backward()
        elif command.command == "left":
            self.left()
        elif command.command == "right":
            self.right()
        if command.command == "stop":
            self.stop()


MOTORS_SERVICE = MotorsService()
