from drivers.Camera import CAMERA_HEIGHT, CAMERA_WIDTH
from drivers.Servo import (
    CAMERA_SERVO_H,
    CAMERA_SERVO_V,
    SERVO_MAX_VALUE,
    SERVO_MIN_VALUE,
)
import threading

from services import Command
from services.Face import Face
from services.ProcessManager import Status
from services.Service import Service

CENTER_OF_CAMERA = [CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2]
CENTER_MARGIN = [50, 50]


class CameraServoService(Service):
    def __init__(self):
        super().__init__("CAMERA_SERVO_SERVICE")
        self.moveCamera = False

    def getStatus(self):
        return CameraServoStatus(
            self.moveCamera,
            CAMERA_SERVO_H.getValue(),
            CAMERA_SERVO_V.getValue(),
            CAMERA_SERVO_H.getValue() >= SERVO_MAX_VALUE,
            CAMERA_SERVO_H.getValue() <= SERVO_MIN_VALUE,
            CAMERA_SERVO_V.getValue() >= SERVO_MAX_VALUE,
            CAMERA_SERVO_V.getValue() <= SERVO_MIN_VALUE,
        )

    def setPosition(self, x, y):
        self.moveCamera = True
        h = threading.Thread(target=CAMERA_SERVO_H.setValue, args=(x,))
        v = threading.Thread(target=CAMERA_SERVO_V.setValue, args=(y,))

        h.start()
        v.start()
        h.join()
        v.join()
        self.moveCamera = False

    def move(self, hStep, vStep):
        self.moveCamera = True
        h = threading.Thread(target=CAMERA_SERVO_H.move, args=(hStep / 100,))
        v = threading.Thread(target=CAMERA_SERVO_V.move, args=(vStep / 100,))

        h.start()
        v.start()
        h.join()
        v.join()
        self.moveCamera = False

    def centralizeFace(self, face: Face):
        moveTo = self.refFromCameraCenter(face.position)
        self.move(2 * moveTo[0], 2 * moveTo[1])

        return moveTo

    def refFromCameraCenter(self, facePosition):
        x, y, w, h = facePosition
        faceCenter = [x + w / 2, y + h / 2]
        direction = [0, 0]
        hDiff = faceCenter[0] - CENTER_OF_CAMERA[0]
        if abs(hDiff) < CENTER_MARGIN[0]:
            direction[0] = 0
        elif hDiff < 0:
            direction[0] = 1
        elif hDiff > 0:
            direction[0] = -1

        vDiff = faceCenter[1] - CENTER_OF_CAMERA[1]
        if abs(vDiff) < CENTER_MARGIN[1]:
            direction[1] = 0
        elif vDiff < 0:
            direction[1] = -1
        elif vDiff > 0:
            direction[1] = 1

        return direction

    def executeCommand(self, command: Command):
        if command.command == "setPosition":
            self.setPosition(command.parameters.get("x"), command.parameters.get("y"))
        elif command.command == "move":
            self.move(command.parameters.get("hStep"), command.parameters.get("vStep"))
        elif command.command == "centralizeFace":
            self.centralizeFace(command.parameters.get("face"))
        if command.command == "stop":
            self.stop()


class CameraServoStatus(Status):
    def __init__(
        self,
        cameraMoving: bool,
        hservo: float,
        vservo: float,
        hservoMax: bool,
        hservoMin: bool,
        vservoMax: bool,
        vservoMin: bool,
    ):
        self.cameraMoving = cameraMoving
        self.vservo = vservo
        self.hservo = hservo
        self.hservoMax = hservoMax
        self.hservoMin = hservoMin
        self.vservoMax = vservoMax
        self.vservoMin = vservoMin


CAMERA_SERVO_SERVICE = CameraServoService()
