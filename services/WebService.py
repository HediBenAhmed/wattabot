import time
from drivers.Camera import CAMERA_FPS
from services.Command import Command
from services.CameraService import CAMERA_SERVICE

from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.MotorsService import MOTORS_SERVICE
from services.Service import Service


class WebParameters:
    def __init__(self):
        self.enable_faces = False
        self.identify_faces = False
        self.enable_center = False


WEB_PARAMETERS = WebParameters()


class WebService(Service):
    def __init__(self):
        super().__init__("WEB_SERVICE")
        CAMERA_SERVO_SERVICE.startConsumer()

    def videoStream(self):
        while True:
            # 10 images /sec
            time.sleep(1 / CAMERA_FPS)
            frame, faces = CAMERA_SERVICE.getImageStream(
                WEB_PARAMETERS.enable_faces, WEB_PARAMETERS.identify_faces
            )
            if WEB_PARAMETERS.enable_center and len(faces) > 0:
                CAMERA_SERVICE.sendCommand(
                    CAMERA_SERVO_SERVICE, Command("centralizeFace", face=faces[0])
                )
            yield (
                b" --frame\r\n" b"Content-type: imgae/jpeg\r\n\r\n" + frame + b"\r\n"
            )

    def switchCamEnableFaces(self):
        WEB_PARAMETERS.enable_faces = not WEB_PARAMETERS.enable_faces

    def switchIdentifyFaces(self):
        WEB_PARAMETERS.identify_faces = not WEB_PARAMETERS.identify_faces

    def switchCamCentralizeFaces(self):
        WEB_PARAMETERS.enable_center = not WEB_PARAMETERS.enable_center

    def camUp(self):
        CAMERA_SERVICE.sendCommand(
            CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=-1)
        )

    def camDown(self):
        CAMERA_SERVICE.sendCommand(
            CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=1)
        )

    def camLeft(self):
        CAMERA_SERVICE.sendCommand(
            CAMERA_SERVO_SERVICE, Command("move", hStep=-1, vStep=0)
        )

    def camRight(self):
        CAMERA_SERVICE.sendCommand(
            CAMERA_SERVO_SERVICE, Command("move", hStep=1, vStep=0)
        )

    def motorForward(self):
        MOTORS_SERVICE.forward()

    def motorBackwoard(self):
        MOTORS_SERVICE.backward()

    def motorLeft(self):
        MOTORS_SERVICE.left()

    def motorRight(self):
        MOTORS_SERVICE.right()

    def motorStop(self):
        MOTORS_SERVICE.stop()


WEB_SERVICE = WebService()
