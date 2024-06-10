from time import sleep
from drivers.Camera import CAMERA_FPS
from feature.Feature import Feature
from services.CameraServoService import CameraServoService
from services.FaceClassifierService import FaceClassfifierService
from services.JobService import getSharedData, startJobInLoop, stopJobInLoop


class FolowObject(Feature):

    def start(self):

        def job():
            sleep(1 / CAMERA_FPS)
            frame = getSharedData("camera.frame")
            faces = FaceClassfifierService.getInsance().idenfiyFaces(frame)

            if len(faces) > 0:
                CameraServoService.getInsance().centralizeFace(faces[0])

        thread, threadName = startJobInLoop(job=job, jobName="folowObject")

        if threadName is not None:
            self.threadName = threadName

    def stop(self):
        if self.threadName is not None:
            stopJobInLoop(self.threadName)

    def execute(self, action: str):
        if action == "START":
            self.start()
        elif action == "STOP":
            self.stop()

        return "folowObject {}".format(action)
