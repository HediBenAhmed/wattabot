import time

import cv2
from drivers.Camera import CAMERA_FPS
from services.CameraService import CameraService

from services.CameraServoService import CameraServoService
from services.JobService import startJobInLoop, stopJobInLoop
from services.MotorsService import MotorsService
from services.Service import Service
from services.SharedData import getSharedData


class WebParameters:
    def __init__(self):
        self.enable_streaming = True
        self.identify_faces = False
        self.enable_center = False


WEB_PARAMETERS = WebParameters()


class WebService(Service):
    def __init__(self):
        self.CAMERA_SERVICE: CameraService = CameraService.getInsance()
        self.CAMERA_SERVICE.startStreaming("camera.frame")

        self.CAMERA_SERVO_SERVICE: CameraServoService = CameraServoService.getInsance()
        self.MOTORS_SERVICE: MotorsService = MotorsService.getInsance()

    def videoStream(self):
        while True:
            time.sleep(1 / CAMERA_FPS)

            frame = getSharedData("camera.frame")
            _, buffer = cv2.imencode(
                ".jpeg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50]
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
            faces = self.CAMERA_SERVICE.scanFaces_dnn(frame)
            faces = self.CAMERA_SERVICE.identifyFaces_dnn(faces)

            face = self.CAMERA_SERVICE.getIdentifiedFace(faces)

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
        self.CAMERA_SERVO_SERVICE.move(hStep=0, vStep=-2)

    def camDown(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=0, vStep=2)

    def camLeft(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=-2, vStep=0)

    def camRight(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=2, vStep=0)

    def camUpLeft(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=-2, vStep=-2)

    def camUpRight(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=2, vStep=-2)

    def camDownRight(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=2, vStep=2)

    def camDownLeft(self):
        self.CAMERA_SERVO_SERVICE.move(hStep=-2, vStep=2)

    def motorForward(self):
        self.MOTORS_SERVICE.forward()

    def motorBackwoard(self):
        self.MOTORS_SERVICE.backward()

    def motorLeft(self):
        self.MOTORS_SERVICE.left()

    def motorRight(self):
        self.MOTORS_SERVICE.right()

    def motorStop(self):
        self.MOTORS_SERVICE.stop()

    def centralizeFace(self):
        frame = getSharedData("camera.frame")
        faces = self.CAMERA_SERVICE.scanFaces_dnn(frame)

        if len(faces) > 0:
            self.CAMERA_SERVO_SERVICE.centralizeFace(faces[0])

    @classmethod
    def createInstance(self):
        return WebService()
