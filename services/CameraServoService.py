from drivers.Camera import CAMERA_HEIGHT, CAMERA_WIDTH
from drivers.Servo import Servo

from services.Configurations import connectorConfig
from services.Face import Face
from services.Service import Service

CENTER_OF_CAMERA = (CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2)
CENTER_MARGIN = (50, 50)


class CameraServoService(Service):
    def __init__(self):
        self.moveCamera = False
        self.CAMERA_SERVO_H = Servo(connectorConfig("CAMERA_SERVO_H"))
        self.CAMERA_SERVO_V = Servo(connectorConfig("CAMERA_SERVO_V"), -0.5, 0.2)

    def isHorizentalMax(self):
        return self.CAMERA_SERVO_H.getValue() >= self.CAMERA_SERVO_H.maxValue

    def isHorizentalMin(self):
        return self.CAMERA_SERVO_H.getValue() <= self.CAMERA_SERVO_H.minValue

    def isVerticalMax(self):
        return self.CAMERA_SERVO_V.getValue() >= self.CAMERA_SERVO_V.maxValue

    def isVerticalMin(self):
        return self.CAMERA_SERVO_V.getValue() <= self.CAMERA_SERVO_V.minValue

    def setPosition(self, x, y):
        self.moveCamera = True

        commands = [
            (self.CAMERA_SERVO_H.setValue, (x,)),
            (self.CAMERA_SERVO_V.setValue, (y,)),
        ]

        self.executeSubTasks(commands)

        self.moveCamera = False

    def move(self, hStep, vStep):
        self.moveCamera = True

        commands = [
            (self.CAMERA_SERVO_H.move, (hStep / 100,)),
            (self.CAMERA_SERVO_V.move, (vStep / 100,)),
        ]

        self.executeSubTasks(commands)

        self.moveCamera = False

    def centralizeFace(self, face: Face):
        h, v = self.refFromCameraCenter(face.position)
        self.move(2 * h, 2 * v)

        return h, v

    def refFromCameraCenter(self, facePosition):
        x, y, w, h = facePosition
        faceCenter = (x + w / 2, y + h / 2)
        hdirection = 0
        vdirection = 0
        hDiff = faceCenter[0] - CENTER_OF_CAMERA[0]
        vDiff = faceCenter[1] - CENTER_OF_CAMERA[1]

        if abs(hDiff) < CENTER_MARGIN[0]:
            hdirection = 0
        elif hDiff < 0:
            hdirection = 1
        elif hDiff > 0:
            hdirection = -1

        if abs(vDiff) < CENTER_MARGIN[1]:
            vdirection = 0
        elif vDiff < 0:
            vdirection = -1
        elif vDiff > 0:
            vdirection = 1

        return hdirection, vdirection


CAMERA_SERVO_SERVICE = CameraServoService()
