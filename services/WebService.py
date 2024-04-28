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

    def videoStream(self):
        while True:
            # 10 images /sec
            time.sleep(1 / CAMERA_FPS)
            frame, faces = CAMERA_SERVICE.getImageStream(
                WEB_PARAMETERS.enable_faces, WEB_PARAMETERS.identify_faces
            )
            if WEB_PARAMETERS.enable_center and len(faces) > 0:
                self.sendCommand(
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
        self.sendCommand(CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=-1))

    def camDown(self):
        self.sendCommand(CAMERA_SERVO_SERVICE, Command("move", hStep=0, vStep=1))

    def camLeft(self):
        self.sendCommand(CAMERA_SERVO_SERVICE, Command("move", hStep=-1, vStep=0))

    def camRight(self):
        self.sendCommand(CAMERA_SERVO_SERVICE, Command("move", hStep=1, vStep=0))

    def motorForward(self):
        self.sendCommand(MOTORS_SERVICE, Command("forward"))

    def motorBackwoard(self):
        self.sendCommand(MOTORS_SERVICE, Command("backward"))

    def motorLeft(self):
        self.sendCommand(MOTORS_SERVICE, Command("left"))

    def motorRight(self):
        self.sendCommand(MOTORS_SERVICE, Command("right"))

    def motorStop(self):
        self.sendCommand(MOTORS_SERVICE, Command("stop"))


WEB_SERVICE = WebService()