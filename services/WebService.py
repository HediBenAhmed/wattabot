import time

import cv2
from drivers.Camera import CAMERA_FPS
from feature.CameraControl import CameraControl
from feature.MotorsControl import MotorsControl
from services.CameraService import CameraService

from services.CameraServoService import CameraServoService
from services.JobService import (
    startJobInLoop,
    stopJobInLoop,
    getSharedData,
)
from services.Service import Service
from services.User import User

from feature.CameraStream import CameraStream
from feature.SystemInfo import SystemInfo


FEATURES = {
    "systemInfo": SystemInfo(),
    "cameraStream": CameraStream(),
    "cameraControl": CameraControl(),
    "motorsControl": MotorsControl(),
}


class WebParameters:
    def __init__(self):
        self.enable_streaming = True
        self.identify_faces = False
        self.enable_center = False


WEB_PARAMETERS = WebParameters()

NO_FRAME = cv2.imread("/home/hedi/wattabot/static/no-video-icon.png")


class WebService(Service):

    def videoStream(self):
        while True:
            time.sleep(1 / CAMERA_FPS)
            frame = getSharedData("camera.frame", 0)

            if frame is None:
                frame = NO_FRAME

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
            faces = CameraService.getInsance().scanFaces_dnn(frame)
            faces = CameraService.getInsance().identifyFaces_dnn(faces)

            face = CameraService.getInsance().getIdentifiedFace(faces)

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

    def centralizeFace(self):
        frame = getSharedData("camera.frame")
        faces = CameraService.getInsance().scanFaces_dnn(frame)

        if len(faces) > 0:
            CameraServoService.getInsance().centralizeFace(faces[0])

    def stop(self):
        print("EXIT ......................")
        for name, feature in FEATURES.items():
            print(feature)
            feature.stop()

    def init(self, user: User):
        print("INIT ......................")
        for feature in user.features:
            print(feature)
            if feature["autostart"] and feature["name"] in FEATURES:
                FEATURES[feature["name"]].start()

    def executeCommand(self, feature: str, action: str):
        if feature in FEATURES:
            FEATURES[feature].execute(action)

    @classmethod
    def createInstance(self):
        return WebService()
