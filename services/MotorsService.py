from drivers.Motor import MOTOR_L1, MOTOR_L2, MOTOR_R1, MOTOR_R2

from services.Command import Command
from services.Service import Service


class MotorsService(Service):

    def forward(self):
        commands = [
            (MOTOR_L1.goForward, ()),
            (MOTOR_L2.goForward, ()),
            (MOTOR_R1.goForward, ()),
            (MOTOR_R2.goForward, ()),
        ]

        self.executeTasks(commands)

    def backward(self):
        commands = [
            (MOTOR_L1.goBackward, ()),
            (MOTOR_L2.goBackward, ()),
            (MOTOR_R1.goBackward, ()),
            (MOTOR_R2.goBackward, ()),
        ]

        self.executeTasks(commands)

    def right(self):
        commands = [
            (MOTOR_L1.goForward, ()),
            (MOTOR_L2.goForward, ()),
            (MOTOR_R1.goBackward, ()),
            (MOTOR_R2.goBackward, ()),
        ]

        self.executeTasks(commands)

    def left(self):
        commands = [
            (MOTOR_L1.goBackward, ()),
            (MOTOR_L2.goBackward, ()),
            (MOTOR_R1.goForward, ()),
            (MOTOR_R2.goForward, ()),
        ]

        self.executeTasks(commands)

    def stop(self):
        commands = [
            (MOTOR_L1.stop, ()),
            (MOTOR_L2.stop, ()),
            (MOTOR_R1.stop, ()),
            (MOTOR_R2.stop, ()),
        ]

        self.executeTasks(commands)

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
