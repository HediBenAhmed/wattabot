from time import sleep
from drivers.Camera import CAMERA_FPS
from feature.Feature import Feature
from services.CameraService import CameraService
from services.JobService import setSharedData, startJobInLoop, stopJobInLoop


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
        stopJobInLoop(self.threadName)
        setSharedData("camera.frame", None)
