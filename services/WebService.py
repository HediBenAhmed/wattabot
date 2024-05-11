import time

import cv2
import numpy as np
from drivers.Camera import CAMERA_FPS
from services.Command import Command
from services.CameraService import CAMERA_SERVICE

from services.CameraServoService import CAMERA_SERVO_SERVICE
from services.JobService import startJobInLoop, stopJobInLoop
from services.MotorsService import MOTORS_SERVICE
from services.Service import Service
from services.SharedData import getSharedData


class WebParameters:
    def __init__(self):
        self.enable_streaming = True
        self.identify_faces = False
        self.enable_center = False

        CAMERA_SERVICE.startStreaming("camera.frame")


WEB_PARAMETERS = WebParameters()


class WebService(Service):

    def videoStream(self):
        while True:
            time.sleep(1 / CAMERA_FPS)

            frame = getSharedData("camera.frame")
            _, buffer = cv2.imencode(
                ".jpeg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 10]
            )

            yield (
                b" --frame\r\n"
                b"Content-type: imgae/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

    def identifyFace(self):

        retry = 0
        face = None
        while True:
            retry += 1
            time.sleep(1 / CAMERA_FPS)

            frame = getSharedData("camera.frame")
            faces = CAMERA_SERVICE.scanFaces_dnn(frame)
            faces = CAMERA_SERVICE.identifyFaces_dnn(faces)

            face = CAMERA_SERVICE.getIdentifiedFace(faces)

            if face is not None:
                return face

            if retry > 10:
                return None

    def switchCamCentralizeFaces(self):
        WEB_PARAMETERS.enable_center = not WEB_PARAMETERS.enable_center

        if WEB_PARAMETERS.enable_center:
            startJobInLoop(self.centralizeFace, "centralizeFace", 1 / CAMERA_FPS)
        else:
            stopJobInLoop("centralizeFace")

    def camUp(self):
        CAMERA_SERVO_SERVICE.move(hStep=0, vStep=-1)

    def camDown(self):
        CAMERA_SERVO_SERVICE.move(hStep=0, vStep=1)

    def camLeft(self):
        CAMERA_SERVO_SERVICE.move(hStep=-1, vStep=0)

    def camRight(self):
        CAMERA_SERVO_SERVICE.move(hStep=1, vStep=0)

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

    def centralizeFace(self):
        frame = getSharedData("camera.frame")
        faces = CAMERA_SERVICE.scanFaces_dnn(frame)

        if len(faces) > 0:
            CAMERA_SERVO_SERVICE.centralizeFace(faces[0])


WEB_SERVICE = WebService("WEB_SERVICE")
