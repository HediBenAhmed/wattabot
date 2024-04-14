from drivers.Camera import Camera
from services.SocketService import SocketService
from drivers.Servo import Servo
from drivers.Connectors import servoPin2, servoPin3
import threading


PORT = 1050

COMMAND_STOP = "STOP"

COMMAND_UP = "UP"
COMMAND_DOWN = "DOWN"
COMMAND_LEFT = "LEFT"
COMMAND_RIGHT = "RIGHT"

COMMAND_UP_LEFT = "UP_LEFT"
COMMAND_DOWN_LEFT = "DOWN_LEFT"
COMMAND_UP_RIGHT = "UP_RIGHT"
COMMAND_DOWN_RIGHT = "DOWN_RIGHT"

COMMAND_SHOT = "SHOT"

COMMAND_RESET = "RESET"


class CameraService(SocketService):
    def __init__(self):
        super().__init__(PORT)
        self.servoCameraH = Servo(servoPin3)
        self.servoCameraV = Servo(servoPin2)
        self.camera = Camera()

    def runAction(self, action: str):
        action = action.upper()
        if action == COMMAND_UP:
            self.up()
        elif action == COMMAND_DOWN:
            self.down()
        elif action == COMMAND_LEFT:
            self.left()
        elif action == COMMAND_RIGHT:
            self.right()
        elif action == COMMAND_UP_LEFT:
            self.up_left()
        elif action == COMMAND_DOWN_LEFT:
            self.down_left()
        elif action == COMMAND_UP_RIGHT:
            self.up_right()
        elif action == COMMAND_DOWN_RIGHT:
            self.down_right()
        elif action == COMMAND_RESET:
            self.reset()
        elif action == COMMAND_STOP:
            self.stop()

        elif action == COMMAND_SHOT:
            return self.shot()

    def up(self):
        self.servoCameraV.move(-1)

    def down(self):
        self.servoCameraV.move(1)

    def left(self):
        self.servoCameraH.move(1)

    def right(self):
        self.servoCameraH.move(-1)

    def up_left(self):
        up = threading.Thread(target=self.up)
        left = threading.Thread(target=self.left)

        up.start()
        left.start()
        up.join()
        left.join()

    def up_right(self):
        up = threading.Thread(target=self.up)
        right = threading.Thread(target=self.right)

        up.start()
        right.start()
        up.join()
        right.join()

    def down_left(self):
        down = threading.Thread(target=self.down)
        left = threading.Thread(target=self.left)

        down.start()
        left.start()
        down.join()
        left.join()

    def down_right(self):
        down = threading.Thread(target=self.down)
        right = threading.Thread(target=self.right)

        down.start()
        right.start()
        down.join()
        right.join()

    def stop(self):
        self.servoCameraH.stop()
        self.servoCameraV.stop()

    def reset(self):
        self.servoCameraH.goToAngle(0)
        self.servoCameraV.goToAngle(0)

    def shot(self):
        return self.camera.getImage(False)
