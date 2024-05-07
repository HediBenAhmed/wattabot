import time

import cv2
import numpy as np
from drivers.Camera import CAMERA_FPS
from services.Command import Command
from services.CameraService import CAMERA_SERVICE

from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.MotorsService import MOTORS_SERVICE
from services.Service import Service


class WebParameters:
    def __init__(self):
        self.enable_streaming = False
        self.enable_faces = False
        self.identify_faces = False
        self.enable_center = False


WEB_PARAMETERS = WebParameters()


class WebService(Service):

    def videoStream(self):
        while True:
            # 20 images /sec
            time.sleep(1 / CAMERA_FPS)

            streamBytes, faces = CAMERA_SERVICE.imageStream(
                WEB_PARAMETERS.identify_faces, 20
            )

            yield (
                b" --frame\r\n"
                b"Content-type: imgae/jpeg\r\n\r\n" + streamBytes + b"\r\n"
            )

            if WEB_PARAMETERS.enable_center and len(faces) > 0:
                CAMERA_SERVO_SERVICE.centralizeFace(faces[0])

    def switchIdentifyFaces(self):
        WEB_PARAMETERS.identify_faces = not WEB_PARAMETERS.identify_faces

    def switchCamCentralizeFaces(self):
        WEB_PARAMETERS.enable_center = not WEB_PARAMETERS.enable_center

    def camUp(self):
        CAMERA_SERVO_SERVICE.move(hStep=0, vStep=-1)

    def camDown(self):
        CAMERA_SERVO_SERVICE.move(hStep=0, vStep=1)

    def camLeft(self):
        CAMERA_SERVO_SERVICE.move(hStep=-1, vStep=0)

    def camRight(self):
        CAMERA_SERVO_SERVICE.move(hStep=1, vStep=0)

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


WEB_SERVICE = WebService("WEB_SERVICE")
