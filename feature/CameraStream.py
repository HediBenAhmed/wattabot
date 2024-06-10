from time import sleep

from flask import json
from drivers.Camera import CAMERA_FPS
from feature.Feature import Feature
from services.CameraService import CameraService
from services.FaceClassifierService import FaceClassfifierService
from services.JobService import (
    getSharedData,
    setSharedData,
    startJobInLoop,
    stopJobInLoop,
)


class CameraStream(Feature):

    def start(self):

        def job():
            ref, frame = CameraService.getInsance().getImage()
            setSharedData("camera.frame", frame)
            sleep(1 / CAMERA_FPS)

        thread, threadName = startJobInLoop(job=job, jobName="streamImages")

        if threadName is not None:
            self.threadName = threadName

    def stop(self):
        if self.threadName is not None:
            stopJobInLoop(self.threadName)
        setSharedData("camera.frame", None)

    def execute(self, action: str):
        if action == "START":
            self.start()
        elif action == "STOP":
            self.stop()
        elif action == "IDENTIFY":
            face = self.identifyFace()

            result = None
            if face is not None:
                result = {"name": face.name, "confidence": face.confidence}

            return json.dumps(result)

        return "cameraStream {}".format(action)

    def identifyFace(self):

        retry = 0
        face = None
        while True:
            retry += 1
            sleep(1 / CAMERA_FPS)

            frame = getSharedData("camera.frame")
            faces = FaceClassfifierService.getInsance().idenfiyFaces(frame)
            faces = FaceClassfifierService.getInsance().reconizeFaces_dnn(faces)
            face = FaceClassfifierService.getInsance().getIdentifiedFace(faces)

            if face is not None:
                return face

            if retry > 5:
                return None
