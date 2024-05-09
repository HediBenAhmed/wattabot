from time import sleep
from drivers.Motor import Motor

from services.Command import Command
from services.Configurations import connectorConfig
from services.Service import Service


class MotorsService(Service):
    def __init__(self, name: str):
        super().__init__(name)

        self.MOTOR_L1 = Motor(
            connectorConfig("M2_IN1"),
            connectorConfig("M2_IN2"),
            connectorConfig("M2_PWM"),
        )
        self.MOTOR_L2 = Motor(
            connectorConfig("M1_IN1"),
            connectorConfig("M1_IN2"),
            connectorConfig("M1_PWM"),
        )
        self.MOTOR_R1 = Motor(
            connectorConfig("M3_IN1"),
            connectorConfig("M3_IN2"),
            connectorConfig("M3_PWM"),
        )
        self.MOTOR_R2 = Motor(
            connectorConfig("M4_IN1"),
            connectorConfig("M4_IN2"),
            connectorConfig("M4_PWM"),
        )

    def forward(self):
        commands = [
            (self.MOTOR_L1.goForward, ()),
            (self.MOTOR_L2.goForward, ()),
            (self.MOTOR_R1.goForward, ()),
            (self.MOTOR_R2.goForward, ()),
        ]

        self.executeSubTasks(commands)

    def backward(self):
        commands = [
            (self.MOTOR_L1.goBackward, ()),
            (self.MOTOR_L2.goBackward, ()),
            (self.MOTOR_R1.goBackward, ()),
            (self.MOTOR_R2.goBackward, ()),
        ]

        self.executeSubTasks(commands)

    def right(self):
        commands = [
            (self.MOTOR_L1.goForward, ()),
            (self.MOTOR_L2.goForward, ()),
            (self.MOTOR_R1.goBackward, ()),
            (self.MOTOR_R2.goBackward, ()),
        ]

        self.executeSubTasks(commands)

    def left(self):
        commands = [
            (self.MOTOR_L1.goBackward, ()),
            (self.MOTOR_L2.goBackward, ()),
            (self.MOTOR_R1.goForward, ()),
            (self.MOTOR_R2.goForward, ()),
        ]

        self.executeSubTasks(commands)

    def stop(self):
        commands = [
            (self.MOTOR_L1.stop, ()),
            (self.MOTOR_L2.stop, ()),
            (self.MOTOR_R1.stop, ()),
            (self.MOTOR_R2.stop, ()),
        ]

        self.executeSubTasks(commands)

    def setPosition(self, position):  # from -1 (0) to 1 (180), move 90° = 1 sec
        if position == 0:
            return

        delay = abs(position)

        if position > 0:
            self.right()
        else:
            self.left()

        sleep(delay)
        self.stop()

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


MOTORS_SERVICE = MotorsService("MOTORS_SERVICE")
