from drivers.Motor import Motor
from services.SocketService import SocketService
from drivers.Connectors import (
    M1_IN3,
    M1_IN4,
    M1_PWM2,
    M2_IN1,
    M2_IN2,
    M2_PWM1,
    M3_IN1,
    M3_IN2,
    M3_PWM1,
    M4_IN3,
    M4_IN4,
    M4_PWM2,
)
import threading


PORT = 1060

COMMAND_STOP = "STOP"

COMMAND_FORWARD = "FORWARD"
COMMAND_BACKWARD = "BACKWARD"
COMMAND_LEFT = "LEFT"
COMMAND_RIGHT = "RIGHT"


class MotorsService(SocketService):
    def __init__(self):
        super().__init__(PORT)

        self.motorL1 = Motor(M2_IN2, M2_IN1, M2_PWM1)
        self.motorL2 = Motor(M1_IN4, M1_IN3, M1_PWM2)
        self.motorR1 = Motor(M3_IN2, M3_IN1, M3_PWM1)
        self.motorR2 = Motor(M4_IN4, M4_IN3, M4_PWM2)

    def runAction(self, action: str):
        action = action.upper()
        if action == COMMAND_FORWARD:
            self.forward()
        elif action == COMMAND_BACKWARD:
            self.backward()
        elif action == COMMAND_LEFT:
            self.left()
        elif action == COMMAND_RIGHT:
            self.right()
        elif action == COMMAND_STOP:
            self.stop()

    def forward(self):
        l1 = threading.Thread(target=self.motorL1.goForward)
        l2 = threading.Thread(target=self.motorL2.goForward)
        r1 = threading.Thread(target=self.motorR1.goForward)
        r2 = threading.Thread(target=self.motorR2.goForward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def backward(self):
        l1 = threading.Thread(target=self.motorL1.goBackward)
        l2 = threading.Thread(target=self.motorL2.goBackward)
        r1 = threading.Thread(target=self.motorR1.goBackward)
        r2 = threading.Thread(target=self.motorR2.goBackward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def left(self):
        l1 = threading.Thread(target=self.motorL1.goForward)
        l2 = threading.Thread(target=self.motorL2.goForward)
        r1 = threading.Thread(target=self.motorR1.goBackward)
        r2 = threading.Thread(target=self.motorR2.goBackward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def right(self):
        l1 = threading.Thread(target=self.motorL1.goBackward)
        l2 = threading.Thread(target=self.motorL2.goBackward)
        r1 = threading.Thread(target=self.motorR1.goForward)
        r2 = threading.Thread(target=self.motorR2.goForward)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()

    def stop(self):
        l1 = threading.Thread(target=self.motorL1.stop)
        l2 = threading.Thread(target=self.motorL2.stop)
        r1 = threading.Thread(target=self.motorR1.stop)
        r2 = threading.Thread(target=self.motorR2.stop)

        l1.start()
        l2.start()
        r1.start()
        r2.start()
        l1.join()
        l2.join()
        r1.join()
        r2.join()
